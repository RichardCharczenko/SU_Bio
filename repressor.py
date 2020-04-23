import random


class Repressor():
    '''Mimics repressor protein function, but in lacop program we assume
    that the repressor protein concentration is constant. If repressor is
    unbound that is represented as the boolean True'''
    repressorMut = {None: 'active', 'lacI-': 'inactive', 'lacIs':'stuck'}

    def __init__(self, mut):
        self.status = self.repressorMut[mut]

    def bound(self, allo, Le, glu):
        if self.status == 'stuck':
            return False
        if self.status == 'active':
            return self.conditionCheck(allo, Le, glu)
        if self.status == 'inactive':
            return True

    def conditionCheck(self, allo, Le, glu):
        '''Work needs to be done
        #I need the [S] vs bound Repressor info in order to
        #accuratly tell if rep is on or off
        below is all tentative work'''
        allo = allo - (glu/2)
        pBound = (allo / 100.0) #tentative equation
        num = random.random()
        return (num < pBound) #or Le > 50
