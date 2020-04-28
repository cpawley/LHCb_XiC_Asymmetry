# def get_col_name(df, num):
# 	# Get a list of all branches and print the name of one specific element
# 	branches = df.GetColumnNames()
# 	br_name = branches[num]

# 	return br_name

# def get_all_cols(df):

# 	l = [get_col_name(df, i) for i in range(tree.GetNbranches())]
# 	return l

# Print values of columns in a tree
# def print_value(tree, num):

# 	col_name = get_col_name(tree, num)

# 	# elem = 0.0
# 	# tree.SetBranchAddress(col_name, elem)

# 	# for i in range(tree.GetEntries() // 300):
# 	# 	print(tree.GetEntry(i))

# 	reader = ROOT.TTreeReader(tree)
# 	elem_reader = ROOT.TTreeReaderArray("double")(reader, col_name)

# 	while (reader.Next()):
# 		print(elem_reader)


# Create a file with the names of all the columns of the tree 
# cols = get_all_cols(df)

# with open("columns.txt", "w") as f:
# 	for col in cols:
# 		f.write(col + "\n")