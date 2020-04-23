#This module keeps track of all the insertion and deletion changes

AAweight = {
            "A":"89Da","R":"174Da","N":"132Da","D":"133Da",
            "B":"133Da","C":"121Da","Q":"146Da","E":"147Da",
            "Z":"147Da","G":"75Da","H":"155Da","I":"131Da",
            "L":"131Da","K":"146Da","M":"149Da","F":"165Da",
            "P":"115Da","S":"105Da","T":"119Da","W":"204Da",
            "Y":"181Da","V":"117Da"
            }

AAdictionary = {
                "K":"Positive","H":"Positive","R":"Positive",
                "D":"Negative","E":"Negative","S":"Uncharged",
                "T":"Uncharged","N":"Uncharged","Q":"Uncharged",
                "A":"Hydrophobic","V":"Hydrophobic","I":"Hydrophobic",
                "L":"Hrydrophobic","M":"Hydrophobic","F":"Hydrophobic",
                "Y":"Hydrophobic","W":"Hydrophobic","C":"Other",
                "U":"Other","G":"Other","P":"Other"
                }


def insertlog(add):
    #tracks change of insertions
    totalWeight = 0
    change = AAdictionary[add]
    totalWeight += int(AAweight[add][:-2])
    return int(totalWeight), change #returns the weight changed, the AA change and the position of change


def delLog(deleted):
    """tracks change in deletions of amino acids"""
    weight = int((AAweight[deleted.upper()])[:-2])# + " lost"
    change = AAdictionary[deleted.upper()]
    return -weight, change

def pointChange(new, old):
    """Keeps track of single point changes in proteins"""
    weightChange = int(AAweight[new][:-2]) - int(AAweight[old][:-2]) 
    pointChange  = [AAdictionary[old], AAdictionary[new]]
    return weightChange, pointChange

                                    
         
def AAlogProcess(AAlog):
    totalWeight = 0
    #repeatLog = AArepeat(AAlog)
    
    for key in AAlog:
        if AAlog[key][2] == "Del":
            change = delLog(AAlog[key][1])
            totalWeight += change[0]
        if AAlog[key][2] == "In":
            change = insertlog(AAlog[key][1])
            totalWeight += change[0]
        if AAlog[key][2] == "Point":
            change = pointChange(AAlog[key][1], AAlog[key][3].upper())
            totalWeight += change[0]
    return totalWeight
            
    
#TESTCODE
#print compare("malw", "malK")

#print AAlogProcess({1:[27,"R","Point","T"], 2:[24,"R","Del"],3:[25,"S","Point","V"]})
#print insertlog('R')
#print delLog ('T')
