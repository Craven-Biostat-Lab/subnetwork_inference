"""
Ranks nodes by degree.
Creates list file with labels according to input label file and mode(s) for
choosing hits.

python rank_by_degree.py hiv_nov2014_bg_genes_only_no_hiv.sif hiv_human_master_labels.tab "hit|interface" hit interface > results/hiv_by_degree.list

"""
import sys
import hiv_utils
import graphy

if len(sys.argv) < 4:
	print "Usage: python rank_by_degree.py bg.sif master_labels.tab [modes from: \"hit|interface\" hit interface] > results/hiv_by_degree.list"

bgfn=sys.argv[1]
labelfn=sys.argv[2]
modes=sys.argv[3:]
for m in modes:
	if m not in ["hit", "hit|interface", "interface"]:
		print 'Please choose one or more of: "hit", "hit|interface", "interface"'
		sys.exit(2)
modes=set(modes)

# read BG
bg = graphy.readInteractions(bgfn, cols=[0,2], delim=" ")	

# read labels
labels=hiv_utils.read_master_labels(labelfn)	# label=set(gene)
negatives=labels["unknown"]
hits=set.union(*[ genes for (l,genes) in labels.items() if l in modes])
combo=set.union(hits,negatives)		
		

degree=[ (g, len(bg.get(g,[]))) for g in combo ]
degree.sort(key=lambda x : -1*x[1])

for (g, d) in degree:
	label=0
	if g in hits:
		label=1
	print "%d\t%d\t%s" % (d, label, g)
		
		
