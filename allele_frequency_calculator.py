#!/usr/bin/env python

import pandas as pd
import numpy as np
import argparse
import os

# Function to parse command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Allele Frequency Calculator")
    parser.add_argument("--genotypes", required=True, help="Genotype file (samples x SNPs, TSV)")
    parser.add_argument("--annotation", required=False, help="SNP annotation file (optional)")
    parser.add_argument("--output", required=True, help="Output TSV file")
    parser.add_argument("--missing", default="NA", help="Missing value code")
    return parser.parse_args()

# Function to compute allele frequencies and genotype counts
def compute_allele_freq(geno_df):
    results = []
    for snp in geno_df.columns:
        # Convert SNP values to numeric, coerce errors to NaN
        snp_values = pd.to_numeric(geno_df[snp], errors='coerce')
        snp_values = snp_values[snp_values.notna()]  # Remove missing values
        n_non_missing = len(snp_values)
        
        # Count genotypes 0, 1, 2 (homozygous ref, heterozygous, homozygous alt)
        counts = snp_values.value_counts().reindex([0,1,2], fill_value=0)
        
        # Compute minor allele frequency (MAF), skip if few non-missing samples
        if n_non_missing < 10:
            maf = np.nan
        else:
            total_alleles = 2 * n_non_missing
            alt_alleles = counts.get(1,0) + 2*counts.get(2,0)
            maf = min(alt_alleles/total_alleles, 1 - alt_alleles/total_alleles)
        
        # Store results for this SNP
        result = {
            "snp_id": snp,
            "count_0": counts.get(0,0),
            "count_1": counts.get(1,0),
            "count_2": counts.get(2,0),
            "n_non_missing": n_non_missing,
            "maf": maf
        }
        results.append(result)
    
    # Convert list of dictionaries to DataFrame
    results_df = pd.DataFrame(results)
    return results_df

def main():
    args = parse_args()
    
    # Check if genotype file exists
    if not os.path.exists(args.genotypes):
        raise FileNotFoundError(f"Genotype file not found: {args.genotypes}")
    
    # Load genotype file (transpose to have SNPs as columns)
    geno_df = pd.read_csv(args.genotypes, sep="\t", index_col=0).T

    # Replace missing value codes with NaN
    geno_df.replace(args.missing, np.nan, inplace=True)
    
    # Compute allele frequencies and genotype counts
    results_df = compute_allele_freq(geno_df)
    
    # Merge SNP annotation if provided
    if args.annotation:
        if not os.path.exists(args.annotation):
            raise FileNotFoundError(f"Annotation file not found: {args.annotation}")
        annot_df = pd.read_csv(args.annotation, sep="\t")
        results_df = results_df.merge(annot_df, on="snp_id", how="left")
        
        # Reorder columns safely
        cols = ["snp_id", "chrom", "pos", "count_0", "count_1", "count_2", "n_non_missing", "maf"]
        results_df = results_df[[c for c in cols if c in results_df.columns]]
    
    # Save results to output file, creating directories
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    results_df.to_csv(args.output, sep="\t", index=False)
    print(f"Allele frequency results saved to {args.output}")

if __name__ == "__main__":
    main()
