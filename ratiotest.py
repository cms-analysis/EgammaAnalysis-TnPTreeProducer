import ROOT
from ROOT import TCanvas, TColor, TGaxis, TH1F, TPad
from ROOT import kBlack, kBlue, kRed

fileName1 = ROOT.TFile.Open("TnPTree_mc_80.root","READ")
fileName2 = ROOT.TFile.Open("TnPTree_mc_81.root","READ")
tree1 = fileName1.Get("tnpEleTrig/fitter_tree")
tree2 = fileName2.Get("tnpEleTrig/fitter_tree")
m1= ROOT.TH1D ("2016postVFP_NLO_amc","2016postVFP_NLO_amc",100,0,100)
m2= ROOT.TH1D ("2016postVFP_NLO_ptbinned","2016postVFP_NLO_ptbinned",100,0,100)

for entryNum in range (0,tree1.GetEntries()):
   tree1.GetEntry(entryNum)
   pt = getattr(tree1,"pair_pt")
   weight= getattr(tree1,"totWeight")
   m1.Fill(pt,weight)
for entryNum in range (0,tree2.GetEntries()):
   tree2.GetEntry(entryNum)
   pt = getattr(tree2,"pair_pt")
   weight= getattr(tree2,"totWeight")
   m2.Fill(pt,weight)

def createRatio(h1, h2):
    h3 = h1.Clone("h3")
    h3.SetLineColor(kBlack)
    h3.SetMarkerStyle(21)
    h3.SetTitle("")
    h3.SetMinimum(0.8)
    h3.SetMaximum(1.35)
    # Set up plot for markers and errors
    h3.Sumw2()
    h3.SetStats(0)
    h3.Divide(h2)

    # Adjust y-axis settings
    y = h3.GetYaxis()
    y.SetTitle("ratio h1/h2 ")
    y.SetNdivisions(505)
    y.SetTitleSize(20)
    y.SetTitleFont(43)
    y.SetTitleOffset(1.55)
    y.SetLabelFont(43)
    y.SetLabelSize(15)

    # Adjust x-axis settings
    x = h3.GetXaxis()
    x.SetTitleSize(20)
    x.SetTitleFont(43)
    x.SetTitleOffset(4.0)
    x.SetLabelFont(43)
    x.SetLabelSize(15)

    return h3


def createCanvasPads():
    c = TCanvas("c", "canvas", 800, 800)
    c.cd()
    # Upper histogram plot is pad1
    pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
    pad1.SetBottomMargin(0)  # joins upper and lower plot
    pad1.SetGridx()
    pad1.Draw()
    # Lower ratio plot is pad2
    c.cd()  # returns to main canvas before defining pad2
    pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
    pad2.SetTopMargin(0)  # joins upper and lower plot
    pad2.SetBottomMargin(0.2)
    pad2.SetGridx()
    pad2.Draw()
    c.Modified()
    c.Update()
    return c, pad1, pad2


def ratioplot():
    # create required parts
    h1 = m1
    h2 = m2
    h3 = createRatio(h1, h2)
#    h3=ROOT.TGraphAsymmErrors()
    c, pad1, pad2 = createCanvasPads()

    # draw everything
    pad1.cd()
    h1.Draw()
    h2.Draw("same")
    h2.Scale(h1.Integral()/h2.Integral())
    h1.SetLineColor (kRed)
    h2.SetLineColor (kBlack)
    # to avoid clipping the bottom zero, redraw a small axis
    h1.GetYaxis().SetLabelSize(0.0)
    axis = TGaxis(-5, 20, -5, 220, 20, 220, 510, "")
    axis.SetLabelFont(43)
    axis.SetLabelSize(15)
    axis.Draw()
    pad2.cd()
    h3.Draw("ep")

#if __name__ == "__main__":
ratioplot()
