import sys
import os



def main():
    rnaSet = set()
    literome_file = sys.argv[1]
    geneDict = {}
    gene_file = sys.argv[2]
    #tfSet =set()
    #tf_file = sys.argv[3]
    rna_file = sys.argv[3]
    
    #build gene dict
    file = open(gene_file,'rU')
    lines = file.readlines()
    file.close()
    for l in lines:
        geneDict[l.split()[0]]=l.split()[1].replace('E','')

    #file = open(tf_file,'rU')
    #lines = file.readlines()
    #file.close()
    #for l in lines:
    #    rnaSet.add(l.split()[0])

    #build expression list
    file = open(rna_file,'rU')
    lines  = file.readlines()
    file.close()
    for l in lines:
        rnaSet.add(l.split()[1].replace('E',''))
    
    #import and read white TF filei
    edgeSet = set()
    file = open(literome_file,'rU')
    lines = file.readlines()
    file.close()
    for l in range(1,len(lines)):
        splitline = lines[l].split()
        if len(splitline) < 2:
            print(splitline)
            continue
        if splitline[1] in geneDict and splitline[2] in geneDict: 
            source = geneDict[splitline[2]]
            target = geneDict[splitline[1]]
        else:
            continue
        if source not in rnaSet or target not in rnaSet:
            continue
        edge = (source,target)
        edgeSet.add(edge)


        outfile = open('./input_data/test_literome.tab','w')
    outfile.write('regulation=Discrete(rna_bind|dna_bind)\n')
    for edge in edgeSet:
        outfile.write('dna_bind\t'+str(edge[0])+'\t'+str(edge[1])+'\t1\t0\n')

    outfile.close()

if __name__ == "__main__":
    main()    
    
