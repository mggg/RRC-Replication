#!/bin/bash

julia aux_script_files/setup.jl
export JULIA_PROJECT=$(pwd)

# Get the Python version (only the major and minor numbers)
GOOD_PYTHON_VERSION=$(python3 -c "import sys; print(sys.version_info.minor >= 10)")

# Check if Python is 3.9 or higher but less than 4.0
if [[ "$GOOD_PYTHON_VERSION" == "True" ]]
then
    echo "Found compatible Python version"
    python3 -m venv .venv 

    source .venv/bin/activate
    pip3 install -r py_requirements.txt
else 
    echo "Error: Python version must be >=3.10. Please install a compatible version."
fi


cargo install binary-ensemble --version 0.2.0
cargo install --git https://github.com/peterrrock2/msms_parser.git --rev 3c37fc5a57b1b9480b95d3d01cad9c37e6564f59
cargo install --git https://github.com/peterrock2/smc_parser.git --rev 03edd583e40e6198045d62e9eeb8a3e543bb1551
cargo install --git https://github.com/mggg/frcw.rs --rev b28260bc1eba425731b7ae6a194ab4a2cd4532b6
cargo install --path ./data_processing/Ben_Tally

# Check if Rscript is installed
if ! command -v Rscript &> /dev/null; then
    echo "Error: Rscript is not installed. Please install R before running this script."
    exit 1
fi

# Install redist from MGGG
Rscript aux_script_files/setup.R