# 输入数据说明

## BED 格式
```
{chrom}	{start}	{end}	{id}	{score}	{strand}
```
示例：
```
Csa01	12345	13000	CHL_v3.0_Chr01g01_1	0	+
```

## .filtered.simple 格式
```
{sp1_chrom}	{sp1_start}	{sp1_end}	{sp2_chrom}	{sp2_start}	{sp2_end}	{orientation}	{sp1_id}	{sp2_id}
```

## seqids 格式
每行一个染色体ID：
```
Csa01
Csa02
...
```

## 8种物种文件
- ChineseLong.bed
- DHL92.bed
- 97103.bed
- USVL1VR-Ls.bed
- Cpepo.bed
- Cargyrosperma.bed
- Cmaxima_Rimu.bed
- Cmoschata_Rifu.bed

## 完整数据链
从原始基因组到 Figure 2A：
1. 原始基因组 GFF3 + CDS FASTA
2. `step06_generate_bed.py` → BED
3. `fix_cds_ids.py` → 去除 .1 后缀
4. `jcvi.compara.catalog ortholog` → anchors
5. `step05_convert_anchors.py` → .filtered 格式
6. `jcvi.compara.synteny filter --minspan=30` → .filtered.simple
7. `figure2A_cucurbits_8species.py` → Figure 2A

## 关键脚本
- `02_scripts/pipeline/step06_generate_bed.py` — GFF3 → BED
- `02_scripts/pipeline/fix_cds_ids.py` — CDS ID 修复
- `02_scripts/pipeline/step05_convert_anchors.py` — anchors → .simple
- `02_scripts/figure2A_cucurbits_8species.py` — ★ 绘图核心