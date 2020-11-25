"""
BDT_script.py

This script uses a weights file from a trained BDT to reduce background events from a root file

Based on an existing tutorial, originally written in C++

Author: Diyon Wickremeratne
"""

import ROOT, os, sys, array, numpy
from ROOT import TFile, TTree

"""

The Main function that will carry out automated analysis

"""
def run():

    ROOT.TMVA.Tools.Instance()

    #Where you store your tuples
    TUPLES = "/data/bfys/dwickrem/tuples/"
    
    #True if running on randomised data, else on regular data
    random_data = True

    #Specify the run you want to apply the BDT to
    run_number = "run_3"

    #Specify where you keep random and normal data inside TUPLES
    #Specify where you want your output files to be stored inside your parent output folder
    if(random_data):
        path = "random_data/"
        output = "blinded_random/"
    else:
        path = "bins/"
        output = "blinded/"
        

    weights_file = "/data/bfys/dwickrem/bdt_train_outputs/BDT_run61/BDT_Xic_pKpi_run61_100trees/weights/BDT_BDT_BDT_Xic_pKpi_run61_100trees.weights.xml"

    total_files = ["Xic_total.root"]

    print("\nBeginning the BDT script")

    TUPLES += run_number+"/"
    
    for i in os.listdir(TUPLES):

        #Ignore folders of clusters that may have not been deleted
        if "cluster" in i:
            continue

        #Ignore text files
        if "description" in i:
            continue

        year = "/"+i.split("_")[0]

        print("Passing total files through BDT for "+i.split("_")[0])

        for tot_file in total_files:

            print("Working on: "+tot_file)
            
            directory = "/data/bfys/dwickrem/root_outputs/"+output+run_number+year+"/"
            
            if not os.path.exists(directory):
                os.makedirs(directory)

            print(TUPLES+i+"/"+tot_file)

            runMVA(tot_file, TUPLES+i+"/"+tot_file, directory , weights_file)

        print("Done with total files")
        
        #Just makes sure to get the right directories
        if(random_data):
            for dset in os.listdir(TUPLES+i+"/random_data/"):

                print("\nWorking on: "+dset)

                for bin_type in os.listdir(TUPLES+i+"/random_data/"+dset+"/"):

                    print("\nFor the "+bin_type)

                    for root_file in os.listdir(TUPLES+i+"/random_data/"+dset+"/"+bin_type+"/"):

                        if not os.path.exists("/data/bfys/dwickrem/root_outputs/blinded_random/"+run_number+year+"/"+dset+"/"+bin_type+"/"):
                            os.makedirs("/data/bfys/dwickrem/root_outputs/blinded_random/"+run_number+year+"/"+dset+"/"+bin_type+"/")

                        saving_directory = "/data/bfys/dwickrem/root_outputs/blinded_random/"+run_number+year+"/"+dset+"/"+bin_type+"/"

                        print("\nWorking on: "+root_file)

                        runMVA(root_file, TUPLES+i+"/random_data/"+dset+"/"+bin_type+"/"+root_file, saving_directory, weights_file)
        else:
            for bin_type in os.listdir(TUPLES+i+"/bins/"):

                print("\nFor the "+bin_type)

                for root_file in os.listdir(TUPLES+i+"/bins/"+bin_type+"/"):

                    if not os.path.exists("/data/bfys/dwickrem/root_outputs/blinded/"+run_number+year+"/"+bin_type+"/"):
                        os.makedirs("/data/bfys/dwickrem/root_outputs/blinded/"+run_number+year+"/"+bin_type+"/")

                    saving_directory = "/data/bfys/dwickrem/root_outputs/blinded/"+run_number+year+"/"+bin_type+"/"

                    print("\nWorking on: "+root_file)

                    runMVA(root_file, TUPLES+i+"/bins/"+bin_type+"/"+root_file, saving_directory, weights_file)

    print("\nDone")


"""

List all your transformed variables here

"""

