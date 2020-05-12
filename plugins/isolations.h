#ifndef EgammaIsolationAlgos_isolations_h
#define EgammaIsolationAlgos_isolations_h

#include "DataFormats/PatCandidates/interface/PackedCandidate.h"

#include <Math/VectorUtil.h>

template<class CandidateContainer>
std::vector<float> computePfLeptonIsolations(CandidateContainer const& targetCandidates,
                                             edm::View<reco::Candidate> const& pfCandidates){

  std::vector<float> leptonIsolations(targetCandidates.size());
  for(auto const& pfcand : pfCandidates) {
    auto absPdg = std::abs(pfcand.pdgId());
    auto pfPackedCand = dynamic_cast<const pat::PackedCandidate&>(pfcand);
    if(!(absPdg==11 || absPdg==13) || pfPackedCand.fromPV() < pat::PackedCandidate::PVTight){
      continue;
    }
    for(unsigned int i = 0; i < targetCandidates.size(); ++i) {
      auto dR = std::abs(ROOT::Math::VectorUtil::DeltaR(pfcand.p4(), targetCandidates[i].p4()));
      // lower dR threshold to avoid adding itself
      if (dR <= 0.3 && dR >= 0.0005){
        leptonIsolations[i] += pfcand.p4().pt();
      }
    }
  }

  return leptonIsolations;
}

#endif
