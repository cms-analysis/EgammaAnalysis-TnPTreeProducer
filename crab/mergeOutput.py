#!/bin/env python
import os, glob

submitVersion = "2020-03-03"
mainOutputDir = '/eos/cms/store/group/phys_egamma/tnpTuples/%s/%s' % (os.environ['USER'], submitVersion)

for eraDir in glob.glob(os.path.join(mainOutputDir, '20*')):
  era = eraDir.split('/')[-1]
  try:    os.makedirs(os.path.join(eraDir, 'merged'))
  except: pass
  print era
  for crabDir in glob.glob(os.path.join(mainOutputDir, era, '*/*/*')):
    targetFile   = os.path.join(eraDir, 'merged', crabDir.split(era + '_')[-1] + '.root')
    filesToMerge = glob.glob(os.path.join(crabDir, '*/*/*.root'))
    os.system('hadd %s %s' % (targetFile, ' '.join(filesToMerge))) 
