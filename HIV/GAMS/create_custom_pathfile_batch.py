"""
Given a solution ID, produce the necessary path sets
for running GAMS inference.

Runs in batch mode. Starts with sol_start and ends with sol_end, exclusive.
outfile should be a pattern like "hiv_75_%d_moresets.gms"

Usage:
python create_custom_pathfile.py sol_start sol_end mode hitmap_file.tab master_paths master_subgraph_edges output_file_pattern
 
where mode is one of {hits, ints, both} and tells us which path positions to check for hidden nodes.

output_file_pattern should be of the form "blah_%d", where %d will be replaced with the sample ID.

Creates:
-Path sets
-Subgraph sets
-hidden node set hide(node)
-novelGene node set (including hidden)
-Interface edge set  intEdge (not including hidden)
-Interface node set	 intNode (not including hidden)

Files needed:
- master file mapping solutions IDs to hits held aside
- master path file
- master subgraph-path association file
"""

import sys
from hiv_utils import *
import os

MODEMAP={"hits":[0], "ints":[-2], "both":[0,-2]}


def main(argv):
	if len(argv) != 9 or argv[3] not in MODEMAP.keys() or "%d" not in argv[8]:
		print "Usage: python create_custom_pathfile.py sol_start sol_end mode all_labels hitmap_file.tab master_paths  master_subgraph_edges outfile_pattern_%d \n where mode in {hits,ints,both}"
		print "and in the output file pattern, %d will be replaced with the sample ID."
		print len(argv)
		for i in range(0,len(argv)):	
			print "%d: %s" % (i, argv[i])
		return 2

	# get requested start solution ID
	sol_s=int(argv[1])	
	sol_e=int(argv[2])
	
	# check hiding mode - hits, ints, both
	mode=argv[3]
	hpos=MODEMAP[mode]	# positions to check for nodes in path set


	# read master node labels so we can populate some node sets
	labelfn=argv[4]

	hitmapfn=argv[5]
	pathfn=argv[6]
	subgraphfn=argv[7]

	# output file pattern
	outp=argv[8]
	
	# before we do anything, check:
	if len(range(sol_s, sol_e))==0:
		print "Please end your sample range with a value at least one more than the start."
		print "You provided:", sol_s, sol_e
		return 2
	
	# check existence of output directory
	od=os.path.split(os.path.abspath(outp))
	#print od
	if not os.path.exists(od[0]):
		print "Output directory %s doesn't exist. Make it and try again." % od[0]
		return 2

	# read node labels
	labels=read_master_labels(labelfn)

	# get the held-aside nodes from the solution match file
	# if sol==-1, nothing held aside
	(hitmap, ever_aside) = read_hitmap(hitmapfn)

	# paths: { pathfinder : { pid : { "nodes":[], "edges":[] } } }
	(master_paths, tot) = read_master_pathfile(pathfn, hide=None, def_pf="all")

	# read master subgraphs
	# get subgraph nodes/edges corresponding to those paths
	master_subgraphs = read_master_subgraph_file_by_paths(subgraphfn)
	#for (s, itmap) in subgraphs.items():
	#	print "%s\t%d nodes\t%d edges" % (s, len(itmap["nodes"]), len(itmap["edges"]))
	print "read paths and subgraphs" 
	sys.stdout.flush()

	# for each solution
	for sol in range(sol_s, sol_e):
		outfn = outp % sol
		print "Writing to %s" % outfn
		sys.stdout.flush()
	
		outf = open(outfn, "w")
		
		# get held-aside hits
		aside = hitmap[sol]
		#print len(aside)

		# get only paths without held aside hits/ints
		

		# next, get the paths that DON'T start or end with those
		# paths: { pathfinder : { pid : { "nodes":[], "edges":[] } } }
		paths = dict( [(pf, {}) for pf in master_paths.keys() ])
		#for (pf, pmap) in paths.items():
		#for (pid, contents)

		#(paths, tot) = read_master_pathfile(pathfn, hide=aside, pos=hpos)

		allpaths=[]
		#		for pmap in paths.values():
		#			allpaths.extend( pmap.keys() )

		paths={}
		# all nodes in paths or subgraph...
		
		
		allnodes=[]
		for (pf, pmap) in master_paths.items():
			paths[pf]={}
			for (pid, contents) in pmap.items():
				# check for held aside nodes
				skip=False
				for p in hpos:
					#print p, contents["nodes"]
					if contents["nodes"][p] in aside:
						#print p, contents["nodes"][p]
						skip=True
						break				 
				if skip:
					continue

				paths[pf][pid]=contents
			
				allnodes.extend(contents["nodes"])
				allpaths.append(pid)

		allpaths=set(allpaths)

		print "read master pathfile"
		sys.stdout.flush()

		outf.write("* Solution %d\n*%s\n*%s\n*%s\n" % (sol, hitmapfn, pathfn, subgraphfn))

		# subgraphs
		subgraphs=dict( [ (subname, {"nodes":set(), "edges":set()}) for subname in master_subgraphs])
		for subname in subgraphs:
			for (pid, itmap) in master_subgraphs[subname].items():
				if pid in allpaths:
					for n in itmap["nodes"]:
						subgraphs[subname]["nodes"].add(n)
					for e in itmap["edges"]:
						subgraphs[subname]["edges"].add(e)

			allnodes.extend( list(subgraphs[subname]["nodes"]) )

		allnodes=set(allnodes)
		print "kept %d paths, %d nodes" % (len(allpaths), len(allnodes))

		# all nodes in paths or subgraph...
		#allnodes=set()
		#for (pf, pmap) in paths.items():
	#		for (pid, contents) in pmap.items():
