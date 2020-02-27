#include "MiniAODL1CandProducer.h"
  
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Photon.h"

typedef MiniAODL1CandProducer<pat::Electron> PatElectronL1CandProducer;
DEFINE_FWK_MODULE(PatElectronL1CandProducer);

typedef MiniAODL1CandProducer<pat::Photon> PatPhotonL1CandProducer;
DEFINE_FWK_MODULE(PatPhotonL1CandProducer);

