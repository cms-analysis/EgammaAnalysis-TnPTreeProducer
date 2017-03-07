#ifndef _SCVARIABLEHELPER_H
#define _SCVARIABLEHELPER_H

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/Candidate/interface/Candidate.h"

#include "DataFormats/RecoCandidate/interface/RecoEcalCandidate.h"
#include "RecoEgamma/EgammaHLTAlgos/interface/EgammaHLTTrackIsolation.h"

template <class T>
class SCVariableHelper : public edm::EDProducer {
 public:
  explicit SCVariableHelper(const edm::ParameterSet & iConfig);
  virtual ~SCVariableHelper() ;
  
  virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup) override;
  
private:
  const edm::EDGetTokenT<std::vector<T> > probesToken_;
  const edm::EDGetTokenT<reco::TrackCollection> trackProducer_;

  const bool countTracks_;
  
  const double trkIsoPtMin_; 
  const double trkIsoConeSize_;
  const double trkIsoZSpan_;   
  const double trkIsoRSpan_;  
  const double trkIsoVetoConeSize_;
  const double trkIsoStripBarrel_;
  const double trkIsoStripEndcap_;
  
  EgammaHLTTrackIsolation* isoCalculator_;
};

template<class T>
SCVariableHelper<T>::SCVariableHelper(const edm::ParameterSet & iConfig) :
probesToken_(consumes<std::vector<T> >(iConfig.getParameter<edm::InputTag>("probes"))),
  trackProducer_       (consumes<reco::TrackCollection>(iConfig.getParameter<edm::InputTag>("trackProducer"))),
  countTracks_         (iConfig.getParameter<bool>("countTracks")),
  trkIsoPtMin_       (iConfig.getParameter<double>("trkIsoPtMin")),
  trkIsoConeSize_    (iConfig.getParameter<double>("trkIsoConeSize")),
  trkIsoZSpan_       (iConfig.getParameter<double>("trkIsoZSpan")),
  trkIsoRSpan_       (iConfig.getParameter<double>("trkIsoRSpan")),
  trkIsoVetoConeSize_(iConfig.getParameter<double>("trkIsoVetoConeSize")),
  trkIsoStripBarrel_ (iConfig.getParameter<double>("trkIsoStripBarrel")),
  trkIsoStripEndcap_ (iConfig.getParameter<double>("trkIsoStripEndcap")) {
  
  isoCalculator_ = new EgammaHLTTrackIsolation(trkIsoPtMin_, trkIsoConeSize_,
					       trkIsoZSpan_, trkIsoRSpan_, trkIsoVetoConeSize_,
					       trkIsoStripBarrel_, trkIsoStripEndcap_);
  
  produces<edm::ValueMap<float> >("scTkIso");
}

template<class T>
SCVariableHelper<T>::~SCVariableHelper()
{}

template<class T>
void SCVariableHelper<T>::produce(edm::Event & iEvent, const edm::EventSetup & iSetup) {

  // read input
  edm::Handle<std::vector<T> > probes;
  iEvent.getByToken(probesToken_,  probes);

  edm::Handle<reco::TrackCollection> trackHandle;
  iEvent.getByToken(trackProducer_, trackHandle);
  const reco::TrackCollection* trackCollection = trackHandle.product();

  // prepare vector for output
  std::vector<float> scIsoValues;
  
  typename std::vector<T>::const_iterator probe, endprobes = probes->end();
  
  for (probe = probes->begin(); probe != endprobes; ++probe) {
    
    float isol;
    if (countTracks_) {
      isol = isoCalculator_->photonTrackCount(&(*probe), trackCollection, false);
    } else {
      isol = isoCalculator_->photonPtSum(&(*probe), trackCollection, false);
    }
    
    scIsoValues.push_back(isol);
  }

  
  // convert into ValueMap and store
  std::auto_ptr<edm::ValueMap<float> > scIsoValMap(new edm::ValueMap<float>());
  edm::ValueMap<float>::Filler scIsoFiller(*scIsoValMap);
  scIsoFiller.insert(probes, scIsoValues.begin(), scIsoValues.end());
  scIsoFiller.fill();
  iEvent.put(scIsoValMap, "scTkIso");
}

#endif
