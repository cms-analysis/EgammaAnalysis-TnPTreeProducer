#!/bin/env python
import os
try:
    from CRABClient.UserUtilities import config
except ImportError:
    print
    print(
        "ERROR: Could not load CRABClient.UserUtilities.  Please source the crab3 setup:"
    )
    print("source /cvmfs/cms.cern.ch/crab3/crab.sh")
    exit(-1)
try:
    cmsswBaseDir = os.environ["CMSSW_BASE"]
except KeyError as e:
    print("Could not find CMSSW_BASE env var; have you set up the CMSSW environment?")
    exit(-1)

from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException
from multiprocessing import Process

#
# Example script to submit TnPTreeProducer to crab
#
##submitVersion = "2022-06-16-Run2018A"  # add some date here
#submitVersion = "2022-7-1-UL2018_NLO_inclusive"  # add some date here
submitVersion = "2016-pre-7-28-2022-NLO-unbinned"  # add some date here
doL1matching = False

defaultArgs = ["doEleID=True", "doPhoID=False", "doTrigger=True"]
mainOutputDir = "/store/user/ryi/LQ/TnP/%s" % (submitVersion)
#mainOutputDir = "/eos/user/r/ryi/LQ/TnP/%s" % (submitVersion)

# Logging the current version of TnpTreeProducer here, such that you can find back what the actual code looked like when you were submitting
# os.system("mkdir -p /eos/cms/%s" % mainOutputDir)
# os.system("(git log -n 1;git diff) &> /eos/cms/%s/git.log" % mainOutputDir)


#
# Common CRAB settings
#
config = config()

config.General.requestName = ""
config.General.transferLogs = False
config.General.workArea = "crab_%s" % submitVersion

config.JobType.pluginName = "Analysis"
config.JobType.psetName = "../python/TnPTreeProducer_cfg.py"
config.JobType.sendExternalFolder = True
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = ""
config.Data.inputDBS = "global"
config.Data.publication = False
# config.Data.allowNonValidInputDataset = True
#config.Site.storageSite = "T2_CH_CERN"
#config.Site.storageSite = "T2_US_Florida"
config.Site.storageSite = "T3_US_FNALLPC"


#
# Certified lumis for the different eras
#   (seems the JSON for UL2017 is slightly different from rereco 2017, it's not documented anywhere though)
#
def getLumiMask(era):
    if era == "2016":
        return "https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt"
    elif era == "2017":
        return "https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt"
    elif era == "2018":
        return "https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions18/13TeV/PromptReco/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt"
    elif "UL2016" in era:
        #return "https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt"
        return "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt"
#https://twiki.cern.ch/twiki/bin/view/CMS/PdmVLegacy2016postVFPAnalysis#Data_Certification
    elif era == "UL2017":
        return "https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt"
    elif era == "UL2018":
        return "https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt"
                                                                       #ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt


#
# Submit command
#
def submit(config, requestName, sample, era, json, extraParam=[]):
    isMC = "SIM" in sample
    config.General.requestName = "%s_%s" % (era, requestName)
    config.Data.inputDataset = sample
    config.Data.outLFNDirBase = "%s/%s/%s/" % (
        mainOutputDir,
        era,
        "mc" if isMC else "data",
    )
    config.Data.splitting = "FileBased" if isMC else "LumiBased"
    #config.Data.splitting = "Automatic" if isMC else "Automatic"
    config.Data.lumiMask = None if isMC else json
    config.Data.unitsPerJob = 5 if isMC else 40
#    config.Data.unitsPerJob = 180 if isMC else 180
    #config.Data.unitsPerJob = 2200 if isMC else 1050000
    config.JobType.pyCfgParams = (
        defaultArgs
        + ["isMC=True" if isMC else "isMC=False", "era=%s" % era]
        + extraParam
    )

    print config
    try:
        crabCommand("submit", config=config)
    except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
    except ClientException as cle:
        print "Failed submitting task: %s" % (cle)
    print
    print


#
# Wrapping the submit command
# In case of doL1matching=True, vary the L1Threshold and use sub-json
#A "wrapper" is a shell script that embeds a system command or utility, that saves a set of parameters passed to to that command. Wrapping a script around a complex command line simplifies invoking it.
def submitWrapper(requestName, sample, era, extraParam=[]):
    if doL1matching:
        from getLeg1ThresholdForDoubleEle import getLeg1ThresholdForDoubleEle

        for leg1Threshold, json in getLeg1ThresholdForDoubleEle(era):
            print "Submitting for leg 1 threshold %s" % (leg1Threshold)
            p = Process(
                target=submit,
                args=(
                    config,
                    "%s_leg1Threshold%s" % (requestName, leg1Threshold),
                    sample,
                    era,
                    json,
                    extraParam + ["L1Threshold=%s" % leg1Threshold],
                ),
            )
            p.start()
            p.join()
    else:
        p = Process(
            target=submit,
            args=(config, requestName, sample, era, getLumiMask(era), extraParam),
        )
        p.start()
        p.join()


