#!/usr/bin/env python3
"""Fix CDS IDs: remove .1 version suffix from cucurbit CDS FASTA files.

Some species (Cpepo, DHL92, 97103, ChineseLong) have CDS entries with .1 suffixes
that don't match the gene IDs in GFF3/BED files. This script strips the suffix.

Usage: python fix_cds_ids.py
"""
import os, glob
from pathlib import Path

def fix_cds_fasta(species, cds_dir):
    """Remove .1 suffix from sequence IDs in a CDS FASTA file."""
    cds_file = cds_dir / f"{species}.cds"
    if not cds_file.exists():
        print(f"  SKIP: {cds_file} not found")
        return 0, 0
    
    out_file = cds_dir / f"{species}.cds.fixed"
    total, fixed = 0, 0
    with open(cds_file) as fin, open(out_file, "w") as fout:
        for line in fin:
            if line.startswith(">"):
                total += 1
                header = line.strip()
                if ".1" in header:
                    header = header.replace(".1", "", 1)
                    fixed += 1
                fout.write(header + "\n")
            else:
                fout.write(line)
    
    # Replace original with fixed
    os.replace(out_file, cds_file)
    return total, fixed

if __name__ == "__main__":
    cds_dir = Path("/data5/qiulei/pfam_pipeline/data/processed/PF00168_jcvi_chain")
    cucurbit_species = ["ChineseLong", "DHL92", "97103", "Cpepo"]
    
    for sp in cucurbit_species:
        total, fixed = fix_cds_fasta(sp, cds_dir)
        if total > 0:
            print(f"{sp}: {total} seqs written ({fixed} had .1 stripped)")
    
    print("Done.")