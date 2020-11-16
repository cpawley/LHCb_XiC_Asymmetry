"""

This is a script for the preparation of tuples from the grid

Dependencies: Imports.py , write_descriptions.py

Authors: Simon Calo, Jonas Tjepkema, Diyon Wickremeratne

"""

import ROOT, os, Imports, sys, numpy, time
from ROOT import TChain, TFile, TTree
from Imports import TUPLE_PATH, RAW_TUPLE_PATH, DATA_jobs_Dict, MC_TUPLE_PATH, MC_jobs_Dict
from numpy import random
from write_descriptions import makeFile, appendBins, appendVars, writeStartOfRandomisation, appendTreeAnalysis, appendTimeElapsed

"""

This method automatically gets the number of times you have run this script

"""
def getRun():
    PATH = TUPLE_PATH
    runs = []
    if (len(os.listdir(PATH))==0):
        run = 1
        return "run_"+str(run)
    else:
        for i in os.listdir(PATH):
            string = i.split("_")
            runs.append(int(string[1]))
        return "run_"+str(numpy.max(runs)+1)


def prepMC():
    print("Prepping MC")

    MC_PATH = MC_TUPLE_PATH

    RAW_TUPLES = RAW_TUPLE_PATH

    TESTING = True

    if not os.path.exists(MC_PATH):
        os.makedirs(MC_PATH)
    
    blind_data = True

    useful_variables = []
    
    if(blind_data):

        variables = ["lcplus_MM", 
                       "lcplus_P", 
                       "lcplus_PT", 
                       "lcplus_ETA",
                       "lcplus_RAPIDITY", 
                       "lcplus_TIP", 
                       "lcplus_IPCHI2_OWNPV", 
                       "lcplus_OWNPV_CHI2", 
                       "lcplus_TAU",
                       "lcplus_IP_OWNPV",
                       "lcplus_L0HadronDecision_TOS", 
                       "lcplus_FD_OWNPV",
                       "lcplus_ENDVERTEX_CHI2",
                       "pplus_M", 
                       "pplus_P", 
                       "pplus_PT",
                       "pplus_RAPIDITY", 
                       "pplus_ETA",
                       "pplus_ProbNNp",
                       "pplus_OWNPV_CHI2",
                       "kminus_OWNPV_CHI2",
                       "piplus_OWNPV_CHI2",
                       "piplus_M",
                       "piplus_P", 
                       "piplus_PT", 
                       "piplus_RAPIDITY",
                       "piplus_ETA",
                       "piplus_ProbNNpi",
                       "piplus_IP_OWNPV",
                       "pplus_PIDp",
                       "kminus_M",
                       "kminus_P", 
                       "kminus_PT", 
                       "kminus_RAPIDITY",
                       "kminus_ETA",
                       "kminus_ProbNNk", 
                       "kminus_PIDK", 
                       "PVNTRACKS",
                       "piplus_PX", 
                       "pplus_PX", 
                       "kminus_PX", 
                       "piplus_PY", 
                       "pplus_PY", 
                       "kminus_PY", 
                       "piplus_PZ", 
                       "pplus_PZ", 
                       "kminus_PZ",
                       "pplus_IP_OWNPV",
                       "kminus_IP_OWNPV",
                       "kminus_IPCHI2_OWNPV",
                       "piplus_IPCHI2_OWNPV",
                       "pplus_IPCHI2_OWNPV",
                       "pplus_TRACK_PCHI2",
                       "piplus_TRACK_PCHI2",
		       "kminus_TRACK_PCHI2"]

        useful_variables = variables
        
    else:
        variables = ["lcplus_MM", 
                       "lcplus_P", 
                       "lcplus_PT", 
                       "lcplus_ETA",
                       "lcplus_RAPIDITY", 
                       "lcplus_TIP", 
                       "lcplus_IPCHI2_OWNPV", 
                       "lcplus_OWNPV_CHI2", 
                       "lcplus_TAU",
                       "lcplus_L0HadronDecision_TOS", 
                       "lcplus_FD_OWNPV",
                       "pplus_M", 
                       "pplus_P", 
                       "pplus_PT",
                       "pplus_RAPIDITY", 
                       "pplus_ETA",
                       "pplus_ProbNNp",
                       "piplus_M",
                       "piplus_P", 
                       "piplus_PT", 
                       "piplus_RAPIDITY",
                       "piplus_ETA",
                       "piplus_ProbNNpi",
                       "pplus_PIDp",
                       "kminus_M",
                       "kminus_P", 
                       "kminus_PT", 
                       "kminus_RAPIDITY",
                       "piplus_IP_OWNPV",
                       "kminus_ETA",
                       "kminus_ProbNNk", 
                       "kminus_PIDK",
                       "PVNTRACKS", 
                       "piplus_PX", 
                       "pplus_PX", 
                       "kminus_PX", 
                       "piplus_PY",
                       "pplus_PY", 
                       "kminus_PY", 
                       "piplus_PZ",
                       "pplus_PZ", 
                       "kminus_PZ",
                       "pplus_IP_OWNPV",
                       "kminus_IP_OWNPV",
                       "kminus_IPCHI2_OWNPV",
                       "piplus_IPCHI2_OWNPV",
                       "pplus_IPCHI2_OWNPV"]

        useful_variables = variables


    if(TESTING):
        dictionary = {"108":["2016","MagDown", 282,"Xic","26103090"]}
    else:
        dictionary = MC_jobs_Dict

    for element in dictionary:
        print("Currently working on "+dictionary[element][0] +"_"+ dictionary[element][1])
        if int(element) > 41 and int(element) < 47:
            extra_variables = ["lcplus_Hlt1TrackAllL0Decision_TOS", "lcplus_Hlt2CharmHadD2HHHDecision_TOS","*L0*","*Hlt*","*HLT*"]
            run = 1
            particle = "Lc"
            
        else:
            extra_variables = ["nSPDHits", "nTracks", "lcplus_Hlt1TrackMVADecision_TOS"]
            particle = dictionary[element][3]
            run = 2

        for extra_variable in extra_variables:
            if not (extra_variable == ""):
                useful_variables.append(extra_variable)

        if(blind_data):
            saving_directory = MC_PATH + dictionary[element][0] +"_"+ dictionary[element][1]+"_blinded/"
        else:
            saving_directory = MC_PATH + dictionary[element][0] +"_"+ dictionary[element][1]+"/"

        if not os.path.exists(saving_directory):
            os.makedirs(saving_directory)

        tfile = ROOT.TFile.Open(saving_directory+particle+"_MC_total.root","RECREATE")

        tree = ROOT.TChain("tuple_Lc2pKpi/DecayTree")

        subjobs = dictionary[element][2]

        print("Adding files to TChain")
        for i in range(subjobs):
            mc_file = RAW_TUPLES+element+"/"+str(i)+"/MC_Lc2pKpiTuple_"+dictionary[element][4]+".root"
            if os.path.exists(RAW_TUPLES+element+"/"+str(i)+"/"):
                tree.Add(mc_file)

        if(tree.GetEntries() == 0) or (tree.GetEntries() == -1):
            print("Stopped creation of "+dictionary[element][0] +"_"+ dictionary[element][1]+" as there were 0 entries")
            tfile.Close()
            del tfile
            os.system("rm -rf {}".format(saving_directory+particle+"_MC_total.root"))
            continue

        print("Activating useful branches on the tree")
        tree = setBranch_function(tree, useful_variables)
        cuts = Imports.getDataCuts(run, blinded = blind_data)

        tfile.cd()
        print("Skimming tree and writing to a new root file")
        new_tree = tree.CopyTree(cuts)
        new_tree.Write("", ROOT.TObject.kOverwrite)
        tfile.Write("", ROOT.TObject.kOverwrite)
        tfile.Close()

    print("Finished prepping MC")


