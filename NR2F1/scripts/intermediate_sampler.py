import random
import sys
import os

#generates random samples of intermediates
#usage python intermediate_sampler.py datasets seed
def main():
    dataset_dir = sys.argv[1]
    rseed = int(sys.argv[2])
    
    random.seed(rseed)

    outfile = open('input_data/sample_' + str(rseed) + '_intermediate.tab','w')
    file = open(dataset_dir+'/intermediates_master.tab','rU')
    lines = file.readlines()
    file.close()

    rand_smpl = [ lines[i] for i in random.sample(xrange(len(lines)),int(0.75 * len(lines)))]
    rand_smpl = lines

    for r in rand_smpl:
        outfile.write(r)

    file = open(dataset_dir + '/DE_rna_seq.tab','rU')
    lines = file.readlines()
    for l in lines:
        outfile.write(l)
    outfile.close()







if __name__=="__main__":
    main()

