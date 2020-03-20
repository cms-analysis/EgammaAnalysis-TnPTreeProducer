# EgammaAnalysis-TnPTreeProducer
TnP package for EGM

If you do not need changes to the default code, you can simply use existing flat tag and probe trees, avalaible for both 2016, 2017 and 2018:
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

# Note about leptonMva
Some leptonMva variables are now included in the TnPTreeProducer trees. Unfortunately, it is very easy to get out of sync for these variables:
even a new global tag could slightly alter the input variables, given some of them are dependent on the jet energy corrections or b-taggers which
were in use when training these leptonMva's. Additionaly, some leptonMva's use (extremely) old effective areas for miniIso or relIso variables.
We therefore strongly recommend leptonMva analyzers to sync with their own analysis code before producing tuples.
The sync can easily be done by setting the debug flag to True in [python/leptonMva\_cff.py](python/leptonMva_cff.py). The leptonMva xml files
are found in [data](data), and implementation of a new leptonMvaType can happen in the produce function in
[plugins/LeptonMvaProducer.cc](plugins/LeptonMvaProducer.cc).
