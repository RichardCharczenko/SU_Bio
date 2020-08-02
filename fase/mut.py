import random
# Change Log#
from InDelLog import *
from shift import *
from AAchange import *


def mut(sequence, divergance, seqType, outSeqsPerInSeq):
    '''Mutates sequence string to iteratively based on  % divergance,
      then returns one or more sequences if user wants more output Seqs for phyGen analysis, etc'''
    lenSequence = len(sequence)
    diverganceFraction = (divergance / float(100))
    mutationRounds = int(lenSequence * diverganceFraction)
    if mutationRounds < 1:
        mutationsRounds = 1
    sequenceList = []
    sequence = sequence.lower()
    seq = sequence
    sequence = list(sequence)

    masterLog = {}
    changeLog = {}
    for mutation in range(mutationRounds):
        pos = random.randint(0, lenSequence - 1)

        if (seqType == 'nuc'):
            sequence[pos] = mutN(sequence[pos])

        if (seqType == 'pep'):
            AAchange = mutA(sequence[pos], pos)
            if len(AAchange) == 2:  # Handles insertions
                sequence.insert(pos + 1, AAchange[1])
                lenSequence = len(sequence)
                changeLog[mutation] = [pos + 1, AAchange[1], "In"]
            if AAchange == '':  # Handles deletions
                changeLog[mutation] = [pos, sequence.pop(pos), "Del"]
                lenSequence = len(sequence)
            if len(AAchange) == 1:  # normal single point change
                changeLog[mutation] = [pos, AAchange, "Point", sequence[pos]]
                sequence[pos] = AAchange

        newSequence = ''.join(sequence)
        if newSequence in masterLog:  # occures in duplicate happens
            del masterLog[newSequence]
            for i in sequenceList:
                if i[0] == newSequence:
                    sequenceList.remove(i)
        masterLog[newSequence] = changeLog.copy()
        sequenceList.append([newSequence, changeLog])  # collects all the mutated seqs
        if len(masterLog) != len(sequenceList):
            raise ValueError("sequenceList and masterLog desynced")
    while len(sequenceList) > outSeqsPerInSeq:  # eliminates most intermediates, seq
        # leaving num requsted by user
        toRemove = random.randint(0, len(sequenceList) - 1)  # note: will not remove final seq
        removed = sequenceList[toRemove]
        sequenceList.remove(sequenceList[toRemove])
        try:
            del masterLog[removed[0]]
        except KeyError:
            raise KeyError('oops')
    return seq, masterLog  # [sequenceList[0][0]]#sequenceList,


