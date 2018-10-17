import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
import sys

process = cms.Process("tnpEGM")

###################################################################
## argument line options
###################################################################
varOptions = VarParsing('analysis')

varOptions.register(
    "isMC", False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Compute MC efficiencies"
    )

varOptions.register(
    "doEleID", True,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Include tree for photon ID SF"
    )

varOptions.register(
    "doPhoID", True,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Include tree for photon ID SF"
    )

varOptions.register(
    "doTrigger", False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Include tree for Trigger SF"
    )

varOptions.register(
    "doRECO", False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Include tree for Reco SF"
    )

varOptions.register(
    "calibEn", False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "use EGM smearer to calibrate photon and electron energy"
    )

#### HLTname is HLT2 in reHLT samples
varOptions.register(
    "HLTname", "HLT",
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "HLT process name (default HLT)"
    )

varOptions.register(
    #"GT","auto",
    "GT","101X_dataRun2_Prompt_v9",
    #"GT","94X_dataRun2_ReReco_EOY17_v6",
    #"GT","80X_dataRun2_2016LegacyRepro_v4",
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "Global Tag to be used"
    )

varOptions.register(
    "includeSUSY", False,
#    "isAOD", True,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "add also the variables used by SUSY"
    )

varOptions.register(
    "isAOD", True,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "use AOD"
    )

varOptions.parseArguments()


###################################################################
## Define TnP inputs 
###################################################################

options = dict()
options['useAOD']               = cms.bool(varOptions.isAOD)

options['HLTProcessName']       = varOptions.HLTname

### set input collections
options['ELECTRON_COLL']        = "slimmedElectrons"
options['PHOTON_COLL']          = "slimmedPhotons"
options['SUPERCLUSTER_COLL']    = "reducedEgamma:reducedSuperClusters" ### not used in AOD
if options['useAOD']:
    options['ELECTRON_COLL']    = "gedGsfElectrons"
    options['PHOTON_COLL'  ]    = "gedPhotons"


options['ELECTRON_CUTS']        = "ecalEnergy*sin(superClusterPosition.theta)>5.0 &&  (abs(-log(tan(superClusterPosition.theta/2)))<2.5)"
options['SUPERCLUSTER_CUTS']    = "abs(eta)<2.5 &&  et>5.0"
options['PHOTON_CUTS']          = "(abs(-log(tan(superCluster.position.theta/2)))<=2.5) && pt> 10"
options['ELECTRON_TAG_CUTS']    = "(abs(-log(tan(superCluster.position.theta/2)))<=2.1) && !(1.4442<=abs(-log(tan(superClusterPosition.theta/2)))<=1.566) && pt >= 30.0"

options['MAXEVENTS']            = cms.untracked.int32(varOptions.maxEvents) 
#options['MAXEVENTS']            = 2000
options['DoTrigger']            = cms.bool( varOptions.doTrigger )
options['DoRECO']               = cms.bool( varOptions.doRECO    )
options['DoEleID']              = cms.bool( varOptions.doEleID   )
options['DoPhoID']              = cms.bool( varOptions.doPhoID   )

options['OUTPUTEDMFILENAME']    = 'edmFile.root'
options['DEBUG']                = cms.bool(False)
options['isMC']                 = cms.bool(False)
options['UseCalibEn']           = varOptions.calibEn

options['addSUSY']               = varOptions.includeSUSY
if options['useAOD']: 
    options['addSUSY']               = cms.bool(False)

if (varOptions.isMC):
    options['isMC']                = cms.bool(True)
    options['OUTPUT_FILE_NAME']    = "TnPTree_mc.root"
    if varOptions.isAOD :  options['OUTPUT_FILE_NAME']    = "TnPTree_mc_aod.root"
