#!/usr/bin/env python3
"""Figure 2A: Cucurbit SRC2 duplication & internal synteny — 8 species.
Chain: ChineseLong → DHL92 → 97103 → USVL1VR-Ls → Cpepo → Cargyrosperma → Cmaxima_Rimu → Cmoschata_Rifu
Red highlights = SRC2 ortholog pairs from OG0000001.
Gray background = all PF00168 synteny."""
import os, sys, subprocess, glob

# ── Nature-style matplotlib settings (before any jcvi import) ──────────────
import matplotlib as mpl
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
mpl.rcParams['svg.fonttype'] = 'none'
mpl.rcParams['pdf.fonttype'] = 42

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "01_data")
JCVI_DIR = "/data5/qiulei/01.plant-phylogenomics/C2domain/PF00168/JCVI"
os.makedirs(JCVI_DIR, exist_ok=True)
os.chdir(JCVI_DIR)

# SRC2 orthologs traced through synteny chain
OG = {
    "ChineseLong":     ["CsaV3_1G038880", "CsaV3_2G006560"],
    "DHL92":           ["MELO3C015314", "MELO3C004229"],
    "97103":           ["Cla97C02G041265", "Cla97C03G067410"],
    "USVL1VR-Ls":      ["Lsi06G001210", "Lsi11G005810"],
    "Cpepo":           ["Cp4.1LG04g00520", "Cp4.1LG07g09010",
                        "Cp4.1LG11g09090", "Cp4.1LG00g08660", "Cp4.1LG00g10790"],
    "Cargyrosperma":   ["Carg25033-RA", "Carg17534-RA", "Carg26763-RA"],
    "Cmaxima_Rimu":    ["RimuC11G010740", "RimuC05G011370", "RimuC12G010060"],
    "Cmoschata_Rifu":  ["RifuC11G010610", "RifuC05G010850", "RifuC12G010240"],
}
ORDER = [
    "ChineseLong", "DHL92", "97103", "USVL1VR-Ls",
    "Cpepo", "Cargyrosperma", "Cmaxima_Rimu", "Cmoschata_Rifu",
]

# ── Nature-style refined palette (Nature Genomics + Nature Clinical) ─────
SPECIES_COLORS = {
    "ChineseLong":          "#0F4D92",   # Nature blue_main
    "DHL92":                "#B64342",   # Nature red_strong
    "97103":                "#42949E",   # Nature teal
    "USVL1VR-Ls":           "#7BAA5B",   # Nature clinical year1 green
    "Cpepo":                "#9A4D8E",   # Nature violet
    "Cargyrosperma":        "#3775BA",   # Nature blue_secondary
    "Cmaxima_Rimu":         "#E28E2C",   # Nature clinical week6 amber
    "Cmoschata_Rifu":       "#5B7FCA",   # Nature genomics wave2
}

SPECIES_LABELS = {
    "ChineseLong":          "C. sativus",
    "DHL92":                "C. melo",
    "97103":                "C. lanatus",
    "USVL1VR-Ls":           "L. siceraria",
    "Cpepo":                "C. pepo",
    "Cargyrosperma":        "C. argyrosperma",
    "Cmaxima_Rimu":         "C. maxima",
    "Cmoschata_Rifu":       "C. moschata",
}

# Nature-style highlight red (for SRC2 ortholog pairs)
HIGHLIGHT_RED = "#D9544D"   # Nature genomics wave1

# Clean old fig2A files
for f in glob.glob("fig2A_*"):
    os.remove(f)
for f in glob.glob("layout_fig2A*"):
    os.remove(f)
for f in glob.glob("seqids_fig2A*"):
    os.remove(f)

# Link data files
for f in os.listdir(PROCESSED_DIR):
    if f.endswith(".bed") or f.endswith(".filtered.simple"):
        src = os.path.join(PROCESSED_DIR, f)
        dst = os.path.join(JCVI_DIR, f)
        if not os.path.exists(dst) and not os.path.islink(dst):
            os.symlink(src, dst)

# Link new species BED files
for sp in ["USVL1VR-Ls", "Cargyrosperma", "Cmaxima_Rimu", "Cmoschata_Rifu"]:
    bed_file = f"{sp}.bed"
    src = os.path.join(PROCESSED_DIR, bed_file)
    dst = os.path.join(JCVI_DIR, bed_file)
    if not os.path.exists(dst) and not os.path.islink(dst) and os.path.exists(src):
        os.symlink(src, dst)

