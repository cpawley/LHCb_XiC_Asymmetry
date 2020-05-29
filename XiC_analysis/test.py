root_ntuple = os.path.join(root_file, ntuple_folder)
root_ntuple = os.path.join(root_ntuple, possible_ntuple.GetName())

background_tree = ROOT.TChain()
background_tree.Add(root_ntuple)

if args.Split:
    store_file = ROOT.TFile("bkg_storage_%i.root"%storage, "RECREATE")

    storage_tree_train = background_tree.CopyTree(cutTrain, "training")
    storage_tree_train.SetName("Training")

    storage_tree_test = background_tree.CopyTree(cutTest, "testing")
    storage_tree_test.SetName("Testing")

    store_file.Write()
    store_file.Close()

    help_Tree1 = ROOT.TChain()
    help_Tree1.Add("bkg_storage_%i.root/Training"%(storage))

    help_Tree2 = ROOT.TChain()
    help_Tree2.Add("bkg_storage_%i.root/Testing"%(storage))
    
    tmva_factory.AddTree(help_Tree1, "Background", background_tree_weight, TCut(""), "train")
    tmva_factory.AddTree(help_Tree2, "Background", background_tree_weight, TCut(""), "test")
    
    log.debug("TMVA.Factory.AddTree(%s, 'Background', %s, %s/%s, 'train/test')"%(root_ntuple, background_tree_weight, cutTrain, cutTest))
    storage += 1
else:

    tmva_factory.AddBackgroundTree(background_tree, background_tree_weight)

    log.debug("TMVA.Factory.AddBackgroundTree(TChain.Add(\"" + root_ntuple +    "\"), " + str(background_tree_weight) + ")")


#!/usr/bin/env python
from ROOT import TMVA, TFile, TTree, TCut
from subprocess import call
from os import listdir

def is_signal(infile):
    """
    Method checks if input string is a signal by looking for 'MA' chars in it.
    """
    if 'MA' in infile:
        return True
    else:
        return False


def tree_name(infile, path= '/path/to/trees/'):
    """
    Method takes a string as input and returns the name of associated tree.
    """
    f = infile

    if is_signal(f):
        out = f.replace(path + 'Out_', 'signal_tree')
        out = out.replace('.root', '')
        return out
    else:
        out = f.replace(path + 'Out_', 'background_tree')
        out = out.replace('.root', '')
        return out
        


def n_entries(infile):
    """
    Method takes a string as an input corresponding to dataset name and returns number of events in dataset.
    """

    file = TFile.Open(infile)
    
    tree_name_ = tree_name(infile)

    tree = file.Get(tree_name_)
    print("Stored {} tree..\n".format(tree_name_))
    n = tree.GetEntries()
    
    return n

def total_entries(infiles = []):
    """
    Method takes list of string corresponding to dataset names and returns the summation over all the file of the entries.
    """
    tot_entries = 0
    for file in infiles:
        tot_entries += n_entries(file)
    return tot_entries


def weight(n_entries, tot_entries):
    """
    return weight for classification
    """
    w = float((tot_entries*0.5/n_entries))
    return w

def background_data(list_file):
    """
    Method filters background names from input list and returns them in form of a list
    """
    bkg = []
    for file in list_file:
        if not is_signal(file) and "MSSM" not in file:
            bkg.append(file)
    return bkg

def signal_data(list_file): 
    """
    Method filters ALL signal names from input list and returns them in form of a list
    """
    sgn = []
    for file in list_file:
        if is_signal(file):
            sgn.append(file)
    return sgn

def custom_signal_data(list_file):                                              #MODIFY THIS TO SELECT SUBSETS OF SIGNAL
    """
    Method filters desired signal names from input list and returns them in form of a list
    """
    sgn = []
    for file in list_file:
        if 'MA400' in file:
            sgn.append(file)
    return sgn


