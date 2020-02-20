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
    "doTrigger", True,
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
    "GT", "auto",
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "Global Tag to be used"
    )

varOptions.register(
    "includeSUSY", False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "add also the variables used by SUSY"
    )

# Note: not sure if the AOD mode has been tested recently
varOptions.register(
    "isAOD", False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "use AOD"
    )

varOptions.register(
    "era", "2018",
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "Data-taking era: 2016, 2017 or 2018"
    )

varOptions.parseArguments()


###################################################################
## Define TnP inputs 
###################################################################

options = dict()
options['useAOD']               = varOptions.isAOD

options['HLTProcessName']       = varOptions.HLTname
options['era']                  = varOptions.era

options['ELECTRON_COLL']        = "gedGsfElectrons" if options['useAOD'] else "slimmedElectrons"
options['PHOTON_COLL']          = "getPhotons" if options['useAOD'] else "slimmedPhotons"
options['SUPERCLUSTER_COLL']    = "reducedEgamma:reducedSuperClusters" ### not used in AOD

options['ELECTRON_CUTS']        = "ecalEnergy*sin(superClusterPosition.theta)>5.0 &&  (abs(-log(tan(superClusterPosition.theta/2)))<2.5)"
options['SUPERCLUSTER_CUTS']    = "abs(eta)<2.5 &&  et>5.0"
options['PHOTON_CUTS']          = "(abs(-log(tan(superCluster.position.theta/2)))<=2.5) && pt> 10"
options['ELECTRON_TAG_CUTS']    = "(abs(-log(tan(superCluster.position.theta/2)))<=2.1) && !(1.4442<=abs(-log(tan(superClusterPosition.theta/2)))<=1.566) && pt >= 30.0"

options['MAXEVENTS']            = cms.untracked.int32(varOptions.maxEvents)
options['DoTrigger']            = varOptions.doTrigger
options['DoRECO']               = varOptions.doRECO
options['DoEleID']              = varOptions.doEleID
options['DoPhoID']              = varOptions.doPhoID

options['DEBUG']                = False
options['isMC']                 = varOptions.isMC
options['UseCalibEn']           = varOptions.calibEn
options['addSUSY']              = varOptions.includeSUSY and not options['useAOD']

if options['era'] == '2016':
  options['TnPPATHS']           = cms.vstring("HLT_Ele27_eta2p1_WPTight_Gsf_v*")
  options['TnPHLTTagFilters']   = cms.vstring("hltEle27erWPTightGsfTrackIsoFilter")
  options['GLOBALTAG']          = 'auto:run2_mc' if varOptions.isMC else 'auto:run2_data'
elif options['era'] == '2017':
  options['TnPPATHS']           = cms.vstring("HLT_Ele32_WPTight_Gsf_L1DoubleEG_v*")
  options['TnPHLTTagFilters']   = cms.vstring("hltEle32L1DoubleEGWPTightGsfTrackIsoFilter","hltEGL1SingleEGOrFilter")
  options['GLOBALTAG']          = 'auto:run2_mc' if varOptions.isMC else 'auto:run2_data'
elif options['era'] == '2018':
  options['TnPPATHS']           = cms.vstring("HLT_Ele32_WPTight_Gsf_v*")
  options['TnPHLTTagFilters']   = cms.vstring("hltEle32WPTightGsfTrackIsoFilter")
  options['GLOBALTAG']          = 'auto:run2_mc' if varOptions.isMC else '102X_dataRun2_v11'
else:
  print '%s is not a valid era' % options['era']

options['TnPHLTProbeFilters']   = cms.vstring()
options['HLTFILTERSTOMEASURE']  = {"passHltEle32WPTightGsf" :                    cms.vstring("hltEle32WPTightGsfTrackIsoFilter"),
                                   "passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg1" : cms.vstring("hltEle23Ele12CaloIdLTrackIdLIsoVLTrackIsoLeg1Filter"),
                                   "passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg2" : cms.vstring("hltEle23Ele12CaloIdLTrackIdLIsoVLTrackIsoLeg2Filter"),
                                  } # Some examples, you can add multiple filters (or OR's of filters, note the vstring) here, each of them will be added to the tuple

options['OUTPUT_FILE_NAME']     = "TnPTree_%s.root" % ("mc" if options['isMC'] else "data")
options['GLOBALTAG']            = varOptions.GT if varOptions.GT != "auto" else options['GLOBALTAG']


###################################################################
## Define input files for test local run
###################################################################
if options['era'] == '2016':
  if options['useAOD'] : from EgammaAnalysis.TnPTreeProducer.etc.tnpInputTestFiles_cff import filesAOD_23Sep2016 as inputs
  else:                  from EgammaAnalysis.TnPTreeProducer.etc.tnpInputTestFiles_cff import filesMiniAOD_23Sep2016 as inputs
if options['era'] == '2017':
  if options['useAOD'] : from EgammaAnalysis.TnPTreeProducer.etc.tnpInputTestFiles_cff import filesAOD_Preliminary2017 as inputs
  else:                  from EgammaAnalysis.TnPTreeProducer.etc.tnpInputTestFiles_cff import filesMiniAOD_Preliminary2017 as inputs
if options['era'] == '2018':
  if options['useAOD'] : from EgammaAnalysis.TnPTreeProducer.etc.tnpInputTestFiles_cff import filesAOD_Preliminary2018 as inputs
  else:                  from EgammaAnalysis.TnPTreeProducer.etc.tnpInputTestFiles_cff import filesMiniAOD_Preliminary2018 as inputs