transformed_variables = ["log(lcplus_FD_OWNPV)",
                         "log(pplus_PT)",
                         "log(piplus_IP_OWNPV)",
                         "log(pplus_IP_OWNPV)",
                         "log(kminus_IP_OWNPV)",
                         "log(kminus_PT)",
                         "log(piplus_PT)",
                         "log(lcplus_PT)",
                         "log(kminus_IPCHI2_OWNPV)",
                         "log(piplus_IPCHI2_OWNPV)",
                         "log(pplus_IPCHI2_OWNPV)",
                         "sqrt(kminus_IPCHI2_OWNPV)",
                         "sqrt(pplus_IPCHI2_OWNPV)" ,
                         "sqrt(piplus_IPCHI2_OWNPV)" ,
                         "sqrt(kminus_IPCHI2_OWNPV + pplus_IPCHI2_OWNPV + piplus_IPCHI2_OWNPV)",
                         "log(kminus_PT + piplus_PT + pplus_PT)" ,
                         "pplus_P / (pplus_P + kminus_P + piplus_P)",
                         "lcplus_ENDVERTEX_CHI2 / lcplus_ENDVERTEX_NDOF"]

"""

You need to manually change these to return the proper string depending on the transformed variable

Due to time restrictions, it was easier to do it like this but I am sure there's an easier way

"""

def getCalculation(tvar):

    if tvar == "log(kminus_PT)":
        return "ROOT.TMath.Log(tree.kminus_PT)"

    if tvar == "lcplus_ENDVERTEX_CHI2 / lcplus_ENDVERTEX_NDOF":
        return "tree.lcplus_ENDVERTEX_CHI2 / tree.lcplus_ENDVERTEX_NDOF"

    if tvar == "pplus_P / (pplus_P + kminus_P + piplus_P)":
        return "tree.pplus_P / (tree.pplus_P + tree.kminus_P + tree.piplus_P)"

    if tvar == "log(kminus_PT + piplus_PT + pplus_PT)":
        return "ROOT.TMath.Log(tree.kminus_PT + tree.piplus_PT + tree.pplus_PT)"

    if tvar == "sqrt(kminus_IPCHI2_OWNPV + pplus_IPCHI2_OWNPV + piplus_IPCHI2_OWNPV)":
        return "ROOT.TMath.Sqrt(tree.kminus_IPCHI2_OWNPV + tree.pplus_IPCHI2_OWNPV + tree.piplus_IPCHI2_OWNPV)"

    if tvar == "log(piplus_IPCHI2_OWNPV)":
        return "ROOT.TMath.Log(tree.piplus_IPCHI2_OWNPV)"

    if tvar == "sqrt(piplus_IPCHI2_OWNPV)":
        return "ROOT.TMath.Sqrt(tree.piplus_IPCHI2_OWNPV)"

    if tvar == "log(pplus_IPCHI2_OWNPV)":
        return "ROOT.TMath.Log(tree.pplus_IPCHI2_OWNPV)"

    if tvar == "sqrt(pplus_IPCHI2_OWNPV)":
        return "ROOT.TMath.Sqrt(tree.pplus_IPCHI2_OWNPV)"
        
    if tvar == "log(kminus_IPCHI2_OWNPV)":
        return "ROOT.TMath.Log(tree.kminus_IPCHI2_OWNPV)"

    if tvar == "sqrt(kminus_IPCHI2_OWNPV)":
        return "ROOT.TMath.Sqrt(tree.kminus_IPCHI2_OWNPV)"

    if tvar == "log(lcplus_PT)":
        return "ROOT.TMath.Log(tree.lcplus_PT)"

    if tvar == "log(piplus_PT)":
        return "ROOT.TMath.Log(tree.piplus_PT)"

    if tvar == "log(lcplus_FD_OWNPV)":
        return "ROOT.TMath.Log(tree.lcplus_FD_OWNPV)"

    if tvar == "log(pplus_PT)":
        return "ROOT.TMath.Log(tree.pplus_PT)"

    if tvar == "log(piplus_IP_OWNPV)":
        return "ROOT.TMath.Log(tree.piplus_IP_OWNPV)"

    if tvar == "log(pplus_IP_OWNPV)":
        return "ROOT.TMath.Log(tree.pplus_IP_OWNPV)"

    if tvar == "log(kminus_IP_OWNPV)":
        return "ROOT.TMath.Log(tree.kminus_IP_OWNPV)"
        
