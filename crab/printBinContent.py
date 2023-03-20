import ROOT

fileName1 = ROOT.TFile.Open("/eos/user/r/ryi/TagandProbe/TnP2016post/2016post-NLO_amc_allrange.root","READ")
tree1 = fileName1.Get("evtCounter/h_sumW")
#tree1 = fileName1.Get("tnpEleTrig/fitter_tree/pair_pt")
binContent = tree1.GetBinContent(tree1.FindBin(0.5));
print(binContent)
fileName1.Close()
