# HPC Files

This folder contains copies of the slurm scripts used to run the Reversible ReCom, Forest ReCom,
and SMC on the Tufts High Performance Cluster (HPC) as well as some of the processed data.


## hpc_logs

This folder is contains a skeleton of the of the log folders where the slurm scripts will write
their logging information. All folders are empty but are left in place to make running the 
replication scripts easier.

## hpc_raw_data

This folder containse a skeleton of the raw data folders where the slurm scripts will write their
output. All folders are empty since the relevant data is too large to store on GitHub, but the data
can be obtained upon request.

## hpc_processed_data 

This folder contains a skeleton of the processed data folders where the relevant data processing
scripts will write their output. All folders are empty since the relevant data is too large to 
store on GitHub, but the data can be obtained upon request.


## slurm_scripts

The scripts contained in the `slurm_scripts`
folder make use of a batch scheduler called SLURM that is available on some cluster computers
but which is not generally available for most consumer-grade computers. As such, the inclusion of 
these scripts is intended to allow for the replication of the results either through replication
on a suitably outfitted cluster computer or through mild modification of the bash scripts to run
on consumer hardware. As a note, the included scripts have been tested and provide a relatively 
good indication of the runtime and resouce requirements for running each of these methods, and 
so it is generally recommended that anyone attempting to replicate this work use the
included default settings.

Note that in order to run the scripts, it is often necessary to load the appropriate modules
for the invoked software. For example, to run the Forest ReCom script on the cluster that we used,
it was necessary to make sure that the Julia module was loaded using

```console
module load julia/1.9.3
```