#!/bin/env python
import os

#
# Example script to submit TnPTreeProducer to crab
# Currently implemented for 2018 data/MC (TODO: get all default values for 2016/2017 in here)
#
submitVersion = "test"

defaultArgs   = ['doEleID=True','doPhoID=False','doTrigger=True', 'era=2018']
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


if __name__ == '__main__':
  from CRABAPI.RawCommand import crabCommand
  from CRABClient.ClientExceptions import ClientException
  from httplib import HTTPException

  # We want to put all the CRAB project directories from the tasks we submit here into one common directory.
  # That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).
  config.General.workArea = 'crab_%s' % submitVersion

  def submit(config, sample, globalTag):
    isMC                        = 'SIM' in sample
    config.General.requestName  = sample.split('/')[-2]
    config.Data.inputDataset    = sample
    config.Data.outLFNDirBase   = '%s/%s/' % (mainOutputDir, 'mc' if isMC else 'data')
    config.Data.splitting       = 'FileBased' if isMC else 'LumiBased'
    config.Data.lumiMask        = None if isMC else 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions18/13TeV/PromptReco/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt'
    config.Data.unitsPerJob     = 5 if isMC else 100
    config.JobType.pyCfgParams  = defaultArgs + ['isMC=True' if isMC else 'isMC=False', 'GT=%' % globalTag]

    try:
      crabCommand('submit', config = config)
    except HTTPException as hte:
      print "Failed submitting task: %s" % (hte.headers)
    except ClientException as cle:
      print "Failed submitting task: %s" % (cle)

  # If you would switch to AOD, don't forget to add 'isAOD=True' to the defaultArgs!
  globalTag = '102X_dataRun2_Sep2018ABC_v2'
  submit(config, '/EGamma/Run2018A-17Sep2018-v2/MINIAOD', globalTag)
  submit(config, '/EGamma/Run2018B-17Sep2018-v1/MINIAOD', globalTag)
  submit(config, '/EGamma/Run2018C-17Sep2018-v1/MINIAOD', globalTag)
  globalTag = '102X_dataRun2_Prompt_v13'
  submit(config, '/EGamma/Run2018D-PromptReco-v2/MINIAOD', globalTag)

  globalTag = '102X_upgrade2018_realistic_v18'
  submit(config, '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', globalTag)
