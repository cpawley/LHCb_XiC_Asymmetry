"""
This script is the 'interface' for the training of the BDT; here the
variables and number of events to train on are defined.

Author: Maris Koopmans 
"""

import time
import ROOT
import os, sys
from Train_BDT import train


def main(run_num, numtrees, outDir):

	start_time = time.time()

	# Define paths to the signal and background folder
	sig_folder = '/data/bfys/dwickrem/sig_bkg_folder/signal_newcuts'
	bkg_folder = '/data/bfys/dwickrem/sig_bkg_folder/background_newcuts'
                

	# Define the MVA method, fraction of events to be used for training
	# (0 = all) and name of the BDT
	method = 'BDT'
	cuts = ''
	numevents = 0.65
	label = f'BDT_Xic_pKpi_run{run_num}_{numtrees}trees'

	# List of all variables to be used for training the BDT
	raw_variables = ['lcplus_RAPIDITY',
                         'piplus_RAPIDITY',
                         'pplus_RAPIDITY',
                         'kminus_RAPIDITY',
                         'lcplus_ENDVERTEX_CHI2',
                         "lcplus_ENDVERTEX_NDOF",
                         'lcplus_IPCHI2_OWNPV',
                         'pplus_OWNPV_CHI2',
                         "pplus_P", 
                         "pplus_PT",
                         "kminus_P", 
                         "kminus_PT",
                         "piplus_P", 
                         "piplus_PT",
                         "kminus_PIDK", 
                         "kminus_PIDp",
                         "piplus_PIDK", 
                         "piplus_PIDp",
                         "pplus_PIDK", 
                         "pplus_PIDp",
                         'kminus_OWNPV_CHI2',
                         'piplus_OWNPV_CHI2',
                         'lcplus_IP_OWNPV',
                         'piplus_ProbNNpi',
                         'pplus_ProbNNp',
                         'kminus_ProbNNk',
                         "pplus_MC15TuneV1_ProbNNp",
                         "pplus_MC15TuneV1_ProbNNk",
                         "pplus_MC15TuneV1_ProbNNpi",
                         "pplus_MC15TuneV1_ProbNNghost",
                         "kminus_MC15TuneV1_ProbNNp",
                         "kminus_MC15TuneV1_ProbNNk",
                         "kminus_MC15TuneV1_ProbNNpi",
                         "kminus_MC15TuneV1_ProbNNghost",
                         "piplus_MC15TuneV1_ProbNNp",
                         "piplus_MC15TuneV1_ProbNNk",
                         "piplus_MC15TuneV1_ProbNNpi",
                         "piplus_MC15TuneV1_ProbNNghost"]

	transfor_variables = []

	transfor_variables = [("log(lcplus_FD_OWNPV)", "lcplus_FD_OWNPV_log"),\
                              ("log(pplus_PT)", "pplus_PT_log"),\
                              ("log(piplus_IP_OWNPV)", "piplus_IP_OWNPV_log"),\
                              ("log(pplus_IP_OWNPV)", "pplus_IP_OWNPV_log"),\
                              ("log(kminus_IP_OWNPV)", "kminus_IP_OWNPV_log"),\
                              ("log(kminus_PT)", "kminus_PT_log"),\
                              ("log(piplus_PT)", "piplus_PT_log"),\
                              ("log(lcplus_PT)", "lcplus_PT_log"),\
                              ("log(kminus_IPCHI2_OWNPV)", "kminus_IPCHI2_OWNPV_log"),\
                              ("log(piplus_IPCHI2_OWNPV)", "piplus_IPCHI2_OWNPV_log"),\
                              ("log(pplus_IPCHI2_OWNPV)", "pplus_IPCHI2_OWNPV_log"),\
                              ("sqrt(kminus_IPCHI2_OWNPV)" , "kminus_IPCHI2_OWNPV_sqrt"),\
                              ("sqrt(pplus_IPCHI2_OWNPV)" , "pplus_IPCHI2_OWNPV_sqrt"),\
                              ("sqrt(piplus_IPCHI2_OWNPV)" , "piplus_IPCHI2_OWNPV_sqrt"),\
                              ("sqrt(kminus_IPCHI2_OWNPV + pplus_IPCHI2_OWNPV + piplus_IPCHI2_OWNPV)" , "pKpi_IPCHI2_OWNPV_sqrt_sum"),\
                              ("log(kminus_PT + piplus_PT + pplus_PT)" , "pKpi_PT_log_sum"),\
                              ("pplus_P / (pplus_P + kminus_P + piplus_P)","pplus_P/(pplus_P + kminus_P + piplus_P)"),\
                              ("lcplus_ENDVERTEX_CHI2 / lcplus_ENDVERTEX_NDOF","lcplus_ENDVERTEX_CHI2 / lcplus_ENDVERTEX_NDOF")]
                

	# Actually train the BDT
	train(bkg_folder, sig_folder, raw_variables, transfor_variables, method, numevents, label, cuts, numtrees, outDir)

	print(f'This run finished in t = {time.time() - start_time} s\n')


run_num = sys.argv[1]
ntrees = sys.argv[2]
outDir = sys.argv[3]
main(run_num, ntrees, outDir)
