import FWCore.ParameterSet.Config as cms

##########################################################################
## TREE CONTENT
#########################################################################
    
from EgammaAnalysis.TnPTreeProducer.cmssw_version import isReleaseAbove

ZVariablesToStore = cms.PSet(
    eta = cms.string("eta"),
    abseta = cms.string("abs(eta)"),
    pt  = cms.string("pt"),
    mass  = cms.string("mass"),
    )   

SCProbeVariablesToStore = cms.PSet(
    sc_eta    = cms.string("eta"),
    sc_phi    = cms.string("phi"),
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
    el_isGap  = cms.string("isGap"),
    
    ## super cluster quantities
    el_sc_e          = cms.string("superCluster().energy"),
    el_sc_rawE       = cms.string("superCluster().rawEnergy"),
    el_sc_esE        = cms.string("superCluster().preshowerEnergy"),
    el_sc_et         = cms.string("superCluster().energy*sin(superClusterPosition.theta)"),    
    el_sc_eta        = cms.string("-log(tan(superCluster.position.theta/2))"),
    el_sc_phi        = cms.string("superCluster.phi"),    
    el_sc_abseta     = cms.string("abs(-log(tan(superCluster.position.theta/2)))"),
    el_seed_e        = cms.string("superCluster.seed.energy"), 
    el_ecalEnergy    = cms.string("ecalEnergy()"),
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

    el_5x5_circularity = cms.InputTag("eleVarHelper:5x5circularity"),
    el_5x5_hoe       = cms.string("full5x5_hcalOverEcal()"),

    el_hoe           = cms.string("hadronicOverEm()"),    
    el_hoe_bc           = cms.string("hcalOverEcalBc"),
    el_eoverp_wES        = cms.string("(superCluster().rawEnergy+superCluster().preshowerEnergy)/gsfTrack().pMode()"),
    el_1overEminus1overP        = cms.string("abs(1-eSuperClusterOverP())/ecalEnergy()"),

    # mva id

    el_nonTrigMVA80X = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Values"),
    el_hzzMVA80X     = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16HZZV1Values"),
    el_noIsoMVA94X     = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV1Values"),
    el_IsoMVA94X     = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17IsoV1RawValues"),
    el_noIsoMVA94XV2     = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV2RawValues"),
    el_IsoMVA94XV2     = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17IsoV2RawValues"),

     
    #isolation
    el_chIso               = cms.string("pfIsolationVariables().sumChargedHadronPt"),
    el_phoIso              = cms.string("pfIsolationVariables().sumPhotonEt"),
    el_neuIso              = cms.string("pfIsolationVariables().sumNeutralHadronEt"),
    el_dr03EcalRecHitSumEt = cms.string("dr03EcalRecHitSumEt"),
    el_ecalIso             = cms.string("ecalPFClusterIso"), # this one seem to be always 0 in CMSSW_10_2_X
    el_hcalIso             = cms.string("hcalPFClusterIso"), # this one seem to be always 0 in CMSSW_10_2_X
    el_trkIso              = cms.string("trackIso"),
    el_dr03TkSumPt         = cms.string("dr03TkSumPt"),

    # this relative PF lepton isolation component is added to the standard PF isolation sum
    # in order to get the isolation variable used in the triboson analysis
    # in the small test runs this variable is always 0, but I guess it is very rare to find another lepton in the cone
    el_relPfLepIso03 = cms.InputTag("eleVarHelper:pfLeptonIsolation"),

    #added for VHbbEIso
    el_sumPUPt       = cms.string("pfIsolationVariables().sumPUPt"),
    el_relIso03_dB   = cms.string("(pfIsolationVariables().sumChargedHadronPt + max(pfIsolationVariables().sumNeutralHadronEt + pfIsolationVariables().sumPhotonEt - 0.5 * pfIsolationVariables().sumPUPt,0.0)) / pt() "),

    # tracker Variabels
    el_tk_pt        = cms.string("gsfTrack().ptMode"),
    el_tk_eta       = cms.string("gsfTrack().etaMode"),
    el_tk_phi       = cms.string("gsfTrack().phiMode"),
    el_fbrem         = cms.string("fbrem"),
    el_mHits         = cms.InputTag("eleVarHelper:missinghits"),
    el_gsfHits         = cms.InputTag("eleVarHelper:gsfhits"),
    el_dz            = cms.InputTag("eleVarHelper:dz"),
    el_dxy           = cms.InputTag("eleVarHelper:dxy"),
    el_sip           = cms.InputTag("eleVarHelper:sip"),
    el_3charge       = cms.string("chargeInfo().isGsfCtfScPixConsistent"),
    el_ecalDriven    = cms.string("ecalDrivenSeed"),

    el_gsfhits        = cms.string("gsfTrack().hitPattern().trackerLayersWithMeasurement()"),
    el_gsfchi2        = cms.string("gsfTrack().normalizedChi2()"),
    el_kfhits         = cms.InputTag("eleVarHelper:kfhits"),
    el_kfchi2         = cms.InputTag("eleVarHelper:kfchi2"),
    el_lost_hits      = cms.string("gsfTrack().lost()"),
    el_found_hits     = cms.string("gsfTrack().found()"), # sometimes called valid_hits
    el_convVtxFitProb  = cms.InputTag("eleVarHelper:convVtxFitProb"),

    el_hasMatchedConversion = cms.InputTag("eleVarHelper:hasMatchedConversion"),

    # Track cluster matching
    el_ep             = cms.string("eSuperClusterOverP()"),
    el_eelepout       = cms.string("eEleClusterOverPout()"),
    el_IoEmIop        = cms.InputTag("eleVarHelper:ioemiop"),

    )

