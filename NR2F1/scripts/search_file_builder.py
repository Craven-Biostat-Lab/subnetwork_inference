import sys
import os

#usage: python search_file_builder.py encode_directory/ white_spreadsheet

def main():
    tfDirectory = sys.argv[1]
    white_file = sys.argv[2]
    rna_file = sys.argv[3]
    file = open(rna_file,'rU')
    lines = file.readlines()
    file.close()
    rnaSet = set()
    for l in lines:
        rnaSet.add(l.split()[1].replace('E',''))
    tfDict = {}
    #import and read white TF file
    file = open(white_file,'rU')
    lines = file.readlines()
    file.close()
    for l in range(1,len(lines)):
        x = lines[l].split()
        tf= x[1]
        tfTarget = x[2]
        if tf not in rnaSet:
            continue
        if tf not in tfDict:
            tfDict[tf] = set()
        if tfTarget in rnaSet:
            tfDict[tf].add(tfTarget)

    #import and read encode files
    for file in os.listdir(tfDirectory):
        if file.startswith("."):
            continue;
        if file.endswith(".csv"):
            print(tfDirectory+file)
            encodeFile = open(tfDirectory + file,'rU')
            lines = encodeFile.readlines()
            encodeFile.close()
            tf = lines[0].split(',')[0]
            if tf not in rnaSet:
                continue
            if tf not in tfDict:
                tfDict[tf]=set()
            for l in range(2,len(lines)):
                x = lines[l].split(',')
                if x[0] in rnaSet:
                    tfDict[tf].add(x[0])

    ntypefile = open('./input_data/ntype.tab','w')
    ntypefile.write('#node\tntype=discrete(tf|rbp)\n')
    tf2file = open('./input_data/test_tf2.tab','w')
    tf2file.write('regulation=Discrete(rna_bind|dna_bind)\n')
    for tf in tfDict:
        ntypefile.write(tf + '\t' + 'tf\n')
        for target in tfDict[tf]:
            tf2file.write('dna_bind\t'+tf+'\t'+target+'\t'+'1\t0\n')
    ntypefile.close()
    tf2file.close()

if __name__ == "__main__":
    main()    
    
