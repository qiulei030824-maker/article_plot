#!/usr/bin/env python3
"""Step 4: Run LAST pairwise alignment for synteny detection.

Usage: python step04_run_last_alignment.py <pfam_id> <species_1> <species_2> ...

This script runs jcvi.compara.catalog ortholog for each consecutive pair
of species in the provided list. It skips pairs where a .last file already exists.
"""
import os,sys,subprocess,shutil,glob,multiprocessing,argparse
from pathlib import Path
MAX_WORKERS = min(multiprocessing.cpu_count(),12)

PFAM_ID = sys.argv[1] if len(sys.argv)>1 else "PF00168"
SPECIES  = sys.argv[2:] if len(sys.argv)>2 else []

results_dir = Path(f"/data5/qiulei/pfam_pipeline/data/processed/{PFAM_ID}_jcvi_chain")
os.makedirs(results_dir, exist_ok=True)
os.chdir(results_dir)

def run_pair(args):
    a,b = args
    out_last = f"{a}.{b}.last"
    print(f"Checkpoint: processing {a} vs {b}...")
    if os.path.exists(out_last) and os.path.getsize(out_last) > 1000:
        print(f"  SKIP: {out_last} already exists ({os.path.getsize(out_last)} bytes)")
        return
    print(f"  Starting {a}.{b} LAST alignment...")
    cmd = ["python","-m","jcvi.compara.catalog","ortholog",
           "--dbtype","prot","--cscore","0.99","--no_strip_names","--notex",a,b]
    subprocess.run(cmd, check=True, capture_output=False, timeout=7200)
    print(f"  DONE: {a}.{b}")

if __name__ == "__main__":
    from itertools import pairwise
    pairs = list(pairwise(SPECIES))
    print(f"Species: {SPECIES}")
    print(f"Pairs: {pairs}")
    for p in pairs:
        run_pair(p)
    print("All done.")