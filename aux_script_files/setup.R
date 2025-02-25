# Ensure 'remotes' is installed for GitHub installations
if (!requireNamespace("remotes", quietly = TRUE)) {
    install.packages("remotes", repos = "https://cloud.r-project.org")
}

# List of required CRAN packages
cran_packages <- c("argparser", "dplyr", "ggplot2", "sf")

# Install any missing CRAN packages and load them
for (pkg in cran_packages) {
    if (!requireNamespace(pkg, quietly = TRUE)) {
        install.packages(pkg, repos = "https://cloud.r-project.org")
    }
    library(pkg, character.only = TRUE)
}

# Install the specific commit of mggg/redist-fork from GitHub
remotes::install_github("mggg/redist-fork", ref = "0cdab508e166c398c3f06663220246194d7692e5")