"""

Main function

"""
def main(script_run):
    print ("Starting main")

    #If you want to test on a small portion of data, then enable it here and add the data to the dictionary below
    TESTING = True

    if(TESTING):
        folders_dict = {"115":["2016_MagDown",186,"Xic"]}
    else:
        #Dictionary for all the data
        folders_dict = DATA_jobs_Dict
    
    #Path to save the tuples
    PATH = TUPLE_PATH+script_run+"/"

    if not os.path.exists(PATH):
        os.makedirs(PATH)
    
    blind_data = True

    makeFile(PATH, script_run, dictionary = folders_dict, blinded = blind_data)

    useful_variables = []
    
    if(blind_data):

        variables = ["lcplus_MM", 
                       "lcplus_P", 
                       "lcplus_PT", 
                       "lcplus_ETA",
                       "lcplus_RAPIDITY", 
                       "lcplus_TIP", 
                       "lcplus_IPCHI2_OWNPV", 
                       "lcplus_OWNPV_CHI2", 
                       "lcplus_TAU",
                       "lcplus_IP_OWNPV",
                       "lcplus_L0HadronDecision_TOS", 
                       "lcplus_FD_OWNPV",
                       "lcplus_ENDVERTEX_CHI2",
                       "pplus_M", 
                       "pplus_P", 
                       "pplus_PT",
                       "pplus_RAPIDITY", 
                       "pplus_ETA",
                       "pplus_ProbNNp",
                       "pplus_OWNPV_CHI2",
                       "kminus_OWNPV_CHI2",
                       "piplus_OWNPV_CHI2",
                       "piplus_M",
                       "piplus_P", 
                       "piplus_PT", 
                       "piplus_RAPIDITY",
                       "piplus_ETA",
                       "piplus_ProbNNpi",
                       "piplus_IP_OWNPV",
                       "pplus_PIDp",
                       "kminus_M",
                       "kminus_P", 
                       "kminus_PT", 
                       "kminus_RAPIDITY",
                       "kminus_ETA",
                       "kminus_ProbNNk", 
                       "kminus_PIDK", 
                       "PVNTRACKS",
                       "piplus_PX", 
                       "pplus_PX", 
                       "kminus_PX", 
                       "piplus_PY", 
                       "pplus_PY", 
                       "kminus_PY", 
                       "piplus_PZ", 
                       "pplus_PZ", 
                       "kminus_PZ",
                       "pplus_IP_OWNPV",
                       "kminus_IP_OWNPV",
                       "kminus_IPCHI2_OWNPV",
                       "piplus_IPCHI2_OWNPV",
                       "pplus_IPCHI2_OWNPV",
                       "pplus_TRACK_PCHI2",
                       "piplus_TRACK_PCHI2",
		       "kminus_TRACK_PCHI2"]

        useful_variables = variables
        
    else:
        variables = ["lcplus_MM", 
                       "lcplus_P", 
                       "lcplus_PT", 
                       "lcplus_ETA",
                       "lcplus_RAPIDITY", 
                       "lcplus_TIP", 
                       "lcplus_IPCHI2_OWNPV", 
                       "lcplus_OWNPV_CHI2", 
                       "lcplus_TAU",
                       "lcplus_L0HadronDecision_TOS", 
                       "lcplus_FD_OWNPV",
                       "pplus_M", 
                       "pplus_P", 
                       "pplus_PT",
                       "pplus_RAPIDITY", 
                       "pplus_ETA",
                       "pplus_ProbNNp",
                       "piplus_M",
                       "piplus_P", 
                       "piplus_PT", 
                       "piplus_RAPIDITY",
                       "piplus_ETA",
                       "piplus_ProbNNpi",
                       "pplus_PIDp",
                       "kminus_M",
                       "kminus_P", 
                       "kminus_PT", 
                       "kminus_RAPIDITY",
                       "piplus_IP_OWNPV",
                       "kminus_ETA",
                       "kminus_ProbNNk", 
                       "kminus_PIDK",
                       "PVNTRACKS", 
                       "piplus_PX", 
                       "pplus_PX", 
                       "kminus_PX", 
                       "piplus_PY",
                       "pplus_PY", 
                       "kminus_PY", 
                       "piplus_PZ",
                       "pplus_PZ", 
                       "kminus_PZ",
                       "pplus_IP_OWNPV",
                       "kminus_IP_OWNPV",
                       "kminus_IPCHI2_OWNPV",
                       "piplus_IPCHI2_OWNPV",
                       "pplus_IPCHI2_OWNPV"]

        useful_variables = variables
        

    appendVars(PATH, script_run, variables = useful_variables)
    
    for element in folders_dict:
        if int(element) > 41 and int(element) < 47:
            extra_variables = ["lcplus_Hlt1TrackAllL0Decision_TOS", "lcplus_Hlt2CharmHadD2HHHDecision_TOS","*L0*","*Hlt*","*HLT*"]
            run = 1
            particle = "Lc"
            
        else:
            extra_variables = ["nSPDHits", "nTracks", "lcplus_Hlt1TrackMVADecision_TOS"]
            particle = folders_dict[element][2]
            run = 2

        for extra_variable in extra_variables:
            if not (extra_variable == ""):
                #If an extra variable is needed, it will be appended
                useful_variables.append(extra_variable)
        
        
        subjobs = folders_dict[element][1]
        
        if (blind_data):
             name = folders_dict[element][0]+"_blinded"
            
        else:
             name = folders_dict[element][0]
        
        saving_directory = PATH+name+"_clusters/"

        cuts = Imports.getDataCuts(run, blinded = blind_data)
        
        if not os.path.exists(saving_directory):
            os.makedirs(saving_directory)
        
        file_directory = RAW_TUPLE_PATH+element
        
        print("\nStarting process for "+name)
        
        #Carries out the process in steps of 20
        step = subjobs//20
        Max = step
        Min = 0
        
        #Clusters are created here
        print("Creation of clusters")
        n = 20 
        i = 0 
        
        while (Max<=subjobs):
            #Progress bar
            if (i<n):
                j = (i+1)/n
                sys.stdout.write("\r")
                sys.stdout.write("[%-20s] %d%%" % ('='*int(20*j), 100*j))
                sys.stdout.flush()
                i+=1
                
            if (Max == Min):
                break
                
            strip_and_save(Min, Max, cuts, file_directory, saving_directory, useful_variables, particle)
            
            temp = Max
            
            if (Max+step > subjobs):
                Max = subjobs
            
            else:
                Max+=step
                
            Min = temp
            
        clusters = os.listdir(saving_directory)
        
        print("\n\nTChaining the clusters")
        
        final_chain = TChain("DecayTree")
        
        n = len(clusters)
        i = 0
        
        for element in clusters:
            if (i<n):
                j = (i+1)/n 
                sys.stdout.write('\r')
                sys.stdout.write("[%-20s] %d%%" % ('='*int(20*j), 100*j))
                sys.stdout.flush()
                i += 1
            final_chain.Add(saving_directory+element)
            
        if not os.path.exists(PATH+name+"/bins"):
            os.makedirs(PATH+name+"/bins")
            
        saving_directory = PATH+name+"/bins/"
        
        print("\n\nCreating the final files")
        
        split_in_bins_and_save(final_chain, saving_directory, run, useful_variables, particle)
        
        print("\nProcess completed for "+name)
        
    #Creation of the total Year Data files 
    print("\nCreation of the total year data files")
    
    mother_particle = ["Xic","Lc"]
    
    BASE_PATH = TUPLE_PATH+script_run+"/"
    
    n = len(os.listdir(BASE_PATH))
    p = 0 
    
    for i in os.listdir(BASE_PATH):

        if (p < n):
            j = (p + 1) / n
            sys.stdout.write('\r')
            sys.stdout.write("[%-20s] %d%%" % ('='*int(20*j), 100*j))
            sys.stdout.flush()
            p += 1

        if "description" in i:
            continue
            
        if "cluster" in i:
            continue
            
        for particle in mother_particle:
                
            totfile = ROOT.TFile.Open(BASE_PATH+i+"/{}_total.root".format(particle),"RECREATE")
            totfile.cd()
            
            tree = TChain("DecayTree")
                
            for j in os.listdir(BASE_PATH+i+"/bins/ybins"):
                if particle in j:
                    tree.Add(BASE_PATH+i+"/bins/ybins/"+j)
            
            tree.Write()
            totfile.Close()
            
            del totfile

    print("\nDeleting clusters")

    os.system("rm -rf {}*_clusters".format(BASE_PATH))
            
    print("\nNTuple preparation is done")

    
