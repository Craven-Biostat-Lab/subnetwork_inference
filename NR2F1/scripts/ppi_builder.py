import sys
import os

#usage: python search_file_builder.py  ppi_file rna_intermediates

def main():
    ppi_file = sys.argv[1]
    rna_file = sys.argv[2]
    file = open(rna_file,'rU')
    lines = file.readlines()
    file.close()
    rnaSet = set()
    for l in lines:
        rnaSet.add(l.split()[1].replace('E',''))

    file = open(ppi_file,'rU')
    lines = file.readlines()
    file.close()
    outfile = open('./input_data/ppi.tab','w')
    outfile.write(lines[0])
    for l in range(1,len(lines)):
        line = lines[l]
        splitline = line.split()
        if splitline[1] in rnaSet and splitline[2] in rnaSet:
            outfile.write(line)


    outfile.close()


if __name__ == "__main__":
    main()    
    
