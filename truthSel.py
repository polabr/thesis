import ROOT 
from ROOT import TFile, gDirectory, TCanvas, TH1D, TColor, TGraphErrors, TMath, TLatex
from ROOT import TH2D

import numpy as np

from larlite import larlite

# larlite i/o
ioll = larlite.storage_manager( larlite.storage_manager.kREAD )
ioll.add_in_filename("/cluster/tufts/wongjiradlab/larbys/data/mcc9/mcc9_v29e_dl_run3b_bnb_nu_overlay_nocrtremerge/data/00/01/41/21/merged_dlreco_06ae2262-83dc-4375-a9a6-e74e63f55849.root")
ioll.open()

ll_nentries = ioll.get_entries()

pionEntries = []

# loop over each event 
for i in range(ll_nentries):

    print("Going to event #: ", i)
    ioll.go_to(i)

    ev_mctrack = ioll.get_data(larlite.data.kMCTrack,"mcreco")
    ev_mcshower = ioll.get_data(larlite.data.kMCShower,"mcreco")

    gtruth = ioll.get_data(larlite.data.kGTruth, "generator")

    print("How many neutrino interactions are in this event?", gtruth.size())
    print("What is total number of primary pions according to GENIE?", gtruth.at(0).fNumPiPlus + gtruth.at(0).fNumPiMinus)

    # check if there is a pi0 in here
    #numPi0 = gtruth.at(0).fNumPi0
    #if (numPi0 > 0):
    #    print("There are this many pi0 in here: ", numPi0 )
    #    print("Skipping event.")
    #    continue

    numMCTracks = ev_mctrack.size()
    print("Grabbed ev_mctrack. There are ", numMCTracks, " tracks in here")

    # flag if there is some event with pdg we don't want
    flag=0

    numMCShowers = ev_mcshower.size()
    print("There are ", numMCShowers, " showers in here")
#    if (numMCShowers > 0):
#        print("Num showers nonzero. Skipping event.")
#        continue # for now, don't want any shower-like particles (?)

    pions = 0
    
    #look at PDGS of all primary tracks in event. if any are not pi, mu, p, or n, throw away event
    # also if more than 1 primary pion, throw away event
    for j in range ( numMCTracks ) :
        mctrack = ev_mctrack.at(j)
        print("This is track number: ", j)
        process = mctrack.Process()
        print("The process is: ", mctrack.Process() )
        if (process == "primary"):
            pdg = mctrack.PdgCode()
            print("PROCESS CHECK: The PDG code of this track is: ", mctrack.PdgCode() )
            if (pdg != -211 and pdg != 211 and pdg != 2212 and pdg != 2112 and pdg != 13):
                print("This PRIMARY particle is NOT a charged pion, mu, proton, or neutron!")
                flag = 1
            if (pdg == 211 or pdg == -211): 
                pions = pions + 1

    if (pions > 1): 
        print("More than one pion. Flag.")
        flag = 1
    
    if (flag == 1):
        print("This event was flagged and so will be skipped.")
        continue

    # now see if shwoers contain anything weird
    for j in range ( numMCShowers ) :
        mcshower = ev_mcshower.at(j)
        print("This is shower number: ", j)
        process = mcshower.Process()
        print("The process of this shower is: ", process)
        if mcshower.Process() == "primary":
            pdg = mcshower.PdgCode()
            print("The PDG code of this PRIMARY SHOWER is: ", mcshower.PdgCode() )
            flag = 1

    if (flag == 1):
        print("This event was flagged: ", flag)
        continue
 
    # loop over each track in event
    for j in range ( numMCTracks ) :
        mctrack = ev_mctrack.at(j)
        print("This is track number: ", j)
        pdg = mctrack.PdgCode()
        print("The PDG code of this track is: ", mctrack.PdgCode() )
        if (pdg == 211 or pdg == -211): # find charged pions first 
            print("PION FOUND!!!!!")
            print("The trackID here is: ", mctrack.TrackID())
            print("But is it primary?") # want primary ones only
            print("mctrack.Process() = ", mctrack.Process() )
            if mctrack.Process() == "primary":
                print("Yes!")
                print("The ancestorID here is: ", mctrack.AncestorTrackID())
                print("But does it at least have energy 70 MeV/c?")
                energy = mctrack.Start().E()
                print("mctrack.Start().E() = ", energy )
                if (energy > 70):
                    print("Yes!! Event #",i," added to list!")
                    pionEntries.append(i)

print("These are the surviving entries:")
print("Entries in the tree with an ev_mctrack containing a pion: ", pionEntries)
print("If an entry number appeared twice, this means there were 2 charged pion tracks in the event. Remove.")

