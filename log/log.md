- Convert .fasta file into .csv and upload into mysql to handle it easily.
- Remove rows with duplicated pair <alpha,beta> to avoid TCR that points to different <HLA,PEP> groups. Export it as nodups.csv
- Remove <HLA,PEP> groups with less than 75 TCR because they are not useful to the analysis. Also, add a column called groupID to identify <HLA,PEP> groups easily. We keep only 12 groups. Export it as clean.csv
