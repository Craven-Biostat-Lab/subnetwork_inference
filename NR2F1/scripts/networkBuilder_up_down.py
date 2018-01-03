#make cytoscape network file from gams output
import sys
def main():

    pathfile = open('./output_data/pathout.txt','rU')
    pathlines = pathfile.readlines()
    pathfile.close()
    resultsfile = open('./final_output/final_results.txt','rU')
    resultslines = resultsfile.readlines()
    resultsfile.close()
    pathresults = []
    for r in resultslines:
        line = r.replace('"', '')
        line = line.replace('\n','')
        pathresults.append(line)

    print('PathResults\t' + str(len(pathresults))+'\n')
    edges = []
    nodes = []
    for p in pathlines:
        x = p.split()
        if x[0] in pathresults:
            edgelist = x[2].split('|')
            for e in edgelist:
                edges.append(e)
            nodelist = x[1].split('|')
            for n in nodelist:
                nodes.append(n)

    edgeset = set(edges)
    edges = list(edgeset)
    nodeset = set(nodes)
    nodes = list(nodeset)
    print('nodes\t' + str(len(nodes))+'\n')

    sourcenode = ['7025']
    targetnodes = []
    #get target nodes
    tnodesfile = open('./input_data/targetntype2.tab','rU')
    targetlines = tnodesfile.readlines()
    tnodesfile.close()
    for t in range(2,len(targetlines)):
        targetnodes.append(targetlines[t].split()[0])


    targetnodes = list(set(targetnodes).intersection(nodeset))
    print('targetnodes\t' +str(len(targetnodes)))

    intermediatenodes = list(nodeset.difference(set(targetnodes)))
    print('intermediate nodes\t' + str(len(intermediatenodes)))


    tffile = open('./input_data/ntype.tab','rU')
    tflines = tffile.readlines()
    tfactors = []
    tffile.close()
    for i in range(1,len(tflines)):
        tfactors.append(tflines[i].split()[0])



    #convert entrez to genesymbol
    tfactors2 = ['10664','6934','7764']



    humangenomefile = sys.argv[1]

    humanfile = open(humangenomefile,'r')
    humanGenes = humanfile.readlines()
    humanfile.close()

    geneDict = {}
    for h in humanGenes:
        asplit = h.split()
        geneDict[asplit[1].replace('E','')]= asplit[0]
        
    
    #print(geneDict)
    outfile = open('./final_output/network.txt','w')
    edgefile = open('./output_data/search_test_gamsId.edge','rU')

    edgelines = edgefile.readlines()
    edgefile.close()

    
    literomefile = open('./input_data/test_literome.tab','rU')
    literomelines = literomefile.readlines()
    literomefile.close()
    literomeSet = set()

    for l in range(1,len(literomelines)):
        line = literomelines[l]
        source = line.split()[1]
        target = line.split()[2]
        literomeSet.add((source,target))

    #literomeSet =set()
    outfile.write('source\tinteraction\ttarget\tedgename\n')
    for i in range(1,len(edgelines)):
        line = edgelines[i].split()
        x = line[3]
        source = line[0]
        inter = line[1]
        target = line[2]
        if x in edges:
            if inter == '(d)' and (source,target) in literomeSet:
                inter='literome'
            outfile.write(geneDict[source]+'\t'+inter+'\t'+geneDict[target]+'\t'+x+'\n')
        

    outfile.close()



    file = open(sys.argv[2],'rU')
    lines = file.readlines()
    file.close()
    regDict = {}
    for l in lines:
        x = l.split()
        regDict[x[1].replace('E','')]=x[2]


    outfile = open('./final_output/nodenet.txt','w')
    outfile2 = open('./final_output/final_intermediates.txt','w')
    outfile.write('node\ttype\n')
    for n in nodes:
        if n in sourcenode:
            outfile.write(geneDict[n]+'\t' + 'Source\n')
        elif n in targetnodes:
            if n in regDict:
                outfile.write(geneDict[n]+'\t'+regDict[n]+'\n')
            else:
                outfile.write(geneDict[n]+'\ttarget\n')
        else:
            if n in tfactors:
                if n in tfactors2:
                    outfile.write(geneDict[n]+'\t'+'TF2\n')
                    outfile2.write(geneDict[n]+n+'\tTF2\n')
                else:
                    outfile.write(geneDict[n]+'\t'+'TF\n')
                    outfile2.write(geneDict[n] + '\t' + n + '\tTF\n')
            else:
                outfile.write(geneDict[n] + '\t' + 'Intermediate\n')
                outfile2.write(geneDict[n] + '\t' + n + '\t' 'Intermediate\n')

    outfile.close()


if __name__ == "__main__":
    main()






