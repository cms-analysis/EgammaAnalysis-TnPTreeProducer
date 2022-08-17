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
    config.Data.outLFNDirBase = '%s/%s/' % (mainOutputDir,'data')
    config.Data.splitting     = 'LumiBased'
    config.Data.lumiMask      = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions22/Cert_Collisions2022_356309_356615_Golden.json'    
    config.Data.unitsPerJob   = 50
    config.JobType.pyCfgParams  = ['isMC=False','isAOD=False',doEleTree,doPhoTree,doHLTTree,doRECO]

    config.General.requestName  = 'Egamma2022B'
    config.Data.inputDataset    = '/EGamma/Run2022B-PromptReco-v1/MINIAOD' 
    submit(config)

    config.General.requestName  = 'Egamma2022C'
    config.Data.inputDataset    = '/EGamma/Run2022C-PromptReco-v1/MINIAOD' 
    submit(config)




