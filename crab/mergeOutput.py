#!/bin/env python
import os, glob, ROOT

submitVersion = "2020-03-03"
mainOutputDir = '/eos/cms/store/group/phys_egamma/tnpTuples/%s/%s' % (os.environ['USER'], submitVersion)


# Check if valid ROOT file exists
def isValidRootFile(fname):
  if not os.path.exists(os.path.expandvars(fname)): return False
  f = ROOT.TFile(fname)
  if not f: return False
  try:
    return not (f.IsZombie() or f.TestBit(ROOT.TFile.kRecovered) or f.GetListOfKeys().IsEmpty())
  finally:
    f.Close()

for eraDir in glob.glob(os.path.join(mainOutputDir, '20*')):
  era = eraDir.split('/')[-1]
  try:    os.makedirs(os.path.join(eraDir, 'merged'))
  except: pass
  print era
  for crabDir in glob.glob(os.path.join(mainOutputDir, era, '*/*/*')):
    targetFile   = os.path.join(eraDir, 'merged', crabDir.split(era + '_')[-1] + '.root')
    filesToMerge = glob.glob(os.path.join(crabDir, '*/*/*.root'))

    if os.path.exists(targetFile): # if existing target file exists and looks ok, skip
      if isValidRootFile(targetFile): continue
      else:                           os.system('rm %s' % targetFile)

    os.system('hadd %s %s' % (targetFile, ' '.join(filesToMerge))) 
