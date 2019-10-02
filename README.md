# EgammaAnalysis-TnPTreeProducer
TnP package for EGM

## For regular users
### 1. Install (for 2018 data/MC in CMSSW\_10\_2\_X)

```
cmsrel CMSSW_10_2_5
cd CMSSW_10_2_5/src
cmsenv
git cms-merge-topic cms-egamma:EgammaID_1023
git clone -b Nm1 https://github.com/swagata87/EgammaAnalysis-TnPTreeProducer EgammaAnalysis/TnPTreeProducer
scram b -j8
```

### 2. Try-out 
You can find the cmsRun executable in EgammaAnalysis/TnPTreeProducer/python:
```
cmsRun TnPTreeProducer_cfg.py isMC=True doTrigger=True 
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
