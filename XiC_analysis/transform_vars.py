import ROOT



def transform_data(label, path, extension, jobs, variables, tree_name):

	# For all small data files, create a new and smaller data file with cuts applied
	for job in range(jobs):

		# Define the file
		chain_file = path + f'/{job}/{extension}'

		# Open the file and get the tree
		f = ROOT.TFile.Open(chain_file)
		tree_raw = f.Get(tree_name)

		for var in variables:
			new_var = var + '_log'

		# Define the output file
		out_file = ROOT.TFile(f'/data/bfys/mkoopmans/data/{label}/{label}_cut_transform_{job}.root', 'recreate')

		# Apply the filters
		tree_cut = tree_raw.CopyTree(filter_str)

		out_file.Write()
