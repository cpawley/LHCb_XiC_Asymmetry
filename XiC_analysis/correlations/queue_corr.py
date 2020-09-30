"""
This script is similar to queue_stoomboot.py, only it is used to queue the
script for calculating correlations.

Author: Maris Koopmans
"""

import os, sys

# Define the output directory
output_dir = f'~/LHCb_XiC_Asymmetry/XiC_analysis/correlations'

# Calculate correlations for both signal and background
for label in ["signal", "background"]:

	# Define a temporary bash file to execute the script
	submit_script = f'execute_stoomboot_corr_{label}.sh'
	run_cmd = f'python ~/LHCb_XiC_Asymmetry/XiC_analysis/correlations/data_correlation.py {label}'

	# Add the command to the submit file
	os.system(f'echo "#!/bin/sh" >> {submit_script}')

	# Move into the directory for the current run
	os.system(f'echo cd {output_dir} >> {submit_script}')
	os.system(f'echo {run_cmd} >> {submit_script}')

	# Define the command to run the script on the cluster and run it
	run_command = f"qsub -q long -j oe -o correlation_calc_{label}_more_vars.out {submit_script}"
	os.system(run_command)

	# Delete the temporary bash file to keep the directory clean
	os.system(f"rm -f {submit_script}")