#    options['TnPPATHS']            = cms.vstring("HLT*")
#    options['TnPHLTTagFilters']    = cms.vstring()
#    options['TnPHLTProbeFilters']  = cms.vstring()
#    options['HLTFILTERTOMEASURE']  = cms.vstring("")
#    options['TnPPATHS']            = cms.vstring("HLT_Ele27_eta2p1_WPTight_Gsf_v*") #FOR 2016
#    options['TnPHLTTagFilters']    = cms.vstring("hltEle27erWPTightGsfTrackIsoFilter") #FOR 2016
#    options['HLTFILTERTOMEASURE']  = cms.vstring("hltEle27erWPTightGsfTrackIsoFilter") #FOR 2016
    options['TnPPATHS']            = cms.vstring("HLT_Ele32_WPTight_Gsf_L1DoubleEG_v*")
    options['TnPHLTTagFilters']    = cms.vstring("hltEle32L1DoubleEGWPTightGsfTrackIsoFilter","hltEGL1SingleEGOrFilter")
    #options['TnPHLTTagFilters']    = cms.vstring("hltEle32L1DoubleEGWPTightGsfTrackIsoFilter")
    options['TnPHLTProbeFilters']  = cms.vstring()
    options['HLTFILTERTOMEASURE']  = cms.vstring("hltEle32L1DoubleEGWPTightGsfTrackIsoFilter")
    options['GLOBALTAG']           = 'auto:run2_mc'
else:
    options['OUTPUT_FILE_NAME']    = "TnPTree_data.root"
#    options['TnPPATHS']            = cms.vstring("HLT_Ele27_eta2p1_WPTight_Gsf_v*") #FOR 2016
#    options['TnPHLTTagFilters']    = cms.vstring("hltEle27erWPTightGsfTrackIsoFilter") #FOR 2016
    options['TnPPATHS']            = cms.vstring("HLT_Ele32_WPTight_Gsf_L1DoubleEG_v*")
    options['TnPHLTTagFilters']    = cms.vstring("hltEle32L1DoubleEGWPTightGsfTrackIsoFilter","hltEGL1SingleEGOrFilter")
    #options['TnPHLTTagFilters']    = cms.vstring("hltEle32L1DoubleEGWPTightGsfTrackIsoFilter")
    options['TnPHLTProbeFilters']  = cms.vstring()
    options['HLTFILTERTOMEASURE']  = cms.vstring("hltEle32L1DoubleEGWPTightGsfTrackIsoFilter")
    options['GLOBALTAG']           = 'auto:run2_data'

if varOptions.GT != "auto" :
    options['GLOBALTAG'] = varOptions.GT


###################################################################
## Define input files for test local run
###################################################################
from EgammaAnalysis.TnPTreeProducer.etc.tnpInputTestFiles_cff import filesMiniAOD_Preliminary2018 as inputs
if options['useAOD'] : from EgammaAnalysis.TnPTreeProducer.etc.tnpInputTestFiles_cff import filesAOD_Preliminary2017 as inputs #

#if options['useAOD'] : 
#from EgammaAnalysis.TnPTreeProducer.etc.tnpInputTestFiles_cff import filesAOD_Preliminary2017 as inputs #switch to 2017 samples if want to cmsRun on AOD
#from EgammaAnalysis.TnPTreeProducer.etc.tnpInputTestFiles_cff import filesAOD_2016 as inputs #switch to 2017 samples if want to cmsRun on AOD
#from EgammaAnalysis.TnPTreeProducer.etc.tnpInputTestFiles_cff import filesMiniAOD_2016 as inputs #switch to 2017 samples if want to cmsRun on AOD
#if options['useAOD'] : from EgammaAnalysis.TnPTreeProducer.etc.tnpInputTestFiles_cff import filesAOD_empty as inputs #switch to 2017 samples if want to cmsRun on AOD
    
options['INPUT_FILE_NAME'] = inputs['data']
if varOptions.isMC:  options['INPUT_FILE_NAME'] =  inputs['mc']

#for file in open("file.list").readlines():
#    inputs['data'].append(file.strip())

###################################################################
## import TnP tree maker pythons and configure for AODs
###################################################################
process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
#process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load('Configuration.StandardSequences.Services_cff') 
process.load('FWCore.MessageService.MessageLogger_cfi')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, options['GLOBALTAG'] , '')

