"""
 Make the "hidden_by_sample" file for samples in a directory created by
 "get_sample_scores.py". The output file is used in the GAMS pipeline
 to create sample-specific GAMS set files.
 
 Usage: python make_hidden_by_sample.py sample_directory kept_percentage num_samples
 
 Input directory format:
 Must contain the "sample_$p_$i_hits_hide.tab" files for some
 kept-percentage $p and each sample $i from 0 to (num_samples-1)
 
 For example, a kept_percentage may be 0.75.
 
 Output format (printed to std out)
 sampleID	num_hidden	E1|...|EN
 
 Note that sample -1 has no hidden nodes. This is used for running the full 
 (unsampled) version.
"""

import sys, os, glob

if len(sys.argv) != 4:
	print "Usage: python make_hidden_by_sample.py sample_directory kept_percentage num_samples"
	print "Example: python make_hidden_by_sample.py samples_nov2014 0.75 100"
	print "See header comments for some details on format."
	sys.exit()

dirname=sys.argv[1]
kept=sys.argv[2]
num_samples=int(sys.argv[3])

if not os.path.exists(dirname):
	print "Couldn't find directory %s." % dirname
	sys.exit()

print "# First %d samples from %s" % (num_samples, os.path.abspath(dirname))
print "-1\t0\t"
for i in range(0, num_samples):
	# read the tab file
	ls=glob.glob(os.path.join(dirname, "sample_%s_%d_hits_hide.tab" % (kept, i)))
	
	if len(ls) != 1:
		print >> sys.stderr, "Didn't find unique sample %d for percentage %s in directory %s. Aborting." % (i, kept, dirname)
		print >> sys.stderr, "glob results:", ls
	
	# must be first and only entry
	fn=ls[0]
	
	aside=[]
	with open(fn) as f:
		for line in f:
			aside.append(line.strip())
	print "%d\t%d\t%s" % (i, len(aside), "|".join(aside))

