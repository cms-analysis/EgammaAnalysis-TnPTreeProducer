#!/usr/bin/env python
import subprocess

# System command and retrieval of its output
def system(command):
  return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)

#
# Simply run a test for both data/MC for 2016, 2017 and 2018
#
for era in ['2016', '2017', '2018']:
  system('eval `scram runtime -sh`;cmsRun ../python/TnPTreeProducer_cfg.py doTrigger=True era=%s maxEvents=1000' % era)
  system('eval `scram runtime -sh`;cmsRun ../python/TnPTreeProducer_cfg.py doTrigger=True era=%s maxEvents=1000 isMC=True' % era)
  system('mv TnPTree_data.root TnPTree_data_%s.root' % era)
  system('mv TnPTree_mc.root TnPTree_mc_%s.root' % era)

#
# TODO: then use compareTrees script for quality check
#
