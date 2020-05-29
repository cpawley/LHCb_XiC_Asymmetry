"""
This script is the 'interface' for the training of the BDT; here the
variables and number of events to train on are defined.

Author: Maris Koopmans 
"""

import time
import ROOT
import os, sys
from Train_BDT import train


def main(run_num, numtrees):

	start_time = time.time()

	# Define paths to the signal and background folder
	sig_folder = '/data/bfys/mkoopmans/data/signal_small'
	bkg_folder = '/data/bfys/mkoopmans/data/background_small'

	# Define the MVA method, fraction of events to be used for training
	# (0 = all) and name of the BDT
	method = 'BDT'
	cuts = ''
	numevents = 0.8
	label = f'BDT_Xic_pKpi_run{run_num}_{numtrees}trees'

	# List of all variables to be used for training the BDT
	raw_variables = ["pplus_ProbNNp",
		"kminus_ProbNNk",
		"piplus_ProbNNpi"]

	transfor_variables = [("log(lcplus_FD_OWNPV)", "lcplus_FD_OWNPV_log"),\
						  ("log(lcplus_ENDVERTEX_CHI2)", "lcplus_ENDVERTEX_CHI2_log"),\
						  ("log(lcplus_IPCHI2_OWNPV)", "lcplus_IPCHI2_OWNPV_log"),\
						  ("log(pplus_OWNPV_CHI2)", "pplus_OWNPV_CHI2_log"),\
						  ("log(kminus_OWNPV_CHI2)", "kminus_OWNPV_CHI2_log"),\
						  ("log(piplus_OWNPV_CHI2)", "piplus_OWNPV_CHI2_log"),\
						  ("log(pplus_PT)", "pplus_PT_log"),\
						  ("log(kminus_PT)", "kminus_PT_log"),\
						  ("log(piplus_PT)", "piplus_PT_log"),\
						  ("log(lcplus_PT)", "lcplus_PT_log"),\
						  ("log(kminus_IPCHI2_OWNPV)", "kminus_IPCHI2_OWNPV_log"),\
						  ("log(piplus_IPCHI2_OWNPV)", "piplus_IPCHI2_OWNPV_log"),\
						  ("log(pplus_IPCHI2_OWNPV)", "pplus_IPCHI2_OWNPV_log")]

	# Actually train the BDT
	train(bkg_folder, sig_folder, raw_variables, transfor_variables, method, numevents, label, cuts, numtrees)

	print(f'This run finished in t = {time.time() - start_time} s\n')


run_num = sys.argv[1]
ntrees = sys.argv[2]
main(run_num, ntrees)