# SignalP5 Batch Run Summary

## Overview

Three batch runs were executed to process all 48 hemipteran species. The runs were designed to handle differences in file format, naming conventions, and data sources between NCBI RefSeq and AphidBase resources.

---

## Batch 1: NCBI RefSeq Species

| Property | Value |
|----------|-------|
| **Script** | `run_signalp5_batch.sh` |
| **Species** | 26 NCBI RefSeq species |
| **Parallel jobs** | 8 |
| **File pattern** | `raw/*/*/*_protein.faa.gz` |
| **Decompression** | Standard `gunzip -c` |
| **SP⁺ criteria** | Column 2 == "YES" in summary output |
| **Merging** | `seqkit grep` for hit extraction |
| **Status** | ✅ Completed |

### Species processed (26)

Adelges_cooleyi, Acyrthosiphon_pisum, Aphis_craccivora, Aphis_gossypii, Apis_mellifera, Apolygus_lucorum, Bemisia_tabaci_MEAM1, Cimex_lectularius, Daktulosphaira_vitifoliae, Diaphorina_citri, Diuraphis_noxia, Frankliniella_occidentalis, Halyomorpha_halys, Homalodisca_vitripennis, Lycorma_delicatula, Macrosteles_quadrilineatus, Melanaphis_sacchari, Metopolophium_dirhodum, Myzus_persicae, Nilaparvata_lugens, Pediculus_humanus, Planococcus_citri, Rhodnius_prolixus, Rhopalosiphum_maidis, Rhopalosiphum_padi, Thrips_palmi

---

## Batch 2: AphidBase Species (Initial Run)

| Property | Value |
|----------|-------|
| **Script** | `run_signalp5_batch2.sh` |
| **Species** | 22 aphidbase species |
| **Parallel jobs** | 8 |
| **File pattern** | `raw/aphid/<species>/*.faa*` |
| **Decompression** | Standard `gunzip -c` |
| **SP⁺ criteria** | Column 3 score > 0.5 |
| **Status** | ⚠️ Issues detected |

### Issue: Mixed gzip/plain-text format

Some `.faa.gz` files from AphidBase were found to be plain text files with `.gz` extensions rather than true gzip files. This caused `gunzip -c` failures and incomplete results.

---

## Batch 3 (Fix): AphidBase Re-run

| Property | Value |
|----------|-------|
| **Script** | `run_signalp5_batch3_fix.sh` |
| **Species** | 22 aphidbase species (re-run) |
| **Parallel jobs** | 4 (reduced) |
| **Decompression** | `gzip -t` detection → gunzip or direct copy |
| **SP⁺ criteria** | Column 3 score > 0.5 |
| **Status** | ✅ Completed |

### Fix: Format detection

```bash
if gzip -t "$faa" 2>/dev/null; then
    gunzip -c "$faa" > "/tmp/${sp}.faa"    # True gzip
else
    cp "$faa" "/tmp/${sp}.faa"              # Plain text
fi
```

### AphidBase species processed (22)

Acyrthosiphon_pisum_JIC, Aphis_fabae, Aphis_rumicis, Aphis_thalictri, Brachycaudus_helichrysi, Brachycaudus_klugkisti, Cinara_cedri, Drepanosiphum_platanoidis, Eriosoma_laniyerum, Hamadryas_cornu, Macrosiphum_euphorbiae, Myzus_cerasi, Myzus_varians, Nasonovia_ribisnigri, Neotoxoptera_formosana, Pentalonia_nigronervosa, Pseudoregma_acericola, Sitobion_avenae, Stomaphis_chinensis, Therioaphis_trifolii, Tuberocephalus_akinire, Tuberolachnus_salignus

---

## Final Merge

| Property | Value |
|----------|-------|
| **Script** | `merge_signalp5_candidates.py` |
| **Total candidates** | 127,977 |
| **Total species** | 48 |
| **Output** | `all_candidates_signalp5.fa` (70 MB) |
| **Header format** | `>species|seqid` |

## Species Without Protein Data (18)

- Adelges_tsugae, Aphis_glycines, Aulacorthum_solani, Phyllaphis_fagi, Schizaphis_graminum
- Magicicada_septendecula, Aphrophora_alni, Triatoma_infestans, Adelphocoris_suturalis
- Laodelphax_striatellus, Sogatella_furcifera, Orius_laevigatus, Arma_chinensis
- Aquarius_paludum, Gerris_buenoi, Bemisia_tabaci_MED, Trialeurodes_vaporariorum