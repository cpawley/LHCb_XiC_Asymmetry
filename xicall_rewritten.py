##xicall.py rewritten in similar style as fit.py
import ROOT, sys, os
from fitting_dependencies import writeFile

## Bukin Parameters --> These need to be put in one "variable" b_params
#mass_range = [2430, 2510] #Is this RANGE?
#peak_range = [2468, 2466, 2470] #Is this VAR_RANGE
normalisation_factor = 1
exponential_normalisation_factor = 1
exponential_range = [-0.0019, -0.2, 0.2]
width_range = [5.5, 0.01, 50]
asym_range = [-0.01, -0.1, 0.1]
rho1_range = [0.05, 0.01, 0.1]
rho2_range = [0.03, 0.001, 0.1]

## Histogram
MEMORY = "/data/bfys/name/root_outputs/temp.root"
DEFAULT_OUTPUT = "/data/bfys/name/pdf_outputs/plots/"
VAR = "lcplus_MM"
UNIT = "MeV/c^{2}"
BINS = 300 #Value from xicall file was 100, changed to 300 to match fit.py

RANGE = [2430, 2510] #Value from xicall file, but was defined as mass_range there
VAR_RANGE = [2466, 2570, 2468] #Value from xicall file, but was defined as peak_range there. Put the first value aka the initial value at the end so no problems would occur for the VAR_RANGE values of other shapes

X = "Mass MeV/c^{2}"
Y = "Events"
T = "Plot of {}" .format(VAR)
CUTS = "BDT_response > -0.12" #In xicall file was "1==1", changed to "BDT_response > -0.12 to match fit.py"

## Tuples and outputs

YEARS = ["2016"] #Change this so you can choose which year you want?
RUN = "run_3" #Change this so you can choose which run you want?

#For the folllowing lines: need to add those folders!
TUPLES = "/data/bfys/name/root_outputs/blinded_random/{}".format(RUN)
PDF_OUTPUT = "/data/bfys/name/pdf_outputs/mass_fits/blinded_random/{}/".format(RUN)
ASYMMETRY_FILE = "/data/bfys/name/pdf_outputs/mass_fits/blinded_random/{}/".format(RUN)
HISTOGRAM_OUPUTS = "/data/bfys/name/pdf_outputs/BDT_comparison/{}/".format(RUN)
DICTIONARY_FILE = "/data/bfys/name/pdf_outputs/mass_fits/blinded_random/{}/".format(RUN)
SETS = ["dataset1", "dataset2"]
TUPLE_BINS = ["ptbins", "ybins", "y_ptbins"]

## Script handling and flags
HANDLES = ["-ph", "-pcp", "-compare","-fit", "-refit","-compareall"]

#Make sure the names of the files are correct
HANDLE_DESC = ["Plots histogram: python fit.py {} <file> [var] [cuts] [out_dir]".format(HANDLES[0]),
               "Makes component plot: python fit.py {} <file> [shapes] [var] [cuts] [out_dir]".format(HANDLES[1]),
               "Makes comparison plot: python fit.py {} <file> [var] [cuts] [out_dir]".format(HANDLES[2]),
               "Runs fitting and computes asymmetry for analysis: python fit.py {}".format(HANDLES[3]),
               "Refits a distribution with new parameters: python fit.py {} <file> <shapes> [var] [cuts] [out_dir]".format(HANDLES[4]),
               "Runs comparison plots for all data: python fit.py {}".format(HANDLES[5])]

flags = []

DICTIONARY = {}

"""
This function plots a histogram. Depending on where or how it's called, it's input parameters can be changed
"""

