import FWCore.ParameterSet.Config as cms


###################################################################################
################  --- TAG AND PROBE collections
###################################################################################
import EgammaAnalysis.TnPTreeProducer.egmGoodParticlesDef_cff as goodPartDef

def setTagsProbes(process, options):

    eleHLTProducer = 'PatElectronTriggerCandProducer'
    gamHLTProducer = 'PatPhotonTriggerCandProducer'
    hltObjects     = 'selectedPatTrigger' if options['era'] == '2016' else 'slimmedPatTrigger'
    genParticles   = 'prunedGenParticles'
    SCEleMatcher   = 'PatElectronMatchedCandidateProducer' 

    if (options['useAOD']):
        eleHLTProducer = 'GsfElectronTriggerCandProducer'
        gamHLTProducer = 'PhotonTriggerCandProducer'
        hltObjects     = 'hltTriggerSummaryAOD'
        genParticles   = 'genParticles'
        SCEleMatcher   = 'GsfElectronMatchedCandidateProducer' 
        goodPartDef.setGoodParticlesAOD(     process, options )

    else:
        goodPartDef.setGoodParticlesMiniAOD( process, options )
        
        
    ####################### TAG ELECTRON ############################
    process.tagEle = cms.EDProducer(eleHLTProducer,
                                        filterNames = cms.vstring(options['TnPHLTTagFilters']),
                                        inputs      = cms.InputTag("tagEleCutBasedTight"),
                                        bits        = cms.InputTag('TriggerResults::' + options['HLTProcessName']),
                                        objects     = cms.InputTag(hltObjects),
                                        dR          = cms.double(0.3),
                                        isAND       = cms.bool(True)
                                    )

    ##################### PROBE ELECTRONs ###########################
    process.probeEle             = process.tagEle.clone()
    process.probeEle.filterNames = cms.vstring(options['TnPHLTProbeFilters'])
    process.probeEle.inputs      = cms.InputTag("goodElectrons")

    ################# PROBE ELECTRONs passHLT #######################
    process.probeElePassHLT        = process.tagEle.clone()
    process.probeElePassHLT.inputs = cms.InputTag("probeEle")
    process.probeElePassHLT.isAND  = cms.bool(False)

    ################# PROBE Matched to L1 #######################
    if options['ApplyL1Matching']:
      print "L1 matching will be applied for some HLTFILTERSTOMEASURE"
      process.goodElectronProbesL1 = cms.EDProducer("PatElectronL1Stage2CandProducer",
                                                  inputs       = cms.InputTag("goodElectrons"),
                                                  objects      = cms.InputTag("caloStage2Digis:EGamma"),
                                                  minET        = cms.double(options['L1Threshold']), #lead eff only
                                                  dRmatch      = cms.double(0.2), #match L1 online to hlt in EB
                                                  dRmatchEE    = cms.double(0.2), #match L1 online to hlt in EE
                                                  isolatedOnly = cms.bool(False)
      )
      process.probeEleL1matched               = process.probeEle.clone()
      process.probeEleL1matched.inputs        = cms.InputTag("goodElectronProbesL1")
      process.probeElePassHLTL1matched        = process.probeElePassHLT.clone()
      process.probeElePassHLTL1matched.inputs = cms.InputTag("probeEleL1matched")

    for flag, filterNames in options['HLTFILTERSTOMEASURE'].iteritems():
      if 'L1match' in flag: setattr(process, flag, process.probeElePassHLTL1matched.clone(filterNames=filterNames))
      else:                 setattr(process, flag, process.probeElePassHLT.clone(filterNames=filterNames))

    ###################### PROBE PHOTONs ############################
    process.probePho  = cms.EDProducer( gamHLTProducer,
                                        filterNames = options['TnPHLTProbeFilters'],
                                        inputs      = cms.InputTag("goodPhotons"),
                                        bits        = cms.InputTag('TriggerResults::' + options['HLTProcessName'] ),
                                        objects     = cms.InputTag(hltObjects),
                                        dR          = cms.double(0.3),
                                        isAND       = cms.bool(True)
                                        )
    if options['useAOD'] : process.probePho = process.goodPhotons.clone()
    
    ######################### PROBE SCs #############################    
    process.probeSC     = cms.EDProducer("RecoEcalCandidateTriggerCandProducer",
                                            filterNames  = cms.vstring(options['TnPHLTProbeFilters']),
                                             inputs       = cms.InputTag("goodSuperClusters"),
                                             bits         = cms.InputTag('TriggerResults::' + options['HLTProcessName']),
                                             objects      = cms.InputTag(hltObjects),
                                             dR           = cms.double(0.3),
                                             isAND        = cms.bool(True)
                                        )
       
    process.probeSCEle = cms.EDProducer( SCEleMatcher,
                                            src     = cms.InputTag("superClusterCands"),
                                            ReferenceElectronCollection = cms.untracked.InputTag("goodElectrons"),
                                            cut = cms.string(options['SUPERCLUSTER_CUTS'])
                                        )

    ########################## gen tag & probes ######################
    if options['isMC'] :
        cut_gen_standard = 'abs(pdgId) == 11 && pt > 3 && abs(eta) < 2.7 && isPromptFinalState'
        cut_gen_flashgg  = 'abs(pdgId) == 11 && pt > 3 && abs(eta) < 2.7 && ( isPromptFinalState || status == 23)'
        cut_gen_tau      = 'abs(pdgId) == 11 && pt > 3 && abs(eta) < 2.7 && ( isPromptFinalState || isDirectPromptTauDecayProductFinalState) '
        
        process.genEle   = cms.EDFilter( "GenParticleSelector",
                                          src = cms.InputTag(genParticles), 
                                          cut = cms.string(cut_gen_standard),
                                          )

        process.genTagEle = cms.EDProducer("MCMatcher",
                                            src      = cms.InputTag("tagEle"),
                                            matched  = cms.InputTag("genEle"),
                                            mcStatus = cms.vint32(),
                                            mcPdgId  = cms.vint32(),
                                            checkCharge = cms.bool(False),
                                            maxDeltaR   = cms.double(0.20),   # Minimum deltaR for the match
                                            maxDPtRel   = cms.double(50.0),    # Minimum deltaPt/Pt for the match
                                            resolveAmbiguities    = cms.bool(False), # Forbid two RECO objects to match to the same GEN objec
                                            resolveByMatchQuality = cms.bool(True),  # False = just match input in order; True = pick lowest deltaR pair first
                                            )        
        
        process.genProbeEle  = process.genTagEle.clone( src = cms.InputTag("probeEle") )
        process.genProbePho  = process.genTagEle.clone( src = cms.InputTag("probePho") )
        process.genProbeSC   = process.genTagEle.clone( src = cms.InputTag("probeSC")  )
    
        
    ########################### TnP pairs ############################
    masscut = cms.string("50<mass<130")         
    process.tnpPairingEleHLT   = cms.EDProducer("CandViewShallowCloneCombiner",
                                        decay = cms.string("tagEle@+ probeEle@-"), 
                                        checkCharge = cms.bool(True),
                                        cut = masscut,
                                        )
    
    process.tnpPairingEleRec             = process.tnpPairingEleHLT.clone()
    process.tnpPairingEleRec.decay       = cms.string("tagEle probeSC" ) 
    process.tnpPairingEleRec.checkCharge = cms.bool(False)
    
    process.tnpPairingEleIDs             = process.tnpPairingEleHLT.clone()
    process.tnpPairingEleIDs.decay       = cms.string("tagEle probeEle")
    process.tnpPairingEleIDs.checkCharge = cms.bool(False)

    process.tnpPairingPhoIDs             = process.tnpPairingEleHLT.clone()
    process.tnpPairingPhoIDs.decay       = cms.string("tagEle probePho")
    process.tnpPairingPhoIDs.checkCharge = cms.bool(False)

    ######################## probe passing ID ##########################
    import EgammaAnalysis.TnPTreeProducer.egmElectronIDModules_cff as egmEleID
    import EgammaAnalysis.TnPTreeProducer.egmPhotonIDModules_cff   as egmPhoID
    egmEleID.setIDs(process, options)
    egmPhoID.setIDs(process, options)

