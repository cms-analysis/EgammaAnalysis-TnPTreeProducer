#ifndef _ElectronMatchedCandidateProducer_h
#define _ElectronMatchedCandidateProducer_h

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/RecoCandidate/interface/RecoEcalCandidate.h"
#include "DataFormats/RecoCandidate/interface/RecoEcalCandidateFwd.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"

#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

#include "DataFormats/Math/interface/deltaR.h"


template <class T>
class ElectronMatchedCandidateProducer : public edm::EDProducer {
  
  typedef std::vector<T> TCollection;
  typedef edm::Ref<TCollection> TRef;
  typedef edm::RefVector<TCollection> TRefVector;
    
 public:
  explicit ElectronMatchedCandidateProducer(const edm::ParameterSet&);
  ~ElectronMatchedCandidateProducer();

 private:
  virtual void produce(edm::Event&, const edm::EventSetup&) override;
  
  edm::EDGetTokenT<TRefVector> electronCollectionToken_;
  edm::EDGetTokenT<reco::RecoEcalCandidateCollection> scCollectionToken_;
  StringCutObjectSelector<reco::RecoEcalCandidate> candSelector_;
};


template <class T>
ElectronMatchedCandidateProducer<T>::ElectronMatchedCandidateProducer(const edm::ParameterSet &params):
electronCollectionToken_(consumes<TRefVector>(params.getUntrackedParameter<edm::InputTag>("ReferenceElectronCollection"))),
  scCollectionToken_(consumes<reco::RecoEcalCandidateCollection> (params.getParameter<edm::InputTag>("src"))),
  candSelector_(params.getParameter<std::string>("cut")) 
{
  produces<edm::RefVector<reco::RecoEcalCandidateCollection> >("superclusters");
  produces<TRefVector>("electrons");
}

template <class T>
ElectronMatchedCandidateProducer<T>::~ElectronMatchedCandidateProducer()
{}

template <class T>
void ElectronMatchedCandidateProducer<T>::produce(edm::Event &event,
						  const edm::EventSetup &eventSetup) {

  std::unique_ptr<edm::RefVector<reco::RecoEcalCandidateCollection> > outCol (new edm::RefVector<reco::RecoEcalCandidateCollection>);
  std::unique_ptr<TRefVector> outCol2 (new TRefVector);
  
  // Read electrons
  edm::Handle<TRefVector> electrons;
  event.getByToken(electronCollectionToken_, electrons);

  //Read candidates
  edm::Handle<reco::RecoEcalCandidateCollection> recoCandColl;
  event.getByToken(scCollectionToken_ , recoCandColl);


  for (size_t sc=0; sc<recoCandColl->size(); sc++) {
    
    reco::RecoEcalCandidateRef ref(recoCandColl, sc);
    if (candSelector_(*ref)) {
      bool matched = false;
      for (size_t elec=0; elec<electrons->size(); elec++) {
	// need to move to parentSuperCluster (i.e.  mustache one) when I know how to make it work in AOD
	double dr = reco::deltaR( (*electrons)[elec]->superCluster()->position(),ref->superCluster()->position() );
	//	if ((*electrons)[elec]->superCluster() == ref->superCluster()) {
	/// for now prefer a simple dR matching since SC ref matching does not in AODs
	if ( dr < 0.1 && !matched) {
	  outCol->push_back(ref);
	  outCol2->push_back((*electrons)[elec]);
	  matched = true;
	}
      } 
    } 
  }
  /*  
  if( outCol->size() < electrons->size() ) {
#include <iostream>
    using namespace std;
    std::cout << " ======================================== " << std::endl;
    std::cout << " ======================================== " << std::endl;
    std::cout << " Size SC  coll: " << recoCandColl->size() << std::endl;
    std::cout << " Size Ele coll: " << electrons->size() << std::endl;
    std::cout << " Size out coll: " << outCol->size() << std::endl;
    for (size_t elec=0; elec<electrons->size(); elec++) {
      cout << " Ele: " << elec << " Energy: " << (*electrons)[elec]->pt() << endl;
      for (size_t sc=0; sc<recoCandColl->size(); sc++) {
	reco::RecoEcalCandidateRef ref(recoCandColl, sc);
	if (candSelector_(*ref)) {
	  double dr = reco::deltaR((*electrons)[elec]->superCluster()->position(),ref->superCluster()->position() );
	  cout << " dr[ SC " << sc << " = " << dr << endl;
	}
      }
    }
  }
  */
  event.put(std::move(outCol ), "superclusters");
  event.put(std::move(outCol2), "electrons");
}

#endif


