# EgammaAnalysis-TnPTreeProducer

Package of the EGamma group to produce Tag-and-Probe trees. The repository has been updated to be thread safe for the CMSSW_13X releases.
```
cmsrel CMSSW_13_1_0

cd CMSSW_13_1_0/src

cmsenv

git clone -b Run3_2022_v1  git@github.com:swagata87/EgammaAnalysis-TnPTreeProducer.git EgammaAnalysis/TnPTreeProducer

scram b

cd EgammaAnalysis/TnPTreeProducer/python/

voms-proxy-init -voms cms

cmsRun TnPTreeProducer_cfg.py isMC=False doEleID=True era=2022
```
