"""
Makes a master node label file to cover all genes in background network.

Usage:
python make_master_label_list.py hits_plus_ints.tab human_gene_net.sif > hiv_human_labels.tab

Input: list of hits and interfaces
Input: sif file of human genes in background network (no HIV, no complexes)

Output: tab-delim file:
gene	hit
gene	unknown
gene	hit|interface
...
"""

import sys

# read hit/interface labels
hits=set()
ints=set()
with open(sys.argv[1]) as f:
	for line in f:
		sp=line.strip().split("\t")
		if "interface" in sp[1].lower():
			ints.add(sp[0])
		elif sp[1].lower() in ["both","hdf","hrf","gadget"]:
			hits.add(sp[0])

allnodes=set()
# read sif
with open(sys.argv[2]) as f:
	for line in f:
		sp=line.strip().split()
		allnodes.add(sp[0])
		allnodes.add(sp[2])
		# sp[1] is the interaction type.
		
allnodes=sorted(list(allnodes))
for a in allnodes:
	if a not in hits and a not in ints:
		print "%s\tunknown" % a
	elif a in hits and a not in ints:
		print "%s\thit" % a
	elif a in ints and a not in hits:
		print "%s\tinterface" % a
	elif a in ints and a in hits:
		print "%s\thit|interface" % a

