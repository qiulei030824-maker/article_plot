#!/bin/bash
# SignalP5 补跑 — 修复版: 22种aphidbase蛷虫 (.faa.gz 实际为纯文本)
SIGNALP="$HOME/.local/signalp-5.0b/bin/signalp"
RAW="/data5/qiulei/coevolution/data/insect_genome/raw"
PROJ="/data5/qiulei/coevolution/hemiptera_effector_erc"
OUTDIR="$PROJ/data/effectors/signalp5_results"
LOG="$PROJ/logs/signalp5_batch3_fix.log"
MAX_JOBS=4

echo "Batch3 Fix Start: $(date)" | tee -a "$LOG"
cd "$PROJ"

SPECIES=(
  Acyrthosiphon_pisum_JIC Aphis_fabae Aphis_rumicis Aphis_thalictri
  Brachycaudus_helichrysi Brachycaudus_klugkisti Cinara_cedri
  Drepanosiphum_platanoidis Eriosoma_laniyerum Hamadryas_cornu
  Macrosiphum_euphorbiae Myzus_cerasi Myzus_varians Nasonovia_ribisnigri
  Neotoxoptera_formosana Pentalonia_nigronervosa Pseudoregma_acericola
  Sitobion_avenae Stomaphis_chinensis Therioaphis_trifolii
  Tuberocephalus_akinire Tuberolachnus_salignus
)

for sp in "${SPECIES[@]}"; do
  sp_out="$OUTDIR/$sp"
  mkdir -p "$sp_out"
  [ -f "$sp_out/done.flag" ] && echo "  SKIP $sp (already done)" | tee -a "$LOG" && continue

  faa=$(find "$RAW/aphid/$sp" -name "*.faa*" 2>/dev/null | head -1)
  [ -z "$faa" ] && echo "  NOFILE $sp" | tee -a "$LOG" && continue

  if gzip -t "$faa" 2>/dev/null; then
    gunzip -c "$faa" > "/tmp/${sp}.faa"
    echo "  $sp: is gzip, decompressed" | tee -a "$LOG"
  else
    cp "$faa" "/tmp/${sp}.faa"
    echo "  $sp: is plain text (pseudo .gz), copied directly" | tee -a "$LOG"
  fi

  seq_count=$(grep -c '^>' "/tmp/${sp}.faa")
  echo "  START $sp ($seq_count seqs, $(du -h /tmp/${sp}.faa | cut -f1))" | tee -a "$LOG"

  (
    export PATH="$HOME/.local/signalp-5.0b/bin:$PATH"
    signalp -fasta "/tmp/${sp}.faa" -format short -org euk -prefix "$sp_out/${sp}" 2>> "$LOG"
    smry="$sp_out/${sp}_summary.signalp5"
    if [ -f "$smry" ]; then
      hits=$(awk -F'\t' 'NR>1 && $3+0>0.5 {c++} END{print c+0}' "$smry")
      echo "  DONE $sp: ${hits} SP+ hits" | tee -a "$LOG"
      touch "$sp_out/done.flag"
    else
      echo "  FAIL $sp: no output" | tee -a "$LOG"
    fi
    rm -f "/tmp/${sp}.faa"
  ) &

  while [ "$(jobs -r | wc -l)" -ge "$MAX_JOBS" ]; do sleep 30; done
done

wait
echo "Batch3 End: $(date)" | tee -a "$LOG"

echo "" | tee -a "$LOG"
echo "=== Summary ===" | tee -a "$LOG"
total=0
for sp in "${SPECIES[@]}"; do
  f="$OUTDIR/$sp/${sp}_summary.signalp5"
  if [ -f "$f" ]; then
    hits=$(awk -F'\t' 'NR>1 && $3+0>0.5 {c++} END{print c+0}' "$f")
    echo "  $sp: $hits" | tee -a "$LOG"
    total=$((total+hits))
  fi
done
echo "Total SP+ candidates (new): $total" | tee -a "$LOG"
echo "Total species processed: $total" | tee -a "$LOG"