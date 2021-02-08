# Written by Melika Yildiz and Nina Oskam (University of Amsterdam, Physics and Astronomy)
# Research Project - Jan 2021

"""Analyzesthe symmetry of the Xic, by comparing the yield of the chained sets of the baryonic and antimatter datasets\
    The code is split into two parts, anti and baryonic. For each datafiles, parameters were set. Note: if dataset == 5, the chained data is considered"""



import ROOT
from ROOT import TChain, TCanvas, TH1
import glob
import plotly.graph_objects as go

# import plotly
# from plotly import graph_objects as go

particle = "Xic"
chain = TChain("DecayTree")


################################################ Antimatter 
files_antimat = glob.glob ("pathname/*.root") # opens files
files_antimat.sort ()
files_antimat.append(files_antimat[0])

redChiSq_anti        = []
bukinYield_anti      = []
sigmabukinYield_anti = []

for i in range (1,6):
    # set parameter of each datafile
    dataset = i
    if dataset == 1:
        mass_range = [2430, 2510]
        peak_range = [2468,2466,2470]
        normalisation_factor = 1
        exponential_normalisation_factor = 1
        exponential_range = [-0.0019, -0.2, 0.2]
        width_range = [5.5, 0.01, 50]
        asym_range = [-0.01, -0.1, 0.1]
        rho1_range = [0.05, 0.01, 0.1]
        rho2_range = [0.03, 0.001, 0.1]

    if dataset == 2:
        mass_range = [2430, 2510]
        peak_range = [2468,2466,2470]
        normalisation_factor = 1
        exponential_normalisation_factor = 1
        exponential_range = [-0.0019, -0.2, 0.2]
        width_range = [5.5, 0.01, 50]
        asym_range = [-0.01, -0.1, 0.1]
        rho1_range = [0.05, 0.01, 0.1]
        rho2_range = [0.03, 0.001, 0.1]

    if dataset == 3:
        mass_range = [2430, 2510]
        peak_range = [2468,2466,2470]
        normalisation_factor = 1
        exponential_normalisation_factor = 1
        exponential_range = [-0.0013, -0.2, 0.2]
        width_range = [7.1, 0.01, 8]
        asym_range = [-0.001, -0.1, 0.1]
        rho1_range = [0.03, 0.01, 0.1]
        rho2_range = [0.001, 0.001, 0.1]

    if dataset == 4:
        mass_range = [2430, 2510]
        peak_range = [2468,2466,2470]
        normalisation_factor = 1
        exponential_normalisation_factor = 1
        exponential_range = [-0.0010, -0.2, 0.2]
        width_range = [4, 0.01, 8]
        asym_range = [-0.001, -0.1, 0.1]
        rho1_range = [0.03, 0.01, 0.1]
        rho2_range = [0.001, 0.001, 0.1]

    cuts = "1==1"
    nbins = 100
    varname = "lcplus_MM"

    # open data from file and get tree
    fileloc = files_antimat[i-1]
    f = ROOT.TFile.Open(fileloc, "READONLY")
    tree = f.Get("DecayTree")
    d = ROOT.TCanvas("d","d")

    # chained dataset
    if dataset == 5:
        tree = chain
        mass_range = [2430, 2510]
        peak_range = [2468,2466,2470]
        normalisation_factor = 1
        exponential_normalisation_factor = 1
        exponential_range = [-0.0010, -0.2, 0.2]
        width_range = [4, 0.01, 8]
        asym_range = [-0.001, -0.1, 0.1]
        rho1_range = [0.03, 0.01, 0.1]
        rho2_range = [0.001, 0.001, 0.1]
        i = "chained"

    mass= ROOT.RooRealVar("lcplus_MM","Lc_mass",mass_range[0],mass_range[1],"MeV/c^{2}")
    data = ROOT.RooDataSet("data","data set", tree, ROOT.RooArgSet(mass), cuts)

    # Bukin shape (peak): pdf + norm (yield)
    Bukin_Xp = ROOT.RooRealVar("Bukin_Xp", "Peak position", peak_range[0], peak_range[1], peak_range[2])
    Bukin_Sigp = ROOT.RooRealVar("Bukin_Sigp", "Peak width", width_range[0], width_range[1], width_range[2])
    Bukin_xi = ROOT.RooRealVar("Bukin_xi", "Peak asymmetry parameter", asym_range[0], asym_range[1], asym_range[2])
    Bukin_rho1 = ROOT.RooRealVar("Bukin_rho1", "Parameter of the left tail", rho1_range[0], rho1_range[1], rho1_range[2])
    Bukin_rho2 = ROOT.RooRealVar("Bukin_rho2", "Parameter of the right tail", rho2_range[0], rho2_range[1], rho2_range[2])
    Bukin_PDF = ROOT.RooBukinPdf("Bukin_PDF", "Bukin shape", mass, Bukin_Xp, Bukin_Sigp, Bukin_xi, Bukin_rho1, Bukin_rho2)
    Bukin_Norm = ROOT.RooRealVar("Bukin_Norm", "Bukin Yield", tree.GetEntries()/nbins * 3/normalisation_factor, 0, tree.GetEntries() * 2)

    # Exponential shape (background): pdf + norm (yield)
    exponential = ROOT.RooRealVar("exponential","C", exponential_range[0], exponential_range[1], exponential_range[2])
    myexponential = ROOT.RooExponential("myexponential","Exponential", mass, exponential)
    exponential_Norm  = ROOT.RooRealVar("exponential_Norm","Exponential Yield", tree.GetEntries()/nbins * 3/exponential_normalisation_factor, 0, tree.GetEntries() * 2)

    # combined signal shape
    Actual_signalshape = ROOT.RooExtendPdf("Actual_signalshape", "Signal shape", Bukin_PDF, Bukin_Norm)
    Actual_signalshape_Norm = ROOT.RooRealVar("Actual_signalshape_Norm","Signal Yield", tree.GetEntries()/nbins * 3/normalisation_factor, 0, tree.GetEntries() * 3)
    signalshape = ROOT.RooAddPdf("signalshape","Signal shape", ROOT.RooArgList(Actual_signalshape, myexponential), ROOT.RooArgList(Actual_signalshape_Norm, exponential_Norm) )

    # fit and plot
    mass_RooFit = ROOT.RooDataHist("masshist_RooFit","masshist RooFit", ROOT.RooArgList(mass), data)
    frame = mass.frame()
    mass_RooFit.plotOn(frame)
    fitresult = signalshape.fitTo(mass_RooFit)
    signalshape.plotOn(frame, ROOT.RooFit.Components("Actual_signalshape"), ROOT.RooFit.LineColor(8), ROOT.RooFit.LineStyle(2))
    signalshape.plotOn(frame, ROOT.RooFit.Components("myexponential"), ROOT.RooFit.LineColor(46), ROOT.RooFit.LineStyle(2))
    signalshape.plotOn(frame)
    frame.SetTitle("Mass fit {0} file {1}".format(particle, i))
    frame.GetYaxis().SetTitle("Number of events")
    frame.Draw()

    print("Chi2/NDF: {0}".format(frame.chiSquare()))
    print("Bukin Yield: {0} +- {1}".format(Actual_signalshape_Norm.getValV(),Actual_signalshape_Norm.getError()))
    print("Exponential Yield: {0} +- {1}".format(exponential_Norm.getValV(),exponential_Norm.getError()))

    d.SaveAs("fit_data_anti{}.pdf".format(i))
    redChiSq_anti.append (frame.chiSquare())
    bukinYield_anti.append (Actual_signalshape_Norm.getValV())
    sigmabukinYield_anti.append (Actual_signalshape_Norm.getError())

    chain.Add (fileloc)


