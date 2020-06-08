import FWCore.ParameterSet.Config as cms

###################################################################
## ID MODULES
###################################################################

from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
from EgammaAnalysis.TnPTreeProducer.cmssw_version import isReleaseAbove

def setIDs(process, options):

    switchOnVIDPhotonIdProducer(process, DataFormat.AOD if options['useAOD'] else DataFormat.MiniAOD)

    # define which IDs we want to produce
    my_id_modules = ['RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_Spring16_V2p2_cff'   ,
                     'RecoEgamma.PhotonIdentification.Identification.mvaPhotonID_Spring16_nonTrig_V1_cff',
                     'RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_Fall17_94X_V1_cff',
                     'RecoEgamma.PhotonIdentification.Identification.mvaPhotonID_Fall17_94X_V2_cff',
                     'RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_Fall17_94X_V2_cff'
                     ]

    if not isReleaseAbove(10, 6): # (photon mva 94X_V1 broken in CMSSW_10_6_X)
      my_id_modules += ['RecoEgamma.PhotonIdentification.Identification.mvaPhotonID_Fall17_94X_V1_cff']
    else: # (only needed in CMSSW_10_6_X
      process.load("RecoEgamma.PhotonIdentification.photonIDValueMapProducer_cff")

    for idmod in my_id_modules:
        setupAllVIDIdsInModule(process, idmod, setupVIDPhotonSelection)

    process.egmPhotonIDs.physicsObjectSrc        = cms.InputTag(options['PHOTON_COLL'])
    process.photonIDValueMapProducer.srcMiniAOD  = cms.InputTag(options['PHOTON_COLL'])
    process.photonMVAValueMapProducer.srcMiniAOD = cms.InputTag(options['PHOTON_COLL'])
#    process.photonMVAValueMapProducer.src        = cms.InputTag(options['PHOTON_COLL'])

    #
    # Add many probe modules, use the PatPhotonNm1Selector in case we want to check the effect of one cut
    #
    def addNewProbeModule(sequence, name, inputTag, cutNamesToMask=None):
      if cutNamesToMask:
        temp = cms.EDProducer('PatPhotonNm1Selector',
                              input          = cms.InputTag("goodPhotons"),
                              cut            = cms.string(options['PHOTON_CUTS']),
                              selection      = cms.InputTag(inputTag),
                              cutNamesToMask = cutNamesToMask,
                              )
      else:
        temp = cms.EDProducer('PhotonSelectorByValueMap' if options['useAOD'] else 'PatPhotonSelectorByValueMap',
                              input     = cms.InputTag("goodPhotons"),
                              cut       = cms.string(options['PHOTON_CUTS']),
                              selection = cms.InputTag(inputTag),
                              id_cut    = cms.bool(True)
                             )
      setattr(process, 'probePho%s' % name, temp)
      sequence += temp

    probeSequence = cms.Sequence()
    for wp in ['Loose', 'Medium', 'Tight']:
      addNewProbeModule(probeSequence, 'CutBased%s80X' % wp,   'egmPhotonIDs:cutBasedPhotonID-Spring16-V2p2-%s' % wp.lower())
      addNewProbeModule(probeSequence, 'CutBased%s94X' % wp,   'egmPhotonIDs:cutBasedPhotonID-Fall17-94X-V1-%s' % wp.lower())
      addNewProbeModule(probeSequence, 'CutBased%s94XV2' % wp, 'egmPhotonIDs:cutBasedPhotonID-Fall17-94X-V2-%s' % wp.lower())

    for wp in ['wp80', 'wp90']:
      addNewProbeModule(probeSequence, 'MVA80X%s' % wp,   'egmPhotonIDs:mvaPhoID-Spring16-nonTrig-V1-%s' % wp)
      addNewProbeModule(probeSequence, 'MVA94XV2%s' % wp, 'egmPhotonIDs:mvaPhoID-RunIIFall17-v2-%s' % wp)
      if not isReleaseAbove(10, 6):
        addNewProbeModule(probeSequence, 'MVA94X%s' % wp,   'egmPhotonIDs:mvaPhoID-RunIIFall17-v1-%s' % wp)


    #
    # For cut based 94X V2, also check partial cuts
    #
    if isReleaseAbove(10, 6): # (name change of cuts)
      allCuts = ["MinPtCut_0", "PhoSCEtaMultiRangeCut_0", "PhoSingleTowerHadOverEmCut_0", "PhoFull5x5SigmaIEtaIEtaCut_0", "PhoGenericRhoPtScaledCut_0", "PhoGenericRhoPtScaledCut_1", "PhoGenericRhoPtScaledCut_2"]
    else:
      allCuts = ["MinPtCut_0", "PhoSCEtaMultiRangeCut_0", "PhoSingleTowerHadOverEmCut_0", "PhoFull5x5SigmaIEtaIEtaCut_0", "PhoAnyPFIsoWithEACut_0", "PhoAnyPFIsoWithEAAndQuadScalingCut_0", "PhoAnyPFIsoWithEACut_1"]

    for cut in allCuts:
      otherCuts = cms.vstring([i for i in allCuts if i!=cut])
      cutName   = cut.replace('_','').replace('0','') # special case for the PhoAnyPFIsoWithEACut_1
      for wp in ['Loose', 'Medium', 'Tight']:
        addNewProbeModule(probeSequence, 'CutBased%s94XV2%s' % (wp, cutName), 'egmPhotonIDs:cutBasedPhotonID-Fall17-94X-V2-%s' % wp.lower(), cutNamesToMask=otherCuts)

    return probeSequence
