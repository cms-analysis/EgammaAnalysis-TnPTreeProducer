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

from EgammaAnalysis.TnPTreeProducer.cmssw_version import isReleaseAbove
if isReleaseAbove(10, 6): erasToTest = ['UL2017', 'UL2018']
else:                     erasToTest = ['2016', '2017', '2018']


#
# Simply run a test for both data/MC for 2016, 2017 and 2018
#
for isAOD in [True, False]:
  if isAOD: treesToRun = ['tnpEleReco']
  else:     treesToRun = ['tnpEleIDs', 'tnpPhoIDs', 'tnpEleTrig']

  for isMC in [False, True]:
    for era in erasToTest:
      if isAOD and not 'UL' in era: continue # don't have specified AOD test files yet for rereco

      options  = ['era=%s' % era, 'maxEvents=1000']
      options += ['isAOD=True', 'doRECO=True', 'doEleID=False', 'doPhoID=False', 'doTrigger=False'] if isAOD else ['doRECO=False', 'doEleID=True', 'doPhoID=True', 'doTrigger=True']
      options += ['isMC=True'] if isMC else []
      system('source /cvmfs/cms.cern.ch/cmsset_default.sh;eval `scram runtime -sh`;cmsRun ../python/TnPTreeProducer_cfg.py %s' % ' '.join(options))

      outFile = 'rootfiles/TnPTree_%s_%s_%s.root' % ('mc' if isMC else 'data', era, 'AOD' if isAOD else 'miniAOD')
      shutil.move('TnPTree_%s.root' % ('mc' if isMC else 'data'), outFile)

      for tree in treesToRun:

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
