#!/usr/bin/env python3
"""Step 6: Generate BED files from GFF3 annotations and create seqids.

Usage: python step06_generate_bed.py <pfam_id> <species_1> <species_2> ...

Generates:
  - {species}.bed (6-column JCVI BED format)
  - seqids.txt (chromosome list for all species)
"""
import os,sys,glob,copy
from pathlib import Path

PFAM_ID = sys.argv[1] if len(sys.argv)>1 else "PF00168"
SPECIES  = sys.argv[2:] if len(sys.argv)>2 else []

DATA_DIR     = "/data5/qiulei/PPI/data"
results_dir  = Path(f"/data5/qiulei/pfam_pipeline/data/processed/{PFAM_ID}_jcvi_chain")
os.makedirs(results_dir, exist_ok=True)
os.chdir(results_dir)

def generate_bed(species_name):
    bed_out = f"{species_name}.bed"
    if os.path.exists(bed_out) and os.path.getsize(bed_out) > 100:
        print(f"  SKIP: {bed_out} already exists ({os.path.getsize(bed_out)} bytes)")
        return
    
    # Find GFF3 file
    species_dir = Path(DATA_DIR) / species_name
    gff3_files = list(species_dir.glob("*.gff3")) + list(species_dir.glob("*.gff")) \
               + list(species_dir.glob("*.GFF3")) + list(species_dir.glob("*.GFF")) \
               + list(species_dir.glob("genomic.gff")) + list(species_dir.glob("genomic.gff3"))
    
    if not gff3_files:
        print(f"  WARNING: No GFF3 found for {species_name} at {species_dir}")
        return
    
    gff3_file = gff3_files[0]
    print(f"  Generating BED for {species_name} from {gff3_file.name}")
    
    # Use JCVI to convert GFF3 to BED
    import subprocess
    cmd = ["python", "-m", "jcvi.formats.gff", "--type=mRNA", "--primary_key=Parent",
           "-o", bed_out, str(gff3_file)]
    subprocess.run(cmd, check=True, capture_output=True)
    
    if os.path.exists(bed_out):
        print(f"    {bed_out}: {os.path.getsize(bed_out)} bytes")
    return bed_out

def generate_seqids():
    bed_files = sorted(glob.glob("*.bed"))
    seqids_content = []
    for bed_file in bed_files:
        species_name = bed_file.replace(".bed", "")
        chromosomes = set()
        with open(bed_file) as f:
            for line in f:
                chrom = line.split("\t")[0].strip()
                if chrom:
                    chromosomes.add(chrom)
        ordered = sorted(chromosomes, key=lambda x: (len(x), x))
        seqids_content.append(f"{species_name}:{",".join(ordered)}")
    
    with open("seqids.txt", "w") as f:
        f.write("\n".join(seqids_content) + "\n")
    print(f"  seqids.txt: {len(seqids_content)} species written")

if __name__ == "__main__":
    for sp in SPECIES:
        generate_bed(sp)
    generate_seqids()
    print("Done.")