# first check which values are duplicates

dupes = []

for i in range(1, len(pionEntries)):
    current_number = pionEntries[i]
    #print("current_number: ", current_number)
    previous_number = pionEntries[i - 1]
    #print("previous_number: ", previous_number)

    if current_number == previous_number:
        print("Duplicate found: ", current_number)
        dupes.append(current_number)
    
print("dupes: ", dupes)

for i in dupes: 
    # list comprehension to remove all instances of the dupe in the list
    pionEntries = [num for num in pionEntries if num != i] 

print("List of pion entries after dupes removed: ", pionEntries)

pRest = 938.272 # proton rest mass
finalList = []

# items to plot
lProtonMom = []
pionMom = []
muonMom = []

### PROTON LOOP ###
print("Of the remaining events (which have a charged pion and meet cuts), investigate the protons.")
for i in pionEntries: 
    
    ioll.go_to(i)
    ev_mctrack = ioll.get_data(larlite.data.kMCTrack,"mcreco")
    numMCTracks = ev_mctrack.size()

    protons = 0
    KEs_P = []
    energiesP = []

    for j in range ( numMCTracks ) :

        mctrack = ev_mctrack.at(j)
        print("This is track number: ", j)
        pdg = mctrack.PdgCode()
        print("The PDG code of this track is: ", mctrack.PdgCode() )

        if (pdg != 2212): # skip anything that's not a proton
            continue
        else:
            print("Proton found!")
            print("The process is: ", mctrack.Process())
            if mctrack.Process() == "primary":
                print("It is a primary, so keep this one.")
                protons = protons + 1 
                energyP = mctrack.Start().E()
                print("The proton energy is: ", energyP)
                KE_P = energyP - pRest
                print("The proton's kinetic energy is: ", KE_P)
                energiesP.append(energyP)
                KEs_P.append(KE_P)
            else: 
                continue 
    
    print("Now in this event, ", i, ", what is the total number of primary protons?")
    print("primary protons: ", protons)
    print("This is the energies for each proton: ", energiesP)
    print("Sum of energies for this event: ", sum(energiesP))
    print("This is the KE for each proton: ", KEs_P)
    print("This is the sum of KE for all protons: ", sum(KEs_P))

    if (sum(energiesP) > 300) and (sum(KEs_P) > 45): 
        finalList.append(i) # passed all cuts!

print("This is the final list of events: ", finalList)

# grab muon, pion momenta values of the finalized list for plotting
for i in finalList:

    print("THIS IS EVENT NUMBER: ", i)
    
    ioll.go_to(i)
    ev_mctrack = ioll.get_data(larlite.data.kMCTrack,"mcreco")
    numMCTracks = ev_mctrack.size()

    muons = 0 # need to check if there is only 1 muon
    protons = 0
    energiesP = []

    for j in range ( numMCTracks ) :

        mctrack = ev_mctrack.at(j)
        pdg = mctrack.PdgCode()
        process = mctrack.Process()



        if (process == "primary"): # only care about primary pi's/nu's

            if (pdg == 13): # mu 
                print("Found muon. PDG: ", pdg)
                energyMu = mctrack.Start().E()
                muons = muons + 1

            if (pdg == -211 or pdg == 211):
                print("Found pion. PDG: ", pdg)
                energyPi = mctrack.Start().E()

            if (pdg == 2212): # protons
                protons = protons + 1 
                energyP = mctrack.Start().E()
                energiesP.append(energyP)

    if (muons == 1):
        muonMom.append( energyMu )
        pionMom.append( energyPi )
        lProtonMom.append ( max(energiesP) )

print("Here are the final lists and their sizes.")
print("lProtonMom: ", lProtonMom, " with a size of: ", len(lProtonMom)) 
print("muonMom: ", muonMom, " with a size of: ", len(muonMom)) 
print("pionMom: ", pionMom, " with a size of: ", len(pionMom)) 

np.savetxt('lProtonMom.csv', lProtonMom, delimiter=',')
np.savetxt('muonMom.csv', muonMom, delimiter=',')
np.savetxt('pionMom.csv', pionMom, delimiter=',')

# Open the file 
#f = TFile("/cluster/tufts/wongjiradlab/larbys/data/mcc9/mcc9_v29e_dl_run3b_bnb_nu_overlay_nocrtremerge/data/00/01/41/21/merged_dlreco_06ae2262-83dc-4375-a9a6-e74e63f55849.root","READ")

# See what is inside the file
#print("Now looking inside the file: ")
#f.ls()

#print("See what variables are stored inside the tree by looking at just one entry ")
#f.MCTree.Show(0)

