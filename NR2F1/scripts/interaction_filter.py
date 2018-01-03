#file = open('/ua/kiblawi/Documents/gould_inference/search_tester/sid_data/test_tf2.tab','rU')
import os
import sys


def main():
    file = open(sys.argv[1])
    lines = file.readlines()
    file.close()

    outfile = open(sys.argv[1],'w')
    outfile.write(lines[0])
    removeset = ['7314','7316','2099','1994']

    for l in range(1,len(lines)):
        splitline = lines[l].split()
        if splitline[1] in removeset or splitline[2] in removeset:
            #print(splitline[1])
            continue
        else:
            outfile.write(lines[l])

    outfile.close()


if __name__ == "__main__":
    main()
