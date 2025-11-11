library(redist)
library(dplyr)
library(sf)

pop_tol <- 0.00001
pop_col <- "population"
vtds <- st_read(dsn = "../../shapefiles/7x7")
population <- sum(vtds$TOT_POP)


for (nsims in seq(from = 5000, to = 100000, by = 5000)) {
	for (rng_seed in 40:61) {
        set.seed(rng_seed)
        seed <- redist_map(vtds, total_pop=pop_col, pop_tol=pop_tol, ndists=7)
        plans <- redist_smc(seed, nsims=nsims, compactness=1)
        prefix <- paste("../raw_data_files/7x7_smc/7x7_compactness_1_seed_", rng_seed, "__", nsims, ".rds")
        saveRDS(plans, prefix)
        saveRDS(attr(plans, "wgt"), paste(prefix, ".wgt", sep=""))
        saveRDS(attr(plans, "plans"), paste(prefix, ".plans", sep=""))
    }
}


for (nsims in seq(from = 50, to = 5000, by = 50)) {
	for (rng_seed in 51:61) {
        set.seed(rng_seed)
        seed <- redist_map(vtds, total_pop=pop_col, pop_tol=pop_tol, ndists=7)
        plans <- redist_smc(seed, nsims=nsims, compactness=1)
        prefix <- paste("../raw_data_files/7x7_smc/7x7_compactness_1_seed_", rng_seed, "__", nsims, ".rds")
        saveRDS(plans, prefix)
        saveRDS(attr(plans, "wgt"), paste(prefix, ".wgt", sep=""))
        saveRDS(attr(plans, "plans"), paste(prefix, ".plans", sep=""))
    }
}