from mut import mut
import random

class Node():
    parent = None
    string_rep = ''

    def __init__(self, maxChildren, sequence, bibNum, datum = None, par = None):
        self.seq = sequence
        self.bib = bibNum
        self.data = datum
        self.max = maxChildren
        self.parent = par
        self.Nodes = []
        self.size = 0

    def enqueue(self, newNode):
        if (self.isEmpty()):
            self.Nodes.append(newNode)
            self.size += 1
            return
        elif (self.isFull()):
            raise Exception("Node is full")
        else:
            self.Nodes.append(newNode)


    def isEmpty(self):
        return self.size == 0

    def isFull(self):
        return self.size == self.max


    def build_string_repr(self, level = 0):
        self.string_rep = "\t"*level + '---Sequence' + self.bib + '\n'
        for child in self.Nodes:
            if child != None:
                self.string_rep += child.__repr__(level+1)
        return self.string_rep

    def __repr__(self, level = 0):
        ret = "\t"*level + '---Sequence' + self.bib + '\n'
        for child in self.Nodes:
            if child != None:
                ret += child.__repr__(level+1)
        return ret

    def __iter__(self):
        return self

class GenerateTree():
    phyloTree = None
    name = ''
    alphabet = ['A','B','C','D','E','F','G','H']


    def __init__(self, seq, seqType, gen = 4, div = 10, outPerIn = 2, default = True):
        '''Constructor intakes a sequence and the sequence type and generates
        a phylogenetic tree based on a certain divergence between parent and
        children sequences'''
        self.generations = gen
        self.sequence = seq
        self.seqType = seqType
        self.divergance = div
        self.outSeqsPerInSeq = outPerIn
        self.phyloTree = Node(outPerIn, seq, '.0')
        self.nodeNum = 0
        if default:
            self.populateTree()
            self.phyloTree.build_string_repr()

    def nextGeneration(self, seq, parent):
        newGeneration = mut(seq, self.divergance, self.seqType, parent.max)[1]
        count = 0
        for newSeq in newGeneration:
            num = random.randint(0, self.outSeqsPerInSeq + 1)
            self.nodeNum += 1
            name = '.' + str(self.nodeNum) + '.'+ self.alphabet[count]
            count += 1
            if count > 8:
                count = 0
            child = Node(num, newSeq, name, newGeneration[newSeq], parent)
            parent.enqueue(child)


    def populateTree(self):
        height = 1
        parents = []
        while height < self.generations:
            if self.phyloTree.isEmpty():
                curNode = self.phyloTree
                self.nextGeneration(curNode.seq, curNode)
                height += 1
                for node in self.phyloTree.Nodes:
                    parents.append(node)
            else:
                newParents = []
                for parent in parents:
                    if parent.isEmpty():
                        self.nextGeneration(parent.seq, parent)
                for parent in parents:
                    for node in parent.Nodes:
                        if node != None:
                            newParents.append(node)
                parents = newParents
                height += 1

    def printTree(self):
        print self.phyloTree
