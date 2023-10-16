import ROOT 
from ROOT import TFile, gDirectory, TCanvas, TH1D, TColor, TGraphErrors, TMath, TLatex
from ROOT import TH2D

import numpy as np

from larlite import larlite

# larlite i/o
#ioll = larlite.storage_manager( larlite.storage_manager.kREAD )
#ioll.add_in_filename("/cluster/tufts/wongjiradlabnu/nutufts/data/ntuples/dlgen2_reco_v2me05_ntuple_v0_mcc9_v29e_dl_run3b_bnb_nu_overlay_nocrtremerge.root")
#ioll.open()
#ll_nentries = ioll.get_entries()

f = TFile("/cluster/tufts/wongjiradlabnu/nutufts/data/ntuples/dlgen2_reco_v2me05_ntuple_v0_mcc9_v29e_dl_run3b_bnb_nu_overlay_nocrtremerge.root","READ")
t = f.Get("EventTree")
t_pot = f.Get("potTree")

entries = t.GetEntries()
print("This is how many entries this ntuple file has: ", entries)

finalList = []
pRest = 0.938272 # proton rest mass in GeV

# items to plot
lProtonMom = []
pionMom = []
muonMom = []

lProtonAng = []
pionAng = []
muonAng = []

weights = []

# returns momentum & angle
def momAngleCalc(px, py, pz): # assumes wrt beam, which is (0, 0, 1)

    mag = np.sqrt( px**2 + py**2 + pz**2 )
    cosTheta = pz / mag 
    return mag, cosTheta

potSum = 0.
for i in range( t_pot.GetEntries() ):
  t_pot.GetEntry(i)
  print("This is event ", i, ", POT is ", t_pot.totGoodPOT)
  potSum = potSum + t_pot.totGoodPOT

print("The total POT here is: ", potSum)

for e in range(entries):

    t.GetEntry(e)
    
    #if (t.run != 14121 or t.subrun != 239 or t.event != 11975):
    #     continue

    print("This is event number: ", e)
    print("This is the run number: ", t.run )
    print("This is the subrun number: ", t.subrun )
    print("This is the event number: ", t.event )

    # looking at "truePrimPart" variables in ntuple
    # these correspond to truth clusters with process = primary

    n = t.nTruePrimParts # how many primary clusters are in the event?
    print("There are ", n, " clusters in this event.")

    # we need at least 1 proton, exctly 1 muon, and exactly 1 pion
    if ( n < 3): 
        print("n < 3. Skipping event.")
        continue

    flag = 0
    pions = 0
    muons = 0
    protons = 0
    #KEs_P = []
    NMomsP = []

    leadingMomP = -999
    leadingAngP = -999
    
    leadingMomMu = -999
    leadingAngMu = -999

    leadingMomPi = -999
    leadingAngPi = -999

    # number of particles above threshold
    protonsN = 0 
    muonsN = 0
    pionsN = 0

    # loop through clusters in event
    for i in range(n):

        pdg = t.truePrimPartPDG[i]
        print("The pdg here is: ", pdg)

        # are any pids NOT a pion, muon, proton or neutron? 
        # if so, flag. event will be skipped
        if (pdg != -211 and pdg != 211 and pdg != 2212 and pdg != 2112 and pdg != 13):
            print("This PRIMARY particle is NOT a charged pion, mu, proton, or neutron! Skip event.")
            flag = 1
            break
        
        # Now looking at the pions. Skip event if > 1 pion. 
        # Also skip if pion energy < 70 MeV/c. 
        if (pdg == 211 or pdg == -211): 
            print("Found pion.")
            pions = pions + 1

            if (pions > 1):
                print("More than 1 pion! Skipping event.")
                flag = 1
                break

            pxPi = t.truePrimPartPx[i]
            pyPi = t.truePrimPartPy[i]
            pzPi = t.truePrimPartPz[i]
            #piEnergy = t.truePrimPartE[i]
            momPi, angPi = momAngleCalc( pxPi, pyPi, pzPi )
            print("Mom Pi is: ", momPi)
            print("Ang Pi is: ", angPi)

            print("Does this pion have at least momentum 70 MeV/c (0.07 GeV/c)?")
            if (momPi > 0.07):
                print("Pi mom is > 0.07 GeV/c. It is: ", momPi, " GeV/c. Incrementing number of N pions.")
                pionsN = pionsN + 1
                leadingMomPi = momPi
                leadingAngPi = angPi

            if (pionsN > 1):
                print("More than 1 pion that meets threshold! Skipping event.")
                flag = 1
                break

        # Looking at muons
        if (pdg == 13): # mu 
            print("Found muon.")
            muons = muons + 1
            
            #energyMu = t.truePrimPartE[i]
            pxMu = t.truePrimPartPx[i]
            pyMu = t.truePrimPartPy[i]
            pzMu = t.truePrimPartPz[i]
            momMu, angMu = momAngleCalc( pxMu, pyMu, pzMu )
            print("Mom Mu is: ", momMu)
            print("Ang Mu is: ", angMu)

            print("Does this muon meet the momentum threshold (max 1.5 GeV)?")
            if ( momMu < 1.5 ):
                print("Yes, it is under 1.5 GeV. Incrementing number of N muons.")
                muonsN = muonsN + 1
                leadingMomMu = momMu
                leadingAngMu = angMu

            if (muonsN > 1):
                print("More than 1 muon that meets threshold! Skipping event.")
                flag = 1
                break
    
        # Now look at protons
        if (pdg == 2212):
            print("Found proton.")
            protons = protons + 1 
            #energyP = t.truePrimPartE[i]
            #print("The proton energy is: ", energyP)
            #KE_P = energyP - pRest
            #print("The proton's kinetic energy is: ", KE_P)
            pxP = t.truePrimPartPx[i]
            pyP = t.truePrimPartPy[i]
            pzP = t.truePrimPartPz[i]
            momP, angP = momAngleCalc( pxP, pyP, pzP )
            print("Mom P is: ", momP)
            print("Ang P is: ", angP)

            print("Does this proton meet the momentum threshold?")
            if ( momP > 0.30 and momP < 1.0 ):
                print("Yes, appending to list of N proton moms.")
                NMomsP.append(momP) # list of N protons in the event
                protonsN = protonsN + 1
                #KEs_P.append(KE_P)

                print("Is this the leading proton?")
                if ( momP == max(NMomsP) ):
                    print("Yes. Updating mom and ang.")
                    leadingMomP = momP
                    leadingAngP = angP 

            else: 
                print("NO. The p mom was ", momP, "which is either < 0.3 GeV or > 1 GeV")

    print("This is the flag for this event: ", flag)
    if (flag == 1): 
        print("Flag == 1, meaning something didn't meet requirements. Skip event.")
        continue

    print("In this event, there were ", protons, " number of primary protons.")
    print("And ", protonsN, " protons were above threshold.")

    print("In this event, there were ", muons, " number of primary muons.")
    print("And ", muonsN, " muons were above threshold.")

    print("In this event, there were ", pions, " number of primary pions.")
    print("And ", pionsN, " pions were above threshold.")

    # require 
    if ( pionsN == 0 ): 
        print("Zero pions above threshold. Skip to next event.")
        continue

    # we need at least one proton that passes cuts in my selection
    if ( protonsN < 1 ): 
        print("Zero protons above threshold. Skip to next event.")
        continue

    # only want 1 muon in my selection
    if ( muonsN == 0 ): 
        print("Zero muons that meet threshold. Skip to next event.")
        continue
    
    print("This is the energies for each proton: ", NMomsP)
    #print("Sum of energies for this event: ", sum(NMomsP))
    #print("This is the KE for each proton: ", KEs_P)
    #print("This is the sum of KE for all protons: ", sum(KEs_P))

    #if (sum(NMomsP) > 0.30) and (sum(KEs_P) > 0.045):  
    print("If got to this point, this means the event wasn't skipped.")
    print("Filling lists...")
    finalList.append(e)
    pionMom.append( leadingMomPi*1000 )
    pionAng.append( leadingAngPi )
    muonMom.append( leadingMomMu*1000 )
    muonAng.append( leadingAngMu )
    lProtonMom.append ( leadingMomP*1000 )
    lProtonAng.append ( leadingAngP )
    weights.append( t.xsecWeight )

    #if (sum(NMomsP) > 300) and (sum(KEs_P) > 45): 
    #    finalList.append(e) # passed all cuts!

    #if pions==1: 
    #    pionEntries.append(e)

