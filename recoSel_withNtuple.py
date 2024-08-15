# 
# This script implements the reco selection.
#
#

import ROOT 
from ROOT import TFile, TTree

import numpy as np
from array import array

f = TFile("/cluster/tufts/wongjiradlabnu/pabrat01/gen2ntuple/outdir/dlgen2_reco_v2me06_ntuple_v5_mcc9_v28_wctagger_bnboverlay.root","READ")

t = f.Get("EventTree")
t_pot = f.Get("potTree")

# Create new .root file that will contain the result of this script
newF = TFile("selectedEventsReco_v2me06_072924_withTruth.root","recreate")
newT = TTree("selectedEvents", "Selected Events Tree") # make this file have a TTree

run_ = array('i', [0])
subrun_ = array('i', [0])
event_ = array('i', [0])
truthLProtonMom_ = array('d', [0.])
truthPionMom_ = array('d', [0.])
truthMuonMom_ = array('d', [0.])
lProtonAng_ = array('d', [0.])
pionAng_ = array('d', [0.])
muonAng_ = array('d', [0.])
pxP_ = array('d', [0.])
pyP_ = array('d', [0.])
pzP_ = array('d', [0.])
pxMu_ = array('d', [0.])
pyMu_ = array('d', [0.])
pzMu_ = array('d', [0.])
pxPi_ = array('d', [0.])
pyPi_ = array('d', [0.])
pzPi_ = array('d', [0.])
eP_ = array('d', [0.])
eMu_ = array('d', [0.])
ePi_ = array('d', [0.])
eNu_ = array('d', [0.])
pdgNu_ = array('i', [0])
#modeNu_ = array('i', [0])
#intrxnNu_ = array('i', [0])
weight_ = array('d', [0.])
recoNuE_ = array('d', [0.])
recoContained_ = array('i', [0])
recoMomPi_ = array('d', [0.])
recoMomMu_ = array('d', [0.])
recoMomP_ = array('d', [0.])
newT.Branch('run_', run_, 'run_/I')
newT.Branch('subrun_', subrun_, 'subrun_/I')
newT.Branch('event_', event_, 'event_/I')
newT.Branch('truthLProtonMom_', truthLProtonMom_, 'truthLProtonMom_/D')
newT.Branch('truthPionMom_', truthPionMom_, 'truthPionMom_/D')
newT.Branch('truthMuonMom_', truthMuonMom_, 'truthMuonMom_/D')
newT.Branch('lProtonAng_', lProtonAng_, 'lProtonAng_/D')
newT.Branch('pionAng_', pionAng_, 'pionAng_/D')
newT.Branch('muonAng_', muonAng_, 'muonAng_/D')
newT.Branch('pxP_', pxP_, 'pxP_/D')
newT.Branch('pyP_', pyP_, 'pyP_/D')
newT.Branch('pzP_', pzP_, 'pzP_/D')
newT.Branch('pxMu_', pxMu_, 'pxMu_/D')
newT.Branch('pyMu_', pyMu_, 'pyMu_/D')
newT.Branch('pzMu_', pzMu_, 'pzMu_/D')
newT.Branch('pxPi_', pxPi_, 'pxPi_/D')
newT.Branch('pyPi_', pyPi_, 'pyPi_/D')
newT.Branch('pzPi_', pzPi_, 'pzPi_/D')
newT.Branch('eP_', eP_, 'eP_/D')
newT.Branch('eMu_', eMu_, 'eMu_/D')
newT.Branch('ePi_', ePi_, 'ePi_/D')
newT.Branch('eNu_', eNu_, 'eNu_/D')
newT.Branch('pdgNu_', pdgNu_, 'pdgNu_/I')
#newT.Branch('modeNu_', modeNu_, 'modeNu_/I')
#newT.Branch('intrxnNu_', intrxnNu_, 'intrxnNu_/I')
newT.Branch('weight_', weight_, 'weight_/D')
newT.Branch('recoNuE_', recoNuE_, 'recoNuE_/D')
newT.Branch('recoContained_', recoContained_, 'recoContained_/I')
newT.Branch('recoMomPi_', recoMomPi_, 'recoMomPi_/D')
newT.Branch('recoMomMu_', recoMomMu_, 'recoMomMu_/D')
newT.Branch('recoMomP_', recoMomP_, 'recoMomP_/D')

entries = t.GetEntries()
print("This is how many entries this ntuple file has: ", entries)

newF.cd()

finalList = []

# masses in MeV
muMass = 105.66
piMass = 139.6
pMass = 938.28

# grab momentum from KE in reco
def recoMomCalc(recoE, mass):
    p = recoE + mass
    return np.sqrt( p**2 - mass**2 ) / 1000. # conversion from MeV to GeV

