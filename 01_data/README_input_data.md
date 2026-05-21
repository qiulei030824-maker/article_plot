# 01_data/ — 输入数据说明

这个目录包含了运行 Figure 2~5 绘图脚本所需的**所有输入文件**。

## BED 文件 (基因位置信息)

格式 (6列 JCVI BED): `染色体ID\t基因ID\t起始位置\t终止位置\t方向\t备注`

| 文件名 | 物种 | 染色体 |
|--------|------|--------|
| `ChineseLong.bed` | 黄瓜 (C. sativus) | chr1-chr7 |
| `DHL92.bed` | 甜瓜 (C. melo) | chr00-chr12 |
| `97103.bed` | 西瓜 (C. lanatus) | Cla97Chr01-11 |
| `Cpepo.bed` | 南瓜 (C. pepo) | Cp4.1LG01-20 |
| `USVL1VR-Ls.bed` | 葫芦 (L. siceraria) | chr01-11 |
| `Cargyrosperma.bed` | C. argyrosperma | Carg_Chr01-20 |
| `Cmaxima_Rimu.bed` | C. maxima | Chr01-20 |
| `Cmoschata_Rifu.bed` | C. moschata | Chr01-20 |

**生成脚本**: `02_scripts/pipeline/step06_generate_bed.py`

## 共线性结果 (.filtered.simple)

格式 (6列 JCVI SimpleFile): `基因A\t基因A\t基因B\t基因B\tscore\t方向`

| 文件 | 物种对 |
|------|--------|
| `ChineseLong.DHL92.filtered.simple` | 黄瓜 ↔ 甜瓜 |
| `DHL92.97103.filtered.simple` | 甜瓜 ↔ 西瓜 |
| `97103.Cpepo.filtered.simple` | 西瓜 ↔ 南瓜 |
| `97103.USVL1VR-Ls.filtered.simple` | 西瓜 ↔ 葫芦 |
| `USVL1VR-Ls.Cpepo.filtered.simple` | 葫芦 ↔ 南瓜 |
| `Cpepo.Cargyrosperma.filtered.simple` | 南瓜 ↔ C. argyrosperma |
| `Cargyrosperma.Cmaxima_Rimu.filtered.simple` | C. argyrosperma ↔ C. maxima |
| `Cmaxima_Rimu.Cmoschata_Rifu.filtered.simple` | C. maxima ↔ C. moschata |

**生成流水线**:
1. CDS ID修复: `fix_cds_ids.py`
2. LAST比对: `step04_run_last_alignment.py`
3. .simple转换: `step05_convert_anchors.py`
4. JCVI过滤: `python -m jcvi.compara.synteny filter --minspan=30`

## 染色体配置 (seqids)

| 文件 | 用途 |
|------|------|
| `seqids_figure2_cleaned.txt` | 8物种完整染色体列表 |
| `seqids_fig2A.txt` | Figure 2A 4个葫芦科 |
| `seqids_fig2B.txt` | Figure 2B 5个被子植物 |

## 完整数据链

```
GFF3/FASTA → step06_generate_bed.py → .bed
                                    → seqids.txt
                                    → .cds → fix_cds_ids.py → step04_run_last_alignment.py
                                                             → .last + .anchors
                                                             → step05_convert_anchors.py
                                                             → .simple → synteny filter
                                                                       → .filtered.simple
                                                                       → jcvi karyotype → Figure 2A
```

## 关键脚本路径

| 步骤 | 脚本 |
|------|------|
| BED生成 | `02_scripts/pipeline/step06_generate_bed.py` |
| CDS ID修复 | `02_scripts/pipeline/fix_cds_ids.py` |
| LAST比对 | `02_scripts/pipeline/step04_run_last_alignment.py` |
| .simple转换 | `02_scripts/pipeline/step05_convert_anchors.py` |
| Figure 2A | `02_scripts/figure2A_cucurbits_8species.py` |
| 一键运行 | `02_scripts/run_all.sh` |