import EgammaAnalysis.TnPTreeProducer.egmTreesSetup_cff as tnpSetup
tnpSetup.setupTreeMaker(process,options)



###################################################################
## Init and Load
###################################################################
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

process.MessageLogger.cerr.threshold = ''
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.source = cms.Source("PoolSource",
                            fileNames = options['INPUT_FILE_NAME'],
                            )
process.maxEvents = cms.untracked.PSet( input = options['MAXEVENTS'])
#process.maxEvents = cms.untracked.PSet(
#    input = cms.untracked.int32(options['MAXEVENTS'] )
#)

if options['addSUSY']    : print "  -- Including variables for SUSY       -- "
if options['DoTrigger'] : print "  -- Producing HLT (trigger ele) efficiency tree -- "
if options['DoRECO']    : print "  -- Producing RECO SF tree        -- "
if options['DoEleID']   : print "  -- Producing electron SF tree    -- "
if options['DoPhoID']   : print "  -- Producing photon SF tree      -- "

    
###################################################################
## Define sequences and TnP pairs
###################################################################
process.cand_sequence = cms.Sequence( process.init_sequence + process.tag_sequence )
if options['addSUSY']                         : process.cand_sequence += process.susy_ele_sequence
if options['DoEleID'] or options['DoTrigger'] : process.cand_sequence += process.ele_sequence
if options['DoPhoID']                         : process.cand_sequence += process.pho_sequence
if options['DoTrigger']                       : process.cand_sequence += process.hlt_sequence
if options['DoRECO']                          : process.cand_sequence += process.sc_sequence

process.tnpPairs_sequence = cms.Sequence()
if options['DoTrigger'] : process.tnpPairs_sequence *= process.tnpPairingEleHLT
if options['DoRECO']    : process.tnpPairs_sequence *= process.tnpPairingEleRec
if options['DoEleID']   : process.tnpPairs_sequence *= process.tnpPairingEleIDs
if options['DoPhoID']   : process.tnpPairs_sequence *= process.tnpPairingPhoIDs

##########################################################################
## TnP Trees
##########################################################################
import EgammaAnalysis.TnPTreeProducer.egmTreesContent_cff as tnpVars
if options['useAOD']: tnpVars.setupTnPVariablesForAOD()
tnpVars.mcTruthCommonStuff.isMC = cms.bool(varOptions.isMC)

process.tnpEleTrig = cms.EDAnalyzer("TagProbeFitTreeProducer",
                                    tnpVars.CommonStuffForGsfElectronProbe, tnpVars.mcTruthCommonStuff,
                                    tagProbePairs = cms.InputTag("tnpPairingEleHLT"),
                                    probeMatches  = cms.InputTag("genProbeEle"),
                                    allProbes     = cms.InputTag("probeEle"),
                                    flags = cms.PSet(
                                        passingHLT        = cms.InputTag("probeElePassHLT"),
                                        passingLoose94X   = cms.InputTag("probeEleCutBasedLoose94X" ),
                                        passingMedium94X  = cms.InputTag("probeEleCutBasedMedium94X"),
                                        passingTight94X   = cms.InputTag("probeEleCutBasedTight94X" ),
                                        ),
                                    )

process.tnpEleReco = cms.EDAnalyzer("TagProbeFitTreeProducer",
                                    tnpVars.mcTruthCommonStuff, tnpVars.CommonStuffForSuperClusterProbe, 
                                    tagProbePairs = cms.InputTag("tnpPairingEleRec"),
                                    probeMatches  = cms.InputTag("genProbeSC"),
                                    allProbes     = cms.InputTag("probeSC"),
                                    flags         = cms.PSet(
        passingRECO   = cms.InputTag("probeSCEle", "superclusters"),
        passingRECOEcalDriven   = cms.InputTag("probeSCEle", "superclustersEcalDriven"),
        passingRECOTrackDriven   = cms.InputTag("probeSCEle", "superclustersTrackDriven")
        ),

                                    )

