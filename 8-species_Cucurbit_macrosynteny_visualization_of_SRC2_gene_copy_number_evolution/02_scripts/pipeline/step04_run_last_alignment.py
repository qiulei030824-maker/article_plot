#!/usr/bin/env python3
"""
Step 4: Run LAST pairwise alignment via JCVI for PF00168 synteny analysis.
"""
import subprocess, os, sys

PROJECT = "PF00168"
WORKDIR = f"/data5/qiulei/PPI/{PROJECT}/JCVI"
os.chdir(WORKDIR)

# Alignment pairs (chain order)
PAIRS = [
    ("ChineseLong","DHL92"),
    ("DHL92","97103"),
    ("97103","USVL1VR-Ls"),
    ("USVL1VR-Ls","Cpepo"),
    ("Cpepo","Cargyrosperma"),
    ("Cargyrosperma","Cmaxima_Rimu"),
    ("Cmaxima_Rimu","Cmoschata_Rifu"),
]

for sp1, sp2 in PAIRS:
    anchors = f"{PROJECT}_{sp1}_{sp2}.anchors"
    if os.path.exists(anchors):
        print(f"[SKIP] {anchors} exists")
        continue
    cmd = f"python -m jcvi.compara.catalog ortholog --dbtype prot --cscore 0.99 --no_strip_names --notex {sp1} {sp2}"
    print(f"[RUN] {cmd}")
    subprocess.run(cmd, shell=True, check=True)
