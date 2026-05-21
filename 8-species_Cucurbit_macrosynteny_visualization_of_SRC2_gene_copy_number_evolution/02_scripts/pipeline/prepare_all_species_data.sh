#!/bin/bash
# Prepare BED and CDS files for all 22 species (6 groups)
set -e

BASE="/data5/qiulei/PPI"

# Group 1: Cucurbits (8 core)
for sp in ChineseLong DHL92 97103 USVL1VR-Ls Cpepo Cargyrosperma Cmaxima_Rimu Cmoschata_Rifu; do
    gff3="$BASE/data/$sp/$sp.gff3"
    bed="$BASE/PF00168/JCVI/$sp.bed"
    [ -f "$gff3" ] || continue
    python step06_generate_bed.py PF00168 "$sp"
done

echo "All BED files generated."
echo "Run fix_cds_ids.py next."
