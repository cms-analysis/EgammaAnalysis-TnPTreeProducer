#ifndef HLTVARIABLEHELPER_H
#define HLTVARIABLEHELPER_H

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/ValueMap.h"

#include "DataFormats/RecoCandidate/interface/RecoEcalCandidate.h"
#include "DataFormats/RecoCandidate/interface/RecoEcalCandidateFwd.h"
#include "DataFormats/RecoCandidate/interface/RecoEcalCandidateIsolation.h"

//#include "DataFormats/EgammaCandidate/interface/SuperCluster.h"

#include "DataFormats/Math/interface/deltaR.h"

template <class T>
class HLTVariableHelper : public edm::EDProducer {

  typedef std::vector<T> TCollection;
  typedef edm::Ref<TCollection> TRef;

public:
  explicit HLTVariableHelper(const edm::ParameterSet & iConfig);
  virtual ~HLTVariableHelper() ;
  
  virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup) override;
  
private:
  edm::EDGetTokenT<TCollection> probesToken_;
  edm::EDGetTokenT<double> rhoToken_;
  edm::EDGetTokenT<std::vector<reco::RecoEcalCandidate> > hltCandToken_;
  std::vector<edm::EDGetTokenT<reco::RecoEcalCandidateIsolationMap> > mapsToken_;
  
  std::vector<std::string> mapNames_;
  std::vector<std::string> hardCodedNames_;
  std::vector<edm::InputTag> inputTags_;
};

template <class T>
HLTVariableHelper<T>::HLTVariableHelper(const edm::ParameterSet & iConfig) : 
probesToken_(consumes<TCollection>(iConfig.getParameter<edm::InputTag>("probes"))),
  rhoToken_(consumes<double>(iConfig.getParameter<edm::InputTag>("rhoInputTag"))),
  hltCandToken_(consumes<std::vector<reco::RecoEcalCandidate> >(iConfig.getParameter<edm::InputTag>("hltCandidateCollection"))),
  mapNames_(iConfig.getParameter<std::vector<std::string> >("mapOutputNames")),
  inputTags_(iConfig.getParameter<std::vector<edm::InputTag> >("mapInputTags")) {

  if (mapNames_.size() != inputTags_.size()) {
    std::cerr << "You need to specify as many strings as inputTags..." << std::endl;
    abort();
  }

  hardCodedNames_.push_back("hltrho");
  hardCodedNames_.push_back("hlte");
  hardCodedNames_.push_back("hltet");
  hardCodedNames_.push_back("hlteta");
  hardCodedNames_.push_back("hltphi");
  
  for (unsigned int i=0; i<hardCodedNames_.size(); i++)
    produces<edm::ValueMap<float> >(hardCodedNames_[i]);

  for (unsigned int i=0; i<mapNames_.size(); i++) { 
    produces<edm::ValueMap<float> >(mapNames_[i]);
    mapsToken_.push_back(consumes<reco::RecoEcalCandidateIsolationMap>(inputTags_[i]));
  }
}

template <class T>
HLTVariableHelper<T>::~HLTVariableHelper()
{}

template <class T>
void HLTVariableHelper<T>::produce(edm::Event & iEvent, const edm::EventSetup & iSetup) {

  // read inputs
  edm::Handle<std::vector<reco::RecoEcalCandidate> > cH;
  edm::Handle<TCollection> probes;
  iEvent.getByToken(probesToken_,  probes);
    
  std::vector<edm::Handle<reco::RecoEcalCandidateIsolationMap> > mapsH(mapsToken_.size());
  std::vector<const reco::RecoEcalCandidateIsolationMap*> maps(inputTags_.size(), 0);

  edm::Handle<double> rhoH;
  iEvent.getByToken(rhoToken_, rhoH);
  double rho;

  if (!rhoH.failedToGet())
    rho = *(rhoH.product());
  else
    rho = 999999.;

  // hardcoded valuemaps
  std::vector<std::vector<float> > hardCodedValues;
  for (unsigned int i=0; i<hardCodedNames_.size(); i++) 
    hardCodedValues.push_back(std::vector<float>(probes->size(), 999999.));

  // prepare vector for output
  std::vector<std::vector<float> > values;
  for (unsigned int i=0; i<inputTags_.size(); i++) 
    values.push_back(std::vector<float>(probes->size(), 999999.));

  iEvent.getByToken(hltCandToken_, cH);
  if (!cH.failedToGet()) {
    for (unsigned int i=0; i<inputTags_.size(); i++) {
      iEvent.getByToken(mapsToken_[i], mapsH[i]);
      if (!mapsH[i].failedToGet())
	maps[i] = mapsH[i].product();
    }

    for (size_t p=0; p<probes->size(); p++) {
      const TRef ref(probes, p);
      float dRmin = 0.3;

      for(size_t nc=0; nc<cH->size(); nc++) {
	reco::RecoEcalCandidateRef cRef(cH, nc);      
	float dR = deltaR(cRef->p4(), ref->p4());

	if (dR < dRmin) {
          dRmin = dR;

	  hardCodedValues[0][p] = rho;
	  hardCodedValues[1][p] = cRef->energy();
	  hardCodedValues[2][p] = cRef->et();//superCluster()->energy()*cRef->superCluster()->position().Theta(); // et
	  hardCodedValues[3][p] = cRef->eta(); // eta
	  hardCodedValues[4][p] = cRef->phi(); // phi
	  
	  for (unsigned int i=0; i<inputTags_.size(); i++) {
	  if (maps[i] != 0)
	    values[i][p] = (*maps[i])[cRef];
	  }
	}
      }
    }
  }

  // Save hardcoded
  for (unsigned int i=0; i<hardCodedNames_.size(); i++) {
    // convert into ValueMap and store
    std::auto_ptr<edm::ValueMap<float> > aMap(new edm::ValueMap<float>());
    edm::ValueMap<float>::Filler aFiller(*aMap);
    aFiller.insert(probes, hardCodedValues[i].begin(), hardCodedValues[i].end());
    aFiller.fill();
    iEvent.put(aMap, hardCodedNames_[i]);
  }

  for (unsigned int i=0; i<mapNames_.size(); i++) {
    // convert into ValueMap and store
    std::auto_ptr<edm::ValueMap<float> > aMap(new edm::ValueMap<float>());
    edm::ValueMap<float>::Filler aFiller(*aMap);
    aFiller.insert(probes, values[i].begin(), values[i].end());
    aFiller.fill();
    iEvent.put(aMap, mapNames_[i]);
  }
}
#endif 
