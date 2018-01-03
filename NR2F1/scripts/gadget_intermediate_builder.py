import sys
import os

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

    file = open(sys.argv[1],'rU')
    lines = file.readlines()
    file.close()

    gadgetDict = {}
    gadgetSet = set()
    for l in range(1,len(lines)):
	x = lines[l].split('\t')
	entrez = x[4]
        print(entrez)
	score = x[7]
	gadgetDict[entrez]=score
	gadgetSet.add(entrez)

    outfile = open('./gams_intermediates/intermediates.gms','w')

    outfile.write('Set interNodes(node)\t"intermediates"\n')
    outfile.write('\t'+'/'+'\t')
    for i in gadgetSet.intersection(remainder):
	outfile.write(i + '\n')
    outfile.write('/;\n')
    outfile.write('PARAMETERS\tw(node)\n')
    outfile.write('\t'+'/'+'\t')

    for i in gadgetSet.intersection(remainder):
	outfile.write(i +'\t' + gadgetDict[i]+'\n')
    outfile.write('/;\n')
    outfile.close()


if __name__ == "__main__":
    main()



