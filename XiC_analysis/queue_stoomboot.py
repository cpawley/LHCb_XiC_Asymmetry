import os, sys

# Define the command we want to use
test_cmd = 'python ~/LHCb_XiC_Asymmetry/XiC_analysis/test_file_write.py'

# Define the script we want to use to execute this command
submit_script = 'execute_test.sh'

# Add the command to the submit file
os.system(f'echo "#!/bin/sh" >> {submit_script}')
os.system(f'echo {test_cmd} >> {submit_script}')

# Define the command to run the script on the cluster and run it
# TODO: is it necesarry to define -q, the destination queue? If so, which queue is best?
run_command = f"qsub -o test_queue_file.out {submit_script}"
os.system(run_command)