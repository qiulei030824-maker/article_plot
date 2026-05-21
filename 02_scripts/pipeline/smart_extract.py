#!/usr/bin/env python3
"""Smart extractor: Extract pep/cds sequences from genome files.

Handles:
  - GFF3 + genome FASTA → CDS extraction
  - Direct PEP/CDS file copying
  - Various genome annotation formats
"""
import os, sys, shutil, subprocess, gzip
from pathlib import Path

DATA_DIR = Path("/data5/qiulei/PPI/data")

def find_genome_file(species_dir):
    """Find genome FASTA file in species directory."""
    patterns = ["*.fa", "*.fasta", "*.fna", "genomic.fna", "genomic.fa"]
    for pat in patterns:
        files = list(species_dir.glob(pat))
        if files:
            return files[0]
    return None

def extract_cds_from_gff(species, gff_file, genome_file, output_cds):
    """Extract CDS sequences using gffread."""
    cmd = ["gffread", "-x", str(output_cds), "-g", str(genome_file), str(gff_file)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0 and output_cds.exists():
        return True
    return False

def main():
    species_list = sys.argv[1:] if len(sys.argv) > 1 else []
    if not species_list:
        print("Usage: python smart_extract.py <species1> <species2> ...")
        print("Available species:")
        for d in sorted(DATA_DIR.iterdir()):
            if d.is_dir():
                print(f"  - {d.name}")
        sys.exit(1)
    
    for sp in species_list:
        sp_dir = DATA_DIR / sp
        if not sp_dir.exists():
            print(f"SKIP: {sp} directory not found")
            continue
        
        # Look for pre-extracted files
        pep_files = list(sp_dir.glob("*.pep"))
        cds_files = list(sp_dir.glob("*.cds"))
        gff_files = list(sp_dir.glob("*.gff*"))
        genome_file = find_genome_file(sp_dir)
        
        print(f"\n{sp}:")
        print(f"  PEP files: {[f.name for f in pep_files]}")
        print(f"  CDS files: {[f.name for f in cds_files]}")
        print(f"  GFF files: {[f.name for f in gff_files]}")
        print(f"  Genome: {genome_file.name if genome_file else 'NOT FOUND'}")

if __name__ == "__main__":
    main()