# 🧬 SRC2 (PF00168) Synteny Analysis in Cucurbits — Article Figures

**Reproducible pipeline for Figure 2A: 8-species Cucurbit macrosynteny visualization of SRC2 gene copy number evolution.**

---

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Directory Structure](#-directory-structure)
3. [Data Sources](#-data-sources)
4. [Analysis Pipeline](#-analysis-pipeline)
5. [Software Dependencies](#-software-dependencies)
6. [How to Reproduce](#-how-to-reproduce)
7. [Methods Summary](#-methods-summary)

---

## 🔬 Overview

**Scientific question**: How did the SRC2 (Soybean genes Regulated by Cotyledons 2) gene copy number evolve across Cucurbitaceae species?

**Key finding**: SRC2 is conserved as 2 copies in most cucurbits (cucumber, melon, watermelon, bottle gourd), but expanded to **5 copies** in *Cucurbita pepo* (squash) via tandem duplication — a genus-specific event.

| Species | Common Name | SRC2 Copies | Notes |
|---------|-------------|-------------|-------|
| *C. sativus* (ChineseLong) | Cucumber | 2 | Ancestral state |
| *C. melo* (DHL92) | Melon | 2 | Ancestral state |
| *C. lanatus* (97103) | Watermelon | 2 | Ancestral state |
| *L. siceraria* (USVL1VR-Ls) | Bottle gourd | 2 | Ancestral state |
| *C. pepo* (Cpepo) | Squash | **5** | Tandem duplication |
| *C. argyrosperma* | C. argyrosperma | 3 | |
| *C. maxima* (Rimu) | Pumpkin | 3 | |
| *C. moschata* (Rifu) | Butternut squash | 3 | |

**Species synteny chain**: `ChineseLong → DHL92 → 97103 → USVL1VR-Ls → Cpepo → Cargyrosperma → Cmaxima_Rimu → Cmoschata_Rifu`

---

## 📁 Directory Structure

```
article_plot/
├── README.md                                          # This file
├── 01_data/                                           # Input data files
│   ├── README_input_data.md                           # Data format documentation
│   ├── {species}.bed                                  # Gene position BED files (8 species)
│   ├── {A}.{B}.filtered.simple                        # JCVI synteny blocks (7 pairwise)
│   ├── seqids_fig2A.txt                               # Chromosome list (Figure 2A)
│   └── seqids_figure2_cleaned.txt                     # Chromosome list (all species)
├── 02_scripts/                                        # All scripts
│   ├── figure2A_cucurbits_8species.py                 # ★ Core: 8-species Figure 2A
│   ├── figure2A_cucurbits.py                          # 4-species version (legacy)
│   ├── figure2B_conservation.py                       # Figure 2B: deep conservation
│   ├── figure3_microsynteny.py                        # Figure 3: microsynteny
│   ├── figure4_copy_number.R                          # Figure 4: copy number heatmap
│   ├── figure5_duplication.R                          # Figure 5: duplication events
│   ├── run_all.sh                                     # One-click run all figures
│   └── pipeline/                                      # Pipeline scripts
│       ├── USAGE_GUIDE.md                             # ★ Full tutorial (Chinese)
│       ├── config/species_config.py                   # Shared config
│       ├── step04_run_last_alignment.py               # LAST alignment
│       ├── step05_convert_anchors.py                  # anchors → .simple
│       ├── step06_generate_bed.py                     # GFF3 → BED
│       ├── fix_cds_ids.py                             # Remove .1 suffix
│       ├── run_jcvi_alignments.sh                     # Batch LAST
│       └── ...
├── metadata/                                          # Analysis metadata
│   ├── methods.txt
│   ├── run_metadata.json
│   └── qc_report.txt
├── 03_figures/                                        # Output figures
│   └── Figure2A_cucurbits_8species.{pdf,svg,tiff}
└── JCVI/                                              # Working directory
    ├── seqids_fig2A_8sp.txt
    ├── layout_fig2A_8sp.csv
    └── fig2A_*.simple
```

---

## 💾 Data Sources

All raw genomic data stored at: `/data5/qiulei/PPI/data/`

| Species | Genome | Source |
|---------|--------|--------|
| ChineseLong (Cucumber) | Chinese Long v3 | Cucurbit Genomics Database |
| DHL92 (Melon) | DHL92 v3.6 | Cucurbit Genomics Database |
| 97103 (Watermelon) | 97103 v2 | Cucurbit Genomics Database |
| USVL1VR-Ls (Bottle gourd) | USVL1VR-Ls v1 | Cucurbit Genomics Database |
| Cpepo (Squash) | C. pepo v4.1 | Cucurbit Genomics Database |
| Cargyrosperma | C. argyrosperma v1 | Cucurbit Genomics Database |
| Cmaxima_Rimu | C. maxima Rimu | Cucurbit Genomics Database |
| Cmoschata_Rifu | C. moschata Rifu | Cucurbit Genomics Database |

---

## 🔧 Analysis Pipeline

### Step 0: Domain Discovery (HMMER3)
```bash
hmmsearch --domtblout all_PF00168.domtblout Pfam-A.hmm PF00168 proteomes/*.pep
```

### Step 1: Representative Sequence Selection
```bash
cd-hit -i all_PF00168.fa -o PF00168_rep.fa -c 0.90
```

### Step 2: Multiple Sequence Alignment
```bash
mafft --auto PF00168_rep.fa > PF00168_aln.fa
clipkit PF00168_aln.fa -o PF00168_trimmed.fa -m kpi-smart-gap
```

### Step 3: Phylogenetic Tree (IQ-TREE2)
```bash
iqtree2 -s PF00168_trimmed.fa -m LG+G4 -B 100 -nt AUTO
```

### Step 4: BED File Generation
```bash
python pipeline/step06_generate_bed.py PF00168 ChineseLong DHL92 97103 Cpepo
python pipeline/fix_cds_ids.py
```

### Step 5: LAST Pairwise Alignment
```bash
python -m jcvi.compara.catalog ortholog --dbtype prot --cscore 0.99 --no_strip_names --notex A B
```

### Step 6: Synteny Filtering → .simple Format
```bash
python pipeline/step05_convert_anchors.py PF00168 sp1 sp2 sp3 ...
python -m jcvi.compara.synteny filter --minspan=30 --simple A.B.anchors A.B.simple
```

### Step 7: Visualization (JCVI Karyotype)
```bash
python 02_scripts/figure2A_cucurbits_8species.py
```

---

## 📦 Software Dependencies

| Tool | Version | Purpose |
|------|---------|---------|
| Python | ≥ 3.10 | Scripting |
| JCVI | ≥ 1.x | `jcvi.graphics.karyotype` |
| LAST | ≥ 1651 | Pairwise CDS alignment |
| MAFFT | ≥ 7 | MSA |
| IQ-TREE2 | ≥ 2 | Phylogeny |
| HMMER3 | ≥ 3.3 | Domain search |
| CD-HIT | ≥ 4.8 | Clustering |
| ClipKIT | ≥ 1.3 | Alignment trimming |
| Inkscape | ≥ 1.0 | PDF → SVG |
| ImageMagick | ≥ 7 | PDF → TIFF |

```bash
pip install jcvi matplotlib
```

---

## 🚀 How to Reproduce

### Quick start
```bash
cd 02_scripts
bash run_all.sh
```

### Step-by-step
```bash
# 1. Generate BED files
python pipeline/step06_generate_bed.py PF00168 ChineseLong DHL92 97103 Cpepo
# 2. Fix CDS IDs
python pipeline/fix_cds_ids.py
# 3. Run LAST alignments
bash pipeline/run_jcvi_alignments.sh
# 4. Convert to .simple format
python pipeline/step05_convert_anchors.py PF00168 ChineseLong DHL92 97103 Cpepo
# 5. Synteny filtering
python -m jcvi.compara.synteny filter --minspan=30 --simple A.B.anchors A.B.simple
# 6. Generate Figure 2A
python figure2A_cucurbits_8species.py
```

---

## 📊 Methods Summary

**Domain identification**: PF00168 (C2 domain) from 33 species via HMMER3 (E<1e-5). 4,621 hits clustered at 90% identity via CD-HIT → 33 representative sequences.

**Phylogenetic reconstruction**: MAFFT v7 (auto, 2,596 positions), ClipKIT trimming (kpi-smart-gap, 902 PI sites), IQ-TREE2 (LG+G4, 100 UFBoot).

**Synteny analysis**: LAST v1651 pairwise CDS alignment via JCVI (cscore=0.99). minspan=30 filtering. JCVI karyotype visualization.

**Figure export**: PDF 600dpi → SVG (Inkscape) + TIFF (ImageMagick 600dpi).

| Parameter | Value |
|-----------|-------|
| HMMER E-value | < 1e-5 |
| CD-HIT identity | 90% |
| MAFFT mode | auto |
| ClipKIT mode | kpi-smart-gap |
| IQ-TREE model | LG+G4 |
| Bootstrap | 100 (UFBoot) |
| JCVI cscore | 0.99 |
| Synteny minspan | 30 |
| Figure DPI | 600 |

---

## 👥 Author

**Lei Qiu** — [GitHub](https://github.com/qiulei030824-maker)