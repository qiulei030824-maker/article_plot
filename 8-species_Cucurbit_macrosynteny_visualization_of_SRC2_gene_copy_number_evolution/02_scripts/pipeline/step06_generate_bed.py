#!/usr/bin/env python3
"""
Step 6: Generate BED files from GFF3 for JCVI synteny analysis.
"""
import os, sys, re
from collections import defaultdict

BED_TEMPLATE = "{chrom}\t{start}\t{end}\t{id}\t0\t{strand}\n"

def gff3_to_bed(gff3, bed_out, feature_type="gene"):
    """Extract gene features from GFF3 and output BED format."""
    with open(gff3) as f, open(bed_out,'w') as out:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split('\t')
            if len(parts) < 9:
                continue
            if parts[2] != feature_type:
                continue
            chrom, src, feat, start, end, score, strand, frame, attr = parts
            
            # Extract gene ID
            m = re.search(r'ID=([^;]+)', attr)
            if not m:
                m = re.search(r'gene_id=([^;]+)', attr)
            if not m:
                continue
            gene_id = m.group(1)
            
            start, end = int(start), int(end)
            if start > end:
                start, end = end, start
            
            out.write(BED_TEMPLATE.format(chrom=chrom, start=start-1, end=end, id=gene_id, strand=strand))
    print(f"[OK] {gff3} -> {bed_out}")

def generate_seqids(species_list, bed_dir, seqids_file):
    """Collect chromosome IDs from BED files."""
    chroms = []
    for sp in species_list:
        bed = os.path.join(bed_dir, f"{sp}.bed")
        if not os.path.exists(bed):
            continue
        seen = set()
        with open(bed) as f:
            for line in f:
                chrom = line.split('\t')[0]
                if chrom not in seen:
                    seen.add(chrom)
                    chroms.append(chrom)
    with open(seqids_file,'w') as out:
        out.write('\n'.join(chroms)+'\n')
    print(f"[OK] {seqids_file}: {len(chroms)} chromosomes")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: step06_generate_bed.py PFAM_ID sp1 sp2 ...")
        sys.exit(1)
    
    pfam_id = sys.argv[1]
    species = sys.argv[2:]
    
    base = "/data5/qiulei/PPI"
    jcvi_dir = os.path.join(base, pfam_id, "JCVI")
    data_dir = os.path.join(base, "data")
    os.makedirs(jcvi_dir, exist_ok=True)
    
    for sp in species:
        sp_dir = os.path.join(data_dir, sp)
        gff3 = os.path.join(sp_dir, f"{sp}.gff3")
        bed = os.path.join(jcvi_dir, f"{sp}.bed")
        if os.path.exists(gff3):
            gff3_to_bed(gff3, bed)
        else:
            print(f"[SKIP] {gff3} not found")
    
    seqids = os.path.join(jcvi_dir, "seqids_fig2A.txt")
    generate_seqids(species, jcvi_dir, seqids)
