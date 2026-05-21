# Hemiptera Effector SignalP5 SP⁺ Candidate Pipeline

## Overview

Systematic identification of secreted effector candidates across 48 hemipteran species spanning 20 taxonomic groups using SignalP5.0 (eukaryote mode). This pipeline predicts classical signal peptide (SP) secretion signals, applies the SP⁺ threshold (score > 0.5), and compiles species-level and pan-hemipteran candidate datasets for downstream effector biology, structural prediction, and evolutionary rate covariation (ERC) analyses.

### Key Outputs

- **127,977 SP⁺ candidates** across 48 species (70 MB merged FASTA)
- **Per-species candidate lists** with sequence-level statistics
- **Publication-ready bar chart** (Nature-style color palette, SVG/600 dpi PNG)
- **15 known effectors** from 9 hemipteran species with PubMed-verified metadata

## Methods

### Signal Peptide Prediction

SignalP5.0 (Almagro Armenteros et al., 2019, *Nature Biotechnology*) was run with the following parameters:

| Parameter | Value | Justification |
|-----------|-------|---------------|
| Organism group | `eukarya` (`-org euk`) | Hemipteran proteins share eukaryotic signal peptidase machinery |
| Output format | `short` (`-format short`) | Tabular output for efficient parsing |
| SP⁺ threshold | Score > 0.5 | Recommended default; balances sensitivity/specificity for secreted proteins |
| Parallel jobs | 4–8 | Adjustable based on available CPU cores |

### Data Sources

| Source | Species | Data Type |
|--------|---------|-----------|
| NCBI RefSeq (GCF/GCA) | 26 species | `*_protein.faa.gz` (annotated proteomes) |
| AphidBase | 22 species | `*_proteins.fa.faa.gz` (curated aphid proteomes) |

### Phylogenetic Coverage

20 taxonomic groups ordered by evolutionary relationship (basal → derived → outgroups):

```
phylloxera → adelgid → aphid → planthopper → leafhopper → froghopper →
cicada → lanternfly → psyllid → whitefly → mealybug → stink_bug →
mirid_bug → bed_bug → predatory_bug → kissing_bug → water_strider →
outgroup_thrips → outgroup_hym (honeybee) → outgroup_psocodea (louse)
```

## Pipeline Workflow

### Phase 1: SignalP5 Batch Prediction

Three batch runs were executed sequentially:

1. **Batch 1** (`run_signalp5_batch.sh`): 26 NCBI RefSeq species, 8 parallel jobs, standard gzip decompression
2. **Batch 2** (`run_signalp5_batch2.sh`): 22 aphidbase species, 8 parallel jobs
3. **Batch 3 (fix)** (`run_signalp5_batch3_fix.sh`): Re-run for aphidbase species with mixed gzip/plain-text format detection (`gzip -t` check)

### Phase 2: Candidate Merging

`merge_signalp5_candidates.py` performs:
- Automatic gzip magic-byte detection (`\x1f\x8b`)
- SP⁺ filtering (score > 0.5) from `_summary.signalp5` files
- FASTA extraction with species-prefixed headers (`>species|seqid`)
- Robust error handling (missing files, corrupt data, format issues)

### Phase 3: Visualization

`plot_signalp5_barchart.py` generates a Nature-style bar chart with:
- 20-group phylogenetic ordering on x-axis
- Group-level color coding (Nature palette, 20 colors)
- Bracket annotations for taxonomic groups
- SP⁺ candidate counts on bar tops
- Group legend below figure
- Output: `signalp5_sp_counts.svg` (editable) + `signalp5_sp_counts.png` (600 dpi)

## Evolutionary Groups and Color Palette

