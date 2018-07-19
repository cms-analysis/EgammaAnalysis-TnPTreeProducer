// -*- C++ -*-
//
// Package:    EventCounter/SimpleEventCounter
// Class:      SimpleEventCounter
// 
/**\class SimpleEventCounter SimpleEventCounter.cc EventCounter/SimpleEventCounter/plugins/SimpleEventCounter.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Francesco Micheli
//         Created:  Wed, 09 May 2018 13:01:25 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"

//
// class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<> and also remove the line from
// constructor "usesResource("TFileService");"
// This will improve performance in multithreaded jobs.

class SimpleEventCounter : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
public:
  explicit SimpleEventCounter(const edm::ParameterSet&);
  ~SimpleEventCounter();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


private:
  virtual void beginJob() override;
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
  virtual void endJob() override;

  // ----------member data ---------------------------
  edm::Service<TFileService> fs_;
  // to keep track of the sum of weights
  TH1F *h_sumW;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
SimpleEventCounter::SimpleEventCounter(const edm::ParameterSet& iConfig)

{
  //now do what ever initialization is needed
  usesResource("TFileService");

}


SimpleEventCounter::~SimpleEventCounter()
{
 
  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
SimpleEventCounter::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;



#ifdef THIS_IS_AN_EVENT_EXAMPLE
  Handle<ExampleData> pIn;
  iEvent.getByLabel("example",pIn);
#endif
   
#ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
  ESHandle<SetupData> pSetup;
  iSetup.get<SetupRecord>().get(pSetup);
#endif

  // To keep track of the sum of weights
  h_sumW->Fill(0.5);

}


// ------------ method called once each job just before starting event loop  ------------
void 
SimpleEventCounter::beginJob()
{
  // to keep track of the sum of weights
  h_sumW = fs_->make<TH1F>("h_sumW", "h_sumW", 1,  0., 1.);
  h_sumW->Sumw2();
}

// ------------ method called once each job just after ending the event loop  ------------
void 
SimpleEventCounter::endJob() 
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
SimpleEventCounter::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(SimpleEventCounter);