"""

Returns a pruned tree from the root file that is fed into the function

"""
def setBranch_function(root_file, useful_variables):

    #Depends on the type of file being fed into the function
    tfile = root_file
    #First deactivate all branches
    tfile.SetBranchStatus("*",False)
    
    #Reactivate useful ones
    for element in useful_variables:
        tfile.SetBranchStatus(element,True)
        
    return tfile
    
"""

Takes in a root file with a DecayTree. Divides the tree into bins and saved in the saving_directory

"""
def split_in_bins_and_save(root_file, saving_directory, run, useful_variables, mother_particle = "Lc"):
    
    #Rapidity and transverse momentum
    ybins = Imports.getYbins()
    ptbins = Imports.getPTbins()
    
    if (run==1):
        particles = ["Lc","Xic"]
    else:
        particles = []
        particles.append(mother_particle)
        
    if not os.path.exists(saving_directory + "ybins/"):
        os.makedirs(saving_directory + "ybins/")
        
    if not os.path.exists(saving_directory + "ptbins/"):
        os.makedirs(saving_directory + "ptbins/")
        
    if not os.path.exists(saving_directory + "y_ptbins/"):
        os.makedirs(saving_directory + "y_ptbins/")
    
    tree = root_file
    
    for particle in particles:
        if particle == "Lc":
            mass_cuts = "lcplus_MM < 2375"
        if particle == "Xic":
            mass_cuts = "lcplus_MM > 2375"
            
    for ybin in ybins:
    
        ycuts = "lcplus_RAPIDITY >= {0} && lcplus_RAPIDITY < {1}".format(ybin[0], ybin[1])
        allcuts = " {0} && {1}".format(ycuts, mass_cuts)
        
        strip_and_save(0, 0, allcuts, "", saving_directory+"ybins/"+particle+"_ybin_{0}-{1}.root".format(ybin[0],ybin[1]), useful_variables, particle, bins = True, tree = tree)
        
        n = len(ptbins)
        i = 0
        
        print("Files with y({0})".format(ybin))
        
        for ptbin in ptbins:
            #Progress bar
            if(i<n):
                j = (i + 1) / n
                sys.stdout.write('\r')
                sys.stdout.write("[%-20s] %d%%" % ('='*int(20*j), 100*j))
                sys.stdout.flush()
                i += 1
            
            ptcuts = "lcplus_PT >= {0} && lcplus_PT < {1}".format(ptbin[0], ptbin[1])
            
            if (ybin[0]==2.0):
                allcuts = " {0} && {1}".format(ptcuts, mass_cuts)
                strip_and_save(0, 0, allcuts, "", saving_directory + "ptbins/" + particle + "_ptbin_{0}-{1}.root".format(ptbin[0], ptbin[1]), useful_variables, particle, bins = True,tree = tree)
                
            ypt_cut = ycuts+"&&"+ptcuts
            allcuts = "{0} && {1}".format(ypt_cut, mass_cuts)
            
            strip_and_save(0, 0, allcuts, "", saving_directory + "y_ptbins/" + particle + "_ybin_{0}-{1}_ptbin_{2}-{3}.root".format(ybin[0],ybin[1],ptbin[0],ptbin[1]), useful_variables, particle, bins = True, tree = tree)
            
        print("\n")
        
