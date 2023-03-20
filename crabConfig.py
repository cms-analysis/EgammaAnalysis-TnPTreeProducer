from CRABClient.UserUtilities import config
config = config()
CFG = 'sumweight'

# To submit to crab:
# crab submit -c crabConfig_data.py
# To check job status:
# crab status -d <config.General.workArea>/<config.General.requestName># To resubmit jobs:
# crab resubmit -d <config.General.workArea>/<config.General.requestName>

# Local job directory will be created in:
# <config.General.workArea>/<config.General.requestName>
config.General.workArea = 'crab_sumweight'
config.General.requestName = CFG
config.General.transferOutputs = True
config.General.transferLogs = False

# CMS cfg file goes here:
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '/afs/cern.ch/user/r/ryi/CMSSW_10_6_13/src/EgammaAnalysis/TnPTreeProducer/sumofweight.py' # analyzer cfg file
config.JobType.maxMemoryMB = 5000
config.JobType.maxJobRuntimeMin = 100
# Define input and units per job here:
#config.Data.userInputFiles = open('MLAnalyzer/list_production.txt'%idx).readlines()
#config.Data.userInputFiles = open('MLAnalyzer/list_production.txt').readlines()
config.Data.userInputFiles = open('list.txt').readlines()
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 2 # units: as defined by config.Data.splitting
config.Data.totalUnits = -1 # -1: all inputs. total jobs submitted = totalUnits / unitsPerJob. cap of 10k jobs per submission
#config.Data.totalUnits = 10 # test production
config.Data.publication = False

# Output files will be stored in config.Site.storageSite at directory:
# <config.Data.outLFNDirBase>/<config.Data.outputPrimaryDataset>/<config.Data.outputDatasetTag>/
config.Site.storageSite = 'T3_US_FNALLPC'
#config.Site.storageSite = 'T2_CH_CERN'
config.Data.outLFNDirBase = '/store/user/ryi' # add your username as subdirectory
#config.Data.outLFNDirBase = '/store/user/ddicroce/' # add your username as subdirectory
config.Data.outputPrimaryDataset = 'sumofweight'
config.Data.outputDatasetTag = config.General.requestName