def plot_histogram (root_file, variable = None, cuts = None, out_dir = None, to_fit = False, to_compare = False):

    name = root_file.split("/")[-1].replace(".root", "") + ".pdf"

    file_name = root_file.split("/")[-1]

    print("Plotting {} on a histogram".format(name))

    if(variable != None):
        v = variable
        else:
            v = VAR
    
    if (cuts != None):
        cut = cuts
        else:
            cut = CUTS

    if (out_dir != None):
        save = out_dir + name
        else:
            save = DEFAULT_OUTPUT + name
    
    #Open data from file and get tree
    f = ROOT.TFile.Open(root_file, "READ")
    temp = ROOT.TFile.Open(MEMORY, "RECREATE")
    t = f.Get("DecayTree")

    histogram = ROOT.TH1F("histogram", T, BINS, VAR_RANGE[0], VAR_RANGE[1])

    c = ROOT.TCanvas("canvas")

    temp.cd()

     if (cut != None) and (cut != ""):
        print("Applying these cuts: {}".format(cut))
        cutTree = t.CopyTree(cut)
        N = cutTree.GetEntries()

        print("Drawing the variable from the pruned tree to a histogram")
        cutTree.Draw(v+">>histogram("+str(BINS)+","+str(RANGE[0])+","+str(RANGE[1])+")")
    else:
        N = t.GetEntries()

        print("Drawing variable from tree to a histogram")
        t.Draw(v+">>histogram("+str(BINS)+","+str(RANGE[0])+","+str(RANGE[1])+")")

    if (to_fit):

        c.Close()
        del c
        
        histogram = ROOT.gDirectory.Get("histogram")
        histogram.GetXaxis().SetRangeUser(VAR_RANGE[0], VAR_RANGE[1])
        histogram.GetYaxis().SetRangeUser(0, histogram.GetMaximum()+1000)
        histogram.SetDirectory(0)

        f.Close()
        temp.Close()

        os.system("rm -rf {}".format(MEMORY))

        return name, file_name, histogram, N

    if (to_compare):
        ROOT.gDirectory.Delete("histogram")
        histogram = ROOT.TH1F("Before", T, BINS, RANGE[0], RANGE[1])
        histogram2 = ROOT.TH1F("After", T, BINS, RANGE[0], RANGE[1])

        title = "Plot of {} before and after BDT".format(v)

        print("Drawing histogram before")
        t.Draw(v+">>Before("+str(BINS)+","+str(RANGE[0])+","+str(RANGE[1])+")")
        histogram = ROOT.gDirectory.Get("Before")
        histogram.SetLineColor(4)
        histogram.GetXaxis().SetTitle(X)
        histogram.GetYaxis().SetTitle(Y)
        histogram.SetTitle(title)

        print("Drawing histogram after")
        cutTree.Draw(v+">>After("+str(BINS)+","+str(RANGE[0])+","+str(RANGE[1])+")")
        histogram2 = ROOT.gDirectory.Get("After")
        histogram2.SetLineColor(3)
        histogram2.GetXaxis().SetTitle(X)
        histogram2.GetYaxis().SetTitle(Y)
        histogram2.SetTitle(title)

        histogram.Draw()
        histogram2.Draw("same")

        legend = ROOT.TLegend(0.8, 0.5, 0.95, 0.65)
        ROOT.SetOwnership(legend, False)
        legend.SetBorderSize(1)
        legend.SetShadowColor(2)
        legend.AddEntry(histogram, "Before", "l")
        legend.AddEntry(histogram2, "After", "l")
        legend.SetTextSize(0.03)
        legend.SetTextColor(1)
        legend.Draw("same")

        entries = str(histogram2.GetEntries())
        mean = str(histogram2.GetMean())
        stdev = str(histogram2.GetRMS())
        
        c.Update()
        c.Draw()
        c.Print(save, "PDF")
        c.Close
        del c

        ROOT.gDirectory.Delete("Before")
        ROOT.gDirectory.Delete("After")

        f.Close()
        temp.Close()
        os.system("rm -rf {}".format(MEMORY))

        return name, entries, mean, stdev

    print("Drawing histogram...")
    title = "Plot of {}".format(v)
    histogram = ROOT.gDirectory.Get("histogram")
    histogram.SetLineColor(4)
    histogram.GetXaxis().SetTitle(X)
    histogram.GetYaxis().SetTitle(Y)
    histogram.SetTitle(title)
    histogram.Draw()

    c.Update()
    c.Draw()
    c.Print(save, "PDF")
    c.Close()
    del c

    ROOT.gDirectory.Delete("histogram")

    f.Close()
    temp.Close()
    os.system("rm -rf {}".format(MEMORY))

    return

