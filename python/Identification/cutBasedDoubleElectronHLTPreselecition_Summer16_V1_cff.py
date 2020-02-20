from PhysicsTools.SelectorUtils.centralIDRegistry import central_id_registry

import FWCore.ParameterSet.Config as cms

# Common functions and classes for ID definition are imported here:
from RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_tools import *


class DoubleEleHLTSelection_V1:
    """
    This is a container class to hold numerical cut values for either
    the barrel or endcap set of cuts for electron cut-based HLT-safe preselection
    """

    def __init__(
        self,
        idName,
        full5x5_sigmaIEtaIEtaCut,
        dEtaInSeedCut,
        dPhiInCut,
        hOverECut,
        absEInverseMinusPInverseCut,
        # isolations
        ecalPFClusterIsoCut,
        hcalPFClusterIsoCut,
        trkIsoCut,
    ):
        self.idName = idName
        self.full5x5_sigmaIEtaIEtaCut = full5x5_sigmaIEtaIEtaCut
        self.dEtaInSeedCut = dEtaInSeedCut
        self.dPhiInCut = dPhiInCut
        self.hOverECut = hOverECut
        self.absEInverseMinusPInverseCut = absEInverseMinusPInverseCut
        self.ecalPFClusterIsoCut = ecalPFClusterIsoCut
        self.hcalPFClusterIsoCut = hcalPFClusterIsoCut
        self.trkIsoCut = trkIsoCut


def psetSimpleEcalPFClusterIsoCut(wpEB, wpEE):
    return cms.PSet(
        cutName=cms.string("PatEleEBEECut"),
        cutString=cms.string("ecalPFClusterIso/pt"),
        cutValueEB=cms.double(wpEB.ecalPFClusterIsoCut),
        cutValueEE=cms.double(wpEE.ecalPFClusterIsoCut),
        needsAdditionalProducts=cms.bool(False),
        isIgnored=cms.bool(False),
    )


def psetSimpleHcalPFClusterIsoCut(wpEB, wpEE):
    return cms.PSet(
        cutName=cms.string("PatEleEBEECut"),
        cutString=cms.string("hcalPFClusterIso/pt"),
        cutValueEB=cms.double(wpEB.hcalPFClusterIsoCut),
        cutValueEE=cms.double(wpEE.hcalPFClusterIsoCut),
        needsAdditionalProducts=cms.bool(False),
        isIgnored=cms.bool(False),
    )


def psetSimpleTrackIsoCut(wpEB, wpEE):
    return cms.PSet(
        cutName=cms.string("PatEleEBEECut"),
        cutString=cms.string("dr03TkSumPt/pt"),
        cutValueEB=cms.double(wpEB.trkIsoCut),
        cutValueEE=cms.double(wpEE.trkIsoCut),
        needsAdditionalProducts=cms.bool(False),
        isIgnored=cms.bool(False),
    )


def configureVIDCutBasedDoubleEleHLTPreselection_V1(wpEB, wpEE):
    parameterSet = cms.PSet(
        idName=cms.string(wpEB.idName),  # same name stored in the _EB and _EE objects
        cutFlow=cms.VPSet(
            psetMinPtCut(),  # min pt cut
            psetPhoSCEtaMultiRangeCut(),  # eta cut
            psetPhoFull5x5SigmaIEtaIEtaCut(wpEB, wpEE),  # full 5x5 sigmaIEtaIEta cut
            psetDEtaInSeedCut(wpEB, wpEE),  # dEtaIn seed cut
            psetDPhiInCut(wpEB, wpEE),  # dPhiIn cut
            psetHadronicOverEMCut(wpEB, wpEE),  # H/E cut
            psetEInerseMinusPInverseCut(wpEB, wpEE),  # |1/e-1/p| cut
            psetSimpleEcalPFClusterIsoCut(wpEB, wpEE),  # ECAL PF Cluster isolation
            psetSimpleHcalPFClusterIsoCut(wpEB, wpEE),  # HCAL PF Cluster isolation
            psetSimpleTrackIsoCut(wpEB, wpEE),  # tracker isolation cut
        ),
    )
    #
    return parameterSet


#
# This file implements the cuts linked in this file in the line with the text
# "For double electron HLT triggers, one available offline emulation is...":
# https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2#HLT_safe_selection_for_2016_data
#

# Veto working point Barrel and Endcap
idName = "cutBasedDoubleElectronHLTPreselection-Summer16-V1"
WP_HLTSafe_EB = DoubleEleHLTSelection_V1(
    idName,  # idName
    0.011,  # full5x5_sigmaIEtaIEtaCut
    0.01,  # dEtaInSeedCut
    0.04,  # dPhiInCut
    0.08,  # hOverECut
    0.01,  # absEInverseMinusPInverseCut
    # Calorimeter isolations:
    0.45,  # ecalPFClusterIsoCut
    0.25,  # hcalPFClusterIsoCut
    # Tracker isolation:
    0.2,  # trkIsoCut
)

WP_HLTSafe_EE = DoubleEleHLTSelection_V1(
    idName,  # idName
    0.031,  # full5x5_sigmaIEtaIEtaCut
    0.01,  # dEtaInSeedCut - no cut
    0.08,  # dPhiInCut - no cut
    0.08,  # hOverECut
    0.01,  # absEInverseMinusPInverseCut
    # Calorimeter isolations:
    0.45,  # ecalPFClusterIsoCut
    0.25,  # hcalPFClusterIsoCut
    # Tracker isolation:
    0.2,  # trkIsoCut
)


#
# Set up VID configuration for all cuts and working points
#
cutBasedDoubleElectronHLTPreselection_Summer16_V1 = configureVIDCutBasedDoubleEleHLTPreselection_V1(
    WP_HLTSafe_EB, WP_HLTSafe_EE
)


# The MD5 sum numbers below reflect the exact set of cut variables
# and values above. If anything changes, one has to
# 1) comment out the lines below about the registry,
# 2) run "calculateMD5 <this file name> <one of the VID config names just above>
# 3) update the MD5 sum strings below and uncomment the lines again.
#

### for now until we have a database...
cutBasedDoubleElectronHLTPreselection_Summer16_V1.isPOGApproved = cms.untracked.bool(True)
