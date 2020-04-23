class singleAAchange(object):
    """
    A class to handle single mutation changes in fase.
    """
    AAdictionary = {
        "K": "Positive", "H": "Positive", "R": "Positive",
        "D": "Negative", "E": "Negative", "S": "Uncharged",
        "T": "Uncharged", "N": "Uncharged", "Q": "Uncharged",
        "A": "Hydrophobic", "V": "Hydrophobic", "I": "Hydrophobic",
        "L": "Hrydrophobic", "M": "Hydrophobic", "F": "Hydrophobic",
        "Y": "Hydrophobic", "W": "Hydrophobic", "C": "Other",
        "U": "Other", "G": "Other", "P": "Other"
    }

    def __init__(self, changeLog):
        """
        :params changeLog: A existing changelog
        """
        self.log = changeLog
        self.polarChange = {}

    def pointChange(self, item):
        """
        Handles a single point change
        :params item: a amino acid
        """
        oldAA = item[3].upper()
        newAA = item[1].upper()
        self.polarChange[item[0]] = [oldAA,
                                     self.AAdictionary[oldAA],
                                     newAA,
                                     self.AAdictionary[newAA],
                                     "Point"]

    def delChange(self, item):
        self.polarChange[item[0]] = [item[1],
                                     self.AAdictionary[item[1].upper()],
                                     "Del"]

    def inChange(self, item):
        self.polarChange[item[0]] = [item[1],
                                     self.AAdictionary[item[1].upper()],
                                     "In"]

    def change(self):
        for key in self.log:
            item = self.log[key]
            if item[-1] == "silent":
                continue
            else:
                if item[2] == "Point":
                    self.pointChange(item)
                if item[2] == "Del":
                    self.delChange(item)
                if item[2] == "In":
                    self.inChange(item)
        return self.polarChange
