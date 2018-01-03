# We save memory by reading in only the sets that we need to for each 
# sample of the data. (We can eliminate some percentage of paths from each run.)
# So, we create sample-specific GAMS set files in advance of running inference.
# This is also moderately time-consuming.
start=0
end=100
mode=both	# both hits and interfaces are sampled

# We use the "hidden by sample" file to identify which paths are candidates for 
# each sample. This was generated in the kernel part of the pipeline.
hitmap=dk_scores_nov2014/hiv_0.75_hidden_by_sample.tab

# Master label file of human genes, marking each as hit, interface, hit|interface,
# or unknown.
# This was generated in the kernel part of the pipeline.
labels=data/hiv_human_gadget_master_labels.tab

# Files produced by Java: full path info and subgraph info.
paths=data/hiv_len3_gadget_master_paths.tab
subgraphs=data/hiv_len3_gadget_master_subgraphs.tab

# Desired output location (remember this for set_up_for_any_limit.sh)
pathfiles=pathfiles_baseline
if [ ! -e $pathfiles ]; then
	mkdir $pathfiles
fi

# Output file name pattern. Will replace %d with the sample ID number.
# You don't need to change this.
outpat="${pathfiles}/hiv_0.75_%d_moresets.gms"

python scripts/create_custom_pathfile_batch.py $start $end $mode $labels $hitmap $paths $subgraphs $outpat 
