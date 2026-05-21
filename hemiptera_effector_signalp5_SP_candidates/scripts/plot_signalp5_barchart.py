#!/usr/bin/env python3
"""
Bar chart: SignalP5 SP+ candidate counts per species
Organized by taxonomic group to show evolutionary relationships.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['font.size'] = 7
plt.rcParams['axes.linewidth'] = 0.6
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['legend.frameon'] = False

PROJ = Path("/data5/qiulei/coevolution/hemiptera_effector_erc")
OUTDIR = PROJ / "data/effectors/signalp5_results"

sp_group = {}
sp_authority = {}
with open(PROJ / "data/insect_local_status.tsv") as f:
    for i, line in enumerate(f):
        if i == 0:
            continue
        parts = line.strip().split("\t")
        if len(parts) >= 3:
            sp_group[parts[0]] = parts[2]
            sp_authority[parts[0]] = True if len(parts) >=5 and parts[4].strip() else False

GROUP_ORDER = [
    "phylloxera", "adelgid", "aphid",
    "planthopper", "leafhopper", "froghopper",
    "cicada", "lanternfly", "psyllid", "whitefly",
    "mealybug", "stink_bug", "mirid_bug", "bed_bug", "predatory_bug",
    "kissing_bug", "water_strider",
    "outgroup_thrips", "outgroup_hym", "outgroup_psocodea"
]

PALETTE = {
    "phylloxera":     "#0F4D92",
    "adelgid":        "#3775BA",
    "aphid":          "#AADCA9",
    "planthopper":    "#8BCF8B",
    "leafhopper":     "#DDF3DE",
    "froghopper":     "#42949E",
    "cicada":         "#B64342",
    "lanternfly":     "#F6CFCB",
    "psyllid":        "#E9A6A1",
    "whitefly":       "#EA84DD",
    "mealybug":       "#9A4D8E",
    "stink_bug":      "#767676",
    "mirid_bug":      "#CFCECE",
    "bed_bug":        "#4D4D4D",
    "predatory_bug":  "#272727",
    "kissing_bug":    "#FFD700",
    "water_strider":  "#E4CCD8",
    "outgroup_thrips":"#B4C0E4",
    "outgroup_hym":   "#7884B4",
    "outgroup_psocodea":"#484878",
}

sp_counts = {}
for sp_dir in sorted(OUTDIR.iterdir()):
    if not sp_dir.is_dir():
        continue
    sp = sp_dir.name
    smry = sp_dir / f"{sp}_summary.signalp5"
    if not smry.exists():
        continue
    n = 0
    with open(smry) as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = line.strip().split("\t")
            if len(parts) >= 4:
                try:
                    if float(parts[2]) > 0.5:
                        n += 1
                except ValueError:
                    pass
    sp_counts[sp] = n

ordered_species = []
for grp in GROUP_ORDER:
    for sp in sorted(sp_counts.keys()):
        if sp_group.get(sp) == grp:
            ordered_species.append((sp, grp, sp_counts[sp]))

names = [x[0] for x in ordered_species]
groups = [x[1] for x in ordered_species]
counts = [x[2] for x in ordered_species]
colors = [PALETTE.get(g, "#CFCECE") for g in groups]

fig, ax = plt.subplots(figsize=(10.5, 4.5))

x = np.arange(len(names))
bars = ax.bar(x, counts, color=colors, edgecolor='white', linewidth=0.3, width=0.75)

for i, (bar, val) in enumerate(zip(bars, counts)):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100,
            f'{val}', ha='center', va='bottom', fontsize=4.5, rotation=45)

ax.set_ylabel('SP+ candidates', fontsize=7)
ax.set_xticks(x)
ax.set_xticklabels(names, rotation=45, ha='right', fontsize=5)

ax2 = ax.twiny()
ax2.set_xlim(ax.get_xlim())

group_boundaries = {}
for i, g in enumerate(groups):
    group_boundaries.setdefault(g, []).append(i)

gap = 0
y_top = max(counts) * 1.08
for grp in GROUP_ORDER:
    if grp not in group_boundaries:
        continue
    idxs = group_boundaries[grp]
    start = idxs[0]
    end = idxs[-1]
    mid = (start + end) / 2
    color = PALETTE.get(grp, '#CFCECE')
    ax.text(mid, y_top + gap * 15, grp.replace('_', ' '),
            ha='center', va='bottom', fontsize=5.5, fontweight='bold',
            color=color, rotation=30)
    ax.plot([start - 0.4, start - 0.4, end + 0.4, end + 0.4],
            [y_top - 200 + gap*15, y_top + gap*15, y_top + gap*15, y_top - 200 + gap*15],
            color=color, linewidth=0.8, clip_on=False)
    gap += 1

ax.set_ylim(0, max(counts) * 1.3)

from matplotlib.patches import Patch
legend_elements = []
for grp in GROUP_ORDER:
    if grp in group_boundaries:
        legend_elements.append(
            Patch(facecolor=PALETTE.get(grp, '#CFCECE'), edgecolor='none',
                  label=grp.replace('_', ' '))
        )

ax.legend(handles=legend_elements, loc='upper center',
          bbox_to_anchor=(0.5, -0.22), ncol=7, fontsize=5.5,
          handlelength=1, handleheight=1)

outdir = PROJ / "figures"
outdir.mkdir(exist_ok=True)

fig.tight_layout()
fig.savefig(str(outdir / "signalp5_sp_counts.svg"), bbox_inches='tight')
fig.savefig(str(outdir / "signalp5_sp_counts.png"), dpi=600, bbox_inches='tight')
plt.close(fig)
print(f"Saved: {outdir / 'signalp5_sp_counts.svg'}")
print(f"Saved: {outdir / 'signalp5_sp_counts.png'}")