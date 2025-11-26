# Strategic Management Research Hub - Data Mining Practical Guide
================================================================

**Version**: 3.1  
**Last Updated**: 2025-11-01  
**Author**: Strategic Management Research Hub  

このガイドでは、本格的なデータマイニング分析を段階的に実行する方法を説明します。

---

## 📚 目次

1. [クイックスタート（5分）](#1-クイックスタート5分)
2. [戦略的グループ分析](#2-戦略的グループ分析)
3. [企業パフォーマンス予測](#3-企業パフォーマンス予測)
4. [特徴量重要度分析](#4-特徴量重要度分析)
5. [異常検知（戦略的アウトライア）](#5-異常検知戦略的アウトライア)
6. [因果推論（ML統合）](#6-因果推論ml統合)
7. [時系列パターン分析](#7-時系列パターン分析)
8. [完全自動化ワークフロー](#8-完全自動化ワークフロー)
9. [論文投稿準備](#9-論文投稿準備)
10. [トラブルシューティング](#10-トラブルシューティング)

---

## 1. クイックスタート（5分）

### 【目的】
最小限のコードで、データマイニング分析の全体像を把握

### 【前提条件】
```python
# 必要なライブラリ
pip install pandas numpy scikit-learn matplotlib seaborn
pip install econml  # 因果推論用（オプション）
pip install xgboost lightgbm  # 高度なML用（オプション）
pip install shap  # 説明可能AI用（オプション）
```

### 【最速実行例】

```python
import pandas as pd
from scripts.advanced_strategic_datamining import AdvancedStrategicDataMining

# 1. データ読み込み
df_panel = pd.read_stata('./data/final/analysis_panel.dta')

# 2. データマイニングエンジン初期化
dm = AdvancedStrategicDataMining(
    data=df_panel,
    firm_id='gvkey',
    time_var='year',
    output_dir='./quick_output/'
)

# 3. 戦略的グループ分析（1コマンド）
groups = dm.strategic_group_analysis(
    features=['rd_intensity', 'capital_intensity', 'international_sales'],
    n_clusters=4
)

# 4. パフォーマンス予測（1コマンド）
predictions = dm.predict_firm_performance(
    target='roa',
    features=['rd_intensity', 'firm_size', 'leverage'],
    model_type='ensemble'
)

# 5. 包括的レポート生成
report_path = dm.generate_comprehensive_report()

print(f"✅ 完了！レポート: {report_path}")
```

**実行時間**: 約2-5分（データサイズによる）  
**出力**:
- 戦略的グループのプロファイル
- パフォーマンス予測モデル
- 特徴量重要度ランキング
- HTMLレポート

---

## 2. 戦略的グループ分析

### 【理論的背景】

**Porter (1980)**: Strategic Groups within Industries  
**研究目的**: 同一産業内で、類似の戦略を採用する企業群（戦略的グループ）を特定

### 【研究での使用例】

#### 例1: 製造業の戦略的グループ特定

```python
from scripts.advanced_strategic_datamining import AdvancedStrategicDataMining
import pandas as pd

# データ準備
df_panel = pd.read_csv('./data/final/manufacturing_firms.csv')

# 分析実行
dm = AdvancedStrategicDataMining(
    data=df_panel,
    firm_id='gvkey',
    time_var='year',
    output_dir='./strategic_groups_output/'
)

# 戦略的次元の選択（理論駆動）
strategic_dimensions = [
    'rd_intensity',          # イノベーション戦略
    'advertising_intensity', # 差別化戦略
    'capital_intensity',     # 資本集約度
    'vertical_integration',  # 垂直統合
    'international_sales'    # 国際化戦略
]

# クラスタリング実行
results = dm.strategic_group_analysis(
    features=strategic_dimensions,
    n_clusters=None,  # 最適クラスタ数を自動決定
    method='kmeans',
    optimal_k_method='silhouette',
    max_k=8
)

# 結果の解釈
print("クラスタリング結果:")
print(results['cluster_profiles'])

# 各グループの特徴分析
for idx, row in results['cluster_profiles'].iterrows():
    print(f"\n戦略的グループ {row['cluster']}:")
    print(f"  企業数: {row['size']} ({row['size_pct']:.1f}%)")
    print(f"  R&D集約度: {row['rd_intensity_mean']:.3f}")
    print(f"  広告集約度: {row['advertising_intensity_mean']:.3f}")
    # ... 他の次元
```

#### 例2: グループ間パフォーマンス比較

```python
# クラスタ割り当てをデータに追加
df_panel['strategic_group'] = results['cluster_labels']

# グループ別パフォーマンス
group_performance = df_panel.groupby('strategic_group').agg({
    'roa': ['mean', 'std', 'count'],
    'sales_growth': ['mean', 'std']
}).round(4)

print("\nグループ別パフォーマンス:")
print(group_performance)

# 統計的検定（ANOVA）
from scipy.stats import f_oneway

groups = [
    df_panel[df_panel['strategic_group'] == i]['roa'].dropna() 
    for i in range(results['n_clusters'])
]
f_stat, p_value = f_oneway(*groups)

print(f"\nANOVA結果:")
print(f"F統計量: {f_stat:.2f}, p値: {p_value:.4f}")
if p_value < 0.05:
    print("→ グループ間で有意なパフォーマンス差あり")
```

### 【論文での報告方法】

**Table X: Strategic Group Profiles**

| Strategic Group | N | R&D Intensity | Advertising Int. | Capital Int. | ROA (Mean) |
|-----------------|---|---------------|------------------|--------------|------------|
| Group 1 (Innovators) | 85 | 0.087 | 0.023 | 0.412 | 0.064 |
| Group 2 (Cost Leaders) | 132 | 0.015 | 0.008 | 0.581 | 0.052 |
| Group 3 (Differentiators) | 98 | 0.042 | 0.095 | 0.338 | 0.071 |
| Group 4 (Integrators) | 67 | 0.038 | 0.031 | 0.694 | 0.058 |

**Figure X**: Strategic Groups (PCA Projection) → `strategic_groups_pca.png`

---

## 3. 企業パフォーマンス予測

### 【理論的背景】

**Resource-Based View (Barney, 1991)**: 企業固有資源がパフォーマンスを決定  
**研究目的**: 戦略的選択から将来パフォーマンスを予測するモデル構築

### 【研究での使用例】

#### 例1: R&D投資の効果予測

```python
# 将来パフォーマンス（2年後ROA）を予測
prediction_results = dm.predict_firm_performance(
    target='roa_lead2',  # 2年後のROA
    features=[
        'rd_intensity_lag1',     # 1期ラグR&D
        'firm_size_lag1',
        'leverage_lag1',
        'firm_age',
        'industry_concentration',
        'env_dynamism',
        'patent_stock'
    ],
    model_type='ensemble',  # Random Forest + Gradient Boosting + XGBoost
    test_size=0.2,
    cv_folds=5,
    tune_hyperparameters=True
)

# モデル性能
best_model = prediction_results['best_model']
metrics = prediction_results['all_results'][best_model]['metrics']

print(f"\nベストモデル: {best_model}")
print(f"テストR²: {metrics['test_r2']:.4f}")
print(f"テストRMSE: {metrics['test_rmse']:.4f}")
print(f"CV R² (平均±標準偏差): {metrics['cv_r2_mean']:.4f} ± {metrics['cv_r2_std']:.4f}")
```

#### 例2: 特徴量重要度の解釈

```python
# 特徴量重要度
importance_df = prediction_results['feature_importance']

print("\nTop 5 Most Important Features:")
print(importance_df.head().to_string(index=False))

# 理論的解釈を追加
interpretation = {
    'rd_intensity_lag1': 'イノベーション投資が将来パフォーマンスの最大ドライバー（RBV支持）',
    'firm_size_lag1': '規模の経済性・資源豊富性',
    'patent_stock': '蓄積された知識資産（Dynamic Capabilities）',
    # ...
}

for feat in importance_df.head()['feature']:
    print(f"{feat}: {interpretation.get(feat, 'N/A')}")
```

### 【論文での報告方法】

**Table X: Performance Prediction Results**

| Model | Test R² | RMSE | CV R² (Mean) | CV R² (SD) |
|-------|---------|------|--------------|------------|
| Random Forest | 0.387 | 0.042 | 0.351 | 0.028 |
| Gradient Boosting | 0.412 | 0.038 | 0.389 | 0.032 |
| **XGBoost** | **0.438** | **0.035** | **0.407** | **0.024** |

**研究への示唆**:
「XGBoostモデルは、1期ラグのR&D intensityから2年後のROAを、テストセットでR²=0.438の精度で予測した。これは、R&D投資が将来パフォーマンスの強力な予測因子であることを示唆し、RBVの予測を支持する。」

---

## 4. 特徴量重要度分析

### 【目的】
どの戦略的変数がパフォーマンスに最も影響するかを定量化

### 【実行例】

```python
importance_results = dm.analyze_feature_importance(
    target='roa',
    features=[
        'rd_intensity', 'advertising_intensity', 'capital_intensity',
        'firm_size', 'leverage', 'firm_age', 'diversification',
        'international_ratio', 'alliance_count', 'ma_experience'
    ],
    method='ensemble',  # Random Forest + Gradient Boosting
    top_n=10
)

# 結果の可視化
# → 自動生成: feature_importance_plot.png

# 理論的含意の議論
top_3 = importance_results.head(3)
print("\nTop 3変数の理論的解釈:")
for idx, row in top_3.iterrows():
    print(f"{row['feature']}: 重要度 {row['ensemble_importance']:.3f}")
    # 理論的解釈を追加...
```

---

## 5. 異常検知（戦略的アウトライア）

### 【理論的意義】

**アウトライア企業の3類型**:
1. **例外的成功企業** (Sustained Competitive Advantage)
2. **失敗リスク企業** (Early Warning Signal)
3. **データ品質問題** (Measurement Error)

### 【実行例】

```python
outliers = dm.detect_strategic_outliers(
    features=[
        'roa', 'sales_growth', 'rd_intensity', 
        'leverage', 'cash_ratio'
    ],
    method='ensemble',  # Isolation Forest + LOF + Elliptic Envelope
    contamination=0.05,  # 期待アウトライア率5%
    save_results=True
)

# アウトライア企業の詳細分析
print(f"\n検出されたアウトライア: {len(outliers)} 企業")
print("\nTop 10 Most Unusual Firms:")
print(outliers.nlargest(10, 'outlier_score'))

# ケーススタディ候補
exceptional_performers = outliers[outliers['roa'] > 0.15]
print(f"\n例外的成功企業（ROA>15%）: {len(exceptional_performers)} 社")
for idx, row in exceptional_performers.iterrows():
    print(f"  {row['firm_name']}: ROA={row['roa']:.1%}, outlier_score={row['outlier_score']:.3f}")
```

### 【論文での活用】

1. **定量研究**: アウトライアを除外してrobustness check
2. **質的研究**: 例外企業の詳細ケーススタディ
3. **理論構築**: アウトライアから新理論の手がかり

---

## 6. 因果推論（ML統合）

### 【内生性問題への対処】

戦略研究の最大の課題: **相関 ≠ 因果**

**典型的な内生性源泉**:
- Selection bias（企業が戦略を自己選択）
- Omitted variable bias（観測不能な企業特性）
- Reverse causality（パフォーマンス → 戦略）

### 【Causal Forest（異質的処置効果）】

#### 理論的意義
従来の回帰分析は「平均的効果」を推定。しかし現実には:
- M&Aが有効な企業と無効な企業が混在
- R&D投資の効果は企業能力に依存

**Causal Forest**は、**どの企業にとって処置が効果的か**を発見

#### 実装例

```python
from scripts.ml_causal_inference_integrated import CausalMLIntegration

# 因果推論システム初期化
causal = CausalMLIntegration(
    data=df_panel,
    firm_id='gvkey',
    time_var='year',
    output_dir='./causal_output/'
)

# M&Aの異質的効果分析
cf_results = causal.causal_forest(
    treatment='ma_dummy',           # M&A実施（0/1）
    outcome='roa_change',           # ROA変化
    controls=[
        'firm_size', 'leverage', 'firm_age', 'prior_ma_count'
    ],
    heterogeneity_vars=[            # 効果の異質性を生む変数
        'firm_size',
        'rd_intensity',
        'prior_ma_experience',
        'industry_dynamism'
    ],
    discrete_treatment=True,
    n_estimators=100
)

# 結果の解釈
print(f"\n平均処置効果（ATE）: {cf_results['ate']:.4f}")
print(f"95% CI: [{cf_results['ate_ci'][0]:.4f}, {cf_results['ate_ci'][1]:.4f}]")

# どの企業特性がM&A効果を左右するか
print("\n異質性ドライバー:")
print(cf_results['feature_importance'])

# 企業規模別の効果
heterogeneity = cf_results['heterogeneity_analysis']
size_effect = heterogeneity['firm_size']
print(f"\n企業規模による効果差:")
print(f"  小規模企業: ATE = {size_effect['ate_low']:.4f}")
print(f"  大規模企業: ATE = {size_effect['ate_high']:.4f}")
print(f"  差: {size_effect['difference']:.4f} (p={size_effect['p_value']:.4f})")
```

#### 論文での報告

**Table X: Heterogeneous M&A Effects (Causal Forest)**

| Firm Characteristic | Low Group ATE | High Group ATE | Difference | p-value |
|---------------------|---------------|----------------|------------|---------|
| Firm Size | 0.018 | 0.042 | 0.024*** | 0.001 |
| R&D Intensity | 0.023 | 0.038 | 0.015** | 0.012 |
| Prior M&A Experience | 0.015 | 0.045 | 0.030*** | 0.000 |

**研究的示唆**:
「Causal Forest分析により、M&Aの効果は企業規模に依存することが明らかになった。大規模企業のATE（0.042）は小規模企業（0.018）の2倍以上であり、資源豊富性がM&A統合を促進する可能性を示唆する（RBV）。」

### 【Double Machine Learning（DML）】

高次元統制変数下での頑健な因果推定

```python
# DML推定
dml_results = causal.double_machine_learning(
    treatment='rd_intensity',
    outcome='roa_lead2',
    controls=[
        # 多数の統制変数（30個以上も可能）
        'firm_size', 'firm_age', 'leverage', 'cash_ratio',
        'tangibility', 'market_to_book', 'sales_growth',
        'industry_concentration', 'industry_rd_mean',
        'gdp_growth', 'interest_rate', 'exchange_rate',
        # ... 高次元でもOK
    ],
    discrete_treatment=False,
    cv_folds=5
)

print(f"\nDML推定結果:")
print(f"ATE: {dml_results['ate']:.4f}")
print(f"SE: {dml_results['ate_stderr']:.4f}")
print(f"p-value: {dml_results['p_value']:.4f}")

# 従来のOLSと比較
if 'ols_comparison' in dml_results:
    ols = dml_results['ols_comparison']
    print(f"\nOLS比較:")
    print(f"  OLS係数: {ols['ols_coef']:.4f} (SE: {ols['ols_se']:.4f})")
    print(f"  DML係数: {dml_results['ate']:.4f} (SE: {dml_results['ate_stderr']:.4f})")
    print(f"  → DMLはconfounding biasに頑健")
```

### 【Synthetic Control Method】

単一処置ユニットのケーススタディ

```python
# 例: Appleの2014年Beats買収がイノベーションに与えた影響
sc_results = causal.synthetic_control(
    treated_unit='AAPL',
    treatment_time='2014-05',
    outcome_var='patent_count',
    donor_pool=['MSFT', 'GOOG', 'AMZN', 'FB', 'NFLX', 'INTC']
)

print(f"\n処置後平均効果: {sc_results['ate_post']:.2f} 特許/年")

# Synthetic controlの構成
print("\nSynthetic Control Weights:")
print(sc_results['weights'])
```

---

## 7. 時系列パターン分析

### 【戦略的軌跡クラスタリング】

企業の戦略的進化パターンを類型化

```python
temporal_results = dm.analyze_temporal_patterns(
    variables=['rd_intensity', 'capital_intensity'],
    method='trajectory_clustering',
    save_results=True
)

# 軌跡クラスタの解釈
trajectory_clusters = temporal_results['trajectory_clusters']
print(f"\n{trajectory_clusters['trajectory_cluster'].nunique()} つの戦略的軌跡を特定")

# 各クラスタの代表企業
for cluster_id in trajectory_clusters['trajectory_cluster'].unique():
    cluster_firms = trajectory_clusters[
        trajectory_clusters['trajectory_cluster'] == cluster_id
    ]
    print(f"\n軌跡クラスタ {cluster_id}: {len(cluster_firms)} 企業")
    print(f"  代表企業: {cluster_firms['firm_name'].head(3).tolist()}")
```

### 【戦略的転換点検出】

企業の戦略転換タイミングを特定

```python
change_points = temporal_results['change_points']
print(f"\n{len(change_points)} 件の戦略的転換点を検出")

# 頻度の高い転換年
common_years = change_points['time'].value_counts().head()
print("\n転換点が集中する年:")
print(common_years)
# → 業界ショック、規制変更等の外部イベントと対応
```

---

## 8. 完全自動化ワークフロー

### 【設定ファイルベースの実行】

```python
# 設定ファイル読み込み
import yaml

with open('./scripts/datamining_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# 自動実行
from scripts.advanced_strategic_datamining import AdvancedStrategicDataMining

dm = AdvancedStrategicDataMining(
    data=df_panel,
    firm_id=config['data']['firm_id'],
    time_var=config['data']['time_var'],
    output_dir=config['project']['output_dir'],
    random_state=config['project']['random_seed']
)

# 設定に基づき全分析を自動実行
if config['strategic_groups']['enabled']:
    dm.strategic_group_analysis(
        features=config['strategic_groups']['features'],
        method=config['strategic_groups']['method'],
        n_clusters=config['strategic_groups']['n_clusters']
    )

if config['performance_prediction']['enabled']:
    dm.predict_firm_performance(
        target=config['performance_prediction']['target'],
        features=config['performance_prediction']['features'],
        model_type=config['performance_prediction']['model_type']
    )

# レポート生成
dm.generate_comprehensive_report()
```

---

## 9. 論文投稿準備

### 【SMJ/AMJ投稿チェックリスト】

#### データマイニング結果の報告要件

- [ ] **方法論の透明性**
  - 使用アルゴリズムの明記（Random Forest, XGBoost等）
  - ハイパーパラメータの報告
  - クロスバリデーション手法

- [ ] **モデル性能指標**
  - R² (訓練/テスト)
  - RMSE, MAE
  - CV性能（平均±標準偏差）

- [ ] **Robustness Checks**
  - 代替モデルでの結果（最低3種類）
  - 代替サンプルでの結果
  - Outlier除外後の結果

- [ ] **理論的解釈**
  - 特徴量重要度の理論的意味
  - 既存理論との対話
  - 実務的示唆

#### 因果推論結果の報告要件

- [ ] **内生性への対処**
  - 内生性源泉の明示的議論
  - 使用手法の理論的根拠
  - 識別戦略の説明

- [ ] **処置効果の報告**
  - ATE/ATT with 95% CI
  - p値
  - 効果サイズの解釈

- [ ] **Balance Diagnostics**（PSM使用時）
  - マッチング前後の共変量バランス
  - Standardized differences
  - Common support確認

- [ ] **Robustness**
  - Alternative matching methods
  - Different caliper widths
  - Sensitivity analysis

### 【レポート生成とエクスポート】

```python
# 論文用の表をLaTeX形式でエクスポート
importance_df.to_latex(
    './output/tables/table_feature_importance.tex',
    index=False,
    float_format="%.3f",
    caption="Feature Importance Rankings",
    label="tab:importance"
)

# 図を高解像度で保存（出版用）
plt.savefig(
    './output/figures/strategic_groups.pdf',
    dpi=600,
    bbox_inches='tight',
    format='pdf'
)
```

---

## 10. トラブルシューティング

### 【よくあるエラーと解決策】

#### エラー1: `MemoryError: Unable to allocate array`

**原因**: データセットが大きすぎてメモリ不足

**解決策**:
```python
# チャンク処理
chunk_size = 10000
results = []

for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    chunk_result = process_chunk(chunk)
    results.append(chunk_result)

final_result = pd.concat(results)
```

#### エラー2: `ValueError: array must not contain NaNs`

**原因**: 欠損値が残っている

**解決策**:
```python
# 欠損値の処理
df_clean = df.dropna(subset=required_features)

# または、補完
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy='median')
X_imputed = imputer.fit_transform(X)
```

#### エラー3: `LinAlgError: Singular matrix`

**原因**: 完全な多重共線性

**解決策**:
```python
# VIFチェック
from statsmodels.stats.outliers_influence import variance_inflation_factor

vif_data = pd.DataFrame()
vif_data["feature"] = features
vif_data["VIF"] = [variance_inflation_factor(X.values, i) 
                   for i in range(X.shape[1])]

# VIF > 10 の変数を除外
features_filtered = vif_data[vif_data["VIF"] < 10]["feature"].tolist()
```

#### エラー4: `Causal Forest: Not enough treated observations`

**原因**: 処置群のサンプルサイズ不足

**解決策**:
```python
# 最低要件: 処置群 ≥ 50 observations
print(f"Treated: {df['treatment'].sum()}")
print(f"Control: {(~df['treatment']).sum()}")

# サンプルサイズ不足なら、PSMやDiDを検討
```

### 【パフォーマンス最適化】

```python
# 並列処理の有効化
dm = AdvancedStrategicDataMining(
    data=df_panel,
    firm_id='gvkey',
    time_var='year',
    output_dir='./output/'
)

# scikit-learnモデルでn_jobs=-1（全CPUコア使用）
from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(
    n_estimators=200,
    n_jobs=-1,  # 全CPUコア使用
    random_state=42
)
```

---

## 📚 参考文献

### データマイニング手法

- Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning*. Springer.
- James, G., Witten, D., Hastie, T., & Tibshirani, R. (2013). *An Introduction to Statistical Learning*. Springer.

### 因果推論

- Pearl, J. (2009). *Causality: Models, Reasoning and Inference* (2nd ed.). Cambridge University Press.
- Imbens, G. W., & Rubin, D. B. (2015). *Causal Inference for Statistics, Social, and Biomedical Sciences*. Cambridge University Press.
- Athey, S., & Imbens, G. W. (2016). Recursive partitioning for heterogeneous causal effects. *PNAS*, 113(27), 7353-7360.

### 戦略経営研究での応用

- Ketchen, D. J., & Shook, C. L. (1996). The application of cluster analysis in strategic management research. *Strategic Management Journal*, 17(6), 441-458.
- Short, J. C., Ketchen, D. J., & Palmer, T. B. (2002). The role of sampling in strategic management research. *Organizational Research Methods*, 5(3), 220-239.

---

## 🚀 次のステップ

1. **チュートリアル完走**: 各セクションの例を実データで実行
2. **カスタマイズ**: 自分の研究テーマに合わせてパラメータ調整
3. **論文執筆**: 結果を`academic-paper-creation` skillで文書化
4. **再現パッケージ**: Phase 8のドキュメント化ガイドに従う

**Support**: strategic-management-research-hub v3.1 skillに質問してください

---

**Last Updated**: 2025-11-01  
**Version**: 3.1  

#データマイニング #機械学習 #因果推論 #戦略経営研究 #実証分析
