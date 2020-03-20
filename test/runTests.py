#!/usr/bin/env python
import subprocess, shutil

# System command and retrieval of its output
def system(command):
  try:
    return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
  except subprocess.CalledProcessError as e:
    print e.output

#
# Simply run a test for both data/MC for 2016, 2017 and 2018
#
for era in ['2016', '2017', '2018']:
  system('source /cvmfs/cms.cern.ch/cmsset_default.sh;eval `scram runtime -sh`;cmsRun ../python/TnPTreeProducer_cfg.py era=%s maxEvents=1000 L1Threshold=5' % era)
  system('source /cvmfs/cms.cern.ch/cmsset_default.sh;eval `scram runtime -sh`;cmsRun ../python/TnPTreeProducer_cfg.py era=%s maxEvents=1000 isMC=True L1Threshold=5' % era)

  for dataset in ['data', 'mc']:
    shutil.move('TnPTree_%s.root' % dataset, 'TnPTree_%s_%s.root' % (dataset, era))
    for tree in ['tnpEleIDs', 'tnpPhoIDs', 'tnpEleTrig']:
      print era, dataset, tree
      print system('./compareTrees TnPTree_%s_%s.root TnPTree_%s_%s_ref.root -s -d %s' % (dataset, era, dataset, era, tree))
      print '\n\n\n\n\n'
