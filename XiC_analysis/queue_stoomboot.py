import os, sys

# Indicate which run we're testing
run = 2

# Boost the tree with some different amount of trees
ntrees = [10, 800, 2500]
# ntrees = [100]

for ntree in ntrees:

	# Define the command we want to use
	test_cmd = f'python ~/LHCb_XiC_Asymmetry/XiC_analysis/load_and_train.py {run} {ntree}'
	# test_cmd = f'python ~/LHCb_XiC_Asymmetry/XiC_analysis/test_write_file.py'
	output_dir = f'/data/bfys/mkoopmans/outputs_BDTs/BDT_run{run}'

	# Define the script we want to use to execute this command
	submit_script = 'execute_stoomboot.sh'

	# Add the command to the submit file
	os.system(f'echo "#!/bin/sh" >> {submit_script}')

	# Add and move into the directory for the current run
	os.system(f'echo mkdir {output_dir} >> {submit_script}')
	os.system(f'echo cd {output_dir} >> {submit_script}')

	os.system(f'echo {test_cmd} >> {submit_script}')

	# Define the command to run the script on the cluster and run it
	run_command = f"qsub -q short -j oe -o /data/bfys/mkoopmans/outputs_BDTs/BDT_run{run}/run_{run}_{ntree}trees.out {submit_script}"
	os.system(run_command)

	# Delete the file to execute the script to keep the directory clean
	os.system(f"rm -f {submit_script}")