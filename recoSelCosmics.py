# This script was edited to run my reco selection on cosmics.
# There is no truth information because this is EXTBNB

import ROOT 
from ROOT import TFile, TTree

import numpy as np
from array import array
import selModule

f = TFile("dlgen2_reco_v2me06_ntuple_v5_mcc9_v29e_dl_run1_extbnb_combined.root","READ")
#f = TFile("/cluster/tufts/wongjiradlabnu/pabrat01/gen2ntuple/outdir/dlgen2_reco_v2me06_ntuple_v5_mcc9_v28_wctagger_bnboverlay.root","READ")

t = f.Get("EventTree")
##t_pot = f.Get("potTree")

# Create new .root file that will contain the result of this script
newF = TFile("selectedEventsTrueRecoBoth_cosmics_vtxOnly_121824_2.root","recreate")
newT = TTree("selectedEvents", "Selected Events Tree") 

passedSel_ = array('i', [0]) # 1 if passed truth, 2 if reco, 3 if both
run_ = array('i', [0])
subrun_ = array('i', [0])
event_ = array('i', [0]) 
weight_ = array('d', [0.])

truthSel_truthLProtonMom_ = array('d', [0.])
truthSel_truthPionMom_ = array('d', [0.])
truthSel_truthMuonMom_ = array('d', [0.])

truthSel_pxP_ = array('d', [0.])
truthSel_pyP_ = array('d', [0.])
truthSel_pzP_ = array('d', [0.])
truthSel_pxMu_ = array('d', [0.])
truthSel_pyMu_ = array('d', [0.])
truthSel_pzMu_ = array('d', [0.])
truthSel_pxPi_ = array('d', [0.])
truthSel_pyPi_ = array('d', [0.])
truthSel_pzPi_ = array('d', [0.])
truthSel_eNu_ = array('d', [0.])
truthSel_eP_ = array('d', [0.])
truthSel_eMu_ = array('d', [0.])
truthSel_ePi_ = array('d', [0.])
'''
lProtonAng_ = array('d', [0.])
pionAng_ = array('d', [0.])
muonAng_ = array('d', [0.])
pdgNu_ = array('i', [0])
#modeNu_ = array('i', [0])
#intrxnNu_ = array('i', [0])
'''

recoSel_recoNuE_ = array('d', [0.])
recoSel_recoContained_ = array('i', [0])
recoSel_recoMomPi_ = array('d', [0.])
recoSel_recoMomMu_ = array('d', [0.])
recoSel_recoMomP_ = array('d', [0.])

recoSel_trkDirPX_ = array('d', [0.])
recoSel_trkDirPY_ = array('d', [0.])
recoSel_trkDirPZ_ = array('d', [0.])
recoSel_trkDirMuX_ = array('d', [0.])
recoSel_trkDirMuY_ = array('d', [0.])
recoSel_trkDirMuZ_ = array('d', [0.])
recoSel_trkDirPiX_ = array('d', [0.])
recoSel_trkDirPiY_ = array('d', [0.])
recoSel_trkDirPiZ_ = array('d', [0.])

recoSel_trackCompMu_ = array('d', [0.])
recoSel_trackCompPi_ = array('d', [0.])
recoSel_trackCompP_ = array('d', [0.])

recoSel_eP_ = array('d', [0.])
recoSel_ePi_ = array('d', [0.])
recoSel_eMu_ = array('d', [0.])

newT.Branch('passedSel_', passedSel_, 'passedSel_/I')
newT.Branch('run_', run_, 'run_/I')
newT.Branch('subrun_', subrun_, 'subrun_/I')
newT.Branch('event_', event_, 'event_/I')
newT.Branch('weight_', weight_, 'weight_/D')
newT.Branch('truthSel_truthLProtonMom_', truthSel_truthLProtonMom_, 'truthSel_truthLProtonMom_/D')
newT.Branch('truthSel_truthPionMom_', truthSel_truthPionMom_, 'truthSel_truthPionMom_/D')
newT.Branch('truthSel_truthMuonMom_', truthSel_truthMuonMom_, 'truthSel_truthMuonMom_/D')

