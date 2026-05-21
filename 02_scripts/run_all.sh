#!/bin/bash
# run_all.sh — 一键运行所有SRC2共线性图

BASE_DIR="/data5/qiulei/01.plant-phylogenomics/C2domain/PF00168/synteny_figures"
SCRIPT_DIR="${BASE_DIR}/02_scripts"
FIGURE_DIR="${BASE_DIR}/03_figures"

cd "${SCRIPT_DIR}"

echo "=========================================="
echo " SRC2 (PF00168) Synteny Figures — Auto Run"
echo "=========================================="
echo ""

# Figure 2A — 葫芦科共线性
echo "[1/5] Figure 2A: Cucurbit macrosynteny ..."
python3 figure2A_cucurbits.py 2>&1 | grep -E '✅|seqids'
cp -f *.pdf *.svg *.tiff 2>/dev/null; true

# Figure 2B — 被子植物保守共线性
echo "[2/5] Figure 2B: Deep conservation ..."
python3 figure2B_conservation.py 2>&1 | grep '✅'
cp -f *.pdf *.svg *.tiff 2>/dev/null; true

# Figure 3 — 微共线性
echo "[3/5] Figure 3: Microsynteny ..."
python3 figure3_microsynteny.py 2>&1 | grep '✅'
cp -f *.pdf 2>/dev/null; true

# Figure 4 — 拷贝数热图
echo "[4/5] Figure 4: Copy number heatmap ..."
Rscript figure4_copy_number.R 2>&1 | tail -1
cp -f *.pdf 2>/dev/null; true

# Figure 5 — 复制事件
echo "[5/5] Figure 5: Duplication events ..."
Rscript figure5_duplication.R 2>&1 | tail -1
cp -f *.pdf 2>/dev/null; true

# 移动所有输出图到03_figures/
echo ""
echo "--- Moving figures to ${FIGURE_DIR}/ ---"
mv -f Figure*.pdf Figure*.svg Figure*.tiff "${FIGURE_DIR}/" 2>/dev/null

echo ""
echo "=========================================="
echo " ✅ 全部完成！图片位于:"
ls -lh "${FIGURE_DIR}/"
echo "=========================================="