#!/usr/bin/env python3
"""Figure 2A: Cucurbit SRC2 duplication & internal synteny.
4 species: C. sativus, C. melo, C. lanatus, C. pepo.
Red highlights = SRC2 ortholog pairs from OG0000001.
Gray background = all PF00168 synteny."""
import os, sys, subprocess, glob

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "01_data")
JCVI_DIR = "/data5/qiulei/01.plant-phylogenomics/C2domain/PF00168/JCVI"
os.chdir(JCVI_DIR)

OG = {
    "ChineseLong": ["CsaV3_1G038880", "CsaV3_2G006560"],
    "DHL92":       ["MELO3C015314", "MELO3C004229"],
    "97103":       ["Cla97C02G041265", "Cla97C03G067410"],
    "Cpepo":       ["Cp4.1LG04g00520", "Cp4.1LG07g09010",
                    "Cp4.1LG11g09090", "Cp4.1LG00g08660", "Cp4.1LG00g10790"],
}
ORDER = ["ChineseLong", "DHL92", "97103", "Cpepo"]
COLOR_RED = "#E41A1C"

for f in glob.glob("fig2A_*"):
    os.remove(f)

for f in os.listdir(PROCESSED_DIR):
    if f.endswith(".bed") or f.endswith(".filtered.simple"):
        src = os.path.join(PROCESSED_DIR, f)
        dst = os.path.join(JCVI_DIR, f)
        if not os.path.exists(dst) and not os.path.islink(dst):
            os.symlink(src, dst)

seqids_all = open(os.path.join(PROCESSED_DIR, "seqids_figure2_cleaned.txt")).read().strip().split("\n")
dhl92_fixed = ",".join([c for c in seqids_all[1].split(",") if c != "chr00"])
seqids_all[1] = dhl92_fixed
with open("seqids_fig2A.txt", "w") as f:
    f.write("\n".join(seqids_all[:4]) + "\n")

def write_highlight(fname, sp_a, sp_b):
    genes_a, genes_b = OG[sp_a], OG[sp_b]
    with open(fname, "w") as f:
        for ga in genes_a:
            for gb in genes_b:
                f.write(f"{COLOR_RED}*{ga}\t{ga}\t{gb}\t{gb}\t100\t+\n")

write_highlight("fig2A_Cc_Dl.simple", "ChineseLong", "DHL92")
write_highlight("fig2A_Dl_97.simple", "DHL92", "97103")
write_highlight("fig2A_97_Cp.simple", "97103", "Cpepo")

layout = """# y, xstart, xend, rotation, color, label, va, bed, label_va
0.88, .05, .95, 0, #E41A1C, C. sativus, top, ChineseLong.bed, center
0.64, .05, .95, 0, #FF7F00, C. melo, top, DHL92.bed, center
0.40, .05, .95, 0, #FB9A99, C. lanatus, top, 97103.bed, center
0.16, .05, .95, 0, #CAB2D6, C. pepo, top, Cpepo.bed, center
# Background edges (PF00168 all synteny)
e, 0, 1, ChineseLong.DHL92.filtered.simple
e, 1, 2, DHL92.97103.filtered.simple
e, 2, 3, 97103.Cpepo.filtered.simple
# SRC2 highlights (red)
e, 0, 1, fig2A_Cc_Dl.simple
e, 1, 2, fig2A_Dl_97.simple
e, 2, 3, fig2A_97_Cp.simple
"""
with open("layout_fig2A.csv", "w") as f:
    f.write(layout)

cmd = [
    "python", "-m", "jcvi.graphics.karyotype",
    "--notex", "--font", "Arial",
    "--figsize", "8x6", "--dpi", "600",
    "--nocircles", "--style", "white",
    "--shadestyle", "curve",
    "-o", "Figure2A_cucurbits.pdf",
    "seqids_fig2A.txt", "layout_fig2A.csv",
]
subprocess.run(cmd, check=True)

if os.path.exists("Figure2A_cucurbits.pdf"):
    subprocess.run(["inkscape", "Figure2A_cucurbits.pdf",
                    "--export-filename=Figure2A_cucurbits.svg",
                    "--export-dpi=600"], check=True)
    subprocess.run(["convert", "-density", "600", "Figure2A_cucurbits.pdf",
                    "-quality", "95", "Figure2A_cucurbits.tiff"], check=True)