#
# List of samples to submit, with eras
#era = "UL2017"
## Data
#submitWrapper(
#    "Run2017B", "/SingleElectron/Run2017B-UL2017_MiniAODv2-v1/MINIAOD", era
#)
#submitWrapper(
#    "Run2017C", "/SingleElectron/Run2017C-UL2017_MiniAODv2-v1/MINIAOD", era
#)
#submitWrapper(
#    "Run2017D", "/SingleElectron/Run2017D-UL2017_MiniAODv2-v1/MINIAOD", era
#)
#submitWrapper(
#    "Run2017E", "/SingleElectron/Run2017E-UL2017_MiniAODv2-v1/MINIAOD", era
#)
#submitWrapper(
#    "Run2017F", "/SingleElectron/Run2017F-UL2017_MiniAODv2-v1/MINIAOD", era
#)
## MC
#submitWrapper(
#    "DY_LO",
#    "/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM",
#    era,
#)
#submitWrapper(
#    "DY_LO_ext",
#    "/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9_ext1-v1/MINIAODSIM",
#    era,
#)
#submitWrapper("DY_NLO_0-50", "/DYJetsToLL_LHEFilterPtZ-0To50_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM", era)
#submitWrapper("DY_NLO_50-100", "/DYJetsToLL_LHEFilterPtZ-50To100_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM", era)
#submitWrapper("DY_NLO_100-250", "/DYJetsToLL_LHEFilterPtZ-100To250_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM", era)
#submitWrapper("DY_NLO_250-400", "/DYJetsToLL_LHEFilterPtZ-250To400_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM", era)
#submitWrapper("DY_NLO_400-650", "/DYJetsToLL_LHEFilterPtZ-400To650_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v4/MINIAODSIM", era)
#submitWrapper("DY_NLO_650-inf", "/DYJetsToLL_LHEFilterPtZ-650ToInf_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM", era)
#submitWrapper("DY_NLO", "/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM", era)


#era = "UL2018"
# Data
#submitWrapper("Run2018A", "/EGamma/Run2018A-UL2018_MiniAODv2-v1/MINIAOD", era)
#submitWrapper("Run2018B", "/EGamma/Run2018B-UL2018_MiniAODv2-v1/MINIAOD", era)
#submitWrapper("Run2018C", "/EGamma/Run2018C-UL2018_MiniAODv2-v1/MINIAOD", era)
#submitWrapper("Run2018D", "/EGamma/Run2018D-UL2018_MiniAODv2-v2/MINIAOD", era)
# MC
#submitWrapper("DY_NLO_0-50", "/DYJetsToLL_LHEFilterPtZ-0To50_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM", era)
#submitWrapper("DY_NLO_50-100", "/DYJetsToLL_LHEFilterPtZ-50To100_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM", era)
#submitWrapper("DY_NLO_100-250", "/DYJetsToLL_LHEFilterPtZ-100To250_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM", era)
#submitWrapper("DY_NLO_250-400", "/DYJetsToLL_LHEFilterPtZ-250To400_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM", era)
#submitWrapper("DY_NLO_400-650", "/DYJetsToLL_LHEFilterPtZ-400To650_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM", era)
#submitWrapper("DY_NLO_650-inf", "/DYJetsToLL_LHEFilterPtZ-650ToInf_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM", era)

#submitWrapper("DY_LO", "/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM", era)
#submitWrapper("DY_LO-ext", "/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1_ext1-v1/MINIAODSIM", era)
#submitWrapper("DY_NLO", "/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM", era)


era = "UL2016preVFP"
# Data
#submitWrapper("Run2016B", "/SingleElectron/Run2016B-ver1_HIPM_UL2016_MiniAODv2-v2/MINIAOD", era) #no good certified data
#submitWrapper("Run2016B_ver2", "/SingleElectron/Run2016B-ver2_HIPM_UL2016_MiniAODv2-v2/MINIAOD", era)
#submitWrapper("Run2016C", "/SingleElectron/Run2016C-HIPM_UL2016_MiniAODv2-v2/MINIAOD", era)
#submitWrapper("Run2016D", "/SingleElectron/Run2016D-HIPM_UL2016_MiniAODv2-v2/MINIAOD", era)
#submitWrapper("Run2016E", "/SingleElectron/Run2016E-HIPM_UL2016_MiniAODv2-v5/MINIAOD", era)
#submitWrapper("Run2016F", "/SingleElectron/Run2016F-HIPM_UL2016_MiniAODv2-v2/MINIAOD", era)
# MC
#submitWrapper("DY_pre_NLO", "/DYJetsToLL_LHEFilterPtZ-0To50_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM", era)
##https://cms-pdmv.cern.ch/grasp/samples?dataset_query=*DYJetsToLL_LHEFilterPtZ*&campaign=RunIISummer20UL16*GEN,RunIISummer20UL16*GENAPV,RunIISummer20UL17*GEN,RunIISummer20UL18*GEN
#submitWrapper("DY_pre_LO",  "/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM", era)
submitWrapper("DY_pre_NLO", "/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM", era)


#era = "UL2016postVFP"
#submitWrapper("Run2016F_postVFP", "/SingleElectron/Run2016F-UL2016_MiniAODv2-v2/MINIAOD", era)
#submitWrapper("Run2016G", "/SingleElectron/Run2016G-UL2016_MiniAODv2-v2/MINIAOD", era)
#submitWrapper("Run2016H", "/SingleElectron/Run2016H-UL2016_MiniAODv2-v2/MINIAOD", era)
##submitWrapper("DY_post_NLO", "/DYJetsToLL_LHEFilterPtZ-0To50_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM", era)
#submitWrapper("DY_post_LO",  "/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM", era)
#submitWrapper("DY_post_NLO", "/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM", era)

#https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVRun2LegacyAnalysis
#NLO:https://cms-pdmv.cern.ch/grasp/samples?dataset_query=*DYJetsToLL_LHEFilterPtZ*&campaign=RunIISummer20UL16*GEN,RunIISummer20UL16*GENAPV,RunIISummer20UL17*GEN,RunIISummer20UL18*GEN