options['INPUT_FILE_NAME'] = inputs['mc' if varOptions.isMC else 'data']


###################################################################
## import TnP tree maker pythons and configure for AODs
###################################################################
process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load('Configuration.StandardSequences.Services_cff') 
process.load('FWCore.MessageService.MessageLogger_cfi')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, options['GLOBALTAG'] , '')

import EgammaAnalysis.TnPTreeProducer.egmTreesSetup_cff as tnpSetup
tnpSetup.setupTreeMaker(process,options)

import EgammaAnalysis.TnPTreeProducer.pileupConfiguration_cff as pileUpSetup
pileUpSetup.setPileUpConfiguration(process, options)

###################################################################
## Init and Load
###################################################################
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.MessageLogger.cerr.threshold = ''
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.source = cms.Source("PoolSource", fileNames = options['INPUT_FILE_NAME'])
process.maxEvents = cms.untracked.PSet( input = options['MAXEVENTS'])

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
                                    flags         = cms.PSet(),
                                    )
for flag in options['HLTFILTERSTOMEASURE']:
  setattr(process.tnpEleTrig.flags, flag, cms.InputTag(flag))



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
                                    flags         = cms.PSet(),
                                    )

# ID's to store in the electron ID and trigger tree
def storeEleId(id):
  setattr(process.tnpEleTrig.flags, 'passing' + id, cms.InputTag('probeEle' + id))
  setattr(process.tnpEleIDs.flags,  'passing' + id, cms.InputTag('probeEle' + id))

cutBasedIds = ['80X',
               '94X',
               '94XV2',
               '94XV2MinPtCut',
               '94XV2GsfEleSCEtaMultiRangeCut',
               '94XV2GsfEleDEtaInSeedCut',
               '94XV2GsfEleDPhiInCut',
               '94XV2GsfEleFull5x5SigmaIEtaIEtaCut',
               '94XV2GsfEleHadronicOverEMEnergyScaledCut',
               '94XV2GsfEleEInverseMinusPInverseCut',
               '94XV2GsfEleRelPFIsoScaledCut',
               '94XV2GsfEleConversionVetoCut',
               '94XV2GsfEleMissingHitsCut']

for cutBasedId in cutBasedIds:
  for wp in ['Veto', 'Loose', 'Medium', 'Tight']:
    storeEleId('CutBased%s%s' % (wp, cutBasedId))

for wp in ['wpLnoiso', 'wp80noiso', 'wp90noiso', 'wpLiso', 'wp80iso', 'wp90iso']:
  storeEleId('MVA94X%s' % wp)
  storeEleId('MVA94X%sV2' % wp)

storeEleId('MVA80Xwp80')
storeEleId('MVA80Xwp90')
storeEleId('MVA94XwpHZZisoV2')


process.tnpPhoIDs = cms.EDAnalyzer("TagProbeFitTreeProducer",
                                    tnpVars.mcTruthCommonStuff, tnpVars.CommonStuffForPhotonProbe,
                                    tagProbePairs = cms.InputTag("tnpPairingPhoIDs"),                                                                                         
                                    probeMatches  = cms.InputTag("genProbePho"),
                                    allProbes     = cms.InputTag("probePho"),
                                    flags         = cms.PSet(),
                                    )


# ID's to store in the photon ID tree
def storePhoId(id):
  setattr(process.tnpPhoIDs.flags,  'passing' + id, cms.InputTag('probePho' + id))

cutBasedIds = ['80X',
               '94X',
               '100XV2',
               '100XV2MinPtCut',
               '100XV2PhoSCEtaMultiRangeCut',
               '100XV2PhoSingleTowerHadOverEmCut',
               '100XV2PhoFull5x5SigmaIEtaIEtaCut',
               '100XV2PhoAnyPFIsoWithEACut',
               '100XV2PhoAnyPFIsoWithEAAndQuadScalingCut',
               '100XV2PhoAnyPFIsoWithEACut1']

for cutBasedId in cutBasedIds:
  for wp in ['Loose', 'Medium', 'Tight']:
    storePhoId('CutBased%s%s' % (wp, cutBasedId))

for mvaId in ['80X', '94X', '94XV2']:
  for wp in ['wp80', 'wp90']:
    storePhoId('MVA%s%s' % (mvaId, wp))


## add pass HLT-safe flag, available for miniAOD only [note: HLT-safe flat is not up to date anymore since early 2016!]
if not options['useAOD'] :
    setattr( process.tnpEleTrig.flags, 'passingHLTsafe', cms.InputTag("probeEleHLTsafe" ) )
    setattr( process.tnpEleIDs.flags , 'passingHLTsafe', cms.InputTag("probeEleHLTsafe" ) )
    setattr( process.tnpEleTrig.flags, 'passingDoubleHLTsafe', cms.InputTag("probeDoubleEleHLTsafe" ) )
    setattr( process.tnpEleIDs.flags , 'passingDoubleHLTsafe', cms.InputTag("probeDoubleEleHLTsafe" ) )

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
if options['DEBUG']:
  process.out = cms.OutputModule("PoolOutputModule",
                                 fileName = cms.untracked.string('edmFile_for_debug.root'),
                                 SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring("p"))
                                 )
  process.outpath = cms.EndPath(process.out)

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
