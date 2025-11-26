# Strategic Management Research Hub - Data Mining Quick Start Guide

**Version**: 3.1  
**Date**: 2025-11-01  
**Author**: Strategic Management Research Hub

---

## 📖 目次

1. [概要](#概要)
2. [インストール](#インストール)
3. [5分で始めるデータマイニング](#5分で始めるデータマイニング)
4. [基本的な使い方](#基本的な使い方)
5. [高度な使い方](#高度な使い方)
6. [トラブルシューティング](#トラブルシューティング)
7. [FAQ](#faq)

---

## 概要

本格的なデータマイニング分析を**コマンド1つ**で実行できる統合パイプライン。

### 🎯 主要機能

1. **戦略的グループ分析** - Porter (1980) の理論に基づく企業グループ化
2. **パフォーマンス予測** - Random Forest, XGBoost, LightGBM による業績予測
3. **特徴量重要度** - SHAP, Permutation Importance による変数重要度分析
4. **異常検知** - Isolation Forest による戦略的アウトライアの特定
5. **因果推論** - Double Machine Learning による因果効果推定
6. **時系列分析** - 戦略的変数の時系列パターン発見
7. **統合レポート** - Publication-Ready なHTMLレポート自動生成
8. **LaTeX表出力** - 論文投稿用の表を自動生成

---

## インストール

### ステップ1: Python環境の準備

```bash
# Python 3.9以上を推奨
python --version

# 仮想環境の作成（推奨）
python -m venv datamining_env

# 仮想環境の有効化
# macOS/Linux:
source datamining_env/bin/activate
# Windows:
datamining_env\Scripts\activate
```

### ステップ2: 必要なパッケージのインストール

#### 🚀 最小インストール（5分）

```bash
pip install pandas numpy scikit-learn statsmodels matplotlib seaborn
```

これで以下が使用可能：
- 戦略的グループ分析
- 基本的なパフォーマンス予測
- 異常検知

#### 🔥 推奨インストール（10分）- 完全機能

```bash
cd /Users/changu/Desktop/研究/skills/user/strategic-management-research-hub
pip install -r requirements_datamining.txt
```

これで以下が追加で使用可能：
- XGBoost, LightGBM（高度なML）
- SHAP（説明可能AI）
- EconML（因果推論）
- UMAP（高度な可視化）

### ステップ3: インストール確認

```bash
python -c "import pandas, sklearn, matplotlib; print('✅ コアパッケージOK')"

# フル機能の確認
python -c "import xgboost, shap, econml; print('✅ 全パッケージOK')"
```

---

## 5分で始めるデータマイニング

### 🚀 最速実行（1コマンド）

```python
from scripts.comprehensive_datamining_pipeline import ComprehensiveDataMiningPipeline

# 1. パイプライン初期化
pipeline = ComprehensiveDataMiningPipeline(
    data_path='./data/final/analysis_panel.dta',
    output_dir='./my_first_analysis/'
)

# 2. 全自動実行
results = pipeline.run_complete_analysis()

# 3. 結果の確認
print(f"✅ 完了！レポート: {pipeline.output_dir / 'comprehensive_report_*.html'}")
```

**これだけで以下が実行されます**：
- データ読み込み＆検証
- 8種類のデータマイニング分析
- 30種類以上のグラフ生成
- HTMLレポート生成
- LaTeX表出力

### 📊 実行時間の目安

| データサイズ | 実行時間 | RAM使用量 |
|-------------|---------|----------|
| ~1,000観測   | 2-5分    | < 1GB    |
| ~10,000観測  | 10-20分  | 2-4GB    |
| ~100,000観測 | 30-60分  | 8-16GB   |

---

## 基本的な使い方

### 📁 ステップ1: データの準備

**必須変数**：
- `gvkey` (企業ID) ※変数名は変更可能
- `year` (年次) ※変数名は変更可能

**推奨変数**：
- `roa` または `roe` (パフォーマンス指標)
- `rd_intensity` (R&D集約度)
- `capital_intensity` (資本集約度)
- `firm_size` (企業規模)
- `leverage` (財務レバレッジ)

**データ形式**：
- Stata (.dta)
- CSV (.csv)
- Parquet (.parquet)

### 🎛️ ステップ2: 設定のカスタマイズ（オプション）

```python
from scripts.comprehensive_datamining_pipeline import DataMiningConfig

# カスタム設定の作成
config = DataMiningConfig(
    data_path='./data/final/my_data.dta',
    output_dir='./custom_analysis/',
    
    # 戦略的特徴量の指定
    strategic_features=[
        'rd_intensity',
        'patent_intensity',
        'organizational_slack'
    ],
    
    # パフォーマンス指標
    performance_target='tobin_q',
    
    # クラスタ数の固定（自動決定の場合はNone）
    n_clusters=4,
    
    # 使用するMLモデル
    prediction_models=['rf', 'xgboost', 'ensemble'],
    
    # 計算設定
    random_seed=42,
    n_jobs=-1  # 全コア使用
)

# パイプライン実行
pipeline = ComprehensiveDataMiningPipeline(config=config)
results = pipeline.run_complete_analysis()
```

### 📊 ステップ3: 結果の確認

```python
# データサマリー
print(results['data_summary'])

# 戦略的グループ
print(f"クラスタ数: {results['strategic_groups']['n_clusters']}")
print(results['strategic_groups']['cluster_profiles'])

# パフォーマンス予測
best_model = results['performance_prediction']['best_model']
best_r2 = results['performance_prediction']['model_results'][best_model]['test_r2']
print(f"最良モデル: {best_model} (R² = {best_r2:.4f})")

# 特徴量重要度
print("Top 5 重要特徴量:")
print(results['feature_importance']['importance_df'].head())
```

---

## 高度な使い方

### 🔬 段階的実行（細かい制御）

```python
pipeline = ComprehensiveDataMiningPipeline(
    data_path='./data/final/analysis_panel.dta'
)

# Phase 1: データ読み込み
pipeline.load_and_validate_data()

# Phase 2: 戦略的グループ分析のみ
sg_results = pipeline.run_strategic_group_analysis(
    features=['rd_intensity', 'capital_intensity', 'international_sales'],
    n_clusters=4,
    method='kmeans'
)

# Phase 3: パフォーマンス予測のみ
pred_results = pipeline.run_performance_prediction(
    target='roa',
    features=['rd_intensity', 'firm_size', 'leverage'],
    models=['rf', 'xgboost']
)

# Phase 4: 特徴量重要度のみ
fi_results = pipeline.run_feature_importance_analysis()

# Phase 5: 異常検知のみ
anomaly_results = pipeline.run_anomaly_detection(
    features=['rd_intensity', 'capital_intensity'],
    contamination=0.05
)

# Phase 8: レポート生成
report_path = pipeline.generate_comprehensive_report()
```

### 🔥 因果推論（Double Machine Learning）

```python
config = DataMiningConfig(
    data_path='./data/final/analysis_panel.dta',
    
    # 因果推論の設定
    treatment_var='rd_intensity',  # 処置: R&D投資
    outcome_var='roa_lead1',       # 結果: 翌年のROA
    causal_method='dml',
    
    control_variables=[
        'firm_size', 'firm_age', 'leverage',
        'industry_concentration'
    ]
)

pipeline = ComprehensiveDataMiningPipeline(config=config)
pipeline.load_and_validate_data()

# 因果推論実行
causal_results = pipeline.run_causal_inference()

print(f"平均処置効果 (ATE): {causal_results['ate']:.4f}")
print(f"95% CI: {causal_results['ate_ci']}")
print(f"P値: {causal_results['p_value']:.4f}")
```

### 🎨 クラスタリング手法の比較

```python
methods = ['kmeans', 'hierarchical', 'dbscan']

for method in methods:
    results = pipeline.run_strategic_group_analysis(
        features=['rd_intensity', 'capital_intensity'],
        method=method
    )
    
    print(f"{method}: シルエットスコア = {results['silhouette_score']:.4f}")
```

### 📈 複数のパフォーマンス指標の予測

```python
targets = ['roa', 'roe', 'tobin_q', 'sales_growth']

for target in targets:
    results = pipeline.run_performance_prediction(
        target=target,
        features=['rd_intensity', 'firm_size', 'leverage']
    )
    
    best_r2 = results['model_results'][results['best_model']]['test_r2']
    print(f"{target}: R² = {best_r2:.4f}")
```

---

## 設定ファイルの使用

### YAMLファイルでの設定管理

```bash
# 設定ファイルのコピー
cp configs/datamining_full_config.yaml configs/my_config.yaml

# 設定ファイルを編集
nano configs/my_config.yaml
```

```yaml
# configs/my_config.yaml

data_path: "./data/final/my_panel.dta"
output_dir: "./my_output/"

strategic_features:
  - "rd_intensity"
  - "capital_intensity"
  - "advertising_intensity"

performance_target: "roa"
n_clusters: null  # 自動決定
prediction_models: ["rf", "xgboost", "lightgbm"]
```

```python
# YAMLファイルから実行
from scripts.comprehensive_datamining_pipeline import ComprehensiveDataMiningPipeline

pipeline = ComprehensiveDataMiningPipeline(
    config_path='./configs/my_config.yaml'
)

results = pipeline.run_complete_analysis()
```

---

## 出力ファイル

### 📂 ディレクトリ構造

```
output_dir/
├── comprehensive_report_YYYYMMDD_HHMMSS.html  # 統合HTMLレポート
├── figures/
│   ├── strategic_groups.png                    # 戦略的グループの可視化
│   ├── feature_importance.png                  # 特徴量重要度
│   ├── anomaly_detection.png                   # 異常検知
│   └── temporal_patterns.png                   # 時系列パターン
├── tables/
│   ├── strategic_groups_profiles.tex           # LaTeX表
│   └── model_comparison.tex                    # モデル比較表
├── models/
│   └── strategic_groups_model.pkl              # 保存されたモデル
└── logs/
    └── pipeline_YYYYMMDD_HHMMSS.log            # 実行ログ
```

### 📊 HTMLレポートの内容

1. **データサマリー** - 観測数、企業数、分析期間
2. **戦略的グループ分析** - クラスタプロファイル、可視化
3. **パフォーマンス予測** - モデル比較、予測精度
4. **特徴量重要度** - 重要度ランキング、可視化
5. **異常検知** - 異常値の特定、可視化
6. **実行時間** - 各フェーズの所要時間

---

## トラブルシューティング

### ❌ エラー: ModuleNotFoundError

```bash
# 不足パッケージのインストール
pip install pandas numpy scikit-learn

# または
pip install -r requirements_datamining.txt
```

### ❌ エラー: FileNotFoundError

```python
# データパスの確認
from pathlib import Path

data_path = './data/final/analysis_panel.dta'
print(f"ファイル存在: {Path(data_path).exists()}")
```

### ❌ エラー: KeyError (変数が見つからない)

```python
# データの変数を確認
import pandas as pd
df = pd.read_stata('./data/final/analysis_panel.dta')
print(df.columns.tolist())

# 変数名を設定で変更
config = DataMiningConfig(
    data_path='./data/final/analysis_panel.dta',
    firm_id='company_id',  # gvkey → company_id
    time_var='fiscal_year'  # year → fiscal_year
)
```

### ❌ エラー: MemoryError (メモリ不足)

```python
# サンプルサイズを削減
import pandas as pd
df = pd.read_stata('./data/final/analysis_panel.dta')
df_sample = df.sample(n=5000, random_state=42)
df_sample.to_csv('./data/final/sample.csv', index=False)

# サンプルデータで実行
pipeline = ComprehensiveDataMiningPipeline(
    data_path='./data/final/sample.csv'
)
```

### ❌ 警告: EconML not installed

```bash
# 因果推論を使用しない場合は無視してOK
# 使用する場合は以下でインストール
pip install econml

# またはconda経由
conda install -c conda-forge econml
```

---

## FAQ

### Q1: どのくらいのデータサイズまで対応？

**A**: 推奨は100,000観測まで。それ以上はサンプリングまたはDaskの使用を推奨。

### Q2: Jupyter Notebookで使用できる？

**A**: はい、完全対応。

```python
# Jupyter Notebookでの使用例
from scripts.comprehensive_datamining_pipeline import ComprehensiveDataMiningPipeline

pipeline = ComprehensiveDataMiningPipeline(
    data_path='./data/final/analysis_panel.dta',
    output_dir='./notebook_output/'
)

results = pipeline.run_complete_analysis()
```

### Q3: 既存のStata/Rコードと統合できる？

**A**: はい、可能です。

```python
# Stataファイルの読み込み
import pandas as pd
df = pd.read_stata('./data/final/stata_output.dta')

# Python分析実行
pipeline = ComprehensiveDataMiningPipeline(...)
results = pipeline.run_complete_analysis()

# 結果をStata形式で保存
results_df = pipeline.data_cleaned
results_df.to_stata('./data/final/python_output.dta')
```

### Q4: 複数のデータセットを一度に処理できる？

**A**: はい、バッチ処理が可能です。

```python
datasets = [
    './data/final/manufacturing.dta',
    './data/final/services.dta',
    './data/final/tech.dta'
]

for data_path in datasets:
    pipeline = ComprehensiveDataMiningPipeline(
        data_path=data_path,
        output_dir=f'./batch_output/{Path(data_path).stem}/'
    )
    pipeline.run_complete_analysis()
```

### Q5: 結果を論文に使用できる品質？

**A**: はい、Publication-Ready です。

- LaTeX表の自動生成
- 高解像度図（300 DPI）
- APA/MLA形式の引用情報
- 完全な再現性（乱数シード固定）
- 詳細な実行ログ

### Q6: クラウド（AWS, GCP）で実行できる？

**A**: はい、対応しています。

```bash
# Dockerコンテナでの実行
docker run -v $(pwd)/data:/data \
           -v $(pwd)/output:/output \
           python:3.11 \
           python scripts/comprehensive_datamining_pipeline.py \
           --data /data/analysis_panel.dta \
           --output /output/
```

---

## 次のステップ

1. **実行例を試す**
   ```bash
   python scripts/datamining_quickstart_examples.py
   ```

2. **詳細ガイドを読む**
   - [DATAMINING_GUIDE.md](./DATAMINING_GUIDE.md) - 全手法の詳細解説
   - [SKILL.md](./SKILL.md) - 研究ワークフロー全体

3. **カスタマイズする**
   - `configs/datamining_full_config.yaml` を編集
   - 独自の戦略的特徴量を追加
   - 因果推論の設定をカスタマイズ

4. **コミュニティに参加**
   - Issue報告・機能要望: GitHub Issues
   - 質問・ディスカッション: GitHub Discussions

---

## 引用

このツールを使用した研究を公開する場合は、以下の形式での引用を推奨します：

**APA形式**:
```
Strategic Management Research Hub. (2025). Comprehensive Data Mining Pipeline 
for Strategic Management Research (Version 3.1) [Computer software]. 
https://github.com/your-org/strategic-management-research-hub
```

**BibTeX**:
```bibtex
@software{strategic_datamining_2025,
  author = {{Strategic Management Research Hub}},
  title = {Comprehensive Data Mining Pipeline for Strategic Management Research},
  version = {3.1},
  year = {2025},
  url = {https://github.com/your-org/strategic-management-research-hub}
}
```

---

## ライセンス

MIT License - 学術研究・商用利用ともに自由に使用可能

---

## サポート

- **ドキュメント**: [DATAMINING_GUIDE.md](./DATAMINING_GUIDE.md)
- **例**: [scripts/datamining_quickstart_examples.py](./scripts/datamining_quickstart_examples.py)
- **テスト**: [tests/test_datamining_pipeline.py](./tests/test_datamining_pipeline.py)

---

**Strategic Management Research Hub v3.1**  
*Empowering Strategic Management Research with Advanced Data Mining*
