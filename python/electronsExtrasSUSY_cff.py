


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

    doJEC = True
    if (doJEC):
        from PhysicsTools.NanoAOD.jets_cff import updatedJets
        from PhysicsTools.NanoAOD.jets_cff import jetCorrFactors # is this needed?
        jetCorrFactors.src ='slimmedJets'
        updatedJets.jetSource ='slimmedJets'
        process.updatedJets = updatedJets
        process.jetCorrFactors = jetCorrFactors
    else:
        ptRatioRelForEle.srcJet = cms.InputTag("slimmedJets")

    process.isoForEle = isoForEle 
    process.ptRatioRelForEle = ptRatioRelForEle
    process.slimmedElectronsWithUserData = slimmedElectronsWithUserData
    process.electronMVATTH = electronMVATTH

    # Also save the raw ptRatio, with the JECs from the miniAOD
    ptRatioRelForEleUncorr = ptRatioRelForEle.clone()
    ptRatioRelForEleUncorr.srcJet = cms.InputTag("slimmedJets")
    process.ptRatioRelForEleUncorr = ptRatioRelForEleUncorr


    # Make a new electron collection, with additional variables that are used for the LeptonMVA below
    process.slimmedElectronsWithUserData.src = cms.InputTag(options['ELECTRON_COLL'])
    process.slimmedElectronsWithUserData.userFloats = cms.PSet(
        miniIsoChg = cms.InputTag("isoForEle:miniIsoChg"),
        miniIsoAll = cms.InputTag("isoForEle:miniIsoAll"),
        PFIsoChg = cms.InputTag("isoForEle:PFIsoChg"),
        PFIsoAll = cms.InputTag("isoForEle:PFIsoAll"),
        PFIsoAll04 = cms.InputTag("isoForEle:PFIsoAll04"),
        ptRatio = cms.InputTag("ptRatioRelForEle:ptRatio"),
        ptRatioUncorr = cms.InputTag("ptRatioRelForEleUncorr:ptRatio"),
        ptRel = cms.InputTag("ptRatioRelForEle:ptRel"),
        jetNDauChargedMVASel = cms.InputTag("ptRatioRelForEle:jetNDauChargedMVASel"),
        )
    process.slimmedElectronsWithUserData.userIntFromBools = cms.PSet() # Removed
    process.slimmedElectronsWithUserData.userInts = cms.PSet() # Removed


    # Run the ttH MVA
    # Cannot take EGMMVA directly from VID, because the TTHMVA producer only loads userFloat. Need to first put the EGMMVA in the object as a userFloats, with the names the TTHMVA expects
    process.slimmedElectronsWithUserDataWithVID = process.slimmedElectronsWithUserData.clone()
    process.slimmedElectronsWithUserDataWithVID.src = cms.InputTag("slimmedElectronsWithUserData")
    process.slimmedElectronsWithUserDataWithVID.userCands = cms.PSet() # Removed
    process.slimmedElectronsWithUserDataWithVID.userFloats = cms.PSet(
        mvaSpring16HZZ = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16HZZV1Values"),
        mvaFall17noIso = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV1Values"),
        )

    process.electronMVATTH.src = cms.InputTag("slimmedElectronsWithUserDataWithVID")

    # At the end of this, everything we need is either a userfloat or in a producer linked with slimmedElectronsWithUserData or slimmedElectronsWithUserDataWithVID

    # Next, we'll call Tom's MyElectronVariableHelper, which will calculate all the needed IDs. Alternatively, we could hack these into the fitter, since all the needed variables exist...
    # ... if the fitter can edit the probe requirements both at the numerator and the denominator, then all the work can be done there, starting from the loosest Tag/Probe combination!

    process.susyEleVarHelper = cms.EDProducer("SusyElectronVariableHelper",
        probes         = cms.InputTag("slimmedElectronsWithUserData"),
        probesWithLepMVA = cms.InputTag("slimmedElectronsWithUserDataWithVID"),        

        mvas           = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Values"),

        dxy            = cms.InputTag("eleVarHelper:dxy"),
        dz             = cms.InputTag("eleVarHelper:dz"),
        leptonMvas     = cms.InputTag("electronMVATTH"),
        rho            = cms.InputTag("fixedGridRhoFastjetAll"),
    )

    # Notes on the order of processes:
    # VID needs to run on the collection used to make goodElectrons (slimmedElectronsWithUserData) --> This means we can never add VID results to the collection making goodElectrons...
    # The DataEmbedder (slimmedElectronsWithUserData) breaks the references, so we need to run VID and EleVarHelper after it --> Again, can never add VID results as userFloats
    # Solution: make a temp electron collection with VID, use it to calculate the TTHMVA, and then teach the SusyElectronVariableHelper to load 2 electron collections, taking MVATTH from the temp one and adding it as a susyEleVarHelper variable. That way, the susyEleVarHelper re-establishes the link between TTHMVA and the main electron collection

    process.susy_sequence = cms.Sequence()

    if (doJEC) :
        process.susy_sequence += process.jetCorrFactors
        process.susy_sequence += process.updatedJets
        process.susy_sequence += process.ptRatioRelForEleUncorr

    process.susy_sequence += process.isoForEle
    process.susy_sequence += process.ptRatioRelForEle
    process.susy_sequence += process.slimmedElectronsWithUserData

    process.susy_sequence_requiresVID = cms.Sequence(
        process.slimmedElectronsWithUserDataWithVID + 
        process.electronMVATTH + 
        process.susyEleVarHelper
        )


