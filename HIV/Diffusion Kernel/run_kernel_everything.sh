#!/bin/bash

# Pipeline for creating the ensemble of DK score sets.
# Samples the hits and interfaces, keeping the same fraction of each.
# USAGE:
# bash run_kernel_everything.sh output_directory sif_file hit_interface_file

# Produces:
# An output directory containing GAMS-ready scores for each sample, and a master file
# that notes which hits/interfaces are held aside per sample
# Kernel scores when no hits/interfaces held aside
# Leave-one-out cross-validation list file (.list files are input to the AUC tool)
# Degree-ranked list file

# Calculate DK scores per sample.
# You need to use numpy for this, so make sure you have the right python. 
# When I left Biostats, we had to use python 2.7, which wasn't the default.

# You should replace the locations of files in the variables at the top.
# It's currently set up to run the baseline.

if [[ $# -ne 3 ]]; then
	echo "Usage: bash run_kernel_everything.sh output_directory sif_file hit_interface_file"
	exit
fi

#### VARIABLES updated by command line.#####
# Location of scripts.
scripts=scripts

# Main directory to put all of the output files into.
output=$1 # e.g., samples_baseline

# Background network from baseline
# The Python script will also check for a pre-made kernel file with the same base name, but 
# suffix _kernel.npy
# to see if we've already generated a kernel for the background network file.
# You need to make a new kernel if you change the background network.
sif=$2  #eg, input_networks/hiv_len3_background_no_hiv_cx.sif

# remove .sif suffix
sif_fn=${sif%%.*}	
# basename for sif file: remove both suffix and path
sif_base=${sif_fn##*/}

# Combined hits and interfaces
hits_and_ints_fn=$3 # eg, input_hits/hits_plus_ints.tab

# check existence
for fn in $sif $hits_and_ints_fn; do
	if [ ! -e ${fn} ]; then
		echo "Can't find file $fn."
		exit
	fi
done

# Number of samples
SOLS=100	


#######


results=${output}/${sif_base}_kernel_results


# Check for directories
if [ ! -e ${output} ]; then
	mkdir ${output}
	echo "Made output directory ${output}"
else
	echo "Sorry, output directory ${output} already exists. Delete and try again?"
	exit
fi

# Check for directories
if [ ! -e ${results} ]; then
	mkdir ${results}
	echo "Made results directory ${results}"
else
	echo "Sorry, results directory  ${results} already exists. Delete and try again?"
	exit
fi


####


# First, get the DK scores. Read in the background network (human genes only; no complexes or HIV),
# read in the hits and interfaces. Do ${SOLS} samples of hits and interfaces each with three different 
# percentages of kept nodes: 0.25, 0.50, 0.75.
# This will take a long time and consume a lot of memory, unless you have a .npy file available!
echo "Starting DK score-smoothing process for samples at three hit-keeping frequencies. Also doing leave-one-out."

karg=""
# check for kernel
if [ -e ${sif_fn}_kernel.npy ]; then
	karg=k
	echo "Will be using existing kernel file ${sif_fn}_kernel.npy."
fi

python ${scripts}/get_sample_scores.py ${karg} ${hits_and_ints_fn} ${sif_fn}.sif ${SOLS} 0.25 0.50 0.75 ${output}
echo "Done with scoring."

# Make the master label file for this background network.
python ${scripts}/make_master_label_list.py ${hits_and_ints_fn} ${sif_fn}.sif > ${sif_fn}_master_labels.tab
echo "Created master label file " ${sif_fn}_master_labels.tab

# make degree-based list file
# you need to list out all of hit|interface, hit, and interface because my script is a little silly
python ${scripts}/rank_by_degree.py ${sif_fn}.sif ${sif_fn}_master_labels.tab "hit|interface" hit interface > ${output}/hiv_by_degree.list


echo "Making files of hits/interfaces hidden per sample."
# Create the "hits hidden per sample" files that we'll use in the inference pipeline.
# In the process, divide sample results into subdirectories in the sample output directory.
for frac in 0.25 0.50 0.75; do
	subdir=${output}/sample${frac}
	if [ ! -e ${subdir} ]; then
		mkdir ${subdir}
		echo "Made" $subdir
	fi
	mv ${output}/sample_${frac}_* ${subdir}	
	echo "Moved samples into " $subdir
	
	python ${scripts}/make_hidden_by_sample.py ${subdir} ${frac} ${SOLS} > ${output}/hiv_${frac}_hidden_by_sample.tab
	echo "Created " ${output}/hiv_${frac}_hidden_by_sample.tab
done

echo "Done."

# Gathers results from sampled kernel scores
echo "Gathering results into .list files."
for p in 0.25 0.50 0.75; do
	python ${scripts}/eval_kernel_sample_results.py ${output}/sample${p}/ ${output}/hiv_${p}_hidden_by_sample.tab ${sif_fn}_master_labels.tab "hit|interface" hit interface > ${results}/hiv_${p}_kernel_hit_and_interface.list
		
done
