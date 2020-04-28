"""
Author: Maris Koopmans
Date: 20-4-2020

This script can be used to determine, based on statistics, what variables are
most telling about the differences between signal and background data. I have
however decided not to use this script as choosing variables based on how well
they discriminate introduces a bias in the selection which can and most likely
will influence the results of the analysis negatively.
"""


import numpy as np
import ROOT


def get_elements(variables, tree):

	n = len(variables)
	length = tree.GetEntries()

	arr = np.zeros(shape=(length,n))

	for elem, var in enumerate(variables):

		reader = ROOT.TTreeReader(tree)
		elem_reader = ROOT.TTreeReaderArray("double")(reader, var)
		counter = 0

		while (reader.Next()):
			arr[counter][elem] = elem_reader[0] # elem_reader is a sequence, so take only the first element
			counter += 1

	return arr


def coords_to_index(lst, shape):

	return sum([elem * (shape[i] - 1)**(i) for i, elem in enumerate(lst)])


def histify_elements(arr):

	nbins = 50
	dim = arr.shape[1]
	shape = [nbins + 1 for i in range(dim)]

	hist_floor = np.zeros(shape=tuple(shape))

	mins = np.amin(arr, axis=0)
	maxs = np.amax(arr, axis=0)

	steps = [(maxs[i] - mins[i])/nbins for i in range(dim)]

	for lst in arr:
		coords = []

		for index, elem in enumerate(lst):
			coords.append(round((elem - mins[index]) / steps[index]))


		put_index = int(coords_to_index(coords, shape))
		new_val = hist_floor.flat[put_index] + 1
		np.put(hist_floor, put_index, new_val)

	return hist_floor


def get_separation(sig_tree, bkg_tree, variables):

	sig_elements = get_elements(variables, sig_tree)
	bkg_elements = get_elements(variables, bkg_tree)

	hist_sig = histify_elements(sig_elements)
	hist_bkg = histify_elements(bkg_elements)

	difference_sq = (hist_sig - hist_bkg)**2

	return np.sum(difference_sq)


if __name__ == '__main__':

	filepath = "/dcache/bfys/jdevries/ntuples/LcAnalysis/ganga"
	MC_files = "/123"
	MC_subjobs = 13
	data_files = "/42"
	data_subjobs = 1155


	job_num = 1

	# Tree file for MC data
	file_sig = filepath + MC_files + f'/{job_num}/MC_Lc2pKpiTuple_25103029.root'
	# Tree file for detector data
	file_bkg = filepath + data_files + f'/{job_num}/Lc2pKpiTuple.root'

	tree_name = "tuple_Lc2pKpi/DecayTree"

	f1 = ROOT.TFile(file_sig)
	f2 = ROOT.TFile(file_bkg)

	tree_sig = f1.Get(tree_name)
	tree_bkg = f2.Get(tree_name)

	variables = ['lcplus_ETA', 'lcplus_RAPIDITY']

	sep = get_separation(tree_sig, tree_bkg, variables)
	print(sep)