"""
This script is similar to queue_stoomboot.py, only it is used to queue the
data cutting script.

Author: Maris Koopmans
"""

import os, sys

# Define the python script which need to be runned
run_cmd = 'python /user/dwickrem/documents/LHCb_XiC_Asymmetry/XiC_Diyon/cut_data.py'

# Define the output directory
output_dir = f'/data/bfys/dwickrem/sig_bkg_folder/'

# Define a temporary bash file to execute the cut script
submit_script = 'execute_stoomboot_cut.sh'

# Add the command to the submit file
os.system(f'echo "#!/bin/sh" >> {submit_script}')
os.system(f'echo ". /user/dwickrem/.bashrc">>{submit_script}')

# Move into the directory for the current run
os.system(f'echo cd {output_dir} >> {submit_script}')

os.system(f'echo {run_cmd} >> {submit_script}')

# Define the command to run the script on the cluster and run it
run_command = f"qsub -o /data/bfys/dwickrem/sig_bkg_folder/cut_data_final_vars_sigsmall.out -e {output_dir}/log.txt {submit_script}"
os.system(run_command)

# Delete the temporary bash file to keep the directory clean
os.system(f"rm -f {submit_script}")
