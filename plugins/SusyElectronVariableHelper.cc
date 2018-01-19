#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/Candidate/interface/Candidate.h"

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "DataFormats/L1Trigger/interface/L1EmParticle.h"
#include "DataFormats/L1Trigger/interface/L1EmParticleFwd.h"

#include "DataFormats/Math/interface/deltaR.h"
#include "TMVA/Reader.h"

#include "FWCore/ParameterSet/interface/FileInPath.h"

#include "TMath.h"

namespace{
  template<typename T> void Store(edm::Event &iEvent, const edm::Handle<std::vector<pat::Electron>> &probes,
	                          const std::vector<T> &values, const std::string &name){
      std::unique_ptr<edm::ValueMap<T>> valMap(new edm::ValueMap<T>());
      typename edm::ValueMap<T>::Filler filler(*valMap);
      filler.insert(probes, values.begin(), values.end());
      filler.fill();
      iEvent.put(std::move(valMap), name);
  }

  // void StoreBoolToFloat(edm::Event &iEvent, const edm::Handle<std::vector<pat::Electron>> &probes,
  //                           const std::vector<bool> &valuesBool, const std::string &name){
  //     std::unique_ptr<edm::ValueMap<float>> valMap(new edm::ValueMap<float>());
  //     edm::ValueMap<float>::Filler filler(*valMap);
  //     std::vector<float> valuesFloat;
  //     for(bool value : valuesBool) valuesFloat.push_back( (float) value);
  //     filler.insert(probes, valuesFloat.begin(), valuesFloat.end());
  //     filler.fill();
  //     iEvent.put(std::move(valMap), name);
  // }

  bool PassMVAVLooseFO(double mva, double abssceta){
    if(abssceta<0.8)        return mva > -0.7;
    else if(abssceta<1.479) return mva > -0.83;
    else if(abssceta<2.5)   return mva > -0.92;
    else                    return false;
  }

  bool PassMVAVLoose(double mva, double abssceta){
    if(abssceta<0.8)        return mva > -0.16;
    else if(abssceta<1.479) return mva > -0.65;
    else if(abssceta<2.5)   return mva > -0.74;
    else                    return false;
  }

  bool PassMVATight(double mva, double abssceta){
    if(abssceta<0.8)        return mva > 0.87;
    else if(abssceta<1.479) return mva > 0.60;
    else if(abssceta<2.5)   return mva > 0.17;
    else                    return false;
  }

  bool PassMVAWP80(double mva, double abssceta){
    if(abssceta<0.8)        return mva > 0.988153;
    else if(abssceta<1.479) return mva > 0.967910;
    else if(abssceta<2.5)   return mva > 0.841729;
    else                    return false;
  }

  bool PassMVAWP90(double mva, double abssceta){
    if(abssceta<0.8)        return mva >  0.972153;
    else if(abssceta<1.479) return mva >  0.922126;
    else if(abssceta<2.5)   return mva >  0.610764;
    else                    return false;
  }

  bool PassTightIP2D(double dxy, double dz){
    return fabs(dxy) < 0.05 && fabs(dz) < 0.1;
  }

  bool PassIDEmu(const pat::Electron &ele){
    if(ele.isEB()){
      return ele.sigmaIetaIeta() < 0.011
	&& ele.hadronicOverEm() < 0.08
	&& fabs(ele.deltaEtaSuperClusterTrackAtVtx()) < 0.01
	&& fabs(ele.deltaPhiSuperClusterTrackAtVtx()) < 0.04
	&& fabs(1./ele.ecalEnergy() - ele.eSuperClusterOverP()/ele.ecalEnergy()) < 0.01;
    }else if(ele.isEE()){
      return ele.sigmaIetaIeta() < 0.031
	&& ele.hadronicOverEm() < 0.08
	&& fabs(ele.deltaEtaSuperClusterTrackAtVtx()) < 0.01
	&& fabs(ele.deltaPhiSuperClusterTrackAtVtx()) < 0.08
	&& fabs(1./ele.ecalEnergy() - ele.eSuperClusterOverP()/ele.ecalEnergy()) < 0.01;
    }else{
      return false;
    }
  }

  bool PassISOEmu(const pat::Electron &ele){
    return ele.ecalPFClusterIso() / ele.pt() < 0.45
      && ele.hcalPFClusterIso() / ele.pt() < 0.25
      && ele.dr03TkSumPt() / ele.pt() < 0.2;
  }

