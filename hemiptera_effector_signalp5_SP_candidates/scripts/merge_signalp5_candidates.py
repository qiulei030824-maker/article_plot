#!/usr/bin/env python3
"""
Merge SignalP5 SP+ candidates from all 48 species into one FASTA.
Uses insect_local_status.tsv as authoritative FASTA path source.
For batch1 (NCBI) species: uses *_protein.faa.gz (RefSeq IDs).
For batch3 (aphidbase) species: uses whatever file SignalP5 found.
"""
import os, sys, gzip, shutil
from pathlib import Path

PROJ = Path("/data5/qiulei/coevolution/hemiptera_effector_erc")
RAW = Path("/data5/qiulei/coevolution/data/insect_genome/raw")
OUTDIR = PROJ / "data/effectors/signalp5_results"
MERGED = PROJ / "data/effectors" / "all_candidates_signalp5.fa"
LOG = PROJ / "logs" / "merge_signalp5_candidates.log"
STATUS_TSV = PROJ / "data" / "insect_local_status.tsv"

log_file = open(LOG, "w")
def log(msg):
    print(msg)
    log_file.write(msg + "\n")
    log_file.flush()

log("=== Merge SignalP5 Candidates (48 species, v3 - fixed gzip detection) ===")
log(f"Start: {__import__('datetime').datetime.now()}")

# --- Parse insect_local_status.tsv for species → protein_file mapping ---
species_faa = {}
with open(STATUS_TSV) as f:
    for i, line in enumerate(f):
        if i == 0:
            continue
        parts = line.strip().split("\t")
        if len(parts) < 8:
            continue
        sp = parts[0]
        protein_col = parts[7].strip()
        if protein_col:
            species_faa[sp] = [p.strip() for p in protein_col.split(";") if p.strip()]

total_seqs = 0
species_count = 0

with open(MERGED, "w") as fout:
    for sp_dir in sorted(OUTDIR.iterdir()):
        if not sp_dir.is_dir():
            continue
        sp = sp_dir.name

        smry = sp_dir / f"{sp}_summary.signalp5"
        if not smry.exists():
            log(f"  \u23ed {sp}: no summary file")
            continue

        ids = set()
        with open(smry) as f:
            for line in f:
                if line.startswith("#"):
                    continue
                parts = line.strip().split("\t")
                if len(parts) >= 4:
                    try:
                        score = float(parts[2])
                        if score > 0.5:
                            ids.add(parts[0])
                    except ValueError:
                        pass

        if not ids:
            log(f"  \u23ed {sp}: 0 SP+ hits in summary")
            continue

        faa_file = None
        candidate_paths = species_faa.get(sp, [])

        if candidate_paths:
            for p in candidate_paths:
                pp = Path(p)
                if pp.name.endswith("_protein.faa.gz") and pp.exists() and pp.stat().st_size > 1000:
                    faa_file = pp
                    break
            if not faa_file:
                for p in candidate_paths:
                    pp = Path(p)
                    if pp.exists() and pp.stat().st_size > 1000:
                        faa_file = pp
                        break

        if not faa_file:
            globs = list(RAW.rglob(f"*/{sp}/*_protein.faa.gz"))
            for g in globs:
                if g.is_file() and g.stat().st_size > 1000:
                    faa_file = g
                    break

        if not faa_file:
            log(f"  \u274c {sp}: protein FASTA not found")
            continue

        tmp = Path(f"/tmp/{sp}_extract.fa")
        try:
            with open(faa_file, "rb") as fin:
                magic = fin.read(2)
            is_gzip = magic == b'\x1f\x8b'

            if is_gzip:
                with gzip.open(faa_file, "rt", errors='replace') as fin:
                    with open(tmp, "w") as fout_tmp:
                        shutil.copyfileobj(fin, fout_tmp)
            else:
                with open(faa_file, "r", errors='replace') as fin:
                    with open(tmp, "w") as fout_tmp:
                        shutil.copyfileobj(fin, fout_tmp)

            n = 0
            seqs = {}
            current_id = None
            current_seq = []
            capture = False
            with open(tmp) as fin:
                for line in fin:
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith(">"):
                        if current_id and capture:
                            seqs[current_id] = "".join(current_seq)
                            n += 1
                        parts = line[1:].split()
                        if not parts:
                            continue
                        current_id = parts[0]
                        current_seq = []
                        capture = current_id in ids
                    elif capture:
                        current_seq.append(line)
                if current_id and capture:
                    seqs[current_id] = "".join(current_seq)
                    n += 1

            for sid, sseq in seqs.items():
                fout.write(f">{sp}|{sid}\n{sseq}\n")

            total_seqs += n
            species_count += 1
            log(f"  \u2705 {sp}: {n} seqs extracted from {faa_file.name}")
        finally:
            if tmp.exists():
                tmp.unlink()

log(f"\n{'='*60}")
log(f"Merged: {MERGED}")
log(f"Species: {species_count}")
log(f"Total SP+ candidates: {total_seqs}")
log(f"End: {__import__('datetime').datetime.now()}")
log_file.close()