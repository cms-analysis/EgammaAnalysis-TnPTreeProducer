# EgammaAnalysis-TnPTreeProducer

Package of the EGamma group to produce Tag-and-Probe trees


cmsrel CMSSW_12_3_6
cd CMSSW_12_3_6/src
cmsenv
git clone -b Run3_2022_v1  git@github.com:swagata87/EgammaAnalysis-TnPTreeProducer.git EgammaAnalysis/TnPTreeProducer
scram b
cd EgammaAnalysis/TnPTreeProducer/python/
voms-proxy-init -voms cms
cmsRun TnPTreeProducer_cfg.py isMC=False doEleID=True era=2022
