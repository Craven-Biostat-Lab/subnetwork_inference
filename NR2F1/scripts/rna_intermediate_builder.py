import sys

def main():
    file = open('./input_data/targetntype2.tab','rU')
    lines = file.readlines()
    file.close()

    sTarget = set()
    for l in range(1,len(lines)):
	    sTarget.add(lines[l].split()[0])

    file = open('./output_data/pathout.txt','rU')
    lines = file.readlines()
    file.close()

    allNodes = set()
    for l in range(1,len(lines)):
    	    path=lines[l].split()[1]
	    nodes = path.split('|')
	    for n in nodes:
		allNodes.add(n)

    remainder = allNodes-sTarget

    file = open(sys.argv[1])
    lines = file.readlines()
    file.close()

    rnaDict = {}
    rnaSet = set()
    for l in range(0,len(lines)):
	    x = lines[l].split('\t')
	    entrez = x[1].replace('E','')
            #print(entrez)
	    score = x[2]
	    rnaDict[entrez]=score
	    rnaSet.add(entrez)

    outfile = open('./gams_intermediates/rnaintermediates.gms','w')

    outfile.write('Set interRnaNodes(node)\t"RNA intermediates"\n')
    outfile.write('\t'+'/'+'\t')
    for i in rnaSet.intersection(remainder):
	outfile.write(i + '\n')
    outfile.write('/;\n')
    outfile.write('PARAMETERS\trw(node)\n')
    outfile.write('\t'+'/'+'\t')

    for i in rnaSet.intersection(remainder):
	outfile.write(i +'\t' + rnaDict[i]+'\n')
    outfile.write('/;\n')
    outfile.close()


if __name__ == "__main__":
        main()


