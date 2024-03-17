import argparse 
import math
import os
from HttStyles import GetStyleHtt
from HttStyles import MakeCanvas
import ROOT
import numpy as np
from array import array

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

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=int, default='1', help="Which type of 2HDM?")
    parser.add_argument('--mass', type=float, default='1', help="Which mass?")
    parser.add_argument('--run', type=int, default='2', help="Which run?")

    args = parser.parse_args()

    brs = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0 ,1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0]

    if args.model == 1:
        typestring = 'I'
    if args.model == 2:
        typestring = 'II'
    if args.model == 3:
        typestring = 'III'
    if args.model == 4:
        typestring = 'IV'

    arrays = {}
    for br in brs:
        if args.model == 1:
            myfile = "BR/BR_I.dat"
        else:
            myfile = "BR/BR_{}_{:.1f}.dat".format(typestring, br)
        array_type, array_mass, array_tanbeta, array_BRbb, array_BRcc, array_BRtt, array_BRmm, array_BRgg, array_BRpp, array_BRusd, array_BRhad = np.loadtxt(myfile, unpack=True)
        arrays[br] = {
            'mass': array("d",array_mass),
            'mm'  : array("d",array_BRmm),
            'tt'  : array("d",array_BRtt),
            'bb'  : array("d",array_BRbb),
        }


    def make_graph(x_obs, y_obs, x_exp, y_exp, channel):
        graph_obs1=ROOT.TGraph()
        graph_obs2=ROOT.TGraph()
        graph_exp=ROOT.TGraph()

        # find the mass index
        found = False
        for mi, ma in enumerate(array_mass): # just the last one, all the same
            if ma<args.mass:
                continue
            found = True
            break

        if not found:
            return graph_obs1, graph_obs2, graph_exp

        def get_factor(br):
            BRmm = arrays[br]['mm'][mi]
            BRtt = arrays[br]['tt'][mi]
            BRbb = arrays[br]['bb'][mi]
            if channel == 'bbtt':
                return 2 * 100 * BRbb * BRtt 
            if channel == 'mmtt':
                if args.run==1:
                    return 2*BRmm*BRtt
                else:
                    return 2*1000*BRmm*BRtt
            if channel == 'mmbb':
                if args.run == 1:
                    return (2*BRmm*BRbb) / 0.00017
                else:
                    return 2*BRmm*BRbb
            if channel == 'tttt':
                if args.run == 1:
                    return 19.3*BRtt*BRtt
                else:
                    return BRtt*BRtt
            if channel == 'tttt2':
                return BRtt*BRtt
            if channel == 'mmtt_boosted':
                if args.run==1:
                    return 2*BRmm*BRtt
                else:
                    return 2*1000*BRmm*BRtt


            return 1
            

        # index of mass
        foundobs = False
        for obsi, ma in enumerate(x_obs):
            if ma < args.mass:
                continue
            foundobs = True
            break

        if not foundobs:
            return graph_obs1, graph_obs2, graph_exp
        
        for i, br in enumerate(brs):
            factor = get_factor(br)
            graph_obs1.SetPoint(i, br, y_obs[obsi] / factor)
            graph_exp.SetPoint(i, br, y_exp[obsi] / factor)
        graph_obs2 = graph_obs1.Clone()
        graph_obs1.SetPoint(i+1, brs[-1], 10000)
        graph_obs1.SetPoint(i+2, brs[0], 10000)
        for j, br in enumerate(brs):
            if args.mass < x_obs[0]:
                factor = get_factor(br)
        graph_obs1.SetPoint(i+3, brs[0], y_obs[0] / factor)

        return graph_obs1, graph_obs2, graph_exp


    # h->aa->mmtautau boosted
    x_mmtt_boosted_obs, y_mmtt_boosted_obs = np.loadtxt('mmtt_boosted_obs.txt', unpack=True)
    x_mmtt_boosted_exp, y_mmtt_boosted_exp = np.loadtxt('mmtt_boosted_exp.txt', unpack=True)
    graph_mmtt_boosted_obs1, graph_mmtt_boosted_obs2, graph_mmtt_boosted_exp = make_graph(x_mmtt_boosted_obs, y_mmtt_boosted_obs, x_mmtt_boosted_exp, y_mmtt_boosted_exp, 'mmtt')


    # skip 4m for now
    # only coding for ma>20, but should be easy to adapt to lower if you want


    if args.run==1:
        order = [
            'mmtt_boosted'
            #'mmtt',
            #'mmbb',
        ]
    else:
        order = [
            'mmtt_boosted'
           # 'mmtt',
            #'mmbb',
            #'bbtt',
        ]

    if args.run == 1:
        labels = {
           #'mmmm': "#splitline{h #rightarrow aa #rightarrow #mu#mu#mu#mu}{PLB 752 (2016) 146}",
           #'tttt': "#splitline{h #rightarrow aa #rightarrow #tau#tau#tau#tau}{JHEP 01 (2016) 079}",
           #'tttt2':"#splitline{h #rightarrow aa #rightarrow #tau#tau#tau#tau}{JHEP 10 (2017) 076}",
          # 'mmtt': "#splitline{h #rightarrow aa #rightarrow #mu#mu#tau#tau}{JHEP 10 (2017) 076}",
           #'mmbb': "#splitline{h #rightarrow aa #rightarrow #mu#mubb}{JHEP 10 (2017) 076}",
        }
    else:
        labels = {
            #'mmmm': "#splitline{h #rightarrow aa #rightarrow #mu#mu#mu#mu}{PLB 796 (2019) 131}",
            'mmtt_boosted': "#splitline{h #rightarrow aa #rightarrow #mu#mu#tau#tau}{JHEP 08 (2020) 139}",
            #'tttt': "#splitline{h #rightarrow aa #rightarrow #tau#tau#tau#tau}{PLB 800 (2019) 135087}",
            #'mmtt': "#splitline{h #rightarrow aa #rightarrow #mu#mu#tau#tau}{JHEP 11 (2018) 018}",
            #'mmbb': "#splitline{h #rightarrow aa #rightarrow #mu#mubb}{PLB 795 (2019) 398}",
            #'bbtt': "#splitline{h #rightarrow aa #rightarrow bb#tau#tau}{PLB 785 (2018) 462}",
        }


    ## bright
    hexes = [
        '#4477AA', # blue
        '#EE6677', # red
        '#228833', # green
        '#CCBB44', # yellow
        '#66CCEE', # cyan
        '#AA3377', # purple
        '#BBBBBB', # grey
    ]
   
    palette = [ROOT.TColor.GetColor(h) for h in hexes]
    alphacolors = [ROOT.TColor(4000+i,
                               float(int(h[1:3], 16))/255,
                               float(int(h[3:5], 16))/255,
                               float(int(h[5:7], 16))/255,
                               '',
                               0.25) for i,h in enumerate(hexes)]
    alphapalette = [a.GetNumber() for a in alphacolors]
    colors = {
        # order here is left to right (increasing ma) then ~top to bottom (increasing sensitivity, but not always)
        #'mmmm':         [palette[0], palette[0], alphapalette[0]],
        'mmtt_boosted': [palette[1], palette[1], alphapalette[1]],
        #'tttt':         [palette[2], palette[2], alphapalette[2]],
        #'tttt2':        [palette[1], palette[1], alphapalette[1]],
        #'mmtt':         [palette[3], palette[3], alphapalette[3]],
        #'mmbb':         [palette[4], palette[4], alphapalette[4]],
        #'bbtt':         [palette[5], palette[5], alphapalette[5]],
    }

    obs_graphs = {}

    canv = ROOT.TCanvas("2HDM+S", "2HDM+S", 740, 640);
    canv.SetGridx(0); canv.SetLogx(1);
    canv.SetGridy(0); canv.SetLogy(1);
    canv.SetLeftMargin(0.11);
    canv.SetRightMargin(0.05);
    canv.SetTopMargin(0.06);
    canv.SetBottomMargin(0.10);  
    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky()
    hr=canv.DrawFrame(0.5, 0.0001, 10., 10000.);
    if (args.model==1):
	    hr=canv.DrawFrame(0.5, 0.00001, 10., 1000.);
    if (args.model==2):
        hr=canv.DrawFrame(0.5, 0.00001, 10., 1000.);
    if (args.model==3):
        hr=canv.DrawFrame(0.5, 0.00001, 10., 10000.);
    if (args.model==4):
        hr=canv.DrawFrame(0.5, 0.00001, 10., 1000.);
    hr.SetXTitle("tan#beta");
    hr.GetXaxis().SetLabelFont(42);
    hr.GetXaxis().SetLabelSize(0.034);
    hr.GetXaxis().SetLabelOffset(0.015); # 0.015
    hr.GetXaxis().SetTitleSize(0.04);
    hr.GetXaxis().SetTitleFont(42);
    hr.GetXaxis().SetTitleColor(1);
    hr.GetXaxis().SetTitleOffset(1.20);
    hr.GetXaxis().SetNdivisions(505);
    hr.GetXaxis().SetMoreLogLabels();
    hr.GetXaxis().SetNoExponent();
    hr.SetYTitle("95% CL on #frac{#sigma_{h}}{#sigma_{SM}}B(h#rightarrow aa)");
    hr.GetYaxis().SetLabelFont(42);
    hr.GetYaxis().SetTitleSize(0.04);
    hr.GetYaxis().SetTitleOffset(1.20);
    hr.GetYaxis().SetLabelSize(0.034);    
    #hr.GetYaxis().SetNdivisions(505);
    #hr.GetYaxis().SetMoreLogLabels();

    graph_mmtt_boosted_exp.SetLineColor(colors['mmtt_boosted'][0]);
    graph_mmtt_boosted_exp.SetLineWidth(303);
    graph_mmtt_boosted_exp.SetFillStyle(3004);
    graph_mmtt_boosted_exp.SetFillColor(colors['mmtt_boosted'][0]);
    graph_mmtt_boosted_exp.SetLineStyle(1);
    graph_mmtt_boosted_exp.Draw("Csame");
    graph_mmtt_boosted_obs2.SetLineColor(colors['mmtt_boosted'][1]);
    graph_mmtt_boosted_obs2.SetLineStyle(1);
    graph_mmtt_boosted_obs2.SetLineWidth(1);
    graph_mmtt_boosted_obs2.SetMarkerStyle(20);
    graph_mmtt_boosted_obs2.SetMarkerSize(0.7);
    graph_mmtt_boosted_obs2.SetMarkerColor(colors['mmtt_boosted'][1]);
    graph_mmtt_boosted_obs1.SetLineColor(colors['mmtt_boosted'][1]);
    graph_mmtt_boosted_obs1.SetFillColor(colors['mmtt_boosted'][2]);
    graph_mmtt_boosted_obs1.SetFillStyle(1001); #3005
    graph_mmtt_boosted_obs1.Draw("Fsame");
    graph_mmtt_boosted_obs2.Draw("Lsame");
    obs_graphs['mmtt_boosted'] = graph_mmtt_boosted_obs1

    line = ROOT.TLine(0.5,1,10,1)
    line.SetLineStyle(2)
    line.SetLineColor(ROOT.kBlack)
    line.Draw("lsame")

    obs = ROOT.TGraph() 
    obs.SetFillColor(ROOT.kGray);
    exp = ROOT.TGraph(); 
    exp.SetLineColor(1); 
    exp.SetFillColor(1); 
    exp.SetLineWidth(303); 
    exp.SetFillStyle(3004);

    leg0_ = ROOT.TLegend(0.4, 0.31, 0.790, 0.4); 
    leg0_.SetBorderSize(0);
    leg0_.SetTextSize(0.03);
    leg0_.SetFillColor (ROOT.kWhite);
    leg0_.AddEntry(obs, "Observed exclusion 95% CL", "F");  
    leg0_.AddEntry(exp, "Expected exclusion 95% CL", "LF");
    leg0_.Draw("same");

    leg1_ = ROOT.TLegend(0.4, 0.120, 0.910, 0.305);
    leg1_.SetBorderSize(0);
    leg1_.SetTextSize(0.024);
    leg1_.SetNColumns(2);
    leg1_.SetFillColor (ROOT.kWhite);
    for k in order:
        leg1_.AddEntry(obs_graphs[k], labels[k], "F")
    leg1_.Draw("same");


    extra = ROOT.TPaveText(0.13, 0.79, 0.8, 0.89, "NDC");
    extra.SetBorderSize(   0 );
    extra.SetFillStyle (   0 );
    extra.SetTextAlign (  12 );
    extra.SetTextSize  (0.04 );
    extra.SetTextColor (   1 );
    extra.SetTextFont  (  62 ); 
    if str(args.model)=="1":
       extra.AddText("2HDM+S type I")
    if str(args.model)=="2":
       extra.AddText("2HDM+S type II")
    if str(args.model)=="3":
       extra.AddText("2HDM+S type III")
    if str(args.model)=="4":
       extra.AddText("2HDM+S type IV")
    if str(args.model)!="1":
       extra.AddText("m_{a} = "+str(args.mass)+" GeV")
    extra.Draw("same")

    lumiBlurb1=add_CMS()
    lumiBlurb1.Draw("same")
    lumiBlurb2=add_Preliminary()
    lumiBlurb2.Draw("same")
    lumiBlurb=add_lumi()
    if (args.run==1):
	    lumiBlurb=add_lumi_runI()
    lumiBlurb.Draw("same")

    canv.Update()
    postfix="_ma"+str(int(args.mass))
    if (args.run==1):
	    postfix=postfix+"_runI"
    canv.SaveAs('plots/run2_plot_BRaa_Type'+str(args.model)+postfix+'_vstanb.png')
    canv.SaveAs('plots/run2_plot_BRaa_Type'+str(args.model)+postfix+'_vstanb.pdf')