newT.Branch('truthSel_pxP_', truthSel_pxP_, 'truthSel_pxP_/D')
newT.Branch('truthSel_pyP_', truthSel_pyP_, 'truthSel_pyP_/D')
newT.Branch('truthSel_pzP_', truthSel_pzP_, 'truthSel_pzP_/D')
newT.Branch('truthSel_pxMu_', truthSel_pxMu_, 'truthSel_pxMu_/D')
newT.Branch('truthSel_pyMu_', truthSel_pyMu_, 'truthSel_pyMu_/D')
newT.Branch('truthSel_pzMu_', truthSel_pzMu_, 'truthSel_pzMu_/D')
newT.Branch('truthSel_pxPi_', truthSel_pxPi_, 'truthSel_pxPi_/D')
newT.Branch('truthSel_pyPi_', truthSel_pyPi_, 'truthSel_pyPi_/D')
newT.Branch('truthSel_pzPi_', truthSel_pzPi_, 'truthSel_pzPi_/D')
newT.Branch('truthSel_eNu_', truthSel_eNu_, 'truthSel_eNu_/D')
newT.Branch('truthSel_eP_', truthSel_eP_, 'truthSel_eP_/D')
newT.Branch('truthSel_eMu_', truthSel_eMu_, 'truthSel_eMu_/D')
newT.Branch('truthSel_ePi_', truthSel_ePi_, 'truthSel_ePi_/D')
'''
newT.Branch('lProtonAng_', lProtonAng_, 'lProtonAng_/D')
newT.Branch('pionAng_', pionAng_, 'pionAng_/D')
newT.Branch('muonAng_', muonAng_, 'muonAng_/D')
newT.Branch('pdgNu_', pdgNu_, 'pdgNu_/I')
#newT.Branch('modeNu_', modeNu_, 'modeNu_/I')
#newT.Branch('intrxnNu_', intrxnNu_, 'intrxnNu_/I')
'''
newT.Branch('recoSel_recoNuE_', recoSel_recoNuE_, 'recoSel_recoNuE_/D')
newT.Branch('recoSel_recoContained_', recoSel_recoContained_, 'recoSel_recoContained_/I')
newT.Branch('recoSel_recoMomPi_', recoSel_recoMomPi_, 'recoSel_recoMomPi_/D')
newT.Branch('recoSel_recoMomMu_', recoSel_recoMomMu_, 'recoSel_recoMomMu_/D')
newT.Branch('recoSel_recoMomP_', recoSel_recoMomP_, 'recoSel_recoMomP_/D')

newT.Branch('recoSel_trkDirPX_', recoSel_trkDirPX_, 'recoSel_trkDirPX_/D')
newT.Branch('recoSel_trkDirPY_', recoSel_trkDirPY_, 'recoSel_trkDirPY_/D')
newT.Branch('recoSel_trkDirPZ_', recoSel_trkDirPZ_, 'recoSel_trkDirPZ_/D')
newT.Branch('recoSel_trkDirMuX_', recoSel_trkDirMuX_, 'recoSel_trkDirMuX_/D')
newT.Branch('recoSel_trkDirMuY_', recoSel_trkDirMuY_, 'recoSel_trkDirMuY_/D')
newT.Branch('recoSel_trkDirMuZ_', recoSel_trkDirMuZ_, 'recoSel_trkDirMuZ_/D')
newT.Branch('recoSel_trkDirPiX_', recoSel_trkDirPiX_, 'recoSel_trkDirPiX_/D')
newT.Branch('recoSel_trkDirPiY_', recoSel_trkDirPiY_, 'recoSel_trkDirPiY_/D')
newT.Branch('recoSel_trkDirPiZ_', recoSel_trkDirPiZ_, 'recoSel_trkDirPiZ_/D')