process.tnpEleIDs = cms.EDAnalyzer("TagProbeFitTreeProducer",
                                    tnpVars.mcTruthCommonStuff, tnpVars.CommonStuffForGsfElectronProbe,
                                    tagProbePairs = cms.InputTag("tnpPairingEleIDs"),
                                    probeMatches  = cms.InputTag("genProbeEle"),
                                    allProbes     = cms.InputTag("probeEle"),
                                    flags         = cms.PSet(
#                                        passingVeto       = cms.InputTag("probeEleCutBasedVeto"  ),
#                                        passingLoose      = cms.InputTag("probeEleCutBasedLoose" ),
#                                        passingMedium     = cms.InputTag("probeEleCutBasedMedium"),
        #                                        passingTight      = cms.InputTag("probeEleCutBasedTight" ),
                                        passingVeto80X    = cms.InputTag("probeEleCutBasedVeto80X"  ),
                                        passingLoose80X   = cms.InputTag("probeEleCutBasedLoose80X" ),
                                        passingMedium80X  = cms.InputTag("probeEleCutBasedMedium80X"),
                                        passingTight80X   = cms.InputTag("probeEleCutBasedTight80X" ),
                                        passingMVA80Xwp90 = cms.InputTag("probeEleMVA80Xwp90" ),
                                        passingMVA80Xwp80 = cms.InputTag("probeEleMVA80Xwp80" ),

                                        passingVeto94X    = cms.InputTag("probeEleCutBasedVeto94X"  ),
                                        passingLoose94X   = cms.InputTag("probeEleCutBasedLoose94X" ),
                                        passingMedium94X  = cms.InputTag("probeEleCutBasedMedium94X"),
                                        passingTight94X   = cms.InputTag("probeEleCutBasedTight94X" ),

                                        passingVeto94XV2    = cms.InputTag("probeEleCutBasedVeto94XV2"  ),
                                        passingLoose94XV2   = cms.InputTag("probeEleCutBasedLoose94XV2" ),
                                        passingMedium94XV2  = cms.InputTag("probeEleCutBasedMedium94XV2"),
                                        passingTight94XV2   = cms.InputTag("probeEleCutBasedTight94XV2" ),

                                        passingVeto94XV2MinPtCut    = cms.InputTag("probeEleCutBasedVeto94XV2MinPtCut"  ),
                                        passingLoose94XV2MinPtCut   = cms.InputTag("probeEleCutBasedLoose94XV2MinPtCut" ),
                                        passingMedium94XV2MinPtCut  = cms.InputTag("probeEleCutBasedMedium94XV2MinPtCut"),
                                        passingTight94XV2MinPtCut   = cms.InputTag("probeEleCutBasedTight94XV2MinPtCut" ),

                                        passingVeto94XV2GsfEleSCEtaMultiRangeCut    = cms.InputTag("probeEleCutBasedVeto94XV2GsfEleSCEtaMultiRangeCut"  ),
                                        passingLoose94XV2GsfEleSCEtaMultiRangeCut   = cms.InputTag("probeEleCutBasedLoose94XV2GsfEleSCEtaMultiRangeCut" ),
                                        passingMedium94XV2GsfEleSCEtaMultiRangeCut  = cms.InputTag("probeEleCutBasedMedium94XV2GsfEleSCEtaMultiRangeCut"),
                                        passingTight94XV2GsfEleSCEtaMultiRangeCut   = cms.InputTag("probeEleCutBasedTight94XV2GsfEleSCEtaMultiRangeCut" ),

                                        passingVeto94XV2GsfEleDEtaInSeedCut    = cms.InputTag("probeEleCutBasedVeto94XV2GsfEleDEtaInSeedCut"  ),
                                        passingLoose94XV2GsfEleDEtaInSeedCut   = cms.InputTag("probeEleCutBasedLoose94XV2GsfEleDEtaInSeedCut" ),
                                        passingMedium94XV2GsfEleDEtaInSeedCut  = cms.InputTag("probeEleCutBasedMedium94XV2GsfEleDEtaInSeedCut"),
                                        passingTight94XV2GsfEleDEtaInSeedCut   = cms.InputTag("probeEleCutBasedTight94XV2GsfEleDEtaInSeedCut" ),

                                        passingVeto94XV2GsfEleDPhiInCut    = cms.InputTag("probeEleCutBasedVeto94XV2GsfEleDPhiInCut"  ),
                                        passingLoose94XV2GsfEleDPhiInCut   = cms.InputTag("probeEleCutBasedLoose94XV2GsfEleDPhiInCut" ),
                                        passingMedium94XV2GsfEleDPhiInCut  = cms.InputTag("probeEleCutBasedMedium94XV2GsfEleDPhiInCut"),
                                        passingTight94XV2GsfEleDPhiInCut   = cms.InputTag("probeEleCutBasedTight94XV2GsfEleDPhiInCut" ),

                                        passingVeto94XV2GsfEleFull5x5SigmaIEtaIEtaCut    = cms.InputTag("probeEleCutBasedVeto94XV2GsfEleFull5x5SigmaIEtaIEtaCut"  ),
                                        passingLoose94XV2GsfEleFull5x5SigmaIEtaIEtaCut   = cms.InputTag("probeEleCutBasedLoose94XV2GsfEleFull5x5SigmaIEtaIEtaCut" ),
                                        passingMedium94XV2GsfEleFull5x5SigmaIEtaIEtaCut  = cms.InputTag("probeEleCutBasedMedium94XV2GsfEleFull5x5SigmaIEtaIEtaCut"),
                                        passingTight94XV2GsfEleFull5x5SigmaIEtaIEtaCut   = cms.InputTag("probeEleCutBasedTight94XV2GsfEleFull5x5SigmaIEtaIEtaCut" ),

                                        passingVeto94XV2GsfEleHadronicOverEMEnergyScaledCut    = cms.InputTag("probeEleCutBasedVeto94XV2GsfEleHadronicOverEMEnergyScaledCut"  ),
                                        passingLoose94XV2GsfEleHadronicOverEMEnergyScaledCut   = cms.InputTag("probeEleCutBasedLoose94XV2GsfEleHadronicOverEMEnergyScaledCut" ),
                                        passingMedium94XV2GsfEleHadronicOverEMEnergyScaledCut  = cms.InputTag("probeEleCutBasedMedium94XV2GsfEleHadronicOverEMEnergyScaledCut"),
                                        passingTight94XV2GsfEleHadronicOverEMEnergyScaledCut   = cms.InputTag("probeEleCutBasedTight94XV2GsfEleHadronicOverEMEnergyScaledCut" ),

                                        passingVeto94XV2GsfEleEInverseMinusPInverseCut    = cms.InputTag("probeEleCutBasedVeto94XV2GsfEleEInverseMinusPInverseCut"  ),
                                        passingLoose94XV2GsfEleEInverseMinusPInverseCut   = cms.InputTag("probeEleCutBasedLoose94XV2GsfEleEInverseMinusPInverseCut" ),
                                        passingMedium94XV2GsfEleEInverseMinusPInverseCut  = cms.InputTag("probeEleCutBasedMedium94XV2GsfEleEInverseMinusPInverseCut"),
                                        passingTight94XV2GsfEleEInverseMinusPInverseCut   = cms.InputTag("probeEleCutBasedTight94XV2GsfEleEInverseMinusPInverseCut" ),

                                        passingVeto94XV2GsfEleRelPFIsoScaledCut    = cms.InputTag("probeEleCutBasedVeto94XV2GsfEleRelPFIsoScaledCut"  ),
                                        passingLoose94XV2GsfEleRelPFIsoScaledCut   = cms.InputTag("probeEleCutBasedLoose94XV2GsfEleRelPFIsoScaledCut" ),
                                        passingMedium94XV2GsfEleRelPFIsoScaledCut  = cms.InputTag("probeEleCutBasedMedium94XV2GsfEleRelPFIsoScaledCut"),
                                        passingTight94XV2GsfEleRelPFIsoScaledCut   = cms.InputTag("probeEleCutBasedTight94XV2GsfEleRelPFIsoScaledCut" ),

                                        passingVeto94XV2GsfEleConversionVetoCut    = cms.InputTag("probeEleCutBasedVeto94XV2GsfEleConversionVetoCut"  ),
                                        passingLoose94XV2GsfEleConversionVetoCut   = cms.InputTag("probeEleCutBasedLoose94XV2GsfEleConversionVetoCut" ),
                                        passingMedium94XV2GsfEleConversionVetoCut  = cms.InputTag("probeEleCutBasedMedium94XV2GsfEleConversionVetoCut"),
                                        passingTight94XV2GsfEleConversionVetoCut   = cms.InputTag("probeEleCutBasedTight94XV2GsfEleConversionVetoCut" ),

                                        passingVeto94XV2GsfEleMissingHitsCut    = cms.InputTag("probeEleCutBasedVeto94XV2GsfEleMissingHitsCut"  ),
                                        passingLoose94XV2GsfEleMissingHitsCut   = cms.InputTag("probeEleCutBasedLoose94XV2GsfEleMissingHitsCut" ),
                                        passingMedium94XV2GsfEleMissingHitsCut  = cms.InputTag("probeEleCutBasedMedium94XV2GsfEleMissingHitsCut"),
                                        passingTight94XV2GsfEleMissingHitsCut   = cms.InputTag("probeEleCutBasedTight94XV2GsfEleMissingHitsCut" ),

                                        passingMVA94XwpLnoiso = cms.InputTag("probeEleMVA94XwpLnoiso" ),
                                        passingMVA94Xwp90noiso = cms.InputTag("probeEleMVA94Xwp90noiso" ),
                                        passingMVA94Xwp80noiso = cms.InputTag("probeEleMVA94Xwp80noiso" ),
                                        passingMVA94XwpLiso = cms.InputTag("probeEleMVA94XwpLiso" ),
                                        passingMVA94Xwp90iso = cms.InputTag("probeEleMVA94Xwp90iso" ),
                                        passingMVA94Xwp80iso = cms.InputTag("probeEleMVA94Xwp80iso" ),
                                        passingMVA94XwpLnoisoV2 = cms.InputTag("probeEleMVA94XwpLnoisoV2" ),
                                        passingMVA94Xwp90noisoV2 = cms.InputTag("probeEleMVA94Xwp90noisoV2" ),
                                        passingMVA94Xwp80noisoV2 = cms.InputTag("probeEleMVA94Xwp80noisoV2" ),
                                        passingMVA94XwpLisoV2 = cms.InputTag("probeEleMVA94XwpLisoV2" ),
                                        passingMVA94Xwp90isoV2 = cms.InputTag("probeEleMVA94Xwp90isoV2" ),
                                        passingMVA94Xwp80isoV2 = cms.InputTag("probeEleMVA94Xwp80isoV2" ),

                                        passingMVA94XwpHZZisoV2 = cms.InputTag("probeEleMVA94XwpHZZisoV2" ),
                                        )
                                    )

