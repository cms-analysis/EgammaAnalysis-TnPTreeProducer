from CRABClient.UserUtilities import config, getUsernameFromSiteDB
import sys
config = config()

submitVersion = "Moriond17_v1"
doEleTree = 'doEleID=True'
doPhoTree = 'doPhoID=True'
doHLTTree = 'doTrigger=False'
calibEn   = 'useCalibEn=False'

mainOutputDir = '/store/group/phys_egamma/tnp/80X/PhoEleIDs/%s' % submitVersion

config.General.transferLogs = False

config.JobType.pluginName  = 'Analysis'

# Name of the CMSSW configuration file
config.JobType.psetName  = 'makeTree.py'
config.Data.allowNonValidInputDataset = False
config.JobType.sendExternalFolder     = True

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
    config.General.workArea = 'crab_project_%s' % submitVersion

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
    config.JobType.pyCfgParams  = ['isMC=True',doEleTree,doPhoTree,doHLTTree,calibEn,'HLTname=HLT2','GT=80X_mcRun2_asymptotic_2016_miniAODv2_v1']

    
    config.General.requestName  = 'DYToLL_mcAtNLO'
    config.Data.inputDataset    = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM'
 #   submit(config)

    config.General.requestName  = 'DYToLL_madgraph_Spring16_reHLT'
#    config.Data.inputDataset    = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM'
    config.Data.inputDataset    = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext1-v1/MINIAODSIM'
    submit(config)

    config.General.requestName  = 'WJets_madgraph'
    config.Data.inputDataset    = '/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v2/MINIAODSIM'
#    submit(config)


 #   config.General.requestName  = 'ttbar_madgraph'
 #   config.Data.inputDataset    = '/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'
 #   submit(config)

    sys.exit(0)

    ##### now submit DATA
    config.Data.outLFNDirBase = '%s/%s/' % (mainOutputDir,'data')
    config.Data.splitting     = 'LumiBased'
    config.Data.lumiMask      = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
    config.Data.unitsPerJob   = 100
    config.JobType.pyCfgParams  = ['isMC=False',doEleTree,doPhoTree,doHLTTree,calibEn,'GT=80X_dataRun2_2016SeptRepro_v4']
 
    config.General.requestName  = '2016rereco_RunB'
    config.Data.inputDataset    = '/SingleElectron/Run2016B-23Sep2016-v3/MINIAOD'
    submit(config)
    config.General.requestName  = '2016rereco_RunC'
    config.Data.inputDataset    = '/SingleElectron/Run2016C-23Sep2016-v1/MINIAOD'
    submit(config)
    config.General.requestName  = '2016rereco_RunD'
    config.Data.inputDataset    = '/SingleElectron/Run2016D-23Sep2016-v1/MINIAOD'
    submit(config)
    config.General.requestName  = '2016rereco_RunE'
    config.Data.inputDataset    = '/SingleElectron/Run2016E-23Sep2016-v1/MINIAOD'
    submit(config)
    config.General.requestName  = '2016rereco_RunF'
    config.Data.inputDataset    = '/SingleElectron/Run2016F-23Sep2016-v1/MINIAOD'
    submit(config)
    config.General.requestName  = '2016rereco_RunG'
    config.Data.inputDataset    = '/SingleElectron/Run2016G-23Sep2016-v1/MINIAOD'
    submit(config)
    config.General.requestName  = '2016prompt_RunHv1'
    config.Data.inputDataset    = '/SingleElectron/Run2016H-PromptReco-v1/MINIAOD'
    submit(config)
    config.General.requestName  = '2016prompt_RunHv2'
    config.Data.inputDataset    = '/SingleElectron/Run2016H-PromptReco-v2/MINIAOD'
    submit(config)
    config.General.requestName  = '2016prompt_RunHv3'
    config.Data.inputDataset    = '/SingleElectron/Run2016H-PromptReco-v3/MINIAOD'
    submit(config)


