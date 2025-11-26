# Basic Workflow Example

## 概要

このディレクトリには、Strategic Research Suiteの基本的な使用方法を示す**最小限の実行例**が含まれています。

### 実行内容

1. **サンプルデータ生成**: 100企業×10年のパネルデータを生成
2. **品質チェック**: 欠損値、外れ値、パネルバランスを自動チェック
3. **記述統計**: 平均、標準偏差、最小値、最大値を計算
4. **相関分析**: 主要変数間の相関係数を算出
5. **結果保存**: CSVファイルとレポートを自動保存

## 実行方法

### 前提条件

```bash
# 必要なパッケージ
pip install pandas numpy pytest
```

### 実行

```bash
cd 1-core-workflow/examples/basic_workflow/
python run_example.py
```

### 実行時間

約5秒（100企業×10年=1,000観測値）

## 出力ファイル

実行後、`output/`ディレクトリに以下のファイルが生成されます：

```
output/
├── sample_panel_data.csv         # 生成されたパネルデータ
├── quality_report.txt            # データ品質レポート
├── descriptive_statistics.csv    # 記述統計表
└── correlation_matrix.csv        # 相関行列
```

## 出力例

### コンソール出力

```
================================================================================
STRATEGIC RESEARCH BASIC WORKFLOW EXAMPLE
================================================================================

[Step 1] Data Generation
--------------------------------------------------------------------------------
Generating sample data: 100 firms × 10 years...
✓ Generated 1,000 observations
  - Firms: 100
  - Years: 2013-2022
  - Variables: 8

[Step 2] Data Quality Checks
--------------------------------------------------------------------------------
✓ Quality checks completed:
  - Missing values: 50
  - Panel balance: Balanced
  - Duplicates: 0

[Step 3] Descriptive Statistics
--------------------------------------------------------------------------------
              roa        roe        sales  rd_intensity   leverage   firm_age
count    1000.000   1000.000     1000.000       950.000   1000.000   1000.000
mean        0.050      0.100    30000.123         0.050      0.500     20.123
std         0.020      0.040    20000.456         0.029      0.173      5.678
min         0.001      0.020     1000.789         0.000      0.200     10.000
25%         0.035      0.075    15000.234         0.025      0.350     16.000
50%         0.050      0.100    25000.567         0.050      0.500     20.000
75%         0.065      0.125    40000.890         0.075      0.650     24.000
max         0.120      0.200   150000.123         0.100      0.800     30.000

[Step 4] Correlation Analysis
--------------------------------------------------------------------------------
               roa  rd_intensity  leverage  firm_age
roa          1.000        -0.023    -0.456     0.123
rd_intensity -0.023         1.000    -0.089     0.045
leverage     -0.456        -0.089     1.000    -0.234
firm_age      0.123         0.045    -0.234     1.000

[Step 5] Saving Results
--------------------------------------------------------------------------------
✓ Data saved: output/sample_panel_data.csv
✓ Quality report saved: output/quality_report.txt
✓ Descriptive statistics saved: output/descriptive_statistics.csv
✓ Correlation matrix saved: output/correlation_matrix.csv

================================================================================
WORKFLOW COMPLETED SUCCESSFULLY!
================================================================================

Next steps:
  1. Review quality report: output/quality_report.txt
  2. Examine data: output/sample_panel_data.csv
  3. Proceed to advanced analysis (Phase 7)
```

## データ構造

生成されるパネルデータの構造：

| Column | Type | Description |
|--------|------|-------------|
| firm_id | int | 企業ID (1-100) |
| year | int | 年度 (2013-2022) |
| firm_name | str | 企業名 (Company_001, etc.) |
| roa | float | Return on Assets (総資産利益率) |
| roe | float | Return on Equity (自己資本利益率) |
| sales | float | 売上高 |
| rd_intensity | float | R&D強度 (R&D支出/売上高) |
| leverage | float | レバレッジ (負債比率) |
| firm_age | int | 企業年齢 |

## カスタマイズ

### サンプルサイズの変更

```python
# run_example.py の該当行を編集
df = generate_sample_data(
    n_firms=200,   # 企業数を200に変更
    n_years=15     # 年数を15に変更
)
```

### 変数の追加

```python
# generate_sample_data() 関数に追加
data.append({
    ...
    'market_share': np.random.uniform(0, 0.5),  # 市場シェア
    'export_ratio': np.random.uniform(0, 0.8)   # 輸出比率
})
```

## トラブルシューティング

### ModuleNotFoundError: No module named 'data_quality_checker'

**原因**: Pythonがscriptsディレクトリを見つけられない

**解決策**:
```bash
# run_example.py と同じディレクトリから実行してください
cd 1-core-workflow/examples/basic_workflow/
python run_example.py
```

### 欠損値が多すぎる

**原因**: サンプルデータ生成時にランダムに5%の欠損値を導入

**解決策**: `generate_sample_data()` 関数の該当行を編集
```python
# 欠損値の割合を1%に変更
missing_indices = np.random.choice(
    len(df), 
    size=int(len(df) * 0.01),  # 0.05 → 0.01 に変更
    replace=False
)
```

## 次のステップ

このBasic Workflowを理解したら、以下の高度な例に進んでください：

1. **japan_innovation/** - 日本企業のイノベーション研究（EDINET使用）
2. **esg_performance/** - ESGとパフォーマンスの関係研究（CDP使用）
3. **merger_did/** - M&Aの因果効果分析（Difference-in-Differences）

## 関連ドキュメント

- [Core Workflow SKILL.md](../../SKILL.md) - Phase 1-8の詳細説明
- [Data Quality Checker](../../scripts/data_quality_checker.py) - 品質チェックスクリプト
- [Quality Standards](../../../_shared/data-quality-standards.md) - データ品質基準

---

**作成日**: 2025-11-01  
**最終更新**: 2025-11-01  
**メンテナー**: Strategic Research Suite Team