PhoProbeVariablesToStore = cms.PSet(
    ph_eta    = cms.string("eta"),
    ph_abseta = cms.string("abs(eta)"),
    ph_et     = cms.string("et"),
    ph_e      = cms.string("energy"),

## super cluster quantities
    ph_sc_energy    = cms.string("superCluster.energy"),
    ph_sc_rawEnergy = cms.string("superCluster.rawEnergy"),
    ph_sc_et        = cms.string("superCluster.energy*sin(superCluster.position.theta)"),
    ph_sc_eta       = cms.string("-log(tan(superCluster.position.theta/2))"),
    ph_sc_abseta    = cms.string("abs(-log(tan(superCluster.position.theta/2)))"),
    ph_sc_etaWidth  = cms.string("superCluster.etaWidth"),
    ph_sc_phiWidth  = cms.string("superCluster.phiWidth"),

## preshower energy plane 1 and 2
    ph_preshower_energy_plane1 = cms.string("superCluster.preshowerEnergyPlane1"),
    ph_preshower_energy_plane2 = cms.string("superCluster.preshowerEnergyPlane2"),


#id based
    ph_full5x5x_r9   = cms.string("full5x5_r9"),
    ph_r9            = cms.string("r9"),
    ph_sieie         = cms.string("full5x5_sigmaIetaIeta"),
    ph_s4            = cms.string("full5x5_showerShapeVariables.e2x2/full5x5_showerShapeVariables.e5x5"),
    ph_sieip         = cms.string("full5x5_showerShapeVariables.sigmaIetaIphi"),
    ph_ESsigma       = cms.string("full5x5_showerShapeVariables.effSigmaRR"),
    ph_hoe           = cms.string("hadronicOverEm"),

#pho mva
    ph_mva80X       = cms.InputTag("photonMVAValueMapProducer:PhotonMVAEstimatorRun2Spring16NonTrigV1Values"),
    ph_mva94X       = cms.InputTag("photonMVAValueMapProducer:PhotonMVAEstimatorRunIIFall17v1p1Values"),
    ph_mva94XV2     = cms.InputTag("photonMVAValueMapProducer:PhotonMVAEstimatorRunIIFall17v2Values"),

# iso
    ph_chIso    = cms.string("chargedHadronIso"),
    ph_neuIso   = cms.string("neutralHadronIso"),
    ph_phoIso   = cms.string("photonIso"),
    ph_chWorIso = cms.string("chargedHadronWorstVtxIso"),
)