################################################ Baryonic
files_baryonic = glob.glob ("pathname/*.root")
files_baryonic.sort ()
files_baryonic.append(files_baryonic[0])

redChiSq_baryonic        = []
bukinYield_baryonic      = []
sigmabukinYield_baryonic = []

chain = TChain("DecayTree")


for i in range (1,6):
    dataset = i
    if dataset == 1:
        mass_range = [2430, 2510]
        peak_range = [2468,2466,2470]
        normalisation_factor = 1
        exponential_normalisation_factor = 1
        exponential_range = [-0.0019, -0.2, 0.2]
        width_range = [5.5, 0.01, 50]
        asym_range = [-0.01, -0.1, 0.1]
        rho1_range = [0.05, 0.01, 0.1]
        rho2_range = [0.03, 0.001, 0.1]

    if dataset == 2:
        mass_range = [2430, 2510]
        peak_range = [2468,2466,2470]
        normalisation_factor = 1
        exponential_normalisation_factor = 1
        exponential_range = [-0.0019, -0.2, 0.2]
        width_range = [5.5, 0.01, 50]
        asym_range = [-0.01, -0.1, 0.1]
        rho1_range = [0.05, 0.01, 0.1]
        rho2_range = [0.03, 0.001, 0.1]

    if dataset == 3:
        mass_range = [2430, 2510]
        peak_range = [2468,2466,2470]
        normalisation_factor = 1
        exponential_normalisation_factor = 1
        exponential_range = [-0.0013, -0.2, 0.2]
        width_range = [6.3, 0.01, 50]
        asym_range = [-0.001, -0.1, 0.1]
        rho1_range = [0.03, 0.01, 0.1]
        rho2_range = [0.001, 0.001, 0.1]

    if dataset == 4:
        mass_range = [2430, 2510]
        peak_range = [2468,2466,2470]
        normalisation_factor = 1
        exponential_normalisation_factor = 1
        exponential_range = [-0.0010, -0.2, 0.2]
        width_range = [4, 0.01, 8]
        asym_range = [-0.001, -0.1, 0.1]
        rho1_range = [0.03, 0.01, 0.1]
        rho2_range = [0.001, 0.001, 0.1]

    cuts = "1==1"
    nbins = 100
    varname = "lcplus_MM"

    fileloc = files_baryonic[i-1]
    f = ROOT.TFile.Open(fileloc, "READONLY")
    tree = f.Get("DecayTree")
    c = ROOT.TCanvas("c","c")

    if dataset == 5:
        tree = chain
        mass_range = [2430, 2510]
        peak_range = [2468,2466,2470]
        normalisation_factor = 1
        exponential_normalisation_factor = 1
        exponential_range = [-0.0010, -0.2, 0.2]
        width_range = [4, 0.01, 8]
        asym_range = [-0.001, -0.1, 0.1]
        rho1_range = [0.03, 0.01, 0.1]
        rho2_range = [0.001, 0.001, 0.1]
        i = "chained"

    mass= ROOT.RooRealVar("lcplus_MM","Lc_mass",mass_range[0],mass_range[1],"MeV/c^{2}")
    data = ROOT.RooDataSet("data","data set", tree, ROOT.RooArgSet(mass), cuts)

    # Bukin shape (peak): pdf + norm (yield)
    Bukin_Xp = ROOT.RooRealVar("Bukin_Xp", "Peak position", peak_range[0], peak_range[1], peak_range[2])
    Bukin_Sigp = ROOT.RooRealVar("Bukin_Sigp", "Peak width", width_range[0], width_range[1], width_range[2])
    Bukin_xi = ROOT.RooRealVar("Bukin_xi", "Peak asymmetry parameter", asym_range[0], asym_range[1], asym_range[2])
    Bukin_rho1 = ROOT.RooRealVar("Bukin_rho1", "Parameter of the left tail", rho1_range[0], rho1_range[1], rho1_range[2])
    Bukin_rho2 = ROOT.RooRealVar("Bukin_rho2", "Parameter of the right tail", rho2_range[0], rho2_range[1], rho2_range[2])
    Bukin_PDF = ROOT.RooBukinPdf("Bukin_PDF", "Bukin shape", mass, Bukin_Xp, Bukin_Sigp, Bukin_xi, Bukin_rho1, Bukin_rho2)
    Bukin_Norm = ROOT.RooRealVar("Bukin_Norm", "Bukin Yield", tree.GetEntries()/nbins * 3/normalisation_factor, 0, tree.GetEntries() * 2)

    # Exponential shape (background): pdf + norm (yield)
    exponential = ROOT.RooRealVar("exponential","C", exponential_range[0], exponential_range[1], exponential_range[2])
    myexponential = ROOT.RooExponential("myexponential","Exponential", mass, exponential)
    exponential_Norm  = ROOT.RooRealVar("exponential_Norm","Exponential Yield", tree.GetEntries()/nbins * 3/exponential_normalisation_factor, 0, tree.GetEntries() * 2)

    # combined signal shape
    Actual_signalshape = ROOT.RooExtendPdf("Actual_signalshape", "Signal shape", Bukin_PDF, Bukin_Norm)
    Actual_signalshape_Norm = ROOT.RooRealVar("Actual_signalshape_Norm","Signal Yield", tree.GetEntries()/nbins * 3/normalisation_factor, 0, tree.GetEntries() * 3)
    signalshape = ROOT.RooAddPdf("signalshape","Signal shape", ROOT.RooArgList(Actual_signalshape, myexponential), ROOT.RooArgList(Actual_signalshape_Norm, exponential_Norm) )

    # fit and plot
    mass_RooFit = ROOT.RooDataHist("masshist_RooFit","masshist RooFit", ROOT.RooArgList(mass), data)
    frame = mass.frame()
    mass_RooFit.plotOn(frame)
    fitresult = signalshape.fitTo(mass_RooFit)
    signalshape.plotOn(frame, ROOT.RooFit.Components("Actual_signalshape"), ROOT.RooFit.LineColor(8), ROOT.RooFit.LineStyle(2))
    signalshape.plotOn(frame, ROOT.RooFit.Components("myexponential"), ROOT.RooFit.LineColor(46), ROOT.RooFit.LineStyle(2))
    signalshape.plotOn(frame)
    frame.SetTitle("Mass fit {0} file {1}".format(particle, i))
    frame.GetYaxis().SetTitle("Number of events")
    frame.Draw()

    print("Chi2/NDF: {0}".format(frame.chiSquare()))
    print("Bukin Yield: {0} +- {1}".format(Actual_signalshape_Norm.getValV(),Actual_signalshape_Norm.getError()))
    print("Exponential Yield: {0} +- {1}".format(exponential_Norm.getValV(),exponential_Norm.getError()))

    c.SaveAs("fit_data_bary{}.pdf".format(i))
    redChiSq_baryonic.append (frame.chiSquare())
    bukinYield_baryonic.append (Actual_signalshape_Norm.getValV())
    sigmabukinYield_baryonic.append (Actual_signalshape_Norm.getError())

    chain.Add (fileloc)


