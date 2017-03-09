#include "SelectorByValueMap.h"

#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Photon.h"

typedef SelectorByValueMap<pat::Electron, bool> PatElectronSelectorByValueMap;
DEFINE_FWK_MODULE(PatElectronSelectorByValueMap);

typedef SelectorByValueMap<reco::GsfElectron, bool> GsfElectronSelectorByValueMap;
DEFINE_FWK_MODULE(GsfElectronSelectorByValueMap);

typedef SelectorByValueMap<reco::Photon, bool> PhotonSelectorByValueMap;
DEFINE_FWK_MODULE(PhotonSelectorByValueMap);

typedef SelectorByValueMap<pat::Photon , bool> PatPhotonSelectorByValueMap;
DEFINE_FWK_MODULE(PatPhotonSelectorByValueMap);
