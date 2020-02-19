#!/usr/bin/env python
import subprocess, shutil

# System command and retrieval of its output
def system(command):
  return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)

#
# Simply run a test for both data/MC for 2016, 2017 and 2018
#
for era in ['2016', '2017', '2018']:
  system('source $VO_CMS_SW_DIR/cmsset_default.sh;eval `scram runtime -sh`;cmsRun ../python/TnPTreeProducer_cfg.py era=%s maxEvents=1000' % era)
  system('source $VO_CMS_SW_DIR/cmsset_default.sh;eval `scram runtime -sh`;cmsRun ../python/TnPTreeProducer_cfg.py era=%s maxEvents=1000 isMC=True' % era)

  for dataset in ['data', 'mc']:
    shutil.move('TnPTree_%s.root' % dataset, 'TnPTree_%s_%s.root' % (dataset, era))
    for tree in ['tnpEleIDs', 'tnpPhoIDs', 'tnpEleTrig']:
      print era, dataset, tree
      print system('./compareTrees TnPTree_%s_%s.root TnPTree_%s_%s_ref.root' % (dataset, era, dataset, era))
      print '\n\n\n\n\n'
