---
name: nl-data-analyst
description: |
  自然言語によるデータ分析スキル。データの前処理（クレンジング）、統計分析（探索的分析）、可視化を自然言語クエリで実行。
  トリガー：「データ分析」「CSV分析」「データクレンジング」「EDA」「探索的分析」「可視化」「このデータを分析」「データプロファイリング」
  対応形式：CSV, Excel, JSON, Parquet, TSV
  主要機能：(1)自動データプロファイリング (2)自然言語クエリによる分析 (3)対話的データクレンジング (4)統計分析・可視化
---

# NL Data Analyst（自然言語データ分析スキル）

Claudeの推論能力を活用し、Julius AIライクな自然言語データ分析を実現するスキル。

## コアワークフロー

### Phase 1: データ読み込みとプロファイリング（自動実行）

1. **データ読み込み**
```python
import pandas as pd
import numpy as np

# ファイル形式に応じた読み込み
df = pd.read_csv(path)  # or read_excel, read_json, read_parquet
```

2. **即座にプロファイリングスクリプト実行**
```bash
python /path/to/skill/scripts/data_profiler.py <file_path>
```

プロファイリング出力内容：
- 基本情報（行数、列数、メモリ使用量）
- 各列の型、欠損率、ユニーク値数
- 数値列の統計量（平均、中央値、標準偏差、四分位）
- カテゴリ列の上位値分布
- 潜在的な品質問題の検出

### Phase 2: 自然言語クエリの解釈と実行

ユーザーの自然言語クエリを以下のステップで処理：

1. **意図分類**
   - データ探索（what/who/how many）
   - データ変換（clean/filter/merge）
   - 統計分析（correlation/distribution/trend）
   - 可視化（plot/chart/graph）

2. **Schema Linking**（重要）
   - クエリ内の概念をデータフレームの列名にマッピング
   - 曖昧な場合は確認を求める

3. **コード生成と実行**
   - Chain-of-Thought形式で分析手順を説明
   - Pythonコード生成・実行
   - 結果の自然言語での説明

### Phase 3: 対話的修正

結果が期待と異なる場合：
- ユーザーフィードバックを受け取る
- 修正コードを生成
- 再実行して結果を提示

## 分析パターンライブラリ

### データクレンジング

```python
# 欠損値処理
df['col'].fillna(df['col'].median(), inplace=True)  # 数値
df['col'].fillna(df['col'].mode()[0], inplace=True)  # カテゴリ
df.dropna(subset=['critical_col'], inplace=True)     # 削除

# 重複削除
df.drop_duplicates(subset=['key_cols'], keep='first', inplace=True)

# 型変換
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

# 外れ値処理（IQR法）
Q1, Q3 = df['col'].quantile([0.25, 0.75])
IQR = Q3 - Q1
df = df[(df['col'] >= Q1 - 1.5*IQR) & (df['col'] <= Q3 + 1.5*IQR)]
```

### 探索的分析（EDA）

```python
# 基本統計
df.describe(include='all')
df.info()

# 相関分析
df.select_dtypes(include='number').corr()

# グループ集計
df.groupby('category').agg({
    'value': ['mean', 'sum', 'count'],
    'other': 'nunique'
})

# クロス集計
pd.crosstab(df['cat1'], df['cat2'], margins=True)

# 時系列分析
df.set_index('date').resample('M').mean()
```

### 可視化

```python
import matplotlib.pyplot as plt
import seaborn as sns

# 日本語フォント設定
plt.rcParams['font.family'] = 'DejaVu Sans'

# 分布
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data=df, x='col', kde=True, ax=ax)
plt.savefig('/mnt/user-data/outputs/distribution.png', dpi=150, bbox_inches='tight')

# 相関ヒートマップ
fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0, ax=ax)
plt.savefig('/mnt/user-data/outputs/correlation.png', dpi=150, bbox_inches='tight')

# 時系列
fig, ax = plt.subplots(figsize=(14, 6))
df.plot(x='date', y='value', ax=ax)
plt.savefig('/mnt/user-data/outputs/timeseries.png', dpi=150, bbox_inches='tight')

# カテゴリ比較
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=df, x='category', y='value', ax=ax)
plt.xticks(rotation=45)
plt.savefig('/mnt/user-data/outputs/barplot.png', dpi=150, bbox_inches='tight')
```

## 自然言語クエリ例と対応

| ユーザークエリ | 意図分類 | 実行内容 |
|--------------|---------|---------|
| 「欠損値を確認して」 | 探索 | `df.isnull().sum()` |
| 「売上の分布を見せて」 | 可視化 | ヒストグラム生成 |
| 「カテゴリ別の平均を出して」 | 分析 | groupby + mean |
| 「外れ値を除去して」 | 変換 | IQR法による除去 |
| 「日付列をdatetime型に変換」 | 変換 | `pd.to_datetime()` |
| 「上位10件の顧客を表示」 | 探索 | sort + head |
| 「相関が強い変数は？」 | 分析 | 相関行列 + 閾値フィルタ |

## 出力形式

### 分析結果の提示

1. **サマリー**：主要な発見を箇条書き
2. **詳細データ**：関連する数値・表
3. **可視化**：グラフを`/mnt/user-data/outputs/`に保存しリンク提供
4. **次のステップ提案**：追加分析の推奨

### 生成コードの提示

```python
# === 実行コード ===
# [説明コメント]
code_here()
```

## 制約と注意点

- **大規模データ**：100万行超の場合はサンプリングを提案
- **機密データ**：個人情報を含む列は分析前に確認
- **複雑なクエリ**：段階的に分解して実行
- **エラー発生時**：エラー内容を説明し修正案を提示

## 追加リソース

- `scripts/data_profiler.py`：自動プロファイリングスクリプト
- `scripts/cleaner.py`：汎用クレンジングユーティリティ
- `scripts/visualizer.py`：標準可視化テンプレート
- `references/analysis_patterns.md`：詳細な分析パターン集
