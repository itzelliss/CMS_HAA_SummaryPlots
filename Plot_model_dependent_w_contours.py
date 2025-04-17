import argparse
import os
import numpy as np
from array import array
import ROOT
from scipy.interpolate import interp1d, UnivariateSpline

# Higgs mass in consideration
Hmass = 125

def add_lumi():
    lowX = 0.685 - 0.045
    lowY = 0.855 - 0.035
    lumi = ROOT.TPaveText(lowX-0.02, lowY + 0.06, lowX + 0.1, lowY + 0.16, "NDC")
    lumi.SetBorderSize(0)
    lumi.SetFillStyle(0)
    lumi.SetTextAlign(12)
    lumi.SetTextColor(1)
    lumi.SetTextFont(42)
    lumi.SetTextSize(0.04)
    lumi.AddText("137.0 fb^{-1} (13 TeV)")
    return lumi

def add_CMS():
    lowX = 0.13 - 0.045
    lowY = 0.865 - 0.035
    cms = ROOT.TPaveText(lowX, lowY + 0.06, lowX + 0.35, lowY + 0.16, "NDC")
    cms.SetTextFont(61)
    cms.SetTextSize(0.06)
    cms.SetBorderSize(0)
    cms.SetFillStyle(0)
    cms.SetTextAlign(12)
    cms.SetTextColor(1)
    cms.AddText("CMS")
    return cms

def add_custom_text(typestring):
    lowX = 0.12
    lowY = 0.72
    custom_text = ROOT.TPaveText(lowX, lowY + 0.06, lowX + 0.2, lowY + 0.16, "NDC")
    custom_text.SetBorderSize(0)
    custom_text.SetFillColor(10)
    custom_text.SetTextAlign(12)
    custom_text.SetTextColor(1)
    custom_text.SetTextFont(42)
    custom_text.SetTextSize(0.03)
    custom_text.AddText(f"2HDM+S Type-{typestring}")
    custom_text.AddText("m_{H} = " + f"{Hmass} GeV")
    return custom_text

# Import array of tanBeta values
#tan_beta = np.loadtxt('tan_beta_5.txt', unpack=True) #For y scale from 0.5 - 5
tan_beta = np.loadtxt('tan_beta.txt', unpack=True) #For y scale from 0.2 - 5.5

def create_graph(x, y, color):
    n = len(x)
    x_array = array('d', x)
    y_array = array('d', y)
    graph = ROOT.TGraph(n, x_array, y_array)
    graph.SetMarkerStyle(0)
    graph.SetMarkerSize(0)
    graph.SetMarkerColor(color)
    graph.SetLineColor(color)
    graph.SetLineWidth(2)
    return graph

def create_graph_exp(x, y, color):
    n = len(x)
    x_array = array('d', x)
    y_array = array('d', y)
    graph = ROOT.TGraph(n, x_array, y_array)
    graph.SetMarkerStyle(1)
    graph.SetMarkerSize(0.5)
    graph.SetMarkerColor(color)
    graph.SetLineColor(color)
    graph.SetLineStyle(7)
    graph.SetLineWidth(2)
    return graph

# Function to smooth the curve using UnivariateSpline
def smooth_curve_spline(x, y, s=1.0, num_points=2000):
    x = np.array(x)
    y = np.array(y)
    unique_x, unique_indices = np.unique(x, return_index=True)
    unique_y = y[unique_indices]
    if len(unique_x) < 2:
        return unique_x, unique_y
    k = min(3, len(unique_x) - 1)  # linear if only 2 points, quadratic for 3, cubic otherwise
    x_smooth = np.linspace(unique_x.min(), unique_x.max(), num_points)
    spline = UnivariateSpline(unique_x, unique_y, s=s, k=k)
    y_smooth = spline(x_smooth)
    return x_smooth, y_smooth

