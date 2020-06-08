#!/bin/env python
import os

#
# Example script to submit TnPTreeProducer to crab
#
submitVersion = "2020-05-20"
doL1matching  = False

defaultArgs   = ['doEleID=True','doPhoID=True','doTrigger=True']
mainOutputDir = '/store/group/phys_egamma/tnpTuples/%s/%s' % (os.environ['USER'], submitVersion)

# Logging the current version of TnpTreeProducer here, such that you can find back what the actual code looked like when you were submitting
os.system('mkdir -p /eos/cms/%s' % mainOutputDir)
os.system('(git log -n 1;git diff) &> /eos/cms/%s/git.log' % mainOutputDir)


#
# Common CRAB settings
#
from CRABClient.UserUtilities import config
config = config()

config.General.requestName             = ''
config.General.transferLogs            = False
config.General.workArea                = 'crab_%s' % submitVersion

config.JobType.pluginName              = 'Analysis'
config.JobType.psetName                = '../python/TnPTreeProducer_cfg.py'
config.JobType.sendExternalFolder      = True
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset               = ''
config.Data.inputDBS                   = 'global'
config.Data.publication                = False
config.Data.allowNonValidInputDataset  = True
config.Site.storageSite                = 'T2_CH_CERN'


#
# Certified lumis for the different eras
#
def getLumiMask(era):
  if   '2016' in era: return 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
  elif '2017' in era: return 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt'
  elif '2018' in era: return 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions18/13TeV/PromptReco/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt'


#
# Submit command
#
from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException

def submit(config, requestName, sample, era, json, extraParam=[]):
  isMC                        = 'SIM' in sample
  config.General.requestName  = '%s_%s' % (era, requestName)
  config.Data.inputDataset    = sample
  config.Data.outLFNDirBase   = '%s/%s/%s/' % (mainOutputDir, era, 'mc' if isMC else 'data')
  config.Data.splitting       = 'FileBased' if isMC else 'LumiBased'
  config.Data.lumiMask        = None if isMC else json
  config.Data.unitsPerJob     = 5 if isMC else 25
  config.JobType.pyCfgParams  = defaultArgs + ['isMC=True' if isMC else 'isMC=False', 'era=%s' % era] + extraParam

  print config
  try:                           crabCommand('submit', config = config)
  except HTTPException as hte:   print "Failed submitting task: %s" % (hte.headers)
  except ClientException as cle: print "Failed submitting task: %s" % (cle)
  print
  print

#
# Wrapping the submit command
# In case of doL1matching=True, vary the L1Threshold and use sub-json
#
from multiprocessing import Process
def submitWrapper(requestName, sample, era, extraParam=[]):
  if doL1matching:
    from getLeg1ThresholdForDoubleEle import getLeg1ThresholdForDoubleEle
    for leg1Threshold, json in getLeg1ThresholdForDoubleEle(era):
      print 'Submitting for leg 1 threshold %s' % (leg1Threshold)
      p = Process(target=submit, args=(config, '%s_leg1Threshold%s' % (requestName, leg1Threshold), sample, era, json, extraParam + ['L1Threshold=%s' % leg1Threshold]))
      p.start()
      p.join()
  else:
    p = Process(target=submit, args=(config, requestName, sample, era, getLumiMask(era), extraParam))
    p.start()
    p.join()


#
# List of samples to submit, with eras
# If you would switch to AOD, don't forget to add 'isAOD=True' to the defaultArgs!
#

era       = 'UL2017'
submitWrapper('Run2017B', '/SingleElectron/Run2017B-09Aug2019_UL2017-v1/MINIAOD', era)
submitWrapper('Run2017C', '/SingleElectron/Run2017C-09Aug2019_UL2017-v1/MINIAOD', era)
submitWrapper('Run2017D', '/SingleElectron/Run2017D-09Aug2019_UL2017-v1/MINIAOD', era)
submitWrapper('Run2017E', '/SingleElectron/Run2017E-09Aug2019_UL2017-v1/MINIAOD', era)
submitWrapper('Run2017F', '/SingleElectron/Run2017F-09Aug2019_UL2017_EcalRecovery-v1/MINIAOD', era)

submitWrapper('DY_NLO',  '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', era)
submitWrapper('DY_LO',   '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', era)



era       = 'UL2018'
submitWrapper('Run2018A', '/EGamma/Run2018A-12Nov2019_UL2018-v2/MINIAOD', era)
submitWrapper('Run2018B', '/EGamma/Run2018B-12Nov2019_UL2018-v2/MINIAOD', era)
submitWrapper('Run2018C', '/EGamma/Run2018C-12Nov2019_UL2018-v2/MINIAOD', era)
submitWrapper('Run2018D', '/EGamma/Run2018D-12Nov2019_UL2018-v4/MINIAOD', era)

submitWrapper('DY_NLO',   '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM', era)
submitWrapper('DY_LO',    '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v1/MINIAODSIM', era)
