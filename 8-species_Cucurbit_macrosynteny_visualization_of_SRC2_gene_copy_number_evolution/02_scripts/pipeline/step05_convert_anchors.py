#!/usr/bin/env python3
"""
Step 5: Convert JCVI anchors to .simple format for synteny visualization.
"""
import os, sys

def convert_anchors(pfam_id, species_list):
    workdir = f"/data5/qiulei/PPI/{pfam_id}/JCVI"
    os.chdir(workdir)
    
    for i in range(len(species_list)-1):
        sp1, sp2 = species_list[i], species_list[i+1]
        anchors = f"{pfam_id}_{sp1}_{sp2}.anchors"
        simple_out = f"fig2A_{pfam_id}_{sp1}_{sp2}.filtered.simple"
        
        if not os.path.exists(anchors):
            print(f"[SKIP] {anchors} not found")
            continue
        
        # anchors format: sp1_gene sp2_gene orientation value
        # .simple format: sp1_chrom sp1_start sp1_end sp2_chrom sp2_start sp2_end orientation sp1_gene sp2_gene
        with open(anchors) as f, open(simple_out,'w') as out:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 3:
                    continue
                g1, g2, orient = parts[0], parts[1], parts[2]
                out.write(f"\t\t\t\t\t\t{orient}\t{g1}\t{g2}\n")
        print(f"[OK] {anchors} -> {simple_out}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: step05_convert_anchors.py PFAM_ID sp1 sp2 sp3 ...")
        sys.exit(1)
    convert_anchors(sys.argv[1], sys.argv[2:])