  // CMS coding rule number 1: be careful with POG recommended packages, especially when they were able to transform something
  // simple as a cut based id into a web of hundreds of python config files and are using bad coding standards
  // Therefore, simply implement the cut based id in a much more transparant way in the following 30 lines
  // Furthermore, we do not want the isolation cut, and you really don't want to mess with the EGamma code
  // Cuts based on: https://twiki.cern.ch/twiki/bin/viewauth/CMS/CutBasedElectronIdentificationRun2#Spring15_selection_25ns
  // Spring15, 25ns		         Veto B    Loose B   Medium B  Tight B    Veto E   Loose E   Medium E  Tight E
  std::vector<float> maxSigmaIetaIeta = {0.0114,   0.0103,   0.0101,   0.0101,    0.0352,  0.0301,   0.0283,   0.0279};
  std::vector<float> maxDEtaIn        = {0.0152,   0.0105,   0.0103,   0.00926,   0.0113,  0.00814,  0.00733,  0.00724};
  std::vector<float> maxDPhiIn        = {0.216,    0.115,    0.0336,   0.0336,    0.237,   0.182,    0.114,    0.0918};
  std::vector<float> maxHOverE        = {0.181,    0.104,    0.0876,   0.0597,    0.116,   0.0897,   0.0678,   0.0615};
  std::vector<float> maxOoEmooP       = {0.207,    0.102,    0.0174,   0.012,     0.174,   0.126,    0.0898,   0.00999};
  std::vector<float> maxd0            = {0.0564,   0.0261,   0.0118,   0.0111,    0.222,   0.118,    0.0739,   0.0351};
  std::vector<float> maxdz            = {0.472,    0.41,     0.373,    0.0466,    0.921,   0.822,    0.602,    0.417};
  std::vector<int>   maxMissingHits   = {2,        2,        2,        2,         3,       1,        1,        1};
  std::vector<bool>  convVeto         = {true,     true,     true,     true,      true,    true,     true,     true};

  bool PassCutBased(const pat::Electron &ele, float dxy, float dz, int missingHits, int level){
    if(ele.isEB())      level = level;
    else if(ele.isEE()) level = level + 4;
    else return false;

    float eInvMinusPInv = std::abs(1.0 - ele.eSuperClusterOverP())/ele.ecalEnergy();

    if(ele.full5x5_sigmaIetaIeta()               >= maxSigmaIetaIeta[level]) return false;
    if(abs(ele.deltaEtaSuperClusterTrackAtVtx()) >= maxDEtaIn[level])        return false;
    if(abs(ele.deltaPhiSuperClusterTrackAtVtx()) >= maxDPhiIn[level])        return false;
    if(ele.hadronicOverEm()                      >= maxHOverE[level])        return false;
    if(eInvMinusPInv                             >= maxOoEmooP[level])       return false;
    if(abs(dxy)                                  >= maxd0[level])            return false;
    if(abs(dz)                                   >= maxdz[level])            return false;
    if(missingHits                               >  maxMissingHits[level])   return false;
    if(convVeto[level] and not ele.passConversionVeto())                     return false;

    return true;
  }


  // On request of Deniz for her TTZ analysis, based on the (as usual to CMS standards) horrible code given here: https://github.com/peruzzim/cmgtools-lite/blob/76X_for2016basis/TTHAnalysis/python/tools/functionsTTH.py#L10-L20
  bool PassCutBasedTTZ(const pat::Electron &ele){
    float eInvMinusPInv = ele.ecalEnergy() > 0 ? (1.0/ele.ecalEnergy() - ele.eSuperClusterOverP()/ele.ecalEnergy()) : 9e9;
    if(ele.isEB()){
      if (ele.hadronicOverEm() >= 0.10)                    return false;
      if (abs(ele.deltaEtaSuperClusterTrackAtVtx())>=0.01) return false;
      if (abs(ele.deltaPhiSuperClusterTrackAtVtx())>=0.04) return false;
      if (eInvMinusPInv<=-0.05)                            return false;
      if (eInvMinusPInv>=0.01)                             return false;
      if (ele.full5x5_sigmaIetaIeta()>=0.011)              return false;
      return true;

    } else if(ele.isEE()){
      if (ele.hadronicOverEm() >= 0.07)                     return false;
      if (abs(ele.deltaEtaSuperClusterTrackAtVtx())>=0.008) return false;
      if (abs(ele.deltaPhiSuperClusterTrackAtVtx())>=0.07)  return false;
      if (eInvMinusPInv<=-0.05)                             return false;
      if (eInvMinusPInv>=0.005)                             return false;
      if (ele.full5x5_sigmaIetaIeta()>=0.03)                return false;
      return true;
    } else return false;
  }

