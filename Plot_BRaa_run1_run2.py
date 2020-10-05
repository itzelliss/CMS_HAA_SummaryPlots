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

    # h->aa->bbtautau
    x_bbtt_obs, y_bbtt_obs = np.loadtxt('bbtt_obs.txt', unpack=True)
    x_bbtt_exp, y_bbtt_exp = np.loadtxt('bbtt_exp.txt', unpack=True)
    graph_bbtt_obs1=ROOT.TGraph()
    graph_bbtt_obs2=ROOT.TGraph()
    graph_bbtt_exp=ROOT.TGraph()
    for i in range(0,len(x_bbtt_obs)):
      BRbb=1.0
      BRtt=1.0
      for j in range(0,len(list_mass)):
	 if list_mass[j]<x_bbtt_obs[i]:
	    BRbb=list_BRbb[j]
            BRtt=list_BRtt[j]
      graph_bbtt_obs1.SetPoint(i,x_bbtt_obs[i],y_bbtt_obs[i]/(2*100*BRbb*BRtt))
      graph_bbtt_exp.SetPoint(i,x_bbtt_exp[i],y_bbtt_exp[i]/(2*100*BRbb*BRtt))
    graph_bbtt_obs2= graph_bbtt_obs1.Clone()
    graph_bbtt_obs1.SetPoint(i+1,x_bbtt_obs[i],10000)
    graph_bbtt_obs1.SetPoint(i+2,x_bbtt_obs[0],10000)
    for j in range(0,len(list_mass)):
      if list_mass[j]<x_bbtt_obs[0]:
          BRbb=list_BRbb[j]
          BRtt=list_BRtt[j]
    graph_bbtt_obs1.SetPoint(i+3,x_bbtt_obs[0],y_bbtt_obs[0]/(2*100*BRbb*BRtt))

    # h->aa->mmtautau
    x_mmtt_obs, y_mmtt_obs = np.loadtxt('mmtt_obs.txt', unpack=True)
    x_mmtt_exp, y_mmtt_exp = np.loadtxt('mmtt_exp.txt', unpack=True)
    if (args.run==1):
       x_mmtt_obs, y_mmtt_obs = np.loadtxt('mmtt_runI_obs.txt', unpack=True)
       x_mmtt_exp, y_mmtt_exp = np.loadtxt('mmtt_runI_exp.txt', unpack=True)
    graph_mmtt_obs1=ROOT.TGraph()
    graph_mmtt_obs2=ROOT.TGraph()
    graph_mmtt_exp=ROOT.TGraph()
    for i in range(0,len(x_mmtt_obs)):
      BRmm=1.0
      BRtt=1.0
      for j in range(0,len(list_mass)):
         if list_mass[j]<x_mmtt_obs[i]:
            BRmm=list_BRmm[j]
            BRtt=list_BRtt[j]
      if (args.run==2):
        graph_mmtt_obs1.SetPoint(i,x_mmtt_obs[i],y_mmtt_obs[i]/(2*1000*BRmm*BRtt))
        graph_mmtt_exp.SetPoint(i,x_mmtt_exp[i],y_mmtt_exp[i]/(2*1000*BRmm*BRtt))
      if (args.run==1):
        graph_mmtt_obs1.SetPoint(i,x_mmtt_obs[i],y_mmtt_obs[i]/(BRtt*BRtt))
        graph_mmtt_exp.SetPoint(i,x_mmtt_exp[i],y_mmtt_exp[i]/(BRtt*BRtt))
    graph_mmtt_obs2= graph_mmtt_obs1.Clone()
    graph_mmtt_obs1.SetPoint(i+1,x_mmtt_obs[i],10000)
    graph_mmtt_obs1.SetPoint(i+2,x_mmtt_obs[0],10000)
    for j in range(0,len(list_mass)):
      if list_mass[j]<x_mmtt_obs[0]:
          BRmm=list_BRmm[j]
          BRtt=list_BRtt[j]
    if (args.run==2):
       graph_mmtt_obs1.SetPoint(i+3,x_mmtt_obs[0],y_mmtt_obs[0]/(2*1000*BRmm*BRtt))
    if (args.run==1):
       graph_mmtt_obs1.SetPoint(i+3,x_mmtt_obs[0],y_mmtt_obs[0]/(BRtt*BRtt))

    # h->aa->mmtautau boosted
    x_mmtt_boosted_obs, y_mmtt_boosted_obs = np.loadtxt('mmtt_boosted_obs.txt', unpack=True)
    x_mmtt_boosted_exp, y_mmtt_boosted_exp = np.loadtxt('mmtt_boosted_exp.txt', unpack=True)
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

    # h->aa->mmbb
    x_mmbb_obs, y_mmbb_obs = np.loadtxt('mmbb_obs.txt', unpack=True)
    x_mmbb_exp, y_mmbb_exp = np.loadtxt('mmbb_exp.txt', unpack=True)
    if (args.run==1):
       x_mmbb_obs, y_mmbb_obs = np.loadtxt('mmbb_runI_obs.txt', unpack=True)
       x_mmbb_exp, y_mmbb_exp = np.loadtxt('mmbb_runI_exp.txt', unpack=True)
    graph_mmbb_obs1=ROOT.TGraph()
    graph_mmbb_obs2=ROOT.TGraph()
    graph_mmbb_exp=ROOT.TGraph()
    for i in range(0,len(x_mmbb_obs)):
      BRmm=1.0
      BRbb=1.0
      for j in range(0,len(list_mass)):
         if list_mass[j]<x_mmbb_obs[i]:
            BRmm=list_BRmm[j]
            BRbb=list_BRbb[j]
      if (args.run==2):
         graph_mmbb_obs1.SetPoint(i,x_mmbb_obs[i],y_mmbb_obs[i]/(2*BRmm*BRbb))
         graph_mmbb_exp.SetPoint(i,x_mmbb_exp[i],y_mmbb_exp[i]/(2*BRmm*BRbb))
      if (args.run==1):
         graph_mmbb_obs1.SetPoint(i,x_mmbb_obs[i],y_mmbb_obs[i]*0.00017/(2*BRmm*BRbb))
         graph_mmbb_exp.SetPoint(i,x_mmbb_exp[i],y_mmbb_exp[i]*0.00017/(2*BRmm*BRbb))
    graph_mmbb_obs2= graph_mmbb_obs1.Clone()
    graph_mmbb_obs1.SetPoint(i+1,x_mmbb_obs[i],10000)
    graph_mmbb_obs1.SetPoint(i+2,x_mmbb_obs[0],10000)
    for j in range(0,len(list_mass)):
      if list_mass[j]<x_mmbb_obs[0]:
          BRmm=list_BRmm[j]
          BRbb=list_BRbb[j]
    if (args.run==2):
       graph_mmbb_obs1.SetPoint(i+3,x_mmbb_obs[0],y_mmbb_obs[0]/(2*BRmm*BRbb))
    if (args.run==1):
       graph_mmbb_obs1.SetPoint(i+3,x_mmbb_obs[0],y_mmbb_obs[0]*0.00017/(2*BRmm*BRbb))

    # h->aa->tttt
    x_tttt_obs, y_tttt_obs = np.loadtxt('tttt_obs.txt', unpack=True)
    x_tttt_exp, y_tttt_exp = np.loadtxt('tttt_exp.txt', unpack=True)
    if (args.run==1):
       x_tttt_obs, y_tttt_obs = np.loadtxt('tttt_runI_obs.txt', unpack=True)
       x_tttt_exp, y_tttt_exp = np.loadtxt('tttt_runI_exp.txt', unpack=True)
    graph_tttt_obs1=ROOT.TGraph()
    graph_tttt_obs2=ROOT.TGraph()
    graph_tttt_exp=ROOT.TGraph()
    for i in range(0,len(x_tttt_obs)):
      BRtt=1.0
      for j in range(0,len(list_mass)):
         if list_mass[j]<x_tttt_obs[i]:
            BRtt=list_BRtt[j]
      if (args.run==2):
         graph_tttt_obs1.SetPoint(i,x_tttt_obs[i],y_tttt_obs[i]/(BRtt*BRtt))
         graph_tttt_exp.SetPoint(i,x_tttt_exp[i],y_tttt_exp[i]/(BRtt*BRtt))
      if (args.run==1):
         graph_tttt_obs1.SetPoint(i,x_tttt_obs[i],y_tttt_obs[i]/(19.3*BRtt*BRtt))
         graph_tttt_exp.SetPoint(i,x_tttt_exp[i],y_tttt_exp[i]/(19.3*BRtt*BRtt))
    graph_tttt_obs2= graph_tttt_obs1.Clone()
    graph_tttt_obs1.SetPoint(i+1,x_tttt_obs[i],10000)
    graph_tttt_obs1.SetPoint(i+2,x_tttt_obs[0],10000)
    for j in range(0,len(list_mass)):
      if list_mass[j]<x_tttt_obs[0]:
          BRtt=list_BRtt[j]
    if (args.run==2):
       graph_tttt_obs1.SetPoint(i+3,x_tttt_obs[0],y_tttt_obs[0]/(BRtt*BRtt))
    if (args.run==1):
       graph_tttt_obs1.SetPoint(i+3,x_tttt_obs[0],y_tttt_obs[0]/(19.3*BRtt*BRtt))

    # h->aa->tttt
    x_ttttv2_obs, y_ttttv2_obs = np.loadtxt('ttttv2_runI_obs.txt', unpack=True)
    x_ttttv2_exp, y_ttttv2_exp = np.loadtxt('ttttv2_runI_exp.txt', unpack=True)
    graph_ttttv2_obs1=ROOT.TGraph()
    graph_ttttv2_obs2=ROOT.TGraph()
    graph_ttttv2_exp=ROOT.TGraph()
    for i in range(0,len(x_ttttv2_obs)):
      BRtt=1.0
      for j in range(0,len(list_mass)):
         if list_mass[j]<x_ttttv2_obs[i]:
            BRtt=list_BRtt[j]
      graph_ttttv2_obs1.SetPoint(i,x_ttttv2_obs[i],y_ttttv2_obs[i]/(BRtt*BRtt))
      graph_ttttv2_exp.SetPoint(i,x_ttttv2_exp[i],y_ttttv2_exp[i]/(BRtt*BRtt))
    graph_ttttv2_obs2= graph_ttttv2_obs1.Clone()
    graph_ttttv2_obs1.SetPoint(i+1,x_ttttv2_obs[i],10000)
    graph_ttttv2_obs1.SetPoint(i+2,x_ttttv2_obs[0],10000)
    for j in range(0,len(list_mass)):
      if list_mass[j]<x_ttttv2_obs[0]:
          BRtt=list_BRtt[j]
    graph_ttttv2_obs1.SetPoint(i+3,x_ttttv2_obs[0],y_ttttv2_obs[0]/(BRtt*BRtt))

    # h->aa->mmmm
    x_mmmm_obs, y_mmmm_obs = np.loadtxt('mmmm_obs.txt', unpack=True)
    #x_mmmm_exp, y_mmmm_exp = np.loadtxt('mmmm_exp.txt', unpack=True)
    if (args.run==1):
       x_mmmm_obs, y_mmmm_obs = np.loadtxt('mmmm_runI_obs.txt', unpack=True)
       #x_mmmm_exp, y_mmmm_exp = np.loadtxt('mmmm_exp.txt', unpack=True)
    graph_mmmm_obs1=ROOT.TGraph()
    graph_mmmm_obs2=ROOT.TGraph()
    #graph_mmmm_exp=ROOT.TGraph()
    for i in range(0,len(x_mmmm_obs)):
      BRtt=1.0
      for j in range(0,len(list_mass)):
         if list_mass[j]<x_mmmm_obs[i]:
            BRmm=list_BRmm[j]
      if args.run==2:
         graph_mmmm_obs1.SetPoint(i,x_mmmm_obs[i],y_mmmm_obs[i]/(54620*BRmm*BRmm))
         #graph_mmmm_exp.SetPoint(i,x_mmmm_exp[i],y_mmmm_exp[i]/(BRmm*BRmm))
      if args.run==1:
         graph_mmmm_obs1.SetPoint(i,x_mmmm_obs[i],y_mmmm_obs[i]/(19300*BRmm*BRmm))
         #graph_mmmm_exp.SetPoint(i,x_mmmm_exp[i],y_mmmm_exp[i]/(19300*BRmm*BRmm))
    graph_mmmm_obs2= graph_mmmm_obs1.Clone()
    graph_mmmm_obs1.SetPoint(i+1,x_mmmm_obs[i],10000)
    graph_mmmm_obs1.SetPoint(i+2,x_mmmm_obs[0],10000)
    for j in range(0,len(list_mass)):
      if list_mass[j]<x_mmmm_obs[0]:
          BRmm=list_BRmm[j]
    if args.run==2:
       graph_mmmm_obs1.SetPoint(i+3,x_mmmm_obs[0],y_mmmm_obs[0]/(54620*BRmm*BRmm))
    if args.run==1:
       graph_mmmm_obs1.SetPoint(i+3,x_mmmm_obs[0],y_mmmm_obs[0]/(19300*BRmm*BRmm))

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
            'mmmm',
            'tttt',
            'tttt2',
            'mmtt',
            'mmbb',
        ]
    else:
        order = [
            'mmmm',
            'tttt',
            'mmtt_boosted',
            'mmtt',
            'mmbb',
            'bbtt',
        ]

    if args.run == 1:
        labels = {
           'mmmm': "#splitline{h #rightarrow aa #rightarrow #mu#mu#mu#mu}{PLB 752 (2016) 146}",
           'tttt': "#splitline{h #rightarrow aa #rightarrow #tau#tau#tau#tau}{JHEP 01 (2016) 079}",
           'tttt2':"#splitline{h #rightarrow aa #rightarrow #tau#tau#tau#tau}{JHEP 10 (2017) 076}",
           'mmtt': "#splitline{h #rightarrow aa #rightarrow #mu#mu#tau#tau}{JHEP 10 (2017) 076}",
           'mmbb': "#splitline{h #rightarrow aa #rightarrow #mu#mubb}{JHEP 10 (2017) 076}",
        }
    else:
        labels = {
            'mmmm': "#splitline{h #rightarrow aa #rightarrow #mu#mu#mu#mu}{PLB 796 (2019) 131}",
            'mmtt_boosted': "#splitline{h #rightarrow aa #rightarrow #mu#mu#tau#tau}{JHEP 08 (2020) 139}",
            'tttt': "#splitline{h #rightarrow aa #rightarrow #tau#tau#tau#tau}{PLB 800 (2019) 135087}",
            'mmtt': "#splitline{h #rightarrow aa #rightarrow #mu#mu#tau#tau}{JHEP 11 (2018) 018}",
            'mmbb': "#splitline{h #rightarrow aa #rightarrow #mu#mubb}{PLB 795 (2019) 398}",
            'bbtt': "#splitline{h #rightarrow aa #rightarrow bb#tau#tau}{PLB 785 (2018) 462}",
        }

    # previous colors: [expline, obsline, obsfill]
    #colors = {
    #    'mmmm':         [ROOT.kMagenta+2, ROOT.kMagenta, tMagenta.GetNumber()],
    #    'mmtt_boosted': [ROOT.kRed-7, ROOT.kRed-4, tRed.GetNumber()],
    #    'tttt':         [ROOT.kCyan+2, ROOT.kCyan, tCyan.GetNumber()],
    #    'tttt2':        [ROOT.kRed+2, ROOT.kRed, tRed.GetNumber()],
    #    'mmtt':         [ROOT.kGreen+2, ROOT.kGreen, tGreen.GetNumber()],
    #    'mmbb':         [ROOT.kOrange+2, ROOT.kOrange, tOrange.GetNumber()],
    #    'bbtt':         [ROOT.kBlue+2, ROOT.kBlue, tBlue.GetNumber()],
    #}

    # colors chosen to avoid issues with color blindness and grayscale
    # ps://cran.r-project.org/web/packages/khroma/vignettes/tol.html
    # https://davidmathlogic.com/colorblind/#%23332288-%23117733-%2344AA99-%2388CCEE-%23DDCC77-%23CC6677-%23AA4499-%23882255
    ## muted:
    #hexes = [
    #    '#44AA99', # teal
    #    '#CC6677', # rose
    #    '#332288', # indigo
    #    '#117733', # green
    #    '#882255', # whine
    #    '#88CCEE', # cyan
    #    '#999933', # olive
    #    '#AA4499', # purple
    #    '#DDCC77', # sand
    #]
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
    ## vibrant
    #hexes = [
    #    '#0077BB', # blue
    #    '#EE7733', # orange
    #    '#33BBEE', # cyan
    #    '#EE3377', # magenta
    #    '#CC3311', # red
    #    '#009988', # teal
    #    '#BBBBBB', # grey
    #]
    ## light
    #hexes = [
    #    '#EEDD88', # light yellow
    #    '#77AADD', # light blue
    #    '#EE8866', # orange
    #    '#FFAABB', # pink
    #    '#44BB99', # mint
    #    '#AAAA00', # olive
    #    '#DDDDDD', # pale grey
    #    '#99DDFF', # light cyan
    #    '#BBCC33', # pear
    #]
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
        'mmmm':         [palette[0], palette[0], alphapalette[0]],
        'mmtt_boosted': [palette[1], palette[1], alphapalette[1]],
        'tttt':         [palette[2], palette[2], alphapalette[2]],
        'tttt2':        [palette[1], palette[1], alphapalette[1]],
        'mmtt':         [palette[3], palette[3], alphapalette[3]],
        'mmbb':         [palette[4], palette[4], alphapalette[4]],
        'bbtt':         [palette[5], palette[5], alphapalette[5]],
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
    hr=canv.DrawFrame(1., 0.0001, 62., 10000.);
    #if (args.model==3 and args.tanbeta==5):
    #	 hr=canv.DrawFrame(1., 0.00001, 62., 10000.);
    if (args.model==1):
	hr=canv.DrawFrame(1., 0.00001, 62., 1000.);
    if (args.model==2):
        hr=canv.DrawFrame(1., 0.00001, 62., 1000.);
    if (args.model==3):
        hr=canv.DrawFrame(1., 0.00001, 62., 10000.);
    if (args.model==4):
        hr=canv.DrawFrame(1., 0.00001, 62., 1000.);
    hr.SetXTitle("m_{a} (GeV)");
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

    graph_bbtt_exp.SetLineColor(colors['bbtt'][0]);
    graph_bbtt_exp.SetLineWidth(303);
    graph_bbtt_exp.SetFillStyle(3004);
    graph_bbtt_exp.SetFillColor(colors['bbtt'][0]);
    graph_bbtt_exp.SetLineStyle(1);
    if args.run==2:
      graph_bbtt_exp.Draw("Csame");
    graph_bbtt_obs2.SetLineColor(colors['bbtt'][1]);
    graph_bbtt_obs2.SetLineStyle(1);
    graph_bbtt_obs2.SetLineWidth(1);
    graph_bbtt_obs2.SetMarkerStyle(20);
    graph_bbtt_obs2.SetMarkerSize(0.7);
    graph_bbtt_obs2.SetMarkerColor(colors['bbtt'][1]);
    graph_bbtt_obs1.SetLineColor(colors['bbtt'][1]);
    graph_bbtt_obs1.SetFillColor(colors['bbtt'][2]);
    graph_bbtt_obs1.SetFillStyle(1001); #3005
    if args.run==2:
      graph_bbtt_obs1.Draw("Fsame");
      graph_bbtt_obs2.Draw("Lsame");
      obs_graphs['bbtt'] = graph_bbtt_obs1

    graph_mmtt_exp.SetLineColor(colors['mmtt'][0]);
    graph_mmtt_exp.SetLineWidth(303);
    graph_mmtt_exp.SetFillStyle(3004);
    graph_mmtt_exp.SetFillColor(colors['mmtt'][0]);
    graph_mmtt_exp.SetLineStyle(1);
    graph_mmtt_exp.Draw("Csame");
    graph_mmtt_obs2.SetLineColor(colors['mmtt'][1]);
    graph_mmtt_obs2.SetLineStyle(1);
    graph_mmtt_obs2.SetLineWidth(1);
    graph_mmtt_obs2.SetMarkerStyle(20);
    graph_mmtt_obs2.SetMarkerSize(0.7);
    graph_mmtt_obs2.SetMarkerColor(colors['mmtt'][1]);
    graph_mmtt_obs1.SetLineColor(colors['mmtt'][1]);
    graph_mmtt_obs1.SetFillColor(colors['mmtt'][2]);
    graph_mmtt_obs1.SetFillStyle(1001); #3005
    graph_mmtt_obs1.Draw("Fsame");
    graph_mmtt_obs2.Draw("Lsame");
    obs_graphs['mmtt'] = graph_mmtt_obs1

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

    graph_mmbb_exp.SetLineColor(colors['mmbb'][0]);
    graph_mmbb_exp.SetLineWidth(303);
    graph_mmbb_exp.SetFillStyle(3004);
    graph_mmbb_exp.SetFillColor(colors['mmbb'][0]);
    graph_mmbb_exp.SetLineStyle(1);
    graph_mmbb_exp.Draw("Csame");
    graph_mmbb_obs2.SetLineColor(colors['mmbb'][1]);
    graph_mmbb_obs2.SetLineStyle(1);
    graph_mmbb_obs2.SetLineWidth(1);
    graph_mmbb_obs2.SetMarkerStyle(20);
    graph_mmbb_obs2.SetMarkerSize(0.7);
    graph_mmbb_obs2.SetMarkerColor(colors['mmbb'][1]);
    graph_mmbb_obs1.SetLineColor(colors['mmbb'][1]);
    graph_mmbb_obs1.SetFillColor(colors['mmbb'][2]);
    graph_mmbb_obs1.SetFillStyle(1001); #3005
    graph_mmbb_obs1.Draw("Fsame");
    graph_mmbb_obs2.Draw("Lsame");
    obs_graphs['mmbb'] = graph_mmbb_obs1

    graph_tttt_exp.SetLineColor(colors['tttt'][0]);
    graph_tttt_exp.SetLineWidth(303);
    graph_tttt_exp.SetFillStyle(3004);
    graph_tttt_exp.SetFillColor(colors['tttt'][0]);
    graph_tttt_exp.SetLineStyle(1);
    graph_tttt_exp.Draw("Csame");
    graph_tttt_obs2.SetLineColor(colors['tttt'][1]);
    graph_tttt_obs2.SetLineStyle(1);
    graph_tttt_obs2.SetLineWidth(1);
    graph_tttt_obs2.SetMarkerStyle(20);
    graph_tttt_obs2.SetMarkerSize(0.7);
    graph_tttt_obs2.SetMarkerColor(colors['tttt'][1]);
    graph_tttt_obs1.SetLineColor(colors['tttt'][1]);
    graph_tttt_obs1.SetFillColor(colors['tttt'][2]);
    graph_tttt_obs1.SetFillStyle(1001); #3005
    graph_tttt_obs1.Draw("Fsame");
    graph_tttt_obs2.Draw("Lsame");
    obs_graphs['tttt'] = graph_tttt_obs1

    graph_ttttv2_exp.SetLineColor(colors['tttt2'][0]);
    graph_ttttv2_exp.SetLineWidth(303);
    graph_ttttv2_exp.SetFillStyle(3004);
    graph_ttttv2_exp.SetFillColor(colors['tttt2'][0]);
    graph_ttttv2_exp.SetLineStyle(1);
    if (args.run==1):
       graph_ttttv2_exp.Draw("Csame");
    graph_ttttv2_obs2.SetLineColor(colors['tttt2'][1]);
    graph_ttttv2_obs2.SetLineStyle(1);
    graph_ttttv2_obs2.SetLineWidth(1);
    graph_ttttv2_obs2.SetMarkerStyle(20);
    graph_ttttv2_obs2.SetMarkerSize(0.7);
    graph_ttttv2_obs2.SetMarkerColor(colors['tttt2'][1]);
    graph_ttttv2_obs1.SetLineColor(colors['tttt2'][1]);
    graph_ttttv2_obs1.SetFillColor(colors['tttt2'][2]);
    graph_ttttv2_obs1.SetFillStyle(1001); #3005
    if (args.run==1):
      graph_ttttv2_obs1.Draw("Fsame");
      graph_ttttv2_obs2.Draw("Lsame");
      obs_graphs['tttt2'] = graph_ttttv2_obs1

    #graph_mmmm_exp.SetLineColor(colors['mmmm'][0]);
    #graph_mmmm_exp.SetLineWidth(303);
    #graph_mmmm_exp.SetFillStyle(3004);
    #graph_mmmm_exp.SetFillColor(colors['mmmm'][0]);
    #graph_mmmm_exp.SetLineStyle(1);
    #graph_mmmm_exp.Draw("Csame");
    graph_mmmm_obs2.SetLineColor(colors['mmmm'][1]);
    graph_mmmm_obs2.SetLineStyle(1);
    graph_mmmm_obs2.SetLineWidth(1);
    graph_mmmm_obs2.SetMarkerStyle(20);
    graph_mmmm_obs2.SetMarkerSize(0.7);
    graph_mmmm_obs2.SetMarkerColor(colors['mmmm'][1]);
    graph_mmmm_obs1.SetLineColor(colors['mmmm'][1]);
    graph_mmmm_obs1.SetFillColor(colors['mmmm'][2]);
    graph_mmmm_obs1.SetFillStyle(1001); #3005
    graph_mmmm_obs1.Draw("Fsame");
    graph_mmmm_obs2.Draw("Lsame");
    obs_graphs['mmmm'] = graph_mmmm_obs1

    line = ROOT.TLine(1,1,62.5,1)
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
       extra.AddText("tan#beta = "+str(args.tanbeta))
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
    postfix=""
    if (args.model>1):
        postfix="_tanbeta"+str(int(args.tanbeta))
    if (args.run==1):
	postfix=postfix+"_runI"
    canv.SaveAs('plots/run2_plot_BRaa_Type'+str(args.model)+postfix+'.png')
    canv.SaveAs('plots/run2_plot_BRaa_Type'+str(args.model)+postfix+'.pdf')

