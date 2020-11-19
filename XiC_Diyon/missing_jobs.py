"""
This holds a dictionary containing all the missing jobs from the grid
"""

JOBS = {"115":["background",170]}

VARS = {"background":["lcplus_PVConstrainedDTF_chi2","lcplus_Hlt2CharmHadXicpToPpKmPipTurboDecision_TOS"]}

def skipJob(label, job, subjob):

    if job in JOBS:
        if (JOBS[job][0] == label) and (JOBS[job][1] == subjob):
            return True
        else:
            return False
    else: 
        return False


def skipVar(label, var):
    
    if label in VARS:
        if var in VARS[label]:
            return True
        else:
            return False

    else:
        return False
        

            
    
