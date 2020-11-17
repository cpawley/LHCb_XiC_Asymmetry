#########
# sWeights for XiC Assym
# Author: Chris Pawley
# Last Update: 16 November 2020
########


import sys
import ROOT, Imports, os
from Imports import *


#####

# multiple steps - which do we want to do today?
getData = True
makesWeights = False
makeFriendTree = False
plotVariable = False
testFriendTree = False

#

# Input Dir is where the reduced tuples live; output is where we will create the sWeights files and friend trees

InputDir = "/data/bfys/dwickrem/tuples/run_2/"
OutputDir = "/data/bfys/cpawley/sWeights-XiC/"

#Years, Magpol, and particle types

years = [2016]
magPol = ["MagDown"]
particle_types = ["Xic"]
datasets = ["dataset1", "dataset2"]

# y and Pt bins may vary, we should import them - we can borrow some code from the other analysis - this is to do

def main (argv):
    global outputdir
    #STOP root plotting so much
    ROOT.gROOT.SetBatch(True)



    #Here we would parse the command line requirements for us to check - borrow code when needed

    


    if(getData):
        print ("I am getting your data file(s)")
        #just to keep us informed
        
        #getthedata - to be more complex in future
        print(InputDir+"{0}_{1}_blinded/random_data/{2}".format(years[0],magPol[0],datasets[0]))
        f1 = ROOT.TFile.Open(InputDir+"{0}_{1}_blinded/random_data/{2}".format(years[0],magPol[0],datasets[0]))

        f2 = ROOT.TFile.Open(InputDir+"{0}_{1}_blinded/random_data/{2}".format(years[0],magPol[0],datasets[1]))
        
        tree1=f1.Get("DecayTree")
        tree2.f2.Get("DecayTree")

        cuts = "(1==1"


        mass = ROOT.RooRealVar("lcplus_MM", "XiCMass", 2420, 2520, "MeV/c^{2}")



    if (makesWeights):
        print ("making sWeights")
    

    return

if __name__=="__main__":
    main(sys.argv[1:])

        
