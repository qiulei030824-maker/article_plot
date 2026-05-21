# Pipeline Quality Control Report

## Data Integrity

### SP⁺ Candidate Distribution

| Metric | Value |
|--------|-------|
| Total species | 48 |
| Total SP⁺ candidates | 127,977 |
| Min per species | 199 (Cinara_cedri) |
| Max per species | 6,501 (Daktulosphaira_vitifoliae) |
| Mean per species | 2,666 |
| Median per species | 2,316 |
| Total merged FASTA size | 70 MB |

### Top 5 Species by SP⁺ Candidate Count

| Rank | Species | Group | SP⁺ Count |
|------|---------|-------|-----------|
| 1 | Daktulosphaira_vitifoliae | phylloxera | 6,501 |
| 2 | Adelges_cooleyi | adelgid | 6,049 |
| 3 | Macrosteles_quadrilineatus | leafhopper | 5,170 |
| 4 | Planococcus_citri | mealybug | 5,014 |
| 5 | Homalodisca_vitripennis | leafhopper | 4,528 |

### Bottom 5 Species by SP⁺ Candidate Count

| Rank | Species | Group | SP⁺ Count |
|------|---------|-------|-----------|
| 44 | Cinara_cedri | aphid | 199 |
| 45 | Pediculus_humanus | outgroup_psocodea | 707 |
| 46 | Eriosoma_laniyerum | aphid | 1,262 |
| 47 | Myzus_cerasi | aphid | 1,259 |
| 48 | Tuberolachnus_salignus | aphid | 1,402 |

## Format Inconsistencies

### Issue 1: SignalP5 Output Column Format

Two different summary formats were observed:

1. **Standard format** (column2 = YES/NO): Most NCBI RefSeq species
2. **Direct score format** (column3 > 0.5): All species

**Resolution**: Applied `column3 > 0.5` threshold uniformly across all species.

### Issue 2: AphidBase FASTA Compression

AphidBase `.faa.gz` files had mixed formats:
- True gzip-compressed files (standard)
- Plain text files with `.gz` extension (pseudo-gzip)

**Resolution**: Added `gzip -t` format detection.

## Known Limitations

1. **SignalP5 SP⁺ is conservative**: Only identifies classical secretory pathway signals.
2. **Annotation quality varies**: AphidBase vs NCBI RefSeq annotations may differ.
3. **Some groups underrepresented**: froghopper, cicada, predatory_bug, water_strider have no protein data.
4. **Cinara_cedri low count (199)**: Likely annotation completeness, not biology.

## Recommended Downstream Analyses

1. **EffectorP3 validation**: Cross-validate SP⁺ candidates
2. **DeepLoc2 localization**: Subcellular localization prediction
3. **TMHMM filtering**: Remove membrane proteins (>1 TM domain)
4. **Homology search**: BLASTp against PHI-base, EffectorDB