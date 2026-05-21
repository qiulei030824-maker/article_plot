#!/bin/bash
# SignalP5 批量运行 — 26种昆虫，8并行
set -euo pipefail

SIGNALP="$HOME/.local/signalp-5.0b/bin/signalp"
RAW="/data5/qiulei/coevolution/data/insect_genome/raw"
PROJ="/data5/qiulei/coevolution/hemiptera_effector_erc"
OUTDIR="$PROJ/data/effectors/signalp5_results"
MERGED="$PROJ/data/effectors/all_candidates_signalp5.fa"
LOG="$PROJ/logs/signalp5_batch.log"
MAX_JOBS=8
mkdir -p "$OUTDIR"
echo "Start: $(date)" > "$LOG"

# 收集所有蛋白文件
FILES=()
while IFS= read -r f; do FILES+=("$f"); done < <(find "$RAW" -name "*_protein.faa.gz" 2>/dev/null)

for f in "${FILES[@]}"; do
    species=$(basename "$(dirname "$f")")
    sp_out="$OUTDIR/$species"
    mkdir -p "$sp_out"
    
    [ -f "$sp_out/done.flag" ] && echo "  SKIP $species" >> "$LOG" && continue
    
    echo "  START $species ($(basename "$f"))" >> "$LOG"
    gunzip -c "$f" > "/tmp/${species}.faa"
    
    (
        export PATH="$HOME/.local/signalp-5.0b/bin:$PATH"
        signalp -fasta "/tmp/${species}.faa" -format short -org euk -prefix "$sp_out/${species}" 2>> "$LOG"
        
        smry="$sp_out/${species}_summary.signalp5"
        if [ -f "$smry" ]; then
            awk -F'\t' 'NR>1 && $2=="YES" {print $1}' "$smry" > "$sp_out/${species}_hits.txt"
            echo "  DONE $species: $(wc -l < "$sp_out/${species}_hits.txt") hits" >> "$LOG"
            touch "$sp_out/done.flag"
        else
            echo "  FAIL $species: no summary" >> "$LOG"
        fi
        rm -f "/tmp/${species}.faa"
    ) &
    
    while [ "$(jobs -r | wc -l)" -ge "$MAX_JOBS" ]; do sleep 5; done
done
wait

# 合并
echo "=== Merging ===" >> "$LOG"
> "$MERGED"
total=0
for f in "${FILES[@]}"; do
    species=$(basename "$(dirname "$f")")
    hits="$OUTDIR/$species/${species}_hits.txt"
    [ ! -f "$hits" ] && continue
    
    faatmp="/tmp/${species}_extract.faa"
    gunzip -c "$f" > "$faatmp"
    n=0
    while IFS= read -r id; do
        seqkit grep -p "$id" "$faatmp" >> "$MERGED" 2>/dev/null && n=$((n+1)) || true
    done < "$hits"
    rm -f "$faatmp"
    total=$((total+n))
    echo "  $species: $n" >> "$LOG"
done
echo "Total: $total candidates" >> "$LOG"
echo "End: $(date)" >> "$LOG"