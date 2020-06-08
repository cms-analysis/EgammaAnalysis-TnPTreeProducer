import FWCore.ParameterSet.Config as cms

# Some miniAOD testfiles, about 1000 events copied to our eos storage
# (not running directly on datasets because they get moved around all the time and xrootd sucks)
filesMiniAOD_2018 = {
    'mc' :   cms.untracked.vstring('file:/eos/cms/store/group/phys_egamma/tnpTuples/testFiles/RunIIAutumn18MiniAOD-DYJetsToLL_M-50.root'),
    'data' : cms.untracked.vstring('file:/eos/cms/store/group/phys_egamma/tnpTuples/testFiles/Egamma-Run2018A-17Sep2018-v2.root'),
}

filesMiniAOD_2017 = {
    'mc' :   cms.untracked.vstring('file:/eos/cms/store/group/phys_egamma/tnpTuples/testFiles/RunIIFall17MiniAODv2-DYJetsToLL_M-50.root'),
    'data' : cms.untracked.vstring('file:/eos/cms/store/group/phys_egamma/tnpTuples/testFiles/SingleElectron-Run2017B-31Mar2018-v1.root'),
}

filesMiniAOD_2016 = {
    'mc' :   cms.untracked.vstring('file:/eos/cms/store/group/phys_egamma/tnpTuples/testFiles/RunIISummer16MiniAODv3-DYJetsToLL_M-50.root'),
    'data' : cms.untracked.vstring('file:/eos/cms/store/group/phys_egamma/tnpTuples/testFiles/SingleElectron-Run2016B-17Jul2018_ver2-v1.root'),
}


# Some miniAOD UL testfiles, which are available now and hopefully don't get deleted too soon
filesMiniAOD_UL2018 = {
    'mc' :   cms.untracked.vstring('/store/mc/RunIISummer19UL18MiniAOD/DYJetsToEE_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/NoPUECALGT1_106X_upgrade2018_realistic_v11_L1v1-v3/50000/0DC236F0-792D-4749-A920-00B3DBE98BF0.root'),
    'data' : cms.untracked.vstring('/store/data/Run2018D/EGamma/MINIAOD/12Nov2019_UL2018-v1/40000/1769B854-08A2-D441-B7B2-1D1646BBF99A.root'),
}

filesMiniAOD_UL2017 = {
    'mc' :   cms.untracked.vstring('/store/mc/RunIISummer19UL17MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/100001/454B5511-3427-834C-A598-AA42475EFC94.root'),
    'data' : cms.untracked.vstring('/store/data/Run2017F/SingleElectron/MINIAOD/09Aug2019_UL2017_rsb-v2/00000/D6FA4039-620B-C74E-B9E3-CC9BBA38A929.root'),
}


# AOD UL testfiles
filesAOD_UL2018 = {
    'mc' :   cms.untracked.vstring('/store/mc/RunIISummer19UL18RECO/DYToEE_M-50_NNPDF31_TuneCP5_13TeV-powheg-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/230000/8175F4B2-8FB9-AD4D-B7C1-72C0033DFF6E.root'),
    'data' : cms.untracked.vstring('/store/data/Run2018D/EGamma/AOD/12Nov2019_UL2018-v1/250000/565E438F-8B09-B146-817F-0DCF66881720.root'),
}

filesAOD_UL2017 = {
    'mc' :   cms.untracked.vstring('/store/mc/RunIISummer19UL17RECO/DYToEE_M-50_NNPDF31_TuneCP5_13TeV-powheg-pythia8/AODSIM/106X_mc2017_realistic_v6-v1/240000/E407D16F-B626-D249-AA8F-678605042AB9.root'),
    'data' : cms.untracked.vstring('/store/data/Run2017F/SingleElectron/AOD/09Aug2019_UL2017_rsb-v2/110000/20034F69-8143-8946-8F26-17954FEFDFF7.root'),
}
