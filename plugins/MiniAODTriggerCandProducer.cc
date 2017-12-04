#include "MiniAODTriggerCandProducer.h"
  
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/RecoCandidate/interface/RecoEcalCandidate.h"
#include "DataFormats/RecoCandidate/interface/RecoEcalCandidateFwd.h"
#include "DataFormats/RecoCandidate/interface/RecoChargedCandidate.h"
#include "DataFormats/RecoCandidate/interface/RecoChargedCandidateFwd.h"

template <>
bool MiniAODTriggerCandProducer<reco::GsfElectron, trigger::TriggerObject>::onlineOfflineMatchingRECO(reco::GsfElectronRef ref, 
												      const std::vector<trigger::TriggerObject>* triggerObjects,
												      const trigger::Keys* keys, float dRmin) {

  for (const auto & key : *keys) {
    float dR = deltaR2(ref->superCluster()->position().eta(), ref->superCluster()->position().phi(),
		       (*triggerObjects)[key].eta(), (*triggerObjects)[key].phi());
    //std::cout << "dr" << dR << std::endl;
    if (dR < dRmin*dRmin) {
      return true;
    }
  }

  return false;
}

template <>
MiniAODTriggerCandProducer<reco::GsfElectron, trigger::TriggerObject>::MiniAODTriggerCandProducer(const edm::ParameterSet& iConfig ):
  filterNames_(iConfig.getParameter<std::vector<std::string> >("filterNames")),
  inputs_(consumes<TRefVector>(iConfig.getParameter<edm::InputTag>("inputs"))),
  triggerBits_(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("bits"))),
  //triggerObjects_(consumes<pat::TriggerObjectStandAloneCollection>(iConfig.getParameter<edm::InputTag>("objects"))),
  //triggerObjects_(consumes<U>(iConfig.getParameter<edm::InputTag>("objects"))),
  triggerEvent_(consumes<trigger::TriggerEvent>(iConfig.getParameter<edm::InputTag>("objects"))),
  dRMatch_(iConfig.getParameter<double>("dR")),
  isAND_(iConfig.getParameter<bool>("isAND")) {
  
  produces<TRefVector>();
}

template <>
void MiniAODTriggerCandProducer<reco::GsfElectron, trigger::TriggerObject>::produce(edm::Event &iEvent, const edm::EventSetup &eventSetup) {
  
  edm::Handle<edm::TriggerResults> triggerBits;
  edm::Handle<trigger::TriggerEvent> trEv;
  iEvent.getByToken(triggerEvent_, trEv);
  const trigger::TriggerObjectCollection& triggerObjects(trEv->getObjects());
  
  edm::Handle<TRefVector> inputs;

  iEvent.getByToken(triggerBits_, triggerBits);
  iEvent.getByToken(inputs_, inputs);

  // Create the output collection
  std::unique_ptr<TRefVector> outColRef(new TRefVector);
  
  if (!triggerBits.isValid()) {
    LogDebug("") << "TriggerResults product not found - returning result=false!";
    return;
  }

  const edm::TriggerNames & triggerNames = iEvent.triggerNames(*triggerBits);
  if (triggerNamesID_ != triggerNames.parameterSetID()) {
    triggerNamesID_ = triggerNames.parameterSetID();
    init(*triggerBits, triggerNames);
  } 

  for (size_t i=0; i<inputs->size(); i++) {
    bool saveObj = true;
    TRef ref = (*inputs)[i];

    //    std::cout << "REF:" << ref->eta() << " " << ref->phi() << " " << ref->et() << std::endl;
    if (filterNames_.size() > 0) {
      unsigned int moduleFilterIndex = 9999;
      if (filterNames_[0] != "") {
	//std::cout << "DIVERSO DA 0" << std::endl;
	for (int i=0;i<trEv->sizeFilters(); i++) {
	  if (trEv->filterLabel(i) == filterNames_[0]) {
	    moduleFilterIndex = i;
	    //std::cout << "myIndex:" << i << std::endl;
	    break;
	  }
	}
	//unsigned int moduleFilterIndex = trEv->filterIndex(filterNames_[0]);
	//std::cout << "Filter: " << filterNames_[0] << std::endl;//" " << moduleFilterIndex << " " << trEv->sizeFilters() << std::endl;
	
	if (moduleFilterIndex+1 > trEv->sizeFilters()) 
	  saveObj = false;
	else {
	  const trigger::Keys &keys = trEv->filterKeys( moduleFilterIndex );
	  saveObj = onlineOfflineMatchingRECO(ref, &triggerObjects, &keys, dRMatch_);
	}
      }
      for (size_t f=1; f<filterNames_.size(); f++) {
      	if (filterNames_[f] != "") {
      	  unsigned int moduleFilterIndex = trEv->filterIndex(filterNames_[f]);
      	  if (moduleFilterIndex+1 > trEv->sizeFilters()) 
      	    saveObj = false;
      	  else {
      	    const trigger::Keys &keys = trEv->filterKeys( moduleFilterIndex );
      	    if (isAND_)
      	      saveObj = (saveObj && onlineOfflineMatchingRECO(ref, &triggerObjects, &keys, dRMatch_));
      	    else		   
      	      saveObj = (saveObj || onlineOfflineMatchingRECO(ref, &triggerObjects, &keys, dRMatch_));
      	  } 
      	}
      }
    }

    //std::cout << saveObj << std::endl;
    if (saveObj)
      outColRef->push_back(ref);
  }	  

  iEvent.put(std::move(outColRef));
}

