"""
Script which organizes the correlations stored in a txt file into a 2D numpy
array, and plots this array with a heatmap. This heatmap can then be used to
judge how correlated two variables are, which can help in excluding/including
them in training.

Author: Maris Koopmans
"""

import matplotlib.pyplot as plt
import numpy as np
import sys


def get_heatmap(lines):

	# Define the number of variables we have
	num_vars = 20

	# Create a 2D numpy array as a means to visualize the correlations
	heatmap = np.zeros((num_vars + 1, num_vars + 1))

	# Counter variable to keep track of the position of the value we want to fill in
	start_point = 0

	# Loop over all variables, filling the heatmap as two triangles.
	# The looping is done backwards because the first row of the heatmap
	# has the most (num_vars) entries in it.
	for i in range(num_vars, 0, -1):
		for elem in range(i):
			# Get the value to fill into the heatmap
			val = float(lines[start_point + elem].split(": ")[1].strip('\n'))

			# Fill row [num_vars - i] columnwise and column [i] row-wise
			heatmap[num_vars - i][elem] = val
			heatmap[num_vars - elem][i] = val

		start_point += i

	return heatmap

def main(cfile, label):

	# Open the file with the correlation data
	with open(cfile, 'r') as f:
		lines = f.readlines()

	# Get the heatmap
	hm = get_heatmap(lines)

	# Plot the heatmap and save the image
	plt.imshow(hm, cmap='hot')
	plt.colorbar()
	plt.savefig(f"correlations_{label}2.png")

if __name__ == '__main__':

	label = sys.argv[1]
	corr_file = f'correlations_{label}2.txt'
	main(corr_file, label)