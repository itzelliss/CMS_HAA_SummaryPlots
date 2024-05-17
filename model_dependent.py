import argparse
import os
import numpy as np
from array import array
import ROOT

def add_lumi():
    lowX=0.685
    lowY=0.855
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.30, lowY+0.16, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextFont(42)
    lumi.SetTextSize(0.04)
    lumi.AddText("35.9 fb^{-1} (13 TeV)")
    return lumi

def add_lumi_runI():
    lowX=0.685
    lowY=0.855
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.30, lowY+0.16, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextFont(42)
    lumi.SetTextSize(0.04)
    lumi.AddText("19.7 fb^{-1} (8 TeV)")
    return lumi

def add_CMS():
    lowX=0.13
    lowY=0.865
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextFont(61)
    lumi.SetTextSize(0.06)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("CMS")
    return lumi 

def add_Preliminary():
    lowX=0.25
    lowY=0.86
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextSize(0.045)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextFont(52)
    lumi.AddText("Preliminary")
    return lumi 



#import array of tanBeta
tan_beta = np.loadtxt('tan_beta.txt', unpack=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=int, default=1, help="Which type of 2HDM?")
    parser.add_argument('--run', type=int, default=2, help="Which run?")
    args = parser.parse_args()

    brs = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0]

    typestring = {1: 'I', 2: 'II', 3: 'III', 4: 'IV'}.get(args.model, '')

    arrays = {}
    for br in brs:
        myfile = "BR/BR_I.dat" if args.model == 1 else f"BR/BR_{typestring}_{br:.1f}.dat"
        array_type, array_mass, array_tanbeta, array_BRbb, array_BRcc, array_BRtt, array_BRmm, array_BRgg, array_BRpp, array_BRusd, array_BRhad = np.loadtxt(myfile, unpack=True)
        arrays[br] = {
            'mass': array("d", array_mass),
            'mm': array("d", array_BRmm),
            'tt': array("d", array_BRtt),
            'bb': array("d", array_BRbb),
        }

    x_mmtt_boosted_obs, y_mmtt_boosted_obs = np.loadtxt('mmtt_boosted_obs.txt', unpack=True)
    x_mmtt_boosted_exp, y_mmtt_boosted_exp = np.loadtxt('mmtt_boosted_exp.txt', unpack=True)

    z_obs = []
    z_exp = []

    for br in brs:
        for i, x_obs in enumerate(x_mmtt_boosted_obs):
            BRmm = 1.0
            BRtt = 1.0
            for j, mass in enumerate(arrays[br]["mass"]):
                if mass < x_obs:
                    BRmm = arrays[br]["mm"][j]
                    BRtt = arrays[br]["tt"][j]
            if args.run == 2:
                BR_plot_obs = y_mmtt_boosted_obs[i] / (2 * 1000 * BRmm * BRtt)
                BR_plot_exp = y_mmtt_boosted_exp[i] / (2 * 1000 * BRmm * BRtt)

                z_obs.append(BR_plot_obs)
                z_exp.append(BR_plot_exp)

    z_obs_array = np.array(z_obs)
    z_exp_array = np.array(z_exp)

    x_mmtt_boosted_obs_total = np.tile(x_mmtt_boosted_obs, len(brs))
    y_mmtt_boosted_obs_total = np.repeat(y_mmtt_boosted_obs, len(brs))
    x_mmtt_boosted_exp_total = np.tile(x_mmtt_boosted_exp, len(brs))
    y_mmtt_boosted_exp_total = np.repeat(y_mmtt_boosted_exp, len(brs))

    canv = ROOT.TCanvas("2HDM+S", "2HDM+S", 740, 640)
    canv.SetRightMargin(0.16) 
    canv.SetLogz()


    # Create graph for observed data
    graph_obs = ROOT.TGraph2D(len(x_mmtt_boosted_obs_total), x_mmtt_boosted_obs_total, tan_beta, z_obs_array)
    graph_obs.SetTitle(";m_{A} [GeV];tan#beta;BR") 
    #graph_obs.GetXaxis().SetTitle("m_{A} [GeV]")  # Set x-axis label as m_A with unit GeV
    #graph_obs.GetYaxis().SetTitle("tan#beta")    # Set y-axis label as tan(beta)
    #graph_obs.GetZaxis().SetTitle("BR")
    graph_obs.SetNpx(100)
    graph_obs.SetNpy(100)
    graph_obs.SetMinimum(0.001)
    graph_obs.SetMaximum(10) #for model 2
    graph_obs.Draw("COLZ")
    canv.Modified()
    canv.Update()

    lumiBlurb1=add_CMS()
    lumiBlurb1.Draw("same")
    lumiBlurb2=add_Preliminary()
    lumiBlurb2.Draw("same")
    lumiBlurb=add_lumi()
    if (args.run==1):
	    lumiBlurb=add_lumi_runI()
    lumiBlurb.Draw("same")
    canv.Update() 
    canv.SaveAs('3D_plot_BR_vs_Mass_vs_tanBeta_obs_model2.png')

    # Create graph for expected data
    graph_exp = ROOT.TGraph2D(len(x_mmtt_boosted_exp_total), x_mmtt_boosted_exp_total, tan_beta, z_exp_array)
    graph_exp.SetTitle(";m_{A} [GeV];tan#beta; BR") 
    #graph_exp.GetXaxis().SetTitle("m_{A} [GeV]")  # Se t x-axis label as m_A with unit GeV
    #graph_exp.GetYaxis().SetTitle("tan#beta")    # Set y-axis label as tan(beta)
    #graph_exp.GetZaxis().SetTitle("BR") 
    graph_exp.SetNpx(100)
    graph_exp.SetNpy(100)
    graph_exp.SetMinimum(0.001)
    graph_exp.SetMaximum(10)
    graph_exp.Draw("COLZ")
    canv.Modified()
    canv.Update()

    lumiBlurb1=add_CMS()
    lumiBlurb1.Draw("same")
    lumiBlurb2=add_Preliminary()
    lumiBlurb2.Draw("same")
    lumiBlurb=add_lumi()
    if (args.run==1):
	    lumiBlurb=add_lumi_runI()
    lumiBlurb.Draw("same")
    canv.Update() 
    canv.SaveAs('3D_plot_BR_vs_Mass_vs_tanBeta_exp_model2.png')