| Group | Color | Code | Species |
|-------|-------|------|---------|
| phylloxera | `#0F4D92` | blue_main | 1 |
| adelgid | `#3775BA` | blue_light | 2 |
| aphid | `#AADCA9` | green_2 | 26 |
| planthopper | `#8BCF8B` | green_3 | 1 |
| leafhopper | `#DDF3DE` | green_1 | 2 |
| froghopper | `#42949E` | teal | 0 |
| cicada | `#B64342` | red_strong | 0 |
| lanternfly | `#F6CFCB` | red_1 | 1 |
| psyllid | `#E9A6A1` | red_2 | 1 |
| whitefly | `#EA84DD` | magenta | 1 |
| mealybug | `#9A4D8E` | violet | 1 |
| stink_bug | `#767676` | neutral_mid | 1 |
| mirid_bug | `#CFCECE` | neutral_light | 1 |
| bed_bug | `#4D4D4D` | neutral_dark | 1 |
| predatory_bug | `#272727` | neutral_black | 0 |
| kissing_bug | `#FFD700` | gold | 1 |
| water_strider | `#E4CCD8` | pink | 0 |
| outgroup_thrips | `#B4C0E4` | pastel_blue | 2 |
| outgroup_hym | `#7884B4` | pastel_purple | 1 |
| outgroup_psocodea | `#484878` | dark_purple | 1 |

**Total species with protein data: 48**

## Known Effector References

15 experimentally validated effectors from 9 species:

| Effector | Species | Reference |
|----------|---------|-----------|
| Bsp9 | *Bemisia tabaci* | Xu et al. 2019 *Nature Comms* |
| Bt56 | *Bemisia tabaci* | Wang et al. 2019 *Plant Cell* |
| Btp2 | *Bemisia tabaci* | Chen et al. 2024 *New Phytol* |
| NlSEF1 | *Nilaparvata lugens* | Ye et al. 2017 *eLife* |
| NlMLP | *Nilaparvata lugens* | Guo et al. 2022 *Plant Comms* |
| Nl12 | *Nilaparvata lugens* | Rao et al. 2019 *Mol Plant* |
| Mp1 | *Myzus persicae* | Rodriguez et al. 2018 *PNAS* |
| Mp10 | *Myzus persicae* | Thorpe et al. 2018 *Insect Biochem* |
| Mp55 | *Myzus persicae* | Wang et al. 2023 *New Phytol* |
| CO02 | *Acyrthosiphon pisum* | Carolan et al. 2009 *Insect Mol Biol* |
| CO06 | *Acyrthosiphon pisum* | Carolan et al. 2011 *J Proteome Res* |
| DcP11 | *Diaphorina citri* | Killiny et al. 2023 *Insect Sci* |
| HhEF1 | *Halyomorpha halys* | Serteyn et al. 2022 *J Insect Physiol* |
| AlEF1 | *Apolygus lucorum* | Yang et al. 2021 *Insect Sci* |

## Directory Structure

```
hemiptera_effector_signalp5_SP_candidates/
├── README.md
├── scripts/
│   ├── run_signalp5_batch.sh
│   ├── run_signalp5_batch2.sh
│   ├── run_signalp5_batch3_fix.sh
│   ├── merge_signalp5_candidates.py
│   └── plot_signalp5_barchart.py
├── data/
│   ├── sp_counts_per_species.tsv
│   ├── effector_metadata.tsv
│   └── insect_species_groups.tsv
├── metadata/
│   ├── signalp5_parameters.md
│   ├── batch_run_summary.md
│   └── pipeline_qc.md
└── figures/
    ├── signalp5_sp_counts.svg
    └── signalp5_sp_counts.png
```

## Requirements

- **SignalP5.0** (licensed; DTU)
- **Python ≥ 3.8** with `matplotlib`, `numpy`
- **seqkit** (optional)

## Reproducibility

```bash
# Edit PROJ path in each script
bash scripts/run_signalp5_batch.sh
bash scripts/run_signalp5_batch2.sh
bash scripts/run_signalp5_batch3_fix.sh
python scripts/merge_signalp5_candidates.py
python scripts/plot_signalp5_barchart.py
```

## Citation

- SignalP5.0: Almagro Armenteros et al. (2019) *Nature Biotechnology* 37, 420–423
- Hemiptera effector dataset: [citation to be added]