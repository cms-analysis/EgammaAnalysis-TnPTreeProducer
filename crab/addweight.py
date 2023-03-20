import ROOT

fileName = "DYJetsToLL_LHEFilterPtZ-650ToInf_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8.root"
treeName = "tnpEleTrig/fitter_tree"
d = ROOT.RDataFrame(treeName, fileName)
df=d.Define("weight_new", "2")
df.Snapshot("tnpEleTrig/fitter_tree", "newfile.root")