#				allnodes = set.union(allnodes, set(contents["nodes"]))
		#for (s, itmap) in subgraphs.items():
		#	if s in allpaths:
		#		allnodes = set.union(allnodes, itmap["nodes"])
		outf.write("* found total of %d nodes in paths and subgraphs\n" % len(allnodes))

		print "* found total of %d nodes in paths and subgraphs\n" % len(allnodes)

		# restrict master label set to only path/subgraph nodes
		temp = {}
		for (l, lset) in labels.items():
			temp[l] = set.intersection(lset, allnodes)	
		labels=temp

		# print node sets - restrict to only path/subgraph nodes
		aside = set.intersection(aside, allnodes)
		
		print_node_edge_sets(labels, aside, paths, mode, outf)
		outf.write("\n")

		print "printed node edge sets"

		# print path sets
		print_path_sets(paths, outf)
		outf.write("\n")

		print "printed path sets"
	
		# print subgraph sets
		print_subgraph_sets(subgraphs, outf)

def print_node_edge_sets(labels, aside, paths, mode, outf):
	"""
	Prints some additional node/edge sets

	Set hide(node)      (hidden nodes)
	Set novelGene(node)	(unknown + hidden)
	Set h(node)			(hits - hidden, if hiding hits)
	Set intNode(node)   (interfaces - hidden, if hiding interfaces)
	Set intEdge(edge)   (interface edges in paths)
	"""
	#print_gams_set("hide(node)", "hidden nodes", aside)
	#print ""

	# genes without labels
	novel=set.union(labels["unknown"], aside)
	print_gams_set("novelGene(node)", "unlabeled or hidden genes", novel, out=outf)
	outf.write("\n")

	# interface nodes and edges - assume we've taken care of hiding
	# them according to the mode by now
	hits=set()
	intNodes=set()
	intEdges=set()	
	
	# { pathfinder : { pid : { "nodes":[], "edges":[] } } }
	for pf in paths:
		for pid in paths[pf]:
			hits.add(paths[pf][pid]["nodes"][0])
			intNodes.add(paths[pf][pid]["nodes"][-2])
			intEdges.add(paths[pf][pid]["edges"][-1])

	print_gams_set("hit(node)", "hits", hits, out=outf)
	outf.write("\n")
	print_gams_set("intNode(node)", "interface nodes", intNodes, out=outf)
	outf.write("\n")
	print_gams_set("intEdge(edge)", "interface edges", intEdges, out=outf)
	outf.write("\n")


def print_path_sets(paths, outf):
	"""
	Prints path sets.
	Example:
	Set path        "all paths (598077)"
	Set pstart(node,path)   "nodes that start paths (377)"
	Set pnode(node,path)    "nodes in paths (4568)"
	Set pedge(edge,path)    "edges in paths (57546)
	
	If you want to split paths by pathfinder, check the commented-out
	section in this function.
	"""
	allpids = []
	pstarts={}	 # { node : set(paths) }
	pnodes={} # { node : set(paths) }
	pedges={} # { edge : set(paths) }
	for pmap in paths.values():
		allpids.extend( pmap.keys() )
		for p in pmap.keys():
			n0 = pmap[p]["nodes"][0]
			if n0 not in pstarts:
				pstarts[n0]=set()
			pstarts[n0].add(p)	
		
			for (name, submap) in ( ("nodes",pnodes), ("edges",pedges)):
				for i in pmap[p][name]:
					if i not in submap:
						submap[i]=set()
					submap[i].add(p)
							

	print_gams_set("path", "all paths", allpids, out=outf)
	outf.write("\n")

	# We aren't doing special pathfinders right now.
	# If we want to, uncomment the following:
	#for (finder, pmap) in paths.items():
	#	print_gams_set("%s(path)" % finder, "paths from pathfinder %s" % finder, pmap.keys(), out=outf)
	#	outf.write("\n")

	print_gams_map("pstart(node,path)", "nodes that start paths", pstarts, out=outf)
	outf.write("\n")
	print_gams_map("pnode(node,path)", "nodes in paths", pnodes, out=outf)
	outf.write("\n") 
	print_gams_map("pedge(edge,path)", "edges in paths", pedges, out=outf)
	

def print_subgraph_sets(subgraphs, outf):
	""" prints subgraph sets:
		Set subgraph    "subgraph IDs (2)"
		Set subnode(subgraph, node)     "subgraphs and nodes (2)"
		Set subedge(subgraph, edge)     "subgraphs and edges (2)"
	"""	
	print_gams_set("subgraph", "subgraph IDs", subgraphs.keys(), out=outf)
	outf.write("\n")

	subnodes = dict( [ (s, subgraphs[s]["nodes"]) for s in subgraphs.keys() ] )
	subedges = dict( [ (s, subgraphs[s]["edges"]) for s in subgraphs.keys() ] )
	print_gams_map("subnode", "subgraphs and nodes", subnodes, collapse=False, out=outf)
	outf.write("\n")

	print_gams_map("subedge", "subgraphs and edges", subedges, out=outf)
	outf.write("\n")
	return


if __name__=="__main__":
	sys.exit(main(sys.argv))
