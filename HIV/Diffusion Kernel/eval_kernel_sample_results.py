"""
 Evaluates an ensemble of kernel scores.
 For each hit/interface (depending on mode), calculates average kernel score when hit held aside.
 For each non-hit/non-interface, calculates average kernel score in all solutions.

Make sure you run this on the version of scores that includes non-path nodes!

Usage:
eval_kernel_sample_results.py score_dir hit_sample_matchfile.tab labels.tab modes
where score_dir contains the gams files for the kernel scores per sample
and where modes are a substring of: hit "hit|interface" interface
(you need to choose all three to get the union of hits and interfaces!)


"""
import sys
import os
import glob
from hiv_utils import *

def main(argv):
	scoredir=argv[1]
	hitmapfn=argv[2]

	# node labels: hit, hit|interface, hiv, unknown
	labelfn=argv[3]
	
	# finally - which genes are we considering hits? hit, hit|interface, interface
	modes=argv[4:]
	for m in modes:
		if m not in ["hit", "hit|interface", "interface"]:
			print 'Please choose one or more of: "hit", "hit|interface", "interface"'
			return 2
	
	
	(hitmap, allhits)=read_hitmap(hitmapfn)
	print "# read %d hits for %d samples from %s" % (len(allhits), len(hitmap), hitmapfn)
	
	
	labels=read_labels(labelfn)
	print "# read %d labelled nodes from %s" % (len(labels), labelfn)
	hits=[ n for (n,l) in labels.items() if "hit" in l]
	

	# discrepancy?
	missing=set.difference(set(hits), allhits)
	if len(missing) > 0:
		print >> sys.stderr, "# %d hits are in labels but not map - verify that this is OK" % (len(missing))
		print >> sys.stderr, missing
		sys.exit()

	#print "%d hits are in labels but not map" % (len(missing))

	ints=[ n for (n,l) in labels.items() if "interface" in l]
	onlyhits=[ n for (n,l) in labels.items() if "hit" in l and "interface" not in l]
	other=set([ n for (n,l) in labels.items() if "unknown" in l])

	hitset = [n for (n,l) in labels.items() if l in modes]

	print "# kernel BG contains %d hits, %d interfaces, and %d hits that are not interfaces" % (len(hits), len(ints), len(onlyhits))
	print "# hitmap contains %d hits that are not interfaces" % len(set.difference(allhits, ints))
	print "# Considering %d hits for PR curve (from sets [%s])" % (len(hitset), ", ".join(modes))
	
	# remove interfaces from the held-aside hit sets if requested
	if len(modes)==1 and modes[0]=="hit":
		temp={}
		tot=set()
		for (sid, gs) in hitmap.items():
			temp[sid]=set.difference(gs,ints)
			tot=set.union(temp[sid], tot)
		hitmap=temp 
		print "# %d hits ever held aside" % len(tot)
		#return
	else:
		tot=set()
		for (sid, gs) in hitmap.items():
			tot=set.union(gs, tot)
		print "# %d nodes held aside" % len(tot)

	# for each non-interface hit and non-interface other node,
	# store count of "in" solutions (inferred, success) and "out" solutions (not inferred, fail)

	tallies={}	# key: EID, val: [] list of scores

	# print results for these genes only
	for h in hitset:
		tallies[h]=[]
	for o in other:
		tallies[o]=[]

	# go through sols
	ls = glob.glob(os.path.join(scoredir, "*.gms"))
	if len(ls)==0:
		print "No gms files found in %s" % scoredir
		return

	done=0
	for f in ls:
		# result_dumped/sample_0.25_101_hits_result_dump
		#print sid
		sid = int(os.path.split(f)[1].split("_")[2])
		#print sid

		#print sid
		scores = get_scores(f)
		#print scores
	
		# append scores for hits held aside
		asides=hitmap.get(sid)
		#print sid, len(asides)
		

		for a in asides:
			tallies[a].append(scores.get(a,0.0))

		# for non-interface, non-hits, also add in scores		
		for a in other:
			tallies[a].append(scores.get(a,0.0))
		done+=1
		if done % 50 == 0:
			print >> sys.stderr, "%s\t%d complete" % (argv[1], done)
	
	vals=[]	# so we can sort the results
	for (t, scores) in tallies.items():
		status=0
		if t in hitset:
			status=1	
		tot=sum(scores)
		avg=0
		if len(scores)>0:
			avg=tot/float(len(scores))
		
		# average\tstatus\teid\tnum_sols_considered
		vals.append([avg, status, t, len(scores)])
	above_zero=[ v[2] for v in vals if v[1]==1 and v[0]>0 ]
	print "# %d targets with score over 0" % len(above_zero)
	
	# higher on top
	vals.sort(key=lambda x : -1*x[0])
	print "# conf\tstatus\tgene\tnum_sols"
	for (avg,status,t, ct) in vals:
		print "%f\t%d\t%s\t%d" % (avg, status, t, ct)

def get_scores(fn):
	""" Gets scores from a gams score file."""
	scores={}
	on=False
	with open(fn) as f:
		for line in f:
			if "*" == line[0]:
				continue
			# start with "Parameter score(n)"
			if "Param" in line:
				#print "on"
				on=True
				continue
			# skip until we get to scores
			if not on:
				continue			

			# first line may have "/" in it
			line=line.replace("/","")
			line=line.replace(";","")
			
			sp=line.strip().split("\t")
			# last line may not have any info
			if len(sp)<2:
				continue
			n=sp[0]
			s=float(sp[1])
			scores[n]=s
	return scores


if __name__=="__main__":
	sys.exit(main(sys.argv))



