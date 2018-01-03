"""
Takes random samples from a hit set and calculates DK scores
for the entire graph. Considers only hits that appear in the BG.

python get_sample_scores.py [k] hitfile graphfile num_samples keep_frac outdir

optional first argument "k" means to load kernel from file with graph's filename,
but suffix .npy.

to run for multiple fractions, just list them:
0.9 0.1 0.3 ..etc

Parameters:
- hit file (NAME\tHDF/HRF)
- graph file (in SIF format: A u B)
- Number of samples
- Percentage to keep in each sample
- directory to print files
- Optional: instruction to read saved kernel - will read from file with graphfile's filename and suffix .npy
If this isn't chosen, will save the kernel.

Samples uniformly from the hit set.
Uses a seeded random number generator for reproducibility.

"""
import sys, datetime, random, os
import numpy as np
import graphy, kernel

# Will ensure that same hits are drawn for each sample
# each time that we run this 
SEED=datetime.datetime(2014, 4, 14, 14, 45, 37, 38770)
LAMBDA=1.0

def main(argv):

	loadkern=False
	if argv[1]=="k":
		loadkern=True
		argv=[argv[0]] + argv[2:]
		#print argv

	hitfn = [argv[1]]		
	graphfn = argv[2]	# graph interaction file 

	# kernel filename for reading or writing
	kernfn = "".join(graphfn.split(".")[:-1])
	kernfn = "%s_kernel.npy" % kernfn

	if loadkern:
		# look for kernel in same directory with same filename as graph
		# but extension .npy
		if os.path.isfile(kernfn):
			loadkern=True
			print "Will read pre-made kernel from %s" % kernfn
		else:
			print "Cannot find requested kernel file %s" % kernfn
			return 2
		
	else:
		print "Will write kernel to %s" % kernfn

	num_samples = int(argv[3])	# number of samples

	# one or more fractions
	fracs=[ float(x) for x in argv[4:-1] ]
	#keep_frac = float(argv[4])	# fraction of hits to keep in each sample
	outdir = argv[-1]
	
	hit_labels = graphy.readHits(hitfn) # map: hit : label
	print "Read %d hits." % len(hit_labels)

	if not os.path.exists(outdir) and not os.path.isdir(outdir):
		print "Creating output directory %s." % outdir
		os.mkdir(outdir)
	
	# read in network and convert to index	
	adj_map_names = graphy.readInteractions(graphfn, cols=[0,2], delim=" ")	# adjacency map, using names	
	(ordered_names, name_map, adj_map) = graphy.convertToIndexedMap(adj_map_names)	

	print "Read graph"
	
	# trim hit_labels down to hits in BG.
	hit_labels = dict([ (h,l) for (h,l) in hit_labels.items() if h in name_map])
	# save sorted order of hits to allow deterministic sampling
	ord_hits = sorted(hit_labels.keys())


	# ordered indices of hits
	hit_ids = [name_map[h] for h in hit_labels ]

	print "%d hits in graph" % (len(hit_labels))

	# build kernel if necessary, or read existing
	K=None
	if not loadkern:
		A = kernel.makeSparseMatrix(adj_map)
		K = kernel.makeKernel(A, LAMBDA)	
		# save
		np.save(kernfn, K)
		print "Made new kernel and saved", K.shape
	else:
		K =	np.load(kernfn)
		print "Read saved kernel", K.shape	
	
	# get scores for full hit set
	q = kernel.makeQ(hit_labels, ordered_names)
	nonzeroQ = [ i for i in range(len(q)) if q[i] > 0]	
	scores = kernel.calculateScores(q, K)
	# map scores to names
	scores=dict([ (ordered_names[i], val) for (i,val) in scores.items()])
	fullfn = "full_hits_scores.gms"	
	fullfn = os.path.join(outdir, fullfn)
	writeScores([], scores, hit_labels, fullfn)
	print "Printed full score set to %s" % fullfn
	
	# get leave-one-out scores
	loofn = "%s/kernel_leave_one_out.list" % outdir
	(crossval, orig) = kernel.crossValidate(range(0,len(ordered_names)), q, K)
	# map scores to names
	crossval=dict([ (ordered_names[i], val) for (i,val) in crossval.items()])
	
	writeCrossValList(crossval, hit_labels, loofn)	
	print "Printed leave-one-out scores to %s" % loofn
	

	# set seed - same seed, so same genes held aside!!
	random.seed(SEED)

	cov=set()

	# for each fraction requested...
	for keep_frac in fracs:
		# for each random sample...
		size = int(keep_frac * len(hit_labels))
		print "Sampling. Keeping %d hits per sample." % size
		for i in range(num_samples):
			fn = "sample_%.2f_%d_hits.gms" % (keep_frac, i)

			# sample hits to keep - from SORTED HITS for determinism
			sampled = random.sample(ord_hits, size)

			print "sampled %d from %d" % (len(sampled), len(ord_hits))
			cov=set.union(cov, set(sampled))

			hidden = set.difference(set(hit_labels), set(sampled))
			remaining=set.difference(set(hit_labels), hidden)
			#print fn, len(hidden), len(remaining)
			
			# write out tab file of hidden hits
			tabfn = os.path.join(outdir, "sample_%.2f_%d_hits_hide.tab" % (keep_frac, i))
			writeHeldAside(hidden, tabfn)	
						
			q = kernel.makeQ(sampled, ordered_names)
			nonzeroQ = [ i for i in range(len(q)) if q[i] > 0]

			#scores={}
			scores = kernel.calculateScores(q, K)

			# map scores to names
			scores=dict([ (ordered_names[i], val) for (i,val) in scores.items()])	
			outfn = os.path.join(outdir, fn)

			nonzeroHidden = [ h for h in hidden if scores[h] > 0]		
			
			print "Total hits %d, kept %d (%.2f), hidden %d, nonzero entries in q %d, nonzero scores for hidden hits %d" % (len(hit_labels), len(sampled), keep_frac, len(hidden), len(nonzeroQ), len(nonzeroHidden))

			writeScores(hidden, scores, remaining, outfn)

			print "\twrote files %s, %s" % (outfn, tabfn) 

	print "total hits covered: %d out of %d" % (len(cov), len(ord_hits))
	return 0

