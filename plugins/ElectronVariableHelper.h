#ifndef _ELECTRONVARIABLEHELPER_H
#define _ELECTRONVARIABLEHELPER_H

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/Candidate/interface/Candidate.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

//#include "DataFormats/L1Trigger/interface/L1EmParticle.h"
//#include "DataFormats/L1Trigger/interface/L1EmParticleFwd.h"
#include "HLTrigger/HLTcore/interface/HLTFilter.h"
#include "DataFormats/L1Trigger/interface/EGamma.h"
#include "DataFormats/HLTReco/interface/TriggerFilterObjectWithRefs.h"
#include "CondFormats/L1TObjects/interface/L1CaloGeometry.h"
#include "CondFormats/DataRecord/interface/L1CaloGeometryRecord.h"

#include "DataFormats/Math/interface/deltaR.h"

#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"

#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/Candidate/interface/Candidate.h"

#include <DataFormats/PatCandidates/interface/Electron.h>

#include "DataFormats/EgammaCandidates/interface/Conversion.h"
#include "RecoEgamma/EgammaTools/interface/ConversionTools.h"

#include "TMath.h"

typedef edm::View<reco::Candidate> CandView;

template <class T>
class ElectronVariableHelper : public edm::EDProducer {
 public:
  explicit ElectronVariableHelper(const edm::ParameterSet & iConfig);
  virtual ~ElectronVariableHelper() ;

  virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup) override;

private:
  void store(const std::string &varName, std::vector<float> vals, edm::Handle<std::vector<T> > &probes, edm::Event &iEvent);

  edm::EDGetTokenT<std::vector<T> > probesToken_;
  edm::EDGetTokenT<reco::VertexCollection> vtxToken_;
  edm::EDGetTokenT<BXVector<l1t::EGamma> > l1EGToken_;
  edm::EDGetTokenT<CandView> pfCandToken_;
  edm::EDGetTokenT<reco::ConversionCollection> conversionsToken_;
  edm::EDGetTokenT<reco::BeamSpot> beamSpotToken_;
};

template<class T>
ElectronVariableHelper<T>::ElectronVariableHelper(const edm::ParameterSet & iConfig) :
  probesToken_(consumes<std::vector<T> >(iConfig.getParameter<edm::InputTag>("probes"))),
  vtxToken_(consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("vertexCollection"))),
  l1EGToken_(consumes<BXVector<l1t::EGamma> >(iConfig.getParameter<edm::InputTag>("l1EGColl"))),
  conversionsToken_(consumes<reco::ConversionCollection>(iConfig.getParameter<edm::InputTag>("conversions"))),
  beamSpotToken_(consumes<reco::BeamSpot>(iConfig.getParameter<edm::InputTag>("beamSpot"))) {

  produces<edm::ValueMap<float> >("dz");
  produces<edm::ValueMap<float> >("dxy");
  produces<edm::ValueMap<float> >("sip");
  produces<edm::ValueMap<float> >("missinghits");
  produces<edm::ValueMap<float> >("gsfhits");
  produces<edm::ValueMap<float> >("l1e");
  produces<edm::ValueMap<float> >("l1et");
  produces<edm::ValueMap<float> >("l1eta");
  produces<edm::ValueMap<float> >("l1phi");
  produces<edm::ValueMap<float> >("pfPt");
  produces<edm::ValueMap<float> >("convVtxFitProb");
  produces<edm::ValueMap<float> >("kfhits");
  produces<edm::ValueMap<float> >("kfchi2");
  produces<edm::ValueMap<float> >("ioemiop");
  produces<edm::ValueMap<float> >("5x5circularity");

  if( iConfig.existsAs<edm::InputTag>("pfCandColl") ) {
    pfCandToken_ = consumes<CandView>(iConfig.getParameter<edm::InputTag>("pfCandColl"));
  }

}

template<class T>
ElectronVariableHelper<T>::~ElectronVariableHelper()
{}

template<class T>
void ElectronVariableHelper<T>::store(const std::string &varName, std::vector<float> vals, edm::Handle<std::vector<T> > &probes, edm::Event &iEvent) {
  // convert into ValueMap and store
  std::unique_ptr<edm::ValueMap<float> > valMap(new edm::ValueMap<float>());
  edm::ValueMap<float>::Filler filler(*valMap);
  filler.insert(probes, vals.begin(), vals.end());
  filler.fill();
  iEvent.put(std::move(valMap), varName);
}

template<class T>
void ElectronVariableHelper<T>::produce(edm::Event & iEvent, const edm::EventSetup & iSetup) {

  // read input
  edm::Handle<std::vector<T> > probes;
  edm::Handle<reco::VertexCollection> vtxH;

  iEvent.getByToken(probesToken_, probes);
  iEvent.getByToken(vtxToken_, vtxH);
  const reco::VertexRef vtx(vtxH, 0);

  edm::Handle<BXVector<l1t::EGamma> > l1Cands;
  iEvent.getByToken(l1EGToken_, l1Cands);

  edm::Handle<reco::ConversionCollection> conversions;
  iEvent.getByToken(conversionsToken_, conversions);

  edm::Handle<reco::BeamSpot> beamSpotHandle;
  iEvent.getByToken(beamSpotToken_, beamSpotHandle);
  const reco::BeamSpot* beamSpot = &*(beamSpotHandle.product());

  edm::Handle<CandView> pfCands;
  if( !pfCandToken_.isUninitialized() ) iEvent.getByToken(pfCandToken_,pfCands);

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
    if( pfCands.isValid() )
    for( size_t ipf = 0; ipf < pfCands->size(); ++ipf ) {
        auto pfcand = pfCands->ptrAt(ipf);
    if( abs( pfcand->pdgId() ) != 11 ) continue;
    float dR = deltaR(pfcand->eta(), pfcand->phi() , probe->eta(), probe->phi());
    if( dR < 0.0001 ) pfpt = pfcand->pt();
    }

    l1EVals.push_back(l1e);
    l1EtVals.push_back(l1et);
    l1EtaVals.push_back(l1eta);
    l1PhiVals.push_back(l1phi);
    pfPtVals.push_back(pfpt);

    // Conversion vertex fit
    reco::ConversionRef convRef = ConversionTools::matchedConversion(*probe, conversions, beamSpot->position());

    float convVtxFitProb = -1.;
    if(!convRef.isNull()) {
        const reco::Vertex &vtx = convRef.get()->conversionVertex();
        if (vtx.isValid()) {
            convVtxFitProb = TMath::Prob( vtx.chi2(),  vtx.ndof());
        }
    }

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

  

  store("dz", dzVals, probes, iEvent);
  store("dxy", dxyVals, probes, iEvent);
  store("sip", sipVals, probes, iEvent);
  store("missinghits", mhVals, probes, iEvent);
  store("l1e", l1EVals, probes, iEvent);
  store("l1et", l1EtVals, probes, iEvent);
  store("l1eta", l1EtaVals, probes, iEvent);
  store("l1phi", l1PhiVals, probes, iEvent);
  store("pfPt", pfPtVals, probes, iEvent);
  store("convVtxFitProb", convVtxFitProbVals, probes, iEvent);
  store("kfhits", kfhitsVals, probes, iEvent);
  store("kfchi2", kfchi2Vals, probes, iEvent);
  store("ioemiop", ioemiopVals, probes, iEvent);
  store("5x5circularity", ocVals, probes, iEvent);


}

#endif
