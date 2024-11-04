import numpy as np

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

# function to determine if event passed reco selection
def recoSel(t): # args: tree

    if (t.foundVertex != 1): 
        #print("MODULE SAYS NO VTX FOUND")
        return False

    n = t.nTracks

    if (n < 3): 
        #print("MODULE: There aren't at least 3 tracks. Skipping...")
        return False

    s = t.nShowers
    twoSecPhoCount = 0

    for i in range(s): 
        if (t.showerProcess[i] == 0): 
            #print("MODULE: There is a primary shower. Skipping...")
            return False # skip all primary showers

    if (twoSecPhoCount > 1): 
        #print("MODULE: twoSecPhoCount > 1. Skipping...")
        return False

    flag = 0
    pions = 0
    muons = 0
    protons = 0
    NMomsP = []
    pdg = -999

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

        #print("MODULE: This is track #", i)

        # first check if it's a primary (code of 0)
        if (t.trackIsSecondary[i] != 0): 
            continue

        # does LArPID think it's a primary?
        if (t.trackProcess[i] != 0): 
            continue

        # LArPID PDG score
        #if (t.trackClassified[i] != 1):
        #    return False
        #else: 
        #    pdg = t.trackPID[i]

        if (t.trackClassified[i] == 1):
            pdg = t.trackPID[i]

        recoTID = t.trackTrueTID[i]

        if (pdg == 211 or pdg == -211): 

            pions = pions + 1

            #print("MODULE: pions: ", pions)

            if (pions > 1):
                flag = 1
                #print("MODULE: pions > 1! Skipping...")
                return False

            recoPiE = t.trackRecoE[i]
            if (recoPiE > 0): 
                recoMomPi = recoMomCalc(recoPiE, piMass)

            if (recoMomPi > 0.07):
                pionsN = pionsN + 1
                leadingMomPi = recoMomPi

            if (pionsN > 1):
                flag = 1
                #print("MODULE: pions > 1! (Check #2). Skipping...")
                return False

            piTID = recoTID

        # Looking at muons
        if (pdg == 13): # mu 

            muons = muons + 1
         
            if (muons > 1):
                flag = 1
                #print("MODULE: muons > 1! Skipping...")
                return False

            recoMuE = t.trackRecoE[i]
            if (recoMuE > 0): 
                recoMomMu = recoMomCalc(recoMuE, muMass)

            if ( recoMomMu < 1.5 ):
                muonsN = muonsN + 1
                leadingMomMu = recoMomMu

            if (muonsN > 1):
                flag = 1
                #print("MODULE: muons > 1! (Check #2) Skipping...")
                return False

            muTID = recoTID

        # Now look at protons
        if (pdg == 2212):

            protons = protons + 1 

            recoPE = t.trackRecoE[i]
            if (recoPE > 0): 
                recoMomP = recoMomCalc(recoPE, pMass)
            
            if ( recoMomP > 0.30 and recoMomP < 1.0 ):
                NMomsP.append(recoMomP) # list of N protons in the event
                protonsN = protonsN + 1

                if ( recoMomP == max(NMomsP) ):
                    leadingMomP = recoMomP

                pTID = recoTID

    # require 
    if ( pionsN == 0 ): 
        #print("Zero pions above threshold. Skip to next event.")
        return False

    # we need at least one proton that passes cuts in my selection
    if ( protonsN < 1 ): 
        #print("Zero protons above threshold. Skip to next event.")
        return False

    # only want 1 muon in my selection
    if ( muonsN == 0 ): 
        #print("Zero muons that meet threshold. Skip to next event.")
        return False

    return True