"""
Returns the normalisation parameters for the gaussian, exponential and crystal ball shapes 
"""
def getGaussNormParams(N):
    return [N , N/500 * 2 , N*2]

def getExpoNormParams(N):
    return [N*0.5 , N/1000, N*2]

def getCBNormParams(N):
    return [N , N/500 * 2 , N*2]

#add bukin shape!
#def getBukinNormParams(N):
    #return [N, N/500 * 2, N*2]

"""
This function neatly writes a dictionary to a python file
"""

def writeDict(path, dictionary):
    python_file = open(path,"w")
    python_file.write("fitting_dictionary = {")

    ds_n = 0
    for ds in dictionary:
        
        python_file.write("\n\t\""+ds+"\":{")

        b_n = 0
        for b in dictionary[ds]:
            
            python_file.write("\n\t\t\""+b+"\":{")
                
            fi_n = 0
            for fi in dictionary[ds][b]:

                python_file.write("\n\t\t\t\""+fi+"\":{")
            
                n = 0
                for r in dictionary[ds][b][fi]:
                    if (n==0):
                        python_file.write("\n\t\t\t\t\"{}\":\"{}\",".format(r , dictionary[ds][b][fi][r]))
                    else:
                        if(n+1 == len(dictionary[ds][b][fi])):
                            python_file.write("\n\t\t\t\t\""+r+"\":"+ str(dictionary[ds][b][fi][r])+" }")
                        else:
                            python_file.write("\n\t\t\t\t\"{}\":{} ,".format(r , dictionary[ds][b][fi][r]))
                    n+=1

                if (fi_n+1 == len(dictionary[ds][b])):
                    python_file.write("\n\t\t\t }")
                else:
                    python_file.write("\n\t\t\t ,")

                fi_n+=1

            if (b_n+1 == len(dictionary[ds])):
                python_file.write("\n\t\t }")
            else:
                python_file.write("\n\t\t ,")

            b_n+=1
        
        if(ds_n +1 == len(dictionary)):
           python_file.write("\n\t}")
        else:
           python_file.write("\n\t,")

        ds_n+=1
    
    python_file.close()

"""
This function builds a dictionary to hold results and data
"""

def build_dict(year):

    for dset in SETS:

        bin_dict = {}
        for bin_type in TUPLE_BINS:

            root_dict = {}
            for root_file in os.listdir(TUPLES+year+"/"+dset+"/"+bin_type+"/"):

                file_dict = {"results" : "", "shape" : []}
                root_dict[root_file] = file_dict

            bin_dict[bin_type] = root_dict

        DICTIONARY[dset] = bin_dict

    #Add 'placeholders' for total files
    for dset in SETS:
        DICTIONARY[dset]["ybins"][dset+"_total.root"] = {"results" : "", "shape" : []}

    return DICTIONARY

    #add "B" for Bukin
