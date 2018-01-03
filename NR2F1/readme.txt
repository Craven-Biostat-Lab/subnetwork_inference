README

CandidatePath.jar runs the candidate path algorithm. Use baseline.config as argument. 
Make sure to change path structure in baseline.config to match user path structure


Data Directory:
	-literome_total_DE-edges contains all literome edges
	- master_ppi.tab is protein protein interactions taken from Biogrid and Hippie
	- ntype2_DE.tab are the differentially expressed targets
	- white_tf_spread.tab contains the Nuclear receptor mapping network for MCF-7 line

	Encode_TFDE: contains files mapping TF to genes from ENCODE

GAMS
	Contains gams files for running process


run_pipeline.sh runs the entire pipeline
Usage: ./run_pipeline.sh <outputsamples> <start> <end>
Make sure to change path to match current structure.


