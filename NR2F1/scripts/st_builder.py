
import sys

def main():
    file = open('./input_data/ntype2.tab','rU')
    lines = file.readlines()
    file.close()

    file = open('./input_data/test_stpairs.tab','w')
    file.write('#source\ttarget\ttype\n')
    for l in range(2,len(lines)):
        x = lines[l].split()
        file.write('7025\t' + x[0] +'\tamplified\n')

    file.close()

if __name__ == "__main__":
    main()
    
