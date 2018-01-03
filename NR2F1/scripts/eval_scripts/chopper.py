"""
Chops PR files off at the last original point before total recall.
Also adds an initial PR point at (0, first_precision) - draw horizontal line
left from first PR point.

CAVEAT:
-This should ONLY be used when the original confidence values include zero values.
In that case, the last point in the .opr represents the recall when including
all zero-confidence items, and so it's reasonable to just cut it off.
If there are NO zero confidence values, then cutting off the last point means
spuriously cutting off the last confidence values.

Usage:
	chopper.py	file.opr file.pr [file.spr]
"""
import sys
import os
from os.path import split, join, splitext

def getCutPoint(oprFile):
	""" Get 1) the cut point from the opr (second to last line)
	and 2) the starting precision (first line), setting recall=0.
	Returns two tuples: (cutR, cutP) and (0.0, origP) """
	
	buffy = ""
	
	first=oprFile.readline()
	sp=first.strip().split()
	origP=float(sp[1])
	
	for line in oprFile:
		line = line.strip()
		sp = line.split()		
		if float(sp[0]) < 1:
			buffy = line
	(cutRecall, cutPrecision) = buffy.split()
	return ( (cutRecall, cutPrecision), (0.0, origP)) 
		
def chop(origFile, newFile, origPoint, cutPoint):
	""" Reads and reprints the origFile up through the cut point."""
	#(cut, orig) = cutPoint
	(cutR, cutP) = cutPoint
	#(origR, origP) = orig
	
	newFile.write("%.10f\t%.10f\n" % origPoint)
	go=True
	while go:
		line = origFile.readline().strip()
		if len(line)==0:
			go=False
			continue			
		(rS,pS) = line.split()
		(rF,pF) = (float(rS), float(pS))
		rS = "%.10f" % rF
		pS = "%.10f" % pF
		#newFile.write(line)
		#newFile.write("\n")
		
		newFile.write("%s\t%s\n" % (rS, pS))
	
		#print line
		if rS==cutR and pS==cutP:
			go=False	
			
def getChopFilename(origName):
	""" Gets the filename for the chopped output."""
	(head, tail) = split(origName)
	(root, ext) = splitext(tail)
	newfn = "%s_chop%s" % (root, ext)
	chopName = join(head, newfn)
	return chopName	

opr = sys.argv[1]
others = sys.argv[2:]

if len(others)==0:
	print "No files to chop."

oprFile = open(opr, "r")
(cutPoint, origPoint) = getCutPoint(oprFile)
oprFile.close()

for o in others:
	ofile = open(o, "r")
	newfilename = getChopFilename(o)
	print "Producing %s" % newfilename
	newfile = open(newfilename, "w")	
	chop(ofile, newfile, origPoint, cutPoint)
	newfile.close()
	ofile.close()





