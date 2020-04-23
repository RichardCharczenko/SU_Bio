'''Driver file for the LacOp project'''
from cellClass import Cell


def RunLO(mutL, plasmid, allo, lacIn, lacOut, Glu):
    mutations = convert_mutList_to_dict(mutL)
    cap = 'Inactive'
    if 'Active' in mutL:
        cap = 'Active'
    C = Cell(mutations, allo, lacIn, lacOut, Glu, cap)

    plasmid_mut = []
    if plasmid != []:
        shift = []
        for item in plasmid:
            shift.append(item[2:])
        C.add_plasmid(convert_mutList_to_dict(shift))
    C.generateData()
    return C

def convert_mutList_to_dict(list):
        mutL = {'ProMutation': None, 'BgalMutation': None,
                   'RepMutation': None, 'OpMutation': None,
                   'PermMutation': None}
        for item in list:
            if item[:4] != 'none':
                if item == 'lacP-':
                    mutL['ProMutation'] = item
                if item == 'lacIs' or item == 'lacI-':
                    mutL['RepMutation'] = item
                if item == 'lacY-':
                    mutL['PermMutation'] = item
                if item == 'lacOc':
                    mutL['OpMutation'] = item
                if item == 'lacZ-':
                    mutL['BgalMutation'] = item
        return mutL
