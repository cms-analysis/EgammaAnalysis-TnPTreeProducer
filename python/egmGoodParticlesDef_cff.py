import FWCore.ParameterSet.Config as cms



def calibrateEGM(process, options ):
    
    ### apply 80X regression
    from EgammaAnalysis.ElectronTools.regressionWeights_cfi import regressionWeights
    process = regressionWeights(process)

    process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
                                                       calibratedPatElectrons  = cms.PSet( initialSeed = cms.untracked.uint32(81),
                                                                                           engineName = cms.untracked.string('TRandom3'),                
                                                                                           ),
                                                       calibratedPatPhotons    = cms.PSet( initialSeed = cms.untracked.uint32(81),
                                                                                           engineName = cms.untracked.string('TRandom3'),                
                                                                                           ),
                                                       )

    process.load('EgammaAnalysis.ElectronTools.regressionApplication_cff')
    process.load('EgammaAnalysis.ElectronTools.calibratedPatElectronsRun2_cfi')
    process.load('EgammaAnalysis.ElectronTools.calibratedPatPhotonsRun2_cfi')

    process.calibratedPatElectrons.electrons = cms.InputTag(options['ELECTRON_COLL'])
    process.calibratedPatPhotons.photons     = cms.InputTag(options['PHOTON_COLL']  )
    if options['isMC']:
        process.calibratedPatElectrons.isMC = cms.bool(True)
        process.calibratedPatPhotons.isMC   = cms.bool(True)
    else :
        process.calibratedPatElectrons.isMC = cms.bool(False)
        process.calibratedPatPhotons.isMC   = cms.bool(False)


    
    process.selectElectronsBase = cms.EDFilter("PATElectronSelector",
                                               src = cms.InputTag('calibratedPatElectrons'),
                                               cut = cms.string(  options['ELECTRON_CUTS']),
                                               )

    process.selectPhotonsBase   = cms.EDFilter("PATPhotonSelector",
                                               src = cms.InputTag('calibratedPatPhotons' ),
                                               cut = cms.string(options['PHOTON_CUTS']),
                                               )

    ### change the input collection to be the calibrated energy one for all other modules from now on
    options['ELECTRON_COLL'] = 'selectElectronsBase'
    options['PHOTON_COLL']   = 'selectPhotonsBase'




###################################################################################
################  --- GOOD particles MiniAOD
################################################################################### 
def setGoodParticlesMiniAOD(process, options):

    if options['UseCalibEn']:  calibrateEGM( process, options )


    ########################### Extra variables for SUSY IDs ############
    if options['addSUSY']: 
        import EgammaAnalysis.TnPTreeProducer.electronsExtrasSUSY_cff  as eleSusyID
        eleSusyID.addSusyIDs( process, options )
        options['ELECTRON_COLL']        = "slimmedElectronsWithUserData"

    process.eleVarHelper = cms.EDProducer("PatElectronVariableHelper",
                                          probes           = cms.InputTag(options['ELECTRON_COLL']),
                                          l1EGColl         = cms.InputTag('caloStage2Digis:EGamma'),
                                          vertexCollection = cms.InputTag("offlineSlimmedPrimaryVertices"),
                                          #pfCandColl       = cms.InputTag("packedPFCandidates"),
                                          )

    ####################  Electron collection
    process.goodElectrons = cms.EDFilter("PATElectronRefSelector",
                                         src = cms.InputTag( options['ELECTRON_COLL'] ),
                                         cut = cms.string(   options['ELECTRON_CUTS'] ),
                                         )
    
    ####################  Photon collection
    process.goodPhotons   =  cms.EDFilter("PATPhotonRefSelector",
                                            src = cms.InputTag( options['PHOTON_COLL'] ),
                                            cut = cms.string(   options['PHOTON_CUTS'] )
                                            )

    
    #################### SUPERCLUSTER collections                                                                 
    process.superClusterCands = cms.EDProducer("ConcreteEcalCandidateProducer",
                                               src = cms.InputTag(options['SUPERCLUSTER_COLL']),
                                               particleType = cms.int32(11),
                                               )
    
    process.goodSuperClusters = cms.EDFilter("RecoEcalCandidateRefSelector",
                                             src = cms.InputTag("superClusterCands"),
                                             cut = cms.string(options['SUPERCLUSTER_CUTS']),
                                             filter = cms.bool(True)
                                             )


    process.sc_sequenceMiniAOD = cms.Sequence(
        process.superClusterCands +
        process.goodSuperClusters 
        )

