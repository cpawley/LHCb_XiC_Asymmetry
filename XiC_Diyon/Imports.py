TUPLE_PATH = "/data/bfys/dwickrem/tuples/"
MC_TUPLE_PATH = "/data/bfys/dwickrem/mc_tuples/"
RAW_TUPLE_PATH = "/dcache/bfys/jdevries/ntuples/LcAnalysis/ganga/"

def getMCCuts (particle, run):
	IDcuts = "abs(piplus_ID)==211 && abs(kminus_ID)==321 && abs(pplus_ID)==2212 && abs(lcplus_ID)==4122"
	if run == 2:
		IDcuts += " && lcplus_Hlt2CharmHad{0}pToPpKmPipTurboDecision_TOS == 1".format(particle)
	if particle == "Lc":
		#BKGCAT = "(lcplus_BKGCAT == 0 || lcplus_BKGCAT == 50)"
		return IDcuts #+ "&&" + BKGCAT
	elif particle == "Xic":
		#BKGCAT = "(lcplus_BKGCAT == 0 || lcplus_BKGCAT == 10 || lcplus_BKGCAT == 50)"
		return IDcuts #+ "&&" + BKGCAT

def getDataCuts (run, blinded = False):
    if(blinded):
        cuts = "lcplus_L0HadronDecision_TOS == 1"
                
    else:
        cuts = "lcplus_P < 300000 && lcplus_OWNPV_CHI2 < 80 && pplus_ProbNNp > 0.5 && kminus_ProbNNk > 0.4 && piplus_ProbNNpi > 0.5 && pplus_P < 120000 && kminus_P < 115000 && piplus_P < 80000 && pplus_PIDp > 0 && kminus_PIDK > 0 && lcplus_L0HadronDecision_TOS == 1"


    if(run == 1):
        trigger_cuts = "lcplus_Hlt1TrackAllL0Decision_TOS == 1 && lcplus_Hlt2CharmHadD2HHHDecision_TOS ==1"
    elif(run == 2):
        trigger_cuts = "lcplus_Hlt1TrackMVADecision_TOS == 1"

    return cuts + " && " + trigger_cuts

def getBackgroundCuts(particle):
	if particle == "Lc":
		cuts = "(lcplus_MM > 2320 && lcplus_MM < 2350) || (lcplus_MM > 2220 && lcplus_MM < 2260)"
	elif particle == "Xic":
		cuts = "lcplus_MM > 2400 && lcplus_MM < 2450 || lcplus_MM > 2490"
	return cuts
    
def getPTbins():
	return [[3200,4000],[4000,5000], [5000,6000], [6000,7000], [7000,8000], [8000,10000], [10000,20000]]
    
def getYbins():
	return  [[2.0,2.5],[2.5,3.0], [3.0,3.5], [3.5,4.0]]


DATA_jobs_Dict = {
        "43":["2011_MagDown", 907],
	"45":["2011_MagUp", 817],
	"46":["2012_MagUp",1342],
	"42":["2012_MagDown",1155],
	"119":["2016_MagDown",527,"Lc"],
	"115":["2016_MagDown",186,"Xic"],
	"91":["2017_MagDown",529,"Lc"],
	"116":["2017_MagDown",257,"Xic"],
	"117":["2018_MagDown",471,"Xic"],
	"92":["2018_MagDown",656,"Lc"]
	} 

       
	
MC_jobs_Dict = {
	"NA":["2011","MagDown", 907,"Lc",""],
	"NA":["2011","MagDown", 907,"Xic",""],
	"NA":["2011","MagUp", 817,"Lc",""],
	"NA":["2011","MagUp", 817,"Xic",""],
	
	"88":["2012","MagDown", 25,"Lc","25103006"],
	"123":["2012","MagDown", 15,"Xic","25103029"],
	"87":["2012","MagUp", 25,"Lc","25103006"],
	"122":["2012","MagUp", 17,"Xic","25103029"],
	
	"107":["2016","MagDown", 290,"Lc","25203000"],
	"108":["2016","MagDown", 282,"Xic","26103090"],
	"105":["2016","MagUp", 281,"Lc","25203000"],
	"106":["2016","MagUp", 286,"Xic","26103090"],
	
	"NA":["2017","MagDown", 285,"Lc","25203000"],
	"102":["2017","MagDown", 281,"Xic","26103090"],
	"95":["2017","MagUp", 284,"Lc","25203000"],
	"96":["2017","MagUp", 284,"Xic","26103090"],
	
	"103":["2018","MagDown", 279,"Lc","25203000"],
	"104":["2018","MagDown", 277,"Xic","26103090"],
	"97":["2018","MagUp", 283,"Lc","25203000"],
	"98":["2018","MagUp", 278,"Xic","26103090"],
}