template<>
bool MiniAODTriggerCandProducer<pat::Electron, pat::TriggerObjectStandAlone>::onlineOfflineMatching(pat::ElectronRef ref, 
												    const std::vector<pat::TriggerObjectStandAlone>* triggerObjects, 
												    std::string filterLabel, float dRmin,const edm::Handle<edm::TriggerResults> & triggerBits,const edm::TriggerNames &triggerNames, edm::Event &iEvent) {
  
  for (pat::TriggerObjectStandAlone obj : *triggerObjects) { 
    //obj.unpackPathNames(triggerNames); 
    obj.unpackPathNames(triggerNames);
    obj.unpackFilterLabels(iEvent, *triggerBits);
    if (obj.hasFilterLabel(filterLabel)) {
      float dR = deltaR(ref->superCluster()->position(), obj.p4());
      if (dR < dRmin)
	return true;
    }
  }

  return false;
}

template <>
bool MiniAODTriggerCandProducer<pat::Photon, pat::TriggerObjectStandAlone>::onlineOfflineMatching(pat::PhotonRef ref,
												  const std::vector<pat::TriggerObjectStandAlone>* triggerObjects, 
												  std::string filterLabel, float dRmin,const edm::Handle<edm::TriggerResults> & triggerBits,const edm::TriggerNames &triggerNames, edm::Event &iEvent) {
  
  for (pat::TriggerObjectStandAlone obj : *triggerObjects) { 
    //obj.unpackPathNames(triggerNames); 

    obj.unpackPathNames(triggerNames);
    obj.unpackFilterLabels(iEvent, *triggerBits);
    if (obj.hasFilterLabel(filterLabel)) {
      float dR = deltaR(ref->superCluster()->position(), obj.p4());
      if (dR < dRmin)
	return true;
    }
  }

  return false;
}

template <>
bool MiniAODTriggerCandProducer<reco::RecoEcalCandidate, pat::TriggerObjectStandAlone>::onlineOfflineMatching(edm::Ref<std::vector<reco::RecoEcalCandidate>> ref,
													      const std::vector<pat::TriggerObjectStandAlone>* triggerObjects, 
													      std::string filterLabel, float dRmin,const edm::Handle<edm::TriggerResults> & triggerBits,const edm::TriggerNames &triggerNames, edm::Event &iEvent) {

  for (pat::TriggerObjectStandAlone obj : *triggerObjects) { 
    //obj.unpackPathNames(triggerNames); 

    obj.unpackPathNames(triggerNames);
    obj.unpackFilterLabels(iEvent, *triggerBits);
    if (obj.hasFilterLabel(filterLabel)) {
      float dR = deltaR(ref->superCluster()->position(), obj.p4());
      if (dR < dRmin)
	return true;
    }
  }

  return false;
}

typedef MiniAODTriggerCandProducer<reco::GsfElectron, trigger::TriggerObject> GsfElectronTriggerCandProducer;
DEFINE_FWK_MODULE(GsfElectronTriggerCandProducer);

typedef MiniAODTriggerCandProducer<pat::Electron, pat::TriggerObjectStandAlone> PatElectronTriggerCandProducer;
DEFINE_FWK_MODULE(PatElectronTriggerCandProducer);

typedef MiniAODTriggerCandProducer<pat::Photon, pat::TriggerObjectStandAlone> PatPhotonTriggerCandProducer;
DEFINE_FWK_MODULE(PatPhotonTriggerCandProducer);

typedef MiniAODTriggerCandProducer<reco::RecoEcalCandidate, pat::TriggerObjectStandAlone> RecoEcalCandidateTriggerCandProducer;
DEFINE_FWK_MODULE(RecoEcalCandidateTriggerCandProducer);
