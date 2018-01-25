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



typedef edm::View<reco::Candidate> CandView;

template <class T>
class ElectronVariableHelper : public edm::EDProducer {
 public:
  explicit ElectronVariableHelper(const edm::ParameterSet & iConfig);
  virtual ~ElectronVariableHelper() ;
  
  virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup) override;
  
private:
  edm::EDGetTokenT<std::vector<T> > probesToken_;
  edm::EDGetTokenT<reco::VertexCollection> vtxToken_;
  edm::EDGetTokenT<BXVector<l1t::EGamma> > l1EGTkn;
  edm::EDGetTokenT<CandView> pfCandToken_;
};

template<class T>
ElectronVariableHelper<T>::ElectronVariableHelper(const edm::ParameterSet & iConfig) :
  probesToken_(consumes<std::vector<T> >(iConfig.getParameter<edm::InputTag>("probes"))),
  vtxToken_(consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("vertexCollection"))),
  l1EGTkn(consumes<BXVector<l1t::EGamma> >(iConfig.getParameter<edm::InputTag>("l1EGColl"))) {

  produces<edm::ValueMap<float> >("chi2");
  produces<edm::ValueMap<float> >("dz");
  produces<edm::ValueMap<float> >("dxy");
  produces<edm::ValueMap<float> >("missinghits");
  produces<edm::ValueMap<float> >("l1e");
  produces<edm::ValueMap<float> >("l1et");
  produces<edm::ValueMap<float> >("l1eta");
  produces<edm::ValueMap<float> >("l1phi");
  produces<edm::ValueMap<float> >("pfPt");

  if( iConfig.existsAs<edm::InputTag>("pfCandColl") ) {
    pfCandToken_ = consumes<CandView>(iConfig.getParameter<edm::InputTag>("pfCandColl"));
  }

}

template<class T>
ElectronVariableHelper<T>::~ElectronVariableHelper()
{}

template<class T>
void ElectronVariableHelper<T>::produce(edm::Event & iEvent, const edm::EventSetup & iSetup) {

  // read input
  edm::Handle<std::vector<T> > probes;
  edm::Handle<reco::VertexCollection> vtxH;
  
  iEvent.getByToken(probesToken_, probes);
  iEvent.getByToken(vtxToken_, vtxH);
  const reco::VertexRef vtx(vtxH, 0);

  edm::Handle<BXVector<l1t::EGamma> > l1Cands;
  iEvent.getByToken(l1EGTkn, l1Cands);
  
  edm::Handle<CandView> pfCands;
  if( !pfCandToken_.isUninitialized() ) iEvent.getByToken(pfCandToken_,pfCands);
  
  // prepare vector for output
  std::vector<float> chi2Vals;
  std::vector<float> dzVals;
  std::vector<float> dxyVals;
  std::vector<float> mhVals;
  std::vector<float> l1EVals;
  std::vector<float> l1EtVals;
  std::vector<float> l1EtaVals;
  std::vector<float> l1PhiVals;
  std::vector<float> pfPtVals;

  typename std::vector<T>::const_iterator probe, endprobes = probes->end();

  for (probe = probes->begin(); probe != endprobes; ++probe) {
    
    chi2Vals.push_back(probe->gsfTrack()->normalizedChi2());
    dzVals.push_back(probe->gsfTrack()->dz(vtx->position()));
    dxyVals.push_back(probe->gsfTrack()->dxy(vtx->position()));
    mhVals.push_back(float(probe->gsfTrack()->hitPattern().numberOfLostHits(reco::HitPattern::MISSING_INNER_HITS)));

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
    
  }

  
  // convert into ValueMap and store
  std::unique_ptr<edm::ValueMap<float> > chi2ValMap(new edm::ValueMap<float>());
  edm::ValueMap<float>::Filler chi2Filler(*chi2ValMap);
  chi2Filler.insert(probes, chi2Vals.begin(), chi2Vals.end());
  chi2Filler.fill();
  iEvent.put(std::move(chi2ValMap), "chi2");

  std::unique_ptr<edm::ValueMap<float> > dzValMap(new edm::ValueMap<float>());
  edm::ValueMap<float>::Filler dzFiller(*dzValMap);
  dzFiller.insert(probes, dzVals.begin(), dzVals.end());
  dzFiller.fill();
  iEvent.put(std::move(dzValMap), "dz");

  std::unique_ptr<edm::ValueMap<float> > dxyValMap(new edm::ValueMap<float>());
  edm::ValueMap<float>::Filler dxyFiller(*dxyValMap);
  dxyFiller.insert(probes, dxyVals.begin(), dxyVals.end());
  dxyFiller.fill();
  iEvent.put(std::move(dxyValMap), "dxy");

  std::unique_ptr<edm::ValueMap<float> > mhValMap(new edm::ValueMap<float>());
  edm::ValueMap<float>::Filler mhFiller(*mhValMap);
  mhFiller.insert(probes, mhVals.begin(), mhVals.end());
  mhFiller.fill();
  iEvent.put(std::move(mhValMap), "missinghits");

  std::unique_ptr<edm::ValueMap<float> > l1EValMap(new edm::ValueMap<float>());
  edm::ValueMap<float>::Filler l1EFill(*l1EValMap);
  l1EFill.insert(probes, l1EVals.begin(), l1EVals.end());
  l1EFill.fill();
  iEvent.put(std::move(l1EValMap), "l1e");

  std::unique_ptr<edm::ValueMap<float> > l1EtValMap(new edm::ValueMap<float>());
  edm::ValueMap<float>::Filler l1EtFill(*l1EtValMap);
  l1EtFill.insert(probes, l1EtVals.begin(), l1EtVals.end());
  l1EtFill.fill();
  iEvent.put(std::move(l1EtValMap), "l1et");

  std::unique_ptr<edm::ValueMap<float> > l1EtaValMap(new edm::ValueMap<float>());
  edm::ValueMap<float>::Filler l1EtaFill(*l1EtaValMap);
  l1EtaFill.insert(probes, l1EtaVals.begin(), l1EtaVals.end());
  l1EtaFill.fill();
  iEvent.put(std::move(l1EtaValMap), "l1eta");

  std::unique_ptr<edm::ValueMap<float> > l1PhiValMap(new edm::ValueMap<float>());
  edm::ValueMap<float>::Filler l1PhiFill(*l1PhiValMap);
  l1PhiFill.insert(probes, l1PhiVals.begin(), l1PhiVals.end());
  l1PhiFill.fill();
  iEvent.put(std::move(l1PhiValMap), "l1phi");

  std::unique_ptr<edm::ValueMap<float> > pfPtValMap(new edm::ValueMap<float>());
  edm::ValueMap<float>::Filler pfPtFill(*pfPtValMap);
  pfPtFill.insert(probes, pfPtVals.begin(), pfPtVals.end());
  pfPtFill.fill();
  iEvent.put(std::move(pfPtValMap), "pfPt");

  
}

#endif
