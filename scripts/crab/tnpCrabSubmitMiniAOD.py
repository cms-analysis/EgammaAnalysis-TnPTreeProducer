from CRABClient.UserUtilities import config, getUsernameFromSiteDB
import sys
config = config()

submitVersion = "Moriond17_GainSwitch_newTnP_v3"
doEleTree = 'doEleID=True'
doPhoTree = 'doPhoID=True'
doHLTTree = 'doTrigger=False'
calibEn   = 'useCalibEn=False'

mainOutputDir = '/store/group/phys_egamma/tnp/80X/PhoEleIDs/%s' % submitVersion

config.General.transferLogs = False

config.JobType.pluginName  = 'Analysis'

# Name of the CMSSW configuration file
config.JobType.psetName  = 'TnPTreeProducer_cfg.py'
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
    config.JobType.pyCfgParams  = ['isMC=True',doEleTree,doPhoTree,doHLTTree,calibEn,'GT=80X_mcRun2_asymptotic_2016_TrancheIV_v6']

    config.General.requestName  = 'ttbar_madgraph'
    config.Data.inputDataset    = '/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'
    submit(config)

 #   sys.exit(0)

    
    config.General.requestName  = 'DYToLL_mcAtNLO'
    config.Data.inputDataset    = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM'
 #   submit(config)


    config.General.requestName  = 'DYToLL_madgraph_Moriond17'
    config.Data.inputDataset    = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/MINIAODSIM'
    submit(config)

    config.General.requestName  = 'WJets_madgraph'
    config.Data.inputDataset    = '/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v2/MINIAODSIM'
#    submit(config)


    config.General.requestName  = 'DYToEE_powheg_m50_120'
    config.Data.inputDataset    = '/ZToEE_NNPDF30_13TeV-powheg_M_50_120/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'
    submit(config)
    
    config.General.requestName  = 'DYToEE_powheg_m120_200'
    config.Data.inputDataset    = '/ZToEE_NNPDF30_13TeV-powheg_M_120_200/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'
    submit(config)
    
    config.General.requestName  = 'DYToEE_powheg_m200_400'
    config.Data.inputDataset    = '/ZToEE_NNPDF30_13TeV-powheg_M_200_400/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'
    submit(config)

    config.General.requestName  = 'DYToEE_powheg_m400_800'
    config.Data.inputDataset    = '/ZToEE_NNPDF30_13TeV-powheg_M_400_800/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'
    submit(config)

    config.General.requestName  = 'DYToEE_powheg_m800_1400'
    config.Data.inputDataset    = '/ZToEE_NNPDF30_13TeV-powheg_M_800_1400/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'
    submit(config)
    
    config.General.requestName  = 'DYToEE_powheg_m1400_2300'
    config.Data.inputDataset    = '/ZToEE_NNPDF30_13TeV-powheg_M_1400_2300/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'
    submit(config)

#    sys.exit(0)

    ##### now submit DATA
    config.Data.outLFNDirBase = '%s/%s/' % (mainOutputDir,'data')
    config.Data.splitting     = 'LumiBased'
    config.Data.lumiMask      = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
    config.Data.unitsPerJob   = 100
    config.JobType.pyCfgParams  = ['isMC=False',doEleTree,doPhoTree,doHLTTree,calibEn,'GT=80X_dataRun2_2016SeptRepro_v7']
 
    config.General.requestName  = '2016rereco_RunB'
    config.Data.inputDataset    = '/SingleElectron/Run2016B-03Feb2017_ver2-v2/MINIAOD'
    submit(config)
    config.General.requestName  = '2016rereco_RunC'
    config.Data.inputDataset    = '/SingleElectron/Run2016C-03Feb2017-v1/MINIAOD'
    submit(config)
    config.General.requestName  = '2016rereco_RunD'
    config.Data.inputDataset    = '/SingleElectron/Run2016D-03Feb2017-v1/MINIAOD'
    submit(config)
    config.General.requestName  = '2016rereco_RunE'
    config.Data.inputDataset    = '/SingleElectron/Run2016E-03Feb2017-v1/MINIAOD'
    submit(config)
    config.General.requestName  = '2016rereco_RunF'
    config.Data.inputDataset    = '/SingleElectron/Run2016F-03Feb2017-v1/MINIAOD'
    submit(config)

    config.JobType.pyCfgParams  = ['isMC=False',doEleTree,doPhoTree,doHLTTree,calibEn,'GT=80X_dataRun2_Prompt_v16']
    config.General.requestName  = '2016rereco_RunG'
    config.Data.inputDataset    = '/SingleElectron/Run2016G-03Feb2017-v1/MINIAOD'
    submit(config)
    config.General.requestName  = '2016prompt_RunHv2'
    config.Data.inputDataset    = '/SingleElectron/Run2016H-03Feb2017_ver2-v1/MINIAOD'
    submit(config)
    config.General.requestName  = '2016prompt_RunHv3'
    config.Data.inputDataset    = '/SingleElectron/Run2016H-03Feb2017_ver3-v1/MINIAOD'
    submit(config)


