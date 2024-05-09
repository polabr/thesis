import ROOT 
from ROOT import TFile, TTree, gDirectory, TCanvas, TH1D, TColor, TGraphErrors, TMath, TLatex
from ROOT import TH2D

import numpy as np
from array import array

from larlite import larlite

# larlite i/o
#ioll = larlite.storage_manager( larlite.storage_manager.kREAD )
#ioll.add_in_filename("/cluster/tufts/wongjiradlabnu/nutufts/data/ntuples/dlgen2_reco_v2me05_ntuple_v0_mcc9_v29e_dl_run3b_bnb_nu_overlay_nocrtremerge.root")
#ioll.open()
#ll_nentries = ioll.get_entries()

#f = TFile("/cluster/tufts/wongjiradlabnu/nutufts/data/ntuples/dlgen2_reco_v2me05_ntuple_v0_mcc9_v29e_dl_run3b_bnb_nu_overlay_nocrtremerge.root","READ")

# new ver with interaction, mode
f = TFile("/cluster/tufts/wongjiradlabnu/pabrat01/gen2ntuple/outdir/reco_v2me05_gen2ntuple_bnb_nu_overlay_run3_v6.root","READ")

t = f.Get("EventTree")
t_pot = f.Get("potTree")

# Create new .root file that will contain the result of this script
newF = TFile("selectedEventsPrim_050824_vetod_test.root","recreate")
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
#xNu_ = array('d', [0.])
#yNu_ = array('d', [0.])
#zNu_ = array('d', [0.])
eP_ = array('d', [0.])
eMu_ = array('d', [0.])
ePi_ = array('d', [0.])
eNu_ = array('d', [0.])
pdgNu_ = array('i', [0])
modeNu_ = array('i', [0])
intrxnNu_ = array('i', [0])
weight_ = array('d', [0.])
recoNuE_ = array('d', [0.])
#maxNTrks = 100
#nTracks_ = array('i', [0])
#trackPID_ = array('i', maxNTrks*[0])
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
#newT.Branch('xNu_', xNu_, 'xNu_/D')
#newT.Branch('yNu_', yNu_, 'yNu_/D')
#newT.Branch('zNu_', zNu_, 'zNu_/D')
newT.Branch('eP_', eP_, 'eP_/D')
newT.Branch('eMu_', eMu_, 'eMu_/D')
newT.Branch('ePi_', ePi_, 'ePi_/D')
newT.Branch('eNu_', eNu_, 'eNu_/D')
newT.Branch('pdgNu_', pdgNu_, 'pdgNu_/I')
newT.Branch('modeNu_', modeNu_, 'modeNu_/I')
newT.Branch('intrxnNu_', intrxnNu_, 'intrxnNu_/I')
newT.Branch('weight_', weight_, 'weight_/D')
newT.Branch('recoNuE_', recoNuE_, 'recoNuE_/D')
#newT.Branch("trackPID_", trackPID_, 'trackPID[nTracks]/I')


entries = t.GetEntries()
print("This is how many entries this ntuple file has: ", entries)

newF.cd()

finalList = []

# events I am vetoing for now
veto = np.loadtxt("allDiff.txt", dtype=float) 
veto = veto.astype(np.int64)
print("Veto'd events: ", veto) 
print("How many events?", veto.shape)

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

