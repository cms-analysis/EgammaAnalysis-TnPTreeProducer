#ifndef _ELECTRONVARIABLEHELPER_H
#define _ELECTRONVARIABLEHELPER_H

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/ValueMap.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "DataFormats/L1Trigger/interface/L1EmParticle.h"
#include "DataFormats/L1Trigger/interface/L1EmParticleFwd.h"
#include "DataFormats/L1Trigger/interface/EGamma.h"
#include "DataFormats/HLTReco/interface/TriggerFilterObjectWithRefs.h"

#include "DataFormats/Math/interface/deltaR.h"

#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/Candidate/interface/Candidate.h"

#include <DataFormats/PatCandidates/interface/Electron.h>

#include "DataFormats/EgammaCandidates/interface/Conversion.h"
#include "RecoEgamma/EgammaTools/interface/ConversionTools.h"

#include "EgammaAnalysis/TnPTreeProducer/plugins/WriteValueMap.h"
#include "EgammaAnalysis/TnPTreeProducer/plugins/isolations.h"

#include "TMath.h"


template <class T>
class ElectronVariableHelper : public edm::EDProducer {
 public:
  explicit ElectronVariableHelper(const edm::ParameterSet & iConfig);
  virtual ~ElectronVariableHelper() ;

  virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup) override;

private:
  edm::EDGetTokenT<std::vector<T> > probesToken_;
  edm::EDGetTokenT<reco::VertexCollection> vtxToken_;
  edm::EDGetTokenT<BXVector<l1t::EGamma> > l1EGToken_;
  edm::EDGetTokenT<reco::ConversionCollection> conversionsToken_;
  edm::EDGetTokenT<reco::BeamSpot> beamSpotToken_;
  edm::EDGetTokenT<edm::View<reco::Candidate>> pfCandidatesToken_;

  bool isMiniAODformat;
};

template<class T>
ElectronVariableHelper<T>::ElectronVariableHelper(const edm::ParameterSet & iConfig) :
  probesToken_(consumes<std::vector<T> >(iConfig.getParameter<edm::InputTag>("probes"))),
  vtxToken_(consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("vertexCollection"))),
  l1EGToken_(consumes<BXVector<l1t::EGamma> >(iConfig.getParameter<edm::InputTag>("l1EGColl"))),
  conversionsToken_(consumes<reco::ConversionCollection>(iConfig.getParameter<edm::InputTag>("conversions"))),
  beamSpotToken_(consumes<reco::BeamSpot>(iConfig.getParameter<edm::InputTag>("beamSpot"))),
  pfCandidatesToken_(consumes<edm::View<reco::Candidate>>(iConfig.getParameter<edm::InputTag>("pfCandidates"))){

  produces<edm::ValueMap<float>>("dz");
  produces<edm::ValueMap<float>>("dxy");
  produces<edm::ValueMap<float>>("sip");
  produces<edm::ValueMap<float>>("missinghits");
  produces<edm::ValueMap<float>>("gsfhits");
  produces<edm::ValueMap<float>>("l1e");
  produces<edm::ValueMap<float>>("l1et");
  produces<edm::ValueMap<float>>("l1eta");
  produces<edm::ValueMap<float>>("l1phi");
  produces<edm::ValueMap<float>>("pfPt");
  produces<edm::ValueMap<float>>("convVtxFitProb");
  produces<edm::ValueMap<float>>("kfhits");
  produces<edm::ValueMap<float>>("kfchi2");
  produces<edm::ValueMap<float>>("ioemiop");
  produces<edm::ValueMap<float>>("5x5circularity");
  produces<edm::ValueMap<float>>("pfLeptonIsolation");
  produces<edm::ValueMap<float>>("hasMatchedConversion");

  isMiniAODformat = true;
}

template<class T>
ElectronVariableHelper<T>::~ElectronVariableHelper()
{}


