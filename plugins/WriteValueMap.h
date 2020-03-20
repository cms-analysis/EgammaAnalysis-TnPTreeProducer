#ifndef _WriteValueMap_h
#define _WriteValueMap_h 

#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Common/interface/ValueMap.h"

/*
 * Very useful function to avoid massive amounts of copied code when making lots of value maps
 */
template <typename ValueType, class HandleType> 
void writeValueMap(edm::Event& iEvent, const edm::Handle<HandleType>& handle, const std::vector<ValueType>& values, const std::string& label) {
  auto valMap = std::make_unique<edm::ValueMap<ValueType>>();
  typename edm::ValueMap<ValueType>::Filler filler(*valMap);
  filler.insert(handle, values.begin(), values.end());
  filler.fill();
  iEvent.put(std::move(valMap), label);
}

#endif
