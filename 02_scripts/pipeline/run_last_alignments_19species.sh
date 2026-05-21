#!/bin/bash
# run_last_alignments_19species.sh — LAST alignment for 19 species

set -e

WORK_DIR="/data5/qiulei/pfam_pipeline/data/processed/PF00168_jcvi_chain"
cd "${WORK_DIR}"

PAIRS=(
  "ChineseLong DHL92"
  "DHL92 97103"
  "97103 Cpepo"
  "Cpepo arabidopsis_thaliana"
  "arabidopsis_thaliana solanum_lycopersicum"
  "solanum_lycopersicum oryza_sativa"
  "oryza_sativa amborella_trichopoda"
)

for pair in "${PAIRS[@]}"; do
  read -r a b <<< "$pair"
  out_last="${a}.${b}.last"
  if [ -f "$out_last" ] && [ $(stat -c%s "$out_last") -gt 1000 ]; then
    echo "SKIP: ${out_last}"
    continue
  fi
  echo "Running: ${a} vs ${b}..."
  python -m jcvi.compara.catalog ortholog \
    --dbtype prot --cscore 0.99 --no_strip_names --notex "$a" "$b"
  echo "DONE: ${a}.${b}"
done

echo "All done."