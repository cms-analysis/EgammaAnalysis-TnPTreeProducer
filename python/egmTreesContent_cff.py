import FWCore.ParameterSet.Config as cms

##########################################################################
## TREE CONTENT
#########################################################################
    
ZVariablesToStore = cms.PSet(
    eta = cms.string("eta"),
    abseta = cms.string("abs(eta)"),
    pt  = cms.string("pt"),
    mass  = cms.string("mass"),
    )   

SCProbeVariablesToStore = cms.PSet(
    sc_eta    = cms.string("eta"),
    sc_abseta = cms.string("abs(eta)"),
    sc_pt     = cms.string("pt"),
    sc_et     = cms.string("et"),
    sc_e      = cms.string("energy"),
    sc_tkIso  = cms.InputTag("recoEcalCandidateHelper:scTkIso"),
    )

EleProbeVariablesToStore = cms.PSet(
    el_eta    = cms.string("eta"),
    el_phi    = cms.string("phi"),
    el_abseta = cms.string("abs(eta)"),
    el_pt     = cms.string("pt"),
    el_pf_pt  = cms.InputTag("eleVarHelper:pfPt"),
    el_et     = cms.string("et"),
    el_e      = cms.string("energy"),
    el_q      = cms.string("charge"),
    
    ## super cluster quantities
    el_sc_e          = cms.string("superCluster().energy"),
    el_sc_rawE       = cms.string("superCluster().rawEnergy"),
    el_sc_esE        = cms.string("superCluster().preshowerEnergy"),
    el_sc_et         = cms.string("superCluster().energy*sin(superClusterPosition.theta)"),    
    el_sc_eta        = cms.string("-log(tan(superCluster.position.theta/2))"),
    el_sc_phi        = cms.string("superCluster.phi"),    
    el_sc_abseta     = cms.string("abs(-log(tan(superCluster.position.theta/2)))"),
    el_seed_e        = cms.string("superCluster.seed.energy"), 
#    el_xseed_e       = cms.string("superCluster.seed.seed.energy"), 

    #id based
#    el_dEtaSeeOut       = cms.string("deltaEtaSeedClusterTrackAtCalo"),
    el_dEtaIn        = cms.string("deltaEtaSuperClusterTrackAtVtx"),
    el_dPhiIn        = cms.string("deltaPhiSuperClusterTrackAtVtx"),
    el_dEtaSeed      = cms.string("deltaEtaSuperClusterTrackAtVtx+log(tan(superCluster.position.theta/2))-log(tan(superCluster.seed.position.theta/2))"),    
    el_phiW          = cms.string("superCluster().phiWidth"),
    el_etaW          = cms.string("superCluster().etaWidth"),

    el_5x5_e1x5      = cms.string("full5x5_showerShape().e1x5"),
    el_5x5_e2x5      = cms.string("full5x5_showerShape().e2x5Max"),
    el_5x5_e5x5      = cms.string("full5x5_showerShape().e5x5"),
    el_5x5_r9        = cms.string("full5x5_showerShape().r9"),
    el_5x5_sieie     = cms.string("full5x5_showerShape().sigmaIetaIeta"),    
    el_5x5_sieip     = cms.string("full5x5_showerShape().sigmaIetaIphi"),    
    el_e1x5          = cms.string("showerShape().e1x5"),
    el_e2x5          = cms.string("showerShape().e2x5Max"),
    el_e5x5          = cms.string("showerShape().e5x5"),
    el_r9            = cms.string("showerShape().r9"),
    el_sieie         = cms.string("showerShape().sigmaIetaIeta"),
    
    el_hoe           = cms.string("hcalOverEcalBc"),
    el_eoverp        = cms.string("(superCluster().rawEnergy+superCluster().preshowerEnergy)/gsfTrack().pMode()"),

    # mva id
    el_nonTrigMVA    = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values"),
    el_nonTrigMVA80X = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Values"),
    el_hzzMVA80X     = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16HZZV1Values"),
    el_trigMVA       = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15Trig25nsV1Values"),
     
    #isolation
    el_chIso         = cms.string("pfIsolationVariables().sumChargedHadronPt"),
    el_phoIso        = cms.string("pfIsolationVariables().sumPhotonEt"),
    el_neuIso        = cms.string("pfIsolationVariables().sumNeutralHadronEt"),
    el_ecalIso       = cms.string("ecalPFClusterIso"),
    el_hcalIso       = cms.string("hcalPFClusterIso"),
    el_trkIso        = cms.string("trackIso"),
    el_dr03TkSumPt   = cms.string("dr03TkSumPt"),

    el_sumPUPt       = cms.string("pfIsolationVariables().sumPUPt"),
    el_reliso03      = cms.string("(pfIsolationVariables().sumChargedHadronPt + max(pfIsolationVariables().sumNeutralHadronEt + pfIsolationVariables().sumPhotonEt - 0.5 * pfIsolationVariables().sumPUPt,0.0)) / pt() "),

    #miniIsolation
    el_miniIsoChg    = cms.InputTag("probeEleMiniIso:h+-DR020-BarVeto000-EndVeto001-kt1000-Min005"),
    el_miniIsoNeu    = cms.InputTag("probeEleMiniIso:h0-DR020-BarVeto000-EndVeto000-kt1000-Min005"),
    el_miniIsoPho    = cms.InputTag("probeEleMiniIso:gamma-DR020-BarVeto000-EndVeto008-kt1000-Min005"),
    el_miniIsoEffA   = cms.InputTag("probeEleMiniIsoEffArea:EA-DR020-kt1000-Min005"),

    # tracker
    el_tk_pt        = cms.string("gsfTrack().ptMode"),
    el_tk_eta       = cms.string("gsfTrack().etaMode"),
    el_tk_phi       = cms.string("gsfTrack().phiMode"),
    el_fbrem         = cms.string("fbrem"),
    el_chisq         = cms.InputTag("eleVarHelper:chi2"),
    el_mHits         = cms.InputTag("eleVarHelper:missinghits"),
    el_dz            = cms.InputTag("eleVarHelper:dz"),
    el_dxy           = cms.InputTag("eleVarHelper:dxy"),
    el_3charge       = cms.string("chargeInfo().isGsfCtfScPixConsistent"),
    el_ecalDriven    = cms.string("ecalDrivenSeed"),
    
    )

