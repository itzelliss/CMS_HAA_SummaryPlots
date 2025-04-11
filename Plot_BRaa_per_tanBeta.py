import argparse
import os
import numpy as np
from array import array
import ROOT

# Higgs mass in consideration
Hmass = 125

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=int, default=1, help="Which type of 2HDM?")
    args = parser.parse_args()

    brs = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
    typestring = {1: 'I', 2: 'II', 3: 'III', 4: 'IV'}.get(args.model, '')

    # Load BR data
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

    # Load observed and expected limits
    x_mmtt_boosted_obs, y_mmtt_boosted_obs = np.loadtxt(f'mmtt_H{Hmass}_ALL_fullRun2_obs.txt', unpack=True)
    x_mmtt_boosted_exp, y_mmtt_boosted_exp = np.loadtxt(f'mmtt_H{Hmass}_ALL_fullRun2_exp.txt', unpack=True)

    x_obs_array = array("d", x_mmtt_boosted_obs)
    x_exp_array = array("d", x_mmtt_boosted_exp)

    for br in brs:
        z_obs = []
        z_exp = []

        for i, x_obs in enumerate(x_mmtt_boosted_obs):
            BRmm = 1.0
            BRtt = 1.0
            for j, mass in enumerate(arrays[br]['mass']):
                if mass < x_obs:
                    BRmm = arrays[br]['mm'][j]
                    BRtt = arrays[br]['tt'][j]

            if BRmm * BRtt > 0:
                BR_plot_obs = y_mmtt_boosted_obs[i] / (2 * 1000 * BRmm * BRtt)
                BR_plot_exp = y_mmtt_boosted_exp[i] / (2 * 1000 * BRmm * BRtt)
            else:
                BR_plot_obs = 0
                BR_plot_exp = 0

            z_obs.append(BR_plot_obs)
            z_exp.append(BR_plot_exp)

        z_obs_array = array("d", z_obs)
        z_exp_array = array("d", z_exp)

        # Create canvas
        br_str = str(br).replace('.', 'p')
        canv = ROOT.TCanvas(f"2HDM_S_{typestring}_{br_str}", f"2HDM Type {typestring} - tan#beta = {br:.1f}", 940, 640)
        canv.SetRightMargin(0.08)
        canv.SetLogy()

        # Plot observed
        graph = ROOT.TGraph(len(x_obs_array), x_obs_array, z_obs_array)
        graph.SetTitle(f"2HDM+S Type {typestring} - tan#beta = {br:.1f}")
        graph.GetXaxis().SetTitle("m_{a} (GeV)")
        graph.GetXaxis().SetLimits(3.5, 21.1)
        graph.GetYaxis().SetTitle("#frac{#sigma_{H}}{#sigma_{SM}}B(H#rightarrow aa)")
        graph.SetMarkerStyle(20)
        graph.SetMarkerSize(0.5)
        graph.SetLineWidth(2)
        graph.SetLineColor(ROOT.kBlue + 1)
        graph.Draw("ALP")

        # Plot expected
        graph_exp = ROOT.TGraph(len(x_exp_array), x_exp_array, z_exp_array)
        graph_exp.SetMarkerStyle(20)
        graph_exp.SetMarkerSize(0.5)
        graph_exp.SetLineWidth(2)
        graph_exp.SetLineColor(ROOT.kRed + 1)
        graph_exp.Draw("LP SAME")

        # Legend
        legend = ROOT.TLegend(0.65, 0.75, 0.88, 0.88)
        legend.AddEntry(graph, "Observed", "l")
        legend.AddEntry(graph_exp, "Expected", "l")
        legend.Draw()

        # Save canvas
        canv.SaveAs(f"./MASSvsBR/mass_vs_BRhaammtt_{typestring}_{br_str}.png")
