#build path dictionary from pathout.txt

'''
file = open('./output_data/pathout.txt','rU')
lines = file.readlines()
file.close()

pathDict = {}
for l in range(1,len(lines)):
    x = lines[l].split()
    pathID = x[0]
    path = x[1]
    pathNodes = x[1].split('|')
    pathTarget = pathNodes[len(pathNodes)-1]
    pathDict[pathID]=pathTarget
'''

file = open('./gams_intermediates/results.txt','rU')
lines = file.readlines()
file.close()

targetSet = set()
for l in lines:
    #pathID = l.split()[0].replace('"','')
    #targetSet.add(pathDict[pathID])
    targetSet.add(l.split()[0].replace('"',''))

outfile = open('./gams_intermediates/truetargets.gms','w')

outfile.write('Set trueTargets(node)\t"targets"\n')
outfile.write('/'+'\t')
for t in targetSet:
    outfile.write(t+'\n')
outfile.write('/;\n')
outfile.close()
print(len(targetSet))

file = open('./input_data/targetntype2.tab','w')
file.write('#node\tntype=discrete(source|target)\n')
file.write('7025\tsource\n')
for t in targetSet:
    file.write(t+'\ttarget\n')
file.close()

