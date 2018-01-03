#!/bin/bash
# Run this script on a directory of .list files. 
# It will run the AUC tool to generate PR curve files, and then
# run the "chopper" tool to cut the curve off at the last recall point.
# AUC tool generates .opr, .pr, .spr files.
# Chopper produces _chop.opr and _chop.pr for each .opr file processed.
# Some corner cases:
# - If the recall in fact does go to 1 (no zero confidence values in .list),
#   then the chopper is not run.
# - If the recall is 0 (no nonzero confidence values in .list), then
#	neither AUC nor chopper is run. 

if [[ $# -ne 1 ]]; then
	echo "Usage: bash run_auc_and_chopper.sh directory"
	exit
fi

# make sure scripts available
if [[ ! -e scripts/eval_scripts/chopper.py ]]; then
	echo "I can't find scripts/chopper.py."
	exit
fi

if [[ ! -e scripts/eval_scripts/auc_chasman.jar ]]; then
	echo "I can't find scripts/auc_chasman.jar."
	exit
fi

for f in $1/*.list; do
	# get the basename
	pathbase=${f%.list}
	
	# check: no nonzero confidence values? then don't run AUC tool.
	above0=$(grep -v "#" ${f} | grep -v "^0\.000000" | wc -l)
	#echo $above0
	if [[ $above0 == 0 ]]; then
		echo "No nonzero confidences for ${f}. Skipping PR curve calculation."
		continue
	fi
	
	# AUC tool calculates PR curve
	java -jar scripts/eval_scripts/auc_chasman.jar -t list -o ${pathbase} ${f} > ${pathbase}.auc
	
	# don't chop if no nonzero confidence values
	at0=$(grep -v "#" ${f} | grep "^0\.000000" | wc -l)
	if [[ $at0 == 0 ]]; then
		echo "Only nonzero confidence scores for ${f}. Skipping the chopper."
		continue
	fi	
	
	# chopper cuts off PR curves at the last recall point
	python scripts/eval_scripts/chopper.py ${pathbase}.opr ${pathbase}.opr ${pathbase}.pr
done

