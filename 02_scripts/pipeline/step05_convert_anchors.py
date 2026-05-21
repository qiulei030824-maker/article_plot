#!/usr/bin/env python3
"""Step 5: Convert LAST anchors to JCVI SimpleFile format.

Usage: python step05_convert_anchors.py <pfam_id> <species_1> <species_2> ...

Reads A.B.anchors (2-column gene pairs) and A.B.last.filtered (LAST scores)
and produces A.B.simple (6-column JCVI SimpleFile).
"""
import os,sys,glob,re
from pathlib import Path

PFAM_ID = sys.argv[1] if len(sys.argv)>1 else "PF00168"
SPECIES  = sys.argv[2:] if len(sys.argv)>2 else []

results_dir = Path(f"/data5/qiulei/pfam_pipeline/data/processed/{PFAM_ID}_jcvi_chain")
os.chdir(results_dir)

def parse_last_filtered(fname):
    scores = {}
    with open(fname) as f:
        for line in f:
            if line.startswith("#"): continue
            parts = line.strip().split()
            if len(parts) >= 12:
                a = parts[0]
                b = parts[1]
                score = parts[11]
                scores[(a,b)] = score
    return scores

def parse_anchors(fname):
    pairs = []
    with open(fname) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                pairs.append((parts[0], parts[1]))
    return pairs

def convert(anchor_a, anchor_b):
    print(f"\nProcessing {anchor_a} vs {anchor_b}...")
    last_filtered = f"{anchor_a}.{anchor_b}.last.filtered"
    anchors_file = f"{anchor_a}.{anchor_b}.anchors"
    out_simple = f"{anchor_a}.{anchor_b}.simple"
    
    if not os.path.exists(anchors_file):
        print(f"  SKIP: {anchors_file} not found")
        return
    
    scores = {}
    if os.path.exists(last_filtered):
        scores = parse_last_filtered(last_filtered)
        print(f"  Loaded {len(scores)} scores from {last_filtered}")
    
    pairs = parse_anchors(anchors_file)
    print(f"  Loaded {len(pairs)} anchor pairs from {anchors_file}")
    
    count = 0
    with open(out_simple, "w") as f:
        for ga, gb in pairs:
            score = scores.get((ga,gb), "100")
            f.write(f"{ga}\t{ga}\t{gb}\t{gb}\t{score}\t+\n")
            count += 1
    print(f"  Written {count} lines to {out_simple}")

if __name__ == "__main__":
    from itertools import pairwise
    pairs = list(pairwise(SPECIES))
    for a,b in pairs:
        convert(a,b)
    print("\nAll done.")