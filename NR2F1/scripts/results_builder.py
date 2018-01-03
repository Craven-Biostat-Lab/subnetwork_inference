import sys
import os
import operator


#usage python results_builder.py results_folder basal_cell_file genename_to_entrez ppi_file literome_basal_file output

def main():

    resultDict = {}
    possibleDict = {}

    #get number of times each gene appears in file
    directory = sys.argv[1]
    for file in os.listdir(directory):
        if file.endswith('.tab'):
            posfile = open(directory+file,'rU')
            lines = posfile.readlines()
            posfile.close()
            for l in lines:
                splitline=l.split()
                gene = splitline[0]
                if gene not in possibleDict:
                    possibleDict[gene]=0
                possibleDict[gene] = possibleDict[gene]+1

        elif file.endswith('.txt'):
            resultsfile = open(directory+file,'rU')
            lines = resultsfile.readlines()
            resultsfile.close()
            for l in lines:
                splitline=l.split()
                gene =splitline[0]
                if gene not in resultDict:
                    resultDict[gene]=0
                resultDict[gene]=resultDict[gene]+1

    # get intermediate files
    relevant = set()
    file = open(sys.argv[2],'rU')
    lines = file.readlines()
    file.close()
    for l in lines:
        relevant.add(l.replace('\n',''))

    entrezrelevant = set()
    entrezDict = {}
    geneDict = {}
    file = open(sys.argv[3],'rU')
    lines = file.readlines()
    file.close()
    for l in lines:
        splitline = l.split()
        if splitline[0] in relevant:
            entrezrelevant.add(splitline[1].replace('E',''))
        geneDict[splitline[0]]=splitline[1].replace('E','')
        entrezDict[splitline[1].replace('E','')] = splitline[0]



    #calculate confidence values
    conf = {}
    for g in resultDict:
        val = float(resultDict[g])/float(possibleDict[g])
        conf[g] = val

    sorted_conf = sorted(conf.items(),key=operator.itemgetter(1),reverse=True)

    
   
    #calculate hop edges ppi
    basalHop = {}
    file = open(sys.argv[4],'rU')
    lines = file.readlines()
    file.close()
    
    for l in lines:
        x = l.split()
        if len(x)<=2:
            continue

        if x[1] in entrezDict and x[2] in entrezDict:
            source = entrezDict[x[1]]
            target = entrezDict[x[2]]
        else:
            continue
        if source in relevant:
            if target not in basalHop:
                basalHop[target] = set()
            basalHop[target].add(source)
        if target in relevant:
            if source not in basalHop:
                basalHop[source]=set()
            basalHop[source].add(target)

    #calculate hop edges literome_basal genes
    file = open(sys.argv[5],'rU')
    lines = file.readlines()
    file.close()

    for l in lines:
        x = l.split()
        if x[2] in relevant:
            if x[1] not in basalHop:
                basalHop[x[1]] = set()
            basalHop[x[1]].add(x[2])
        if x[1] in relevant:
            if x[2] not in basalHop:
                basalHop[x[2]]=set()
            basalHop[x[2]].add(x[1])



    #generate result.list file
    outfile = open(sys.argv[6],'w')
    hopval=0
    count = 0
    totalset = set()
    for s in sorted_conf:
        if s[0] in relevant:
            relval = '1'
        else:
            relval = '0'
        if s[0] in basalHop:
            totalset = totalset.union(basalHop[s[0]])
            count = len(totalset)
            hopval = hopval+1
            icount = len(basalHop[s[0]])
        else:
            count = len(totalset)
            hopval = hopval+0
            icount = 0
        outfile.write(str(s[1]) + '\t' + str(relval) +'\t' + s[0] +'\t' + str(resultDict[s[0]])+'\t' + str(possibleDict[s[0]]-resultDict[s[0]]) + '\t' + str(count) + '\t' + str(hopval) + '\t' + str(icount)+ '\n')

    '''
    for g in possibleDict:
        if g not in resultDict:
            if g in relevant:
                relval = '1'
            else:
                relval = '0'
            outfile.write('0.000000' + '\t' + str(relval) +'\t' + g +'\t' + '0'+'\t' + str(possibleDict[g]) + '\n')
    '''
if __name__ == "__main__":
    main()