PhoProbeVariablesToStore = cms.PSet(
    ph_eta    = cms.string("eta"),
    ph_abseta = cms.string("abs(eta)"),
    ph_et     = cms.string("et"),
    ph_e      = cms.string("energy"),

## super cluster quantities
    ph_sc_energy = cms.string("superCluster.energy"),
    ph_sc_et     = cms.string("superCluster.energy*sin(superCluster.position.theta)"),    
    ph_sc_eta    = cms.string("-log(tan(superCluster.position.theta/2))"),
    phsc_abseta = cms.string("abs(-log(tan(superCluster.position.theta/2)))"),


#id based
    ph_full5x5x_r9   = cms.string("full5x5_r9"),
    ph_r9            = cms.string("r9"),
    ph_sieie         = cms.string("full5x5_sigmaIetaIeta"),
    ph_sieip         = cms.InputTag("photonIDValueMapProducer:phoFull5x5SigmaIEtaIPhi"),
    ph_ESsigma       = cms.InputTag("photonIDValueMapProducer:phoESEffSigmaRR"),
    ph_hoe           = cms.string("hadronicOverEm"),

#iso
    ph_chIso    = cms.InputTag("photonIDValueMapProducer:phoChargedIsolation"),
    ph_neuIso   = cms.InputTag("photonIDValueMapProducer:phoNeutralHadronIsolation"),
    ph_phoIso   = cms.InputTag("photonIDValueMapProducer:phoPhotonIsolation"),
    ph_chWorIso = cms.InputTag("photonIDValueMapProducer:phoWorstChargedIsolation"), 

#pho mva
    ph_mva          = cms.InputTag("photonMVAValueMapProducer:PhotonMVAEstimatorRun2Spring15NonTrig25nsV2p1Values"),
    ph_mva80X       = cms.InputTag("photonMVAValueMapProducer:PhotonMVAEstimatorRun2Spring16NonTrigV1Values"),
)




