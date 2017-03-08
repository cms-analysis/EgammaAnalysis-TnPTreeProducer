#include "SCVariableHelper.h"

#include "DataFormats/RecoCandidate/interface/RecoEcalCandidate.h"
#include "FWCore/Framework/interface/MakerMacros.h"


typedef SCVariableHelper<reco::RecoEcalCandidate> RecoEcalCandidateVariableHelper;
DEFINE_FWK_MODULE(RecoEcalCandidateVariableHelper);