"""

Takes a range of TChained subjobs, applies cuts and saves it  

"""
def strip_and_save(Min, Max, cuts, directory, saving_directory, useful_variables, particle, bins = False, tree = None):
    
    if not (bins):
        filename = "{0}2pKpiTuple.root".format(particle)
        
        extra_dir = ""

        alldata = ROOT.TChain("tuple_{0}2pKpi/DecayTree".format(particle))

        for job in range(Min,Max):

            if os.path.isfile("{0}/{1}{2}/{3}".format(directory,job,extra_dir,filename)):

                alldata.Add("{0}/{1}{2}/{3}".format(directory,job,extra_dir,filename))
                
        
        #Check for errors in the data
        if (alldata.GetEntries() == 0):
            print("Error: entries = 0 for range " + str(Min) + "-" + str(Max))
            return
            
        if (alldata.GetEntries() == -1):
            print("Error: entries = -1 for range " + str(Min) + "-" + str(Max))
            return

        alldata = setBranch_function(alldata, useful_variables)
        extra_string = particle + "_cluster_{0}-{1}.root".format(Min, Max)
        
    else:
        if not (tree==None):
            alldata = tree
        
        extra_string = ""
        
    wfile = TFile.Open(saving_directory + extra_string, "RECREATE")
    subtree = alldata.CopyTree(cuts)
    wfile.cd()
    subtree.Write("",ROOT.TObject.kOverwrite)
    wfile.Write("",ROOT.TObject.kOverwrite)
    wfile.Close()