TagVariablesToStore = cms.PSet(
    Ele_eta    = cms.string("eta"),
    Ele_phi    = cms.string("phi"),
    Ele_abseta = cms.string("abs(eta)"),
    Ele_pt     = cms.string("pt"),
    Ele_et     = cms.string("et"),
    Ele_e      = cms.string("energy"),
    Ele_q      = cms.string("charge"),
    
    ## super cluster quantities
    sc_e      = cms.string("superCluster.energy"),
    sc_et     = cms.string("superCluster.energy*sin(superClusterPosition.theta)"),    
    sc_eta    = cms.string("-log(tan(superClusterPosition.theta/2))"),
    sc_abseta = cms.string("abs(-log(tan(superCluster.position.theta/2)))"),

#    Ele_mHits         = cms.InputTag("eleVarHelper:missinghits"),
    Ele_dz            = cms.InputTag("eleVarHelper:dz"),
    Ele_dxy           = cms.InputTag("eleVarHelper:dxy"),
    Ele_nonTrigMVA    = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values"),
    Ele_trigMVA       = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15Trig25nsV1Values"),

    )

CommonStuffForGsfElectronProbe = cms.PSet(
    addEventVariablesInfo   =  cms.bool(True),

    variables        = cms.PSet(EleProbeVariablesToStore),
    pairVariables    =  cms.PSet(ZVariablesToStore),
    tagVariables     =  cms.PSet(TagVariablesToStore),

    ignoreExceptions = cms.bool (True),
    addRunLumiInfo   = cms.bool (True),
    pileupInfoTag    = cms.InputTag("slimmedAddPileupInfo"),
    vertexCollection = cms.InputTag("offlineSlimmedPrimaryVertices"),    
    beamSpot         = cms.InputTag("offlineBeamSpot"),
    addCaloMet       = cms.bool(False),
    pfMet            = cms.InputTag("slimmedMETsPuppi"),
    rho              = cms.InputTag("fixedGridRhoFastjetAll"),
    #    pfMet = cms.InputTag("slimmedMETsNoHF"),

    pairFlags     =  cms.PSet(
#    mass60to120 = cms.string("60 < mass < 120")
        ),
    tagFlags       =  cms.PSet(),    
    
    )

CommonStuffForPhotonProbe = CommonStuffForGsfElectronProbe.clone()
CommonStuffForPhotonProbe.variables = cms.PSet(PhoProbeVariablesToStore)

CommonStuffForSuperClusterProbe = CommonStuffForGsfElectronProbe.clone()
CommonStuffForSuperClusterProbe.variables = cms.PSet(SCProbeVariablesToStore)

mcTruthCommonStuff = cms.PSet(
    isMC = cms.bool(True),
    tagMatches   = cms.InputTag("genTagEle"),
    motherPdgId = cms.vint32(),
    #motherPdgId = cms.vint32(22,23),
    #motherPdgId = cms.vint32(443), # JPsi
    #motherPdgId = cms.vint32(553), # Yupsilon
    makeMCUnbiasTree = cms.bool(False),
    #checkMotherInUnbiasEff = cms.bool(False),
    mcVariables = cms.PSet(
        probe_eta    = cms.string("eta"),
        probe_phi    = cms.string("phi"),
        probe_et     = cms.string("et"),
        probe_e      = cms.string("energy"),
        ),
    mcFlags     =  cms.PSet(
        probe_flag = cms.string("pt>0")
        ),      
    )



def setupTnPVariablesForAOD():
    CommonStuffForSuperClusterProbe.pileupInfoTag    = cms.InputTag("addPileupInfo")
    CommonStuffForSuperClusterProbe.vertexCollection = cms.InputTag("offlinePrimaryVerticesWithBS")
    CommonStuffForSuperClusterProbe.pfMet            = cms.InputTag("pfMet")

    CommonStuffForGsfElectronProbe.pileupInfoTag     = cms.InputTag("addPileupInfo")
    CommonStuffForGsfElectronProbe.vertexCollection  = cms.InputTag("offlinePrimaryVerticesWithBS")
    CommonStuffForGsfElectronProbe.pfMet             = cms.InputTag("pfMet")

    CommonStuffForPhotonProbe.pileupInfoTag          = cms.InputTag("addPileupInfo")
    CommonStuffForPhotonProbe.vertexCollection       = cms.InputTag("offlinePrimaryVerticesWithBS")
    CommonStuffForPhotonProbe.pfMet                  = cms.InputTag("pfMet")

    del CommonStuffForGsfElectronProbe.variables.el_ecalIso
    del CommonStuffForGsfElectronProbe.variables.el_hcalIso
    del CommonStuffForGsfElectronProbe.variables.el_trkIso
   
