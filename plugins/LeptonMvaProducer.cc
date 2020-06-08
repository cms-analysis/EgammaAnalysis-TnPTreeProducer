#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/Candidate/interface/Candidate.h"

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

#include "FWCore/Utilities/interface/Exception.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"
#include "EgammaAnalysis/TnPTreeProducer/plugins/WriteValueMap.h"
#include "TMVA/Reader.h"

#include <algorithm>
#include <string>
#include <fstream>
#include <iostream>
#include <iomanip>

/*
 * LeptonMvaProducer class definition
 */
class LeptonMvaProducer : public edm::EDProducer {
  public:
    explicit LeptonMvaProducer(const edm::ParameterSet & iConfig);
    virtual ~LeptonMvaProducer(){};

    virtual void beginJob();
    virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup) override;

  private:
    std::string                                                   leptonMvaType_;
    std::string                                                   weightFileName_;
    edm::EDGetTokenT<std::vector<pat::Electron>>                  probesToken_;
    edm::EDGetTokenT<edm::View<reco::Candidate>>                  probesViewToken_;
    edm::EDGetTokenT<edm::ValueMap<reco::CandidatePtr>>           closestJetToken_;
    std::map<std::string, edm::EDGetTokenT<edm::ValueMap<float>>> floatTokens_;
    bool                                                          debug_;

    std::map<std::string, float> inputValues;
    TMVA::Reader *reader;
};



/*
 * LeptonMvaProducer constructor
 */
LeptonMvaProducer::LeptonMvaProducer(const edm::ParameterSet & iConfig) :
  leptonMvaType_(                                                  iConfig.getParameter<std::string>("leptonMvaType")),
  weightFileName_(                                                 iConfig.getParameter<edm::FileInPath>("weightFile").fullPath()),
  probesToken_(        consumes<std::vector<pat::Electron>>(       iConfig.getParameter<edm::InputTag>("probes"))),
  probesViewToken_(    consumes<edm::View<reco::Candidate>>(       iConfig.getParameter<edm::InputTag>("probes"))),
  closestJetToken_(    consumes<edm::ValueMap<reco::CandidatePtr>>(iConfig.getParameter<edm::InputTag>("closestJet"))),
  debug_(                                                          iConfig.getParameter<bool>("debug"))
{
    // This dirty code simply finds all the float inputs in the parameterset (the only ones having ":" in their InputTag except closestJet)
    // and automatically initializes the floatTokens
    for(std::string param : iConfig.getParameterNames()){
      if(iConfig.getParameterAsString(param).find(':') != std::string::npos and param!="closestJet"){
        floatTokens_[param] = consumes<edm::ValueMap<float>>(iConfig.getParameter<edm::InputTag>(param));
      }
    }
    produces<edm::ValueMap<float>>(leptonMvaType_);
    produces<edm::ValueMap<float>>("closestJetDeepCsv");
    produces<edm::ValueMap<float>>("closestJetDeepFlavour");
}



/*
 * Begin job: initialize the TMVA reader [variables are automatically read from xml]
 */
void LeptonMvaProducer::beginJob(){
  reader = new TMVA::Reader("!Color:!Silent");

  std::ifstream file(weightFileName_);
  std::string line;
  while (std::getline(file, line)){
    if(line.find("VarIndex") == std::string::npos) continue;
    std::size_t start = line.find("Expression=\"")+12;
    std::size_t end   = line.find("\" Label");
    std::string var   = line.substr(start, end-start);
    reader->AddVariable(var, &inputValues[var]);
  }

  reader->BookMVA("BDTG method", weightFileName_.c_str());
}



/*
 * Produce function for each event
 */
