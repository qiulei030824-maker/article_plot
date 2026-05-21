#!/bin/bash
# run_last_parallel.sh — Parallel LAST alignment using GNU parallel
# Usage: bash run_last_parallel.sh

set -e

WORK_DIR="/data5/qiulei/pfam_pipeline/data/processed/PF00168_jcvi_chain"
cd "${WORK_DIR}"

PAIRS=(
  "ChineseLong DHL92"
  "DHL92 97103"
  "97103 USVL1VR-Ls"
  "USVL1VR-Ls Cpepo"
  "Cpepo Cargyrosperma"
  "Cargyrosperma Cmaxima_Rimu"
  "Cmaxima_Rimu Cmoschata_Rifu"
)

run_pair() {
  local a="$1" b="$2"
  local out_last="${a}.${b}.last"
  if [ -f "$out_last" ] && [ $(stat -c%s "$out_last") -gt 1000 ]; then
    echo "SKIP: ${out_last} exists ($(stat -c%s "$out_last") bytes)"
    return 0
  fi
  echo "Running: ${a} vs ${b}..."
  python -m jcvi.compara.catalog ortholog \
    --dbtype prot --cscore 0.99 --no_strip_names --notex "$a" "$b"
  echo "DONE: ${a}.${b}"
}

export -f run_pair

parallel -j 6 run_pair ::: $(for p in "${PAIRS[@]}"; do echo $p; done)

echo ""
echo "All done."