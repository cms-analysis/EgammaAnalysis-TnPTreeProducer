#!/usr/bin/env python

import ROOT, glob, os

#
# System command
#
import subprocess
def system(command):
  return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)


#
# Write mixed output tree based on dyDir, inputTreeDir and fractions
#
def mix(target, inputs, inputTreeDir, fractions):
  assert abs(sum(fractions.values())-1.) < 0.001, 'Fractions do not sum up to 1!'

  inputData = []
  for input in inputs:
    inputFile    = ROOT.TFile(input)
    inputTree    = inputFile.Get('%s/fitter_tree' % inputTreeDir)
    totalEntries = inputTree.GetEntries()
    threshold    = input.split('_leg1Threshold')[-1].split('.root')[0]
    inputData.append((totalEntries, threshold, inputTree, inputFile))

  inputData.sort() # Make sure the one with the least amount of events sits in the back, in this way we minimize the loss of statistics from missing/failed jobs
  totalEntries = inputData[-1][0]

  events = set()
  filesToMerge = ''
  for _,threshold, inputTree,_ in inputData:
    toCopy        = int(totalEntries*fractions[threshold])
    outFile       = ROOT.TFile(target.replace('.root', '_%s.root' % threshold), 'RECREATE')
    filesToMerge += target.replace('.root', '_%s.root' % threshold) + ' '
    outFileDir    = outFile.mkdir(inputTreeDir)
    outFile.cd()
    outFileDir.cd()

    print 'Saving %s entries from %s for threshold %s' % (toCopy, totalEntries, threshold)
    outTree = inputTree.CloneTree(0)
    i, j = 0, 0
    while j < toCopy and i < totalEntries:
      inputTree.GetEntry(i)
      i+=1
      if (inputTree.event, inputTree.el_pt) in events: continue # Check if this event was not yet written (and also the pt because you have sometime two entries for one pair)
      events.add((inputTree.event, inputTree.el_pt))
      j+=1
      outTree.Fill()
      if j%100000==0:
        print 'Event %d written' % j
        outTree.AutoSave()
    outTree.AutoSave()
    outFile.Close()

  print system('hadd -f %s %s;rm %s' % (target, filesToMerge, filesToMerge)) # merge and delete the temporary outfiles

#
# Main script
#
submitVersion='2020-03-03'
allFilesPerThreshold = glob.glob('/eos/cms/store/group/phys_egamma/tnpTuples/*/%s/*/merged/DY*.root' % submitVersion)
allFilesBase         = set(f.split('_leg1Threshold')[0] for f in allFilesPerThreshold)

for base in allFilesBase:
  filesToMix = [f for f in allFilesPerThreshold if (base + '_leg1Threshold') in f]
  target     = base+'_L1matched.root'
  print 'Mixing for %s using\n  %s' % (target, '\n  '.join(filesToMix))

  if   '2016' in base: fractions = {'15': 0.4176, '18': 0.3888, '23': 0.1890, '24': 0.0047}
  elif '2017' in base: fractions = {'18': 0.0018, '22': 0.7959, '24': 0.0870, '25': 0.1153}
  elif '2018' in base: fractions = {'22': 0.9119, '25': 0.0881}

  try:
    mix(target, filesToMix, 'tnpEleTrig', fractions) 
  except Exception as e:
    print(e)
