def write_to_file(item):
    newFile = open("new_test_file.txt", 'w')
    newFile.write(item)

def write_to_html_paragraph(item):
    html = "<p>"
    for char in item:
        html += char
    html += "</p>"
    return html

def generate_fasta(name, sequence):
    fastaTitle = str(name)
    fasta = ""
    newLine = ""
    count = 0
    for seq in sequence:
        count += 1
        newLine += seq
        if count >= 30:
            count = 0
            fasta = fasta + newLine
            #newFile.write(newLine)
            newLine = ""
    if count < 30:
        fasta += newLine
    return write_to_html_paragraph(fastaTitle), write_to_html_paragraph(fasta)


