#!/usr/bin/env python3
"""
Shared configuration for Pfam domain analysis pipeline.

This file centralizes:
  - Species groups and colors
  - Base paths (supports both legacy C2 mode and generic Pfam mode)
  - Utility functions (get_species, get_protein_id, get_group, parse_newick_tips)
"""

import os
import re
from pathlib import Path

# ── Base paths ─────────────────────────────────────────────────────────────
DATA_DIR = "/data5/qiulei/PPI/data"
BASE_ROOT = Path("/data5/qiulei/PPI/03.OrthoFinder_MCScanX/0430")
SKIP_DIRS = {"logs", "pfamdb", "__pycache__", "taxonomy_classification",
             "memory.md", "process_genomes.py", "reorganize.sh",
             "setup_erast.sh", "README_ERAST.md", "README.md"}

PIPELINE_ROOT = Path("/data5/qiulei/pfam_pipeline")
PIPELINE_RESULTS = PIPELINE_ROOT / "results"
PIPELINE_DATA = PIPELINE_ROOT / "data"

# ── Species groups ────────────────────────────────────────────────────────
SPECIES_GROUP = {
    "Cucurbits": [
        "97103", "Cargyrosperma", "Cmaxima_Rimu", "Cmoschata_Rifu",
        "Cpepo", "ChineseLong", "DHL92", "USVL1VR-Ls",
    ],
    "Brassicaceae": [
        "arabidopsis_halleri", "arabidopsis_lyrata", "arabidopsis_thaliana",
        "brassica_napus", "brassica_oleracea", "brassica_rapa",
        "eutrema_salsugineum", "arabis_alpina",
    ],
    "Solanaceae": [
        "capsicum_annuum", "nicotiana_attenuata",
        "solanum_lycopersicum", "solanum_tuberosum",
    ],
    "Fabids": [
        "corylus_avellana", "quercus_lobata", "eucalyptus_grandis",
        "pistacia_vera", "gossypium_raimondii", "theobroma_cacao",
        "ficus_carica", "malus_domestica_golden", "rosa_chinensis",
        "glycine_max", "medicago_truncatula", "phaseolus_vulgaris",
        "citrus_clementina", "manihot_esculenta", "populus_trichocarpa",
        "prunus_persica",
    ],
    "Vitales": ["vitis_vinifera"],
    "Monocots": [
        "asparagus_officinalis", "ananas_comosus",
        "brachypodium_distachyon", "sorghum_bicolor", "zea_mays",
        "oryza_sativa", "musa_acuminata",
    ],
    "Basal_Angiosperms": ["amborella_trichopoda", "nymphaea_colorata"],
    "Non_Vascular": [
        "marchantia_polymorpha", "physcomitrium_patens",
        "selaginella_moellendorffii",
    ],
}

# ── Group colors (for plotting) ────────────────────────────────────────────
GROUP_COLORS = {
    "Cucurbits": "#2166AC",
    "Brassicaceae": "#4393C3",
    "Solanaceae": "#92C5DE",
    "Fabids": "#D1E5F0",
    "Vitales": "#FDDBC7",
    "Monocots": "#F4A582",
    "Basal_Angiosperms": "#D6604D",
    "Non_Vascular": "#B2182B",
    "Other": "#BABABA",
}


def get_species(tip_label):
    return tip_label.split("|")[0]

def get_protein_id(tip_label):
    return tip_label.split("|")[1] if "|" in tip_label else tip_label

def get_group(species_name):
    for group, members in SPECIES_GROUP.items():
        if species_name in members:
            return group
    return "Other"

def get_group_color(species_name):
    return GROUP_COLORS.get(get_group(species_name), GROUP_COLORS["Other"])

def parse_newick_tips(filepath):
    with open(filepath) as f:
        newick = f.read().strip()
    cleaned = re.sub(r'\)\d+:', '):', newick)
    cleaned = re.sub(r':[\d.eE+-]+', '', cleaned)
    matches = re.findall(r'[,(](\S+?)[,)]', cleaned)
    seen = set()
    tips = []
    for m in matches:
        m = m.strip()
        if m and not m.startswith('(') and m not in seen:
            seen.add(m)
            tips.append(m)
    return tips

def resolve_pfam_paths(pfam_id, pipeline_root=None):
    if pipeline_root is None:
        pipeline_root = BASE_ROOT
    pipeline_root = Path(pipeline_root)
    is_c2 = pfam_id.upper() == "C2"
    if is_c2:
        base_dir = pipeline_root
        pep_dir = pipeline_root / "C2domain_pep"
        cds_dir = pipeline_root / "C2domain_cds"
        hmmer_dir = pipeline_root / "hmmer"
        tree_dir = pipeline_root / "tree"
        align_dir = pipeline_root / "algin"
        hmmer_file = hmmer_dir / "all_C2.domtblout"
        tree_file = tree_dir / "C2_tree.treefile"
    else:
        base_dir = pipeline_root / pfam_id
        pep_dir = base_dir / "pep"
        cds_dir = base_dir / "cds"
        hmmer_dir = base_dir / "hmmer"
        tree_dir = base_dir / "tree"
        align_dir = base_dir / "algin"
        hmmer_file = hmmer_dir / f"all_{pfam_id}.domtblout"
        tree_file = tree_dir / f"{pfam_id}_tree.treefile"
    return {
        "base_dir": base_dir, "pep_dir": pep_dir, "cds_dir": cds_dir,
        "hmmer_dir": hmmer_dir, "tree_dir": tree_dir, "align_dir": align_dir,
        "hmmer_file": hmmer_file, "tree_file": tree_file, "is_c2": is_c2,
    }

def resolve_output_paths(pfam_id):
    output_base = PIPELINE_RESULTS / pfam_id
    return {
        "output_base": output_base,
        "gene_structure_dir": output_base / "gene_structure",
        "dnds_dir": output_base / "dnds",
        "duplication_dir": output_base / "gene_duplication",
        "chromosome_map_dir": output_base / "chromosome_map",
        "alignment_view_dir": output_base / "alignment_view",
    }

def resolve_step_paths(pfam_id):
    return resolve_pfam_paths(pfam_id, pipeline_root=PIPELINE_DATA)