README

1. Data Directory
	a) Edges Directory
		- Contains all files used to connect nodes from variety of biomedical sources (biogrid,hprd,reactome)
	b) Nodes Directory
		- agg_interfaces.tab: List of interfaces retrieved from Roger Ptak
		- hits_gadget.tab: List of hits from experiments RNAi experiments as well as potential hits identified with GADGET
		- hiv_genes.tab: list of HIV genes
		- ubiqiutin.tab: ubiquitin varients used for filtering

2. Candidate Path Directory
	Contains code for running candidate path. Run using CandidatePath.jar
	gadget_hiv_baseline.config is the configuration file that is treated as an argument passed in when running
	Change file structures in config file to match your own directory paths

3. Diffusion Kernel Directory
	run_kernel_everything.sh runs the diffusion kernel. Requires network file output from candidate path as well as a file combining both hits and interfaces. 
	Outputs into directory with kernel scores as well as multiple datasets where 25% of hits and interfaces were held aside. 


4. GAMS directory
	contains all necessary GAMS scripts to perform IP. 
	create_custom_pathfile_batch generates pathfiles based on sampling done in Diffusion kernel
	run_sample_maxpath_replace.gms runs the IP based on the model contianed in model.gms 



