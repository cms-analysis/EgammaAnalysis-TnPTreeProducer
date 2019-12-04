#include "MiniAODL1Stage2CandProducer.h"
          
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Photon.h"

typedef MiniAODL1Stage2CandProducer<pat::Electron> PatElectronL1Stage2CandProducer;
DEFINE_FWK_MODULE(PatElectronL1Stage2CandProducer);

typedef MiniAODL1Stage2CandProducer<reco::GsfElectron> GsfElectronL1Stage2CandProducer;
DEFINE_FWK_MODULE(GsfElectronL1Stage2CandProducer);

//typedef MiniAODL1CandProducer<pat::Photon> PatPhotonL1CandProducer;
//DEFINE_FWK_MODULE(PatPhotonL1CandProducer);