process.tnpPhoIDs = cms.EDAnalyzer("TagProbeFitTreeProducer",
                                    tnpVars.mcTruthCommonStuff, tnpVars.CommonStuffForPhotonProbe,
                                    tagProbePairs = cms.InputTag("tnpPairingPhoIDs"),                                                                                         
                                    probeMatches  = cms.InputTag("genProbePho"),
                                    allProbes     = cms.InputTag("probePho"),
                                    flags         = cms.PSet(
#                                        passingLoose      = cms.InputTag("probePhoCutBasedLoose"),
#                                        passingMedium     = cms.InputTag("probePhoCutBasedMedium"),
#                                        passingTight      = cms.InputTag("probePhoCutBasedTight"),
#                                        passingMVA        = cms.InputTag("probePhoMVA"),
                                         passingLoose80X   = cms.InputTag("probePhoCutBasedLoose80X"),
                                         passingMedium80X  = cms.InputTag("probePhoCutBasedMedium80X"),
                                         passingTight80X   = cms.InputTag("probePhoCutBasedTight80X"),
                                         passingMVA80Xwp90 = cms.InputTag("probePhoMVA80Xwp90"),
                                         passingMVA80Xwp80 = cms.InputTag("probePhoMVA80Xwp80"),
                                         
                                         passingLoose94X   = cms.InputTag("probePhoCutBasedLoose94X"),
                                         passingMedium94X  = cms.InputTag("probePhoCutBasedMedium94X"),
                                         passingTight94X   = cms.InputTag("probePhoCutBasedTight94X"),

                                         passingLoose100XV2   = cms.InputTag("probePhoCutBasedLoose100XV2"),
                                         passingMedium100XV2  = cms.InputTag("probePhoCutBasedMedium100XV2"),
                                         passingTight100XV2   = cms.InputTag("probePhoCutBasedTight100XV2"),

                                         passingLoose100XV2MinPtCut   = cms.InputTag("probePhoCutBasedLoose100XV2MinPtCut"),
                                         passingMedium100XV2MinPtCut  = cms.InputTag("probePhoCutBasedMedium100XV2MinPtCut"),
                                         passingTight100XV2MinPtCut   = cms.InputTag("probePhoCutBasedTight100XV2MinPtCut"),

                                         passingLoose100XV2PhoSCEtaMultiRangeCut   = cms.InputTag("probePhoCutBasedLoose100XV2PhoSCEtaMultiRangeCut"),
                                         passingMedium100XV2PhoSCEtaMultiRangeCut  = cms.InputTag("probePhoCutBasedMedium100XV2PhoSCEtaMultiRangeCut"),
                                         passingTight100XV2PhoSCEtaMultiRangeCut   = cms.InputTag("probePhoCutBasedTight100XV2PhoSCEtaMultiRangeCut"),

                                         passingLoose100XV2PhoSingleTowerHadOverEmCut   = cms.InputTag("probePhoCutBasedLoose100XV2PhoSingleTowerHadOverEmCut"),
                                         passingMedium100XV2PhoSingleTowerHadOverEmCut  = cms.InputTag("probePhoCutBasedMedium100XV2PhoSingleTowerHadOverEmCut"),
                                         passingTight100XV2PhoSingleTowerHadOverEmCut   = cms.InputTag("probePhoCutBasedTight100XV2PhoSingleTowerHadOverEmCut"),

                                         passingLoose100XV2PhoFull5x5SigmaIEtaIEtaCut   = cms.InputTag("probePhoCutBasedLoose100XV2PhoFull5x5SigmaIEtaIEtaCut"),
                                         passingMedium100XV2PhoFull5x5SigmaIEtaIEtaCut  = cms.InputTag("probePhoCutBasedMedium100XV2PhoFull5x5SigmaIEtaIEtaCut"),
                                         passingTight100XV2PhoFull5x5SigmaIEtaIEtaCut   = cms.InputTag("probePhoCutBasedTight100XV2PhoFull5x5SigmaIEtaIEtaCut"),

                                         passingLoose100XV2PhoAnyPFIsoWithEACut   = cms.InputTag("probePhoCutBasedLoose100XV2PhoAnyPFIsoWithEACut"),
                                         passingMedium100XV2PhoAnyPFIsoWithEACut  = cms.InputTag("probePhoCutBasedMedium100XV2PhoAnyPFIsoWithEACut"),
                                         passingTight100XV2PhoAnyPFIsoWithEACut   = cms.InputTag("probePhoCutBasedTight100XV2PhoAnyPFIsoWithEACut"),

                                         passingLoose100XV2PhoAnyPFIsoWithEAAndQuadScalingCut   = cms.InputTag("probePhoCutBasedLoose100XV2PhoAnyPFIsoWithEAAndQuadScalingCut"),
                                         passingMedium100XV2PhoAnyPFIsoWithEAAndQuadScalingCut  = cms.InputTag("probePhoCutBasedMedium100XV2PhoAnyPFIsoWithEAAndQuadScalingCut"),
                                         passingTight100XV2PhoAnyPFIsoWithEAAndQuadScalingCut   = cms.InputTag("probePhoCutBasedTight100XV2PhoAnyPFIsoWithEAAndQuadScalingCut"),

                                         passingLoose100XV2PhoAnyPFIsoWithEACut1   = cms.InputTag("probePhoCutBasedLoose100XV2PhoAnyPFIsoWithEACut1"),
                                         passingMedium100XV2PhoAnyPFIsoWithEACut1  = cms.InputTag("probePhoCutBasedMedium100XV2PhoAnyPFIsoWithEACut1"),
                                         passingTight100XV2PhoAnyPFIsoWithEACut1   = cms.InputTag("probePhoCutBasedTight100XV2PhoAnyPFIsoWithEACut1"),

                                         passingMVA94Xwp90 = cms.InputTag("probePhoMVA94Xwp90"),
                                         passingMVA94Xwp80 = cms.InputTag("probePhoMVA94Xwp80"),

                                         passingMVA94XV2wp90 = cms.InputTag("probePhoMVA94XV2wp90"),
                                         passingMVA94XV2wp80 = cms.InputTag("probePhoMVA94XV2wp80"),
                                        )
                                    )