def fit_data(root_file, year = None, shapes = ["G","E","CB", "B"] , variable = None, cuts = None, out_dir = None, dset = None, bin_type = None, refit_dictionary = None):

    if (variable != None):
        var = variable
    else:
        var = VAR

    if (cuts != None):
        cut = cuts
    else:
        cut = CUTS

    if(out_dir != None):
        save_fit = out_dir
    else:
        save_fit = DEFAULT_OUTPUT


    name, file_name, histogram, N = plot_histogram(root_file, var, cut, save_fit, True, False)

    c = ROOT.TCanvas("canvas")

    fit_title = "Fit plot of {}".format(var)

    histogram.SetLineColor(0)
    histogram.GetXaxis().SetTitle(X)
    histogram.GetYaxis().SetTitle(Y)
    histogram.SetTitle(fit_title)
    histogram.Draw()

    rvar = ROOT.RooRealVar(var , var, VAR_RANGE[0], VAR_RANGE[1])

    argList = ROOT.RooArgList()
    normArgList = ROOT.RooArgList()
    components = []

    if (refit_dictionary == None):
        shape = shapes
        
        if(year != None):
            DICTIONARY[dset][bin_type][file_name]["shape"] = shape
    else:
        shape = refit_dictionary[dset][bin_type][file_name]["shape"]

    if "G" in shape:
        
        if (refit_dictionary == None):

            GAUSS_PARAMS = gauss_params
            GNP = getGaussNormParams(N)

            if(dset != None) and (bin_type != None) and (year != None):
                DICTIONARY[dset][bin_type][file_name]["gaussParams"] = GAUSS_PARAMS
                DICTIONARY[dset][bin_type][file_name]["gaussNormParams"] = [GNP[0]/N , GNP[1]/N , GNP[2]/N]

        else:
            GAUSS_PARAMS = refit_dictionary[dset][bin_type][file_name]["gaussParams"]
            GNP = []
            for gparam in refit_dictionary[dset][bin_type][file_name]["gaussNormParams"]:
                GNP.append(gparam * N)

        gaussMean = ROOT.RooRealVar("gaussMean","gaussMean", GAUSS_PARAMS[0], GAUSS_PARAMS[1], GAUSS_PARAMS[2])
        gaussWidth = ROOT.RooRealVar("gaussWidth","gaussWidth", GAUSS_PARAMS[3], GAUSS_PARAMS[4], GAUSS_PARAMS[5])
        gaussNorm = ROOT.RooRealVar("gaussNorm","gaussNorm", GNP[0], GNP[1], GNP[2])

        gauss = ROOT.RooGaussian("gauss","gauss",rvar, gaussMean, gaussWidth)

        argList.add(gauss)
        normArgList.add(gaussNorm)
        components.append("gauss")

    if "E" in shape:

        if (refit_dictionary == None):

            EXPONENTIAL_PARAMS = exponential_params
            ENP = getExpoNormParams(N)
            
            if (dset != None) and (bin_type != None) and (year != None):
                DICTIONARY[dset][bin_type][file_name]["expoParams"] = EXPONENTIAL_PARAMS
                DICTIONARY[dset][bin_type][file_name]["expoNormParams"] = [ENP[0]/N , ENP[1]/N , ENP[2]/N]

        else:
            EXPONENTIAL_PARAMS = refit_dictionary[dset][bin_type][file_name]["expoParams"]
            ENP = []
            for eparam in refit_dictionary[dset][bin_type][file_name]["expoNormParams"]:
                ENP.append(eparam * N)

        e = ROOT.RooRealVar("e","e",EXPONENTIAL_PARAMS[0], EXPONENTIAL_PARAMS[1], EXPONENTIAL_PARAMS[2])
        bkgNorm = ROOT.RooRealVar("bkgNorm","bkgNorm", ENP[0], ENP[1], ENP[2])

        bkg = ROOT.RooExponential("bkg","bkg", rvar, e)

        argList.add(bkg)
        normArgList.add(bkgNorm)
        components.append("bkg")

        
        
    if "CB" in shape:
            
        if (refit_dictionary == None):

            CB_PARAMS = cb_params
            CBNP = getCBNormParams(N)
            
            if (dset != None) and (bin_type != None) and (year != None):
                DICTIONARY[dset][bin_type][file_name]["cbParams"] = CB_PARAMS
                DICTIONARY[dset][bin_type][file_name]["cbNormParams"] = [CBNP[0]/N , CBNP[1]/N , CBNP[2]/N]

        else:
            CB_PARAMS = refit_dictionary[dset][bin_type][file_name]["cbParams"]
            CBNP = []
            for cbparam in refit_dictionary[dset][bin_type][file_name]["cbNormParams"]:
                CBNP.append(cbparam * N)

        cbw = ROOT.RooRealVar("cbw","cbw", CB_PARAMS[0], CB_PARAMS[1], CB_PARAMS[2])
        cba = ROOT.RooRealVar("cba","cba", EXPONENTIAL_PARAMS[0], EXPONENTIAL_PARAMS[1], EXPONENTIAL_PARAMS[2])
        cbn = ROOT.RooRealVar("cbn","cbn", CB_PARAMS[3], CB_PARAMS[4], CB_PARAMS[5])
        cbNorm = ROOT.RooRealVar("cbNorm","cbNorm", CBNP[0], CBNP[1], CBNP[2])

        CB = ROOT.RooCBShape("CB","CB", rvar, gaussMean, cbw, cba, cbn)

        argList.add(CB)
        normArgList.add(cbNorm)
        components.append("CB")

    if "B" in shape:

        if (refit_dictionary == None):

            B_PARAMS = b_params 
            BNP = getBukinNormParams(N)

            if (dset != None) and (bin_type != None) and (year != None):
                DICTIONARY[dset][bin_type][file_name]["bParams"] = B_PARAMS
                DICTIONARY[dset][bin_type][file_name]["bNormParams"] = [BNP[0]/N, BNP[1]/N, BNP[2]/N]

        else:

        B_PARAMS = refit_dictionary[dset][bin_type][file_name]["bParams"]
        BNP = []
        for bparam in refit_dictionary[dset][bin_type][file_name]["bNormParams"]:
            BNP.append(bparam * N)


        ##In fit.py file mean, width and norm get defined, but in the xicall file there are much more variables that get defined
        Bukin_Xp = ROOT.RooRealVar("Bukin_Xp", "Peak position", peak_range[0], peak_range[1], peak_range[2])
        Bukin_Sigp = ROOT.RooRealVar("Bukin_Sigp", "Peak width", width_range[0], width_range[1], width_range[2])
        Bukin_xi = ROOT.RooRealVar("Bukin_xi", "Peak asymmetry parameter", asym_range[0], asym_range[1], asym_range[2])
        Bukin_rho1 = ROOT.RooRealVar("Bukin_rho1", "Parameter of the left tail", rho1_range[0], rho1_range[1], rho1_range[2])
        Bukin_rho2 = ROOT.RooRealVar("Bukin_rho2", "Parameter of the right tail", rho2_range[0], rho2_range[1], rho2_range[2])
        Bukin_Norm = ROOT.RooRealVar("Bukin_Norm", "Bukin Yield", tree.GetEntries()/nbins * 3/normalisation_factor, 0, tree.GetEntries() * 2)
        
        #Maybe this can be simplified by using rvar?
        Bukin = ROOT.RooBukinPdf(("Bukin_PDF", "Bukin shape", rvar, Bukin_Xp, Bukin_Sigp, Bukin_xi, Bukin_rho1, Bukin_rho2))

        argList.add(Bukin)
        normArgList.add(Bukin_Norm)
        components.append("Bukin")

    model = ROOT.RooAddPdf("model" , "model", argList, normArgList)
    rHist = ROOT.RooDataHist("rHist", "rHist", ROOT.RooArgList(rvar), histogram)
    rHist.SetNameTitle("rHist" , fit_title)

    model.fitTo(rHist)

    frame = rvar.frame()

    rHist.plotOn(frame)

    colours = [8, 46, 2]

    for i in range(len(components)):
        model.plotOn(frame, ROOT.RooFit.Components(components[i]), ROOT.RooFit.LineColor(colours[i]), ROOT.RooFit.LineStyle(2))
    
    model.plotOn(frame)

    y = normArgList[0].getValV()
    e = normArgList[0].getError()
    chi = frame.chiSquare()

    print("Nbkg: {} +/- {}".format(str(normArgList[1].getValV()),str(normArgList[1].getError())))

    if (chi < 0.4) or (chi > 2):
        flags.append("{}:{}:{}:{}".format(year,dset,bin_type,file_name))

    legend = ROOT.TLegend(0.6, 0.6, 0.85 ,0.75)
    ROOT.SetOwnership(legend, False)
    legend.SetBorderSize(0)
    legend.SetShadowColor(2)
    legend.AddEntry(rHist, "Yield: {} +/- {}".format(int(y),int(e)), "")
    legend.AddEntry(rHist, "Chi2: {}".format(chi), "")
    legend.SetTextSize(0.03)
    legend.SetTextColor(1)
    legend.Draw("same")

    frame.Draw("same")

    if (refit_dictionary == None) and (year != None):
        DICTIONARY[dset][bin_type][file_name]["results"] = "{}:{}:{}".format(str(y) , str(e), str(chi))

    else:
        #Just added this incase 1 component plot had to be made
        if(year != None):
            refit_dictionary[dset][bin_type][file_name]["results"] = "{}:{}:{}".format(str(y) , str(e), str(chi))
            
            writeDict(DICTIONARY_FILE+year+"/fitting_dictionary.py" , refit_dictionary)

    c.Update()
    c.Draw()
    c.Print(save_fit+name, "PDF")
    c.Close()
    del c

    ROOT.gDirectory.Delete("histogram")

    print("Done for "+name)

