import random


class Bgal(object):
    """
    mimics the functionality of B-Gal, assuming Mg is a cofactor
    and reaction takes place at 30 degrees C.
    """

    def __init__(self, mut):
        """
        :param mut: mutation of bgal object, a string that is either lacZ-, or None
        """
        self.mut = mut
        self.age = 0

    def catalyze(self, lacIn, allo):
        """
        Handles BetaGalactisidase catalyzation
        :param lacIn: lactose inside cell concentration
        :param allo: allolactose concentration
        """
        self.age += 1
        if self.mut == 'lacZ-':
            return 0, 'lac'
        if allo < 1 and lacIn < 1:
            return 0, 'lac'
        p = (lacIn/(allo+lacIn))
        choice = random.random()
        if choice < p and lacIn > 1:
            return self.Lrate(lacIn), 'lac'
        elif allo > 1:
            return self.Arate(allo), 'allo'
        else:
            return 0, 'allo'

    def Arate(self, allo):
        """
        Uses the Michaelis menten equation and the current concentration of allolactose
        to determine the rate or the amount of allolactose reduced.

        :param allo: allolactose concentration
        """
        KmAllo = 9400  # in uM, and found from:http://www.uniprot.org/uniprot/P00722
        VmaxAllo = 4.97  # in umol/min/mg[E] and found from:http://www.uniprot.org/uniprot/P00722
        if self.mut == None:
            v = (VmaxAllo*allo)/(KmAllo + allo)
            return v

    def Lrate(self, lacIn):
        """
        Uses the Michaelis menten equation and the current concentration of lactose
        to determine the rate or the amount of lactose reduced

        :param lacIn:
        """
        KmLactose = 1350.0  # Found from:http://www.uniprot.org/uniprot/P00722
        VmaxLactose = 30.9  # Found from:http://www.uniprot.org/uniprot/P00722
        if self.mut == None:
            v = (VmaxLactose * lacIn)/(KmLactose + lacIn)  # Michaelis-menten equation
            return v