newT.Branch('recoSel_trackCompMu_', recoSel_trackCompMu_, 'recoSel_trackCompMu_/D')
newT.Branch('recoSel_trackCompPi_', recoSel_trackCompPi_, 'recoSel_trackCompPi_/D')
newT.Branch('recoSel_trackCompP_', recoSel_trackCompP_, 'recoSel_trackCompP_/D')

newT.Branch('recoSel_eP_', recoSel_eP_, 'recoSel_eP_/D')
newT.Branch('recoSel_ePi_', recoSel_ePi_, 'recoSel_ePi_/D')
newT.Branch('recoSel_eMu_', recoSel_eMu_, 'recoSel_eMu_/D')



entries = t.GetEntries()
print("This is how many entries this ntuple file has: ", entries)

newF.cd()

finalList_truth = []
finalList_reco = []
finalList_both = []

'''
# events I am vetoing for now
veto = np.loadtxt("allDiff.txt", dtype=float) 
veto = veto.astype(np.int64)
print("Veto'd events: ", veto) 
print("How many events?", veto.shape)
'''

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

'''
potSum = 0.
for i in range( t_pot.GetEntries() ):
    t_pot.GetEntry(i)
    #print("This is event ", i, ", POT is ", t_pot.totGoodPOT)
    potSum = potSum + t_pot.totGoodPOT

print("The total POT here is: ", potSum)
'''

######################## 
#  LOOP THRU NTUPLES!  #
########################