def mutA(aa, pos):
    '''Takes an amino acid, swaps out for another'''
    aa = aa.upper()
    # estimated from http://gbe.oxfordjournals.org/content/7/6/1815.full.pdf+html
    # Indel Rate per kbase pair, in a protein,nondisordered regions about .075 in DNA
    # ratio of indels to substitutions about 0.05-0.1
    indelNum = random.randint(1, 30)
    if (indelNum == 1):  # delete
        return ''
    elif (indelNum == 2):
        aaList = ('A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V')
        newAa = random.choice(aaList)

        insertion = aa + newAa
        return insertion

        # Blosum62 used to guide realative frequency of each substittion
        #  inspired by http://www.ncbi.nlm.nih.gov/pubmed/15286655

    if (aa == 'A'):
        aaList = ((['A'] * 0) + (['R'] * 3) + (['N'] * 2) + (['D'] * 2) + (['C'] * 4) + (['Q'] * 3) + (['E'] * 3) + (
                    ['G'] * 4) + (['H'] * 2) + (['I'] * 3) + (['L'] * 3) + (['K'] * 3) + (['M'] * 3) + (['F'] * 2) + (
                              ['P'] * 3) + (['S'] * 5) + (['T'] * 4) + (['W'] * 1) + (['Y'] * 2) + (['V'] * 4))
    elif (aa == 'R'):
        aaList = ((['A'] * 3) + (['R'] * 0) + (['N'] * 4) + (['D'] * 2) + (['C'] * 1) + (['Q'] * 3) + (['E'] * 5) + (
                    ['G'] * 4) + (['H'] * 2) + (['I'] * 1) + (['L'] * 2) + (['K'] * 6) + (['M'] * 3) + (['F'] * 1) + (
                              ['P'] * 2) + (['S'] * 3) + (['T'] * 3) + (['W'] * 1) + (['Y'] * 2) + (['V'] * 1))
    elif (aa == 'N'):
        aaList = ((['A'] * 0) + (['R'] * 3) + (['N'] * 2) + (['D'] * 2) + (['C'] * 4) + (['Q'] * 3) + (['E'] * 3) + (
                    ['G'] * 4) + (['H'] * 2) + (['I'] * 3) + (['L'] * 3) + (['K'] * 3) + (['M'] * 3) + (['F'] * 2) + (
                              ['P'] * 3) + (['S'] * 5) + (['T'] * 4) + (['W'] * 1) + (['Y'] * 2) + (['V'] * 4))
    elif (aa == 'D'):
        aaList = ((['A'] * 3) + (['R'] * 3) + (['N'] * 5) + (['D'] * 0) + (['C'] * 2) + (['Q'] * 5) + (['E'] * 7) + (
                    ['G'] * 4) + (['H'] * 4) + (['I'] * 2) + (['L'] * 1) + (['K'] * 4) + (['M'] * 2) + (['F'] * 2) + (
                              ['P'] * 4) + (['S'] * 5) + (['T'] * 4) + (['W'] * 1) + (['Y'] * 2) + (['V'] * 2))
    elif (aa == 'C'):
        aaList = ((['A'] * 5) + (['R'] * 2) + (['N'] * 2) + (['D'] * 3) + (['C'] * 0) + (['Q'] * 2) + (['E'] * 1) + (
                    ['G'] * 2) + (['H'] * 2) + (['I'] * 4) + (['L'] * 4) + (['K'] * 2) + (['M'] * 4) + (['F'] * 3) + (
                              ['P'] * 2) + (['S'] * 4) + (['T'] * 4) + (['W'] * 3) + (['Y'] * 3) + (['V'] * 4))
    elif (aa == 'Q'):
        aaList = ((['A'] * 3) + (['R'] * 5) + (['N'] * 4) + (['D'] * 4) + (['C'] * 1) + (['Q'] * 0) + (['E'] * 6) + (
                    ['G'] * 2) + (['H'] * 4) + (['I'] * 1) + (['L'] * 2) + (['K'] * 5) + (['M'] * 4) + (['F'] * 1) + (
                              ['P'] * 3) + (['S'] * 4) + (['T'] * 3) + (['W'] * 2) + (['Y'] * 3) + (['V'] * 2))
    elif (aa == 'E'):
        aaList = ((['A'] * 4) + (['R'] * 5) + (['N'] * 5) + (['D'] * 7) + (['C'] * 1) + (['Q'] * 7) + (['E'] * 0) + (
                    ['G'] * 3) + (['H'] * 5) + (['I'] * 2) + (['L'] * 2) + (['K'] * 6) + (['M'] * 3) + (['F'] * 2) + (
                              ['P'] * 4) + (['S'] * 5) + (['T'] * 4) + (['W'] * 2) + (['Y'] * 3) + (['V'] * 3))
    elif (aa == 'G'):
        aaList = ((['A'] * 5) + (['R'] * 3) + (['N'] * 5) + (['D'] * 4) + (['C'] * 4) + (['Q'] * 3) + (['E'] * 3) + (
                    ['G'] * 0) + (['H'] * 3) + (['I'] * 1) + (['L'] * 1) + (['K'] * 3) + (['M'] * 2) + (['F'] * 2) + (
                              ['P'] * 3) + (['S'] * 5) + (['T'] * 3) + (['W'] * 3) + (['Y'] * 2) + (['V'] * 2))
    elif (aa == 'H'):
        aaList = ((['A'] * 2) + (['R'] * 4) + (['N'] * 5) + (['D'] * 3) + (['C'] * 1) + (['Q'] * 4) + (['E'] * 4) + (
                    ['G'] * 2) + (['H'] * 0) + (['I'] * 1) + (['L'] * 1) + (['K'] * 3) + (['M'] * 2) + (['F'] * 3) + (
                              ['P'] * 2) + (['S'] * 3) + (['T'] * 2) + (['W'] * 2) + (['Y'] * 6) + (['V'] * 1))
    elif (aa == 'I'):
        aaList = ((['A'] * 4) + (['R'] * 2) + (['N'] * 2) + (['D'] * 2) + (['C'] * 4) + (['Q'] * 2) + (['E'] * 2) + (
                    ['G'] * 1) + (['H'] * 2) + (['I'] * 0) + (['L'] * 7) + (['K'] * 2) + (['M'] * 6) + (['F'] * 5) + (
                              ['P'] * 2) + (['S'] * 3) + (['T'] * 4) + (['W'] * 2) + (['Y'] * 4) + (['V'] * 8))
    elif (aa == 'L'):
        aaList = ((['A'] * 4) + (['R'] * 3) + (['N'] * 2) + (['D'] * 1) + (['C'] * 4) + (['Q'] * 3) + (['E'] * 2) + (
                    ['G'] * 1) + (['H'] * 2) + (['I'] * 7) + (['L'] * 0) + (['K'] * 3) + (['M'] * 7) + (['F'] * 5) + (
                              ['P'] * 2) + (['S'] * 3) + (['T'] * 4) + (['W'] * 3) + (['Y'] * 4) + (['V'] * 6))
    elif (aa == 'K'):
        aaList = ((['A'] * 3) + (['R'] * 6) + (['N'] * 4) + (['D'] * 1) + (['C'] * 3) + (['Q'] * 5) + (['E'] * 5) + (
                    ['G'] * 2) + (['H'] * 3) + (['I'] * 1) + (['L'] * 2) + (['K'] * 0) + (['M'] * 3) + (['F'] * 1) + (
                              ['P'] * 3) + (['S'] * 4) + (['T'] * 3) + (['W'] * 1) + (['Y'] * 2) + (['V'] * 2))
    elif (aa == 'M'):
        aaList = ((['A'] * 2) + (['R'] * 2) + (['N'] * 1) + (['D'] * 0) + (['C'] * 4) + (['Q'] * 3) + (['E'] * 1) + (
                    ['G'] * 0) + (['H'] * 1) + (['I'] * 4) + (['L'] * 5) + (['K'] * 2) + (['M'] * 0) + (['F'] * 3) + (
                              ['P'] * 1) + (['S'] * 2) + (['T'] * 2) + (['W'] * 2) + (['Y'] * 2) + (['V'] * 4))
    elif (aa == 'F'):
        aaList = ((['A'] * 3) + (['R'] * 2) + (['N'] * 2) + (['D'] * 2) + (['C'] * 3) + (['Q'] * 2) + (['E'] * 2) + (
                    ['G'] * 2) + (['H'] * 4) + (['I'] * 5) + (['L'] * 5) + (['K'] * 2) + (['M'] * 5) + (['F'] * 0) + (
                              ['P'] * 1) + (['S'] * 3) + (['T'] * 3) + (['W'] * 6) + (['Y'] * 8) + (['V'] * 4))
    elif (aa == 'P'):
        aaList = ((['A'] * 4) + (['R'] * 3) + (['N'] * 3) + (['D'] * 4) + (['C'] * 2) + (['Q'] * 4) + (['E'] * 4) + (
                    ['G'] * 3) + (['H'] * 3) + (['I'] * 2) + (['L'] * 2) + (['K'] * 4) + (['M'] * 7) + (['F'] * 1) + (
                              ['P'] * 0) + (['S'] * 4) + (['T'] * 4) + (['W'] * 1) + (['Y'] * 2) + (['V'] * 3))
    elif (aa == 'S'):
        aaList = ((['A'] * 5) + (['R'] * 3) + (['N'] * 5) + (['D'] * 4) + (['C'] * 3) + (['Q'] * 4) + (['E'] * 4) + (
                    ['G'] * 4) + (['H'] * 3) + (['I'] * 2) + (['L'] * 2) + (['K'] * 4) + (['M'] * 3) + (['F'] * 2) + (
                              ['P'] * 3) + (['S'] * 0) + (['T'] * 5) + (['W'] * 1) + (['Y'] * 2) + (['V'] * 2))
    elif (aa == 'T'):
        aaList = ((['A'] * 3) + (['R'] * 2) + (['N'] * 3) + (['D'] * 2) + (['C'] * 2) + (['Q'] * 2) + (['E'] * 2) + (
                    ['G'] * 1) + (['H'] * 1) + (['I'] * 2) + (['L'] * 2) + (['K'] * 2) + (['M'] * 1) + (['F'] * 2) + (
                              ['P'] * 2) + (['S'] * 4) + (['T'] * 0) + (['W'] * 1) + (['Y'] * 1) + (['V'] * 3))
    elif (aa == 'W'):
        aaList = ((['A'] * 2) + (['R'] * 2) + (['N'] * 2) + (['D'] * 1) + (['C'] * 2) + (['Q'] * 3) + (['E'] * 2) + (
                    ['G'] * 1) + (['H'] * 6) + (['I'] * 3) + (['L'] * 3) + (['K'] * 2) + (['M'] * 3) + (['F'] * 7) + (
                              ['P'] * 1) + (['S'] * 2) + (['T'] * 2) + (['W'] * 6) + (['Y'] * 0) + (['V'] * 3))
    elif (aa == 'Y'):
        aaList = ((['A'] * 2) + (['R'] * 2) + (['N'] * 2) + (['D'] * 1) + (['C'] * 2) + (['Q'] * 3) + (['E'] * 2) + (
                    ['G'] * 1) + (['H'] * 6) + (['I'] * 3) + (['L'] * 3) + (['K'] * 2) + (['M'] * 3) + (['F'] * 7) + (
                              ['P'] * 1) + (['S'] * 2) + (['T'] * 2) + (['W'] * 6) + (['Y'] * 0) + (['V'] * 3))
    elif (aa == 'V'):
        aaList = ((['A'] * 4) + (['R'] * 1) + (['N'] * 1) + (['D'] * 1) + (['C'] * 3) + (['Q'] * 2) + (['E'] * 2) + (
                    ['G'] * 1) + (['H'] * 1) + (['I'] * 7) + (['L'] * 5) + (['K'] * 2) + (['M'] * 5) + (['F'] * 3) + (
                              ['P'] * 2) + (['S'] * 2) + (['T'] * 4) + (['W'] * 1) + (['Y'] * 3) + (['V'] * 0))
    else:
        aaList = ((['A'] * 1) + (['R'] * 1) + (['N'] * 1) + (['D'] * 1) + (['C'] * 1) + (['Q'] * 1) + (['E'] * 1) + (
                    ['G'] * 1) + (['H'] * 1) + (['I'] * 1) + (['L'] * 1) + (['K'] * 1) + (['M'] * 1) + (['F'] * 1) + (
                              ['P'] * 1) + (['S'] * 1) + (['T'] * 1) + (['W'] * 1) + (['Y'] * 1) + (['V'] * 1))

    NewAA = random.choice(aaList)
    return NewAA