'''
print("Final List: ", finalList)
print("pionMom: ", pionMom)
print("pionAng: ", pionAng)
print("muonMom: ", muonMom)
print("muonAng: ", muonAng)
print("lpMom: ", lProtonMom)
print("lpAng: ", lProtonAng)
'''


print("Here are the final lists and their sizes (momentum in MeV/c)")

print("lProtonMom: ", lProtonMom, " with a size of: ", len(lProtonMom)) 
print("muonMom: ", muonMom, " with a size of: ", len(muonMom)) 
print("pionMom: ", pionMom, " with a size of: ", len(pionMom)) 

print("muonAng: ", muonAng, " with a size of: ", len(muonAng)) 
print("pionAng: ", pionAng, " with a size of: ", len(pionAng)) 
print("lProtonAng: ", lProtonAng, " with a size of: ", len(lProtonAng)) 

np.savetxt('ntuple_lProtonMom_101523.csv', lProtonMom, delimiter=',')
np.savetxt('ntuple_muonMom_101523.csv', muonMom, delimiter=',')
np.savetxt('ntuple_pionMom_101523.csv', pionMom, delimiter=',')

np.savetxt('ntuple_muonAng_101523.csv', muonAng, delimiter=',')
np.savetxt('ntuple_pionAng_101523.csv', pionAng, delimiter=',')
np.savetxt('ntuple_lProtonAng_101523.csv', lProtonAng, delimiter=',')

np.savetxt('ntuple_weights_101523.csv', weights, delimiter=',')

'''
    # if >1 pion in event, will skip
    if (pions > 1): 
        print("More than one pion. Flag.")
        flag = 1

    if (flag == 1):
        print("This event was flagged and so will be skipped.")
        continue
'''


        #px = t.truePrimPartPx[0]
        #print("Ths is the px: ", px)

