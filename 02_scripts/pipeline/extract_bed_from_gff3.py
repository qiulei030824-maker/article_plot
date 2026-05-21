#!/usr/bin/env python3
"""Smart GFF3 parser that extracts gene coordinates as BED format.

Handles multiple GFF3 annotation styles:
  - Standard 'gene' features with 'ID=' attribute
  - mRNA features with 'Parent=' attribute
  - ID formats with suffixes: gene:XXX, mRNA:XXX, CDS:XXX
  - Automatically identifies main chromosomes vs scaffolds
"""
import os, sys, re, gzip
from collections import defaultdict
from pathlib import Path

CHROMOSOME_PATTERNS = [
    re.compile(r'^(chr|Chr|chromosome|Chromosome)[0-9]+'),
    re.compile(r'^[0-9]+$'),
    re.compile(r'^(LG|Chr|chr|NC_|CM_|AC_|AE_|CP_)[A-Za-z0-9_.]+'),
]

def is_main_chromosome(name):
    for pat in CHROMOSOME_PATTERNS:
        if pat.match(name):
            return True
    return False

def parse_gff3(gff3_path, gene_prefixes=None):
    """Parse GFF3 and extract gene/mRNA coordinates."""
    if gene_prefixes is None:
        gene_prefixes = ["gene:", "mRNA:", "CDS:", "transcript:", "", "rna-"]
    
    genes = []
    open_fn = gzip.open if str(gff3_path).endswith('.gz') else open
    mode = 'rt' if str(gff3_path).endswith('.gz') else 'r'
    
    with open_fn(gff3_path, mode) as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split('\t')
            if len(parts) < 9:
                continue
            chrom, source, feature, start, end, score, strand, phase, attrs = parts[:9]
            
            if feature not in ['gene', 'mRNA', 'transcript', 'CDS', 'exon', 'pseudogene']:
                continue
            
            # Parse ID from attributes
            attr_dict = {}
            for attr in attrs.split(';'):
                attr = attr.strip()
                if '=' in attr:
                    k, v = attr.split('=', 1)
                    attr_dict[k] = v
            
            gene_id = None
            if 'ID' in attr_dict:
                gene_id = attr_dict['ID']
            elif 'Parent' in attr_dict:
                parent = attr_dict['Parent']
                # Try to extract gene ID from Parent
                for prefix in gene_prefixes:
                    if parent.startswith(prefix):
                        gene_id = parent
                        break
            elif 'Name' in attr_dict and feature == 'gene':
                gene_id = attr_dict['Name']
            
            if gene_id and feature in ['gene', 'mRNA', 'transcript']:
                genes.append({
                    'chrom': chrom,
                    'start': int(start),
                    'end': int(end),
                    'strand': strand,
                    'id': gene_id,
                    'feature': feature,
                })
    
    return genes

def write_bed(genes, output_path, main_chromosomes_only=True):
    """Write genes in 6-column BED format."""
    if main_chromosomes_only:
        genes = [g for g in genes if is_main_chromosome(g['chrom'])]
    
    # Sort by chrom, then start
    genes.sort(key=lambda x: (x['chrom'], x['start']))
    
    # Deduplicate by ID (keep first occurrence)
    seen_ids = set()
    unique_genes = []
    for g in genes:
        if g['id'] not in seen_ids:
            seen_ids.add(g['id'])
            unique_genes.append(g)
    
    with open(output_path, 'w') as f:
        for g in unique_genes:
            f.write(f"{g['chrom']}\t{g['id']}\t{g['start']}\t{g['end']}\t.\t{g['strand']}\n")
    
    n_scaffold = len(genes) - len(unique_genes)
    return len(unique_genes), n_scaffold

def main():
    if len(sys.argv) < 3:
        print("Usage: python extract_bed_from_gff3.py <gff3_path> <output_bed>")
        sys.exit(1)
    
    gff3_path = sys.argv[1]
    output_bed = sys.argv[2]
    
    if not os.path.exists(gff3_path):
        print(f"Error: {gff3_path} not found")
        sys.exit(1)
    
    genes = parse_gff3(gff3_path)
    unique, dedup = write_bed(genes, output_bed)
    print(f"Written {unique} unique genes to {output_bed} ({dedup} duplicate IDs skipped)")

if __name__ == "__main__":
    main()