"""

This function conducts the randomisation process in which it sorts events from each data folder into two datasets. Useful in the
case of a blinded analysis

"""

def randomise(script_run):
    
    bins = ["ybins","ptbins","y_ptbins"]

    print ("Beginning randomise")

    PATH = TUPLE_PATH+script_run+"/"

    writeStartOfRandomisation(PATH, script_run)

    for i in os.listdir(PATH):

        if "description" in i:
            continue

        if "cluster" in i:
            continue
        
        print("\nWorking on "+i+" data")
        
        for bin_type in bins:

            print("\nFor the "+bin_type)

            ##DATASET1
            if not os.path.exists(PATH+i+"/random_data/dataset1/"+bin_type+"/"): 
                os.makedirs(PATH+i+"/random_data/dataset1/"+bin_type+"/")

            ##DATASET2
            if not os.path.exists(PATH+i+"/random_data/dataset2/"+bin_type+"/"): 
                os.makedirs(PATH+i+"/random_data/dataset2/"+bin_type+"/")

        
            for root_file in os.listdir(PATH+i+"/bins/"+bin_type+"/"):
                
                print("\nRandomising: "+root_file)

                name = root_file

                read_file = ROOT.TFile(PATH+i+"/bins/"+bin_type+"/"+name, "READ")
                dataTree = read_file.Get("DecayTree")

                file1 = ROOT.TFile.Open(PATH+i+"/random_data/dataset1/"+bin_type+"/"+name,"RECREATE")
                file2 = ROOT.TFile.Open(PATH+i+"/random_data/dataset2/"+bin_type+"/"+name,"RECREATE")
                file1.cd()
                tree1 = dataTree.CloneTree(0)
                file2.cd()
                tree2 = dataTree.CloneTree(0)
                
                n = dataTree.GetEntries()
                x = 0

                
                for entry in range(dataTree.GetEntries()):

                    dataTree.GetEntry(entry)

                    #Progress 
                    if(x%1000==0):
                        j = (x / n)*100
                        sys.stdout.write('\r')
                        sys.stdout.write("{0}%".format(str(int(j))))
                        sys.stdout.flush()
                                          
                
                    #50% probability of being added to dataset1 or dataset2
                    if(random.rand()>0.5):
                        tree1.Fill()
                        
                    else:
                        tree2.Fill()

                    x+=1
    

                sys.stdout.write("\r")
                sys.stdout.write("100%")
                sys.stdout.flush()

                appendTreeAnalysis(PATH, script_run, i,  name, dataTree.GetEntries(), tree1.GetEntries(),tree2.GetEntries())

                tree1.SetName("DecayTree")
                file1.cd()
                tree1.Write("",ROOT.TObject.kOverwrite)
                print("\nEvents in tree1: "+str(tree1.GetEntries()))
                file1.Close()
                
                tree2.SetName("DecayTree")
                file2.cd()
                tree2.Write("",ROOT.TObject.kOverwrite)
                print("\nEvents in tree2: "+str(tree2.GetEntries()))
                file2.Close()

                read_file.Close()

                print("\nRandomisation finished for: "+name)

                

if __name__ == '__main__':

    start = time.time()

    script_run = getRun()

    #prepMC()
    main(script_run)
    randomise(script_run)

    appendTimeElapsed(TUPLE_PATH+script_run+"/" , script_run, (time.time() - start))