  bool PassMultiIso(TString level, double mini_iso, double jetPtRatio, double jetPtRel){
    if(level == "VL") return mini_iso < 0.25 && (jetPtRatio > 0.67 || jetPtRel > 4.4);
    if(level == "L")  return mini_iso < 0.20 && (jetPtRatio > 0.69 || jetPtRel > 6.0);
    if(level == "M")  return mini_iso < 0.16 && (jetPtRatio > 0.76 || jetPtRel > 7.2);
    if(level == "T")  return mini_iso < 0.12 && (jetPtRatio > 0.80 || jetPtRel > 7.2);
    if(level == "VT") return mini_iso < 0.09 && (jetPtRatio > 0.84 || jetPtRel > 7.2);
    return false;
  }

  bool PassLeptonMva(TString level, double mva){
    if(level == "VL") return mva > -0.3;
    if(level == "L")  return mva > 0.25;
    if(level == "M")  return mva > 0.5;
    if(level == "T")  return mva > 0.65;
    if(level == "VT") return mva > 0.75;
    if(level == "ET") return mva > 0.85;
    return false;
  }
}



class SusyElectronVariableHelper : public edm::EDProducer {
public:
  explicit SusyElectronVariableHelper(const edm::ParameterSet & iConfig);
  virtual ~SusyElectronVariableHelper() ;
  
  virtual void beginJob();
  bool combine(std::map<TString, std::vector<bool>>& passWorkingPoints, std::vector<TString> wps);
  virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup) override;
  
private:
  edm::EDGetTokenT<std::vector<pat::Electron>> probesToken_;
  edm::EDGetTokenT<edm::View<reco::Candidate>> probesViewToken_;
  edm::EDGetTokenT<edm::ValueMap<float>> mvaToken_;
  edm::EDGetTokenT<edm::ValueMap<float>> dxyToken_;
  edm::EDGetTokenT<edm::ValueMap<float>> dzToken_;
  edm::EDGetTokenT<edm::ValueMap<float>> leptonMvaToken_;

  std::vector<TString> workingPoints;
};

SusyElectronVariableHelper::SusyElectronVariableHelper(const edm::ParameterSet & iConfig) :
  probesToken_(        consumes<std::vector<pat::Electron>>(iConfig.getParameter<edm::InputTag>("probes"))),
  probesViewToken_(    consumes<edm::View<reco::Candidate>>(iConfig.getParameter<edm::InputTag>("probes"))),
  mvaToken_(           consumes<edm::ValueMap<float>>(      iConfig.getParameter<edm::InputTag>("mvas"))),
  dxyToken_(           consumes<edm::ValueMap<float>>(      iConfig.getParameter<edm::InputTag>("dxy"))),
  dzToken_(            consumes<edm::ValueMap<float>>(      iConfig.getParameter<edm::InputTag>("dz"))),
  leptonMvaToken_(     consumes<edm::ValueMap<float>>(      iConfig.getParameter<edm::InputTag>("leptonMvas"))){

    produces<edm::ValueMap<float> >("sip3d");

    workingPoints = {"ConvVeto", "MVAVLooseFO", "MVAVLoose", "Mini", "Mini2", "Mini4",
		     "MVAVLooseMini", "MVAVLooseMini2", "MVAVLooseMini4", "MVATight", "MVAWP80", "MVAWP90",
		     "TightIP2D", "TightIP3D", "IDEmu", "ISOEmu", "Charge", "IHit0", "IHit1", "Loose2D",
		     "FOID2D", "Tight2D3D", "TightID2D3D", "ConvIHit0", "TightConvIHit0", "ConvIHit1", "ConvIHit0Chg",
		     "MultiIsoM", "MultiIsoT", "MultiIsoVT", "MultiIsoEmu", "LeptonMvaM", "LeptonMvaVT",
		     "CutBasedVeto", "CutBasedLoose", "CutBasedMedium", "CutBasedTight",
		     "CutBasedMediumMini", "CutBasedTightMini", "CutBasedTTZ", "CutBasedIllia", "CutBasedStopsDilepton",
		     "LeptonMvaVTIDEmuTightIP2DSIP3D8miniIso04", "LeptonMvaMIDEmuTightIP2DSIP3D8miniIso04"};

    for(TString wp : workingPoints) produces<edm::ValueMap<bool>>(("pass" + wp).Data());
}

