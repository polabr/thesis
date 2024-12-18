# 
# This script implements the truth selection, 
# then track-ID matches the assocuated reco tracks. 
#
import ROOT 
from ROOT import TFile, TTree

import numpy as np
from array import array
import selModule

f = TFile("/cluster/tufts/wongjiradlabnu/pabrat01/gen2ntuple/outdir/dlgen2_reco_v2me06_ntuple_v5_mcc9_v28_wctagger_bnboverlay.root","READ")
#f = TFile("/cluster/tufts/wongjiradlabnu/pabrat01/gen2ntuple/outdir/reco_v2me05_gen2ntuple_bnb_nu_overlay_run3_v6.root","READ")

t = f.Get("EventTree")
t_pot = f.Get("potTree")

# Create new .root file that will contain the result of this script
newF = TFile("selectedEventsSim_v2me06_101524_withContainedVar.root","recreate")
# Make this file have a TTree
newT = TTree("selectedEvents", "Selected Events Tree")

#newT = t.CloneTree(0) # clone structure of Matt's ntuple tree
# Add variables to TTree (in Python they must be arrays to mimic C++ types)
run_ = array('i', [0])
subrun_ = array('i', [0])
event_ = array('i', [0])
lProtonMom_ = array('d', [0.])
pionMom_ = array('d', [0.])
muonMom_ = array('d', [0.])
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
trackCompMu_ = array('d', [0.])
trackCompPi_ = array('d', [0.])
trackCompP_ = array('d', [0.])
trackTrueCompMu_ = array('d', [0.])
trackTrueCompPi_ = array('d', [0.])
trackTrueCompP_ = array('d', [0.])
newT.Branch('run_', run_, 'run_/I')
newT.Branch('subrun_', subrun_, 'subrun_/I')
newT.Branch('event_', event_, 'event_/I')
newT.Branch('lProtonMom_', lProtonMom_, 'lProtonMom_/D')
newT.Branch('pionMom_', pionMom_, 'pionMom_/D')
newT.Branch('muonMom_', muonMom_, 'muonMom_/D')
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
newT.Branch('trackCompMu_', trackCompMu_, 'trackCompMu_/D')
newT.Branch('trackCompPi_', trackCompPi_, 'trackCompPi_/D')
newT.Branch('trackCompP_', trackCompP_, 'trackCompP_/D')
newT.Branch('trackTrueCompMu_', trackTrueCompMu_, 'trackTrueCompMu_/D')
newT.Branch('trackTrueCompPi_', trackTrueCompPi_, 'trackTrueCompPi_/D')
newT.Branch('trackTrueCompP_', trackTrueCompP_, 'trackTrueCompP_/D')

entries = t.GetEntries()
print("This is how many entries this ntuple file has: ", entries)


newF.cd()

lProtonAng = []

finalList = []
passedModule = []

# events I am vetoing for now
veto = np.loadtxt("allDiff.txt", dtype=float) 
veto = veto.astype(np.int64)
print("Veto'd events: ", veto) 
print("How many events?", veto.shape)

# returns momentum & angle
def momAngleCalc(px, py, pz): # assumes wrt beam, which is (0, 0, 1)
    mag = np.sqrt( px**2 + py**2 + pz**2 )
    cosTheta = pz / mag 
    return mag, cosTheta

# masses in MeV
muMass = 105.66
piMass = 139.6
pMass = 938.28

# grab momentum from KE in reco
def recoMomCalc(recoE, mass):
    p = recoE + mass
    return np.sqrt( p**2 - mass**2 )
    ####return np.sqrt( p**2 - mass**2 ) / 1000. # conversion from MeV to GeV

potSum = 0.
for i in range( t_pot.GetEntries() ):
  t_pot.GetEntry(i)
  #print("This is event ", i, ", POT is ", t_pot.totGoodPOT)
  potSum = potSum + t_pot.totGoodPOT

print("The total POT here is: ", potSum)