def writeHeldAside(hidden, outfn):
	"""
	Writes list of held-aside genes to tab file
	"""
	hidden=sorted(list(hidden))
	with open(outfn, "w") as f:
		for h in hidden:
			f.write("%s\n" % h)
	return

def writeScores(hidden, scores, remaining, outfn):
	"""
	Write hidden hits and scores to a gams file. 
	Only write scores > 0.
	"""
	
	with open(outfn, "w") as f:
		# write hidden hits!
		if len(hidden)>0:
			f.write('Set hide(node)\t"hits to hide (%d)" \n/ %s /;\n' % (len(hidden), ", ".join(hidden)))
		else:
			f.write('Set hide(node)\t"hits to hide (0)" \n/ null /;\n')

		# write scores
		f.write("Parameter score(node)\t\"Node scores from DK, hits sampled\"\n")
		f.write("/ ")
		for (n,l) in scores.items():	
			# don't bother writing scores for hits? nah, keep them; might be interesting
			if l > 0:		
				f.write("%s\t%f\n" % (n,l))
				#if n in hidden:
				#	print "score for hidden hit", n,l
		f.write("/;\n")
		
		
def writeCrossValList(scores, hit_labels, outfn):
	"""
	Writes confidence values from of leave-one-out cross-validation to list file.
	Scores: { node : score }
	"""
	# first, get scores and sort in decreasing order
	srtscores=sorted(scores.items(), key=lambda x:-1*x[1])
	with open(outfn, "w") as f:
		f.write("# Leave-one-out cross-validation results\n")
		for (node, val) in srtscores:
			label=0
			if node in hit_labels:
				label=1
			f.write("%f\t%d\t%s\n" % (val, label, node))
	
if __name__=="__main__":
	sys.exit(main(sys.argv))