for e in range(entries): #entries

    t.GetEntry(e)

    #cosmicPassed = 0

    print("-----------------------------------------")

    print("   THIS IS ENTRY NUMBER: ", e)

    print("This is the run number: ", t.run )
    print("This is the subrun number: ", t.subrun )
    print("This is the event number: ", t.event )

    '''
    if (e in veto):  
        print("This entry is in the veto list!")
        continue
    '''

    # setting this to 0 by default
    passedSel = 0

    '''
    if (selModule.truthSel(t) == True): 
        if (selModule.recoSel(t) == True): 
            passedSel = 3 # passed both truth and reco selection
        else: 
            passedSel = 1 # only passed truth selection
    elif (selModule.recoSel(t) == True):
        passedSel = 2 # only passed reco selection
    '''

    # note that with EXTBNB, there is no truth info, so can't run truth selection
    if (selModule.recoSelVtxOnly(t) == True):
        passedSel = 2 # passed reco selection

    # skip event and don't fill if passed neither truth nor reco sel
    if (passedSel == 0): continue

    # print("passedSel number? (1 for true only, 2 for reco only, 3 for both): ", passedSel)
    # print("Passed truthSel? ", selModule.truthSel(t))
    # print("Passed recoSel? ", selModule.recoSel(t))

    truthsel_pions = 0
    truthsel_muons = 0
    truthsel_protons = 0
    truthsel_NMomsP = []

    recosel_pions = 0
    recosel_muons = 0
    recosel_protons = 0
    recosel_NMomsP = []

    truthsel_leadingAngP = -999
    truthsel_leadingAngMu = -999
    truthsel_leadingAngPi = -999

    # momentum vars for each of the three particles
    # to be filled after checks if passed truth/reco sel
    truthSel_truthPionMom = -999
    truthSel_truthMuonMom = -999
    truthSel_truthLProtonMom = -999

    truthSel_trkDirPX = -999
    truthSel_trkDirPY = -999
    truthSel_trkDirPZ = -999
    truthSel_trkDirMuX = -999
    truthSel_trkDirMuY = -999
    truthSel_trkDirMuZ = -999
    truthSel_trkDirPiX = -999
    truthSel_trkDirPiY = -999
    truthSel_trkDirPiZ = -999

    truthSel_nuE = -999
    truthSel_eMu = -999
    truthSel_ePi = -999
    truthSel_eP = -999

    recoSel_recoNuE = -999
    recoSel_recoContained = -999
    recoSel_recoMomPi = -999
    recoSel_recoMomMu = -999
    recoSel_recoMomP = -999

    recoSel_trkDirPX = -999
    recoSel_trkDirPY = -999
    recoSel_trkDirPZ = -999
    recoSel_trkDirMuX = -999
    recoSel_trkDirMuY = -999
    recoSel_trkDirMuZ = -999
    recoSel_trkDirPiX = -999
    recoSel_trkDirPiY = -999
    recoSel_trkDirPiZ = -999

    recoSel_trackCompMu = -1.0
    recoSel_trackCompPi = -1.0
    recoSel_trackCompP = -1.0

    recoSel_eP = -999
    recoSel_ePi = -999
    recoSel_eMu = -999

    pTID = -999
    piTID = -999
    muTID = -999

    # number of particles above threshold in truth sel
    truthsel_protonsN = 0 
    truthsel_muonsN = 0
    truthsel_pionsN = 0

    # number of particles above threshold in reco sel
    recosel_protonsN = 0 
    recosel_muonsN = 0
    recosel_pionsN = 0

    '''
    ## TRUTH CLUSTER LOOP ##
    if (passedSel == 1) or (passedSel == 3):
        m = t.nTrueSimParts # how many truth clusters are in the event?
        for i in range(m):

            if (t.trueSimPartProcess[i] != 0): 
                print("Skipping cluster. Process is not 0 (primary)")
                continue

            pdg = t.trueSimPartPDG[i]

            if (pdg == 211 or pdg == -211): 
                print("Found pion.")
                truthsel_pions = truthsel_pions + 1
                piTID = t.trueSimPartTID[i]

                pxPi = t.trueSimPartPx[i]
                pyPi = t.trueSimPartPy[i]
                pzPi = t.trueSimPartPz[i]
                energyPi = t.trueSimPartE[i]
                momPi, angPi = truthMomAngleCalc( pxPi, pyPi, pzPi )

                print("Does this pion have at least momentum 70 MeV/c (0.07 GeV/c)?")
                if (momPi > 0.07):
                    print("Pi mom is > 0.07 GeV/c. It is: ", momPi, " GeV/c. Incrementing number of N truthsel_pions.")
                    truthsel_pionsN = truthsel_pionsN + 1
                    truthSel_truthPionMom = momPi
                    truthsel_leadingAngPi = angPi

                    truthSel_trkDirPiX = pxPi
                    truthSel_trkDirPiY = pyPi
                    truthSel_trkDirPiZ = pzPi

                    truthSel_ePi = energyPi

            # Looking at truthsel_muons
            if (pdg == 13): # mu
                print("Found muon.")
                truthsel_muons = truthsel_muons + 1
                muTID = t.trueSimPartTID[i]
                
                pxMu = t.trueSimPartPx[i]
                pyMu = t.trueSimPartPy[i]
                pzMu = t.trueSimPartPz[i]
                energyMu = t.trueSimPartE[i]
                momMu, angMu = truthMomAngleCalc( pxMu, pyMu, pzMu ) # GeV

                print("Does this muon meet the momentum threshold (max 1.5 GeV)?")
                if ( momMu < 1.5 ):
                    print("Yes, it is under 1.5 GeV. Incrementing number of N truthsel_muons.")
                    truthsel_muonsN = truthsel_muonsN + 1
                    truthSel_truthMuonMom = momMu # GeV
                    truthsel_leadingAngMu = angMu

                    truthSel_trkDirMuX = pxMu # MeV
                    truthSel_trkDirMuY = pyMu # MeV
                    truthSel_trkDirMuZ = pzMu # MeV

                    truthSel_eMu = energyMu # MeV

            # Now look at truthsel_protons
            if (pdg == 2212):
                print("Found proton.")
                truthsel_protons = truthsel_protons + 1 
                pxP = t.trueSimPartPx[i]
                pyP = t.trueSimPartPy[i]
                pzP = t.trueSimPartPz[i]
                energyP = t.trueSimPartE[i]
                momP, angP = truthMomAngleCalc( pxP, pyP, pzP )

                print("Does this proton meet the momentum threshold?")
                if ( momP > 0.30 and momP < 1.0 ):
                    print("Yes, appending to list of N proton moms.")
                    truthsel_NMomsP.append(momP) # list of N truthsel_protons in the event
                    truthsel_protonsN = truthsel_protonsN + 1

                    print("Is this the leading proton?")
                    if ( momP == max(truthsel_NMomsP) ):
                        print("Yes. Updating mom and ang.")
                        truthSel_truthLProtonMom = momP
                        truthsel_leadingAngP = angP 

                        truthSel_trkDirPX = pxP
                        truthSel_trkDirPY = pyP
                        truthSel_trkDirPZ = pzP

                        truthSel_eP = energyP

                        pTID = t.trueSimPartTID[i]

        print("In this event, there were ", truthsel_protons, " number of primary truthsel_protons.")
        print("And ", truthsel_protonsN, " truthsel_protons were above threshold.")

        print("In this event, there were ", truthsel_muons, " number of primary truthsel_muons.")
        print("And ", truthsel_muonsN, " truthsel_muons were above threshold.")

        print("In this event, there were ", truthsel_pions, " number of primary truthsel_pions.")
        print("And ", truthsel_pionsN, " truthsel_pions were above threshold.")

        print("If got to this point, this means the event wasn't skipped.")

        print("The TIDs were (piTID, muTID, pTID): ", piTID, ", ", muTID, ", ", pTID)
    '''

    # ## RECO CLUSTER LOOP ##
    # #if (passedSel == 2) or (passedSel == 3):
    # if (passedSel == 2) or (passedSel == 3):

    #     n = t.nTracks

    #     for i in range(n):
            
    #         print("This is track #", i)

    #         # first check if it's a primary (code of 0)
    #         if (t.trackIsSecondary[i] != 0): 
    #             print("Not a primary! Its code is not 0. It is: ", t.trackIsSecondary[i])
    #             continue
    #         else:
    #             print("Yup, it's a primary! It is: ", t.trackIsSecondary[i])

    #         # does LArPID think it's a primary?
    #         if (t.trackProcess[i] != 0): 
    #             print("Not a primary according to LArPID! Its code is not 0. It is: ", t.trackProcess[i])
    #             continue
    #         else:
    #             print("Yup, it's a primary according to LArPID too. Code: ", t.trackProcess[i])

    #         # LArPID PDG score
    #         if (t.trackClassified[i] != 1):
    #             print("Not classified! Its code is not 1. It is: ", t.trackClassified[i])
    #             continue
    #         else: 
    #             print("Yep, it was classified!")
    #             pdg = t.trackPID[i]
    #             print("Its LArPID predicted PDG score is: ", pdg)

    #         #recoTID = t.trackTrueTID[i]

    #         # # Looking at pions
    #         # if (pdg == 211 or pdg == -211): 

    #         #     print("Found pion.")
    #         #     recosel_pions = recosel_pions + 1

    #         #     recoPiE = t.trackRecoE[i] # in MeV
    #         #     print("recoPiE: ", recoPiE)
    #         #     if (recoPiE > 0): 
    #         #         recoMomPi = recoMomCalc(recoPiE, piMass) # now in GeV

    #         #     print("Does this pion have at least momentum 70 MeV/c (0.07 GeV/c)?")
    #         #     print("recoMomPi: ", recoMomPi)
    #         #     if (recoMomPi > 0.07):
    #         #         print("Pi mom is > 0.07 GeV/c. It is: ", recoMomPi, " GeV/c. Incrementing number of N recosel_pions.")
    #         #         recosel_pionsN = recosel_pionsN + 1
    #         #         recoSel_recoMomPi = recoMomPi

    #         #         recoSel_trkDirPiX = t.trackStartDirX[i]*recoMomPi
    #         #         recoSel_trkDirPiY = t.trackStartDirY[i]*recoMomPi
    #         #         recoSel_trkDirPiZ = t.trackStartDirZ[i]*recoMomPi

    #         #         recoSel_trackCompPi = t.trackComp[i]

    #         #         recoSel_ePi = recoPiE + piMass # convert from KE -> total energy

    #         #         # if got to this point: 
    #         #         cosmicPassed = cosmicPassed + 1

    #         # Looking at muons
    #         if (pdg == 13): # mu 

    #             print("Found muon.")
    #             recosel_muons = recosel_muons + 1

    #             recoMuE = t.trackRecoE[i] # this is the kinetic energy, in MeV
    #             print("recoMuE: ", recoMuE)
    #             if (recoMuE > 0): 
    #                 recoMomMu = recoMomCalc(recoMuE, muMass)

    #             print("Does this muon meet the momentum threshold (max 1.5 GeV)?")
    #             print("recoMomMu: ", recoMomMu)
    #             if ( recoMomMu < 1.5 ):
    #                 print("Yes, it is under 1.5 GeV. Incrementing number of N recosel_muons.")
    #                 recosel_muonsN = recosel_muonsN + 1
    #                 recoSel_recoMomMu = recoMomMu

    #                 recoSel_trkDirMuX = t.trackStartDirX[i]*recoMomMu
    #                 recoSel_trkDirMuY = t.trackStartDirY[i]*recoMomMu
    #                 recoSel_trkDirMuZ = t.trackStartDirZ[i]*recoMomMu

    #                 recoSel_trackCompMu = t.trackComp[i]

    #                 recoSel_eMu = recoMuE + muMass # convert from KE -> total energy

    #                 # if got to this point: 
    #                 #cosmicPassed = 3

    #         # # Now look at protons
    #         # if (pdg == 2212):

    #         #     print("Found proton.")
    #         #     recosel_protons = recosel_protons + 1 

    #         #     recoPE = t.trackRecoE[i]
    #         #     print("recoPE: ", recoPE)
    #         #     if (recoPE > 0): 
    #         #         recoMomP = recoMomCalc(recoPE, pMass)
                
    #         #     print("recoMomP = ", recoMomP)
    #         #     print("Does this proton meet the momentum threshold?")
    #         #     if ( recoMomP > 0.30 and recoMomP < 1.0 ):
    #         #         print("Yes, appending to list of N proton moms.")
    #         #         recosel_NMomsP.append(recoMomP) # list of N recosel_protons in the event
    #         #         recosel_protonsN = recosel_protonsN + 1

    #         #         print("Is this the leading proton?")
    #         #         if ( recoMomP == max(recosel_NMomsP) ):
    #         #             print("Yes. Updating mom and ang.")
    #         #             recoSel_recoMomP = recoMomP

    #         #         recoSel_trkDirPX = t.trackStartDirX[i]*recoMomP
    #         #         recoSel_trkDirPY = t.trackStartDirY[i]*recoMomP
    #         #         recoSel_trkDirPZ = t.trackStartDirZ[i]*recoMomP

    #         #         recoSel_trackCompP = t.trackComp[i]

    #         #         recoSel_eP = recoPE  + pMass # convert from KE -> total energy

    #         #         # if got to this point: 
    #         #         cosmicPassed = cosmicPassed + 1

    #         #     else: 
    #         #         print("NO. The p mom was ", recoMomP, "which is either < 0.3 GeV or > 1 GeV")

    #         recoSel_recoNuE = t.recoNuE
    #         recoSel_recoContained = t.vtxContainment

    #         #print("cosmicPassed score was: ", cosmicPassed)


    #if (cosmicPassed == 3):
    
    print("Filling lists...")

    '''
    if (passedSel == 1) or (passedSel == 3):
        finalList_truth.append(e)
    if (passedSel == 2) or (passedSel == 3):
        finalList_reco.append(e)
    if (passedSel == 3): 
        finalList_both.append(e)
    '''

    passedSel_[0] = passedSel
    run_[0] = t.run
    subrun_[0] = t.subrun
    event_[0] = t.event
    ##weight_[0] = t.xsecWeight

    '''
    # truth selection items
    truthSel_truthPionMom_[0] = truthSel_truthPionMom
    #pionAng_[0] = truthsel_leadingAngPi
    truthSel_truthMuonMom_[0] = truthSel_truthMuonMom
    #muonAng_[0] = truthsel_leadingAngMu
    truthSel_truthLProtonMom_[0] = truthSel_truthLProtonMom

    truthSel_pxP_[0] = truthSel_trkDirPX/1000. # convert MeV to GeV
    truthSel_pyP_[0] = truthSel_trkDirPY/1000.
    truthSel_pzP_[0] = truthSel_trkDirPZ/1000.

    truthSel_pxPi_[0] = truthSel_trkDirPiX/1000.
    truthSel_pyPi_[0] = truthSel_trkDirPiY/1000.
    truthSel_pzPi_[0] = truthSel_trkDirPiZ/1000.

    truthSel_pxMu_[0] = truthSel_trkDirMuX/1000.
    truthSel_pyMu_[0] = truthSel_trkDirMuY/1000.
    truthSel_pzMu_[0] = truthSel_trkDirMuZ/1000.

    truthSel_eNu_[0] = t.trueNuE # already in GeV in ntuple?
    truthSel_eMu_[0] = truthSel_eMu/1000.
    truthSel_ePi_[0] = truthSel_ePi/1000.
    truthSel_eP_[0] = truthSel_eP/1000.
    '''

    recoSel_recoNuE_[0] = recoSel_recoNuE/1000.
    recoSel_recoContained_[0] = recoSel_recoContained
    recoSel_recoMomPi_[0] = recoSel_recoMomPi
    recoSel_recoMomMu_[0] = recoSel_recoMomMu
    recoSel_recoMomP_[0] = recoSel_recoMomP

    recoSel_trkDirPX_[0] = recoSel_trkDirPX
    recoSel_trkDirPY_[0] = recoSel_trkDirPY
    recoSel_trkDirPZ_[0] = recoSel_trkDirPZ
    recoSel_trkDirMuX_[0] = recoSel_trkDirMuX
    recoSel_trkDirMuY_[0] = recoSel_trkDirMuY
    recoSel_trkDirMuZ_[0] = recoSel_trkDirMuZ
    recoSel_trkDirPiX_[0] = recoSel_trkDirPiX
    recoSel_trkDirPiY_[0] = recoSel_trkDirPiY
    recoSel_trkDirPiZ_[0] = recoSel_trkDirPiZ

    recoSel_trackCompMu_[0] = recoSel_trackCompMu
    recoSel_trackCompPi_[0] = recoSel_trackCompPi
    recoSel_trackCompP_[0] = recoSel_trackCompP

    recoSel_eMu_[0] = recoSel_eMu/1000.
    recoSel_ePi_[0] = recoSel_ePi/1000.
    recoSel_eP_[0] = recoSel_eP/1000.

    #lProtonAng_[0] = truthsel_leadingAngP
    #pxP_[0] = pxP/1000.
    #pyP_[0] = pyP/1000.
    #pzP_[0] = pzP/1000.
    #pxMu_[0] = pxMu/1000.
    #pyMu_[0] = pyMu/1000.
    #pzMu_[0] = pzMu/1000.
    #pxPi_[0] = pxPi/1000.
    #pyPi_[0] = pyPi/1000.
    #pzPi_[0] = pzPi/1000.
    #eP_[0] = energyP/1000.
    #eMu_[0] = energyMu/1000.
    #ePi_[0] = energyPi/1000.
    #eNu_[0] = t.trueNuE
    #pdgNu_[0] = t.trueNuPDG
    #modeNu_[0] = t.trueNuMode
    #intrxnNu_[0] = t.trueNuIntrxnType

    newT.Fill()


print("Done!")

# np.savetxt('finalList_bothSel_truth_091524.csv', finalList_truth, delimiter=',')
# np.savetxt('finalList_bothSel_reco_091524.csv', finalList_reco, delimiter=',')
# np.savetxt('finalList_bothSel_both_091524.csv', finalList_both, delimiter=',')

newF.Write()
newF.Close()

