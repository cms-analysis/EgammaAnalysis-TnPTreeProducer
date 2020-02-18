# EgammaAnalysis-TnPTreeProducer
TnP package for EGM

## For regular users
### 1. Install (CMSSW\_10\_2\_10 or higher, works for 2016, 2017 and 2018 data/MC)

```
cmsrel CMSSW_10_2_10
cd CMSSW_10_2_10/src
cmsenv
git clone -b RunIIfinal https://github.com/tomcornelis/EgammaAnalysis-TnPTreeProducer EgammaAnalysis/TnPTreeProducer
scram b -j8
```

### 2. Try-out 
You can find the cmsRun executable in EgammaAnalysis/TnPTreeProducer/python:
```
cmsRun TnPTreeProducer_cfg.py isMC=True doTrigger=True era=2018
```
Check TnPTreeProducer\_cfg.py for all available options. Update the code if you need to implement custom-made recipes.
Test files can be defined in python/etc/tnpInputTestFiles_cff.py

### 3. Submit jobs
Check in EgammaAnalysis/TnPTreeProducer/scripts/crab for scripts to submit your jobs using crab

## For developpers
1. On github fork the package https://github.com/cms-analysis/EgammaAnalysis-TnPTreeProducer 
2. Add the remote 
```
git remote add username-push git@github.com:username/EgammaAnalysis-TnPTreeProducer.git
```
3. push commits to fork and then standard pull request process
```
git push username-push branchname
```