def mutN(base):
    """Takes an base, swaps out for another"""
    # based on rates from http://www.ncbi.nlm.nih.gov/pmc/articles/PMC203328/

    base = base.upper()
    mutTypeNum = random.randint(1, 40)
    if (mutTypeNum < 4):  # indels .1 as freq in snps, 3/4 deletions
        print "DELETED", base
        return ''
    elif (mutTypeNum == 4):  # 1/4 indels are insertion
        baseList = ('A', 'T', 'G', 'C')
        insertedBase = random.choice(baseList)
        bases = base + insertedBase
        print "INSERTION", bases
        return bases
    mutOptions = ('trans', 'trans', 'trans', 'trans', 'transv1', 'transv2')
    mutType = random.choice(mutOptions)
    # print "initialbase:", base, " mutType:", mutType

    if (base == 'A'):
        if (mutType == 'trans'):
            base = 'G'
        elif (mutType == 'transv1'):
            base = 'C'
        elif (mutType == 'transv2'):
            base = 'T'
    elif (base == 'G'):
        if (mutType == 'trans'):
            base = 'A'
        elif (mutType == 'transv1'):
            base = 'C'
        elif (mutType == 'transv2'):
            base = 'T'
    elif (base == 'C'):
        if (mutType == 'trans'):
            base = 'T'
        elif (mutType == 'transv1'):
            base = 'A'
        elif (mutType == 'transv2'):
            base = 'G'
    elif (base == 'T'):
        if (mutType == 'trans'):
            base = 'C'
        elif (mutType == 'transv1'):
            base = 'A'
        elif (mutType == 'transv2'):
            base = 'G'
    elif base == 'N':
        baseOptions = ('A', 'G', 'C', 'T')
        base = random.choice(baseOptions)

    return base


def testRun():
    seq = 'AAVVGGDDAVDRRRRNNNNCCCCAAAAVVVVCCCCEEENNENANNEARCCQQQNARQCNAR'
    div = 10
    typ = 'pep'
    outPerIn = 2
    data = mut(seq, div, typ, outPerIn)
    for item in data:
        print "\n NEW ITEM: \n"
        print item