def classifier(path = '/path/to/trees/', tmva_output_file_name = 'TMVA_Output.root'):

    tmva_output_file =TFile.Open(tmva_output_file_name, 'RECREATE')             #Opens TMVA output file. Ovverrides if tmva_output_file_name is not changed.

    TMVA.Tools.Instance()
    TMVA.PyMethodBase.PyInitialize()
    factory = TMVA.Factory('TMVAClassification', tmva_output_file,
                           '!V:!Silent:Color:DrawProgressBar:Transformations=D,G:AnalysisType=Classification')  


    all_files = listdir(path)                                           #array containing all the file names in path
    bkg_data = [path+b for b in background_data(all_files)]                             #load background dataset
    sgn_data = [path+s for s in custom_signal_data(all_files)]                          #load signal dataset
    #TOT_ENTRIES = total_entries(all_files)                                     #uncomment when using all the data.
    TOT_ENTRIES = total_entries(bkg_data)                                       #comment this when using all data.
    TOT_ENTRIES += total_entries(sgn_data)                                      #comment this when using all data.
    print("TOTAL ENTRIES ======> ")
    print(TOT_ENTRIES)

    variables = ["dimuon_deltar",                                               #Define discrimination variables
                 "dimuon_deltaphi",         
                 "dimuon_deltaeta",
                 "met_pt",
                 "bjet_n",
                 #"no_btag_jet",
                 "bjet_1.Pt()",
                 "bjet_1.Eta()",
                 #"btag_jet_over2.4",
                 "deltar_bjet1_dimuon",
                 "deltapt_bjet1_dimuon",
                 "deltaeta_bjet1_dimuon"
                ]
        
    dataloader = TMVA.DataLoader('dataset')
    for v in variables:
        dataloader.AddVariable(v)

    
    for b in bkg_data:
        f =  TFile.Open(b)
        bkg_tree = f.Get(tree_name(b))
        n = bkg_tree.GetEntries()
        bkg_weight = weight(n, TOT_ENTRIES)
        dataloader.AddBackgroundTree(bkg_tree, bkg_weight)

    for s in sgn_data:
        f =TFile.Open(s)
        sgn_tree = f.Get(tree_name(s))
        n = sgn_tree.GetEntries()
        sgn_weight = weight(n, TOT_ENTRIES)
        dataloader.AddSignalTree(sgn_tree, sgn_weight)
        

    dataloader.PrepareTrainingAndTestTree(TCut(''), "nTrain_Signal=10000:nTrain_Background=100000:nTest_Signal=0:nTest_Background=0:SplitMode=Random:NormMode=None:!V")

###################################################################### Book methods ########################################################################

    # Generate model
    #factory.BookMethod(dataloader, TMVA.Types.kBDT, "BDTG",
                               # "!H:!V:NTrees=1000:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.20:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=6" );

    factory.BookMethod(dataloader, TMVA.Types.kBDT, "BDT",
               "!H:!V:NTrees=1000:MinNodeSize=2.5%:MaxDepth=6:BoostType=AdaBoost:AdaBoostBeta=0.3:UseBaggedBoost:BaggedSampleFraction=0.3:SeparationType=GiniIndex:nCuts=20" );

    #factory.BookMethod(dataloader, TMVA.Types.kBDT, "BDTB",
                              #  "!H:!V:NTrees=1000:BoostType=Bagging:SeparationType=GiniIndex:nCuts=20" );

    #factory.BookMethod(dataloader, TMVA.Types.kBDT, "BDTD",
                               # "!H:!V:NTrees=1000:MinNodeSize=2.5%:MaxDepth=6:BoostType=AdaBoost:AdaBoostBeta=0.7:SeparationType=GiniIndex:nCuts=20:VarTransform=Decorrelate" );

    # Run training, test and evaluation
    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()

    tmva_output_file.close()

    print("""
            ==> Wrote root file: {} \n
            ==> TMVAClassification is done!\n
          """).format(tmva_output_file.GetName())

classifier()