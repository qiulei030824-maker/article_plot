#!/bin/bash
# One-click run all figures
set -e

PROJECT="PF00168"
WORKDIR="/data5/qiulei/PPI/${PROJECT}/JCVI"
cd "${WORKDIR}"

echo "=== Step 4: LAST Pairwise Alignments ==="
python ../02_scripts/pipeline/step04_run_last_alignment.py

echo "=== Step 5: Convert anchors to .simple ==="
python ../02_scripts/pipeline/step05_convert_anchors.py ${PROJECT} ChineseLong DHL92 97103 Cpepo

echo "=== Step 6: Synteny filtering (minspan=30) ==="
for anchors in fig2A_${PROJECT}_*.simple; do
    name=${anchors%.simple}
    python -m jcvi.compara.synteny filter --minspan=30 --simple ${name}.anchors ${anchors}
done

echo "=== Figure 2A (8 species) ==="
python ../02_scripts/figure2A_cucurbits_8species.py

echo "=== Figure 2A (4 species, legacy) ==="
python ../02_scripts/figure2A_cucurbits.py

echo "=== Figures 2B-5 ==="
python ../02_scripts/figure2B_conservation.py
python ../02_scripts/figure3_microsynteny.py
Rscript ../02_scripts/figure4_copy_number.R
Rscript ../02_scripts/figure5_duplication.R

echo "=== All figures generated ==="
ls -lh ../03_figures/
