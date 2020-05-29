"""
This script is used to calculate the correlations between all pairs of variables for a
certain type of data (singal or background).

Author: Maris Koopmans
"""

import ROOT
import time
import sys

start_time = time.time()

def get_correlations(label, tree):

	# Define the file to which to write the correlations
	corr_file = open(f"correlations/correlations_{label}2.txt", "w")

	# Get a list of the variables in the tree
	leaves = tree.GetListOfLeaves()

	# Get the number of variables in the tree
	num_cols = leaves.GetEntries()

	# Make a list with all possible pairs of variables to calculate the correlation
	# they have with each other
	cols_list = [(i, j) for i in range(num_cols) for j in range(i + 1, num_cols)]

	# Define a histogram which needs to be used to calculate the correlations
	hist_list = [ROOT.TH2F(f"Corr_hist_{label}_i", f"Histogram to calculate correlations for {label} data",\
				 100, tree.GetMinimum(leaves.At(elem[0]).GetName()), tree.GetMaximum(leaves.At(elem[0]).GetName()),\
				 100, tree.GetMinimum(leaves.At(elem[1]).GetName()), tree.GetMaximum(leaves.At(elem[1]).GetName())) for elem in cols_list]

	# Loop over all these pairs
	for index, elem in enumerate(cols_list):
		print(f'Testing {label} data, columns {leaves.At(elem[0]).GetName()} and {leaves.At(elem[1]).GetName()}')

		# Add each datapoint to the histogram
		for ent in range(tree.GetEntries()):

			# Get the datapoint of variable 1
			leaf1 = leaves.At(elem[0])
			tree.GetEntry(ent)
			ent1 = leaf1.GetValue()

			# Get the datapoint of variable 2
			leaf2 = leaves.At(elem[1])
			tree.GetEntry(ent)
			ent2 = leaf2.GetValue()

			# Add them to the histogram
			hist_list[index].Fill(ent1, ent2)

		# Calculate the correlation and write it to the correlations file
		corr = hist_list[index].GetCorrelationFactor()
		corr_file.write(f'{leaf1.GetName()}, {leaf2.GetName()}: {corr}\n')


if __name__ == '__main__':

	label = sys.argv[1]

	# Get the appropriate number of subfolders for the data type
	if label == 'signal':
		num_files = 13
	elif label == 'background':
		num_files = 1155

	# The name of the folder where the data is stored
	folder = f'/data/bfys/mkoopmans/data/{label}'

	# Chain all data together
	chain = ROOT.TChain('DecayTree')
	for num in range(num_files):
		chain.Add(folder + f'/{label}_cut_{num}.root')

	tree = chain.CopyTree('')

	# Calculate the correlations and write them away
	get_correlations(label, tree)

	print(f'Time it took for the {label} script to finish: {time.time() - start_time}')