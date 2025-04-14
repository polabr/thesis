import ROOT as rt
import numpy as np

rt.gStyle.SetOptStat(0)

output_file = rt.TFile("histograms4.root", "RECREATE")

# # Define histogram names and titles
# histogram_definitions = {
#     "h_trueAndReco_deg": ("Reco Neutrino Energy (deg)", 10, 0, 180),
#     "h_trueAndReco_mom": ("Reco Neutrino Momentum", 10, 0, 1000),
#     "h_true": ("True", 10, 0, 180),
#     "h_reco": ("Reco", 10, 0, 180),
#     "h_reco_cosmics": ("Reco Cosmics", 10, 0, 180)
# }

# # Create histograms using a loop
# for name, (title, bins, xmin, xmax) in histogram_definitions.items():
#     histograms[name] = rt.TH1F(name, title, bins, xmin, xmax)

# # Create multiple versions of h_trueAndReco_[name]
# for suffix in ["A", "B", "C", "D", "E", "F"]:
#     hist_name = f"h_trueAndReco_{suffix}"
#     histograms[hist_name] = rt.TH1F(hist_name, f"Reco Neutrino Energy {suffix}", 10, 0, 180)


h_trueAndReco_delAlphaT = rt.TH1F("h_trueAndReco_delAlphaT","trueAndReco delAlphaT",10, 0, 180)
h_trueAndReco_delAlphaT.SetFillColor(rt.kBlue)
h_trueAndReco_pN = rt.TH1F("h_trueAndReco_pN","truAndReco pN",100, 0, 2)
h_trueAndReco_pN.SetFillColor(rt.kBlue)

h_true = rt.TH1F("h_true","True",10, 0, 180)

h_reco_delAlphaT = rt.TH1F("h_reco_delAlphaT","Reco delAlphaT",10, 0, 180)
h_reco_pN = rt.TH1F("h_reco_pN","Reco pN",100, 0, 2)

h_reco_delAlphaT_cosmics = rt.TH1F("h_reco_delAlphaT_cosmics","Reco Cosmics delAlphaT",10, 0, 180)
h_reco_delAlphaT_cosmics.SetFillColor(rt.kRed)
h_reco_pN_cosmics = rt.TH1F("h_reco_pN_cosmics","Reco Cosmics pN",100, 0, 2)


f = rt.TFile("selectedEventsTrueRecoBoth_fullSel_withTKI_011625.root","READ") # full sel with TKI
t = f.Get("selectedEvents")
entries = t.GetEntries()

f2 = rt.TFile("selectedEventsTrueRecoBoth_cosmics_fixed_120224.root","READ")
t2 = f2.Get("selectedEvents")
entries2 = t2.GetEntries()

output_file.cd()

completeness = 0.5

# for calculating the total purity and efficiencies later
sum_overlay_weights_both_list = []
sum_overlay_weights_selected_list = []

n_neutrino_both = 0.0
n_neutrino_sel = 0.0 # reco
n_neutrino_sig = 0.0 # truth

for e in range(entries):

    t.GetEntry(e)
    
    if (t.passedSel_ == 1) or (t.passedSel_ == 3): # passes truth selection
        h_true.Fill((t.recoSel_delAlphaT_)*180/np.pi, t.weight_)
        n_neutrino_sig += t.weight_
        if (t.passedSel_ == 2) or (t.passedSel_ == 3): # passes reco selection as well (so both selections)
            if (t.recoSel_recoContained_==2):
            #if (t.recoSel_recoContained_==2) and (t.recoSel_trackCompMu_ > completeness) and (t.recoSel_trackCompPi_ > completeness) and (t.recoSel_trackCompP_ > completeness):
                h_trueAndReco_delAlphaT.Fill((t.recoSel_delAlphaT_)*180/np.pi, t.weight_)
                h_trueAndReco_pN.Fill(t.recoSel_pN_, t.weight_)
                sum_overlay_weights_both_list.append(t.weight_)
                n_neutrino_both += t.weight_
    if (t.passedSel_ == 2) or (t.passedSel_ == 3): # passes reco selection
        if (t.recoSel_recoContained_==2):
        #if (t.recoSel_recoContained_==2) and (t.recoSel_trackCompMu_ > completeness) and (t.recoSel_trackCompPi_ > completeness) and (t.recoSel_trackCompP_ > completeness):
            h_reco_delAlphaT.Fill((t.recoSel_delAlphaT_)*180/np.pi, t.weight_)
            h_reco_pN.Fill(t.recoSel_pN_, t.weight_)
            sum_overlay_weights_selected_list.append(t.weight_)
            n_neutrino_sel += t.weight_

