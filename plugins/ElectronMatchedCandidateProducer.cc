#include "ElectronMatchedCandidateProducer.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"


typedef ElectronMatchedCandidateProducer<reco::GsfElectron> GsfElectronMatchedCandidateProducer;
DEFINE_FWK_MODULE(GsfElectronMatchedCandidateProducer);

typedef ElectronMatchedCandidateProducer<pat::Electron> PatElectronMatchedCandidateProducer;
DEFINE_FWK_MODULE(PatElectronMatchedCandidateProducer);

