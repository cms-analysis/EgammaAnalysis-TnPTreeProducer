// -*- C++ -*-
//
// Package:    PileupWeightProducer
// Class:      PileupWeightProducer
// 
/**\class PileupWeightProducer PileupWeightProducer.cc 

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Ricardo Vasquez Sierra,6 R-025,+41227672274,
//         Created:  Mon Nov 21 15:05:26 CET 2011
//
//
#include <numeric>
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h" 

#include <vector>
#include <iostream>

class PileupWeightProducer : public edm::EDProducer {
public:
  explicit PileupWeightProducer(const edm::ParameterSet&);
  ~PileupWeightProducer();
  
private:
  //virtual void beginJob() ;
  virtual void produce(edm::Event&, const edm::EventSetup&);
  //virtual void endJob() ;

  edm::EDGetTokenT< std::vector<PileupSummaryInfo> > pileupInfoTag_;
  std::vector<double> pileupMC_;
  std::vector<double> pileupData_;
  std::vector<double> pileupWeights_;
};

PileupWeightProducer::PileupWeightProducer(const edm::ParameterSet& iConfig) {

  pileupMC_   = iConfig.getParameter<std::vector<double> >("PileupMC");
  pileupData_ = iConfig.getParameter<std::vector<double> >("PileupData");
  pileupInfoTag_ = consumes<std::vector<PileupSummaryInfo> >(iConfig.getParameter<edm::InputTag>("pileupInfoTag"));

  unsigned int nbins = std::min(pileupData_.size(), pileupMC_.size());
  pileupData_.resize(nbins);
  pileupMC_.resize(nbins);
  
  auto scl  = std::accumulate(pileupMC_.begin(), pileupMC_.end(), 0.)/std::accumulate(pileupData_.begin(), pileupData_.end(),0.);
  for(size_t ib = 0; ib<pileupData_.size(); ++ib) {
    pileupWeights_.push_back(pileupData_[ib] * scl / pileupMC_[ib]);
    //std::cout << pileupWeights_.back() << std::endl;
    if( pileupMC_[ib] < 1e-6) pileupWeights_[pileupWeights_.size()-1] = 0;
  }

  produces<double>( "pileupWeights" ).setBranchAlias( "pileupWeights" );
}

PileupWeightProducer::~PileupWeightProducer()
{}

void PileupWeightProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

  std::unique_ptr<double> pileupWeight( new double );
  *pileupWeight = 1.;

  edm::Handle<std::vector<PileupSummaryInfo> > PupInfo;
  
  if(!iEvent.isRealData() ) {
    iEvent.getByToken(pileupInfoTag_, PupInfo);
    int nPUtrue = PupInfo->begin()->getTrueNumInteractions();
    //    *pileupWeight = pileupWeights_[nPUtrue+1]; // NOT 100% sure
    *pileupWeight = pileupWeights_[nPUtrue]; // most likely better estimate
  }
  iEvent.put(std::move(pileupWeight), "pileupWeights"); 

}

//define this as a plug-in
DEFINE_FWK_MODULE(PileupWeightProducer);
