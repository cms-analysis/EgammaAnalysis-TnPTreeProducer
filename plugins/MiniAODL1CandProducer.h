#ifndef _MINIADOL1CANDPRODUCER_H_
#define _MINIADOL1CANDPRODUCER_H_

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "DataFormats/L1Trigger/interface/L1EmParticle.h"
#include "DataFormats/L1Trigger/interface/L1EmParticleFwd.h"

#include <DataFormats/Math/interface/deltaR.h>

#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include <string>
#include <vector>

template <class T>
class MiniAODL1CandProducer : public edm::EDProducer {

  typedef std::vector<T> TCollection;
  typedef edm::Ref<TCollection> TRef;
  typedef edm::RefVector<TCollection> TRefVector;

public:
  MiniAODL1CandProducer(const edm::ParameterSet&);
  ~MiniAODL1CandProducer();

  bool l1OfflineMatching(const l1extra::L1EmParticleCollection& triggerObjects, 
			 math::XYZTLorentzVector refP4, float dRmin, int& index);

 private:
  /// compare two l1Extra in et
  struct ComparePt {
    bool operator()( const l1extra::L1EmParticle& t1, const l1extra::L1EmParticle& t2 ) const {
      return t1.et() > t2.et();
    }
  };
  ComparePt ptComparator;

  virtual void produce(edm::Event&, const edm::EventSetup&) override;
  
  edm::EDGetTokenT<TRefVector> inputs_;
  edm::EDGetTokenT<l1extra::L1EmParticleCollection> l1IsoObjectsToken_;
  edm::EDGetTokenT<l1extra::L1EmParticleCollection> l1NonIsoObjectsToken_;
  float minET_;
  float dRMatch_;
};

template <class T>
MiniAODL1CandProducer<T>::MiniAODL1CandProducer(const edm::ParameterSet& iConfig ) :
  inputs_(consumes<TRefVector>(iConfig.getParameter<edm::InputTag>("inputs"))),
  l1IsoObjectsToken_(consumes<l1extra::L1EmParticleCollection>(iConfig.getParameter<edm::InputTag>("isoObjects"))),
  l1NonIsoObjectsToken_(consumes<l1extra::L1EmParticleCollection>(iConfig.getParameter<edm::InputTag>("nonIsoObjects"))),
  minET_(iConfig.getParameter<double>("minET")),		
  dRMatch_(iConfig.getParameter<double>("dRmatch")) {

  produces<TRefVector>();
}

template <class T>
MiniAODL1CandProducer<T>::~MiniAODL1CandProducer()
{}

template <class T>
void MiniAODL1CandProducer<T>::produce(edm::Event &iEvent, const edm::EventSetup &eventSetup) {

  edm::Handle<l1extra::L1EmParticleCollection> l1IsoObjectsH;
  edm::Handle<l1extra::L1EmParticleCollection> l1NonIsoObjectsH;
  edm::Handle<TRefVector> inputs;

  iEvent.getByToken(l1IsoObjectsToken_, l1IsoObjectsH);
  iEvent.getByToken(l1NonIsoObjectsToken_, l1NonIsoObjectsH);
  iEvent.getByToken(inputs_, inputs);

  // Merge L1 objects and sort by et
  l1extra::L1EmParticleCollection mergedL1;
  for (l1extra::L1EmParticleCollection::const_iterator it=l1IsoObjectsH.product()->begin();
       it!=l1IsoObjectsH.product()->end(); it++)
    mergedL1.push_back(*it);

  for (l1extra::L1EmParticleCollection::const_iterator it=l1NonIsoObjectsH.product()->begin();
       it!=l1NonIsoObjectsH.product()->end(); it++)
    mergedL1.push_back(*it);

  std::sort(mergedL1.begin(), mergedL1.end(), ptComparator);

  // Create the output collection
  std::auto_ptr<TRefVector> outColRef(new TRefVector);

  for (size_t i=0; i<inputs->size(); i++) {
    TRef ref = (*inputs)[i];
    int index = -1;

    if (l1OfflineMatching(mergedL1, ref->p4(), dRMatch_, index)) {
      outColRef->push_back(ref);
    }
  }	  

  iEvent.put(outColRef);
}

template <class T>
bool MiniAODL1CandProducer<T>::l1OfflineMatching(const l1extra::L1EmParticleCollection& l1Objects, 
						 math::XYZTLorentzVector refP4, float dRmin, int& index) {
  
  index = 0;
  for (l1extra::L1EmParticleCollection::const_iterator it=l1Objects.begin(); it != l1Objects.end(); it++) {
    if (it->et() < minET_)
      continue;

  float dR = deltaR(refP4, it->p4());
    if (dR < dRmin)
      return true;
    
    index++;
  }

  return false;
}


#endif
