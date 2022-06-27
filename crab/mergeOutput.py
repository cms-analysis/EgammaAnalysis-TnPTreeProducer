#!/bin/env python
import os, glob, ROOT, subprocess

submitVersion = "2021-02-10"
mainOutputDir = '/eos/cms/store/group/phys_egamma/tnpTuples/%s/%s' % (os.environ['USER'], submitVersion)

print("submitVersion: %s"%submitVersion)
print("mainOutputDir: %s"%mainOutputDir)
def system(command):
    # print "=="*51
    # print "COMMAND: ",command
    return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)

# Check if valid ROOT file exists
def isValidRootFile(fname):
    if not os.path.exists(os.path.expandvars(fname)): return False
    f = ROOT.TFile(fname)
    if not f: return False
    try:
        return not (f.IsZombie() or f.TestBit(ROOT.TFile.kRecovered) or f.GetListOfKeys().IsEmpty())
    finally:
        f.Close()

for eraDir in glob.glob(os.path.join(mainOutputDir, 'UL2016*')):
    era = eraDir.split('/')[-1]
    try:
        os.makedirs(os.path.join(eraDir, 'merged'))
    except:
        pass
    print("era:",era)
    for crabDir in glob.glob(os.path.join(mainOutputDir, era, '*/*/*')):
        print "=="*51
        targetFile   = os.path.join(eraDir, 'merged', crabDir.split(era + '_')[-1] + '.root')
        filesToMerge = glob.glob(os.path.join(crabDir, '*/*/*.root'))
        print "crabDir: ",crabDir
        print "targetFile: ",targetFile
        # print "filesToMerge: ",filesToMerge

        if os.path.exists(targetFile): # if existing target file exists and looks ok, skip
            if isValidRootFile(targetFile):
                print("Seems hadd is already performed.")
                continue
            else:   os.system('rm %s' % targetFile)

        for f in filesToMerge:
            if not isValidRootFile(f):
                print('WARNING: something wrong with %s' % f)

        if len(filesToMerge)>100:
            print('A lof of files to merge, this might take some time...')

            tempTargets = []
            # split the list of all root files into chunk of 100 files
            tempFilesToMerge = [filesToMerge[x:x+100] for x in range(0, len(filesToMerge), 100)]

            # print "tempFilesToMerge:",len(tempFilesToMerge)

            for i in range(0,len(tempFilesToMerge)):
                print "---"
                tempTargetFile = targetFile.replace('.root', '-temp%s.root' % str(i))
                print("tempTargetFile: %s"%tempTargetFile)
                tempTargets.append(tempTargetFile)
                if os.path.exists(tempTargetFile): # if existing target file exists and looks ok, skip
                    if isValidRootFile(tempTargetFile): continue
                    else:
                        print("Removing temp hadd file {}".format(tempTargetFile))
                        os.system('rm %s' % tempTargetFile)
                # tempFilesToMerge = [f for f in filesToMerge if ('%s.root' % str(i)) in f]
                print(system('hadd %s %s' % (tempTargetFile, ' '.join(tempFilesToMerge[i]))))
            print(system('hadd %s %s' % (targetFile, ' '.join(tempTargets))))
            for i in tempTargets:
                system('rm %s' % i)
        else:
            print(system('hadd %s %s' % (targetFile, ' '.join(filesToMerge))))