# function to determine if event passed truth selection
def truthSel(t): # args: tree

    n = t.nTrueSimParts # how many sim clusters are in the event?
    m = t.nTruePrimParts # how many prim clusters are in the event?

    # check if there are at least 3 primary clusters in genie
    if ( m < 3): 
        #print("MODULE: m < 3. Skipping event.")
        return False

    # loop through primPart clusters, skip any event with the following: 
    # an event with fewer than 3 primary tracks according to genie
    # pdg that is not a pion, muon, proton, or neutron
    for j in range(m):
        primPDG = t.truePrimPartPDG[j]
        if (primPDG != -211 and primPDG != 211 and primPDG != 2212 and primPDG != 2112 and primPDG != 13):
            #print("MODULE: Found an unwanted pdg! It is: ", primPDG)
            #print("MODULE: Skipping this whole event.")
            return False

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
    
    # loop through truth clusters in event
    for i in range(n):

        #print("MODULE: This is track #", i)
        
        if (t.trueSimPartProcess[i] != 0): 
            ##print("Skipping cluster. Process is not 0 (primary)")
            continue

        pdg = t.trueSimPartPDG[i]
        #print("MODULE: The sim pdg here is: ", pdg)

        if (pdg != -211 and pdg != 211 and pdg != 2212 and pdg != 2112 and pdg != 13):
            flag = 1
            #print("MODULE: PDG is not -211, 211, 2212, or 13! It is: ", pdg)
            return False

        # Now looking at the pions. Skip event if > 1 pion. 
        # Also skip if pion energy < 70 MeV/c. 
        if (pdg == 211 or pdg == -211): 

            pions = pions + 1
            piTID = t.trueSimPartTID[i]

            if (pions > 1):
                flag = 1
                #print("MODULE: pions > 1! Skipping event...")
                return False

            pxPi = t.trueSimPartPx[i]
            pyPi = t.trueSimPartPy[i]
            pzPi = t.trueSimPartPz[i]
            energyPi = t.trueSimPartE[i]
            momPi, angPi = truthMomAngleCalc( pxPi, pyPi, pzPi )

            #print("MODULE: momPi is calculated to be: ", momPi)

            if (momPi > 0.07):
                #print("MODULE: pion passed threshold of 0.07.")
                pionsN = pionsN + 1
                leadingMomPi = momPi
                leadingAngPi = angPi

            if (pionsN > 1):
                flag = 1
                #print("MODULE: pionsN > 1! Skipping event...")
                return False

        # Looking at muons
        if (pdg == 13): # mu 
            muons = muons + 1
            muTID = t.trueSimPartTID[i]

            if (muons > 1):
                flag = 1
                #print("MODULE: muons > 1! Skipping event...")
                return False
            
            pxMu = t.trueSimPartPx[i]
            pyMu = t.trueSimPartPy[i]
            pzMu = t.trueSimPartPz[i]
            energyMu = t.trueSimPartE[i]
            momMu, angMu = truthMomAngleCalc( pxMu, pyMu, pzMu )

            if ( momMu < 1.5 ):
                muonsN = muonsN + 1
                leadingMomMu = momMu
                leadingAngMu = angMu

            if (muonsN > 1):
                flag = 1
                #print("MODULE: muonsN > 1! Skipping event...")
                return False

        # Now look at protons
        if (pdg == 2212):
            protons = protons + 1 
            pxP = t.trueSimPartPx[i]
            pyP = t.trueSimPartPy[i]
            pzP = t.trueSimPartPz[i]
            energyP = t.trueSimPartE[i]
            momP, angP = truthMomAngleCalc( pxP, pyP, pzP )

            if ( momP > 0.30 and momP < 1.0 ):
                NMomsP.append(momP) # list of N protons in the event
                protonsN = protonsN + 1

                if ( momP == max(NMomsP) ):
                    leadingMomP = momP
                    leadingAngP = angP 

                    pTID = t.trueSimPartTID[i]

    # require 
    if ( pionsN == 0 ): 
        #print("MODULE: No pions found. Skipping event...")
        return False

    # we need at least one proton that passes cuts in my selection
    if ( protonsN < 1 ): 
        #print("MODULE: Not at least 1 proton found. Skipping event...")
        return False

    # only want 1 muon in my selection
    if ( muonsN == 0 ): 
        #print("MODULE: No muons found. Skipping event...")
        return False

    return True

