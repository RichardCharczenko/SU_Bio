'''
Author: Richard Charczenko
Last Edited: 11/20/2018

Any research articles for permease should be listed below:

'''
class permease(object):
    '''mimics permease membrane protein, is constructed with either no mutation
    or a non-functional mutation (lacY-).

    Biological meaning: the lacY- mutant is a non-functional protein that is
    constructed at the same rate as a WT Protein

    Implemenation invariance: the lacY- causes the rate function to always increment
    the passed in doubles by 0.'''
    permeaseMut = {None:0.2, 'lacY-':0.0 } #Dictionary of equilibrium constants based on mutation

    def __init__(self, mut):
        self.mut = mut#allows for some permease to have mutations
        self.age = 0

    def rate(self, lacO, lacI):
        '''affects equilibrium of permease'''
        self.age += 1
        if lacO > 1.0:
            return (lacO - self.permeaseMut[self.mut]), (lacI + self.permeaseMut[self.mut])#permease is based on a equilibrium, need to do research here
        return lacO, lacI
