from CRABClient.UserUtilities import config #, getUsernameFromSiteDB
import sys
config = config()

submitVersion = "ntuple_Run3"

doEleTree = 'doEleID=True'
doPhoTree = 'doPhoID=True'
doHLTTree = 'doTrigger=True'
doRECO    = 'doRECO=False'

mainOutputDir = '/store/group/phys_egamma/ec/swmukher/TnP_Aug17/%s' % submitVersion

config.General.transferLogs = False

config.JobType.pluginName  = 'Analysis'

# Name of the CMSSW configuration file
config.JobType.psetName  = '../python/TnPTreeProducer_cfg.py'
config.Data.allowNonValidInputDataset = True

config.Data.inputDBS = 'global'
config.Data.publication = False

#config.Data.publishDataName = 
config.Site.storageSite = 'T2_CH_CERN'


if __name__ == '__main__':

    from CRABAPI.RawCommand import crabCommand
    from CRABClient.ClientExceptions import ClientException
    from http.client import HTTPException

    # We want to put all the CRAB project directories from the tasks we submit here into one common directory.
    # That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).
    config.General.workArea = 'crab_%s' % submitVersion

    def submit(config):
        try:
            crabCommand('submit', config = config)
        except HTTPException as hte:
            print ("Failed submitting task:" %s) % (hte.headers)
        except ClientException as cle:
            print ("Failed submitting task:" %s) % (cle)


    ##### now submit DATA
    config.Data.outLFNDirBase = '%s/%s/' % (mainOutputDir,'mc')
    config.Data.splitting     = 'FileBased'
    config.Data.unitsPerJob   = 10
    config.JobType.pyCfgParams  = ['isMC=True','isAOD=False',doEleTree,doPhoTree,doHLTTree,doRECO]

    config.General.requestName  = 'DYEE_powheg'
    config.Data.inputDataset    = '/DYToEE_M-50_NNPDF31_TuneCP5_13p6TeV-powheg-pythia8/Run3Winter22MiniAOD-FlatPU0to70_122X_mcRun3_2021_realistic_v9-v2/MINIAODSIM'
    submit(config)

    config.General.requestName  = 'DYLL_madgraph'
    config.Data.inputDataset    = '/DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8/Run3Winter22MiniAOD-FlatPU0to70_122X_mcRun3_2021_realistic_v9_ext1-v2/MINIAODSIM'
    submit(config)