################################################ Analysis
asym_vals = []
for i in range (0, len(bukinYield_anti)):
    sigma_yields = bukinYield_anti[i] - bukinYield_baryonic[i]
    sum_yields = bukinYield_anti[i] + bukinYield_baryonic[i]
    asym_vals.append (sigma_yields / sum_yields)


# print ("Baryonic Chi2/NDF:{}".format (redChiSq_baryonic))
# print ("Baryonic Bukin Yield:{}".format (bukinYield_baryonic))
# print ("Baryonic Sigma Bukin Yield:{}".format (sigmabukinYield_baryonic))
# print ("Antimatter Chi2/NDF:{}".format(redChiSq_anti))
# print ("Antimatter Bukin Yield:{}".format (bukinYield_anti))
# print ("Antimatter Sigma Bukin Yield:{}".format (sigmabukinYield_anti))

# print ("Asymmetry values: {}".format (asym_vals))

barTable = go.Figure(data=[go.Table(header=dict(values=['Repidity', 'CHi2/NDF', 'Bukin Yield']),
                 cells=dict(values=[['2.0 - 2.5', '2.5 - 3.0', '3.0 - 3.5','3.5 - 4.0', 'Chained Tree' ],

                                    # row with reduced Chi2
                                    ['{:.3f}'.format(redChiSq_baryonic[0]),
                                     '{:.3f}'.format(redChiSq_baryonic[1]),
                                     '{:.3f}'.format(redChiSq_baryonic[2]),
                                     '{:.3f}'.format(redChiSq_baryonic[3]),
                                     '{:.3f}'.format(redChiSq_baryonic[4])],

                                    # row with bukin yield
                                    ['{0:.3e} +- {1:.3e}'.format (bukinYield_baryonic[0], sigmabukinYield_baryonic[0]),
                                     '{0:.3e} +- {1:.3e}'.format (bukinYield_baryonic[1], sigmabukinYield_baryonic[1]),
                                     '{0:.3e} +- {1:.3e}'.format (bukinYield_baryonic[2], sigmabukinYield_baryonic[2]),
                                     '{0:.3e} +- {1:.3e}'.format (bukinYield_baryonic[3], sigmabukinYield_baryonic[3]),
                                     '{0:.3e} +- {1:.3e}'.format (bukinYield_baryonic[4], sigmabukinYield_baryonic[4])]]))
                     ])
