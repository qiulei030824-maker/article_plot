# PF00168 JCVI 共线性分析完整管线使用指南

## 1. 准备环境
```bash
conda activate jcvi
```

## 2. 数据准备
数据路径：/data5/qiulei/PPI/

物种目录结构：
```
PPI/
├── data/ChineseLong/   # 黄瓜 Chinese Long v3
├── data/DHL92/         # 甜瓜 DHL92 v3.6
├── data/97103/         # 西瓜 97103 v2
...
└── PF00168/JCVI/       # 工作目录
```

## 3. BED 文件生成
```bash
cd /data5/qiulei/PPI/PF00168/JCVI
python ../02_scripts/pipeline/step06_generate_bed.py PF00168 ChineseLong DHL92 97103 Cpepo
```

## 4. CDS ID 修复
```bash
python ../02_scripts/pipeline/fix_cds_ids.py
```

## 5. LAST 比对
```bash
python ../02_scripts/pipeline/step04_run_last_alignment.py
```

## 6. 转换为 .simple 格式
```bash
python ../02_scripts/pipeline/step05_convert_anchors.py PF00168 ChineseLong DHL92 97103 Cpepo
```

## 7. 过滤
```bash
python -m jcvi.compara.synteny filter --minspan=30 --simple A.B.anchors A.B.simple
```

## 8. 绘图
```bash
python ../02_scripts/figure2A_cucurbits_8species.py
```