SusyElectronVariableHelper::~SusyElectronVariableHelper(){
}

void SusyElectronVariableHelper::beginJob(){
    
}

// Combine workingpoints
bool SusyElectronVariableHelper::combine(std::map<TString, std::vector<bool>>& passWorkingPoints, std::vector<TString> wps){
    for(TString wp : wps) if(!passWorkingPoints[wp].back()) return false;
    return true;
}


void SusyElectronVariableHelper::produce(edm::Event & iEvent, const edm::EventSetup & iSetup) {
  // read input
  edm::Handle<std::vector<pat::Electron>> probes;      iEvent.getByToken(probesToken_,         probes);
  edm::Handle<edm::View<reco::Candidate>> probes_view; iEvent.getByToken(probesViewToken_,     probes_view);
  edm::Handle<edm::ValueMap<float>> mvas;              iEvent.getByToken(mvaToken_,            mvas);
  edm::Handle<edm::ValueMap<float>> dxys;              iEvent.getByToken(dxyToken_,            dxys);
  edm::Handle<edm::ValueMap<float>> dzs;               iEvent.getByToken(dzToken_,             dzs);
  edm::Handle<edm::ValueMap<float>> leptonMvas;        iEvent.getByToken(leptonMvaToken_,      leptonMvas);

  // prepare vector for output
  std::vector<float> sip3dValues;


  std::map<TString, std::vector<bool>> passWorkingPoints;
  for(TString wp : workingPoints) passWorkingPoints[wp] = std::vector<bool>();

  size_t i = 0;
  for(const auto &probe: *probes){
    edm::RefToBase<reco::Candidate> pp = probes_view->refAt(i);

    float ip3d             = probe.dB(pat::Electron::PV3D);
    float ip3d_err         = probe.edB(pat::Electron::PV3D);
    float sip3d            = ip3d/ip3d_err;
    float mva              = (*mvas)[pp];
    float dxy              = (*dxys)[pp];
    float dz               = (*dzs)[pp];
    float mini_iso         = probe.userFloat("miniIsoAll")/probe.pt();
    float jetPtRatio       = probe.userFloat("ptRatio");
    float jetPtRel         = probe.userFloat("ptRel");
    int   missingInnerHits   = probe.gsfTrack()->hitPattern().numberOfAllHits(reco::HitPattern::MISSING_INNER_HITS);
    float leptonMva        = (*leptonMvas)[pp];


    sip3dValues.push_back(sip3d);

    passWorkingPoints["ConvVeto"].push_back(      probe.passConversionVeto());
    passWorkingPoints["MVAVLooseFO"].push_back(   PassMVAVLooseFO(mva, fabs(probe.superCluster()->eta())));
    passWorkingPoints["MVAVLoose"].push_back(     PassMVAVLoose(  mva, fabs(probe.superCluster()->eta())));
    passWorkingPoints["MVATight"].push_back(      PassMVATight(   mva, fabs(probe.superCluster()->eta())));
    passWorkingPoints["MVAWP80"].push_back(       PassMVAWP80(    mva, fabs(probe.superCluster()->eta())));
    passWorkingPoints["MVAWP90"].push_back(       PassMVAWP90(    mva, fabs(probe.superCluster()->eta())));
    passWorkingPoints["TightIP2D"].push_back(     PassTightIP2D(dxy, dz));
    passWorkingPoints["TightIP3D"].push_back(     fabs(sip3d) < 4.);
    passWorkingPoints["SIP3D4"].push_back(        fabs(sip3d) < 4.);
    passWorkingPoints["SIP3D8"].push_back(        fabs(sip3d) < 8.);
    passWorkingPoints["Mini"].push_back(          mini_iso < 0.1);
    passWorkingPoints["Mini2"].push_back(         mini_iso < 0.2);
    passWorkingPoints["Mini4"].push_back(         mini_iso < 0.4);
    passWorkingPoints["IDEmu"].push_back(         PassIDEmu(probe));
    passWorkingPoints["ISOEmu"].push_back(        PassISOEmu(probe));
    passWorkingPoints["Charge"].push_back(        probe.isGsfCtfScPixChargeConsistent());
    passWorkingPoints["IHit0"].push_back(         missingInnerHits == 0);
    passWorkingPoints["IHit1"].push_back(         missingInnerHits <= 1);
    passWorkingPoints["MultiIsoM"].push_back(     PassMultiIso("M",  mini_iso, jetPtRatio, jetPtRel));
    passWorkingPoints["MultiIsoT"].push_back(     PassMultiIso("T",  mini_iso, jetPtRatio, jetPtRel));
    passWorkingPoints["MultiIsoVT"].push_back(    PassMultiIso("VT", mini_iso, jetPtRatio, jetPtRel));
    passWorkingPoints["LeptonMvaM"].push_back(    PassLeptonMva("M",  leptonMva));
    passWorkingPoints["LeptonMvaVT"].push_back(   PassLeptonMva("VT", leptonMva));
    passWorkingPoints["CutBasedVeto"].push_back(  PassCutBased(probe, dxy, dz, missingInnerHits, 0));
    passWorkingPoints["CutBasedLoose"].push_back( PassCutBased(probe, dxy, dz, missingInnerHits, 1));
    passWorkingPoints["CutBasedMedium"].push_back(PassCutBased(probe, dxy, dz, missingInnerHits, 2));
    passWorkingPoints["CutBasedTight"].push_back( PassCutBased(probe, dxy, dz, missingInnerHits, 3));

    passWorkingPoints["MVAVLooseMini"].push_back(                           combine(passWorkingPoints, {"MVAVLoose", "Mini"}));
    passWorkingPoints["MVAVLooseMini2"].push_back(                          combine(passWorkingPoints, {"MVAVLoose", "Mini2"}));
    passWorkingPoints["MVAVLooseMini4"].push_back(                          combine(passWorkingPoints, {"MVAVLoose", "Mini4"}));
    passWorkingPoints["Loose2D"].push_back(                                 combine(passWorkingPoints, {"MVAVLoose", "TightIP2D"}));
    passWorkingPoints["FOID2D"].push_back(                                  combine(passWorkingPoints, {"MVAVLooseFO", "IDEmu", "TightIP2D"}));
    passWorkingPoints["Tight2D3D"].push_back(                               combine(passWorkingPoints, {"MVATight", "TightIP2D", "SIP3D4"}));
    passWorkingPoints["TightID2D3D"].push_back(                             combine(passWorkingPoints, {"MVATight", "IDEmu", "TightIP2D", "SIP3D4"}));
    passWorkingPoints["CutBasedStopsDilepton"].push_back(                   combine(passWorkingPoints, {"CutBasedTight", "TightIP2D", "SIP3D4"}));
    passWorkingPoints["ConvIHit1"].push_back(                               combine(passWorkingPoints, {"ConvVeto","IHit1"}));
    passWorkingPoints["ConvIHit0"].push_back(                               combine(passWorkingPoints, {"ConvVeto","IHit0"}));
    passWorkingPoints["ConvIHit0Chg"].push_back(                            combine(passWorkingPoints, {"ConvIHit0", "Charge"}));
    passWorkingPoints["TightConvIHit0"].push_back(                          combine(passWorkingPoints, {"Tight2D3D", "ConvVeto","IHit0"}));
    passWorkingPoints["MultiIsoEmu"].push_back(                             combine(passWorkingPoints, {"MultiIsoT", "ISOEmu"}));
    passWorkingPoints["CutBasedMediumMini"].push_back(                      combine(passWorkingPoints, {"CutBasedMedium", "Mini"}));
    passWorkingPoints["CutBasedTightMini"].push_back(                       combine(passWorkingPoints, {"CutBasedTight", "Mini"}));
    passWorkingPoints["CutBasedTTZ"].push_back(                             combine(passWorkingPoints, {"CutBasedMedium","TightIP2D", "SIP3D4"}) and PassCutBasedTTZ(probe));
    passWorkingPoints["CutBasedIllia"].push_back(                           combine(passWorkingPoints, {"CutBasedTTZ", "Charge"}));
    passWorkingPoints["LeptonMvaVTIDEmuTightIP2DSIP3D8miniIso04"].push_back(combine(passWorkingPoints, {"LeptonMvaVT", "IDEmu", "TightIP2D", "SIP3D8", "Mini4"}));
    passWorkingPoints["LeptonMvaMIDEmuTightIP2DSIP3D8miniIso04"].push_back( combine(passWorkingPoints, {"LeptonMvaM", "IDEmu", "TightIP2D", "SIP3D8", "Mini4"}));

    ++i;
  }

  Store(iEvent, probes, sip3dValues, "sip3d");

  for(TString wp : workingPoints){
    Store(iEvent, probes, passWorkingPoints[wp], ("pass" + wp).Data());
  }
}


#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(SusyElectronVariableHelper);
