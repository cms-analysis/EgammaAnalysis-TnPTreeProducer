#!/usr/bin/env python
import subprocess, shutil, os

if not 'CMSSW_BASE' in os.environ or os.environ['CMSSW_BASE'].replace('/storage_mnt/storage','') not in os.getcwd():
  print('\033[1m\033[91mPlease do cmsenv first!')
  exit(0)

try:    os.makedirs('log')
except: pass

# System command and retrieval of its output
def system(command):
  try:
    return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
  except subprocess.CalledProcessError as e:
    print e.output

#
# Simply run a test for both data/MC for 2016, 2017 and 2018
#
for isAOD in [False]:
  for isMC in [False, True]:
    for era in ['2016', '2017', '2018']:

      options  = ['doRECO=True', 'era=%s maxEvents=1000' % era]
      options += ['isAOD=True'] if isAOD else []
      options += ['isMC=True'] if isMC else []
      system('source /cvmfs/cms.cern.ch/cmsset_default.sh;eval `scram runtime -sh`;cmsRun ../python/TnPTreeProducer_cfg.py %s' % ' '.join(options))

      outFile = 'rootfiles/TnPTree_%s_%s_%s.root' % ('mc' if isMC else 'data', era, 'AOD' if isAOD else 'miniAOD')
      shutil.move('TnPTree_%s.root' % ('mc' if isMC else 'data'), outFile)

      for tree in ['tnpEleIDs', 'tnpPhoIDs', 'tnpEleTrig', 'tnpEleReco']:
	report = 'log/report_%s_%s_%s_%s.log' % ('mc' if isMC else 'data', era, 'AOD' if isAOD else 'miniAOD', tree)

	print ('Testing for options %s and tree %s...' % (' '.join(options), tree)),
	system('./compareTrees %s %s -s -d %s &> %s' % (outFile, outFile.replace('.root', '_ref.root'), tree, report))
	print ' report saved in %s' % report

	with open(report) as f:
	  scanSection=True
	  section=[]
	  for line in f.readlines():
	    if 'Branches' in line: 
	      scanSection=False
	      if any(['Entries' in line and not 'Entries: 0' in line for line in section]):
		for line in section:
		  print line,
	      section=[]
	    if 'Branches which differ' in line or 'Branches found' in line: 
	      scanSection=True
	    if scanSection:
	      section.append(line)
	print '\n\n\n'
