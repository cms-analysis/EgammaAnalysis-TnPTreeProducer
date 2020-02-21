#!/bin/env python
import os

#
# Example script to submit TnPTreeProducer to crab
# Currently implemented for 2018 data/MC (TODO: get all default values for 2016/2017 in here)
#
submitVersion = "test"

defaultArgs   = ['doEleID=True','doPhoID=False','doTrigger=True']
mainOutputDir = '/store/user/%s/tnpTuples/%s' % (os.environ['USER'], submitVersion)
from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config
config = config()

config.General.requestName            = ''
config.General.transferLogs           = False
config.JobType.pluginName             = 'Analysis'

config.JobType.psetName               = '../../python/TnPTreeProducer_cfg.py'
config.JobType.sendExternalFolder     = True

config.Data.inputDataset              = ''
config.Data.inputDBS                  = 'global'
config.Data.publication               = False
config.Data.allowNonValidInputDataset = True
config.Site.storageSite               = 'T2_CH_CERN'


def getLumiMask(era):
  if   era=='2016': return 'TO_BE_ADDED'
  elif era=='2017': return 'TO_BE_ADDED'
  elif era=='2018': return 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions18/13TeV/PromptReco/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt'

if __name__ == '__main__':
  from CRABAPI.RawCommand import crabCommand
  from CRABClient.ClientExceptions import ClientException
  from httplib import HTTPException

  # We want to put all the CRAB project directories from the tasks we submit here into one common directory.
  # That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).
  config.General.workArea = 'crab_%s' % submitVersion

  def submit(config, requestName, sample, era, globalTag):
    isMC                        = 'SIM' in sample
    config.General.requestName  = requestName
    config.Data.inputDataset    = sample
    config.Data.outLFNDirBase   = '%s/%s/' % (mainOutputDir, 'mc' if isMC else 'data')
    config.Data.splitting       = 'FileBased' if isMC else 'LumiBased'
    config.Data.lumiMask        = None if isMC else getLumiMask(era) 
    config.Data.unitsPerJob     = 5 if isMC else 100
    config.JobType.pyCfgParams  = defaultArgs + ['isMC=True' if isMC else 'isMC=False', 'GT=%' % globalTag, 'era=%s' % era]

    try:
      crabCommand('submit', config = config)
    except HTTPException as hte:
      print "Failed submitting task: %s" % (hte.headers)
    except ClientException as cle:
      print "Failed submitting task: %s" % (cle)

  # If you would switch to AOD, don't forget to add 'isAOD=True' to the defaultArgs!
  era       = '2016'
  globalTag = '94X_dataRun2_v10'
  submit(config, 'Run2016B', '/SingleElectron/Run2016B-07Aug17_ver2-v2/MINIAOD', era, globalTag)
  submit(config, 'Run2016C', '/SingleElectron/Run2016C-07Aug17-v1/MINIAOD', era, globalTag)
  submit(config, 'Run2016D', '/SingleElectron/Run2016D-07Aug17-v1/MINIAOD', era, globalTag)
  submit(config, 'Run2016E', '/SingleElectron/Run2016E-07Aug17-v1/MINIAOD', era, globalTag)
  submit(config, 'Run2016F', '/SingleElectron/Run2016F-07Aug17-v1/MINIAOD', era, globalTag)
  submit(config, 'Run2016G', '/SingleElectron/Run2016G-07Aug17-v1/MINIAOD', era, globalTag)
  submit(config, 'Run2016H', '/SingleElectron/Run2016H-07Aug17v1/MINIAOD', era, globalTag)

  globalTag = '94X_mcRun2_asymptotic_v3'
  submit(config, 'DY_NLO', '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1/MINIAODSIM', era, globalTag)
  submit(config, 'DY_LO',  '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM', era, globalTag)

  era       = '2017'
  globalTag = '94X_dataRun2_v11'
  submit(config, 'Run2017B', '/SingleElectron/Run2017B-31Mar2018-v1/MINIAOD', era, globalTag)
  submit(config, 'Run2017C', '/SingleElectron/Run2017C-31Mar2018-v1/MINIAOD', era, globalTag)
  submit(config, 'Run2017D', '/SingleElectron/Run2017D-31Mar2018-v1/MINIAOD', era, globalTag)
  submit(config, 'Run2017E', '/SingleElectron/Run2017E-31Mar2018-v1/MINIAOD', era, globalTag)
  submit(config, 'Run2017F', '/SingleElectron/Run2017F-31Mar2018-v1/MINIAOD', era, globalTag)

  globalTag = '94X_mc2017_realistic_v17'
  submit(config, 'DY1_LO',     '/DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM', era, globalTag)
  submit(config, 'DY1_LO_ext', '/DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_v3_94X_mc2017_realistic_v14_ext1-v2/MINIAODSIM', era, globalTag)
  submit(config, 'DY_NLO',     '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',  era, globalTag)
  submit(config, 'DY_NLO_ext', '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', era, globalTag)
 


  era       = '2018'
  globalTag = '102X_dataRun2_v12'
  submit(config, 'Run2018A', '/EGamma/Run2018A-17Sep2018-v2/MINIAOD', era, globalTag)
  submit(config, 'Run2018B', '/EGamma/Run2018B-17Sep2018-v1/MINIAOD', era, globalTag)
  submit(config, 'Run2018C', '/EGamma/Run2018C-17Sep2018-v1/MINIAOD', era, globalTag)
  globalTag = '102X_dataRun2_Prompt_v15'
  submit(config, 'Run2018D', '/EGamma/Run2018D-PromptReco-v2/MINIAOD', era, globalTag)

  globalTag = '102X_upgrade2018_realistic_v20'
  submit(config, 'DY',     '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', era, globalTag)
  submit(config, 'DY_pow', '/DYToEE_M-50_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', era, globalTag) 

