# 🧬 SRC2 (PF00168) 共线性分析流水线 — 使用教程

> 手把手教你如何从零生成 Figure 2 的所有输入数据

---

## 📋 目录

1. [准备工作](#1-准备工作你需要什么)
2. [第 1 步：生成 BED 文件](#2-第-1-步生成-bed-文件)
3. [第 2 步：准备 CDS 文件](#3-第-2-步准备-cds-文件)
4. [第 3 步：运行 LAST 比对](#4-第-3-步运行-last-比对)
5. [第 4 步：转换为 SimpleFile 格式](#5-第-4-步转换为-simplefile-格式)
6. [第 5 步：查看结果并绘图](#6-第-5-步查看结果并绘图)
7. [一键运行所有比对](#7-一键运行所有比对)
8. [附录：命令速查表](#8-附录命令速查表)
9. [拓展：SRC2 拷贝数进化的物种选择策略](#9-拓展src2-拷贝数进化的物种选择策略)
10. [一键准备所有物种数据](#10-一键准备所有物种数据)

---

## 1️⃣ 准备工作：你需要什么

### 软件安装

```bash
pip install jcvi

R -e 'install.packages(c("ape","ggtree","ggplot2","RColorBrewer","reshape2","patchwork"))'

sudo apt install inkscape imagemagick
```

### 数据文件

所有物种的基因组数据（GFF3、CDS、蛋白序列）都在：`/data5/qiulei/PPI/data/`

### 工作目录

所有计算结果生成在：`/data5/qiulei/pfam_pipeline/data/processed/PF00168_jcvi_chain/`

---

## 2️⃣ 第 1 步：生成 BED 文件

**BED 文件格式**：`chrID\tgeneID\tstart\tend\t.\tstrand`

```bash
cd /data5/qiulei/01.plant-phylogenomics/C2domain/PF00168/synteny_figures/02_scripts/pipeline
python step06_generate_bed.py PF00168 ChineseLong DHL92 97103 Cpepo
```

非葫芦科物种：
```bash
python regenerate_non_cucurbit_beds.py
```

---

## 3️⃣ 第 2 步：准备 CDS 文件

**关键问题**：CDS 的 ID 和 BED 的 ID 必须一致。有些葫芦科物种的 CDS 文件名带有版本号 `.1`，需要去除。

```bash
cd /data5/qiulei/pfam_pipeline/data/processed/PF00168_jcvi_chain/
python fix_cds_ids.py
```

---

## 4️⃣ 第 3 步：运行 LAST 比对

**核心命令**（对两个物种的 CDS 序列进行两两比对，找到相似的基因对）：

```bash
cd /data5/qiulei/pfam_pipeline/data/processed/PF00168_jcvi_chain/
python -m jcvi.compara.catalog ortholog \
  --dbtype prot --cscore 0.99 --no_strip_names --notex \
  ChineseLong DHL92
```

**用流水线脚本一键跑所有物种对**：
```bash
python step04_run_last_alignment.py PF00168 ChineseLong DHL92 97103 Cpepo
```

---

## 5️⃣ 第 4 步：转换为 SimpleFile 格式

**SimpleFile 格式**（JCVI 的 6 列格式）：`基因A\t基因A\t基因B\t基因B\tscore\tstrand`

```bash
python step05_convert_anchors.py PF00168 ChineseLong DHL92 97103 Cpepo
```

**JCVI 内置过滤**：
```bash
python -m jcvi.compara.synteny filter --minspan=30 --simple A.B.anchors A.B.simple
```

---

## 6️⃣ 第 5 步：查看结果并绘图

```bash
cd /data5/qiulei/01.plant-phylogenomics/C2domain/PF00168/synteny_figures/02_scripts
bash run_all.sh
```

所有 Figure 自动生成到 `03_figures/` 目录。

---

## 7️⃣ 一键运行所有比对

```bash
cd /data5/qiulei/01.plant-phylogenomics/C2domain/PF00168/synteny_figures/02_scripts/pipeline
bash run_jcvi_alignments.sh
```

---

## 8️⃣ 附录：命令速查表

| 步骤 | 命令 | 输入 | 输出 |
|------|------|------|------|
| BED生成 | `python step06_generate_bed.py PF00168 <species...>` | GFF3 | `.bed` |
| BED修正 | `python regenerate_non_cucurbit_beds.py` | GFF3 | 非葫芦科 `.bed` |
| CDS修复 | `python fix_cds_ids.py` | 原始 CDS (带`.1`) | 修复后 CDS (去`.1`) |
| LAST比对 | `python step04_run_last_alignment.py PF00168 <species...>` | CDS | `.last`, `.anchors` |
| LAST批处理 | `bash run_jcvi_alignments.sh` | CDS | `.last`, `.anchors` |
| 格式转换 | `python step05_convert_anchors.py PF00168 <species...>` | `.anchors`+`.last` | `.simple` |
| JCVI过滤 | `python -m jcvi.compara.synteny filter ...` | `.simple` | `.filtered.simple` |
| 绘图(Figure 2-3) | `python ../figure2A_cucurbits.py` | BED + .filtered.simple | PDF/SVG/TIFF |
| 绘图(Figure 4-5) | `Rscript ../figure4_copy_number.R` | OrthoFinder结果 | PDF |
| 一键到底 | `bash ../run_all.sh` | 全部输入 | 全部Figure |

---

## 9️⃣ 拓展：SRC2 拷贝数进化的物种选择策略

### 问题：拟南芥中 SRC2 是单拷贝，它在其他类群中的拷贝数如何变化？

```
被子植物 Angiosperms
├── 基部被子植物
│   └── amborella_trichopoda (无油樟) — SRC2=1拷贝
├── 核心真双子叶植物
│   ├── 十字花科 Brassicaceae
│   │   ├── arabidopsis_thaliana  ★ 参考物种(1拷贝)
│   │   ├── brassica_rapa         ★ 白菜(三倍体化后拷贝数)
│   │   └── brassica_napus        ★ 异源四倍体(加倍后拷贝数)
│   ├── 茄科 Solanaceae
│   │   ├── solanum_lycopersicum  ★ 参考物种(3拷贝)
│   │   ├── capsicum_annuum       ★ 辣椒
│   │   └── solanum_tuberosum     ★ 马铃薯
│   ├── 葫芦科 Cucurbitaceae (核心研究对象)
│   │   ├── ChineseLong (黄瓜)    ★ 2拷贝
│   │   ├── DHL92 (甜瓜)          ★ 2拷贝
│   │   ├── 97103 (西瓜)          ★ 2拷贝
│   │   └── Cpepo (南瓜)          ★ 5拷贝(串联重复扩增)
│   └── 蔷薇类 Fabids
│       ├── glycine_max (大豆)    ★ 豆科
│       └── populus_trichocarpa   ★ 杨树
└── 单子叶植物 Monocots
    ├── oryza_sativa (水稻)       ★ 1拷贝
    └── zea_mays (玉米)           ★ 古四倍体
```

---

## 🔟 一键准备所有物种数据

如果要从头准备**全部22个物种**的 BED + CDS 文件：

```bash
cd /data5/qiulei/01.plant-phylogenomics/C2domain/PF00168/synteny_figures/02_scripts/pipeline
bash prepare_all_species_data.sh
```

| 分组 | 物种 | 数量 |
|------|------|------|
| ① 十字花科 | arabidopsis_thaliana, arabidopsis_halleri, arabis_alpina, brassica_rapa, brassica_napus | 5种 |
| ② 茄科 | solanum_lycopersicum, capsicum_annuum, nicotiana_attenuata, solanum_tuberosum | 4种 |
| ③ 葫芦科 | ChineseLong, DHL92, 97103, Cpepo | 4种 |
| ④ 禾本科 | oryza_sativa, brachypodium_distachyon, sorghum_bicolor, zea_mays | 4种 |
| ⑤ 蔷薇类 | glycine_max, eucalyptus_grandis, populus_trichocarpa, vitis_vinifera | 4种 |
| ⑥ 基部被子植物 | amborella_trichopoda | 1种 |

**输出目录**: `/data5/qiulei/pfam_pipeline/data/processed/PF00168_jcvi_chain/