void LeptonMvaProducer::produce(edm::Event & iEvent, const edm::EventSetup & iSetup) {
  edm::Handle<std::vector<pat::Electron>> probes;            iEvent.getByToken(probesToken_,         probes);
  edm::Handle<edm::View<reco::Candidate>> probes_view;       iEvent.getByToken(probesViewToken_,     probes_view);
  edm::Handle<edm::ValueMap<reco::CandidatePtr>> closestJet; iEvent.getByToken(closestJetToken_,     closestJet);

  // Loading in all the floats into floats[varName][eleIndex]
  // This might look a bit like over-engineering, but you know mva people like to change variables all the time
  // so in this way we avoid everytime manually changing the handles stuff etc...
  std::map<int, std::map<std::string, float>> floatsForAllProbes;
  for(auto& it : floatTokens_){
    edm::Handle<edm::ValueMap<float>> handle;
    iEvent.getByToken(it.second, handle);
    for(size_t i=0; i<(*probes).size();++i){
      edm::RefToBase<reco::Candidate> pp = probes_view->refAt(i);
      floatsForAllProbes[i][it.first] = (*handle)[pp];
    }
  }

  std::vector<float> leptonMvaValues;
  std::vector<float> closestJetDeepCsvValues;
  std::vector<float> closestJetDeepFlavourValues;

  size_t i = 0;
  for(const auto &probe: *probes){
    edm::RefToBase<reco::Candidate> pp = probes_view->refAt(i);
    auto& floats = floatsForAllProbes[i];

    float deepFlavour = 0;
    float deepCsv = 0;
    if(((*closestJet)[pp]).isNonnull()){
      const pat::Jet* jet = reinterpret_cast<const pat::Jet*>(((*closestJet)[pp]).get());
      float probb    = jet->bDiscriminator("pfDeepFlavourJetTags:probb");
      float probbb   = jet->bDiscriminator("pfDeepFlavourJetTags:probbb");
      float problepb = jet->bDiscriminator("pfDeepFlavourJetTags:problepb");
      deepFlavour    = std::isnan(probb+probbb+problepb) ? 0. :  std::max(probb+probbb+problepb, (float)0.);

      probb   = jet->bDiscriminator("pfDeepCSVJetTags:probb");
      probbb  = jet->bDiscriminator("pfDeepCSVJetTags:probbb");
      deepCsv = std::isnan(probb+probbb) ? 0. :  std::max(probb+probbb, (float)0.);
    }

    // If you need a new leptonMvaType, you can implement the mapping of the variables here:
    if(leptonMvaType_=="leptonMvaTTH"){
      inputValues["LepGood_pt"]                   = pp->pt();
      inputValues["LepGood_eta"]                  = pp->eta();
      inputValues["LepGood_jetNDauChargedMVASel"] = floats["jetNDauChargedMVASel"];
      inputValues["LepGood_miniRelIsoCharged"]    = floats["miniIsoChg"];
      inputValues["LepGood_miniRelIsoNeutral"]    = floats["miniIsoAll"] - floats["miniIsoChg"];
      inputValues["LepGood_jetPtRelv2"]           = floats["ptRel"];
      inputValues["LepGood_jetDF"]                = deepFlavour;
      inputValues["LepGood_jetPtRatio"]           = std::min(floats["ptRatio"],(float)1.5);
      inputValues["LepGood_dxy"]                  = log(fabs(probe.dB(pat::Electron::PV2D)));
      inputValues["LepGood_sip3d"]                = fabs(probe.dB(pat::Electron::PV3D)/probe.edB(pat::Electron::PV3D));
      inputValues["LepGood_dz"]                   = log(fabs(probe.dB(pat::Electron::PVDZ)));
      inputValues["LepGood_mvaFall17V2noIso"]     = floats["mvas"];
    } else if(leptonMvaType_=="leptonMvaGhent"){
      inputValues["pt"]                     = pp->pt();
      inputValues["eta"]                    = fabs(pp->eta());
      inputValues["trackMultClosestJet"]    = floats["jetNDauChargedMVASel"];
      inputValues["miniIsoCharged"]         = floats["miniIsoChg"];
      inputValues["miniIsoNeutral"]         = floats["miniIsoAll"] - floats["miniIsoChg"];
      inputValues["pTRel"]                  = floats["ptRel"];
      inputValues["relIso"]                 = floats["PFIsoAll"];
      inputValues["deepCsvClosestJet"]      = deepCsv;
      inputValues["ptRatio"]                = std::min(floats["ptRatio"],(float)1.5);
      inputValues["dxy"]                    = log(fabs(probe.dB(pat::Electron::PV2D)));
      inputValues["sip3d"]                  = fabs(probe.dB(pat::Electron::PV3D)/probe.edB(pat::Electron::PV3D));
      inputValues["dz"]                     = log(fabs(probe.dB(pat::Electron::PVDZ)));
      inputValues["electronMvaSpring16GP"]  = floats["mvas"]; // because these names actually differ given on the training
      inputValues["electronMvaFall17NoIso"] = floats["mvas"];
    } else if(leptonMvaType_=="leptonMvaTOP"){
      inputValues["pt"]                     = pp->pt();
      inputValues["etaAbs"]                 = fabs(pp->eta());
      inputValues["trackMultClosestJet"]    = floats["jetNDauChargedMVASel"];
      inputValues["miniIsoCharged"]         = floats["miniIsoChg"];
      inputValues["miniIsoNeutral"]         = floats["miniIsoAll"] - floats["miniIsoChg"];
      inputValues["pTRel"]                  = floats["ptRel"];
      inputValues["relIso"]                 = floats["PFIsoAll"];
      inputValues["bTagDeepJetClosestJet"]  = deepFlavour;
      inputValues["ptRatio"]                = std::min(floats["ptRatio"],(float)1.5);
      inputValues["dxylog"]                 = log(fabs(probe.dB(pat::Electron::PV2D)));
      inputValues["sip3d"]                  = fabs(probe.dB(pat::Electron::PV3D)/probe.edB(pat::Electron::PV3D));
      inputValues["dzlog"]                  = log(fabs(probe.dB(pat::Electron::PVDZ)));
      inputValues["mvaIdFall17v2noIso"]     = floats["mvas"];
    } else {
      throw cms::Exception("unknownLeptonMvaType") << "Please add " << leptonMvaType_ << " definitions to " << __FILE__ << " at line " <<  __LINE__;
    }


    float leptonMva = reader->EvaluateMVA("BDTG method");
    leptonMvaValues.push_back(leptonMva);
    closestJetDeepCsvValues.push_back(deepCsv);
    closestJetDeepFlavourValues.push_back(deepFlavour);

    if(debug_){
      for(auto& pair : inputValues) std::cout << std::left << std::setw(30) << pair.first << "\t" << pair.second << std::endl;
      std::cout << "--> " << std::left << std::setw(26) << leptonMvaType_ << "\t" << leptonMva << std::endl << std::endl << std::endl;
    }

    ++i;
  }

  writeValueMap(iEvent, probes, leptonMvaValues, leptonMvaType_);
  writeValueMap(iEvent, probes, closestJetDeepCsvValues, "closestJetDeepCsv");
  writeValueMap(iEvent, probes, closestJetDeepFlavourValues, "closestJetDeepFlavour");
}


#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(LeptonMvaProducer);
