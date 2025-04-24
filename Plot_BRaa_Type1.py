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
    lumi  = ROOT.TPaveText(lowX-0.01, lowY+0.06, lowX+0.30, lowY+0.16, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextFont(42)
    lumi.SetTextSize(0.04)
    lumi.AddText("138 fb^{-1} (13 TeV)")
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
    lumi  = ROOT.TPaveText(lowX-0.04, lowY+0.06, lowX+0.35, lowY+0.16, "NDC")
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

def add_custom_text(model, tanbeta):
    lowX = 0.13
    lowY = 0.76
    custom_text = ROOT.TPaveText(lowX, lowY + 0.08, lowX + 0.2, lowY + 0.16, "NDC")
    custom_text.SetBorderSize(0)
    custom_text.SetFillColor(10)
    custom_text.SetTextAlign(12)
    custom_text.SetTextColor(1)
    custom_text.SetTextFont(42)
    custom_text.SetTextSize(0.03)
    custom_text.AddText(f"2HDM+S Type-I")
    custom_text.AddText("m_{H} = " + f" 125 GeV")
    #custom_text.AddText(f"tan#beta = {tanbeta}")
    return custom_text

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=int, default='1', help="Which type of 2HDM?")
    parser.add_argument('--tanbeta', type=float, default='1', help="Which tan beta?")
    parser.add_argument('--run', type=int, default='2', help="Which run?")

    args = parser.parse_args()

    myfile="BR/BR_II_2.0.dat"
    if args.model==1:
      myfile="BR/BR_I.dat"
    elif args.model==2:
      if args.tanbeta==0.5:
         myfile="BR/BR_II_0.5.dat"
      elif args.tanbeta==2:
         myfile="BR/BR_II_2.0.dat"
      elif args.tanbeta==5:
         myfile="BR/BR_II_5.0.dat"
    elif args.model==3:
      if args.tanbeta==0.5:
         myfile="BR/BR_III_0.5.dat"
      elif args.tanbeta==2:
         myfile="BR/BR_III_2.0.dat"
      elif args.tanbeta==5:
         myfile="BR/BR_III_5.0.dat"
    elif args.model==4:
      if args.tanbeta==0.5:
         myfile="BR/BR_IV_0.5.dat"
      elif args.tanbeta==2:
         myfile="BR/BR_IV_2.0.dat"
      elif args.tanbeta==5:
         myfile="BR/BR_IV_5.0.dat"

    array_type, array_mass, array_tanbeta, array_BRbb, array_BRcc, array_BRtt, array_BRmm, array_BRgg, array_BRpp, array_BRusd, array_BRhad = np.loadtxt(myfile, unpack=True)
    list_mass=array("d",array_mass)
    list_BRbb=array("d",array_BRbb)
    list_BRtt=array("d",array_BRtt)
    list_BRmm=array("d",array_BRmm)


    # h->aa->mmtautau boosted
    x_mmtt_boosted_obs, y_mmtt_boosted_obs = np.loadtxt('mmtt_H125_ALL_fullRun2_obs.txt', unpack=True)
    x_mmtt_boosted_exp, y_mmtt_boosted_exp = np.loadtxt('mmtt_H125_ALL_fullRun2_exp.txt', unpack=True)
    graph_mmtt_boosted_obs1=ROOT.TGraph()
    graph_mmtt_boosted_obs2=ROOT.TGraph()
    graph_mmtt_boosted_exp=ROOT.TGraph()
    for i in range(0,len(x_mmtt_boosted_obs)):
      BRmm=1.0
      BRtt=1.0
      for j in range(0,len(list_mass)):
         if list_mass[j]<x_mmtt_boosted_obs[i]:
            BRmm=list_BRmm[j]
            BRtt=list_BRtt[j]
      if (args.run==2):
        graph_mmtt_boosted_obs1.SetPoint(i,x_mmtt_boosted_obs[i],y_mmtt_boosted_obs[i]/(2*1000*BRmm*BRtt))
        graph_mmtt_boosted_exp.SetPoint(i,x_mmtt_boosted_exp[i],y_mmtt_boosted_exp[i]/(2*1000*BRmm*BRtt))
    graph_mmtt_boosted_obs2= graph_mmtt_boosted_obs1.Clone()
    graph_mmtt_boosted_obs1.SetPoint(i+1,x_mmtt_boosted_obs[i],10000)
    graph_mmtt_boosted_obs1.SetPoint(i+2,x_mmtt_boosted_obs[0],10000)
    for j in range(0,len(list_mass)):
      if list_mass[j]<x_mmtt_boosted_obs[0]:
          BRmm=list_BRmm[j]
          BRtt=list_BRtt[j]
    if (args.run==2):
       graph_mmtt_boosted_obs1.SetPoint(i+3,x_mmtt_boosted_obs[0],y_mmtt_boosted_obs[0]/(2*1000*BRmm*BRtt))


    tRed     = ROOT.TColor(3001,  1.,  0.,  0., "tRed"     , 0.15);
    tGreen   = ROOT.TColor(3002,  0.,  1.,  0., "tGreen"   , 0.15);
    tBlue    = ROOT.TColor(3003,  0.,  0.,  1., "tBlue"    , 0.15);
    tMagenta = ROOT.TColor(3004,  1.,  0.,  1., "tMagenta" , 0.15);
    tCyan    = ROOT.TColor(3005,  0.,  1.,  1., "tCyan"    , 0.50);
    tYellow  = ROOT.TColor(3006,  1.,  1.,  0., "tYellow"  , 0.15);
    tOrange  = ROOT.TColor(3007,  1.,  .5,  0., "tOrange"  , 0.15);
    tBlack   = ROOT.TColor(3008,  0.,  0.,  0., "tBlack"   , 0.15);
    kCombDark= ROOT.TColor(3009, .48, .88,  1., "kCombDark");
    kComb    = ROOT.TColor(3010, .28, .58, .70, "kComb");
    tComb    = ROOT.TColor(3011, .28, .58, .70, "tComb"    , 0.25);

    if args.run==1:
        order = [
            #'mmmm',
            #'tttt',
            #'tttt2',
            'mmtt',
            #'mmbb',
        ]
    else:
        order = [
            #'mmmm',
            #'tttt',
            'mmtt_boosted',
            #'mmtt',
            #'mmbb',
            #'bbtt',
        ]

    if args.run == 1:
        labels = {
           #'mmmm': "#splitline{h #rightarrow aa #rightarrow #mu#mu#mu#mu}{PLB 752 (2016) 146}",
           #'tttt': "#splitline{h #rightarrow aa #rightarrow #tau#tau#tau#tau}{JHEP 01 (2016) 079}",
           #'tttt2':"#splitline{h #rightarrow aa #rightarrow #tau#tau#tau#tau}{JHEP 10 (2017) 076}",
           'mmtt': "#splitline{h #rightarrow aa #rightarrow #mu#mu#tau#tau}{JHEP 10 (2017) 076}",
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
       # 'tttt':         [palette[2], palette[2], alphapalette[2]],
        #'tttt2':        [palette[1], palette[1], alphapalette[1]],
        #'mmtt':         [palette[3], palette[3], alphapalette[3]],
       # 'mmbb':         [palette[4], palette[4], alphapalette[4]],
       # 'bbtt':         [palette[5], palette[5], alphapalette[5]],
    }

    obs_graphs = {}

    canv = ROOT.TCanvas("2HDM+S", "2HDM+S", 740, 640);
    #canv.SetGridx(0); canv.SetLogx(1);
    canv.SetGridy(0); canv.SetLogy(1);
    canv.SetLeftMargin(0.11);
    canv.SetRightMargin(0.05);
    canv.SetTopMargin(0.06);
    canv.SetBottomMargin(0.10);  
    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky()
    hr=canv.DrawFrame(3.8, 0.001, 21., 100.);
    #if (args.model==3 and args.tanbeta==5):
    #	 hr=canv.DrawFrame(1., 0.00001, 62., 10000.);
    if (args.model==1):
	     hr=canv.DrawFrame(3.8, 0.001, 21., 100.);
    if (args.model==2):
        hr=canv.DrawFrame(3.8, 0.001, 21., 100.);
    if (args.model==3):
        hr=canv.DrawFrame(3.8, 0.001, 21., 100.);
    if (args.model==4):
        hr=canv.DrawFrame(3.8, 0.001, 21., 100.);
    hr.SetXTitle("m_{a} (GeV)");
    hr.GetXaxis().SetLabelFont(42);
    hr.GetXaxis().SetLabelSize(0.034);
    hr.GetXaxis().SetLabelOffset(0.015); # 0.015
    hr.GetXaxis().SetTitleSize(0.04);
    hr.GetXaxis().SetTitleFont(42);
    hr.GetXaxis().SetTitleColor(1);
    hr.GetXaxis().SetTitleOffset(1.20);
    #hr.GetXaxis().SetNdivisions(505);
    hr.GetXaxis().SetMoreLogLabels();
    hr.GetXaxis().SetNoExponent();
    hr.SetYTitle("95% CL on #frac{#sigma_{h}}{#sigma_{SM}}B(H#rightarrow aa)");
    hr.GetYaxis().SetLabelFont(42);
    hr.GetYaxis().SetTitleSize(0.04);
    hr.GetYaxis().SetTitleOffset(1.20);
    hr.GetYaxis().SetLabelSize(0.034);    
    #hr.GetYaxis().SetNdivisions(505);
    #hr.GetYaxis().SetMoreLogLabels();

    

    graph_mmtt_boosted_exp.SetLineColor(ROOT.kBlue);
    graph_mmtt_boosted_exp.SetLineWidth(302);
    graph_mmtt_boosted_exp.SetFillStyle(3004);
    graph_mmtt_boosted_exp.SetFillColor(ROOT.kBlue);
    graph_mmtt_boosted_exp.SetLineStyle(1);
    graph_mmtt_boosted_exp.Draw("Csame");
    graph_mmtt_boosted_obs2.SetLineColor(ROOT.kBlack);
    graph_mmtt_boosted_obs2.SetLineStyle(1);
    graph_mmtt_boosted_obs2.SetLineWidth(1);
    graph_mmtt_boosted_obs2.SetMarkerStyle(20);
    graph_mmtt_boosted_obs2.SetMarkerSize(0.7);
    graph_mmtt_boosted_obs2.SetMarkerColor(colors['mmtt_boosted'][1]);
    graph_mmtt_boosted_obs1.SetLineColor(colors['mmtt_boosted'][1]);
    graph_mmtt_boosted_obs1.SetFillColor(colors['mmtt_boosted'][2]);
    graph_mmtt_boosted_obs1.SetFillStyle(0); #3005 #1001
    graph_mmtt_boosted_obs1.Draw("Fsame");
    graph_mmtt_boosted_obs2.Draw("Lsame");
    obs_graphs['mmtt_boosted'] = graph_mmtt_boosted_obs1


    line = ROOT.TLine(3.8,1,21,1)
    line.SetLineStyle(7)
    line.SetLineColor(ROOT.kRed)
    line.SetLineWidth(3)
    line.Draw("lsame")

    line2 = ROOT.TLine(3.8,0.16,21,0.16)
    line2.SetLineStyle(7)
    line2.SetLineColor(ROOT.kGreen+2)
    line2.SetLineWidth(3)
    line2.Draw("lsame")

    #obs = ROOT.TGraph() 
    #obs.SetFillColor(colors['mmtt_boosted'][2]);
    exp = ROOT.TGraph(); 
    exp.SetLineColor(ROOT.kBlue); 
    exp.SetFillColor(ROOT.kBlue); 
    exp.SetLineWidth(302); 
    exp.SetFillStyle(3004);

    leg0_ = ROOT.TLegend(0.53, 0.16, 0.92, 0.32); 
    leg0_.SetBorderSize(0);
    leg0_.SetTextSize(0.03);
    leg0_.SetFillColor (ROOT.kWhite);
    leg0_.AddEntry(graph_mmtt_boosted_obs2, "Observed exclusion 95% CL", "L");  
    leg0_.AddEntry(exp, "Expected exclusion 95% CL", "LF");
    leg0_.AddEntry(line, "B(H#rightarrow aa) = 1.0", "L") 
    leg0_.AddEntry(line2, "B(H#rightarrow aa) = 0.16", "L") 
    leg0_.Draw("same");

    # leg1_ = ROOT.TLegend(0.4, 0.120, 0.910, 0.305);
    # leg1_.SetBorderSize(0);
    # leg1_.SetTextSize(0.024);
    # leg1_.SetNColumns(2);
    # leg1_.SetFillColor (ROOT.kWhite);
    # for k in order:
    #     leg1_.AddEntry(obs_graphs[k], labels[k], "F")
    # leg1_.Draw("same");


    # extra = ROOT.TPaveText(0.13, 0.79, 0.8, 0.89, "NDC");
    # extra.SetBorderSize(   0 );
    # extra.SetFillStyle (   0 );
    # extra.SetTextAlign (  12 );
    # extra.SetTextSize  (0.04 );
    # extra.SetTextColor (   1 );
    # extra.SetTextFont  (  62 ); 
    # if str(args.model)=="1":
    #    extra.AddText("2HDM+S type I")
    # if str(args.model)=="2":
    #    extra.AddText("2HDM+S type II")
    # if str(args.model)=="3":
    #    extra.AddText("2HDM+S type III")
    # if str(args.model)=="4":
    #    extra.AddText("2HDM+S type IV")
    # if str(args.model)!="1":
    #    extra.AddText("tan#beta = "+str(args.tanbeta))
    # extra.Draw("same")

    lumiBlurb1=add_CMS()
    lumiBlurb1.Draw("same")
    #lumiBlurb2=add_Preliminary()
    #lumiBlurb2.Draw("same")
    lumiBlurb=add_lumi()
    if (args.run==1):
       lumiBlurb=add_lumi_runI()
    lumiBlurb.Draw("same")

    # Add custom text
    custom_text_box = add_custom_text(args.model, args.tanbeta)
    custom_text_box.Draw("same")

    canv.Update()
    postfix=""
    if (args.model>1):
        postfix="_tanbeta"+str(int(args.tanbeta))
    if (args.run==1):
       postfix=postfix+"_runI"
    canv.SaveAs('Plots/Contour_Plots/Updated_limits/fix-labels_run2_plot_BRaa_Type'+str(args.model)+postfix+'.png')
    canv.SaveAs('Plots/Contour_Plots/Updated_limits/fix-labels_run2_plot_BRaa_Type'+str(args.model)+postfix+'.pdf')

