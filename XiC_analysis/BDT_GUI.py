"""
This script takes an input .root file which represents a BDT, and uses the TMVAGUI
module to visualize its contents.

Author: Maris Koopmans
"""

import ROOT

# Define some parameters which describe the file
method = 'BDT'
run = 5
numtrees = 800
label = f'BDT_Xic_pKpi_run{run}_{numtrees}trees'

# Define the path to the file 
data_file = f'/data/bfys/mkoopmans/outputs_BDTs/BDT_run{run}/TMVA_{method}_{label}.root'

# Open the GUI
ROOT.TMVA.TMVAGUI(data_file, label)

# Keep this to prevent the GUI from closing instantaneously
input("Press enter to continue")