# Main execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=int, default=1, help="Which type of 2HDM?")
    parser.add_argument('--run', type=int, default=2, help="Which run?")
    args = parser.parse_args()

    brs = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5]
    typestring = {1: 'I', 2: 'II', 3: 'III', 4: 'IV'}.get(args.model, '')

    # Create dictionary to store arrays of BR values
    arrays = {}
    for br in brs:
        myfile = "BR/BR_I.dat" if args.model == 1 else f"BR/BR_{typestring}_{br:.1f}.dat"
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

    z_obs = []
    z_exp = []
    for br in brs:
        for i, x_obs in enumerate(x_mmtt_boosted_obs):
            BRmm = 1.0
            BRtt = 1.0
            for j, mass in enumerate(arrays[br]['mass']):
                if mass < x_obs:
                    BRmm = arrays[br]['mm'][j]
                    BRtt = arrays[br]['tt'][j]
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

    # Create TCanvas and TGraph2D for observed limits
    canv = ROOT.TCanvas("2HDM+S", "2HDM+S", 740, 640)
    canv.SetRightMargin(0.16)
    canv.SetLogz()
    ROOT.gStyle.SetPalette(ROOT.kPastel)

    graph_obs = ROOT.TGraph2D(len(x_mmtt_boosted_obs_total),
                              array("d", x_mmtt_boosted_obs_total),
                              tan_beta,
                              z_obs_array)
    graph_obs.SetTitle(";m_{a} (GeV);tan #beta; #frac{#sigma_{H}}{#sigma_{SM}}B(H#rightarrow aa)")
    graph_obs.SetNpx(100)
    graph_obs.SetNpy(100)
    graph_obs.SetMinimum(0.001)
    graph_obs.SetMaximum(10)
    graph_obs.Draw("COLZ")
    canv.Modified()
    canv.Update()

    # Add CMS, lumi, and custom text
    lumi = add_lumi()
    lumi.Draw("same")
    cms = add_CMS()
    cms.Draw("same")
    custom_text = add_custom_text(typestring)
    custom_text.Draw("same")
    canv.Update()

    # Compute closest points for observed contour (where z is close to 1)
    closest_points_obs1 = {}
    for i, (ma, z_value) in enumerate(zip(x_mmtt_boosted_obs_total, z_obs_array)):
        if abs(z_value - 1) < 1:
            tan_beta_val = tan_beta[i]
            diff_from_1 = abs(z_value - 1)
            if ma not in closest_points_obs1 or diff_from_1 < closest_points_obs1[ma][1]:
                closest_points_obs1[ma] = (tan_beta_val, diff_from_1)

    # Prepare arrays of m_a and tan_beta for the observed contour
    ma_values_obs1 = np.array(list(closest_points_obs1.keys()))
    tan_beta_values_obs1 = np.array([closest_points_obs1[ma][0] for ma in ma_values_obs1])
    sorted_obs1_pairs = sorted(zip(ma_values_obs1, tan_beta_values_obs1))
    if sorted_obs1_pairs:
        ma_values_obs1, tan_beta_values_obs1 = zip(*sorted_obs1_pairs)
        ma_values_obs1 = np.array(ma_values_obs1)
        tan_beta_values_obs1 = np.array(tan_beta_values_obs1)
    else:
        ma_values_obs1 = np.array([])
        tan_beta_values_obs1 = np.array([])

    # For model 2, force segmentation at m_a = 11 and plot both segments (before and after 11)
    #For model 4, force segmentation at m_a = 4 and plot both segments (before and after 4)
    if args.model == 2:
        lower_threshold = 10.8
        upper_threshold = 10.82
        # Compute separate masks for observed contour
        mask_lower_obs = ma_values_obs1 <= lower_threshold
        mask_upper_obs = ma_values_obs1 > upper_threshold
        # Plot observed segment with m_a <= 11
        if np.any(mask_lower_obs):
            x_lower = ma_values_obs1[mask_lower_obs]
            y_lower = tan_beta_values_obs1[mask_lower_obs]
            x_smooth_lower, y_smooth_lower = smooth_curve_spline(x_lower, y_lower, s=0.5)
            graph_lower_obs1 = create_graph(x_smooth_lower, y_smooth_lower, ROOT.kRed)
            graph_lower_obs1.Draw("L SAME")
        # Plot observed segment with m_a > 11
        if np.any(mask_upper_obs):
            x_upper = ma_values_obs1[mask_upper_obs]
            y_upper = tan_beta_values_obs1[mask_upper_obs]
            x_smooth_upper, y_smooth_upper = smooth_curve_spline(x_upper, y_upper, s=0.5)
            graph_upper_obs1 = create_graph(x_smooth_upper, y_smooth_upper, ROOT.kRed)
            graph_upper_obs1.Draw("L SAME")
        #Draw vertical line before and after thresholds   
        line_lower = ROOT.TLine(x_lower[-1], y_lower[-1], x_lower[-1], 5) 
        line_lower.SetLineColor(ROOT.kRed)
        line_lower.SetLineStyle(1)
        line_lower.SetLineWidth(2)
        line_lower.Draw("SAME")
        line_upper = ROOT.TLine(x_upper[0], y_smooth_upper[0], x_upper[0], 5)
        line_upper.SetLineColor(ROOT.kRed)
        line_upper.SetLineStyle(1)
        line_upper.SetLineWidth(2)
        line_upper.Draw("SAME")
    elif args.model == 4:    
        #Compute separate masks for observed contour
        mask_lower_obs = ma_values_obs1 <= 4.075
        mask_upper_obs = ma_values_obs1 > 4.1
        # Plot observed segment with m_a <= 4.0
        if np.any(mask_lower_obs):
            x_lower = ma_values_obs1[mask_lower_obs]
            y_lower = tan_beta_values_obs1[mask_lower_obs]
            x_smooth_lower, y_smooth_lower = smooth_curve_spline(x_lower, y_lower, s=1.0)
            graph_lower_obs1 = create_graph(x_smooth_lower, y_smooth_lower, ROOT.kRed)
            graph_lower_obs1.Draw("L SAME")
        # Plot observed segment with m_a > 4.1
        if np.any(mask_upper_obs):
            x_upper = ma_values_obs1[mask_upper_obs]
            y_upper = tan_beta_values_obs1[mask_upper_obs]
            x_smooth_upper, y_smooth_upper = smooth_curve_spline(x_upper, y_upper, s=1.0)
            graph_upper_obs1 = create_graph(x_smooth_upper, y_smooth_upper, ROOT.kRed)
            graph_upper_obs1.Draw("L SAME")
        #Draw vertical line before and after thresholds
        line_lower_obs1 = ROOT.TLine(x_lower[-1], 0.5, x_lower[-1], y_lower[-1])  
        line_lower_obs1.SetLineColor(ROOT.kRed)
        line_lower_obs1.SetLineStyle(1)
        line_lower_obs1.SetLineWidth(2)
        line_lower_obs1.Draw("SAME")
        line_upper_obs1 = ROOT.TLine(x_upper[0], 0.5, x_upper[0], y_smooth_upper[0])
        line_upper_obs1.SetLineColor(ROOT.kRed)
        line_upper_obs1.SetLineStyle(1)
        line_upper_obs1.SetLineWidth(2)
        line_upper_obs1.Draw("SAME")
    else:
        x_smooth_obs1, y_smooth_obs1 = smooth_curve_spline(ma_values_obs1, tan_beta_values_obs1, s=0.5)
        graph_obs1 = create_graph(x_smooth_obs1, y_smooth_obs1, ROOT.kRed)
        graph_obs1.Draw("L SAME")

    # Compute closest points for expected contour (where z is close to 1)
    closest_points_exp1 = {}
    for i, (ma, z_value) in enumerate(zip(x_mmtt_boosted_exp_total, z_exp_array)):
        if abs(z_value - 1) < 1:
            tan_beta_val = tan_beta[i]
            diff_from_1 = abs(z_value - 1)
            if ma not in closest_points_exp1 or diff_from_1 < closest_points_exp1[ma][1]:
                closest_points_exp1[ma] = (tan_beta_val, diff_from_1)
    
    # Prepare arrays of m_a and tan_beta for the expected contour
    ma_values_exp1 = np.array(list(closest_points_exp1.keys()))
    tan_beta_values_exp1 = np.array([closest_points_exp1[ma][0] for ma in ma_values_exp1])
    sorted_exp1_pairs = sorted(zip(ma_values_exp1, tan_beta_values_exp1))
    if sorted_exp1_pairs:
        ma_values_exp1, tan_beta_values_exp1 = zip(*sorted_exp1_pairs)
        ma_values_exp1 = np.array(ma_values_exp1)
        tan_beta_values_exp1 = np.array(tan_beta_values_exp1)
    else:
        ma_values_exp1 = np.array([])
        tan_beta_values_exp1 = np.array([])

    # For model 2, force segmentation at m_a = 11 and plot both segments for expected contour
     #For model 4, force segmentation at m_a = 4 and plot both segments (before and after 4)
    if args.model == 2:
        # Compute separate masks for expected contour
        mask_lower_exp = ma_values_exp1 <= 10.8
        mask_upper_exp = ma_values_exp1 > 10.82
        # Plot expected segment with m_a <= 11
        if np.any(mask_lower_exp):
            x_lower = ma_values_exp1[mask_lower_exp]
            y_lower = tan_beta_values_exp1[mask_lower_exp]
            x_smooth_lower, y_smooth_lower = smooth_curve_spline(x_lower, y_lower, s=0.5)
            graph_lower_exp1 = create_graph_exp(x_smooth_lower, y_smooth_lower, ROOT.kRed)
            graph_lower_exp1.Draw("L SAME")
        # Plot expected segment with m_a > 11
        if np.any(mask_upper_exp):
            x_upper = ma_values_exp1[mask_upper_exp]
            y_upper = tan_beta_values_exp1[mask_upper_exp]
            x_smooth_upper, y_smooth_upper = smooth_curve_spline(x_upper, y_upper, s=0.5)
            graph_upper_exp1 = create_graph_exp(x_smooth_upper, y_smooth_upper, ROOT.kRed)
            graph_upper_exp1.Draw("L SAME")
        #Draw vertical line before and after thresholds
        line_lower_exp1 = ROOT.TLine(x_lower[-1], y_lower[-1], x_lower[-1], 5)
        line_lower_exp1.SetLineColor(ROOT.kRed)
        line_lower_exp1.SetLineStyle(7)
        line_lower_exp1.SetLineWidth(2)
        line_lower_exp1.Draw("SAME")
        line_upper_exp1= ROOT.TLine(x_upper[0], y_smooth_upper[0]+0.05, x_upper[0], 5)
        line_upper_exp1.SetLineColor(ROOT.kRed)
        line_upper_exp1.SetLineStyle(7)
        line_upper_exp1.SetLineWidth(2)
        line_upper_exp1.Draw("SAME")
    elif args.model == 4:
        # Compute separate masks for expected contour
        mask_lower_exp = ma_values_exp1 <= 4.075
        mask_upper_exp = ma_values_exp1 > 4.1
        # Plot expected segment with m_a <= 4.0
        if np.any(mask_lower_exp):
            x_lower = ma_values_exp1[mask_lower_exp]
            y_lower = tan_beta_values_exp1[mask_lower_exp]
            x_smooth_lower, y_smooth_lower = smooth_curve_spline(x_lower, y_lower, s=1.0)
            graph_lower_exp1 = create_graph_exp(x_smooth_lower, y_smooth_lower, ROOT.kRed)
            graph_lower_exp1.Draw("L SAME")
        # Plot expected segment with m_a > 4.1
        if np.any(mask_upper_exp):
            x_upper = ma_values_exp1[mask_upper_exp]
            y_upper = tan_beta_values_exp1[mask_upper_exp]
            x_smooth_upper, y_smooth_upper = smooth_curve_spline(x_upper, y_upper, s=1.0)
            graph_upper_exp1 = create_graph_exp(x_smooth_upper, y_smooth_upper, ROOT.kRed)
            graph_upper_exp1.Draw("L SAME")
    else:
        x_smooth_exp1, y_smooth_exp1 = smooth_curve_spline(ma_values_exp1, tan_beta_values_exp1, s=0.5)
        graph_exp1 = create_graph_exp(x_smooth_exp1, y_smooth_exp1, ROOT.kRed)
        graph_exp1.Draw("L SAME")

    # (Similar blocks for observed/expected values close to 0.16 follow...)

    # Observed values close to 0.16
    closest_points_obs16 = {}
    for i, (ma, z_value) in enumerate(zip(x_mmtt_boosted_obs_total, z_obs_array)):
        if abs(z_value - 0.16) < 0.5:
            tan_beta_val = tan_beta[i]
            diff_from_16 = abs(z_value - 0.16)
            if ma not in closest_points_obs16 or diff_from_16 < closest_points_obs16[ma][1]:
                closest_points_obs16[ma] = (tan_beta_val, diff_from_16)
    ma_values_obs16 = np.array(list(closest_points_obs16.keys()))
    tan_beta_values_obs16 = np.array([closest_points_obs16[ma][0] for ma in ma_values_obs16])
    sorted_obs16_pairs = sorted(zip(ma_values_obs16, tan_beta_values_obs16))
    if sorted_obs16_pairs:
        ma_values_obs16, tan_beta_values_obs16 = zip(*sorted_obs16_pairs)
        ma_values_obs16 = np.array(ma_values_obs16)
        tan_beta_values_obs16 = np.array(tan_beta_values_obs16)
    else:
        ma_values_obs16 = np.array([])
        tan_beta_values_obs16 = np.array([])

    if args.model == 2:
        mask_lower_obs16 = ma_values_obs16 <= 10.6
        mask_upper_obs16 = ma_values_obs16 > 10.82 
        if np.any(mask_lower_obs16):
            x_lower = ma_values_obs16[mask_lower_obs16]
            y_lower = tan_beta_values_obs16[mask_lower_obs16]
            x_smooth_lower, y_smooth_lower = smooth_curve_spline(x_lower, y_lower, s=0.5)
            graph_lower_obs16 = create_graph(x_smooth_lower, y_smooth_lower, ROOT.kGreen+2)
            graph_lower_obs16.Draw("L SAME")
        if np.any(mask_upper_obs16):
            x_upper = ma_values_obs16[mask_upper_obs16]
            y_upper = tan_beta_values_obs16[mask_upper_obs16]
            x_smooth_upper, y_smooth_upper = smooth_curve_spline(x_upper, y_upper, s=0.5)
            graph_upper_obs16 = create_graph(x_smooth_upper, y_smooth_upper, ROOT.kGreen+2)
            graph_upper_obs16.Draw("L SAME")
        # Draw vertical line before and after thresholds
        line_lower_obs16 = ROOT.TLine(x_lower[-1], y_lower[-1], x_lower[-1], 5)
        line_lower_obs16.SetLineColor(ROOT.kGreen+2)
        line_lower_obs16.SetLineStyle(1)
        line_lower_obs16.SetLineWidth(2)
        line_lower_obs16.Draw("SAME")
        line_upper_obs16 = ROOT.TLine(x_upper[0], y_smooth_upper[0], x_upper[0], 5)
        line_upper_obs16.SetLineColor(ROOT.kGreen+2)
        line_upper_obs16.SetLineStyle(1)
        line_upper_obs16.SetLineWidth(2)
        line_upper_obs16.Draw("SAME")
    elif args.model == 4:
        mask_lower_obs16 = ma_values_obs16 <= 4.075
        mask_upper_obs16 = ma_values_obs16 > 4.1
        if np.any(mask_lower_obs16):
            x_lower = ma_values_obs16[mask_lower_obs16]
            y_lower = tan_beta_values_obs16[mask_lower_obs16]
            x_smooth_lower, y_smooth_lower = smooth_curve_spline(x_lower, y_lower, s=0.5)
            graph_lower_obs16 = create_graph(x_smooth_lower, y_smooth_lower, ROOT.kGreen+2)
            graph_lower_obs16.Draw("L SAME")
        if np.any(mask_upper_obs16):
            x_upper = ma_values_obs16[mask_upper_obs16]
            y_upper = tan_beta_values_obs16[mask_upper_obs16]
            x_smooth_upper, y_smooth_upper = smooth_curve_spline(x_upper, y_upper, s=0.5)
            graph_upper_obs16 = create_graph(x_smooth_upper, y_smooth_upper, ROOT.kGreen+2)
            graph_upper_obs16.Draw("L SAME")
        # Draw vertical line before and after thresholds
        line_lower_obs16 = ROOT.TLine(x_lower[-1], 0.5 , x_lower[-1], y_lower[-1])
        line_lower_obs16.SetLineColor(ROOT.kGreen+2)
        line_lower_obs16.SetLineStyle(1)
        line_lower_obs16.SetLineWidth(2)
        line_lower_obs16.Draw("SAME")
        line_upper_obs16 = ROOT.TLine(x_upper[0], 0.5, x_upper[0], y_smooth_upper[0])
        line_upper_obs16.SetLineColor(ROOT.kGreen+2)
        line_upper_obs16.SetLineStyle(1)
        line_upper_obs16.SetLineWidth(2)
        line_upper_obs16.Draw("SAME")
    else:
        x_smooth_obs16, y_smooth_obs16 = smooth_curve_spline(ma_values_obs16, tan_beta_values_obs16, s=0.5)
        graph_obs16 = create_graph(x_smooth_obs16, y_smooth_obs16, ROOT.kGreen+2)
        graph_obs16.Draw("L SAME")

    # Expected values close to 0.16
    closest_points_exp16 = {}
    for i, (ma, z_value) in enumerate(zip(x_mmtt_boosted_exp_total, z_exp_array)):
        if abs(z_value - 0.16) < 0.5:
            tan_beta_val = tan_beta[i]
            diff_from_16 = abs(z_value - 0.16)
            if ma not in closest_points_exp16 or diff_from_16 < closest_points_exp16[ma][1]:
                closest_points_exp16[ma] = (tan_beta_val, diff_from_16)
    ma_values_exp16 = np.array(list(closest_points_exp16.keys()))
    tan_beta_values_exp16 = np.array([closest_points_exp16[ma][0] for ma in ma_values_exp16])
    sorted_exp16_pairs = sorted(zip(ma_values_exp16, tan_beta_values_exp16))
    if sorted_exp16_pairs:
        ma_values_exp16, tan_beta_values_exp16 = zip(*sorted_exp16_pairs)
        ma_values_exp16 = np.array(ma_values_exp16)
        tan_beta_values_exp16 = np.array(tan_beta_values_exp16)
    else:
        ma_values_exp16 = np.array([])
        tan_beta_values_exp16 = np.array([])

    if args.model == 2:
        mask_lower_exp16 = ma_values_exp16 <= 10.8
        mask_upper_exp16 = ma_values_exp16 > 10.82
        if np.any(mask_lower_exp16):
            x_lower = ma_values_exp16[mask_lower_exp16]
            y_lower = tan_beta_values_exp16[mask_lower_exp16]
            x_smooth_lower, y_smooth_lower = smooth_curve_spline(x_lower, y_lower, s=0.5)
            graph_lower_exp16 = create_graph_exp(x_smooth_lower, y_smooth_lower, ROOT.kGreen+2)
            graph_lower_exp16.Draw("L SAME")
        if np.any(mask_upper_exp16):
            x_upper = ma_values_exp16[mask_upper_exp16]
            y_upper = tan_beta_values_exp16[mask_upper_exp16]
            x_smooth_upper, y_smooth_upper = smooth_curve_spline(x_upper, y_upper, s=0.5)
            graph_upper_exp16 = create_graph_exp(x_smooth_upper, y_smooth_upper, ROOT.kGreen+2)
            graph_upper_exp16.Draw("L SAME")
        # Draw vertical line before and after thresholds
        line_lower_exp16 = ROOT.TLine(x_lower[-1], y_lower[-1], x_lower[-1], 5)
        line_lower_exp16.SetLineColor(ROOT.kGreen+2)
        line_lower_exp16.SetLineStyle(7)
        line_lower_exp16.SetLineWidth(2)
        line_lower_exp16.Draw("SAME")
    elif args.model == 4:
        mask_lower_exp16 = ma_values_exp16 <= 4.075
        mask_upper_exp16 = ma_values_exp16 > 4.1
        if np.any(mask_lower_exp16):
            x_lower = ma_values_exp16[mask_lower_exp16]
            y_lower = tan_beta_values_exp16[mask_lower_exp16]
            x_smooth_lower, y_smooth_lower = smooth_curve_spline(x_lower, y_lower, s=1.0)
            graph_lower_exp16 = create_graph_exp(x_smooth_lower, y_smooth_lower, ROOT.kGreen+2)
            graph_lower_exp16.Draw("L SAME")
        if np.any(mask_upper_exp16):
            x_upper = ma_values_exp16[mask_upper_exp16]
            y_upper = tan_beta_values_exp16[mask_upper_exp16]
            x_smooth_upper, y_smooth_upper = smooth_curve_spline(x_upper, y_upper, s=1.0)
            graph_upper_exp16 = create_graph_exp(x_smooth_upper, y_smooth_upper, ROOT.kGreen+2)
            graph_upper_exp16.Draw("L SAME")
    else:
        x_smooth_exp16, y_smooth_exp16 = smooth_curve_spline(ma_values_exp16, tan_beta_values_exp16, s=0.5)
        graph_exp16 = create_graph_exp(x_smooth_exp16, y_smooth_exp16, ROOT.kGreen+2)
        graph_exp16.Draw("L SAME")


    # Add legend
    if args.model == 3:
        leg0_ = ROOT.TLegend(0.51, 0.58, 0.82, 0.88)
        leg0_.SetBorderSize(0)
        leg0_.SetTextSize(0.03)
        leg0_.SetFillColor(ROOT.kWhite)
        leg0_.SetHeader("95% CL upper limits", 'L')
        leg0_.AddEntry(graph_exp1, "#splitline{Expected exclusion}{B(H#rightarrow aa) = 1.0}", "L")
        leg0_.AddEntry(graph_obs1, "#splitline{Observed exclusion}{B(H#rightarrow aa) = 1.0}", "LF")
        leg0_.AddEntry(graph_exp16, "#splitline{Expected exclusion}{B(H#rightarrow aa) = 0.16}", "L")
        leg0_.AddEntry(graph_obs16, "#splitline{Observed exclusion}{B(H#rightarrow aa) = 0.16}", "L")
        leg0_.Draw("same")
    else:
        leg0_ = ROOT.TLegend(0.51+0.05, 0.58, 0.82+0.018, 0.88)
        leg0_.SetBorderSize(0)
        leg0_.SetTextSize(0.03)
        leg0_.SetFillColor(ROOT.kWhite)
        leg0_.SetHeader("95% CL upper limits", 'L')
        leg0_.AddEntry(graph_lower_exp1, "#splitline{Expected exclusion}{B(H#rightarrow aa) = 1.0}", "L")
        leg0_.AddEntry(graph_lower_obs1, "#splitline{Observed exclusion}{B(H#rightarrow aa) = 1.0}", "LF")
        leg0_.AddEntry(graph_lower_exp16, "#splitline{Expected exclusion}{B(H#rightarrow aa) = 0.16}", "L")
        leg0_.AddEntry(graph_lower_obs16, "#splitline{Observed exclusion}{B(H#rightarrow aa) = 0.16}", "L")
        leg0_.Draw("same")

    canv.Update()
    canv.SaveAs(f"./Plots/Contour_Plots/Updated_limits/NewScale-2HDM+S_{typestring}_H{Hmass}_obs.png")
    canv.SaveAs(f"./Plots/Contour_Plots/Updated_limits/NewScale-2HDM+S_{typestring}_H{Hmass}_obs.pdf")
