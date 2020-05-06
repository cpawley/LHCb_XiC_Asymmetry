import time
import ROOT
import os, sys
from Train_BDT import train


def main(run_num, numtrees):

	start_time = time.time()
	# Define the folders and files where the data can be found
	filepath = "/dcache/bfys/jdevries/ntuples/LcAnalysis/ganga"
	MC_files = "/123"
	MC_subjobs = 13
	data_files = "/42"
	data_subjobs = 1155
	tree_name = "tuple_Lc2pKpi/DecayTree"

	# Tree file for MC data
	sig_file = filepath + MC_files
	# Tree file for detector data
	bkg_file = filepath + data_files

	sig_tree_raw = ROOT.TChain(tree_name)
	bkg_tree_raw = ROOT.TChain(tree_name)

	# Load in the signal and background tree
	for job in range(MC_subjobs):

		sig_chain_file = sig_file + f'/{job}/MC_Lc2pKpiTuple_25103029.root'
		sig_tree_raw.Add(sig_chain_file)

	print(f'Succesfully chained all MC files into a single tree')

	for job in range(data_subjobs):

		bkg_chain_file = bkg_file + f'/{job}/Lc2pKpiTuple.root'
		bkg_tree_raw.Add(bkg_chain_file)

	print(f'Succesfully chained all bkg files into a single tree')

	# col_name = 'lcplus_L0Global_TOS'
	# sig_tree_raw.SetBranchAddress(col_name, 0)

	# reader = ROOT.TTreeReader(sig_tree_raw)
	# elem_reader = ROOT.TTreeReaderArray("int")(reader, col_name)

	# while (reader.Next()):
	# 	print(elem_reader)

	# Filter the signal, checking that the particle detected is really a hadron
	sig_filter_str = 'pplus_L0HadronDecision_TOS == 1 || piplus_L0HadronDecision_TOS == 1 || kminus_L0HadronDecision_TOS == 1 || lcplus_L0Global_TOS == 1'

	# Cut out the signal mass of the detector signal to get the background signal
	bkg_filter_str = 'lcplus_MM < 2450 || lcplus_MM > 2480'

	sig_tree = sig_tree_raw.CopyTree(sig_filter_str)
	bkg_tree = bkg_tree_raw.CopyTree(bkg_filter_str)

	print(f'Succesfully filtered both trees')
	print(f'Number of signal events: {sig_tree.GetEntries()}')
	print(f'Number of background events: {bkg_tree.GetEntries()}')

	# List of all variables to be used for training the decision tree
	variables = ["lcplus_PT",
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
		"piplus_OWNPV_CHI2"]

	# Define the MVA method, number of events to be used (0 = all) and name of the BDT
	method = 'BDT'
	cuts = ''
	numevents = 0.8
	label = f'BDT_Xic_pKpi_run{run_num}_{numtrees}trees'

	train(bkg_tree, sig_tree, variables, method, numevents, label, cuts, numtrees)

	print(f'This run finished in t = {time.time() - start_time} s\n')

# if __name__ == '__main__':

run_num = sys.argv[1]
ntrees = sys.argv[2]
main(run_num, ntrees)