from CRABClient.UserUtilities import config, getUsernameFromSiteDB
import sys
config = config()

submitVersion = "RECOSFs_2016"

doEleTree = 'doEleID=False'
doPhoTree = 'doPhoID=False'
doHLTTree = 'doTrigger=False'
doRECO    = 'doRECO=True'

mainOutputDir = '/store/group/phys_egamma/tnp/80X/RecoSF/%s' % submitVersion

config.General.transferLogs = False

config.JobType.pluginName  = 'Analysis'

# Name of the CMSSW configuration file
config.JobType.psetName  = 'makeTree.py'
config.Data.allowNonValidInputDataset = False

config.Data.inputDBS = 'global'
config.Data.publication = False

#config.Data.publishDataName = 
config.Site.storageSite = 'T2_CH_CERN'


if __name__ == '__main__':

    from CRABAPI.RawCommand import crabCommand
    from CRABClient.ClientExceptions import ClientException
    from httplib import HTTPException

    # We want to put all the CRAB project directories from the tasks we submit here into one common directory.
    # That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).
    config.General.workArea = 'crab_projects_%s' % submitVersion

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
    config.Data.unitsPerJob   = 20
    config.JobType.pyCfgParams  = ['isMC=True','isAOD=True',doEleTree,doPhoTree,doHLTTree,doRECO]

    
#    config.General.requestName  = 'DYToLL_mcAtNLO'
#    config.Data.inputDataset    = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16DR80-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/AODSIM'
#    submit(config)
#    config.General.requestName  = 'DYToLL_madgraph'
#    config.Data.inputDataset    = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16DR80-PUSpring16_80X_mcRun2_asymptotic_2016_v3_ext1-v1/AODSIM'
#    submit(config)

    config.General.requestName  = 'DYToLL_madgraph_Winter2017'
    config.Data.inputDataset    = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/AODSIM'
    submit(config)

#    config.General.requestName  = 'WJets_madgraph'
#    config.Data.inputDataset    = '/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v2/MINIAODSIM'
#    submit(config)

#    config.General.requestName  = 'ttbar_madgraph'
#    config.Data.inputDataset    = '/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'
#    submit(config)

    ##### now submit DATA
    config.Data.outLFNDirBase = '%s/%s/' % (mainOutputDir,'data')
    config.Data.splitting     = 'LumiBased'
    config.Data.lumiMask      = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/ReReco/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
    config.Data.unitsPerJob   = 100
    config.JobType.pyCfgParams  = ['isMC=False','isAOD=True',doEleTree,doPhoTree,doHLTTree,doRECO,'GT=80X_dataRun2_2016SeptRepro_v4']

    config.General.requestName  = '2016rereco_RunB'
    config.Data.inputDataset    = '/SingleElectron/Run2016B-23Sep2016-v3/AOD'
    submit(config)

    config.General.requestName  = '2016rereco_RunC'
    config.Data.inputDataset    = '/SingleElectron/Run2016C-23Sep2016-v1/AOD'
    submit(config)

    config.General.requestName  = '2016rereco_RunD'
    config.Data.inputDataset    = '/SingleElectron/Run2016D-23Sep2016-v1/AOD'
    submit(config)

    config.General.requestName  = '2016rereco_RunE'
    config.Data.inputDataset    = '/SingleElectron/Run2016E-23Sep2016-v1/AOD'
    submit(config)

    config.General.requestName  = '2016rereco_RunF'
    config.Data.inputDataset    = '/SingleElectron/Run2016F-23Sep2016-v1/AOD'
    submit(config)

    config.General.requestName  = '2016rereco_RunG'
    config.Data.inputDataset    = '/SingleElectron/Run2016G-23Sep2016-v1/AOD'
    submit(config)

    config.General.requestName  = '2016prompt_RunHv1'
    config.Data.inputDataset    = '/SingleElectron/Run2016H-PromptReco-v1/AOD'
    submit(config)

    config.General.requestName  = '2016prompt_RunHv2'
    config.Data.inputDataset    = '/SingleElectron/Run2016H-PromptReco-v2/AOD'
    submit(config)

    config.General.requestName  = '2016prompt_RunHv3'
    config.Data.inputDataset    = '/SingleElectron/Run2016H-PromptReco-v3/AOD'
    submit(config)




    
