#ifndef _MINIADOL1STAGE2CANDPRODUCER_H_
#define _MINIADOL1STAGE2CANDPRODUCER_H_

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

//#include "DataFormats/L1Trigger/interface/L1EmParticle.h"                                                                                                          
//#include "DataFormats/L1Trigger/interface/L1EmParticleFwd.h"                                                                                                       
#include "DataFormats/L1Trigger/interface/EGamma.h" //for stage 2 L1                                                                                                 
#include <DataFormats/Math/interface/deltaR.h>

#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include <string>
#include <vector>

template <class T>
class MiniAODL1Stage2CandProducer : public edm::EDProducer {

  typedef std::vector<T> TCollection;
  typedef edm::Ref<TCollection> TRef;
  typedef edm::RefVector<TCollection> TRefVector;

 public:
  MiniAODL1Stage2CandProducer(const edm::ParameterSet&);
  ~MiniAODL1Stage2CandProducer();

  bool l1OfflineMatching(const std::vector<l1t::EGamma>& triggerObjects,
                         math::XYZTLorentzVector refP4, float dRmin, float dRminEE, int& index);
 private:
  /// compare two l1Extra in et                                                                                                                                      
  struct ComparePt {
    bool operator()( const l1t::EGamma& t1, const l1t::EGamma& t2 ) const {
      return t1.et() > t2.et();
    }
  };
  ComparePt ptComparator;

  virtual void produce(edm::Event&, const edm::EventSetup&) override;

  edm::EDGetTokenT<TRefVector> inputs_;
  edm::EDGetTokenT<l1t::EGammaBxCollection> l1ObjectsToken_;
  float minET_;
  float dRMatch_;
  float dRMatchEE_;

};

template <class T>
MiniAODL1Stage2CandProducer<T>::MiniAODL1Stage2CandProducer(const edm::ParameterSet& iConfig ) :

 
  inputs_(consumes<TRefVector>(iConfig.getParameter<edm::InputTag>("inputs"))),
  l1ObjectsToken_(consumes<l1t::EGammaBxCollection> ( iConfig.getParameter<edm::InputTag>("objects"))),
  minET_(iConfig.getParameter<double>("minET")),
  dRMatch_(iConfig.getParameter<double>("dRmatch"))
{
 
  if(iConfig.exists("dRmatchEE"))
    dRMatchEE_ = (iConfig.getParameter<double>("dRmatchEE"));
  else
    dRMatchEE_ = dRMatch_; //for backwards compatibility
  
  produces<TRefVector>();
}

template <class T>
MiniAODL1Stage2CandProducer<T>::~MiniAODL1Stage2CandProducer()
{}

template <class T>
void MiniAODL1Stage2CandProducer<T>::produce(edm::Event &iEvent, const edm::EventSetup &eventSetup) {

  edm::Handle<l1t::EGammaBxCollection> l1ObjectsH;
  edm::Handle<TRefVector> inputs;

  iEvent.getByToken(l1ObjectsToken_, l1ObjectsH);
  iEvent.getByToken(inputs_, inputs);
 
   //Merge L1 objects and sort by et
  std::vector<l1t::EGamma> mergedL1;
  for(auto it=l1ObjectsH->begin(0); it!=l1ObjectsH->end(0); it++){
    mergedL1.push_back(*it);
    // std::cout << "L1: "  << endl;
  }
 
  std::sort(mergedL1.begin(), mergedL1.end(), ptComparator);

  // Create the output collection                                                                                                                                    
  // std::auto_ptr<TRefVector> outColRef(new TRefVector);
  std::unique_ptr<TRefVector> outColRef(new TRefVector);
 
  for (size_t i=0; i<inputs->size(); i++) {
    TRef ref = (*inputs)[i];
    int index = -1;

    if (l1OfflineMatching(mergedL1, ref->p4(), dRMatch_, dRMatchEE_, index)) {
      outColRef->push_back(ref);
    }
  }
  
  //iEvent.put(outColRef);
  iEvent.put(std::move(outColRef));
}

template <class T>
bool MiniAODL1Stage2CandProducer<T>::l1OfflineMatching(const std::vector<l1t::EGamma>& l1Objects,
						       math::XYZTLorentzVector refP4, float dRmin, float dRminEE, int& index) {

 
  index = 0;
  //for (auto it=l1Objects.begin(0); it != l1Objects.end(0); it++) { //bx 0 only considered 
  for (auto it=l1Objects.begin(); it != l1Objects.end(); it++) {
    if (it->et() < minET_)
      continue;
   
    float dR = deltaR(refP4, it->p4());
    if(fabs(refP4.eta()) < 1.5)
      if (dR < dRmin)
	return true;
    if(dR < dRminEE) //allow for looser requirements in EE (not needed for stage2)
      return true;
    index++;
  }

  return false;
  
}


#endif