# returns truth momentum (from px/py/pz) & angle
def truthMomAngleCalc(px, py, pz): # assumes wrt beam, which is (0, 0, 1)
    mag = np.sqrt( px**2 + py**2 + pz**2 ) / 1000. # conversion to GeV
    cosTheta = pz / mag 
    return mag, cosTheta

potSum = 0.
for i in range( t_pot.GetEntries() ):
    t_pot.GetEntry(i)
    #print("This is event ", i, ", POT is ", t_pot.totGoodPOT)
    potSum = potSum + t_pot.totGoodPOT

print("The total POT here is: ", potSum)

#
#  LOOP THRU NTUPLES! 
#
for e in range(entries): #entries

    t.GetEntry(e)

    print("-----------------------------------------")

    print("   THIS IS ENTRY NUMBER: ", e)

    print("This is the run number: ", t.run )
    print("This is the subrun number: ", t.subrun )
    print("This is the event number: ", t.event )

    if (t.foundVertex != 1): 
        print("No vtx found. Skipping...")
        continue

    print("Vtx was found!")
    n = t.nTracks
    print("Number of reco tracks associated with the vtx: ", n)

    m = t.nTrueSimParts # how many sim clusters are in the event?

    if (n < 3): 
        print("There aren't at least 3 tracks. Skipping...")
        continue

    s = t.nShowers

    twoSecPhoCount = 0

    for i in range(s): 
        if (t.showerProcess[i] == 0): continue # skip all primary showers
        #if (t.showerProcess[i] == 1) and (t.showerPID==22): 
        #   print("Secondary photon found.")
        #   twoSecPhoCount = twoSecPhoCount + 1

    if (twoSecPhoCount > 1): continue

    # check if we have at least 3 tracks classified as primaries
    # both upstream and downstream of LArPID
    # and that at least 3 particles were classified (didn't fail reco)

    flag = 0
    pions = 0
    muons = 0
    protons = 0
    NMomsP = []

    leadingMomP = -999
    leadingAngP = -999
        
    leadingMomMu = -999
    leadingAngMu = -999

    leadingMomPi = -999
    leadingAngPi = -999

    recoMomPi = -1.0
    recoMomMu = -1.0
    recoMomP = -1.0

    pTID = -999
    piTID = -999
    muTID = -999

    # number of particles above threshold
    protonsN = 0 
    muonsN = 0
    pionsN = 0
        
    # loop through tracks
    for i in range(n):

        # first check if it's a primary (code of 0)
        if (t.trackIsSecondary[i] != 0): 
            print("Not a primary! Its code is not 0. It is: ", t.trackIsSecondary[i])
            continue
        else:
            print("Yup, it's a primary! It is: ", t.trackIsSecondary[i])

        # does LArPID think it's a primary?
        if (t.trackProcess[i] != 0): 
            print("Not a primary according to LArPID! Its code is not 0. It is: ", t.trackProcess[i])
            continue
        else:
            print("Yup, it's a primary according to LArPID too. Code: ", t.trackProcess[i])

        # LArPID PDG score
        if (t.trackClassified[i] != 1):
            print("Not classified! Its code is not 1. It is: ", t.trackClassified[i])
            continue
        else: 
            print("Yep, it was classified!")
            pdg = t.trackPID[i]
            print("Its LArPID predicted PDG score is: ", pdg)

        recoTID = t.trackTrueTID[i]

        if (pdg == 211 or pdg == -211): 

            print("Found pion.")
            pions = pions + 1

            if (pions > 1):
                print("More than 1 pion! Skipping event.")
                flag = 1
                break

            recoPiE = t.trackRecoE[i]
            print("recoPiE: ", recoPiE)
            if (recoPiE > 0): 
                recoMomPi = recoMomCalc(recoPiE, piMass)

            print("Does this pion have at least momentum 70 MeV/c (0.07 GeV/c)?")
            print("recoMomPi: ", recoMomPi)
            if (recoMomPi > 0.07):
                print("Pi mom is > 0.07 GeV/c. It is: ", recoMomPi, " GeV/c. Incrementing number of N pions.")
                pionsN = pionsN + 1
                leadingMomPi = recoMomPi

            if (pionsN > 1):
                print("More than 1 pion that meets threshold! Skipping event.")
                flag = 1
                break

            piTID = recoTID

        # Looking at muons
        if (pdg == 13): # mu 

            print("Found muon.")
            muons = muons + 1
         
            if (muons > 1):
                print("More than 1 muon! Skipping event.")
                flag = 1
                break

            recoMuE = t.trackRecoE[i]
            print("recoMuE: ", recoMuE)
            if (recoMuE > 0): 
                recoMomMu = recoMomCalc(recoMuE, muMass)

            print("Does this muon meet the momentum threshold (max 1.5 GeV)?")
            print("recoMomMu: ", recoMomMu)
            if ( recoMomMu < 1.5 ):
                print("Yes, it is under 1.5 GeV. Incrementing number of N muons.")
                muonsN = muonsN + 1
                leadingMomMu = recoMomMu

            if (muonsN > 1):
                print("More than 1 muon that meets threshold! Skipping event.")
                flag = 1
                break

            muTID = recoTID

        # Now look at protons
        if (pdg == 2212):

            print("Found proton.")
            protons = protons + 1 

            recoPE = t.trackRecoE[i]
            print("recoPE: ", recoPE)
            if (recoPE > 0): 
                recoMomP = recoMomCalc(recoPE, pMass)
            
            print("recoMomP = ", recoMomP)
            print("Does this proton meet the momentum threshold?")
            if ( recoMomP > 0.30 and recoMomP < 1.0 ):
                print("Yes, appending to list of N proton moms.")
                NMomsP.append(recoMomP) # list of N protons in the event
                protonsN = protonsN + 1

                print("Is this the leading proton?")
                if ( recoMomP == max(NMomsP) ):
                    print("Yes. Updating mom and ang.")
                    leadingMomP = recoMomP

                pTID = recoTID

            else: 
                print("NO. The p mom was ", recoMomP, "which is either < 0.3 GeV or > 1 GeV")


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

    print("If I got to this point, means the event wasn't skipped.")

    print("The TIDs were (piTID, muTID, pTID): ", piTID, ", ", muTID, ", ", pTID)

    print("recoMomPi: ", recoMomPi)
    print("recoMomMu: ", recoMomMu)
    print("recoMomP: ", recoMomP)

    truthMomPi = -1.0
    truthMomMu = -1.0
    truthMomP = -1.0

    # now look at the truth info
    for k in range(m):

        trueTID = t.trueSimPartTID[k]

        # truth pion information
        if (trueTID == piTID): 
            truePiPID = t.trueSimPartPDG[k]
            pxPi = t.trueSimPartPx[k]
            pyPi = t.trueSimPartPy[k]
            pzPi = t.trueSimPartPz[k]
            truePiE = t.trueSimPartE[k] # kinetic energy
            print("Truth Track PID: ", truePiPID)
            print("True energy: ", truePiE)
            truthMomPi, truthAngPi = truthMomAngleCalc( pxPi, pyPi, pzPi )
            #if (truePiE > 0): 
            #    trueMomPi = trueMomCalc(truePiE, piMass)
            print("This is the truth pion mom in GeV: ", truthMomPi)

        # truth muon information
        if (trueTID == muTID): 
            trueMuPID = t.trueSimPartPDG[k]
            pxMu = t.trueSimPartPx[k]
            pyMu = t.trueSimPartPy[k]
            pzMu = t.trueSimPartPz[k]
            trueMuE = t.trueSimPartE[k] # kinetic energy
            print("Truth Track PID: ", trueMuPID)
            print("True energy: ", trueMuE)
            truthMomMu, truthAngMu = truthMomAngleCalc( pxMu, pyMu, pzMu )
            #if (truePiE > 0): 
            #    trueMomPi = trueMomCalc(truePiE, piMass)
            print("This is the truth muon mom in GeV: ", truthMomMu)

        # truth leading proton information
        if (trueTID == pTID): 
            truePPID = t.trueSimPartPDG[k]
            pxP = t.trueSimPartPx[k]
            pyP = t.trueSimPartPy[k]
            pzP = t.trueSimPartPz[k]
            truePE = t.trueSimPartE[k] # kinetic energy
            print("Truth Track PID: ", truePPID)
            print("True energy: ", truePE)
            truthMomP, truthAngP = truthMomAngleCalc( pxP, pyP, pzP )
            #if (truePiE > 0): 
            #    trueMomPi = trueMomCalc(truePiE, piMass)
            print("This is the truth leading proton mom in GeV: ", truthMomP)


    print("Filling lists...")
    finalList.append(e)
    run_[0] = t.run
    subrun_[0] = t.subrun
    event_[0] = t.event
    weight_[0] = t.xsecWeight
    recoNuE_[0] = t.recoNuE
    recoContained_[0] = t.vtxContainment
    recoMomPi_[0] = leadingMomPi
    recoMomMu_[0] = leadingMomMu
    recoMomP_[0] = leadingMomP
    truthPionMom_[0] = truthMomPi
    truthMuonMom_[0] = truthMomMu
    truthLProtonMom_[0] = truthMomP
    newT.Fill()

print("Done!")

newF.Write()
newF.Close()

