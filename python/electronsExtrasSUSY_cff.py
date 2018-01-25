


import FWCore.ParameterSet.Config as cms
from math import ceil,log

 # All workingpoints we need to probe
# Note: cut based wp are without isolation
workingPoints = ["ConvVeto", "MVAVLooseFO", "MVAVLoose", "Mini", "Mini2", "Mini4",
    "MVAVLooseMini", "MVAVLooseMini2", "MVAVLooseMini4", "MVATight", "MVAWP80", "MVAWP90",
     "TightIP2D", "TightIP3D", "IDEmu", "ISOEmu", "Charge", "IHit0", "IHit1", "Loose2D",
     "TightIP2D", "TightIP3D", "IDEmu", "ISOEmu", "IHit0", "IHit1", "Loose2D",
     "FOID2D", "Tight2D3D", "TightID2D3D", "ConvIHit0", "TightConvIHit0", "ConvIHit1", "ConvIHit0Chg",
     "FOID2D", "Tight2D3D", "TightID2D3D", "TightConvIHit0", "ConvIHit1", "ConvIHit0Chg",
     "MultiIsoM", "MultiIsoT", "MultiIsoVT", "MultiIsoEmu", "LeptonMvaM", "LeptonMvaVT",
     "CutBasedVetoNoIso", "CutBasedLooseNoIso", "CutBasedMediumNoIso", "CutBasedTightNoIso",
     "CutBasedVetoNoIso94X", "CutBasedLooseNoIso94X", "CutBasedMediumNoIso94X", "CutBasedTightNoIso94X",
     "CutBasedMediumMini", "CutBasedTightMini", "CutBasedMediumMini94X", "CutBasedTightMini94X", "CutBasedStopsDilepton",
     "LeptonMvaVTIDEmuTightIP2DSIP3D8miniIso04", "LeptonMvaMIDEmuTightIP2DSIP3D8miniIso04"]



def addSusyIDs(process, options):

    # For some reason importing the NanoAOD configuration breakes VID, so we need to make 
    # sure these lines are called before calling setIDs() in the egmTreesSetup
    from PhysicsTools.NanoAOD.electrons_cff import isoForEle 
    from PhysicsTools.NanoAOD.electrons_cff import ptRatioRelForEle
    from PhysicsTools.NanoAOD.electrons_cff import slimmedElectronsWithUserData
    from PhysicsTools.NanoAOD.electrons_cff import electronMVATTH

    process.isoForEle = isoForEle 
    process.ptRatioRelForEle = ptRatioRelForEle
    process.slimmedElectronsWithUserData = slimmedElectronsWithUserData
    process.electronMVATTH = electronMVATTH

    # Make a new electron collection, with additional variables that are used for the LeptonMVA below
    process.slimmedElectronsWithUserData.src = cms.InputTag(options['ELECTRON_COLL'])
    process.slimmedElectronsWithUserData.userFloats = cms.PSet(
        miniIsoChg = cms.InputTag("isoForEle:miniIsoChg"),
        miniIsoAll = cms.InputTag("isoForEle:miniIsoAll"),
        PFIsoChg = cms.InputTag("isoForEle:PFIsoChg"),
        PFIsoAll = cms.InputTag("isoForEle:PFIsoAll"),
        ptRatio = cms.InputTag("ptRatioRelForEle:ptRatio"),
        ptRel = cms.InputTag("ptRatioRelForEle:ptRel"),
        jetNDauChargedMVASel = cms.InputTag("ptRatioRelForEle:jetNDauChargedMVASel"),
        )
    process.slimmedElectronsWithUserData.userIntFromBools = cms.PSet() # Removed
    process.slimmedElectronsWithUserData.userInts = cms.PSet() # Removed

    # Run the ttH MVA, modify src and take MVA directly from VID (VID must run before this producer)
    process.electronMVATTH.src = cms.InputTag("slimmedElectronsWithUserData")
    process.electronMVATTH.variables = cms.PSet(
        LepGood_pt = cms.string("pt"),
        LepGood_eta = cms.string("eta"),
        LepGood_jetNDauChargedMVASel = cms.string("userFloat('jetNDauChargedMVASel')"),
        LepGood_miniRelIsoCharged = cms.string("userFloat('miniIsoChg')/pt"),
        LepGood_miniRelIsoNeutral = cms.string("(userFloat('miniIsoAll')-userFloat('miniIsoChg'))/pt"),
        LepGood_jetPtRelv2 = cms.string("userFloat('ptRel')"),
        LepGood_jetPtRatio = cms.string("min(userFloat('ptRatio'),1.5)"),
        LepGood_jetBTagCSV = cms.string("?userCand('jetForLepJetVar').isNonnull()?max(userCand('jetForLepJetVar').bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags'),0.0):-99.0"),
        LepGood_sip3d = cms.string("abs(dB('PV3D')/edB('PV3D'))"),
        LepGood_dxy = cms.string("log(abs(dB('PV2D')))"),
        LepGood_dz = cms.string("log(abs(dB('PVDZ')))"),
        LepGood_mvaIdSpring16HZZ = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16HZZV1Values"),
    )

    # At the end of this, everything we need is either a userfloat or in a producer linked with slimmedElectronsWithUserData

    # Next, we'll call Tom's MyElectronVariableHelper, which will calculate all the needed IDs. Alternatively, we could hack these into the fitter, since all the needed variables exist...
    # ... if the fitter can edit the probe requirements both at the numerator and the denominator, then all the work can be done there, starting from the loosest Tag/Probe combination!

    process.susyEleVarHelper = cms.EDProducer("SusyElectronVariableHelper",
        probes         = cms.InputTag("slimmedElectronsWithUserData"),
        mvas           = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values"),
        dxy            = cms.InputTag("eleVarHelper:dxy"),
        dz             = cms.InputTag("eleVarHelper:dz"),
        leptonMvas     = cms.InputTag("electronMVATTH"),
        rho            = cms.InputTag("fixedGridRhoFastjetAll"),
    )



    process.susy_sequence = cms.Sequence(
        process.isoForEle +
        process.ptRatioRelForEle + 
        process.slimmedElectronsWithUserData 
        )

    process.susy_sequence_requiresVID = cms.Sequence(
        process.electronMVATTH + 
        process.susyEleVarHelper
        )