if __name__ == '__main__':

    if (len(sys.argv)<2):
        print("Improper handle to run this script. Please use one of the following: ")
        
        i = 0
        for handle in HANDLES:
            print(handle+" :")
            print(HANDLE_DESC[i])
            print("")
            i+=1
        sys.exit()
    
    option = sys.argv[1]

    if not option in HANDLES:
        print("Improper handle to run this script. Please use one of the following: ")
        
        i = 0
        for handle in HANDLES:
            print(handle+" :")
            print(HANDLE_DESC[i])
            print("")
            i+=1

        sys.exit()

    else:
        #1
        if (option == HANDLES[0]):
            if (len(sys.argv) == 3):
                plot_histogram(sys.argv[2])
            sys.exit()

        #2
        if(option == HANDLES[1]):
            if (len(sys.argv) == 3):
                fit_data(sys.argv[2])

            elif (len(sys.argv) == 7):
                fit_data(sys.argv[2], None, shapes = sys.argv[3], variable = sys.argv[4], cuts = sys.argv[5], out_dir = sys.argv[6], dset = None,bin_type= None,refit_dictionary= None)
                
            else:
                print("Your arguments are incorrect. Check your function")

            sys.exit()
            
            

        #3
        if(option == HANDLES[2]):

            if not os.path.exists(DEFAULT_OUTPUT):
                os.makedirs(DEFAULT_OUTPUT)

            text = open(DEFAULT_OUTPUT+"afterHistograms.txt","w")

            if (len(sys.argv) == 3):
            
                name, entries, mean, stdev = plot_histogram(sys.argv[2], to_compare = True)
            
                text.write(name)
                text.write("\nEntries: "+entries)
                text.write("\nMean: "+mean)
                text.write("\nStd Dev: "+stdev)
                text.write("\n")
                text.close()

            elif (len (sys.argv) == 6):

                name, entries, mean, stdev = plot_histogram(sys.argv[2], variable = sys.argv[3], cuts = sys.argv[4], out_dir = sys.argv[5], to_fit = False, to_compare = True)

                text.write(name)
                text.write("\nEntries: "+entries)
                text.write("\nMean: "+mean)
                text.write("\nStd Dev: "+stdev)
                text.write("\n")
                text.close()

            else:
                text.close()
                print("Your arguments are incorrect. Check your function")
                
            sys.exit()

            

        #4
        if (option == HANDLES[3]):

            print("Fitting all data")
            for year in YEARS:

                DICTIONARY = build_dict(year)

                print("For year: "+year)
                for ds in SETS:

                    print("Making the total file")

                    tot_file = ROOT.TFile.Open(TUPLES+year+"/"+ds+"/"+ds+"_total.root","RECREATE")

                    tot_tree = ROOT.TChain("DecayTree")

                    for f in os.listdir(TUPLES+year+"/"+ds+"/ybins/"):
                        tot_tree.Add(TUPLES+year+"/"+ds+"/ybins/"+f)

                    tot_file.cd()
                    tot_tree.Write("", ROOT.TObject.kOverwrite)
                    tot_file.Write("", ROOT.TObject.kOverwrite)

                    print("Fitting total file: "+ds+"_total.root")

                    out = PDF_OUTPUT+year+"/"+ds+"/"

                    if not os.path.exists(out):
                        os.makedirs(out)
                    
                    fit_data(TUPLES+year+"/"+ds+"/"+ds+"_total.root", shapes = ["G","E"] , year = year, variable = VAR, cuts = CUTS, out_dir = out, dset = ds, bin_type = "ybins", refit_dictionary = None)
                    
                    tot_file.Close()

                    print("Fitting files in all bins now")

                    for b in TUPLE_BINS:

                        print(b)

                        for root_file in os.listdir(TUPLES+year+"/"+ds+"/"+b+"/"):

                            print(root_file)

                            out = PDF_OUTPUT+year+"/"+ds+"/"+b+"/"
                            if not os.path.exists(out):
                                os.makedirs(out)
                                
                            fit_data(TUPLES+year+"/"+ds+"/"+b+"/"+root_file, shapes = ["G","E"] , year = year, variable = VAR, cuts = CUTS, out_dir = out, dset = ds, bin_type = b, refit_dictionary = None)


                print("Writing files...")
            
                writeFile(PDF_OUTPUT+year+"/asymmetry.txt", DICTIONARY, year)
                writeDict(PDF_OUTPUT+year+"/fitting_dictionary.py", DICTIONARY)

            print("Done")

            if (len(flags) > 0):
                print("Some files were flagged and might need refitting:")
                for flag in flags:
                    print(flag)

            print("To refit, use python fit.py -refit <year>:<dset>:<bin>:<file>")

            sys.exit()
            

                
        #5
        if(option == HANDLES[4]):
            if (len(sys.argv) == 3):
            
                year = sys.argv[2].split(":")[0]
                dset = sys.argv[2].split(":")[1]
                bin_type = sys.argv[2].split(":")[2]
                root_file = sys.argv[2].split(":")[3]

                if not year in YEARS:
                    print("Not a proper year")
                    sys.exit()

                if not dset in SETS:
                    print("Not a proper data set")
                    sys.exit()

                if not bin_type in TUPLE_BINS:
                    print("Not a proper bin")
                    sys.exit()
                    
                if not os.path.isfile(TUPLES+year+"/"+dset+"/"+bin_type+"/"+root_file):
                    print("File does not exist")
                    sys.exit()

                sys.path.insert(0, "/data/bfys/dwickrem/pdf_outputs/mass_fits/blinded_random/{}/{}/".format(RUN,YEAR))

                from fitting_dictionary import fitting_dictionary as refit_dictionary

                out = PDF_OUTPUT+year+"/"+ds+"/"+b+"/"

                fit_data(TUPLES+year+"/"+dset+"/"+bin_type+"/"+root_file, shapes = [], year = year, variable = VAR, cuts = CUTS, out_dir = out, dset = dset, bin_type = bin_type, refit_dictionary = refit_dictionary)

                print("Done")
                
            
            
        #6
        if(option == HANDLES[5]):

            for year in YEARS:

                if not os.path.exists(HISTOGRAM_OUTPUTS+year):
                    os.makedirs(HISTOGRAM_OUTPUTS+year)
                
                text = open(HISTOGRAM_OUTPUTS+year+"/afterHistograms.txt", "w")

                for ds in SETS:
                    for bin_type in TUPLE_BINS:
                        for root_file in os.listdir(TUPLES+year+"/"+ds+"/"+bin_type+"/"):

                            out = HISTOGRAM_OUTPUTS+year+"/"+ds+"/"+bin_type+"/"

                            if not os.path.exists(out):
                                os.makedirs(out)
                                

                            name, entries, mean, stdev = plot_histogram(TUPLES+year+"/"+ds+"/"+bin_type+"/"+root_file, out_dir = out, to_compare = True)
            
                            text.write(name)
                            text.write("\nEntries: "+entries)
                            text.write("\nMean: "+mean)
                            text.write("\nStd Dev: "+stdev)
                            text.write("\n")

                text.close()