"""

This function carries out the TMVA analysis

Parameters are a file name, the root file to analyse, where you want to save it and finally the weights file you want to use

"""
def runMVA(file_name, root_file, saving_directory, weights_file):

    reader = ROOT.TMVA.Reader("V:Color:!Silent")

    #Variables used in training. must be in exact order
    variables =['lcplus_RAPIDITY',
                'piplus_RAPIDITY',
                'pplus_RAPIDITY',
                'kminus_RAPIDITY',
                'lcplus_ENDVERTEX_CHI2',
                'lcplus_ENDVERTEX_NDOF',
                'lcplus_IPCHI2_OWNPV',
                'pplus_OWNPV_CHI2',
                'pplus_P', 
                'pplus_PT',
                'kminus_P', 
                'kminus_PT',
                'piplus_P', 
                'piplus_PT',
                'kminus_PIDK', 
                'kminus_PIDp',
                'piplus_PIDK', 
                'piplus_PIDp',
                'pplus_PIDK', 
                'pplus_PIDp',
                'kminus_OWNPV_CHI2',
                'piplus_OWNPV_CHI2',
                'lcplus_IP_OWNPV',
                'piplus_ProbNNpi',
                'pplus_ProbNNp',
                'kminus_ProbNNk',
                'pplus_TRACK_PCHI2',
                'piplus_TRACK_PCHI2',
                'kminus_TRACK_PCHI2',
                'pplus_MC15TuneV1_ProbNNp',
                'pplus_MC15TuneV1_ProbNNk',
                'pplus_MC15TuneV1_ProbNNpi',
                'pplus_MC15TuneV1_ProbNNghost',
                'kminus_MC15TuneV1_ProbNNp',
                'kminus_MC15TuneV1_ProbNNk',
                'kminus_MC15TuneV1_ProbNNpi',
                'kminus_MC15TuneV1_ProbNNghost',
                'piplus_MC15TuneV1_ProbNNp',
                'piplus_MC15TuneV1_ProbNNk',
                'piplus_MC15TuneV1_ProbNNpi',
                'piplus_MC15TuneV1_ProbNNghost']

    for t in transformed_variables:
        variables.append(t)

    print(len(variables))

    #Create an array per variable. The reader needs a variable of type array
    n = 0
    for var in variables:
        exec('var'+str(n)+' = array.array(\'f\',[0])')
        exec('reader.AddVariable("'+var+'",var'+str(n)+')')
        n+=1

    reader.BookMVA('BDT', weights_file)

    read_file = ROOT.TFile(root_file, "READ")
    dataTree = read_file.Get("DecayTree")

    MVAOutput = numpy.zeros(1, dtype=float) 
    save_file = ROOT.TFile.Open(saving_directory+"BDT_"+file_name,"RECREATE")

    tree = dataTree.CopyTree("0")
    tree.Branch('BDT_response', MVAOutput,'BDT_response/D') 
    N = dataTree.GetEntries()

    #Evaluate each entry, fill tree
    for i in range(N):

        if (i%10000 == 0):
            k = (i / N)*100
            sys.stdout.write('\r')
            sys.stdout.write("Progress: {0}%".format(str(int(k))))
            sys.stdout.flush()

        dataTree.GetEntry(i)

        a = 0
        for var in variables:

            #print(var)

            #this is to get the final calculation of the transformed variables
            if "log(" in var:
                exec('var'+str(a)+'[0] = '+getCalculation(var))

            elif "sqrt(" in var:
                exec('var'+str(a)+'[0] = '+getCalculation(var))

            elif "/" in var:
                exec('var'+str(a)+'[0] = '+getCalculation(var))

            else:
                exec('var'+str(a)+'[0] = tree.'+var)
            a += 1

        MVAOutput[0] = reader.EvaluateMVA('BDT')
        tree.Fill()

    sys.stdout.write('\r')
    sys.stdout.write("Progress: 100%")
    sys.stdout.flush()
     
    tree.Write("", ROOT.TObject.kOverwrite)
    save_file.Write("", ROOT.TObject.kOverwrite)
    save_file.Close()
    
"""

There is an option to run it on one particular root file by entering the appropriate arguments after the python command.

Usage: >python BDT_script.py <path to root file> <saving directoy>

"""

if __name__ == '__main__':
    
    if(len(sys.argv) == 3):

        root_file = sys.argv[1]

        strings = root_file.split("/")
        index = len(strings)-1
        name = strings[index]

        saving_directory = sys.argv[2]

        wf = "/data/bfys/dwickrem/bdt_train_outputs/BDT_run61/BDT_Xic_pKpi_run61_100trees/weigts/BDT_BDT_BDT_Xic_pKpi_run61_100trees.weights.xml"

        runMVA(name, root_file, saving_directory, wf)

    else:
        run()


