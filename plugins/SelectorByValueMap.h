#ifndef SelectorByValueMap_h
#define SelectorByValueMap_h

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Common/interface/Handle.h"

#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

#include "DataFormats/RecoCandidate/interface/RecoEcalCandidate.h"
#include "DataFormats/RecoCandidate/interface/RecoEcalCandidateFwd.h"

#include "DataFormats/EgammaReco/interface/SuperCluster.h"
#include "DataFormats/EgammaReco/interface/SuperClusterFwd.h"

#include <vector>
#include <string>

template <typename C>
struct CompatibleConfigurationType {
  typedef C type;
};
    
// "float" is not allowed, as it conflicts with "double"
template <>
struct CompatibleConfigurationType<float> {
  typedef double type;
};
  
template <typename T, typename C>
class SelectorByValueMap : public edm::EDProducer {
public:
  explicit SelectorByValueMap(edm::ParameterSet const & config);
  
private:
  typedef T candidate_type;
  typedef C selection_type;
  typedef typename CompatibleConfigurationType<selection_type>::type cut_type;
  typedef std::vector<candidate_type> candidateCollection;
  typedef edm::Ref<candidateCollection> candidateRef;
  typedef edm::RefVector<candidateCollection> candidateRefVector;
  
  void produce(edm::Event & event, edm::EventSetup const & setup);
  reco::RecoEcalCandidateRef getRecoEcalCandidate(reco::SuperClusterRef scRef, edm::Handle<reco::RecoEcalCandidateRefVector> candH);
  
  edm::EDGetTokenT<candidateRefVector>    token_inputs;
  StringCutObjectSelector<T> candSelector;
  edm::EDGetTokenT<edm::ValueMap<selection_type> >  token_selection;
  edm::EDGetTokenT<reco::RecoEcalCandidateRefVector> token_recoecal;
  
  cut_type m_cut;
  bool isGreaterThan_;
  bool saveSCRef_;
};

template <typename T, typename C>
  SelectorByValueMap<T,C>::SelectorByValueMap(edm::ParameterSet const & config) :
  token_inputs(consumes<candidateRefVector>(config.getParameter<edm::InputTag>("input"))),
    candSelector(config.getParameter<std::string>("cut")),
    token_selection(consumes<edm::ValueMap<selection_type> >(config.getParameter<edm::InputTag>("selection"))),
    m_cut(config.getParameter<cut_type>("id_cut")) {
    
    isGreaterThan_ = true;
    if (config.existsAs<bool>("isGreaterThan")) 
      isGreaterThan_ = config.getParameter<bool>("isGreaterThan");
    
    saveSCRef_ = false;
    if (config.existsAs<bool>("saveSCRef")) {
      saveSCRef_ = config.getParameter<bool>("saveSCRef");
      token_recoecal = mayConsume<reco::RecoEcalCandidateRefVector>(config.getParameter<edm::InputTag>("recoEcalCandidates"));
    }
    
    if (saveSCRef_)
      produces<reco::RecoEcalCandidateRefVector>("superclusters");
    else
      produces<candidateRefVector>();
  }


template <typename T, typename C>
reco::RecoEcalCandidateRef SelectorByValueMap<T, C>::getRecoEcalCandidate(reco::SuperClusterRef scRef, edm::Handle<reco::RecoEcalCandidateRefVector> candH) {
  
  const reco::RecoEcalCandidateRefVector* cands = candH.product();
  for (unsigned int i=0; i<cands->size(); i++) {
    if ((*cands)[i]->superCluster() == scRef)
      return (*cands)[i];
  }
  
  return reco::RecoEcalCandidateRef();
}

template <typename T, typename C>
void SelectorByValueMap<T, C>::produce(edm::Event & event, const edm::EventSetup & setup) {
  std::auto_ptr<candidateRefVector> candidates(new candidateRefVector());
  std::auto_ptr<reco::RecoEcalCandidateRefVector> scCandidates(new reco::RecoEcalCandidateRefVector());

  edm::Handle<candidateRefVector> h_inputs;
  event.getByToken(token_inputs, h_inputs);

  // read the selection map from the Event
  edm::Handle<edm::ValueMap<selection_type> > h_selection;
  event.getByToken(token_selection, h_selection);
  edm::ValueMap<selection_type> const & selectionMap = * h_selection;

  edm::Handle<reco::RecoEcalCandidateRefVector> candH;
  if (saveSCRef_) 
    event.getByToken(token_recoecal, candH);

  for (unsigned int i = 0; i < h_inputs->size(); ++i) {

    candidateRef ptr = (*h_inputs)[i];
    if (candSelector(*ptr)) {
      if (isGreaterThan_) {
	if (selectionMap[ptr] >= m_cut) {
	  if (saveSCRef_) {
	    reco::RecoEcalCandidateRef ref = getRecoEcalCandidate(ptr->superCluster(), candH);
	    if (ref.isNonnull()) 
	      scCandidates->push_back(ref);
	  } else
	    candidates->push_back(ptr);
	}
      } else {
	if (selectionMap[ptr] < m_cut) {
	  if (saveSCRef_) {
	    reco::RecoEcalCandidateRef ref = getRecoEcalCandidate(ptr->superCluster(), candH);
	    if (ref.isNonnull()) 
	      scCandidates->push_back(ref);
	  } else
	    candidates->push_back(ptr);
	}
      }
    }
  }
  
  if (saveSCRef_)
    event.put(scCandidates, "superclusters");
  else
    event.put(candidates);
}
#endif