if not isReleaseAbove(10, 6): # old way of accessing these in CMSSW_10_2
    PhoProbeVariablesToStore.ph_sieip    = cms.InputTag("photonIDValueMapProducer:phoFull5x5SigmaIEtaIPhi")
    PhoProbeVariablesToStore.ph_ESsigma  = cms.InputTag("photonIDValueMapProducer:phoESEffSigmaRR")
    PhoProbeVariablesToStore.ph_chIso    = cms.InputTag("photonIDValueMapProducer:phoChargedIsolation")
    PhoProbeVariablesToStore.ph_neuIso   = cms.InputTag("photonIDValueMapProducer:phoNeutralHadronIsolation")
    PhoProbeVariablesToStore.ph_phoIso   = cms.InputTag("photonIDValueMapProducer:phoPhotonIsolation")
    PhoProbeVariablesToStore.ph_chWorIso = cms.InputTag("photonIDValueMapProducer:phoWorstChargedIsolation")

TagVariablesToStore = cms.PSet(
    Ele_eta    = cms.string("eta"),
    Ele_phi    = cms.string("phi"),
    Ele_abseta = cms.string("abs(eta)"),
    Ele_pt     = cms.string("pt"),
    Ele_et     = cms.string("et"),
    Ele_e      = cms.string("energy"),
    Ele_q      = cms.string("charge"),
    Ele_3charge = cms.string("chargeInfo().isGsfCtfScPixConsistent"),
    
    ## super cluster quantities
    sc_e      = cms.string("superCluster.energy"),
    sc_et     = cms.string("superCluster.energy*sin(superClusterPosition.theta)"),    
    sc_eta    = cms.string("-log(tan(superClusterPosition.theta/2))"),
    sc_abseta = cms.string("abs(-log(tan(superCluster.position.theta/2)))"),

#    Ele_mHits         = cms.InputTag("eleVarHelper:missinghits"),
    Ele_dz            = cms.InputTag("eleVarHelper:dz"),
    Ele_dxy           = cms.InputTag("eleVarHelper:dxy"),
    el_sip           = cms.InputTag("eleVarHelper:sip"),
    Ele_nonTrigMVA80X    = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Values"),
    Ele_hzzMVA80X    = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16HZZV1Values"),

    Ele_trigMVA       = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17IsoV1Values"),

    Ele_noIsoMVA94X   = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV1Values"), 
    Ele_IsoMVA94X   = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17IsoV1Values"),
    Ele_noIsoMVA94XV2   = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV2Values"), 
    Ele_IsoMVA94XV2   = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17IsoV2Values"),
    )

CommonStuffForGsfElectronProbe = cms.PSet(
    addEventVariablesInfo   =  cms.bool(True),

    variables        = cms.PSet(EleProbeVariablesToStore),
    pairVariables    =  cms.PSet(ZVariablesToStore),
    tagVariables     =  cms.PSet(TagVariablesToStore),

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


def getTnPVariablesForMCTruth(isMC=True):
    if isMC:
      return cms.PSet(
        isMC                   = cms.bool(True),
        tagMatches             = cms.InputTag("genTagEle"),
        motherPdgId            = cms.vint32(),
       #motherPdgId            = cms.vint32(22,23),
       #motherPdgId            = cms.vint32(443), # JPsi
       #motherPdgId            = cms.vint32(553), # Yupsilon
        makeMCUnbiasTree       = cms.bool(False),
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
    else:
      return cms.PSet(isMC = cms.bool(False))


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
   