for e in range(entries): #entries

    t.GetEntry(e)

    print("   THIS IS ENTRY NUMBER: ", e)

    if (e in veto): 
        continue

    print("This is the run number: ", t.run )
    print("This is the subrun number: ", t.subrun )
    print("This is the event number: ", t.event )

    outModule = selModule.truthSel(t)
    if (outModule == True): 
        passedModule.append(e)

    print( selModule.truthSel(t) )

    # looking at "truePrimPart" variables in ntuple
    # these correspond to truth clusters with process = primary

    n = t.nTrueSimParts # how many sim clusters are in the event?
    m = t.nTruePrimParts # how many prim clusters are in the event?
    print("There are ", n, " sim clusters in this event.")
    print("There are ", m, " prim clusters in this event.")

    nn = t.nTracks # how many reco tracks are in the event?

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

    pTID = -999
    piTID = -999
    muTID = -999

    # number of particles above threshold
    protonsN = 0 
    muonsN = 0
    pionsN = 0

    # check if there are at least 3 primary clusters in genie
    if ( m < 3): 
        print("m < 3. Skipping event.")
        continue

    # loop through primPart clusters, skip any event with the following: 
        # an event with fewer than 3 primary tracks according to genie
        # pdg that is not a pion, muon, proton, or neutron
    for j in range(m):
        primPDG = t.truePrimPartPDG[j]
        if (primPDG != -211 and primPDG != 211 and primPDG != 2212 and primPDG != 2112 and primPDG != 13):
            print("Found an unwanted pdg! It is: ", primPDG)
            flag = 1
            print("Skipping this whole event.")
            break

    '''
    # loop through primPart clusters which have genie info for pi0's
    # is there *any* cluster in this event that is a primary pi0? if so, skip!
    for j in range(m):
        primPDG = t.truePrimPartPDG[j]
        if (primPDG == 111):
            print("Found a primary pi0! Skipping this whole event.")
            flag = 1
            break
    '''

    # loop through truth clusters in event
    for i in range(n):

        print("This is cluster #", i)

        #if (t.trueSimPartProcess[i] == 1 and pdg == 22): 
        #    print("Found a gamma.")
        #    print("Its parent particle is ")

        #print("Process is: ", t.trueSimPartProcess[i])

        # Careful!! Process == 0 is NOT necessarily a primary, can be a secondary!!!
        # so for e.g. a muon, need to match the primary lepton energy...
        # stuill want to throw away everything nonzero though
        if (t.trueSimPartProcess[i] != 0): 
            #print("Skipping cluster. Process is not 0 (primary)")
            continue

        pdg = t.trueSimPartPDG[i]
        print("The sim pdg here is: ", pdg)

        # are any pids NOT a pion, muon, proton or neutron? 
        # if so, flag. event will be skipped. don't want any of these
        if (pdg != -211 and pdg != 211 and pdg != 2212 and pdg != 2112 and pdg != 13):
            print("This PRIMARY particle is NOT a charged pion, mu, proton, or neutron! Skip event.")
            flag = 1
            break

        # Now looking at the pions. Skip event if > 1 pion. 
        # Also skip if pion energy < 70 MeV/c. 
        if (pdg == 211 or pdg == -211): 
            print("Found pion.")
            pions = pions + 1
            piTID = t.trueSimPartTID[i]

            if (pions > 1):
                print("More than 1 pion! Skipping event.")
                flag = 1
                break

            pxPi = t.trueSimPartPx[i]
            pyPi = t.trueSimPartPy[i]
            pzPi = t.trueSimPartPz[i]
            energyPi = t.trueSimPartE[i]
            momPi, angPi = momAngleCalc( pxPi, pyPi, pzPi )
            momPi = momPi / 1000. # convert from MeV to GeV
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
            muTID = t.trueSimPartTID[i]

            if (muons > 1):
                flag = 1
                print("More than 1 muon! Skipping event...")
                flag = 1
                break
            
            pxMu = t.trueSimPartPx[i]
            print(pxMu)
            pyMu = t.trueSimPartPy[i]
            pzMu = t.trueSimPartPz[i]
            energyMu = t.trueSimPartE[i]
            momMu, angMu = momAngleCalc( pxMu, pyMu, pzMu )
            momMu = momMu / 1000. # convert from MeV to GeV
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
            pxP = t.trueSimPartPx[i]
            pyP = t.trueSimPartPy[i]
            pzP = t.trueSimPartPz[i]
            energyP = t.trueSimPartE[i]
            momP, angP = momAngleCalc( pxP, pyP, pzP )
            momP = momP / 1000. # convert from MeV to GeV
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

                    pTID = t.trueSimPartTID[i]

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

    print("The TIDs were (piTID, muTID, pTID): ", piTID, ", ", muTID, ", ", pTID)

    recoMomPi = -1.0
    recoMomMu = -1.0
    recoMomP = -1.0

    trackCompMu = -1.0
    trackCompPi = -1.0
    trackCompP = -1.0

    trackTrueCompMu = -1.0
    trackTrueCompPi = -1.0
    trackTrueCompP = -1.0

    # now look at the reco info
    for k in range(nn):


        recoTID = t.trackTrueTID[k]
        print("This is the reco'd TID!", recoTID)

        # reco'd pion information
        if (recoTID == piTID): 
            recoPiPID = t.trackPID[k]
            trackCompPi = t.trackComp[k]
            trackTrueCompPi = t.trackTrueComp[k]
            recoPiE = t.trackRecoE[k] # kinetic energy
            print("Reco Track PID: ", recoPiPID)
            print("Reco energy: ", recoPiE)
            if (recoPiE > 0): 
                recoMomPi = recoMomCalc(recoPiE, piMass)
            print("This is the reco'd mom in GeV: ", recoMomPi)

        # reco'd muon information
        if (recoTID == muTID): 
            recoMuPID = t.trackPID[k]
            trackCompMu = t.trackComp[k]
            trackTrueCompMu = t.trackTrueComp[k]
            recoMuE = t.trackRecoE[k] # kinetic energy
            print("Reco Track PID: ", recoMuPID)
            print("Reco energy: ", recoMuE)
            if (recoMuE > 0): 
                recoMomMu = recoMomCalc(recoMuE, muMass)
            print("This is the reco'd mom in GeV: ", recoMomMu)

        # reco'd leading proton information
        if (recoTID == pTID): 
            recopPID = t.trackPID[k]
            trackCompP = t.trackComp[k]
            trackTrueCompP = t.trackTrueComp[k]
            recopE = t.trackRecoE[k] # kinetic energy
            print("Reco Track PID: ", recopPID)
            print("Reco energy: ", recopE)
            if (recopE > 0): 
                recoMomP = recoMomCalc(recopE, pMass)
            print("This is the reco'd mom in GeV: ", recoMomP)

        
        

    if (recoMomPi != -1) and (recoMomMu != -1) and (recoMomP != -1): 
        print("THESE ARE ALL THE FINAL THINGS: ")
        print("run: ", t.run)
        print("subrun: ", t.subrun)
        print("event: ", t.event)
        print("truth pionMom: ", leadingMomPi*1000.)
        print("truth pionAng: ", leadingAngPi)
        print("truth muonMom: ", leadingMomMu*1000.)
        print("muonAng: ", leadingAngMu)
        print("lProtonMom: ", leadingMomP*1000.)
        print("lProtonAng: ", leadingAngP)
        print("pxP: ", pxP/1000.)
        print("pyP: ", pyP/1000.)
        print("pzP: ", pzP/1000.)
        print("pxMu: ", pxMu/1000.)
        print("pyMu: ", pyMu/1000.)
        print("pzMu: ", pzMu/1000.)
        print("pxPi: ", pxPi/1000.)
        print("pyPi: ", pyPi/1000.)
        print("pzPi: ", pzPi/1000.)
        print("eP: ", energyP/1000.)
        print("eMu: ", energyMu/1000.)
        print("ePi: ", energyPi/1000.)
        print("eNu: ", t.trueNuE)
        print("pdgNu: ", t.trueNuPDG)
        #print("modeNu: ", t.trueNuMode)
        #print("intrxnNu: ", t.trueNuIntrxnType)
        print("weight: ", t.xsecWeight)
        print("recoNuE_: ", t.recoNuE)
        print("recoContained_: ", t.vtxContainment)
        print("trackRecoPi: ", recoPiE)
        print("trackRecoMu: ", recoMuE)
        print("trackRecoP: ", recopE)
        print("recoMomPi: ", recoMomPi)
        print("recoMomMu: ", recoMomMu)
        print("recoMomP: ", recoMomP)


    print("Filling lists...")
    finalList.append(e)
    run_[0] = t.run
    subrun_[0] = t.subrun
    event_[0] = t.event
    pionMom_[0] = leadingMomPi*1000.
    pionAng_[0] = leadingAngPi
    muonMom_[0] = leadingMomMu*1000.
    muonAng_[0] = leadingAngMu
    lProtonMom_[0] = leadingMomP*1000.
    lProtonAng.append ( leadingAngP )
    lProtonAng_[0] = leadingAngP
    pxP_[0] = pxP/1000.
    pyP_[0] = pyP/1000.
    pzP_[0] = pzP/1000.
    pxMu_[0] = pxMu/1000.
    pyMu_[0] = pyMu/1000.
    pzMu_[0] = pzMu/1000.
    pxPi_[0] = pxPi/1000.
    pyPi_[0] = pyPi/1000.
    pzPi_[0] = pzPi/1000.
    eP_[0] = energyP/1000.
    eMu_[0] = energyMu/1000.
    ePi_[0] = energyPi/1000.
    eNu_[0] = t.trueNuE
    pdgNu_[0] = t.trueNuPDG
    #modeNu_[0] = t.trueNuMode
    #intrxnNu_[0] = t.trueNuIntrxnType
    weight_[0] = t.xsecWeight
    recoNuE_[0] = t.recoNuE
    recoContained_[0] = t.vtxContainment
    recoMomPi_[0] = recoMomPi
    recoMomMu_[0] = recoMomMu
    recoMomP_[0] = recoMomP
    trackCompMu_[0] = trackCompMu
    trackCompPi_[0] = trackCompPi
    trackCompP_[0] = trackCompP
    trackTrueCompMu_[0] = trackCompMu
    trackTrueCompPi_[0] = trackCompPi
    trackTrueCompP_[0] = trackCompP
    newT.Fill()

print("Done!")
print("Final List: ", finalList)
print("lProtonAng: ", lProtonAng, " with a size of: ", len(lProtonAng)) 

#np.savetxt('finalList_truth_082624.csv', finalList, delimiter=',')

newF.Write()
newF.Close()

print("finalList = ", finalList)
print("passedModule = ", passedModule)

print("This is how many were in finalList but NOT passedModule:")
print( list(set(finalList) - set(passedModule)) )

print("This is how many were in passedModule but NOT finalList:")
print( list(set(passedModule) - set(finalList)) )