barTable.update_layout (title = 'Representation of results for baryonic matter')

antiTable = go.Figure(data=[go.Table(header=dict(values=['Repidity', 'CHi2/NDF', 'Bukin Yield']),
                 cells=dict(values=[['2.0 - 2.5', '2.5 - 3.0', '3.0 - 3.5','3.5 - 4.0', 'Chained Tree' ],

                                    # row with reduced Chi2
                                    ['{:.3f}'.format(redChiSq_anti[0]),
                                     '{:.3f}'.format(redChiSq_anti[1]),
                                     '{:.3f}'.format(redChiSq_anti[2]),
                                     '{:.3f}'.format(redChiSq_anti[3]),
                                     '{:.3f}'.format(redChiSq_anti[4])],

                                    # row with bukin yield
                                    ['{0:.3e} +- {1:.3e}'.format (bukinYield_anti[0], sigmabukinYield_anti[0]),
                                     '{0:.3e} +- {1:.3e}'.format (bukinYield_anti[1], sigmabukinYield_anti[1]),
                                     '{0:.3e} +- {1:.3e}'.format (bukinYield_anti[2], sigmabukinYield_anti[2]),
                                     '{0:.3e} +- {1:.3e}'.format (bukinYield_anti[3], sigmabukinYield_anti[3]),
                                     '{0:.3e} +- {1:.3e}'.format (bukinYield_anti[4], sigmabukinYield_anti[4])]]))
                     ])
antiTable.update_layout (title = 'Representation of results for antimatter')

asymTable = go.Figure(data=[go.Table(header=dict(values=['Repidity', 'f_asymmetry']),
                 cells=dict(values=[['2.0 - 2.5', '2.5 - 3.0', '3.0 - 3.5','3.5 - 4.0', 'Chained Tree' ],

                                    ['{0:.3f}'.format (asym_vals[0]),
                                     '{0:.3f}'.format (asym_vals[1]),
                                     '{0:.3f}'.format (asym_vals[2]),
                                     '{0:.3f}'.format (asym_vals[3]),
                                     '{0:.3f}'.format (asym_vals[4])]]))
                     ])
asymTable.update_layout (title = 'f_symmetry of matter-antimatter files with corresponding repidity')


antiTable.show()
barTable.show()
asymTable.show ()

