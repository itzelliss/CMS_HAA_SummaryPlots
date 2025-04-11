#plot ma vs obseerved and expected values

import ROOT
import numpy as np
from array import array
import os
import argparse
import math

# Higgs mass in consideration
Hmass = 125

# Load observed and expected limits
x_mmtt_boosted_obs, y_mmtt_boosted_obs = np.loadtxt(f'mmtt_H{Hmass}_ALL_fullRun2_obs.txt', unpack=True)
x_mmtt_boosted_exp, y_mmtt_boosted_exp = np.loadtxt(f'mmtt_H{Hmass}_ALL_fullRun2_exp.txt', unpack=True)

x_obs_array = array("d", x_mmtt_boosted_obs)
x_exp_array = array("d", x_mmtt_boosted_exp)
y_obs_array = array("d", y_mmtt_boosted_obs)
y_exp_array = array("d", y_mmtt_boosted_exp)

#x is mass, y is BR

#plot x vs y
def plot_graph(x, y, title, x_title, y_title,color):
    # Create a TGraph
    graph = ROOT.TGraph(len(x), x, y)
    graph.SetTitle(title)
    graph.GetXaxis().SetTitle(x_title)
    graph.GetYaxis().SetTitle(y_title)
    graph.SetMarkerStyle(20)
    graph.SetMarkerSize(0.5)
    graph.SetLineWidth(2)
    graph.SetLineColor(color)
    
    
    # Draw the graph
    canvas = ROOT.TCanvas("canvas", "canvas", 800, 600)
    graph.Draw("ALP")
    
    # Set log scale if needed
    #canvas.SetLogy()
    
    # Save the canvas as an image
    canvas.SaveAs(f"{title}.png")

plot_graph(x_obs_array, y_obs_array, "Observed Limits", "m_{a} (GeV)", "#frac{#sigma_{H}}{#sigma_{SM}}B(H#rightarrow aa)", ROOT.kBlue)
plot_graph(x_exp_array, y_exp_array, "Expected Limits", "m_{a} (GeV)", "#frac{#sigma_{H}}{#sigma_{SM}}B(H#rightarrow aa)", ROOT.kRed)

