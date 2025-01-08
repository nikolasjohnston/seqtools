# Load required libraries
library("Biostrings")
library("ape")

# Set the working directory
setwd("~/OneDrive/Work/PostDoc/2024/Research/papers_projects/ABRS_Calliphoridae/Sternalis paper/Data analysis/phylo/u148785_1034134/")

# Read the alignment file (e.g., in FASTA format)
alignment_file <- readDNAStringSet("sternalis_part_alignment.fasta")

# Read the label data CSV
label_data <- read.csv("label_data.csv")

# Create a named vector for the new labels with original labels as names
label_dict <- setNames(label_data$new_label, label_data$old_label)

# Create a new DNAStringSet by renaming the sequence names
new_alignment <- alignment_file
names(new_alignment) <- sapply(names(alignment_file), function(seq_name) {
  if (seq_name %in% names(label_dict)) {
    return(label_dict[[seq_name]])
  } else {
    return(seq_name)
  }
})

# Write the new alignment to a file
writeXStringSet(new_alignment, filepath = "sternalis_part_alignment_renamed.fasta", format = "fasta")

# Optional: If you want to compare the names before and after renaming
print("Original names:")
print(names(alignment_file))
print("Renamed names:")
print(names(new_alignment))
