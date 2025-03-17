import argparse
import os
import numpy as np
from array import array
import ROOT
from scipy.interpolate import interp1d

# Change the mass accordingly
Hmass = 125

def add_lumi():
    lowX=0.685-0.045
    lowY=0.855-0.035
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.30, lowY+0.16, "NDC")
    lumi.SetBorderSize(0)
    lumi.SetFillStyle(0)
    lumi.SetTextAlign(12)
    lumi.SetTextColor(1)
    lumi.SetTextFont(42)
    lumi.SetTextSize(0.04)
    lumi.AddText("137.6 fb^{-1} (13 TeV)")
    return lumi

def add_lumi_runI():
    lowX=0.685-0.045
    lowY=0.855-0.045
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.30, lowY+0.16, "NDC")
    lumi.SetBorderSize(0)
    lumi.SetFillStyle(0)
    lumi.SetTextAlign(12)
    lumi.SetTextColor(1)
    lumi.SetTextFont(42)
    lumi.SetTextSize(0.04)
    lumi.AddText("19.7 fb^{-1} (8 TeV)")
    return lumi

def add_CMS():
    lowX=0.13-0.045
    lowY=0.865-0.035
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextFont(61)
    lumi.SetTextSize(0.06)
    lumi.SetBorderSize(0)
    lumi.SetFillStyle(0)
    lumi.SetTextAlign(12)
    lumi.SetTextColor(1)
    lumi.AddText("CMS")
    return lumi 

def add_Preliminary():
    lowX=0.25-0.045
    lowY=0.86-0.035
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextSize(0.045)
    lumi.SetBorderSize(0)
    lumi.SetFillStyle(0)
    lumi.SetTextAlign(12)
    lumi.SetTextColor(1)
    lumi.SetTextFont(52)
    lumi.AddText("Preliminary")
    return lumi 

def add_custom_text(typestring):
    lowX = 0.12
    lowY = 0.72
    custom_text = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.2, lowY+0.16, "NDC")
    custom_text.SetBorderSize(0)
    custom_text.SetFillColor(10)
    custom_text.SetTextAlign(12)
    custom_text.SetTextColor(1)
    custom_text.SetTextFont(42)
    custom_text.SetTextSize(0.03)
    custom_text.AddText(f"2HDM+S Type-{typestring}")  # Set type based on argument
    custom_text.AddText("m_{H} = " + f"{Hmass} GeV")
    return custom_text

#Define function to interpolate points
def interpolate_points(x, y, num_points=2000):
    f = interp1d(x, y, kind='cubic')  # Cubic interpolation for smooth curves
    x_new = np.linspace(min(x), max(x), num_points)
    y_new = f(x_new)
    return x_new, y_new

