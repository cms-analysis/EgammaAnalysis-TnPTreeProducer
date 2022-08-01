# EgammaAnalysis-TnPTreeProducer

Package of the EGamma group to produce Tag-and-Probe trees

## Overview of branches

| Branch                                     | release            | tnpEleIDs          | tnpPhoIDs          | tnpEleTrig         | tnpEleReco         | purpose                                |
| ------------------------------------------ | ------------------ |:------------------:|:------------------:|:------------------:|:------------------:|:--------------------------------------:|
|                                            |                    | *miniAOD*          | *miniAOD*          | *miniAOD*          | *AOD*              |                                        |
| [RunIIfinal](../../tree/RunIIfinal)        | CMSSW\_10\_2       | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | Run II analysis                        |
| [RunIIfinal](../../tree/RunIIfinal)        | CMSSW\_10\_6       | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | Run II analysis using ultra-legacy     |
| [CMSSW\_11\_X\_Y](../../tree/CMSSW_11_X_Y) | CMSSW\_11          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :white_check_mark: | Development for Run III (experimental) |

Note: because of a dataformat CMSSW\_10\_6 can only be used for ultra-legacy samples, and CMSSW\_10\_2 should be used for the rereco samples.

## Available tuples

### ReReco 2016, 2017 and 2018
If you do not need changes to the default code, you can simply use existing flat tag and probe trees, avalaible for both 2016, 2017 and 2018 (RunIIfinal branch):

```bash
ls /eos/cms/store/group/phys_egamma/tnpTuples/tomc/2020-06-09/*/merged/
```

These inlcude the tnpEleTrig, tnpEleIDs and tnpPhoIDs trees produced with the RunIIfinal branch.
*Main change with respect to the 2020-02-28 production is the inclusion of some additional branches, e.g. the leptonMva's*

### ReReco 2016, 2017 and 2018 - L1 matched
In case you need L1 matching for the measurement of doubleEle HLT triggers, you can use the tnpEleTrig trees found in:

```bash
ls /eos/cms/store/group/phys_egamma/tnpTuples/tomc/2020-03-03/*/merged/*L1matched.root
```

### UL2017 and UL2018
For ultra-legacy  we have tnpEleTrig, tnpEleIDs and tnpPhoIDs trees available at:
```
ls /eos/cms/store/group/phys_egamma/tnpTuples/tomc/2020-05-20/UL2018/merged
ls /eos/cms/store/group/phys_egamma/tnpTuples/tomc/2020-05-20/UL2017/merged
ls /eos/cms/store/group/phys_egamma/tnpTuples/rasharma/2021-02-10/UL2016postVFP/merged
ls /eos/cms/store/group/phys_egamma/tnpTuples/rasharma/2021-02-10/UL2016preVFP/merged
```


## To produce new tuples
### 1a. Install for rereco (CMSSW\_10\_2\_X with X=10 or higher, works for 2016, 2017 and 2018 data/MC)

```bash
cmsrel CMSSW_10_2_22
cd CMSSW_10_2_22/src
cmsenv
git clone -b RunIIfinal git@github.com:cms-egamma/EgammaAnalysis-TnPTreeProducer.git EgammaAnalysis/TnPTreeProducer
scram b -j8
```

### 1b. Install for ultra-legacy (CMSSW\_10\_6\_X, works for UL2017 and UL2018 data/MC)

```bash
cmsrel CMSSW_10_6_13
cd CMSSW_10_6_13/src
cmsenv
git clone -b RunIIfinal git@github.com:cms-egamma/EgammaAnalysis-TnPTreeProducer.git EgammaAnalysis/TnPTreeProducer
scram b -j8
```

### 2. Try-out
You can find the cmsRun executable in EgammaAnalysis/TnPTreeProducer/python:
```bash
cd EgammaAnalysis/TnPTreeProducer/python/
cmsRun TnPTreeProducer_cfg.py isMC=True doTrigger=True era=UL2018
```
Check [TnPTreeProducer\_cfg.py](python/TnPTreeProducer_cfg.py) for all available options. Update the code if you need to implement custom-made recipes.

Test files can be defined in [python/etc/tnpInputTestFiles\_cff.py](python/etc/tnpInputTestFiles_cff.py)
If you update the code, you can use the ./runTests.py script in the test directory to check for new differences in the 2016, 2017 and 2018 test files.

