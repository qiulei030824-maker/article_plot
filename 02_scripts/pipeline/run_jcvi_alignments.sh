#!/bin/bash
# run_jcvi_alignments.sh — Batch LAST alignment for cucurbit synteny
# Usage: bash run_jcvi_alignments.sh

set -e

WORK_DIR="/data5/qiulei/pfam_pipeline/data/processed/PF00168_jcvi_chain"
cd "${WORK_DIR}"

echo "Working directory: ${WORK_DIR}"
echo ""

# Cucurbit chain
PAIRS=(
  "ChineseLong DHL92"
  "DHL92 97103"
  "97103 Cpepo"
)

for pair in "${PAIRS[@]}"; do
  read -r a b <<< "$pair"
  out_last="${a}.${b}.last"
  
  if [ -f "$out_last" ] && [ $(stat -c%s "$out_last") -gt 1000 ]; then
    echo "SKIP: ${out_last} exists ($(stat -c%s "$out_last") bytes)"
    continue
  fi
  
  echo "Running: ${a} vs ${b}..."
  python -m jcvi.compara.catalog ortholog \
    --dbtype prot --cscore 0.99 --no_strip_names --notex "$a" "$b"
  echo "DONE: ${a}.${b}"
done

echo ""
echo "Output files:"
ls -lh *.last 2>/dev/null || echo "No .last files"
echo ""
echo "All done."