template<class T>
void ElectronVariableHelper<T>::produce(edm::Event & iEvent, const edm::EventSetup & iSetup) {

  // read input
  edm::Handle<std::vector<T>> probes;
  edm::Handle<reco::VertexCollection> vtxH;

  iEvent.getByToken(probesToken_, probes);
  iEvent.getByToken(vtxToken_, vtxH);
  const reco::VertexRef vtx(vtxH, 0);

  edm::Handle<BXVector<l1t::EGamma>> l1Cands;
  iEvent.getByToken(l1EGToken_, l1Cands);

  edm::Handle<reco::ConversionCollection> conversions;
  iEvent.getByToken(conversionsToken_, conversions);

  edm::Handle<reco::BeamSpot> beamSpotHandle;
  iEvent.getByToken(beamSpotToken_, beamSpotHandle);
  const reco::BeamSpot* beamSpot = &*(beamSpotHandle.product());

  edm::Handle<edm::View<reco::Candidate>> pfCandidates;
  iEvent.getByToken(pfCandidatesToken_, pfCandidates);

  // prepare vector for output
  std::vector<float> dzVals;
  std::vector<float> dxyVals;
  std::vector<float> sipVals;
  std::vector<float> mhVals;

  std::vector<float> l1EVals;
  std::vector<float> l1EtVals;
  std::vector<float> l1EtaVals;
  std::vector<float> l1PhiVals;
  std::vector<float> pfPtVals;
  std::vector<float> convVtxFitProbVals;
  std::vector<float> kfhitsVals;
  std::vector<float> kfchi2Vals;
  std::vector<float> ioemiopVals;
  std::vector<float> ocVals;

  std::vector<float> gsfhVals;

  std::vector<float> hasMatchedConversionVals;

  typename std::vector<T>::const_iterator probe, endprobes = probes->end();

  for (probe = probes->begin(); probe != endprobes; ++probe) {

    //---Clone the pat::Electron
    pat::Electron l((pat::Electron)*probe);

    dzVals.push_back(probe->gsfTrack()->dz(vtx->position()));
    dxyVals.push_back(probe->gsfTrack()->dxy(vtx->position()));

    // SIP
    float IP      = fabs(l.dB(pat::Electron::PV3D));
    float IPError = l.edB(pat::Electron::PV3D);
    sipVals.push_back(IP/IPError);

    mhVals.push_back(float(probe->gsfTrack()->hitPattern().numberOfLostHits(reco::HitPattern::MISSING_INNER_HITS)));
    gsfhVals.push_back(float(probe->gsfTrack()->hitPattern().trackerLayersWithMeasurement()));
    float l1e = 999999.;    
    float l1et = 999999.;
    float l1eta = 999999.;
    float l1phi = 999999.;
    float pfpt = 999999.;
    float dRmin = 0.3;

    for (std::vector<l1t::EGamma>::const_iterator l1Cand = l1Cands->begin(0); l1Cand != l1Cands->end(0); ++l1Cand) {

      float dR = deltaR(l1Cand->eta(), l1Cand->phi() , probe->superCluster()->eta(), probe->superCluster()->phi());
      if (dR < dRmin) {
        dRmin = dR;
        l1e = l1Cand->energy();
        l1et = l1Cand->et();
        l1eta = l1Cand->eta();
        l1phi = l1Cand->phi();
      }
    }

    for( size_t ipf = 0; ipf < pfCandidates->size(); ++ipf ) {
      auto pfcand = pfCandidates->ptrAt(ipf);
      if(abs(pfcand->pdgId()) != 11) continue;
      float dR = deltaR(pfcand->eta(), pfcand->phi(), probe->eta(), probe->phi());
      if(dR < 0.0001) pfpt = pfcand->pt();
    }

    l1EVals.push_back(l1e);
    l1EtVals.push_back(l1et);
    l1EtaVals.push_back(l1eta);
    l1PhiVals.push_back(l1phi);
    pfPtVals.push_back(pfpt);

    // Store hasMatchedConversion (currently stored as float instead of bool, as it allows to implement it in the same way as other variables)
    #if (CMSSW_MAJOR_VERSION>=10 && CMSSW_MINOR_VERSION>=4) || (CMSSW_MAJOR_VERSION>=11)
    hasMatchedConversionVals.push_back((float)ConversionTools::hasMatchedConversion(*probe, *conversions, beamSpot->position()));
    #else
    hasMatchedConversionVals.push_back((float)ConversionTools::hasMatchedConversion(*probe, conversions, beamSpot->position()));
    #endif

    // Conversion vertex fit
    float convVtxFitProb = -1.;

    #if (CMSSW_MAJOR_VERSION>=10 && CMSSW_MINOR_VERSION>=4) || (CMSSW_MAJOR_VERSION>=11)
    reco::Conversion const* convRef = ConversionTools::matchedConversion(*probe,*conversions, beamSpot->position());
    if(!convRef==0) {
        const reco::Vertex &vtx = convRef->conversionVertex();
        if (vtx.isValid()) {
            convVtxFitProb = TMath::Prob( vtx.chi2(),  vtx.ndof());
        }
    }
    #else
    reco::ConversionRef convRef = ConversionTools::matchedConversion(*probe, conversions, beamSpot->position());
    if(!convRef.isNull()) {
        const reco::Vertex &vtx = convRef.get()->conversionVertex();
        if (vtx.isValid()) {
            convVtxFitProb = TMath::Prob( vtx.chi2(),  vtx.ndof());
        }
    }
    #endif
    convVtxFitProbVals.push_back(convVtxFitProb);


    // kf track related variables
    bool validKf=false;
    reco::TrackRef trackRef = probe->closestCtfTrackRef();
    validKf = trackRef.isAvailable();
    validKf &= trackRef.isNonnull();
    float kfchi2 = validKf ? trackRef->normalizedChi2() : 0 ; //ielectron->track()->normalizedChi2() : 0 ;
    float kfhits = validKf ? trackRef->hitPattern().trackerLayersWithMeasurement() : -1. ;

    kfchi2Vals.push_back(kfchi2);
    kfhitsVals.push_back(kfhits);

    // 5x5circularity
    float oc = probe->full5x5_e5x5() != 0. ? 1. - (probe->full5x5_e1x5() / probe->full5x5_e5x5()) : -1.;
    ocVals.push_back(oc);

    // 1/E - 1/p
    float ele_pin_mode  = probe->trackMomentumAtVtx().R();
    float ele_ecalE     = probe->ecalEnergy();
    float ele_IoEmIop   = -1;
    if(ele_ecalE != 0 || ele_pin_mode != 0) {
        ele_IoEmIop = 1.0 / ele_ecalE - (1.0 / ele_pin_mode);
    }

    ioemiopVals.push_back(ele_IoEmIop);
  }

  // convert into ValueMap and store
  writeValueMap(iEvent, probes, dzVals, "dz");
  writeValueMap(iEvent, probes, dxyVals, "dxy");
  writeValueMap(iEvent, probes, sipVals, "sip");
  writeValueMap(iEvent, probes, mhVals, "missinghits");
  writeValueMap(iEvent, probes, gsfhVals, "gsfhits");
  writeValueMap(iEvent, probes, l1EVals, "l1e");
  writeValueMap(iEvent, probes, l1EtVals, "l1et");
  writeValueMap(iEvent, probes, l1EtaVals, "l1eta");
  writeValueMap(iEvent, probes, l1PhiVals, "l1phi");
  writeValueMap(iEvent, probes, pfPtVals, "pfPt");
  writeValueMap(iEvent, probes, convVtxFitProbVals, "convVtxFitProb");
  writeValueMap(iEvent, probes, kfhitsVals, "kfhits");
  writeValueMap(iEvent, probes, kfchi2Vals, "kfchi2");
  writeValueMap(iEvent, probes, ioemiopVals, "ioemiop");
  writeValueMap(iEvent, probes, ocVals, "5x5circularity");
  writeValueMap(iEvent, probes, hasMatchedConversionVals, "hasMatchedConversion");

  // PF lepton isolations (will only work in miniAOD)
  if(isMiniAODformat){
    try {
      auto pfLeptonIsolations = computePfLeptonIsolations(*probes, *pfCandidates);
      for(unsigned int i = 0; i < probes->size(); ++i){
	pfLeptonIsolations[i] /= (*probes)[i].pt();
      }
      writeValueMap(iEvent, probes, pfLeptonIsolations, "pfLeptonIsolation");
    } catch (std::bad_cast){
      isMiniAODformat = false;
    }
  }
}

#endif
