import random

from repressor import Repressor
from permease import permease
from bGal import Bgal
from GenomeInfo import Genome
from cc_Complex import CAPcAMP


class Cell:
    """
    Overarching class that controls all data from lactose operon
    """
    permEnz = []
    bgalEnz = []
    archiveConditions = {'perm': [], 'bgal': [],
                         'allo': [], 'lacIn': [],
                         'lacOut': [], 'glucose + galactose': []}
    time = 0.0
    # TODO : Add an iterator that will iterate through time intervals

    def __init__(self, mutList, allo, lacIn, lacOut, glu, capStatus = 'Inactive', time=400):
        self.permNum = 0
        self.bgalNum = 0
        self.gluGal = glu
        self.DNA = Genome(mutList)
        self.plasmid = False
        self.plasmid_data = None
        self.allo = allo
        self.lacIn = lacIn
        self.lacOut = lacOut
        self.rep = []  # Repressor(self.get_mutation('RepMutation', self.DNA))
        self.CAP = CAPcAMP(capStatus)

    def add_plasmid(self, plasmid_mut):
        """
        Updates the class with Sequence data for a plasmid.

        :param plasmid_mut: a list of plasmid mutations
        """
        self.plasmid_data = Genome(plasmid_mut)
        self.plasmid = True

    def get_mutation(self, mutation, location):
        """
        Retrieves mutation from genome object, checks both DNA genome object and plasmid
        Genome object.
        """
        gene_data = location.mut[mutation]
        return gene_data

    def signal(self):
        if self.lacOut > 50 and self.DNA.mut['PermMutation'] == None:
            self.allo += 2

    def translate(self, location):
        """
        Increases the amount of enzyme class objects, the number of new objects
        varies based of wether the CAP-cAMP complex is is active or not. The previouse
        number of objects is recorded to be used in graph data later.
        """

        if location.transcribe(self.allo, self.lacOut, self.rep, self.gluGal):
            if (location == self.DNA):
                transNum = 1
                if self.CAP.get_status(self.gluGal):
                    transNum = 6
                for i in range(transNum):
                    for gene in location:
                        if gene == "BgalMutation" and location.mut[gene] is None:
                            if random.randint(1, 8) == 1:  # B-Gal is transcribed more than Perm on the mRNA strand.
                                self.bgalEnz.append(Bgal(self.get_mutation('BgalMutation', location)))
                            self.bgalEnz.append(Bgal(self.get_mutation('BgalMutation', location)))
                        if gene == "PermMutation" and location.mut[gene] is None:
                            self.permEnz.append(permease(self.get_mutation('PermMutation', location)))
            else:
                for item in location:
                    if item == "BgalMutation" and location.mut[item] == None:
                        self.bgalEnz.append(Bgal(self.get_mutation('BgalMutation', location)))
                    if item == "PermMutation" and location.mut[item] == None:
                        self.permEnz.append(permease(self.get_mutation('PermMutation', location)))

    def degrade(self):
        """
        Mimics degradation lactose operon proteins
        """
        degrade_rate = (len(self.permEnz) + len(self.bgalEnz)) / 10
        if degrade_rate == 0:
            degrade_rate = 1
        for int in range(degrade_rate):
            num = random.randint(1,2)
            if num == 1:
                if self.permEnz:
                    value = self.permEnz.pop(len(self.permEnz)-1)
                if self.bgalEnz:
                    value = self.bgalEnz.pop(len(self.bgalEnz)-1)

    def backgroundTranscription(self, location):
        """
        biologicaly occures even if the lac operon is being regulated,
         and creates small amounts of protein.
        """
        if self.get_mutation('RepMutation', self.DNA) == 'lacIs':
            return
        if self.plasmid:
            if self.get_mutation('RepMutation', self.plasmid_data) == 'lacIs':
                return
        num = random.randint(1,12)
        if num == 1:
            if self.get_mutation('PermMutation', location) == None:
                self.permEnz.append(permease(self.get_mutation('PermMutation', location)))
            if self.get_mutation('BgalMutation', location) == None:
                self.bgalEnz.append(Bgal(self.get_mutation('BgalMutation', location)))

    def activeEnzymes(self):
        """
        Activates all lactose operon enzymes within cell, meaning
        that the all enzymes will be passes the sugar values and then
        then calculate the change in each concentration based on.
        """
        self.archiveConditions['allo'].append(self.allo)
        self.archiveConditions['lacIn'].append(self.lacIn)
        self.archiveConditions['lacOut'].append(self.lacOut)
        self.archiveConditions['glucose + galactose'].append(self.gluGal)
        for item in self.permEnz:
            change = item.rate(self.lacOut, self.lacIn)
            self.lacOut = change[0]
            self.lacIn = change[1]

        for item in self.bgalEnz:
            change = item.catalyze(self.lacIn, self.allo)
            if change[1] == 'lac':
                self.lacIn -= change[0]
                self.allo += change[0]
            else:
                self.allo -= change[0]
                self.gluGal += change[0]

    def backGroundTransport(self):
        """
        Background trasnport occures occures independant of
        permease protein.
        """
        if self.lacIn > 0 and self.lacOut > 0:
            num = random.randint(1,3)
            if num == 1 and self.lacOut > 1.0:
                self.lacOut -= 0.2
                self.lacIn += 0.2

    def generateData(self, time = 400.0):
        """
        Generates Data used in graphical output, essentially a driver
        for the cell class that runs the cell object for 400 iterations.
        """
        self.permEnz = []
        self.bgalEnz = []
        self.archiveConditions = {'perm': [], 'bgal': [],
                                 'allo': [], 'lacIn': [],
                                 'lacOut': [], 'glucose + galactose': []}
        while self.time < time:  # 400 is a the arviturary time set for the simulation to run
            self.archiveConditions['perm'].append(len(self.permEnz))
            self.archiveConditions['bgal'].append(len(self.bgalEnz))
            # repressor
            self.rep.append(Repressor(self.get_mutation('RepMutation', self.DNA)))
            if self.plasmid and self.plasmid_data.has('RepMutation'):
                self.rep.append(Repressor(self.get_mutation('RepMutation', self.plasmid_data)))
            # translation
            self.translate(self.DNA)
            if self.plasmid:
                self.translate(self.plasmid_data)
                if self.get_mutation('ProMutation', self.plasmid_data) is None:
                    self.backgroundTranscription(self.plasmid_data)
            if self.get_mutation('ProMutation', self.DNA) is None:
                self.backgroundTranscription(self.DNA)
            # degradataion
            if self.lacOut + self.lacIn + self.allo < random.randint(0, 50)\
                    and not self.DNA.transcribe(self.allo, self.lacOut, self.rep, self.gluGal):
                self.degrade()
            # enzyme activity
            self.activeEnzymes()
            self.backGroundTransport()
            self.time = self.time + 1