### 3. Submit jobs
Check in EgammaAnalysis/TnPTreeProducer//crab the tnpCrabSubmit.py script to submit your jobs using crab

```bash
source /cvmfs/cms.cern.ch/common/crab-setup.sh
```

## To make a pull request to this repository
1. On github fork the package https://github.com/cms-analysis/EgammaAnalysis-TnPTreeProducer
2. Add the remote
```bash
git remote add username-push git@github.com:username/EgammaAnalysis-TnPTreeProducer.git
```
3. push commits to fork and then standard pull request process
```bash
git push username-push branchname
```

## Adding new workingpoints
You can add new electron workingpoints in [python/egmElectronIDModules\_cff.py](python/egmElectronIDModules_cff.py) and new photon workingpoints
in [python/egmPhotonIDModules\_cff.py](python/egmPhotonIDModules_cff.py). Each new workingpoint added in these python config fragments will
add a new "passing<WP>" boolean in the electron and photon trees respectively. Of course, one can also choose to simply add a variable in
[python/egmTreesContent\_cff.py](python/egmTreesContent\_cff.py), which might be preferred for MVA variables when you want to have the
flexibility to explore different workingpoints: you can simply put a cut on these variable in the egm\_tnp\_analysis package.

## Description of variables

Description of some of variables in the output tree is given [here](VariablesInfo.md).
  
  
  
  
  ## notes from Ruole Yi
  The process of Tag&probe analysis

1. Make tnptree https://github.com/sethcooper/EgammaAnalysis-TnPTreeProducer
* Dataset: https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVRun2LegacyAnalysis NLO sample https://cms-pdmv.cern.ch/grasp/samples?dataset_query=*DYJetsToLL_LHEFilterPtZ*&campaign=RunIISummer20UL16*GEN,RunIISummer20UL16*GENAPV,RunIISummer20UL17*GEN,RunIISummer20UL18*GEN
* Setup tree structure: https://github.com/sethcooper/EgammaAnalysis-TnPTreeProducer/blob/legacyTriggerScaleFactorsLQ/python/TnPTreeProducer_cfg.py
* Use file to submit job to crab: https://github.com/sethcooper/EgammaAnalysis-TnPTreeProducer/blob/legacyTriggerScaleFactorsLQ/crab/tnpCrabSubmit.py
* Submit to crab: crab submit -c tnpCrabSubmit.py
* If wanna kill job: crab kill + path of output file 
* Summit failed job: first check job status then `crab resubmit`
* Check output: login cmslpc check /eos/uscms/store/user/ryi/LQ/TnP/
* Combine crab output:https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3AdvancedTopic#Merging_output_files or use hadd mergedfile.root out_file_*.root (先开启cmssw-cmsenv)
* Cmslpc-eos 的job可以转移到lxplus-afs 的cern box：/eos/user/r/ryi
scp /eos/uscms/store/user/ryi/LQ/TnP/2018UL-DY-LO-ext.root  ryi@lxplus.cern.ch:/eos/user/r/ryi/TagandProbe/TnP2017/


2. Analyse tnptree https://github.com/sethcooper/egm_tnp_analysis 
* Cmsenv first 
* python tnpEGM_fitter.py etc/config/settings_passTrigger.py
* python tnpEGM_fitter.py etc/config/settings_passTrigger.py  --flag passingTrigger --createBins
* python tnpEGM_fitter.py etc/config/settings_passTrigger.py  --flag passingTrigger --checkBins
* python tnpEGM_fitter.py etc/config/settings_passTrigger.py --flag passingTrigger --createHists

nominal fit
python tnpEGM_fitter.py etc/config/settings_passTrigger.py --flag passingTrigger --doFit

MC fit to constrain alternate signal parameters
python tnpEGM_fitter.py etc/config/settings_passTrigger.py --flag passingTrigger --doFit --mcSig  --altSig --addGaus

Alternate signal fit
python tnpEGM_fitter.py etc/config/settings_passTrigger.py --flag passingTrigger --doFit  --altSig --addGaus

Alternate background fit
python tnpEGM_fitter.py etc/config/settings_passTrigger.py --flag passingTrigger --doFit  --altBkg

Check fits and redo failed ones
python tnpEGM_fitter.py etc/config/settings_passTrigger.py --flag passingTrigger --doFit --iBin ib

egm txt ouput file
* python tnpEGM_fitter.py etc/config/settings_passTrigger.py --flag passingTrigger --sumUp
 