# muon-only reco selection
def recoSelMuOnly(t): # args: tree

    if (t.foundVertex != 1): 
        #print("MODULE SAYS NO VTX FOUND")
        return False

    n = t.nTracks

    # if (n < 3): 
    #     #print("MODULE: There aren't at least 3 tracks. Skipping...")
    #     return False

    s = t.nShowers
    twoSecPhoCount = 0

    for i in range(s): 
        if (t.showerProcess[i] == 0): 
            #print("MODULE: There is a primary shower. Skipping...")
            return False # skip all primary showers

    if (twoSecPhoCount > 1): 
        #print("MODULE: twoSecPhoCount > 1. Skipping...")
        return False

    flag = 0
    pions = 0
    muons = 0
    protons = 0
    NMomsP = []
    pdg = -999

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

        #print("MODULE: This is track #", i)

        # first check if it's a primary (code of 0)
        if (t.trackIsSecondary[i] != 0): 
            continue

        # does LArPID think it's a primary?
        if (t.trackProcess[i] != 0): 
            continue

        # LArPID PDG score
        #if (t.trackClassified[i] != 1):
        #    return False
        #else: 
        #    pdg = t.trackPID[i]

        if (t.trackClassified[i] == 1):
            pdg = t.trackPID[i]

        recoTID = t.trackTrueTID[i]

        # if (pdg == 211 or pdg == -211): 

        #     pions = pions + 1

        #     #print("MODULE: pions: ", pions)

        #     if (pions > 1):
        #         flag = 1
        #         #print("MODULE: pions > 1! Skipping...")
        #         return False

        #     recoPiE = t.trackRecoE[i]
        #     if (recoPiE > 0): 
        #         recoMomPi = recoMomCalc(recoPiE, piMass)

        #     if (recoMomPi > 0.07):
        #         pionsN = pionsN + 1
        #         leadingMomPi = recoMomPi

        #     if (pionsN > 1):
        #         flag = 1
        #         #print("MODULE: pions > 1! (Check #2). Skipping...")
        #         return False

        #     piTID = recoTID

        # Looking at muons
        if (pdg == 13): # mu 

            muons = muons + 1
         
            if (muons > 1):
                flag = 1
                #print("MODULE: muons > 1! Skipping...")
                return False

            recoMuE = t.trackRecoE[i]
            if (recoMuE > 0): 
                recoMomMu = recoMomCalc(recoMuE, muMass)

            if ( recoMomMu < 1.5 ):
                muonsN = muonsN + 1
                leadingMomMu = recoMomMu

            if (muonsN > 1):
                flag = 1
                #print("MODULE: muons > 1! (Check #2) Skipping...")
                return False

            muTID = recoTID

        # # Now look at protons
        # if (pdg == 2212):

        #     protons = protons + 1 

        #     recoPE = t.trackRecoE[i]
        #     if (recoPE > 0): 
        #         recoMomP = recoMomCalc(recoPE, pMass)
            
        #     if ( recoMomP > 0.30 and recoMomP < 1.0 ):
        #         NMomsP.append(recoMomP) # list of N protons in the event
        #         protonsN = protonsN + 1

        #         if ( recoMomP == max(NMomsP) ):
        #             leadingMomP = recoMomP

        #         pTID = recoTID

    # # require 
    # if ( pionsN == 0 ): 
    #     #print("Zero pions above threshold. Skip to next event.")
    #     return False

    # # we need at least one proton that passes cuts in my selection
    # if ( protonsN < 1 ): 
    #     #print("Zero protons above threshold. Skip to next event.")
    #     return False

    # only want 1 muon in my selection
    if ( muonsN == 0 ): 
        #print("Zero muons that meet threshold. Skip to next event.")
        return False

    return True

