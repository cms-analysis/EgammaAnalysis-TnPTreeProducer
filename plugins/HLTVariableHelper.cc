#include "HLTVariableHelper.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/PatCandidates/interface/Electron.h"

typedef  HLTVariableHelper<pat::Electron> PatElectronHLTVariableHelper;
DEFINE_FWK_MODULE(PatElectronHLTVariableHelper);

typedef  HLTVariableHelper<reco::GsfElectron> GsfElectronHLTVariableHelper;
DEFINE_FWK_MODULE(GsfElectronHLTVariableHelper);
