import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from jcvi.graphics.karyotype import Karyotype
from jcvi.apps.base import needs_update
import os, sys

# ============================================================
# Figure 2A: 8-species Cucurbit macrosynteny of SRC2 (PF00168)
# ============================================================

PROJECT = "PF00168"
WORKDIR = "/data5/qiulei/PPI/PF00168/JCVI"
OUTDIR = "/data5/qiulei/PPI/PF00168/03_figures"
os.chdir(WORKDIR)

# ========== 8 species order (synteny chain) ==========
SPECIES = [
    "ChineseLong",         # 1. Cucumber
    "DHL92",               # 2. Melon
    "97103",               # 3. Watermelon
    "USVL1VR-Ls",          # 4. Bottle gourd
    "Cpepo",               # 5. Squash (5 copies!)
    "Cargyrosperma",       # 6. C. argyrosperma
    "Cmaxima_Rimu",        # 7. Pumpkin
    "Cmoschata_Rifu",      # 8. Butternut squash
]

# ========== SRC2 ortholog groups ==========
SRC2 = {
    "ChineseLong":    ["CHL_v3.0_Chr02g31050_1","CHL_v3.0_Chr02g31060_1"],
    "DHL92":          ["MELO3C020768.2","MELO3C020769.2"],
    "97103":          ["Cla97C02G040740","Cla97C02G040750"],
    "USVL1VR-Ls":     ["Lsi02G013450","Lsi02G013440"],
    "Cpepo":          ["Cp4.1LG05g03400","Cp4.1LG05g03410","Cp4.1LG05g03420","Cp4.1LG05g03380","Cp4.1LG05g03390"],
    "Cargyrosperma":  ["Cargy08770s0001","Cargy08780s0001","Cargy08790s0001"],
    "Cmaxima_Rimu":   ["CmaX_Chr05g0206260","CmaX_Chr05g0206270","CmaX_Chr05g0206280"],
    "Cmoschata_Rifu": ["CmoCh05G027290","CmoCh05G027280","CmoCh05G027300"],
}

# ========== Synteny chains (7 pairwise) ==========
CHAINS = [
    ("ChineseLong","DHL92"),
    ("DHL92","97103"),
    ("97103","USVL1VR-Ls"),
    ("USVL1VR-Ls","Cpepo"),
    ("Cpepo","Cargyrosperma"),
    ("Cargyrosperma","Cmaxima_Rimu"),
    ("Cmaxima_Rimu","Cmoschata_Rifu"),
]

# ========== Karyotype config files ==========
SEQIDS = "seqids/seqids_fig2A.txt"
LAYOUT = "layout/layout_fig2A.csv"

# Generate .simple file list
SIMPLE_FILES = []
for A, B in CHAINS:
    fn = f"fig2A_{PROJECT}_{A}_{B}.filtered.simple"
    SIMPLE_FILES.append(fn)

# ========== Colors ==========
SRC2_COLOR = "#E63946"       # Red highlight
BG_COLOR = "#999999"          # Gray background

# Nature-style species colors (lighter)
SP_COLORS = ["#457B9D","#1D3557","#2A9D8F","#E9C46A","#F4A261","#E76F51","#A8DADC","#D4A373"]

# ========== Plot ==========
fig = Karyotype(
    seqidsfile=SEQIDS,
    layoutfile=LAYOUT,
    tracks=["track1","track2","track3","track4","track5","track6","track7","track8"],
    figsize=(8,6),
    dpi=600,
    style="white",
)

ax = fig.ax

# Draw synteny links (all PF00168 background)
for i, fn in enumerate(SIMPLE_FILES):
    if os.path.exists(fn):
        bedfiles = [f"{s}.bed" for s in [CHAINS[i][0], CHAINS[i][1]]]
        fig.add_synteny(
            fn,
            bedfiles=bedfiles,
            color=BG_COLOR,
            alpha=0.3,
            lw=0.5,
        )

# Highlight SRC2 ortholog pairs
for A, B in CHAINS:
    src2_a = SRC2.get(A,[])
    src2_b = SRC2.get(B,[])
    if src2_a and src2_b:
        # Find all pairs between A and B
        for ga in src2_a:
            for gb in src2_b:
                fig.add_highlight(ga, gb, color=SRC2_COLOR, lw=2.0, alpha=0.9)

# Save
outpdf = os.path.join(OUTDIR, "Figure2A_cucurbits_8species.pdf")
fig.savefig(outpdf, dpi=600, bbox_inches="tight")
print(f"Saved: {outpdf}")

# Post-process via shell
os.system(f'inkscape {outpdf} --export-filename={outpdf.replace(".pdf",".svg")}')
os.system(f'convert -density 600 {outpdf} -quality 95 {outpdf.replace(".pdf",".tiff")}')
print("Done.")
