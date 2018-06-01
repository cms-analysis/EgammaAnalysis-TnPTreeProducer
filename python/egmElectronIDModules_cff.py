import FWCore.ParameterSet.Config as cms

###################################################################
## ID MODULES
###################################################################

from PhysicsTools.SelectorUtils.tools.vid_id_tools import *

def setIDs(process, options):

    dataFormat = DataFormat.MiniAOD
    eleProducer = "PatElectronSelectorByValueMap"
    if (options['useAOD']):
        dataFormat = DataFormat.AOD
        eleProducer = "GsfElectronSelectorByValueMap"
        
    switchOnVIDElectronIdProducer(process, dataFormat)

    # define which IDs we want to produce
    my_id_modules = [
        'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Summer16_80X_V1_cff',
        'RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV60_cff',
         'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring16_GeneralPurpose_V1_cff',
        'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Fall17_94X_V1_cff',
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_noIso_V1_cff',
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_iso_V1_cff',
       ]

    ### add only miniAOD supported IDs
    if not options['useAOD'] :
        my_id_modules.append( 'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronHLTPreselecition_Summer16_V1_cff' )
                 
    for idmod in my_id_modules:
        setupAllVIDIdsInModule(process, idmod, setupVIDElectronSelection)

    process.egmGsfElectronIDs.physicsObjectSrc     = cms.InputTag(options['ELECTRON_COLL'])
    process.electronMVAValueMapProducer.srcMiniAOD = cms.InputTag(options['ELECTRON_COLL'])
    process.electronRegressionValueMapProducer.srcMiniAOD = cms.InputTag(options['ELECTRON_COLL'])

    process.probeEleCutBasedVeto = cms.EDProducer(eleProducer,
                                                      input     = cms.InputTag("goodElectrons"),
                                                      cut       = cms.string(options['ELECTRON_CUTS']),
                                                      selection = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-veto"),
                                                      id_cut    = cms.bool(True)
                                                  )
    
    ######################################################################################
    ## MODULES FOR N-1 CUT BASED STUDIES
    ######################################################################################
    # List of cuts
    #0 MinPtCut
    #1 GsfEleSCEtaMultiRangeCut
    #2 GsfEleDEtaInCut
    #3 GsfEleDPhiInCut
    #4 GsfEleFull5x5SigmaIEtaIEtaCut
    #5 GsfEleHadronicOverEMCut
    #6 GsfEleDxyCut 
    #7 GsfEleDzCut
    #8 GsfEleEInverseMinusPInverseCut
    #9 GsfEleEffAreaPFIsoCut
    #10 GsfEleConversionVetoCut
    #11 GsfEleMissingHitsCut
    

    process.probeEleHLTsafe = process.probeEleCutBasedVeto.clone()
    process.probeEleHLTsafe.selection = cms.InputTag("egmGsfElectronIDs:cutBasedElectronHLTPreselection-Summer16-V1")

    process.probeEleCutBasedLoose  = process.probeEleCutBasedVeto.clone()
    process.probeEleCutBasedMedium = process.probeEleCutBasedVeto.clone()
    process.probeEleCutBasedTight  = process.probeEleCutBasedVeto.clone()
    process.probeEleCutBasedLoose.selection  = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-loose" )
    process.probeEleCutBasedMedium.selection = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-medium")
    process.probeEleCutBasedTight.selection  = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-tight" )

    process.probeEleCutBasedVeto80X   = process.probeEleCutBasedVeto.clone()
    process.probeEleCutBasedLoose80X  = process.probeEleCutBasedVeto.clone()
    process.probeEleCutBasedMedium80X = process.probeEleCutBasedVeto.clone()
    process.probeEleCutBasedTight80X  = process.probeEleCutBasedVeto.clone()
    process.probeEleMVA80Xwp90        = process.probeEleCutBasedVeto.clone()
    process.probeEleMVA80Xwp80        = process.probeEleCutBasedVeto.clone()
    process.probeEleCutBasedVeto80X.selection   = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-veto"  )
    process.probeEleCutBasedLoose80X.selection  = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-loose" )
    process.probeEleCutBasedMedium80X.selection = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-medium")
    process.probeEleCutBasedTight80X.selection  = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-tight" )
    process.probeEleMVA80Xwp90.selection        = cms.InputTag("egmGsfElectronIDs:mvaEleID-Spring16-GeneralPurpose-V1-wp90" )
    process.probeEleMVA80Xwp80.selection        = cms.InputTag("egmGsfElectronIDs:mvaEleID-Spring16-GeneralPurpose-V1-wp80" )


    process.probeEleCutBasedVeto94X   = process.probeEleCutBasedVeto.clone()
    process.probeEleCutBasedLoose94X  = process.probeEleCutBasedVeto.clone()
    process.probeEleCutBasedMedium94X = process.probeEleCutBasedVeto.clone()
    process.probeEleCutBasedTight94X  = process.probeEleCutBasedVeto.clone()
    process.probeEleMVA94XwpLnoiso        = process.probeEleCutBasedVeto.clone()
    process.probeEleMVA94Xwp90noiso        = process.probeEleCutBasedVeto.clone()
    process.probeEleMVA94Xwp80noiso        = process.probeEleCutBasedVeto.clone()
    process.probeEleMVA94XwpLiso        = process.probeEleCutBasedVeto.clone()
    process.probeEleMVA94Xwp90iso        = process.probeEleCutBasedVeto.clone()
    process.probeEleMVA94Xwp80iso        = process.probeEleCutBasedVeto.clone()
    process.probeEleCutBasedVeto94X.selection   = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-veto"  )
    process.probeEleCutBasedLoose94X.selection  = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-loose" )
    process.probeEleCutBasedMedium94X.selection = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-medium")
    process.probeEleCutBasedTight94X.selection  = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-tight" )
    process.probeEleMVA94XwpLnoiso.selection        = cms.InputTag("egmGsfElectronIDs:mvaEleID-Fall17-noIso-V1-wpLoose" )
    process.probeEleMVA94Xwp90noiso.selection        = cms.InputTag("egmGsfElectronIDs:mvaEleID-Fall17-noIso-V1-wp90" )
    process.probeEleMVA94Xwp80noiso.selection        = cms.InputTag("egmGsfElectronIDs:mvaEleID-Fall17-noIso-V1-wp80" )
    process.probeEleMVA94XwpLiso.selection        = cms.InputTag("egmGsfElectronIDs:mvaEleID-Fall17-iso-V1-wpLoose" )
    process.probeEleMVA94Xwp90iso.selection        = cms.InputTag("egmGsfElectronIDs:mvaEleID-Fall17-iso-V1-wp90" )
    process.probeEleMVA94Xwp80iso.selection        = cms.InputTag("egmGsfElectronIDs:mvaEleID-Fall17-iso-V1-wp80" )


    
    process.tagEleCutBasedTight = cms.EDProducer(eleProducer,
                                                     input     = cms.InputTag("goodElectrons"),
                                                     cut       = cms.string(options['ELECTRON_TAG_CUTS']),
                                                     selection = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-tight"),
                                                     id_cut    = cms.bool(True)
                                                )    
    process.tagEleCutBasedTight.selection = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-tight")

    if options['addSUSY'] :

        from EgammaAnalysis.TnPTreeProducer.electronsExtrasSUSY_cff  import workingPoints

        process.susy_ele_sequence = cms.Sequence()

        # Based on https://github.com/UAEDF-tomc/cmssw/blob/susy_tnp_80X_v3/PhysicsTools/TagAndProbe/python/makeTreeSusy_cfi.py#L76-L184
        # Applies probe cuts and WP (numerators and denominators both need to be listed here)
        def getProbes(name):
            temp = process.probeEleCutBasedVeto.clone()
            temp.selection = cms.InputTag('susyEleVarHelper:pass' + wp)
            setattr(process, 'probes' + name, temp)
            process.susy_ele_sequence += temp

        for wp in workingPoints: getProbes(wp)