###################################################################################
################  --- GOOD particles AOD
################################################################################### 
def setGoodParticlesAOD(process, options):


    process.eleVarHelper = cms.EDProducer("GsfElectronVariableHelper",
                                          probes      = cms.InputTag(options['ELECTRON_COLL']),
                                          vertexCollection = cms.InputTag("offlinePrimaryVertices"),
                                          l1EGColl    = cms.InputTag("caloStage2Digis:EGamma"),
                                          #pfCandColl  = cms.InputTag("particleFlow"),
                                          )

    process.hltVarHelper = cms.EDProducer("GsfElectronHLTVariableHelper",
                                            probes = cms.InputTag(options['ELECTRON_COLL']),
                                            hltCandidateCollection = cms.InputTag("hltEgammaCandidates"),
                                            mapOutputNames = cms.vstring("hltsieie",
                                                                        "hltecaliso",
                                                                        "hlthcaliso",
                                                                        "hlthoe",
                                                                        "hlttkiso",
                                                                        "hltdeta",
                                                                        "hltdetaseed",
                                                                        "hltdphi",
                                                                        "hlteop",
                                                                        "hltmishits"),
                                            mapInputTags = cms.VInputTag("hltEgammaClusterShape:sigmaIEtaIEta5x5",
                                                                        "hltEgammaEcalPFClusterIso",
                                                                        "hltEgammaHcalPFClusterIso",
                                                                        "hltEgammaHoverE", 
                                                                        "hltEgammaEleGsfTrackIso",
                                                                        "hltEgammaGsfTrackVars:Deta",
                                                                        "hltEgammaGsfTrackVars:DetaSeed",
                                                                        "hltEgammaGsfTrackVars:Dphi",
                                                                        "hltEgammaGsfTrackVars:OneOESuperMinusOneOP",
                                                                        "hltEgammaGsfTrackVars:MissingHits")
                                            )




   

    ####################  Electron collection
    process.goodElectrons = cms.EDFilter("GsfElectronRefSelector",
                                         src = cms.InputTag(options['ELECTRON_COLL']),
                                         cut = cms.string(options['ELECTRON_CUTS'])
                                         )

    ####################  Photon collection
    ### dummy in AOD (use miniAOD for photons)
    process.goodPhotons    =  cms.EDFilter("PhotonRefSelector",
                                            src = cms.InputTag( options['PHOTON_COLL'] ),
                                            cut = cms.string(   options['PHOTON_CUTS'] )
                                            )
    
    #################### SUPERCLUSTER collections                                                                 
    process.superClusterMerger =  cms.EDProducer("EgammaSuperClusterMerger",
                                                 src = cms.VInputTag(cms.InputTag("particleFlowSuperClusterECAL:particleFlowSuperClusterECALBarrel"),
                                                                     cms.InputTag("particleFlowSuperClusterECAL:particleFlowSuperClusterECALEndcapWithPreshower"),
#                                                                     cms.InputTag("particleFlowEGamma"),
                                                                     ),
                                                 )
    
    
    process.superClusterCands = cms.EDProducer("ConcreteEcalCandidateProducer",
                                               src = cms.InputTag("superClusterMerger"),
                                               particleType = cms.int32(11),
                                               )
    
    process.goodSuperClusters = cms.EDFilter("RecoEcalCandidateRefSelector",
                                             src = cms.InputTag("superClusterCands"),
                                             cut = cms.string(options['SUPERCLUSTER_CUTS']),
                                             filter = cms.bool(True)
                                             )


    process.recoEcalCandidateHelper = cms.EDProducer("RecoEcalCandidateVariableHelper",
                                                     probes = cms.InputTag("superClusterCands"),
                                                     countTracks = cms.bool( False ),
                                                     trkIsoPtMin = cms.double( 0.5 ),
                                                     trkIsoStripEndcap = cms.double( 0.03 ),
                                                     trackProducer = cms.InputTag( "generalTracks" ),
                                                     trkIsoStripBarrel = cms.double( 0.03 ),
                                                     trkIsoConeSize = cms.double( 0.4 ),
                                                     trkIsoVetoConeSize = cms.double( 0.06 ),
                                                     trkIsoRSpan = cms.double( 999999.0 ),
                                                     trkIsoZSpan = cms.double( 999999. )
                                                     )
    process.sc_sequenceAOD = cms.Sequence(
        process.superClusterMerger      +
        process.superClusterCands       +
        process.recoEcalCandidateHelper +
        process.goodSuperClusters     
        )
