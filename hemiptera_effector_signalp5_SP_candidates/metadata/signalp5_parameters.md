# SignalP5.0 Run Parameters

## Core Command

```
signalp -fasta <input.faa> -format short -org euk -prefix <output_prefix>
```

## Parameter Details

| Parameter | Value | Description |
|-----------|-------|-------------|
| `-fasta` | `<input.faa>` | Input protein sequences in FASTA format |
| `-format` | `short` | Tabular output (one line per sequence) |
| `-org` | `euk` | Eukaryote organism group |
| `-prefix` | `<outdir>/<species>` | Output file prefix |

## Output Files

| File | Description |
|------|-------------|
| `<prefix>_summary.signalp5` | Main prediction results table (tab-separated) |
| `<prefix>_output.gff3` | GFF3 format output (not used) |
| `<prefix>_processed_entries.fasta` | FASTA with signal peptide removed (not used) |

## Summary File Format

```
# Header line (tab-separated columns):
# ID    Prediction    SP(Sec/SPI)    OTHER    CS Position

# ID:           Sequence identifier
# Prediction:   Prediction class (SP(Sec/SPI) / OTHER / TAT / Sec/SPII / LIPO / TATLIPO)
# SP(Sec/SPI):  Signal Peptide score (0-1)
# OTHER:        Non-secreted score (0-1)
# CS Position:  Cleavage site position (for SP predictions)
```

## SP⁺ Filtering Criteria

Two formats were used depending on SignalP5 version:

1. **Standard format** (most species): Column 2 == "YES" indicates SP prediction
2. **Score-based format** (batch 2/3): Column 3 (SP score) > 0.5

### NCBI RefSeq Species (Batch 1)
```
awk -F'\t' 'NR>1 && $2=="YES" {print $1}' <summary>
```

### AphidBase Species (Batch 2 & 3)
```
awk -F'\t' 'NR>1 && $3+0>0.5 {c++} END{print c+0}' <summary>
```

## File Size Dependence

SignalP5 requires sufficient input for accurate prediction. Minimum protein file size threshold: >1000 bytes. Files below this threshold are skipped.

## Parallel Execution

- **Batch 1 & 2**: MAX_JOBS=8
- **Batch 3 (fix)**: MAX_JOBS=4 (reduced due to mixed format complexity)
- Job management: Bash job control (`jobs -r | wc -l`)
- Output directory: `data/effectors/signalp5_results/<species>/`