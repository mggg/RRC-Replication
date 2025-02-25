# Reversible Recom Replication

This is a repository containing some of the code needed to replicate the
work for our reversible recom paper
[Spanning Trees and Redistricting: New Methods for Sampling and Validation](https://mggg.org/rrc).

This repository is not complete at this time.

## Folder Descriptions

- aux_script_files: Contains a script to set up the Julia environment and install the
    necessary packages.
- cli_file: Contains the CLIs created for running both the SMC and the Forest ReCom 
    methods. These were necessary for batching jobs on the HPC.
- data_processing: Contains the main file used for processing much of the raw data
    into a format that can be used for the figure scripts.
    - Ben_Tally: Contains the `Ben-Tally` rust library which is used to tally the 
        cut edges, key values, and assignment filp counts for ensembles of interest.
    - other_processing_scripts: Contains more scripts used for data processing. Mainly,
        this directory contains the scipts used to generate the complete enumeration of
        7x7 grid graphs into 7-ominos.
- example_files: Contains some example files that can be used to recreate several steps in
    the analysis pipeline.
- figure_and_table_generation: Contains the scripts used to generate the figures and tables
    in the paper.
    - figure_scripts: Contains the scripts used to generate the figures in the paper.
    - figures: Contains copies of the figures that were used in the paper.
    - table-outputs: Contains the outputs of the table scripts. Used to construct tables 
        in the paper.
    - table_scripts: Contains the scripts used to generate the tables in the paper.
- hpc_files: 
    - hpc_logs: An empty folder that is left in place to make the replication process easier
        when running slurm scripts.
    - hpc_processed_data: An empty folder that is left in place to make the replication process easier
        when running slurm scripts.
    - hpc_raw_data: An empty folder that is left in place to make the replication process easier
        when running slurm scripts.
    - slurm_scripts: Contains copies of the slurm scripts used to run the Reversible ReCom, Forest
        ReCom, and SMC on the Tufts HPC.
- JSON_dualgraphs: Contains the JSON-formatted dual graphs used in the creation of our
    figures.
- other_data_files: Contains some data and script files used to process the remainder 
    of the data obtained from experimental runs.
    - data_files: Additional data files needed for our analysis.
    - script_files: Additional scripts used to make relevant data files. These scripts
        were generally not used in the cluster, but were instead ran on a local machine.
- shapefiles: Contains the shapefiles used in the creation of some of our figures (necessary
    for SMC).

## Simple Setup

To set up this project to run some of the analysis scripts contained within, you 
can simply invoke

```console
source setup_all.sh
```

sourcing is necessary to make sure that the Julia project is set up correctly.
You will need to have Julia, Cargo, and RStudio installed in order for this to run without 
errors. (Note: This script requires the use of a Unix based operating system, such as 
MacOS or Linux. Windows users may invoke this by setting up the subsystem for Linux)


To install Cargo, visit the 
[Rustup Download Page](https://doc.rust-lang.org/cargo/getting-started/installation.html)
and follow the instructions for your operating system. Likewise, to install Julia,
visit the [Julia Installation Page](https://julialang.org/downloads/).
And installing R/RStudio can be done through the 
[RStudio Installation Page](https://posit.co/download/rstudio-desktop/)
All of the work for this project was done using Julia version 1.9.3, and but it should
still work with Julia versions 1.9.\*-1.x.\*, and all R work was done using version
4.4.0, but everything will be fine on versions 4.4.\*.

(Note: It may be easier for MacOS users to install Julia using the Homebrew package manager
than installing from the Julia website.)

> :warning: There appears to be a memory leak bug that sometimes appears when running the `redist`
> package. This memory leak appears to be an issue with the R interpreter not freeing memory
> appropriately when the R base language and the relevant RCpp and Rarmadillo libraries
> are compiled with an earler version of gcc. To avoid this bug, please make sure to have
> R version >= 4.4.2 and a gcc released after 15 May 2024. Relevant gdal and fortran compilation
> libraries should also be up-to-date.

## More Detailed Setup instructions in case the script fails

### Julia

To run any of the Julia script files contained in this repository, you will need to
download the the correct version of the Julia code from github using the included setup file:

```console
julia aux_script_files/setup.jl
```

Alternatively, you can activate the Julia interactive terminal by calling `julia`
and then make the following commands:

```julia
julia> import Pkg
julia> Pkg.activate(".")
julia> Pkg.add(RandomNumbers)
julia> Pkg.add(url="https://github.com/peterrrock2/Multi-Scale-Map-Sampler#msms_with_alpha")
```

You may also need to set your `JULIA_PROJECT` environment variable to the same directory
as this README file. This can be done by running the following command:

```console
export JULIA_PROJECT=$(pwd)
```

### R and RStudio

To run the Sequential Monte Carlo (SMC) code for this repository, you will need to have the
appropriate version of R (you don't _need_ RStudio, but it is nice to have) installed, as
well as the following packages:
 
- argparser
- dplyr
- ggplot2
- remotes
- sf

To install these packages, you can simply invoke the R terminal (or open RStudio)
and call

```R
> install.packages("argparser")
> install.packages("dplyr")
> install.packages("ggplot2")
> install.packages("remotes")
> install.packages("sf")
> install.packages("argparser")
> library("remotes")
> remotes::install_github("mggg/redist-fork", ref = "0cdab508e166c398c3f06663220246194d7692e5")
```

After that, the `smc_cli.R` file should work as expected.


### Common issues with R installation

During the installation process, you might come accross an error saying that the packages 's2'
and 'units' are not installed. If you then try to install 's2' using R's package 
manager, you may then get an error like

```console
ERROR: configuration failed for package ‘s2’
* removing ‘/usr/local/lib/R/site-library/s2’

The downloaded source packages are in
        ‘/tmp/RtmpNb5oyb/downloaded_packages’
Error in library(pkg, character.only = TRUE) :
  there is no package called ‘s2’
In addition: Warning message:
In install.packages(pkg, repos = "https://cloud.r-project.org") :
  installation of package ‘s2’ had non-zero exit status
Execution halted
```

This generally means that your system is missing some dependencies. In an Debian-based distro
(e.g. Ubuntu), you may rectify this via 

```console
apt update && apt install -y \
  libgdal-dev \
  libgeos-dev \
  libproj-dev \
  libudunits2-dev \
  libssl-dev \
  libcurl4-openssl-dev \
  libprotobuf-dev \
  protobuf-compiler \
  libcairo2-dev
```

Which will install the packages needed for 's2' to work on your system.

If you are on mac, then the corresponding brew packages would be:

```console
brew update && brew install \
  gdal \
  geos \
  proj \
  udunits \
  openssl \
  cairo
```

### Other dependencies

In order to convert the "atlas" format that is output by the MSMS code to an assignment-vector 
format, it is necessary to install the `msms_parser`, `smc_parser` and `ben` cli tools. This
can be downloaded using the Cargo package manager. 
The `ben` cli tool may then be installed using the command

```console
cargo install binary-ensemble
```

and `msms_parser` and `smc_parser` can be installed using

```console
cargo install --git https://github.com/peterrrock2/msms_parser.git
cargo install --git https://github.com/peterrrock2/smc_parser.git
```

In addition to these CLI tools, you will need the `ben-tally` cli tool that allows for tallying across an output BEN file.
This is included in the 'Ben_Tally' folder and may be installed using

```console
cargo install --path ./data_processing/Ben_Tally
```

There are a couple of different modes for the `ben-tally` CLI. The default mode tallies the cut edges of the partition
and may be invoked using

```console
ben-tally -g <path-to-JSON-file> -b <path-to-BEN-file-to-tally>
```

This will output a file with the suffix "cut-edges.parquet" added to it which can then be read in python.
In the event that you would like to tally particular attributes of graph, you will need to use the command


```console
ben-tally -m tally-keys -g <path-to-JSON-file> -b <path-to-BEN-file-to-tally> --keys <list-of-keys-to-tally>
```

so an example usage would be

```console
ben-tally -m tally-keys -g ./JSON/VA_precincts.json -b VA_Forest_steps_10000000_rng_seed_278986_gamma_0.0_alpha_1.0_ndists_11_20241112_124346.jsonl.ben --keys G16DPRS G16RPRS
```


## Replicating the Work

Replication of much of this work requires access to a HPC (and one that uses the Slurm 
scheduler if you would like to run the batch script files contained in this repository).

### Running the Slurm Batch Scripts

Each of the Slurm batch scripts should be runable from a copy of this repository. That is
to say, if you clone a copy of this repository, then you should be able to run the
scipts simply by calling 

```console
sbatch <script-name>
```

from the command line while in the `slurm_scripts` directory (Note: if you call the script from
the wrong directory, you will get some path errors due to relative path resolution issues).
