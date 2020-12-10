"""
This script appends efficiency values to a run's description file
"""

import ROOT, os, sys, numpy
import write_descriptions
from write_descriptions import appendEfficiency

RUN = "3"
ASYMMETRY_FILE = "/data/bfys/dwickrem/pdf_outputs/mass_fits/blinded_random/run_{}/".format(RUN)
MC = "/data/bfys/dwickrem/mc_tuples/"
BDT_MC = "/data/bfys/dwickrem/root_outputs/mc_blinded/"
CUT = "BDT_response > -0.12"

HANDLES = ["-bdt"]

def computeBDTEfficiency():

    name = "BDT"

    tries = 10

    efficiencies = []

    for folder in os.listdir(MC):
        year = folder.split("_")[0]
        
        outDir = BDT_MC+year+"/"
        
        if not os.path.exists(outDir):
            os.makedirs(outDir)
        
        i = 0
        while (i < tries):

            print("Iteration: "+str(i))

            print("Opening the MC file")
            mc_file = MC+folder+"/Xic_MC_total.root"

            total_file = ROOT.TFile.Open(mc_file, "READ")
            total_tree = total_file.Get("DecayTree")
            
            temp_file = ROOT.TFile.Open(outDir+"temp.root","RECREATE")
            reduced_tree = total_tree.CloneTree(0)

            print("Reducing tree to the fraction of training events")
            temp_file.cd()
            for e in range(total_tree.GetEntries()):
                
                total_tree.GetEntry(e)

                if(numpy.random.random() > 0.65):
                    reduced_tree.Fill()

            reduced_tree.SetName("DecayTree")
            reduced_tree.Write("",ROOT.TObject.kOverwrite)
            temp_file.Write("",ROOT.TObject.kOverwrite)
            temp_file.Close()

            total_file.Close()
                
            print("Passing through BDT")
            os.system("python BDT_script.py {} {}".format(outDir+"temp.root",outDir))
            
            root_file = ROOT.TFile.Open(outDir+"BDT_temp.root","READ")
            tree = root_file.Get("DecayTree")
       
            cut_tree = tree.CopyTree(CUT)

            value = cut_tree.GetEntries() / tree.GetEntries()

            efficiencies.append(value)

            root_file.Close()

            del temp_file
            del root_file
            os.system("rm {}".format(outDir+"BDT_temp.root"))
            os.system("rm {}".format(outDir+"temp.root"))

            i+=1
            
        print("Computing BDT efficiency...")

        mean = numpy.mean(efficiencies)

        uncertainty = (numpy.amax(efficiencies) - numpy.amin(efficiencies))/2

        string = str(mean)+" +/ "+str(uncertainty)

        appendEfficiency(ASYMMETRY_FILE+year+"/",name, string, year)

        print("Done")

if __name__ == '__main__':
    
    if(len(sys.argv) !=  2):
        print("\nPlease use one handle: >python compute_efficiencies.py <handle>")
        print("\nAvailable handles are: ")
        print(HANDLES)
        sys.exit()

    if(sys.argv[1] == HANDLES[0]):
        computeBDTEfficiency()


        
