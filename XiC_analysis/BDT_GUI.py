import ROOT

method = 'BDT'
run = 1
numtrees = 10
label = f'BDT_Xic_pKpi_run{run}_{numtrees}trees'

data_file = f'/data/bfys/mkoopmans/outputs_BDTs/BDT_run{run}/TMVA_{method}_{label}.root'
# data_file = f'TMVA_{method}_{label}.root'

ROOT.TMVA.TMVAGUI(data_file, label)
input("Press enter to continue")