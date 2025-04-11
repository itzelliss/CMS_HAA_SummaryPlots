# This code plots mass vs BR(mm) * BR(tt) for different 2HDM models

import argparse
import os
import numpy as np
from array import array
import ROOT
from scipy.interpolate import UnivariateSpline

# Higgs mass in consideration
Hmass = 125

# Main execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=int, default=1, help="Which type of 2HDM?")
    args = parser.parse_args()

    brs = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
    typestring = {1: 'I', 2: 'II', 3: 'III', 4: 'IV'}.get(args.model, '')

    # Create dictionary to store arrays of BR values
    arrays = {}
    for br in brs:
        if args.model == 1:
            myfile = "BR/BR_I.dat"
        else:
            myfile = f"BR/BR_{typestring}_{br:.1f}.dat"

        (array_type, array_mass, array_tanbeta, array_BRbb, array_BRcc,
         array_BRtt, array_BRmm, array_BRgg, array_BRpp, array_BRusd,
         array_BRhad) = np.loadtxt(myfile, unpack=True)
        
        arrays[br] = {
            'mass': array("d", array_mass),
            'mm': array("d", array_BRmm),
            'tt': array("d", array_BRtt),
            'bb': array("d", array_BRbb),
        }

# Plot mass vs BR(mm)*BR(tt), restricting mass range to [3.6, 21] GeV

#For model 2,3,4
if args.model in [2, 3, 4]:
    for br in brs:
        x = np.array(arrays[br]['mass'])
        y = 1/(np.array(arrays[br]['mm']) * np.array(arrays[br]['tt']))

        # Apply mask for mass between 3.6 and 21 GeV
        mask = (x >= 3.6) & (x <= 21.0)
        x_filtered = x[mask]
        y_filtered = y[mask]

        # Skip this BR if no points in range
        if len(x_filtered) == 0:
            print(f"[Warning] No data points in mass range for BR = {br}")
            continue

        # Convert to ROOT-compatible format
        x_arr = array("d", x_filtered)
        y_arr = array("d", y_filtered)

        # Prepare canvas
        br_str = str(br).replace('.', 'p')
        canv = ROOT.TCanvas(f"2HDM_S_{typestring}_{br_str}", f"2HDM Type {typestring} - BR={br:.1f}", 940, 640)
        canv.SetRightMargin(0.08)
        canv.SetLogy()

        # Create TGraph
        graph = ROOT.TGraph(len(x_arr), x_arr, y_arr)
        graph.SetTitle(f"2HDM+S Type {typestring} - tan#beta = {br:.1f}")
        graph.GetXaxis().SetTitle("m_{a} (GeV)")
        graph.GetXaxis().SetLimits(3.5, 21.1) 
        graph.GetYaxis().SetTitle("1/ (BR_{#mu#mu} #times BR_{#tau#tau})")
        graph.SetMarkerStyle(20)
        graph.SetMarkerSize(0.5)
        graph.SetLineWidth(2)
        graph.SetLineColor(ROOT.kBlue + 1)

        # Draw
        graph.Draw("ALP")

        # Save plot
        canv.SaveAs(f"./MASSvsBR/mass_vs_BRmmtt_{typestring}_{br_str}.png")
#For model 1 no need to iterate over brs        
else:
    # Correct filename for model 1
    myfile = "BR/BR_I.dat"

    # Load values from file
    (array_type, array_mass, array_tanbeta, array_BRbb, array_BRcc,
     array_BRtt, array_BRmm, array_BRgg, array_BRpp, array_BRusd,
     array_BRhad) = np.loadtxt(myfile, unpack=True)

    x = np.array(array_mass)
    y = 1 / (np.array(array_BRmm) * np.array(array_BRtt))

    # Apply mask for mass between 3.6 and 21 GeV
    mask = (x >= 3.6) & (x <= 21.0)
    x_filtered = x[mask]
    y_filtered = y[mask]

    if len(x_filtered) == 0:
        print("[Warning] No data points in mass range for model 1")
    else:
        x_arr = array("d", x_filtered)
        y_arr = array("d", y_filtered)

        canv = ROOT.TCanvas("2HDM_S_I", "2HDM+S Type I ", 940, 640)
        canv.SetRightMargin(0.08)
        canv.SetLogy()

        graph = ROOT.TGraph(len(x_arr), x_arr, y_arr)
        graph.SetTitle("2HDM Type I")
        graph.GetXaxis().SetTitle("m_{a} (GeV)")
        graph.GetXaxis().SetLimits(3.5, 21.1) 
        graph.GetYaxis().SetTitle("1 / (BR_{#mu#mu} #times BR_{#tau#tau})")
        graph.SetMarkerStyle(20)
        graph.SetMarkerSize(0.5)
        graph.SetLineWidth(2)
        graph.SetLineColor(ROOT.kBlue + 1)

        graph.Draw("ALP")
        canv.SaveAs("./MASSvsBR/mass_vs_BRmmtt_I.png")

       