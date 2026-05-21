#!/usr/bin/env python3
"""
Fix CDS IDs: remove .1 version suffix from cucurbit CDS FASTA headers.
"""
import os, re

def fix_fasta_ids(fasta):
    """Remove trailing .1 from FASTA headers."""
    if not os.path.exists(fasta):
        return
    out = fasta + ".fixed"
    with open(fasta) as f, open(out,'w') as outfile:
        for line in f:
            if line.startswith('>'):
                header = line.strip()
                # Remove .1 suffix but keep _1 suffixes
                header = re.sub(r'\.1(?=[\s>]|$)', '', header)
                outfile.write(header + '\n')
            else:
                outfile.write(line)
    os.replace(out, fasta)
    print(f"[FIXED] {fasta}")

if __name__ == "__main__":
    base = "/data5/qiulei/PPI"
    for sp in ["ChineseLong","DHL92","97103","Cpepo"]:
        cds = os.path.join(base, "data", sp, f"{sp}.cds.fa")
        fix_fasta_ids(cds)
