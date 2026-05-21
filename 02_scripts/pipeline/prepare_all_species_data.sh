#!/bin/bash
# prepare_all_species_data.sh — One-click prepare all 22 species BED + CDS
# Usage: bash prepare_all_species_data.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK_DIR="/data5/qiulei/pfam_pipeline/data/processed/PF00168_jcvi_chain"
mkdir -p "${WORK_DIR}"
cd "${WORK_DIR}"

echo "=========================================="
echo " Preparing BED + CDS for all 22 species"
echo "=========================================="
echo ""

# Brassicaceae
echo "[1/6] Brassicaceae..."
python "${SCRIPT_DIR}/step06_generate_bed.py" PF00168 \
  arabidopsis_thaliana arabidopsis_halleri arabis_alpina brassica_rapa brassica_napus

# Solanaceae
echo "[2/6] Solanaceae..."
python "${SCRIPT_DIR}/step06_generate_bed.py" PF00168 \
  solanum_lycopersicum capsicum_annuum nicotiana_attenuata solanum_tuberosum

# Cucurbits
echo "[3/6] Cucurbits..."
python "${SCRIPT_DIR}/step06_generate_bed.py" PF00168 \
  ChineseLong DHL92 97103 Cpepo

# Poaceae
echo "[4/6] Poaceae..."
python "${SCRIPT_DIR}/step06_generate_bed.py" PF00168 \
  oryza_sativa brachypodium_distachyon sorghum_bicolor zea_mays

# Fabids + Vitales
echo "[5/6] Fabids + Vitales..."
python "${SCRIPT_DIR}/step06_generate_bed.py" PF00168 \
  glycine_max eucalyptus_grandis populus_trichocarpa vitis_vinifera

# Basal
echo "[6/6] Basal Angiosperms..."
python "${SCRIPT_DIR}/step06_generate_bed.py" PF00168 amborella_trichopoda

echo ""
echo "Output:"
ls -lh *.bed 2>/dev/null | wc -l
echo "BED files generated."
ls -lh *.cds 2>/dev/null | wc -l
echo "CDS files."
echo ""
echo "All done."