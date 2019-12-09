#!/bin/env python

### Version of submission ###
submitVersion = "test"



defaultArgs   = ['isMC=False','doEleID=False','doPhoID=False','doTrigger=True', 'GT=101X_dataRun2_Prompt_v9']
mainOutputDir = '/store/user/tomc/tnpTuples/%s' % submitVersion # Change to your own

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
config.Site.storageSite               = 'T2_BE_IIHE' #'T2_CH_CERN'


  
if __name__ == '__main__':

  import urllib, os, glob
  def download(url, destination):
    try:    os.makedirs(destination)
    except: pass
    urllib.urlretrieve(url, os.path.join(destination, url.split('/')[-1])) 

  def getSeedsForDoubleEle(year): # note: only getting DoubleEle seeds here
    prescalePage = 'https://tomc.web.cern.ch/tomc/triggerPrescales/%s/' % year
    hltTrigger   = 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'
    dirToStore   = os.path.join('prescaleInformation', year, hltTrigger)
    download(prescalePage + hltTrigger + '.php', dirToStore) 
    with open(os.path.join(dirToStore, hltTrigger + '.php')) as f:
      for line in f:
        if 'prescale1' in line and 'L1_DoubleEG' in line: 
          download(prescalePage + line.split('>')[0].split('=')[-1], dirToStore)

    for json in glob.glob(os.path.join(dirToStore, '*.json')):
      leg1 = int(json.split('L1_DoubleEG_')[-1].split('_')[0].replace('LooseIso', ''))
      leg2 = int(json.split('L1_DoubleEG_')[-1].split('_')[1].replace('LooseIso', ''))
      yield leg1, leg2, json


  from CRABAPI.RawCommand import crabCommand
  from CRABClient.ClientExceptions import ClientException
  from httplib import HTTPException

  # We want to put all the CRAB project directories from the tasks we submit here into one common directory.
  # That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).
  config.General.workArea = 'crab_%s' % submitVersion

  def submit(config, sample, leg1threshold, leg2threshold, json):
    config.General.requestName  = sample.split('/')[-2] + '_%s_%s' % (leg1threshold, leg2threshold)
    config.Data.inputDataset    = '/EGamma/Run2018A-PromptReco-v1/MINIAOD'
    config.Data.outLFNDirBase   = '%s/%s/' % (mainOutputDir,'data')
    config.Data.splitting       = 'LumiBased'
    config.Data.lumiMask        = json
    config.Data.unitsPerJob     = 100
    config.JobType.pyCfgParams  = defaultArgs + ['leg1Threshold=%s' % leg1threshold, 'leg2Threshold=%s' % leg2threshold] 

    try:
      crabCommand('submit', config = config)
    except HTTPException as hte:
      print "Failed submitting task: %s" % (hte.headers)
    except ClientException as cle:
      print "Failed submitting task: %s" % (cle)

  for leg1, leg2, json in getSeedsForDoubleEle('2018'):
    # Crab fails on this on second iteration, of course with only a very cryptic error message
    # Not sure how to workaround this
    submit(config, '/EGamma/Run2018A-PromptReco-v1/MINIAOD', leg1, leg2, json)

