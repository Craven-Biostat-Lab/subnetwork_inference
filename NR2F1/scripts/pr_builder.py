import sys
import os 
import operator

def main():
    file = open(sys.argv[1],'rU')
    lines = file.readlines()
    file.close()

    resDict = {}
    place = int(sys.argv[2])

    outfile = open(sys.argv[3],'w')
    for i in range(0,len(lines)):
        x = lines[i].split()
        outfile.write(str(i) + '\t'+x[place] + '\n')


    #sorted_x = sorted(resDict.items(),key = operator.itemgetter(0))
    
    #for s in sorted_x:
    #    outfile.write(s[0] + '\t' +s[1] + '\n')

    outfile.close()
if __name__ == "__main__":
    main()