targetPOT = 1.3e21 # total expected POT for runs 1-5 in MicroBooNE
simPOT = 4.68e20 # this is for run 1
n_neutrino_sel *= targetPOT/simPOT
n_neutrino_both *= targetPOT/simPOT
n_neutrino_sig *= targetPOT/simPOT
print(n_neutrino_sel)
print(n_neutrino_both)
print(n_neutrino_sig)

# cosmics looop (reco only)

# for calculating the total purity later
cosmics_counter = 0

for e in range(entries2):

    t2.GetEntry(e)
    
    if (t2.passedSel_ == 2) or (t2.passedSel_ == 3): # passes reco selection
        if (t.recoSel_recoContained_==2):
        #if (t.recoSel_recoContained_==2) and (t.recoSel_trackCompMu_ > completeness) and (t.recoSel_trackCompPi_ > completeness) and (t.recoSel_trackCompP_ > completeness):
            h_reco_delAlphaT_cosmics.Fill((t2.recoSel_delAlphaT_)*180/np.pi)
            h_reco_pN_cosmics.Fill(t2.recoSel_pN_)
            cosmics_counter = cosmics_counter + 1

targetPOT = 1.3e21 # total expected POT for runs 1-5 in MicroBooNE
simPOT = 4.68e20 # this is for run 1
simPOT_cosmics = 3.297e20 # this is for run 1 EXTBNB
cosmics_counter *= targetPOT/simPOT_cosmics
print(cosmics_counter)

h_trueAndReco_delAlphaT.Scale(targetPOT/simPOT)
h_trueAndReco_pN.Scale(targetPOT/simPOT)
h_reco_delAlphaT.Scale(targetPOT/simPOT)
h_reco_pN.Scale(targetPOT/simPOT)
h_true.Scale(targetPOT/simPOT)

h_reco_delAlphaT_cosmics.Scale(targetPOT/simPOT_cosmics)
h_reco_pN_cosmics.Scale(targetPOT/simPOT_cosmics)

all_sel = n_neutrino_sel + cosmics_counter
print(all_sel)

h_sel_all = h_reco_delAlphaT + h_reco_delAlphaT_cosmics


h_nonsignal_delAlphaT = h_reco_delAlphaT - h_trueAndReco_delAlphaT
h_nonsignal_pN = h_reco_pN - h_trueAndReco_pN

# Create dictionaries to store the histograms and canvases
histograms = {}
canvases = {}

# Define the names and titles for the histograms
histogram_info = [
    ("h_stacked_delAlphaT", "delAlphaT"),
    ("h_stacked_pN", "pN")
]

# Create the histograms and canvases and store them in the dictionaries
for name, title in histogram_info:
    histograms[name] = rt.THStack(name, title)
    canvases[name] = rt.TCanvas(f"c_{name}", title, 800, 600)

# Add histograms to the stacks
histograms["h_stacked_delAlphaT"].Add(h_nonsignal_delAlphaT, "hist")
histograms["h_stacked_delAlphaT"].Add(h_reco_delAlphaT_cosmics, "hist")
histograms["h_stacked_delAlphaT"].Add(h_trueAndReco_delAlphaT, "hist")

histograms["h_stacked_pN"].Add(h_nonsignal_pN, "hist")
histograms["h_stacked_pN"].Add(h_reco_pN_cosmics, "hist")
histograms["h_stacked_pN"].Add(h_trueAndReco_pN, "hist")

# Create canvases and draw the histograms
for name, title in histogram_info:

    canvas = canvases[name]
    canvas.cd()

    histograms[name].Draw("hist")
    histograms[name].GetXaxis().SetTitle(f"{title} (deg)")
    histograms[name].GetYaxis().SetTitle("Events")
    
    # Create a legend
    legend = rt.TLegend(0.7, 0.7, 0.9, 0.9)


    if name == "h_stacked_delAlphaT":
        legend.AddEntry(h_nonsignal_delAlphaT, "Non-signal delAlphaT", "f")
        legend.AddEntry(h_reco_delAlphaT_cosmics, "Reco delAlphaT Cosmics", "f")
        legend.AddEntry(h_trueAndReco_delAlphaT, "True and Reco delAlphaT", "f")
    elif name == "h_stacked_pN":
        legend.AddEntry(h_nonsignal_pN, "Non-signal pN", "f")
        legend.AddEntry(h_reco_pN_cosmics, "Reco pN Cosmics", "f")
        legend.AddEntry(h_trueAndReco_pN, "True and Reco pN", "f")
    
    histograms[name].GetHistogram().GetListOfFunctions().Add(legend)

    legend.Draw()

    canvas.Draw()
    canvas.SaveAs(f"{name}.png")  # Save the canvas as an image file

    canvas.Write()

# Write each histogram to the ROOT file
#for name in histograms:
#    histograms[name].Write()

# Close the ROOT file
output_file.Close()