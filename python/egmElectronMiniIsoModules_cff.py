import FWCore.ParameterSet.Config as cms

###################################################################
## ID MODULES
###################################################################

def addMiniIso(process, options):

    from RecoEgamma.EgammaIsolationAlgos.egmGedGsfElectronMiniIsolation_cfi import egmGedGsfElectronMiniNoPileUpIsolation
    process.probeEleMiniIso = egmGedGsfElectronMiniNoPileUpIsolation.clone()
    process.probeEleMiniIso.srcToIsolate = cms.InputTag(options['ELECTRON_COLL'])
    process.probeEleMiniIso.srcForIsolationCone = cms.InputTag("packedPFCandidates")
    process.probeEleMiniIso.isolationConeDefinitions[1].ktScale = cms.double(10.)

    from RecoEgamma.EgammaIsolationAlgos.egmGedGsfElectronMiniIsolation_cfi import egmGedGsfElectronEffAreaMiniIsolation
    process.probeEleMiniIsoEffArea = egmGedGsfElectronEffAreaMiniIsolation.clone()
    process.probeEleMiniIsoEffArea.srcToIsolate = cms.InputTag(options['ELECTRON_COLL'])
    process.probeEleMiniIsoEffArea.isolationConeDefinitions[0].effAreaFile = cms.FileInPath("RecoEgamma/ElectronIdentification/data/Summer16/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_80X.txt")

