"""
This script is used to cut the 'raw' data from the detector into smaller
data files containing only variables and events we want to look at. The
script has two options:
	- Store all data in two (signal and background) big data files
	- Store all data in two (signal and background) folders in a lot of
	  smaller files

Author: Maris Koopmans
"""

import os, sys
import time
import ROOT

def cut_tree(label, path, extension, jobs, filter_str, variables, tree_name):
    """
    This function is used to store all 'raw' data in two big files
    """

    # Start the tree chain
    tree_raw = ROOT.TChain(tree_name)

    # Chain all 'small file' trees together
    for job in range(jobs):
        chain_file = path + f'/{job}/{extension}'
        tree_raw.Add(chain_file)

    # Deactivate all branches we don't look at
    tree_raw.SetBranchStatus('*', 0)
    for var in variables:
        tree_raw.SetBranchStatus(var, 1)

    # Define the output file
    out_file = ROOT.TFile(f'/data/bfys/dwickrem/sig_bkg_folder/{label}_cut.root', 'recreate')

    # Apply the filters
    tree_cut = tree_raw.CopyTree(filter_str)

    out_file.Write()

    print(f'Succesfully cut and written {label} data to output file')


def cut_tree_small_files(label, path, extension, jobs, filter_str, variables, tree_name):
    """
    This function is used to store all 'raw' data in a lot of small files,
    keeping the same structure as in the original data.
    """
    if not os.path.exists("/data/bfys/dwickrem/sig_bkg_folder/{}_finalvars_sigsmall/".format(label)):
        os.makedirs("/data/bfys/dwickrem/sig_bkg_folder/{}_finalvars_sigsmall/".format(label))

    # For all small data files, create a new and smaller data file with cuts applied
    for job in range(jobs):

        if(label == "background") and (job == 170):
            continue

        # Define the file
        chain_file = path + "/{}/{}".format(job,extension)

        # Open the file and get the tree
        f = ROOT.TFile.Open(chain_file,"READ")
        tree_raw = f.Get(tree_name)
        
        # Deactivate all branches we don't look at
        tree_raw.SetBranchStatus('*', False)
        for var in variables:

            if (label == "background") and (var == "lcplus_PVConstrainedDTF_chi2"):
                continue

            tree_raw.SetBranchStatus(var, True)

        # Define the output file
        out_file = ROOT.TFile("/data/bfys/dwickrem/sig_bkg_folder/{}_finalvars_sigsmall/{}_cut_{}.root".format(label,label,job), "RECREATE")
            
        # Apply the filters
        tree_cut = tree_raw.CopyTree(filter_str)
            
        out_file.Write()

        f.Close()
            
    print("Succesfully cut and written {} data to output files".format(label))


def main():
    """
    This function defines the locations and subfolders of the data folder,
    variables and filter string. It then calls the desired cut function
    """

    start_time = time.time()
    # Define the folders and files where the data can be found
    filepath = "/dcache/bfys/jdevries/ntuples/LcAnalysis/ganga"
    sig_files = "/108"
    sig_subjobs = 282
    bkg_files = "/115"
    bkg_subjobs = 185
    signal_tree_name = "tuple_Lc2pKpi/DecayTree"
    background_tree_name = "tuple_Xic2pKpi/DecayTree"

    # Tree file for MC data
    sig_file = filepath + sig_files
    # Tree file for detector data
    bkg_file = filepath + bkg_files

    # Filter the signal, checking that the particle detected is really a hadron
    sig_filter_str = '(pplus_L0HadronDecision_TOS == 1 || piplus_L0HadronDecision_TOS == 1 || kminus_L0HadronDecision_TOS == 1 || lcplus_L0Global_TOS == 1) && (lcplus_MM > 2440 && lcplus_MM < 2490)'
    # Cut out the signal mass of the detector signal to get the background signal
    bkg_filter_str = '(lcplus_MM > 2340 && lcplus_MM < 2440)'# || (lcplus_MM > 2490) && lcplus_MM < 2590)'

    # List of all variables to be used for cutting the data
    cut_variables = ["lcplus_PT",
                     "lcplus_ENDVERTEX_CHI2",
                     "lcplus_IPCHI2_OWNPV",
                     "lcplus_FD_OWNPV",
                     "pplus_ProbNNp",
                     "pplus_PT",
                     "pplus_IPCHI2_OWNPV",
                     "pplus_OWNPV_CHI2",
                     "kminus_ProbNNk",
                     "kminus_PT",
                     "kminus_IPCHI2_OWNPV",
                     "kminus_OWNPV_CHI2",
                     "piplus_ProbNNpi",
                     "piplus_PT",
                     "piplus_IPCHI2_OWNPV",
                     "piplus_OWNPV_CHI2",
                     "lcplus_L0Global_TOS",
                     "pplus_L0HadronDecision_TOS",
                     "piplus_L0HadronDecision_TOS",
                     "kminus_L0HadronDecision_TOS",
                     "lcplus_MM",
                     "lcplus_RAPIDITY",
                     "piplus_RAPIDITY",
                     "pplus_RAPIDITY",
                     "kminus_RAPIDITY",
                     "lcplus_TIP",
                     "piplus_TIP",
                     "pplus_TIP",
                     "kminus_TIP",
                     "lcplus_IP_OWNPV",
                     "piplus_IP_OWNPV",
                     "pplus_IP_OWNPV",
                     "kminus_IP_OWNPV",
                     "lcplus_PVConstrainedDTF_chi2",
                     "lcplus_DIRA_OWNPV",
                     "pplus_TRACK_PCHI2",
                     "kminus_TRACK_PCHI2",
                     "piplus_TRACK_PCHI2"]

    # Call the desired cut function
    cut_tree_small_files('signal', sig_file, 'MC_Lc2pKpiTuple_26103090.root', sig_subjobs, sig_filter_str, cut_variables, signal_tree_name)
    cut_tree_small_files('background', bkg_file, 'Xic2pKpiTuple.root', bkg_subjobs, bkg_filter_str, cut_variables, background_tree_name)

    print(f'Time it took to chain and cut both trees: {time.time() - start_time}')

if __name__ == '__main__':

    main()
