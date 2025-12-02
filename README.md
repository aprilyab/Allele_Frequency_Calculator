# Allele Frequency Calculator

## Overview
The **Allele Frequency Calculator** is a Galaxy tool designed to calculate **per-SNP genotype counts** and **minor allele frequencies (MAF)** from genotype data in tabular (TSV) format. It is useful for genetic association studies, quality control of SNP data, and downstream population genetics analysis.

Clone this repository: hg clone https://henok_yoseph@toolshed.g2.bx.psu.edu/repos/henok_yoseph/allele_frequency_calculator
---

## Features

- Computes **genotype counts** for each SNP:
  - `count_0` → homozygous reference
  - `count_1` → heterozygous
  - `count_2` → homozygous alternative
- Computes **Minor Allele Frequency (MAF)**
- Handles missing values (`NA` by default, customizable)
- Optional **SNP annotation merge** (chromosome and position)
- Outputs **tabular TSV file** ready for downstream analysis
- Compatible with Galaxy workflows

---

## Installation

### Dependencies
The tool uses Python 3 and requires the following Python packages (handled via Galaxy Conda integration):

- `pandas >= 1.0`
- `numpy >= 1.0`

### Galaxy Installation
1. Clone or copy the tool directory to your local Galaxy `tools/` folder.
2. Ensure the XML wrapper and Python script are in the same directory.
3. Add the tool directory to your `tool_conf.xml` in Galaxy if not using auto-discovery.
4. Install dependencies automatically via Galaxy Conda integration.

---

## Input Files

### Required
1. **Genotype File** (`TSV` format)
   - Samples in rows, SNPs in columns, or vice versa (ensure the `--transpose` parameter if needed)
   - Missing values can be represented by `NA` or other characters
   - Example:
     ```
     snp_id    rs100000    rs100001    rs100002
     sample1   0           1           2
     sample2   1           0           NA
     ```

### Optional
2. **SNP Annotation File** (`TSV` format)
   - Columns: `snp_id`, `chrom`, `pos`
   - Allows adding chromosome and position information to output

---

## Parameters

| Parameter        | Description |
|-----------------|-------------|
| `--genotypes`    | Path to the input genotype TSV file (required) |
| `--annotation`   | Path to SNP annotation file (optional) |
| `--output`       | Path to save the output TSV file (required) |
| `--missing`      | Character representing missing values (default: `NA`) |

---

## Output

- A **tabular TSV file** with the following columns:
snp_id     chrom  pos  count_0  count_1  count_2  n_non_missing maf
rs1000001  10100  50     30       20       100        0.25
rs1000011  10200  45     35       20       100        0.275


## Usage in Galaxy

1. Upload your **genotype file** and optionally **SNP annotation file**.
2. Set missing value code if different from `NA`.
3. Run the tool and download the **Allele Frequency Results**.


## Testing

A set of test files is included in `test-data/`:

- `genotypes.tsv` → sample genotype input
- `snp_annotation.tsv` → sample SNP annotation
- `expected_output.tsv` → expected output for Planemo tests

Run automated tests with Planemo:

```bash
planemo test allele_frequency_calculator.xml

Development Notes

    -The script is written in Python using pandas for data manipulation.

    -Missing values are handled using pandas NaN.

    -The tool supports optional annotation merging and safe reordering of columns.

    -For large datasets, ensure enough memory is allocated to the Galaxy server.
