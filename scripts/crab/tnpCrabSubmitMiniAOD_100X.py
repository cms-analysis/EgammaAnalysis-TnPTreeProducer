from CRABClient.UserUtilities import config, getUsernameFromSiteDB
import sys

# this will use CRAB client API
from CRABAPI.RawCommand import crabCommand

# talk to DBS to get list of files in this dataset
from dbs.apis.dbsClient import DbsApi
dbs = DbsApi('https://cmsweb.cern.ch/dbs/prod/global/DBSReader')

dataset_amc = '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer18MiniAOD-101X_upgrade2018_realistic_v7-v2/MINIAODSIM'
#'/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISpring18MiniAOD-100X_upgrade2018_realistic_v10-v2/MINIAODSIM'
fileDictList_amc=dbs.listFiles(dataset=dataset_amc)

print ("dataset %s has %d files" % (dataset_amc, len(fileDictList_amc)))

# DBS client returns a list of dictionaries, but we want a list of Logical File Names
lfnList_amc = [ dic['logical_file_name'] for dic in fileDictList_amc ]



dataset_mad = '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer18MiniAOD-FlatPU0to70_101X_upgrade2018_realistic_v7-v2/MINIAODSIM'
#'/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISpring18MiniAOD-100X_upgrade2018_realistic_v10-v2/MINIAODSIM'
fileDictList_mad=dbs.listFiles(dataset=dataset_mad)

print ("dataset %s has %d files" % (dataset_mad, len(fileDictList_mad)))

# DBS client returns a list of dictionaries, but we want a list of Logical File Names
lfnList_mad = [ dic['logical_file_name'] for dic in fileDictList_mad ]

# this now standard CRAB configuration

from WMCore.Configuration import Configuration

config = config()

submitVersion ="2018Data_FullRunBForHEMStudies"
doEleTree = 'doEleID=True'
doPhoTree = 'doPhoID=True'
#doHLTTree = 'doTrigger=False'
#calibEn   = 'useCalibEn=False'

mainOutputDir = '/store/group/phys_egamma/soffi/TnP/ntuples_06152018/%s' % submitVersion

config.General.transferLogs = False

config.JobType.pluginName  = 'Analysis'

# Name of the CMSSW configuration file
config.JobType.psetName  = '/afs/cern.ch/work/s/soffi/EGM-WORK/CMSSW-1011-2018DataTnP/src/EgammaAnalysis/TnPTreeProducer/python/TnPTreeProducer_cfg.py'
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

#    config.Data.splitting     = 'FileBased'
#    config.Data.unitsPerJob   = 10
#    config.Data.inputDataset    = '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISpring18MiniAOD-100X_upgrade2018_realistic_v10-v2/MINIAODSIM'

#    config.Data.outLFNDirBase = '%s/%s/' % (mainOutputDir,'mc')
#    config.JobType.pyCfgParams  = ['isMC=True',doEleTree,doPhoTree,'GT=101X_upgrade2018_realistic_v7']
#    config.Data.userInputFiles = lfnList_amc
#    config.Data.splitting = 'FileBased'
#    config.General.requestName  = 'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8'
#    config.Data.unitsPerJob = 1
#    submit(config)

#    config.Data.outLFNDirBase = '%s/%s/' % (mainOutputDir,'mc')
#    config.JobType.pyCfgParams  = ['isMC=True',doEleTree,doPhoTree,'GT=101X_upgrade2018_realistic_v7'] #100X_upgrade2018_realistic_v10
#    config.Data.userInputFiles = lfnList_mad
#    config.Data.splitting = 'FileBased'
#    config.General.requestName  = 'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8'
#    config.Data.unitsPerJob = 1
#    submit(config)


    ##### now submit DATA
    config.Data.outLFNDirBase = '%s/%s/' % (mainOutputDir,'data')
    config.Data.splitting     = 'LumiBased'
    config.Data.lumiMask      = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/DCSOnly/json_DCSONLY.txt'
    config.Data.unitsPerJob   = 100
    config.JobType.pyCfgParams  = ['isMC=False',doEleTree,doPhoTree,'GT=101X_dataRun2_Prompt_v9']
 
    config.General.requestName  = 'Prompt2018_RunA_v1'
    config.Data.inputDataset    = '/EGamma/Run2018A-PromptReco-v1/MINIAOD'
#    submit(config)    

    config.General.requestName  = 'Prompt2018_RunA_v2'
    config.Data.inputDataset    = '/EGamma/Run2018A-PromptReco-v2/MINIAOD'
#    submit(config)    

    config.General.requestName  = 'Prompt2018_RunA_v3'
    config.Data.inputDataset    = '/EGamma/Run2018A-PromptReco-v3/MINIAOD'
#    submit(config)    

    config.General.requestName  = 'Prompt2018_RunB_v2'
    config.Data.inputDataset    = '/EGamma/Run2018B-PromptReco-v2/MINIAOD'
    submit(config)    
