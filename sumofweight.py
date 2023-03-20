import glob
import ROOT
tot=0
files=open("list.txt","r")
filenames=files.readlines()
files.close()

tc=ROOT.TChain("Runs")
for name in filenames:
#    ifile=glob.glob(name)[0]
#    print(ifile)
    tc.Add(name)
    for iev in tc:
        print(iev.genEventSumw)
        tot+=iev.genEventSumw
print(tot)
