#!/bin/bash

# Runs the pipeline



topdir=$(pwd)
sample_dir=$1
start=$2
stop=$3

mkdir inter_results
mkdir network_files

cd ${sample_dir}

for i in $(seq $start $stop); do

    #make directories
    if [ ! -d "samples_${i}" ]; then
        echo Creating folder $i
        mkdir samples_${i}
    fi
    cd samples_${i}

    if [ ! -d "input_data" ]; then
        mkdir input_data
    fi
    
    if [ ! -d "output_data" ]; then
        mkdir output_data
    fi

    if [ ! -d "gams_intermediates" ]; then
        mkdir gams_intermediates
    fi

    if [ ! -d "final_output" ]; then
        mkdir final_output
    fi

    #link in specific files for search test
    ln -s ${topdir}/search_tester/CandidatePath.jar .
    ln -s ${topdir}/search_tester/baseline.config  .
    ln -s ${topdir}/datasets/ntype2_DE.tab ./input_data/ntype2.tab
    ln -s ${topdir}/datasets/test_cand_reg.tab ./input_data/test_cand_reg.tab

    #generate intermediate samples
    python ${topdir}/scripts/intermediate_sampler.py ${topdir}/datasets ${i}

    #generate ppi network
    python ${topdir}/scripts/ppi_builder.py ${topdir}/datasets/master_ppi.tab ./input_data/sample_${i}_intermediate.tab 
    python ${topdir}/scripts/interaction_filter.py ./input_data/ppi.tab #filters out non-coding genes

    #generate tf network
    python ${topdir}/scripts/search_file_builder.py ${topdir}/datasets/ENCODE_TFDE/ ${topdir}/datasets/white_tf_spread.tab ./input_data/sample_${i}_intermediate.tab
    python ${topdir}/scripts/interaction_filter.py ./input_data/test_tf2.tab 

    #generate literome network
    python ${topdir}/scripts/literome_edge_builder.py ${topdir}/datasets/literome_total_DE_edges.txt ${topdir}/datasets/genename_to_entrez.txt ./input_data/sample_${i}_intermediate.tab
    python ${topdir}/scripts/interaction_filter.py ./input_data/test_literome.tab




    #generate st pairs
    python ${topdir}/scripts/st_builder.py


    #run search_tester
    java -jar CandidatePath.jar ./baseline.config

    #link in gams file
    ln -s ${topdir}/gams_files/solver_target_hits.gms .
    ln -s ${topdir}/gams_files/max_rna_solver.gms .
    ln -s ${topdir}/gams_files/combined_solver_max_edges.gms .
    ln -s ${topdir}/gams_files/cplex.opt .

    #run gams to find maximum number of targets reached
    gams solver_target_hits.gms -lo 2

    #make intermediates
    python ${topdir}/scripts/target_ntype2_builder.py
    python ${topdir}/scripts/rna_intermediate_builder.py ./input_data/sample_${i}_intermediate.tab


    #make more intermediates
    python ${topdir}/scripts/gadget_intermediate_builder.py ${topdir}/datasets/breast_cancer_gadget.txt

    #run gams for combined
    gams max_rna_solver.gms -lo 2 

    #run final values
    python ${topdir}/scripts/networkBuilder_up_down.py ${topdir}/datasets/genename_to_entrez.txt ${topdir}/datasets/master_DE_gene_list.txt

    cp ./final_output/final_intermediates.txt ${topdir}/inter_results/intermediate_${i}.txt
    cp ./input_data/sample_${i}_intermediate.tab ${topdir}/inter_results/
    cp ./final_output/network.txt ${topdir}/network_files/network_${i}.txt
    cp ./final_output/nodenet.txt ${topdir}/network_files/nodenet_${i}.txt


    # re run
    cd ${topdir}
    cd ${sample_dir}

done




