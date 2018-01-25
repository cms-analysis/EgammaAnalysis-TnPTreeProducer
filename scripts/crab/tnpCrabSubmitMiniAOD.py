from CRABClient.UserUtilities import config, getUsernameFromSiteDB
import sys
config = config()

submitVersion = "Moriond18_V1"
doEleTree = 'doEleID=True'
doPhoTree = 'doPhoID=True'
#doHLTTree = 'doTrigger=False'
#calibEn   = 'useCalibEn=False'

mainOutputDir = '/store/group/phys_egamma/soffi/TnP/ntuples_01162018/%s' % submitVersion

config.General.transferLogs = False

config.JobType.pluginName  = 'Analysis'

# Name of the CMSSW configuration file
config.JobType.psetName  = '/afs/cern.ch/user/s/soffi/scratch0/TEST/CMSSW-10-0-0-pre3/src/EgammaAnalysis/TnPTreeProducer/python/TnPTreeProducer_cfg.py'
#config.Data.allowNonValidInputDataset = False
config.JobType.sendExternalFolder     = True

config.Data.inputDBS = 'global'
config.Data.publication = False
config.Data.allowNonValidInputDataset = True
#config.Data.publishDataName = 

config.Site.storageSite = 'T2_CH_CERN'



if __name__ == '__main__':

    from CRABAPI.RawCommand import crabCommand
    from CRABClient.ClientExceptions import ClientException
    from httplib import HTTPException

    # We want to put all the CRAB project directories from the tasks we submit here into one common directory.
    # That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).
    config.General.workArea = 'crab_%s' % submitVersion

    def submit(config):
        try:
            crabCommand('submit', config = config)
        except HTTPException as hte:
            print "Failed submitting task: %s" % (hte.headers)
        except ClientException as cle:
            print "Failed submitting task: %s" % (cle)


    ##### submit MC
    config.Data.outLFNDirBase = '%s/%s/' % (mainOutputDir,'mc')
    config.Data.splitting     = 'FileBased'
    config.Data.unitsPerJob   = 8
    config.JobType.pyCfgParams  = ['isMC=True',doEleTree,doPhoTree,'GT=94X_mc2017_realistic_v10']


    config.General.requestName  = 'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8'
    config.Data.inputDataset    = '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-RECOSIMstep_94X_mc2017_realistic_v10-v1/MINIAODSIM'
    submit(config)
    config.General.requestName  = 'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8-ext1'
    config.Data.inputDataset    = '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-RECOSIMstep_94X_mc2017_realistic_v10_ext1-v1/MINIAODSIM'
    submit(config)

    ##### now submit DATA
    config.Data.outLFNDirBase = '%s/%s/' % (mainOutputDir,'data')
    config.Data.splitting     = 'LumiBased'
    config.Data.lumiMask      = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/PromptReco/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'
    config.Data.unitsPerJob   = 100
    config.JobType.pyCfgParams  = ['isMC=False',doEleTree,doPhoTree,'GT=94X_dataRun2_ReReco17_forValidation']
 
    config.General.requestName  = '17Nov2017_RunB'
    config.Data.inputDataset    = '/SingleElectron/Run2017B-17Nov2017-v1/MINIAOD'
  #  submit(config)    
    config.General.requestName  = '17Nov2017_RunC'
    config.Data.inputDataset    = ''
  #  submit(config)    
    config.General.requestName  = '17Nov2017_RunD'
    config.Data.inputDataset    = '/SingleElectron/Run2017D-17Nov2017-v1/MINIAOD'
   # submit(config)    
    config.General.requestName  = '17Nov2017_RunE'
    config.Data.inputDataset    = '/SingleElectron/Run2017E-17Nov2017-v1/MINIAOD'
 #   submit(config)    
    config.General.requestName  = '17Nov2017_RunF'
    config.Data.inputDataset    = '/SingleElectron/Run2017F-17Nov2017-v1/MINIAOD'
    #submit(config)    





#/SingleElectron/Run2017A-PromptReco-v2/MINIAOD
#/SingleElectron/Run2017A-PromptReco-v3/MINIAOD
#/SingleElectron/Run2017B-PromptReco-v1/MINIAOD
#/SingleElectron/Run2017B-PromptReco-v2/MINIAOD
#/SingleElectron/Run2017C-PromptReco-v1/MINIAOD
#/SingleElectron/Run2017C-PromptReco-v2/MINIAOD
#/SingleElectron/Run2017C-PromptReco-v3/MINIAOD
#/SingleElectron/Run2017D-PromptReco-v1/MINIAOD
#/SingleElectron/Run2017E-PromptReco-v1/MINIAOD



