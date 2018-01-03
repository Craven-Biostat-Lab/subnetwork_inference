file = open('./gams_intermediates/resultsrna.txt','rU')
lines = file.readlines()
file.close()
val = lines[0].replace('\n','')

outfile = open('./gams_intermediates/rna_score.gms','w')
outfile.write('Equation countRNA    "count relevant noes";\n')
outfile.write('countRNA .. '+str(val)+' =e= sum(interRnaNodes,rw(interRnaNodes)*y(interRnaNodes));\n')

