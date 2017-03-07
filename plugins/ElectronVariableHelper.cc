#include "ElectronVariableHelper.h"

#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/PatCandidates/interface/Electron.h"

#include "FWCore/Framework/interface/MakerMacros.h"

typedef ElectronVariableHelper<pat::Electron>     PatElectronVariableHelper;
DEFINE_FWK_MODULE(PatElectronVariableHelper);

typedef ElectronVariableHelper<reco::GsfElectron> GsfElectronVariableHelper;
DEFINE_FWK_MODULE(GsfElectronVariableHelper);
