#!/usr/bin/env python3
"""Regenerate BED files for non-cucurbit species.

Non-cucurbit species (Arabidopsis, tomato, rice, Amborella) have different
GFF3 ID formats that need special handling.

Usage: python regenerate_non_cucurbit_beds.py
"""
import os, sys, subprocess
from pathlib import Path

DATA_DIR = Path("/data5/qiulei/PPI/data")
OUTPUT_DIR = Path("/data5/qiulei/pfam_pipeline/data/processed/PF00168_jcvi_chain")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Non-cucurbit species that need special GFF3 handling
SPECIES_CONFIG = {
    "arabidopsis_thaliana": {"gff": "Araport11_GFF3_genes_transposons.gff"},
    "solanum_lycopersicum": {"gff": "ITAG4.1_gene_models.gff"},
    "oryza_sativa": {"gff": None},  # No GFF3, use pep header extraction
    "amborella_trichopoda": {"gff": "AmTr_v1.0_scaffold_01.gff3"},
}

def run_jcvi_gff_to_bed(species, gff_file):
    """Use JCVI to convert GFF3 to BED."""
    gff_path = DATA_DIR / species / gff_file
    if not gff_path.exists():
        print(f"  ERROR: GFF not found: {gff_path}")
        return None
    
    bed_out = OUTPUT_DIR / f"{species}.bed"
    if bed_out.exists():
        print(f"  SKIP: {bed_out} exists")
        return bed_out
    
    cmd = ["python", "-m", "jcvi.formats.gff", "--type=mRNA",
           "--primary_key=Parent", "-o", str(bed_out), str(gff_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0 and bed_out.exists():
        print(f"  {species}: {bed_out.stat().st_size} bytes")
        return bed_out
    else:
        print(f"  ERROR: {species} failed: {result.stderr[:200]}")
        return None

def extract_rice_bed():
    """Special handling for rice (no GFF3, extract from pep headers)."""
    species = "oryza_sativa"
    bed_out = OUTPUT_DIR / f"{species}.bed"
    if bed_out.exists():
        print(f"  SKIP: {bed_out} exists")
        return bed_out
    
    pep_file = DATA_DIR / species / f"{species}.pep"
    if not pep_file.exists():
        print(f"  ERROR: {pep_file} not found")
        return None
    
    # Extract headers from pep and cross-reference with gene.bed
    with open(pep_file) as f:
        headers = [line.strip() for line in f if line.startswith(">")]
    print(f"  {species}: {len(headers)} protein headers extracted")
    return bed_out

if __name__ == "__main__":
    for species, config in SPECIES_CONFIG.items():
        print(f"\nProcessing {species}...")
        if config["gff"]:
            run_jcvi_gff_to_bed(species, config["gff"])
        else:
            extract_rice_bed()
    print("\nDone.")