###################################################################################
################  --- SEQUENCES
###################################################################################      
def setSequences(process, options):

    process.init_sequence = cms.Sequence()
    if options['UseCalibEn']:
        process.enCalib_sequence = cms.Sequence(
            process.regressionApplication  *
            process.calibratedPatElectrons *
            process.calibratedPatPhotons   *
            process.selectElectronsBase    *
            process.selectPhotonsBase      
            )
        process.init_sequence += process.enCalib_sequence

    if options['addSUSY'] : process.init_sequence += process.susy_sequence
    process.init_sequence += process.egmGsfElectronIDSequence
    process.init_sequence += process.eleVarHelper 
    if options['addSUSY'] : process.init_sequence += process.susy_sequence_requiresVID



    process.sc_sequence  = cms.Sequence( )
    process.ele_sequence = cms.Sequence( )
    process.pho_sequence = cms.Sequence( )
    process.hlt_sequence = cms.Sequence( process.hltFilter )
    
    process.tag_sequence = cms.Sequence(
        process.goodElectrons             +
        process.tagEleCutBasedTight       +
        process.tagEle 
        )



    if options['useAOD'] : process.sc_sequence += process.sc_sequenceAOD
    else :                 process.sc_sequence += process.sc_sequenceMiniAOD
    process.sc_sequence += process.probeSC
    process.sc_sequence += process.probeSCEle

    # TODO: shorten this code in a similar way as is done for the hltfilters below
    process.ele_sequence = cms.Sequence(
#        process.probeEleCutBasedVeto      +
#        process.probeEleCutBasedLoose     +
#        process.probeEleCutBasedMedium    +
#        process.probeEleCutBasedTight     +
        process.probeEleCutBasedVeto80X   +
        process.probeEleCutBasedLoose80X  +
        process.probeEleCutBasedMedium80X +
        process.probeEleCutBasedTight80X  +
        process.probeEleMVA80Xwp90        +
        process.probeEleMVA80Xwp80        +
        process.probeEleCutBasedVeto94X   +
        process.probeEleCutBasedLoose94X  +
        process.probeEleCutBasedMedium94X +
        process.probeEleCutBasedTight94X  +

        process.probeEleCutBasedVeto94XV2   +
        process.probeEleCutBasedLoose94XV2  +
        process.probeEleCutBasedMedium94XV2 +
        process.probeEleCutBasedTight94XV2  +

        process.probeEleCutBasedVeto94XV2MinPtCut   +
        process.probeEleCutBasedLoose94XV2MinPtCut  +
        process.probeEleCutBasedMedium94XV2MinPtCut +
        process.probeEleCutBasedTight94XV2MinPtCut  +

        process.probeEleCutBasedVeto94XV2GsfEleSCEtaMultiRangeCut   +
        process.probeEleCutBasedLoose94XV2GsfEleSCEtaMultiRangeCut  +
        process.probeEleCutBasedMedium94XV2GsfEleSCEtaMultiRangeCut +
        process.probeEleCutBasedTight94XV2GsfEleSCEtaMultiRangeCut  +

        process.probeEleCutBasedVeto94XV2GsfEleDEtaInSeedCut   +
        process.probeEleCutBasedLoose94XV2GsfEleDEtaInSeedCut  +
        process.probeEleCutBasedMedium94XV2GsfEleDEtaInSeedCut +
        process.probeEleCutBasedTight94XV2GsfEleDEtaInSeedCut  +

        process.probeEleCutBasedVeto94XV2GsfEleDPhiInCut   +
        process.probeEleCutBasedLoose94XV2GsfEleDPhiInCut  +
        process.probeEleCutBasedMedium94XV2GsfEleDPhiInCut +
        process.probeEleCutBasedTight94XV2GsfEleDPhiInCut  +

        process.probeEleCutBasedVeto94XV2GsfEleFull5x5SigmaIEtaIEtaCut   +
        process.probeEleCutBasedLoose94XV2GsfEleFull5x5SigmaIEtaIEtaCut  +
        process.probeEleCutBasedMedium94XV2GsfEleFull5x5SigmaIEtaIEtaCut +
        process.probeEleCutBasedTight94XV2GsfEleFull5x5SigmaIEtaIEtaCut  +

        process.probeEleCutBasedVeto94XV2GsfEleHadronicOverEMEnergyScaledCut   +
        process.probeEleCutBasedLoose94XV2GsfEleHadronicOverEMEnergyScaledCut  +
        process.probeEleCutBasedMedium94XV2GsfEleHadronicOverEMEnergyScaledCut +
        process.probeEleCutBasedTight94XV2GsfEleHadronicOverEMEnergyScaledCut  +

        process.probeEleCutBasedVeto94XV2GsfEleEInverseMinusPInverseCut   +
        process.probeEleCutBasedLoose94XV2GsfEleEInverseMinusPInverseCut  +
        process.probeEleCutBasedMedium94XV2GsfEleEInverseMinusPInverseCut +
        process.probeEleCutBasedTight94XV2GsfEleEInverseMinusPInverseCut  +

        process.probeEleCutBasedVeto94XV2GsfEleRelPFIsoScaledCut   +
        process.probeEleCutBasedLoose94XV2GsfEleRelPFIsoScaledCut  +
        process.probeEleCutBasedMedium94XV2GsfEleRelPFIsoScaledCut +
        process.probeEleCutBasedTight94XV2GsfEleRelPFIsoScaledCut  +

        process.probeEleCutBasedVeto94XV2GsfEleConversionVetoCut   +
        process.probeEleCutBasedLoose94XV2GsfEleConversionVetoCut  +
        process.probeEleCutBasedMedium94XV2GsfEleConversionVetoCut +
        process.probeEleCutBasedTight94XV2GsfEleConversionVetoCut  +

        process.probeEleCutBasedVeto94XV2GsfEleMissingHitsCut   +
        process.probeEleCutBasedLoose94XV2GsfEleMissingHitsCut  +
        process.probeEleCutBasedMedium94XV2GsfEleMissingHitsCut +
        process.probeEleCutBasedTight94XV2GsfEleMissingHitsCut  +

        process.probeEleMVA94XwpLnoiso        +
        process.probeEleMVA94Xwp90noiso        +
        process.probeEleMVA94Xwp80noiso        +
        process.probeEleMVA94XwpLiso        +
        process.probeEleMVA94Xwp90iso        +
        process.probeEleMVA94Xwp80iso        +
        process.probeEleMVA94XwpLnoisoV2        +
        process.probeEleMVA94Xwp90noisoV2        +
        process.probeEleMVA94Xwp80noisoV2        +
        process.probeEleMVA94XwpLisoV2        +
        process.probeEleMVA94Xwp90isoV2        +
        process.probeEleMVA94Xwp80isoV2        +
        process.probeEleMVA94XwpHZZisoV2 +
        process.probeEle
        )

    if options['ApplyL1Matching']:
      process.ele_sequence += process.goodElectronProbesL1
      process.ele_sequence += process.probeEleL1matched

    if not options['useAOD'] : process.ele_sequence += process.probeEleHLTsafe
    if not options['useAOD'] : process.ele_sequence += process.probeDoubleEleHLTsafe

    process.pho_sequence = cms.Sequence(
        process.goodPhotons               +
        process.egmPhotonIDSequence       +
        #process.probePhoCutBasedLoose     +
        #process.probePhoCutBasedMedium    +
        #process.probePhoCutBasedTight     +
        #process.probePhoMVA               +
        process.probePhoCutBasedLoose80X  +
        process.probePhoCutBasedMedium80X +
        process.probePhoCutBasedTight80X  +
        process.probePhoMVA80Xwp90       +
        process.probePhoMVA80Xwp80       +
        process.probePhoCutBasedLoose94X  +
        process.probePhoCutBasedMedium94X +
        process.probePhoCutBasedTight94X  +
        process.probePhoCutBasedLoose100XV2  +
        process.probePhoCutBasedMedium100XV2 +
        process.probePhoCutBasedTight100XV2  +
        process.probePhoCutBasedLoose100XV2MinPtCut  +
        process.probePhoCutBasedMedium100XV2MinPtCut +
        process.probePhoCutBasedTight100XV2MinPtCut  +
        process.probePhoCutBasedLoose100XV2PhoSCEtaMultiRangeCut  +
        process.probePhoCutBasedMedium100XV2PhoSCEtaMultiRangeCut +
        process.probePhoCutBasedTight100XV2PhoSCEtaMultiRangeCut  +
        process.probePhoCutBasedLoose100XV2PhoSingleTowerHadOverEmCut  +
        process.probePhoCutBasedMedium100XV2PhoSingleTowerHadOverEmCut +
        process.probePhoCutBasedTight100XV2PhoSingleTowerHadOverEmCut  +

        process.probePhoCutBasedLoose100XV2PhoFull5x5SigmaIEtaIEtaCut  +
        process.probePhoCutBasedMedium100XV2PhoFull5x5SigmaIEtaIEtaCut +
        process.probePhoCutBasedTight100XV2PhoFull5x5SigmaIEtaIEtaCut  +

        process.probePhoCutBasedLoose100XV2PhoAnyPFIsoWithEACut  +
        process.probePhoCutBasedMedium100XV2PhoAnyPFIsoWithEACut +
        process.probePhoCutBasedTight100XV2PhoAnyPFIsoWithEACut  +

        process.probePhoCutBasedLoose100XV2PhoAnyPFIsoWithEAAndQuadScalingCut  +
        process.probePhoCutBasedMedium100XV2PhoAnyPFIsoWithEAAndQuadScalingCut +
        process.probePhoCutBasedTight100XV2PhoAnyPFIsoWithEAAndQuadScalingCut  +

        process.probePhoCutBasedLoose100XV2PhoAnyPFIsoWithEACut1  +
        process.probePhoCutBasedMedium100XV2PhoAnyPFIsoWithEACut1 +
        process.probePhoCutBasedTight100XV2PhoAnyPFIsoWithEACut1  +

        process.probePhoMVA94Xwp90       +
        process.probePhoMVA94Xwp80       +
        process.probePhoMVA94XV2wp90       +
        process.probePhoMVA94XV2wp80       +
        process.probePho                
        )

    process.hlt_sequence = cms.Sequence()
    for flag in options['HLTFILTERSTOMEASURE']:
        process.hlt_sequence += getattr(process, flag)

    if options['isMC'] :
        process.tag_sequence += process.genEle + process.genTagEle 
        process.ele_sequence += process.genProbeEle
        process.pho_sequence += process.genProbePho
        process.sc_sequence  += process.genProbeSC

            
###################################################################################
################  --- tree Maker setup
###################################################################################
def setupTreeMaker(process, options) :
    from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
    process.hltFilter = hltHighLevel.clone()
    process.hltFilter.throw = cms.bool(True)
    process.hltFilter.HLTPaths = options['TnPPATHS']
    process.hltFilter.TriggerResultsTag = cms.InputTag("TriggerResults","",options['HLTProcessName'])

    setTagsProbes( process, options )
    setSequences(  process, options )

    
def customize( tnpTree, options ):
    tnpTree.arbitration = cms.string("HighestPt")
    if options['isMC'] :
        tnpTree.isMC = cms.bool( True ) 
        tnpTree.eventWeight = cms.InputTag("generator")
        tnpTree.PUWeightSrc = cms.InputTag("pileupReweightingProducer","pileupWeights")
    else:
        tnpTree.isMC = cms.bool( False ) 
 
