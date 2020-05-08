import FWCore.ParameterSet.Config as cms

# Some miniAOD testfiles, which are available now and hopefully don't get deleted too soon
filesMiniAOD_2018 = {
    'mc' :   cms.untracked.vstring('/store/mc/RunIIAutumn18MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/90000/17D5FDFE-C156-FE47-9202-F819E74881D3.root'),
    'data' : cms.untracked.vstring('/store/data/Run2018A/EGamma/MINIAOD/17Sep2018-v2/100000/0004A5E9-9F18-6B42-B31D-4206406CE423.root'),
}

filesMiniAOD_2017 = {
    'mc' :   cms.untracked.vstring('/store/mc/RunIIFall17MiniAODv2/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14_ext3-v1/30000/84A5C6DA-1EDF-E911-B22B-FA163E1A63BB.root'),
    'data' : cms.untracked.vstring('/store/data/Run2017B/SingleElectron/MINIAOD/31Mar2018-v1/90000/021B46D3-C537-E811-9064-008CFAE452E0.root')
}

filesMiniAOD_2016 = {
    'mc' :   cms.untracked.vstring('/store/mc/RunIISummer16MiniAODv3/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1/100000/005FEC6C-D6C2-E811-A83B-A0369FC5E094.root'),
    'data' : cms.untracked.vstring('/store/data/Run2016B/SingleElectron/MINIAOD/17Jul2018_ver2-v1/00000/00293812-4D8C-E811-B7C5-00266CFFC80C.root')
}

# No AOD tests files accessible on lxplus!
