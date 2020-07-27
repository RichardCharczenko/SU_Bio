from mut import mut
from genFastaFile import generate_fasta


def fasta_format(data, name):
    fasta_form = [name]
    newLine = ""
    count = 0
    for val in data:
        newLine += str(val)
        if count >= 70:
            fasta_form.append(newLine)
            newLine = ""
            count = 0
        count += 1
    if count < 70:
        fasta_form.append(newLine)
    return fasta_form


def main_fase(sequence, divergence, sequenceType, outPerIns):
    """ Driver duntion for fase, collects 4 inputs and passes them into mut function within fase.py
    then uses formating function to prep for them the website."""
    data = mut(sequence.replace(" ", ""), int(divergence), sequenceType, int(outPerIns))
    count = 0
    forms = []
    forms.append(fasta_format(sequence.lower().replace(" ", ""), "Original Sequence"))
    for key in data[1]:
        name = "Sequence: " + str(key)[:3] + str(count)
        forms.append(fasta_format(str(key), name))
        count += 1
    return forms