## add pass HLT-safe flag, available for miniAOD only
if not options['useAOD'] :
    setattr( process.tnpEleTrig.flags, 'passingHLTsafe', cms.InputTag("probeEleHLTsafe" ) )
    setattr( process.tnpEleIDs.flags , 'passingHLTsafe', cms.InputTag("probeEleHLTsafe" ) )

# Add SUSY variables to the "variables", add SUSY IDs to the "flags"
if options['addSUSY'] :
    setattr( process.tnpEleIDs.variables , 'el_miniIsoChg', cms.string("userFloat('miniIsoChg')") )
    setattr( process.tnpEleIDs.variables , 'el_miniIsoAll', cms.string("userFloat('miniIsoAll')") )
    setattr( process.tnpEleIDs.variables , 'el_ptRatio', cms.string("userFloat('ptRatio')") )
    setattr( process.tnpEleIDs.variables , 'el_ptRatioUncorr', cms.string("userFloat('ptRatioUncorr')") )
    setattr( process.tnpEleIDs.variables , 'el_ptRel', cms.string("userFloat('ptRel')") )
    setattr( process.tnpEleIDs.variables , 'el_MVATTH', cms.InputTag("susyEleVarHelper:electronMVATTH") )   
    setattr( process.tnpEleIDs.variables , 'el_sip3d', cms.InputTag("susyEleVarHelper:sip3d") )
    def addFlag(name):
        setattr( process.tnpEleIDs.flags, 'passing'+name, cms.InputTag('probes'+name ) )
    from EgammaAnalysis.TnPTreeProducer.electronsExtrasSUSY_cff  import workingPoints
    for wp in workingPoints: addFlag(wp)


