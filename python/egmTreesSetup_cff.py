import FWCore.ParameterSet.Config as cms


###################################################################################
################  --- TAG AND PROBE collections
###################################################################################
import EgammaAnalysis.TnPTreeProducer.egmGoodParticlesDef_cff as goodPartDef

def setTagsProbes(process, options):

    eleHLTProducer = 'PatElectronTriggerCandProducer'
    gamHLTProducer = 'PatPhotonTriggerCandProducer'
    hltObjects     = 'slimmedPatTrigger' # 'selectedPatTrigger' FOR 2016
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
    process.probeElePassHLT              = process.tagEle.clone()
    process.probeElePassHLT.inputs       = cms.InputTag("probeEle")  
    process.probeElePassHLT.filterNames  = cms.vstring(options['HLTFILTERTOMEASURE'])
    process.probeElePassHLT.isAND        = cms.bool(False)

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
        process.probeEleMVA94XwpLnoiso        +
        process.probeEleMVA94Xwp90noiso        +
        process.probeEleMVA94Xwp80noiso        +
        process.probeEleMVA94XwpLiso        +
        process.probeEleMVA94Xwp90iso        +
        process.probeEleMVA94Xwp80iso        +
        process.probeEle 
        )
    if not options['useAOD'] : process.ele_sequence += process.probeEleHLTsafe

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
        process.probePhoMVA94Xwp90       +
        process.probePhoMVA94Xwp80       +
        process.probePho                
        )

    process.hlt_sequence = cms.Sequence( process.probeElePassHLT )

    if options['isMC'] :
        process.tag_sequence += process.genEle + process.genTagEle 
        process.ele_sequence += process.genProbeEle
        process.pho_sequence += process.genProbePho
        process.sc_sequence  += process.genProbeSC

    from EgammaAnalysis.TnPTreeProducer.pileupConfiguration_cfi import pileupProducer
    process.pileupReweightingProducer = pileupProducer.clone()
    if options['useAOD']: process.pileupReweightingProducer.pileupInfoTag = "addPileupInfo"

    process.mc_sequence = cms.Sequence()
    if options['isMC'] : process.mc_sequence = cms.Sequence( process.pileupReweightingProducer )
            
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
 