# Import array of tanBeta
tan_beta = np.loadtxt('tan_beta_5.txt', unpack=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=int, default=1, help="Which type of 2HDM?")
    parser.add_argument('--run', type=int, default=2, help="Which run?")
    args = parser.parse_args()

    brs = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

    # Define model types
    typestring = {1: 'I', 2: 'II', 3: 'III', 4: 'IV'}.get(args.model, '')

    # Create dictionary to store arrays of BR values
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

    # Load observed and expected limit values 
    x_mmtt_boosted_obs, y_mmtt_boosted_obs = np.loadtxt(f'mmtt_H{Hmass}_ALL_fullRun2_obs.txt', unpack=True)
    x_mmtt_boosted_exp, y_mmtt_boosted_exp = np.loadtxt('mmtt_H125_ALL_fullRun2_exp.txt', unpack=True)

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

    # Set color palette
    ROOT.gStyle.SetPalette(ROOT.kPastel)

    # Create graph for observed data
    graph_obs = ROOT.TGraph2D(len(x_mmtt_boosted_obs_total), x_mmtt_boosted_obs_total, tan_beta, z_obs_array)
    graph_obs.SetTitle(";m_{a} (GeV);tan #beta; #frac{#sigma_{H}}{#sigma_{SM}}B(H#rightarrow aa)") 
    graph_obs.SetNpx(100)
    graph_obs.SetNpy(100)
    graph_obs.SetMinimum(0.001)
    graph_obs.SetMaximum(10)
    graph_obs.Draw("COLZ")
    canv.Modified()
    canv.Update()

    lumiBlurb1 = add_CMS()
    lumiBlurb1.Draw("same")
    lumiBlurb2 = add_Preliminary()
    lumiBlurb2.Draw("same")
    lumiBlurb = add_lumi_runI() if args.run == 1 else add_lumi()
    lumiBlurb.Draw("same")

    # Add custom text box with dynamic model type
    custom_text_box = add_custom_text(typestring)
    custom_text_box.Draw("same")

    #Observed values equal to 1
    # Dictionary to store the closest points for each m_a
    closest_points_obs1 = {}

    for i, (ma, z_value) in enumerate(zip(x_mmtt_boosted_obs_total, z_obs_array)):
        if abs(z_value - 1) < 1:  # Check if z_obs_array is close to 1
            tan_beta_val = tan_beta[i]
            diff_from_1 = abs(z_value - 1)
            
            # Update the dictionary if the point is closer to 1 than any previously stored point for this m_a
            if ma not in closest_points_obs1 or diff_from_1 < closest_points_obs1[ma][1]:
                closest_points_obs1[ma] = (tan_beta_val, diff_from_1)

    # Prepare arrays of m_a and tan_beta for the closest points
    ma_values_br_1 = list(closest_points_obs1.keys())
    tan_beta_values_br_1 = [closest_points_obs1[ma][0] for ma in ma_values_br_1]

    sorted_br_1_pairs = sorted(zip(ma_values_br_1,tan_beta_values_br_1))
    ma_values_br_1_sorted, tan_beta_values_br_1_sorted = zip(*sorted_br_1_pairs)

    ma_values_br_1_interp, tan_beta_values_br_1_interp = interpolate_points(ma_values_br_1_sorted, tan_beta_values_br_1_sorted)

    # Plot points for BR = 1

    graph_br_1_line = ROOT.TGraph(len(ma_values_br_1_interp), array("d", ma_values_br_1_interp), array("d", tan_beta_values_br_1_interp))
    graph_br_1_line.SetLineStyle(1)  # Solid line
    graph_br_1_line.SetLineWidth(2)  # Line width
    graph_br_1_line.SetLineColor(ROOT.kRed)  # Set color for visibility
    graph_br_1_line.Draw("L SAME")
    #graph_br_1_line.Smooth(2)  # Apply smoothing; higher values smooth more


    # if ma_values_br_1_sorted and tan_beta_values_br_1_sorted:  # Ensure there are points to plot
    #     graph_br_1_line = ROOT.TGraph(len(ma_values_br_1_sorted), array("d", ma_values_br_1_sorted), array("d", tan_beta_values_br_1_sorted))
    #     graph_br_1_line.SetLineStyle(1)  # Solid line
    #     graph_br_1_line.SetLineWidth(3)  # Line width
    #     graph_br_1_line.SetLineColor(ROOT.kRed)  # Set color for visibility
    #     graph_br_1_line.Draw("L SAME")  # Draw as line
    
    #Observed values equal to 0.16
    # Dictionary to store the closest points for each m_a
    closest_points_obs16 = {}

    for i, (ma, z_value) in enumerate(zip(x_mmtt_boosted_obs_total, z_obs_array)):
        if abs(z_value - 0.16) < 0.5:  # Check if z_obs_array is close to 1 (0.05 originallt)
            tan_beta_val = tan_beta[i]
            diff_from_16 = abs(z_value - 0.16)
            
            # Update the dictionary if the point is closer to 1 than any previously stored point for this m_a
            if ma not in closest_points_obs16 or diff_from_16 < closest_points_obs16[ma][1]:
                closest_points_obs16[ma] = (tan_beta_val, diff_from_16)

    # Prepare arrays of m_a and tan_beta for the closest points
    ma_values_br_16 = list(closest_points_obs16.keys())
    tan_beta_values_br_16 = [closest_points_obs16[ma][0] for ma in ma_values_br_16]

    sorted_br_16_pairs = sorted(zip(ma_values_br_16,tan_beta_values_br_16))
    ma_values_br_16_sorted, tan_beta_values_br_16_sorted = zip(*sorted_br_16_pairs)

    ma_values_br_16_interp, tan_beta_values_br_16_interp = interpolate_points(ma_values_br_16_sorted, tan_beta_values_br_16_sorted)

    # Plot points for BR = 0.16

    graph_br_16_points = ROOT.TGraph(len(ma_values_br_16_interp), array("d", ma_values_br_16_interp), array("d", tan_beta_values_br_16_interp))
    graph_br_16_points.SetLineStyle(1)  # Solid line
    graph_br_16_points.SetLineWidth(2)  # Line width
    graph_br_16_points.SetLineColor(ROOT.kGreen+2)  # Set color for visibility
    graph_br_16_points.Draw("L SAME")

    # if ma_values_br_16_sorted and tan_beta_values_br_16_sorted:  # Ensure there are points to plot
    #     graph_br_16_points = ROOT.TGraph(len(ma_values_br_16_sorted), array("d", ma_values_br_16_sorted), array("d", tan_beta_values_br_16_sorted))
    #     graph_br_16_points.SetLineStyle(1)  # Set line style
    #     graph_br_16_points.SetLineWidth(3)    # Adjust line size
    #     graph_br_16_points.SetLineColor(ROOT.kGreen+2)  # Set color for visibility
    #     graph_br_16_points.Draw("L SAME")  # Draw as line

    #Expected values equal to 1
    # Dictionary to store the closest points for each m_a
    closest_points_exp1 = {}

    for i, (ma, z_value) in enumerate(zip(x_mmtt_boosted_exp_total, z_exp_array)):
        if abs(z_value - 1) < 1:  # Check if z_obs_array is close to 1
            tan_beta_val = tan_beta[i]
            diff_from_1 = abs(z_value - 1)
            
            # Update the dictionary if the point is closer to 1 than any previously stored point for this m_a
            if ma not in closest_points_exp1 or diff_from_1 < closest_points_exp1[ma][1]:
                closest_points_exp1[ma] = (tan_beta_val, diff_from_1)

    # Prepare arrays of m_a and tan_beta for the closest points
    ma_values_exp_1 = list(closest_points_exp1.keys())
    tan_beta_values_exp_1 = [closest_points_exp1[ma][0] for ma in ma_values_exp_1]

    sorted_exp_1_pairs = sorted(zip(ma_values_exp_1,tan_beta_values_exp_1))
    ma_values_exp_1_sorted, tan_beta_values_exp_1_sorted = zip(*sorted_exp_1_pairs)

    ma_values_exp_1_interp, tan_beta_values_exp_1_interp = interpolate_points(ma_values_exp_1_sorted, tan_beta_values_exp_1_sorted)

    # Plot points for BR = 1

    graph_exp_1_points = ROOT.TGraph(len(ma_values_exp_1_interp), array("d", ma_values_exp_1_interp), array("d", tan_beta_values_exp_1_interp))
    graph_exp_1_points.SetLineStyle(7)  # Dashed line
    graph_exp_1_points.SetLineWidth(2)  # Line width
    graph_exp_1_points.SetLineColor(ROOT.kRed)  # Set color for visibility
    graph_exp_1_points.Draw("L SAME")

    # if ma_values_exp_1_sorted and tan_beta_values_exp_1_sorted:  # Ensure there are points to plot
    #     graph_exp_1_points = ROOT.TGraph(len(ma_values_exp_1_sorted), array("d", ma_values_exp_1_sorted), array("d", tan_beta_values_exp_1_sorted))
    #     graph_exp_1_points.SetLineStyle(7) # Set marker style to points
    #     graph_exp_1_points.SetLineWidth(3)   # Adjust marker size
    #     graph_exp_1_points.SetLineColor(ROOT.kRed)  # Set color for visibility
    #     graph_exp_1_points.Draw("L SAME")  # Draw only points

    #Expected values equal to 0.16
    # Dictionary to store the closest points for each m_a
    closest_points_exp16 = {}

    for i, (ma, z_value) in enumerate(zip(x_mmtt_boosted_exp_total, z_exp_array)):
        if abs(z_value - 0.16) < 0.5:  # Check if z_obs_array is close to 0.16
            tan_beta_val = tan_beta[i]
            diff_from_16 = abs(z_value - 0.16)
            
            # Update the dictionary if the point is closer to 1 than any previously stored point for this m_a
            if ma not in closest_points_exp16 or diff_from_16 < closest_points_exp16[ma][1]:
                closest_points_exp16[ma] = (tan_beta_val, diff_from_16)

    # Prepare arrays of m_a and tan_beta for the closest points
    ma_values_exp_16 = list(closest_points_exp16.keys())
    tan_beta_values_exp_16 = [closest_points_exp16[ma][0] for ma in ma_values_exp_16]

    sorted_exp_16_pairs = sorted(zip(ma_values_exp_16,tan_beta_values_exp_16))
    ma_values_exp_16_sorted, tan_beta_values_exp_16_sorted = zip(*sorted_exp_16_pairs)

    ma_values_exp_16_interp, tan_beta_values_exp_16_interp = interpolate_points(ma_values_exp_16_sorted, tan_beta_values_exp_16_sorted)

    # Plot points for BR = 0.16

    graph_exp_16_points = ROOT.TGraph(len(ma_values_exp_16_interp), array("d", ma_values_exp_16_interp), array("d", tan_beta_values_exp_16_interp))
    graph_exp_16_points.SetLineStyle(7)  # Dashed line
    graph_exp_16_points.SetLineWidth(2)  # Line width
    graph_exp_16_points.SetLineColor(ROOT.kGreen+2)  # Set color for visibility
    graph_exp_16_points.Draw("L SAME")


    # if ma_values_exp_16_sorted and tan_beta_values_exp_16_sorted:  # Ensure there are points to plot
    #     graph_exp_16_points = ROOT.TGraph(len(ma_values_exp_16_sorted), array("d", ma_values_exp_16_sorted), array("d", tan_beta_values_exp_16_sorted))
    #     graph_exp_16_points.SetLineStyle(7)  # Set marker style to points
    #     graph_exp_16_points.SetLineWidth(3)    # Adjust marker size
    #     graph_exp_16_points.SetLineColor(ROOT.kGreen+2)  # Set color for visibility
    #     graph_exp_16_points.Draw("L SAME")  # Draw only points


    leg0_ = ROOT.TLegend(0.51, 0.58, 0.82, 0.88)
    leg0_.SetBorderSize(0)
    leg0_.SetTextSize(0.03)
    leg0_.SetFillColor(ROOT.kWhite)
    leg0_.SetHeader("95% CL upper limits",'L')
    leg0_.AddEntry(graph_exp_1_points, "#splitline{Expected exclusion}{B(H#rightarrow aa) = 1.0}", "L")
    leg0_.AddEntry(graph_br_1_line, "#splitline{Observed exclusion}{B(H#rightarrow aa) = 1.0}", "LF")
    leg0_.AddEntry(graph_exp_16_points, "#splitline{Expected exclusion}{B(H#rightarrow aa) = 0.16}", "L")
    leg0_.AddEntry(graph_br_16_points, "#splitline{Observed exclusion}{B(H#rightarrow aa) = 0.16}", "L")
    leg0_.Draw("same")

    #print(ma_values_br_1_sorted,tan_beta_values_br_1_sorted)

    canv.Update()
    canv.SaveAs(f'./Contour_Plots/Updated_limits/Line_smooth_Model_Dependent_plot_H{Hmass}_model_{args.model}_Run2_OBS_0-5.png')