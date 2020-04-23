
class Genome:
    """
    Keeps track of all genomic information, meaning what mutations are
    active or not.
    """

    def __init__(self, mutations):
        self.mut = mutations
        self.counter = 0
        self.visited = []  # Iterator counter

    def has(self, item):
        """
        checks if item is in mut dictionary.
        :params item: a mutation string name
        """
        return item in self.mut

    def transcribe(self, allo, lacOut, rep, glucose):
        """
        Checks status of both operator and promoter and if both are True
        then transcription can occur.
        """
        if self.operator(allo, lacOut, rep, glucose) and self.promoter():
            return True
        return False

    def promoter(self):
        """
        Models the Lactose operon promoter and simply return True
        if no mutation and False otherwise.

        Future notes:
        Promoter research article
        https://www.ncbi.nlm.nih.gov/pmc/articles/PMC178712/pdf/1790423.pdf
        """
        return self.mut['ProMutation'] is None

    def operator(self, allo, lacOut, rep, glucose):
        """
        Lactose operon operator, if there is no mutation within the operator
        then the repressor may be checked. Else operator will always be active.
        When lactose is present in the enviroment then other compounds within the
        cell will be converted to allo, thus the += 5 in the pressence of lacOut.

        Returns:
            Bool true or false, represents operator on or off.
        pre:
            only is affected by repressor when no mutations
        """
        if self.mut['OpMutation'] is None:
            for r in rep:
                if not r.bound(allo, lacOut, glucose):
                    return False
        return True

    def __iter__(self):
        return self

    def next(self):
        if self.counter < len(self.mut):
            for i in self.mut:
                if i not in self.visited:
                    self.visited.append(i)
                    self.counter += 1
                    return i
        else:
            self.counter = 0
            self.visited = []
            raise StopIteration

    def __str__(self):
        repr = ''
        for item in self.mut:
            repr += str(item) + " : " + str(self.mut[item]) + " "
        return repr
