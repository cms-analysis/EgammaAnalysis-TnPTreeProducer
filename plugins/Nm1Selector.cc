#ifndef Nm1Selector_h
#define Nm1Selector_h

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Common/interface/Handle.h"

#include "DataFormats/PatCandidates/interface/VIDCutFlowResult.h"

#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Photon.h"

#include <vector>
#include <string>

//template <typename C>
//struct CompatibleConfigurationType {
//  typedef C type;
//};
    
//// "float" is not allowed, as it conflicts with "double"
//template <>
//struct CompatibleConfigurationType<float> {
//  typedef double type;
//};
  
template <typename T>
class Nm1Selector : public edm::EDProducer {
public:
  explicit Nm1Selector(edm::ParameterSet const & config);
  
private:
  typedef T candidate_type;

  typedef std::vector<candidate_type> candidateCollection;
  typedef edm::Ref<candidateCollection> candidateRef;
  typedef edm::RefVector<candidateCollection> candidateRefVector;

  void produce(edm::Event & event, edm::EventSetup const & setup);
    
  edm::EDGetTokenT<candidateRefVector>    token_inputs;
  StringCutObjectSelector<T> candSelector;
  edm::EDGetTokenT<edm::ValueMap<vid::CutFlowResult> >  token_selection;
  std::vector<unsigned int> cutIndicesToMask_;
  std::vector<std::string> cutNamesToMask_;
};
  
template <typename T>
Nm1Selector<T>::Nm1Selector(edm::ParameterSet const & config) :
  token_inputs(consumes<candidateRefVector>(config.getParameter<edm::InputTag>("input"))),
  candSelector(config.getParameter<std::string>("cut")),
  token_selection(consumes<edm::ValueMap<vid::CutFlowResult> >(config.getParameter<edm::InputTag>("selection"))) {

  if (config.existsAs<std::vector<unsigned int> >("cutIndicesToMask")) {
    cutIndicesToMask_ = config.getParameter<std::vector<unsigned int> >("cutIndicesToMask");
  } else {
    cutNamesToMask_ = config.getParameter<std::vector<std::string> >("cutNamesToMask");
    cutIndicesToMask_ = std::vector<unsigned int>();
  }

  produces<candidateRefVector>();
}
  
template <typename T>
void Nm1Selector<T>::produce(edm::Event & event, const edm::EventSetup & setup) {
  std::auto_ptr<candidateRefVector> candidates(new candidateRefVector());

  edm::Handle<candidateRefVector> h_inputs;
  event.getByToken(token_inputs, h_inputs);

  // read the selection map from the Event
  edm::Handle<edm::ValueMap<vid::CutFlowResult> > cutflow;
  event.getByToken(token_selection, cutflow);
  
  for (unsigned int i = 0; i < h_inputs->size(); ++i) {

    candidateRef ptr = (*h_inputs)[i];

    bool pass = false;    
    if (candSelector(*ptr)) {
      vid::CutFlowResult fullCutFlowData = (*cutflow)[ptr];
      if (cutIndicesToMask_.size() > 0) {
	vid::CutFlowResult maskedCutFlowData = fullCutFlowData.getCutFlowResultMasking(cutIndicesToMask_);
	if (maskedCutFlowData.cutFlowPassed())
	  pass = true;
	//std::cout << pass << std::endl;
	//int ncuts = maskedCutFlowData.cutFlowSize();
	//for(int icut = 0; icut<ncuts; icut++) {
	//	std::cout << icut << " " << maskedCutFlowData.getNameAtIndex(icut).c_str() 
	//		  << (int)maskedCutFlowData.isCutMasked(icut) << " " 
	//		  << maskedCutFlowData.getValueCutUpon(icut) << " " 
	//		  << (int)maskedCutFlowData.getCutResultByIndex(icut) << std::endl;
	//}
      } else {
	vid::CutFlowResult maskedCutFlowData = fullCutFlowData.getCutFlowResultMasking(cutNamesToMask_);
	if (maskedCutFlowData.cutFlowPassed())
	  pass = true;
      }
    }

    if (pass)
      candidates->push_back(ptr);
  }
  
  event.put(candidates);
}
#endif

typedef Nm1Selector<pat::Electron> PatElectronNm1Selector;
DEFINE_FWK_MODULE(PatElectronNm1Selector);

typedef Nm1Selector<pat::Photon> PatPhotonNm1Selector;
DEFINE_FWK_MODULE(PatPhotonNm1Selector);