tnpSetup.customize( process.tnpEleTrig , options )
tnpSetup.customize( process.tnpEleIDs  , options )
tnpSetup.customize( process.tnpPhoIDs  , options )
tnpSetup.customize( process.tnpEleReco , options )


process.tree_sequence = cms.Sequence()
if (options['DoTrigger']): process.tree_sequence *= process.tnpEleTrig
if (options['DoRECO'])   : process.tree_sequence *= process.tnpEleReco
if (options['DoEleID'])  : process.tree_sequence *= process.tnpEleIDs
if (options['DoPhoID'])  : process.tree_sequence *= process.tnpPhoIDs


##########################################################################
## PATHS
##########################################################################
process.out = cms.OutputModule("PoolOutputModule", 
                               fileName = cms.untracked.string(options['OUTPUTEDMFILENAME']),
                               SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring("p"))
                               )
process.outpath = cms.EndPath(process.out)
if (not options['DEBUG']):
    process.outpath.remove(process.out)

process.evtCounter = cms.EDAnalyzer('SimpleEventCounter')

process.p = cms.Path(
        process.evtCounter        +
        process.hltFilter         +
        process.cand_sequence     + 
        process.tnpPairs_sequence +
        process.mc_sequence       +
        process.tree_sequence 
        )

process.TFileService = cms.Service(
    "TFileService", fileName = cms.string(options['OUTPUT_FILE_NAME']),
    closeFileFast = cms.untracked.bool(True)
    )