for e in range(0,1000): #entries

    t.GetEntry(e)

    if (e in veto): 
        continue
    
    #if (t.run != 14121 or t.subrun != 239 or t.event != 11975):
    #     continue

    print("    THIS IS ENTRY NUMBER: ", e)
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
            energyPi = t.truePrimPartE[i]
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
            
            pxMu = t.truePrimPartPx[i]
            print(pxMu)
            pyMu = t.truePrimPartPy[i]
            pzMu = t.truePrimPartPz[i]
            energyMu = t.truePrimPartE[i]
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
            energyP = t.truePrimPartE[i]
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

    print("THESE ARE ALL THE FINAL THINGS: ")
    print("run: ", t.run)
    print("subrun: ", t.subrun)
    print("event: ", t.event)
    print("pionMom: ", leadingMomPi*1000)
    print("pionAng: ", leadingAngPi)
    print("muonMom: ", leadingMomMu*1000)
    print("muonAng: ", leadingAngMu)
    print("lProtonMom: ", leadingMomP*1000)
    print("lProtonAng: ", leadingAngP)
    print("pxP: ", pxP)
    print("pyP: ", pyP)
    print("pzP: ", pzP)
    print("pxMu: ", pxMu)
    print("pyMu: ", pyMu)
    print("pzMu: ", pzMu)
    print("pxPi: ", pxPi)
    print("pyPi: ", pyPi)
    print("pzPi: ", pzPi)
    print("eP: ", energyP)
    print("eMu: ", energyMu)
    print("ePi: ", energyPi)
    print("eNu: ", t.trueNuE)
    print("pdgNu: ", t.trueNuPDG)
    print("modeNu: ", t.trueNuMode)
    print("intrxnNu: ", t.trueNuIntrxnType)
    print("weight: ", t.xsecWeight)
    print("recoNuE_: ", t.recoNuE)

    #if (sum(NMomsP) > 0.30) and (sum(KEs_P) > 0.045):  
    print("If got to this point, this means the event wasn't skipped.")
    print("Filling lists...")
    finalList.append(e)
    run_[0] = t.run
    subrun_[0] = t.subrun
    event_[0] = t.event
    pionMom.append( leadingMomPi*1000 )
    pionMom_[0] = leadingMomPi*1000
    pionAng.append( leadingAngPi )
    pionAng_[0] = leadingAngPi
    muonMom.append( leadingMomMu*1000 )
    muonMom_[0] = leadingMomMu*1000
    muonAng.append( leadingAngMu )
    muonAng_[0] = leadingAngMu
    lProtonMom.append ( leadingMomP*1000 )
    lProtonMom_[0] = leadingMomP*1000
    lProtonAng.append ( leadingAngP )
    lProtonAng_[0] = leadingAngP
    pxP_[0] = pxP
    pyP_[0] = pyP
    pzP_[0] = pzP
    pxMu_[0] = pxMu
    pyMu_[0] = pyMu
    pzMu_[0] = pzMu
    pxPi_[0] = pxPi
    pyPi_[0] = pyPi
    pzPi_[0] = pzPi
    #xNu_[0] = t.trueVtxX
    #yNu_[0] = t.trueVtxY
    #zNu_[0] = t.trueVtxZ
    eP_[0] = energyP
    eMu_[0] = energyMu
    ePi_[0] = energyPi
    eNu_[0] = t.trueNuE
    pdgNu_[0] = t.trueNuPDG
    modeNu_[0] = t.trueNuMode
    intrxnNu_[0] = t.trueNuIntrxnType
    weights.append( t.xsecWeight )
    weight_[0] = t.xsecWeight
    recoNuE_[0] = t.recoNuE
    #trackPID_[0] = t.trackPID
    newT.Fill()

    #if (sum(NMomsP) > 300) and (sum(KEs_P) > 45): 
    #    finalList.append(e) # passed all cuts!

    #if pions==1: 
    #    pionEntries.append(e)

print("Final List: ", finalList)
print("lProtonMom: ", lProtonMom, " with a size of: ", len(lProtonMom)) 

##np.savetxt('finalList_prim_may6.csv', finalList, delimiter=',')

'''
print("Final List: ", finalList)
print("pionMom: ", pionMom)
print("pionAng: ", pionAng)
print("muonMom: ", muonMom)
print("muonAng: ", muonAng)
print("lpMom: ", lProtonMom)
print("lpAng: ", lProtonAng)
'''

'''
print("Here are the final lists and their sizes (momentum in MeV/c)")

print("lProtonMom: ", lProtonMom, " with a size of: ", len(lProtonMom)) 
print("muonMom: ", muonMom, " with a size of: ", len(muonMom)) 
print("pionMom: ", pionMom, " with a size of: ", len(pionMom)) 

print("muonAng: ", muonAng, " with a size of: ", len(muonAng)) 
print("pionAng: ", pionAng, " with a size of: ", len(pionAng)) 
print("lProtonAng: ", lProtonAng, " with a size of: ", len(lProtonAng)) 
'''

#np.savetxt('ntuple_lProtonMom_011124_2.csv', lProtonMom, delimiter=',')
#np.savetxt('ntuple_muonMom_011124_2.csv', muonMom, delimiter=',')
#np.savetxt('ntuple_pionMom_011124_2.csv', pionMom, delimiter=',')

#np.savetxt('ntuple_muonAng_011124_2.csv', muonAng, delimiter=',')
#np.savetxt('ntuple_pionAng_011124_2.csv', pionAng, delimiter=',')
#np.savetxt('ntuple_lProtonAng_011124_2.csv', lProtonAng, delimiter=',')

#np.savetxt('ntuple_weights_011124_2.csv', weights, delimiter=',')

newF.Write()
newF.Close()

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

