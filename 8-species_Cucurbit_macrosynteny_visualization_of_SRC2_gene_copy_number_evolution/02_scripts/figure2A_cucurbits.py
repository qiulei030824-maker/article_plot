import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from jcvi.graphics.karyotype import Karyotype
import os

PROJECT = "PF00168"
WORKDIR = "/data5/qiulei/PPI/PF00168/JCVI"
OUTDIR = "/data5/qiulei/PPI/PF00168/03_figures"
os.chdir(WORKDIR)

SPECIES = ["ChineseLong","DHL92","97103","Cpepo"]

SRC2 = {
    "ChineseLong": ["CHL_v3.0_Chr02g31050_1","CHL_v3.0_Chr02g31060_1"],
    "DHL92": ["MELO3C020768.2","MELO3C020769.2"],
    "97103": ["Cla97C02G040740","Cla97C02G040750"],
    "Cpepo": ["Cp4.1LG05g03400","Cp4.1LG05g03410","Cp4.1LG05g03420","Cp4.1LG05g03380","Cp4.1LG05g03390"],
}

CHAINS = [("ChineseLong","DHL92"),("DHL92","97103"),("97103","Cpepo")]

SEQIDS = "seqids/seqids_figure2_cleaned.txt"
LAYOUT = "layout/layout_fig2A.csv"

SIMPLE_FILES = []
for A,B in CHAINS:
    fn = f"fig2A_{PROJECT}_{A}_{B}.filtered.simple"
    if os.path.exists(fn):
        SIMPLE_FILES.append(fn)

fig = Karyotype(seqidsfile=SEQIDS, layoutfile=LAYOUT, figsize=(8,6), dpi=600, style="white")
for fn in SIMPLE_FILES:
    fig.add_synteny(fn, color="#999999", alpha=0.3, lw=0.5)

SRC2_COLOR = "#E63946"
for A,B in CHAINS:
    for ga in SRC2.get(A,[]):
        for gb in SRC2.get(B,[]):
            fig.add_highlight(ga, gb, color=SRC2_COLOR, lw=2.0, alpha=0.9)

outpdf = os.path.join(OUTDIR,"Figure2A_cucurbits.pdf")
fig.savefig(outpdf, dpi=600, bbox_inches="tight")
print(f"Saved: {outpdf}")