# Create seqids — remove pseudo-chromosomes (chr00, LG00)
seqids = {
    "ChineseLong":          "chr1,chr2,chr3,chr4,chr5,chr6,chr7",
    "DHL92":                "chr01,chr02,chr03,chr04,chr05,chr06,chr07,chr08,chr09,chr10,chr11,chr12",
    "97103":                "Cla97Chr01,Cla97Chr02,Cla97Chr03,Cla97Chr04,Cla97Chr05,Cla97Chr06,Cla97Chr07,Cla97Chr08,Cla97Chr09,Cla97Chr10,Cla97Chr11",
    "USVL1VR-Ls":           "chr01,chr02,chr03,chr04,chr05,chr06,chr07,chr08,chr09,chr10,chr11",
    "Cpepo":                "Cp4.1LG01,Cp4.1LG02,Cp4.1LG03,Cp4.1LG04,Cp4.1LG05,Cp4.1LG06,Cp4.1LG07,Cp4.1LG08,Cp4.1LG09,Cp4.1LG10,Cp4.1LG11,Cp4.1LG12,Cp4.1LG13,Cp4.1LG14,Cp4.1LG15,Cp4.1LG16,Cp4.1LG17,Cp4.1LG18,Cp4.1LG19,Cp4.1LG20",
    "Cargyrosperma":        "Carg_Chr01,Carg_Chr02,Carg_Chr03,Carg_Chr04,Carg_Chr05,Carg_Chr06,Carg_Chr07,Carg_Chr08,Carg_Chr09,Carg_Chr10,Carg_Chr11,Carg_Chr12,Carg_Chr13,Carg_Chr14,Carg_Chr15,Carg_Chr16,Carg_Chr17,Carg_Chr18,Carg_Chr19,Carg_Chr20",
    "Cmaxima_Rimu":         "Chr01,Chr02,Chr03,Chr04,Chr05,Chr06,Chr07,Chr08,Chr09,Chr10,Chr11,Chr12,Chr13,Chr14,Chr15,Chr16,Chr17,Chr18,Chr19,Chr20",
    "Cmoschata_Rifu":       "Chr01,Chr02,Chr03,Chr04,Chr05,Chr06,Chr07,Chr08,Chr09,Chr10,Chr11,Chr12,Chr13,Chr14,Chr15,Chr16,Chr17,Chr18,Chr19,Chr20",
}

seqids_list = [seqids[sp] for sp in ORDER]
with open("seqids_fig2A_8sp.txt", "w") as f:
    f.write("\n".join(seqids_list) + "\n")

# SRC2 highlight .simple files
def write_highlight(fname, sp_a, sp_b):
    genes_a, genes_b = OG[sp_a], OG[sp_b]
    with open(fname, "w") as f:
        for ga in genes_a:
            for gb in genes_b:
                f.write(f"{HIGHLIGHT_RED}*{ga}\t{ga}\t{gb}\t{gb}\t100\t+\n")

pairs = [
    ("fig2A_Cc_Dl.simple", "ChineseLong", "DHL92"),
    ("fig2A_Dl_97.simple", "DHL92", "97103"),
    ("fig2A_97_Us.simple", "97103", "USVL1VR-Ls"),
    ("fig2A_Us_Cp.simple", "USVL1VR-Ls", "Cpepo"),
    ("fig2A_Cp_Cg.simple", "Cpepo", "Cargyrosperma"),
    ("fig2A_Cg_Cx.simple", "Cargyrosperma", "Cmaxima_Rimu"),
    ("fig2A_Cx_Cf.simple", "Cmaxima_Rimu", "Cmoschata_Rifu"),
]
for fname, a, b in pairs:
    write_highlight(fname, a, b)

# Build layout
n = len(ORDER)
track_lines = []
spacing = 0.85 / (n - 1)
xstart = 0.25
xend = 0.95
for i, sp in enumerate(ORDER):
    y = 0.90 - i * spacing
    color = SPECIES_COLORS[sp]
    label = SPECIES_LABELS[sp]
    track_lines.append(f"{y:.3f}, {xstart}, {xend}, 0, {color}, {label}, top, {sp}.bed, center")

edge_lines = []
background_edges = [
    (0, 1, "ChineseLong.DHL92.filtered.simple"),
    (1, 2, "DHL92.97103.filtered.simple"),
    (2, 3, "97103.USVL1VR-Ls.filtered.simple"),
    (3, 4, "USVL1VR-Ls.Cpepo.filtered.simple"),
    (4, 5, "Cpepo.Cargyrosperma.filtered.simple"),
    (5, 6, "Cargyrosperma.Cmaxima_Rimu.filtered.simple"),
    (6, 7, "Cmaxima_Rimu.Cmoschata_Rifu.filtered.simple"),
]
for i_from, i_to, fname in background_edges:
    edge_lines.append(f"e, {i_from}, {i_to}, {fname}")

highlight_edges = [
    (0, 1, "fig2A_Cc_Dl.simple"),
    (1, 2, "fig2A_Dl_97.simple"),
    (2, 3, "fig2A_97_Us.simple"),
    (3, 4, "fig2A_Us_Cp.simple"),
    (4, 5, "fig2A_Cp_Cg.simple"),
    (5, 6, "fig2A_Cg_Cx.simple"),
    (6, 7, "fig2A_Cx_Cf.simple"),
]
for i_from, i_to, fname in highlight_edges:
    edge_lines.append(f"e, {i_from}, {i_to}, {fname}")

layout_content = "# y, xstart, xend, rotation, color, label, va, bed, label_va\n"
for line in track_lines:
    layout_content += line + "\n"
layout_content += "# Background edges (PF00168 all synteny)\n"
for line in edge_lines:
    layout_content += line + "\n"

with open("layout_fig2A_8sp.csv", "w") as f:
    f.write(layout_content)

# Run JCVI
cmd = [
    "python", "-m", "jcvi.graphics.karyotype",
    "--notex", "--font", "Arial",
    "--figsize", "8x6", "--dpi", "600",
    "--nocircles", "--style", "white",
    "--shadestyle", "curve",
    "-o", "Figure2A_cucurbits_8species.pdf",
    "seqids_fig2A_8sp.txt", "layout_fig2A_8sp.csv",
]
subprocess.run(cmd, check=True)

# Post-process
if os.path.exists("Figure2A_cucurbits_8species.pdf"):
    subprocess.run(["inkscape", "Figure2A_cucurbits_8species.pdf",
                    "--export-filename=Figure2A_cucurbits_8species.svg",
                    "--export-dpi=600"], check=True)
    subprocess.run(["convert", "-density", "600", "Figure2A_cucurbits_8species.pdf",
                    "-quality", "95", "Figure2A_cucurbits_8species.tiff"], check=True)