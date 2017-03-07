from CRABClient.UserUtilities import config
from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException


import argparse
import pickle
import sys,os,subprocess
import string


### Fabrice Couderc: script in development to hadd jobs and create datasetdefinion
### one arg = crab project area
### eos dir should be mounted first in current directory: use  eosmount eos

### log
#       13 July 2016 : first commit
#                      no protection, you should know what you are doing
#                      only work on eos
#                      campaign is named after crab project area (to be improved)




parser = argparse.ArgumentParser(description='tnp check crab jobs')
parser.add_argument('-s', action='store_false', help = 'deactivate crab status')
parser.add_argument('-r', action='store_false', help = 'deactivate crab report')
parser.add_argument('--hadd'   , action = 'store_true' , help = 'create output tree')
parser.add_argument('--addAll' , action = 'store_true' , help = 'hadd file in any status (default false: only finished)')
parser.add_argument('crabDir'  , default = None        , help = 'crabDir')
parser.add_argument('--dry_run', action='store_true'   , help = 'do not hadd, just test')

args = parser.parse_args()
print args
if args.crabDir is None :
    print 'Need to specify a crabDirectory as argument'
    sys.exit(0)


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def file_size_kb(file_path):
    """
    this function will return the file size in KB
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return file_info.st_size/1024.0


dirToCheck = args.crabDir + "/"

inputTnPCrab = pickle.load(open(dirToCheck+'.requestcache','rb'))

config = None
if inputTnPCrab.has_key('OriginalConfig'):
    config = inputTnPCrab['OriginalConfig'] 

print config


### mount eos directory
#print os.environ
#subprocess.call(['bash','-i','-c','eosumount eos'])
#subprocess.call(['bash','-i','-c','eosmount eos'])
#os.rmdir('eos')
#os.mkdir('eos')

dasDataset = string.split(config.Data.inputDataset,'/')[1]
crabName   = 'crab_' + config.General.requestName


proc = subprocess.Popen('ls eos/cms/%s/%s/%s/*/*/*root'%(config.Data.outLFNDirBase,dasDataset,crabName), shell=True, 
                        stdout=subprocess.PIPE)
out,err = proc.communicate()
filelistTmp = string.split(out,'\n')
#print filelist

filelist = {}
for f in filelistTmp:
    if len(f) > 0:
        jobIdTmp = string.split(f,'_')
        jobId = int(jobIdTmp[len(jobIdTmp)-1].split('.root')[0])
        filelist[jobId] = f


###################################################################
##############  Check STATUS
###################################################################
statusOut   = None

if args.s:
    try:
        statusOut = crabCommand('status', dir = dirToCheck )
    except:
        print "Crab command status failed ... "
        sys.exit(1)

jobStatus = {}
if statusOut != None:
    for job in statusOut['jobs']:
        jobId = int(job)
        state = statusOut['jobs'][job]['State']
        jobStatus[jobId] = state
    
filelistsDone    = { 'running' : [] , 'finished': [] , 'transferring': [], 'other' : [], 'failed' : [] }
filelistsMissing = { 'running' : [] , 'finished': [] , 'transferring': [], 'other' : [], 'failed' : [] }

for jobId in filelist.keys():
    if jobId in jobStatus.keys():
        ## ensure file is not in transfer (size (kB) > 0.1 )
        if file_size_kb(filelist[jobId]) < 0.1 : continue
        if   jobStatus[jobId] == 'finished':
            filelistsDone['finished'].append( filelist[jobId] )
        elif jobStatus[jobId] == 'transferring':
            filelistsDone['transferring'].append( filelist[jobId] )
        elif jobStatus[jobId] == 'running'     :
            filelistsDone['running'].append( filelist[jobId] )
        elif jobStatus[jobId] == 'failed'     :
            filelistsDone['failed'].append( filelist[jobId] )
        else:
            filelistsDone['other'].append( filelist[jobId] )
            print '==> Job: %d in state (not finished): %s but file is already transferred' % (jobId,jobStatus[jobId])
    else:
        print '==> SEVERE WARNING: jobId %d does not exist !' % jobId

for jobId in jobStatus.keys():
    if not jobId in filelist.keys():
        if   jobStatus[jobId] == 'finished':
            filelistsMissing['finished'].append(jobId)
        elif jobStatus[jobId] == 'transferring':
            filelistsMissing['transferring'].append(jobId)
        elif jobStatus[jobId] == 'running':
            filelistsMissing['running'].append(jobId)
        elif jobStatus[jobId] == 'failed':
            filelistsMissing['failed'].append(jobId)
        else:
            filelistsMissing['other'].append(jobId)

nOnDisk  = len( filelistsDone['finished']) + len(filelistsDone['transferring'] ) + len(filelistsDone['running']) + len(filelistsDone['other']) + len(filelistsDone['failed'])
nMissing = len( filelistsMissing['finished']) + len(filelistsMissing['transferring'] ) + len(filelistsMissing['running']) + len(filelistsMissing['other']) + len(filelistsMissing['failed'])

print '============== crab summary for job: %s ===============' % config.General.requestName
print 'On disk : %4d/%4d (%2.1f%%)' % (nOnDisk,len(jobStatus.keys() ),float(nOnDisk)/len(jobStatus.keys() )*100)
if len(filelistsDone['finished']) > 0    : print ' - crab state finished: ', len(filelistsDone['finished'])
if len(filelistsDone['transferring']) >0 : print ' - crab state transfer: ', len(filelistsDone['transferring'])
if len(filelistsDone['running'])     >0  : print ' - crab state running : ', len(filelistsDone['running'])
if len(filelistsDone['failed'])      >0  : print ' - crab state failed  : ', len(filelistsDone['failed'])
if len(filelistsDone['other']) > 0       : print ' - crab state ??      : ', len(filelistsDone['other'])

print 'Missing : %4d/%4d (%2.1f%%)' % (nMissing,len(jobStatus.keys() ),float(nMissing)/len(jobStatus.keys() )*100)
if len(filelistsMissing['finished']) > 0    : print ' - crab state finished: ', len(filelistsMissing['finished'])
if len(filelistsMissing['transferring']) >0 : print ' - crab state transfer: ', len(filelistsMissing['transferring'])
if len(filelistsMissing['running'])     >0  : print ' - crab state running : ', len(filelistsMissing['running'])
if len(filelistsMissing['failed'])      >0  : print ' - crab state failed  : ', len(filelistsMissing['failed'])
if len(filelistsMissing['other']) > 0       : print ' - crab state ??      : ', len(filelistsMissing['other'])

if len(filelistsMissing['finished']) > 0: print ' Need to resubmit following jobs:'
for jobId in filelistsMissing['finished']:
    print jobId
    

###################################################################
##############  Check REPORT
###################################################################
reportOut = None
nEvtsRead = -1
lumiProccessedFile = None
if args.r:
    try:
        reportOut = crabCommand('report', dir = dirToCheck )
#        print reportOut
        nEvtsRead          = reportOut['numEventsRead']
        lumiProccessedFile = '%s/%s/%s' % (os.getcwd(),dirToCheck,'results/processedLumis.json')
    except:
        print "Crab command report failed ... "
        
    

###################################################################
##############  hAdd
###################################################################
if not args.hadd: sys.exit(0)

outDir  = dirToCheck 
outFile = '%s/TnPTree_%s_%s.root' % (outDir,dasDataset,config.General.requestName)
print 'hadd will be saved to %s ' % outFile
print ' - if file is moved properly to eos one should remove it (not automated for now)'

dataset = {}
dataset['campaign'] = config.General.workArea
dataset['dataset']  = '%s_%s' % ( dasDataset, config.General.requestName )
dataset['file' ]    = '%s/%s' % (config.Data.outLFNDirBase,os.path.basename(outFile))
dataset['nEvts']    = nEvtsRead
dataset['lumiProcessedFile' ]  = lumiProccessedFile
dataset['lumi' ]    = -1
print dataset

filelistTohAdd  = filelistsDone['finished']
if args.addAll:
    filelistTohAdd += filelistsDone['transferring']
    filelistTohAdd += filelistsDone['running']
    filelistTohAdd += filelistsDone['failed']
    filelistTohAdd += filelistsDone['other']

print 'Hadding %d files ' % len(filelistTohAdd)

if args.dry_run:
    sys.exit(0)

haddCommand = ['hadd','-f',outFile]
haddCommand += filelistTohAdd

subprocess.call(haddCommand)
subprocess.call(['mv',outFile,'eos/cms/%s'%config.Data.outLFNDirBase])

