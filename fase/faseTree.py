from Tree import GenerateTree

def main_tree(seq, seqType, maxChild, divergence):
    gen = 4
    tree = GenerateTree(seq, seqType, gen, divergence, maxChild)
    tree_repr = tree.phyloTree.string_rep
    sequence_repr = format_sequences(tree.phyloTree)
    tree_repr = tree_repr.replace('\t', '     ')
    return tree_repr, sequence_repr

def format_sequences(tree):
    name = ">Sequence"+tree.bib+': '
    rep = create_sequence_list(tree.seq, name)
    for node in tree.Nodes:
        rep += format_sequences(node)
    return rep

def create_sequence_list(seq, name):
    lines = [name]
    count = 0
    line = ''
    for item in seq:
        line += item
        if count == 80:
            lines.append(line)
            line = ''
            count = 0
        count += 1
    lines.append(line)
    return lines
