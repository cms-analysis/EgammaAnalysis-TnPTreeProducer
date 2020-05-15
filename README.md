# EgammaAnalysis-TnPTreeProducer
TnP package for EGM

## Overview of branches

| Branch                                     | release            | tnpEleIDs          | tnpPhoIDs          | tnpEleTrig         | tnpEleReco         |
| ------------------------------------------ | ------------------ |:------------------:|:------------------:|:------------------:|:------------------:|
|                                            |                    | *miniAOD*          | *miniAOD*          | *miniAOD*          | *AOD*              |
| [RunIIfinal](../../tree/RunIIfinal)        | CMSSW\_10\_2       | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| [RunIIfinal\_UL](../../tree/RunIIfinal_UL) | CMSSW\_10\_6       | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| [CMSSW\_11\_X\_Y](../../tree/CMSSW_11_X_Y) | CMSSW\_11          | :heavy_check_mark: | :white_check_mark: | :heavy_check_mark: | :white_check_mark: |

Note: do not use the RunIIfinal\_UL/CMSSW\_10\_6 branch on other samples than ultra-legacy, because of a dataformat chance CMSSW\_10\_6 can only be used for ultra-legacy.

## Available trees 

If you do not need changes to the default code, you can simply use existing flat tag and probe trees, avalaible for both 2016, 2017 and 2018 (RunIIfinal branch):
```
ls /eos/cms/store/group/phys_egamma/tnpTuples/tomc/2020-02-28/*/merged/ 
``` 
These inlcude the tnpEleTrig, tnpEleIDs and tnpPhoIDs trees.
In case you need L1 matching for the measurement of doubleEle HLT triggers, you can use the tnpEleTrig trees found in:
```
ls /eos/cms/store/group/phys_egamma/tnpTuples/tomc/2020-03-03/*/merged/*L1matched.root 
```

## To produce new tuples
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
Check [TnPTreeProducer\_cfg.py](python/TnPTreeProducer_cfg.py) for all available options. Update the code if you need to implement custom-made recipes.

Test files can be defined in [python/etc/tnpInputTestFiles\_cff.py](python/etc/tnpInputTestFiles_cff.py)
If you update the code, you can use the ./runTests.py script in the test directory to check for new differences in the 2016, 2017 and 2018 test files.

### 3. Submit jobs
Check in EgammaAnalysis/TnPTreeProducer//crab the tnpCrabSubmit.py script to submit your jobs using crab

## To make a pull request to this repository
1. On github fork the package https://github.com/cms-analysis/EgammaAnalysis-TnPTreeProducer 
2. Add the remote 
```
git remote add username-push git@github.com:username/EgammaAnalysis-TnPTreeProducer.git
```
3. push commits to fork and then standard pull request process
```
git push username-push branchname
```

## Adding new workingpoints
You can add new electron workingpoints in [python/egmElectronIDModules\_cff.py](python/egmElectronIDModules_cff.py) and new photon workingpoints
in [python/egmPhotonIDModules\_cff.py](python/egmPhotonIDModules_cff.py). Each new workingpoint added in these python config fragments will
add a new "passing<WP>" boolean in the electron and photon trees respectively. Of course, one can also choose to simply add a variable in
[python/egmTreesContent\_cff.py](python/egmTreesContent\_cff.py), which might be preferred for MVA variables when you want to have the
flexibility to explore different workingpoints: you can simply put a cut on these variable in the egm\_tnp\_analysis package.
