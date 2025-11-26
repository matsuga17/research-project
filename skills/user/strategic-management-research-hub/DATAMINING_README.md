# Strategic Management Research Hub - Data Mining README

**Version**: 3.1  
**Date**: 2025-11-01  
**Status**: Production Ready ✅

---

## 🎯 Overview

本格的なデータマイニング・機械学習・因果推論を戦略経営研究に統合した、トップジャーナル水準の分析システム。

**主要機能**:
- ✅ 戦略的グループ分析（クラスタリング）
- ✅ 企業パフォーマンス予測（アンサンブル学習）
- ✅ 特徴量重要度分析（SHAP, Permutation）
- ✅ 異常検知（アウトライア企業特定）
- ✅ 因果推論（Causal Forest, DML, Synthetic Control, PSM）
- ✅ 時系列パターン分析（戦略的軌跡）
- ✅ 説明可能AI（XAI）
- ✅ 包括的レポート自動生成

---

## 🚀 Quick Start (5分)

### ステップ1: 環境準備

```bash
# 基本ライブラリ
pip install pandas numpy scikit-learn matplotlib seaborn statsmodels

# 因果推論（オプション、推奨）
pip install econml

# 高度なML（オプション）
pip install xgboost lightgbm shap
```

### ステップ2: デモ実行

```bash
cd /Users/changu/Desktop/研究/skills/user/strategic-management-research-hub/scripts

# サンプルデータでデモ
python quick_datamining_demo.py

# 自分のデータで実行
python quick_datamining_demo.py --data ../data/final/your_data.csv

# 因果推論も実行
python quick_datamining_demo.py --causal
```

### ステップ3: 結果確認

```bash
# 出力ディレクトリ
./demo_output/
├── datamining_report.html      # 📊 包括的レポート（ブラウザで開く）
├── strategic_groups_pca.png    # 戦略的グループの可視化
├── prediction_performance.png  # 予測性能
├── feature_importance_plot.png # 特徴量重要度
├── outliers_pca.png            # アウトライア検出
├── strategic_group_profiles.xlsx  # グループプロファイル
├── feature_importance.xlsx     # 重要度ランキング
└── strategic_outliers.xlsx     # アウトライア企業リスト
```

---

## 📂 File Structure

```
scripts/
├── advanced_strategic_datamining.py      # 🔥 メインエンジン
├── ml_causal_inference_integrated.py     # 🔥 因果推論システム
├── datamining_config.yaml                # ⚙️ 設定ファイル
├── quick_datamining_demo.py              # 🎬 デモスクリプト
└── [既存の他のスクリプト]

DATAMINING_GUIDE.md                        # 📚 詳細ガイド（必読）
```

---

## 💡 Usage Examples

### 例1: 戦略的グループ分析

```python
from scripts.advanced_strategic_datamining import AdvancedStrategicDataMining
import pandas as pd

df = pd.read_stata('./data/final/analysis_panel.dta')

dm = AdvancedStrategicDataMining(
    data=df,
    firm_id='gvkey',
    time_var='year',
    output_dir='./my_analysis/'
)

# 戦略的次元でクラスタリング
groups = dm.strategic_group_analysis(
    features=['rd_intensity', 'capital_intensity', 'advertising_intensity'],
    n_clusters=4
)

print(groups['cluster_profiles'])
```

### 例2: パフォーマンス予測

```python
# 2年後のROAを予測
predictions = dm.predict_firm_performance(
    target='roa_lead2',
    features=['rd_intensity_lag1', 'firm_size_lag1', 'leverage_lag1'],
    model_type='ensemble'  # RF + GBM + XGBoost
)

print(f"Test R²: {predictions['all_results'][predictions['best_model']]['metrics']['test_r2']:.4f}")
```

### 例3: Causal Forest（異質的処置効果）

```python
from scripts.ml_causal_inference_integrated import CausalMLIntegration

causal = CausalMLIntegration(
    data=df,
    firm_id='gvkey',
    time_var='year',
    output_dir='./causal_analysis/'
)

# M&Aの異質的効果
cf_results = causal.causal_forest(
    treatment='ma_dummy',
    outcome='roa_change',
    controls=['firm_size', 'leverage', 'firm_age'],
    heterogeneity_vars=['firm_size', 'rd_intensity', 'industry_dynamism']
)

print(f"ATE: {cf_results['ate']:.4f}")
print(cf_results['heterogeneity_analysis'])
```

---

## 📊 Key Features Explained

### 1. **Strategic Group Analysis** (Clustering)
- **理論**: Porter (1980), Ketchen & Shook (1996)
- **手法**: K-Means, Hierarchical, GMM, DBSCAN
- **出力**: グループプロファイル、検証指標、PCA可視化

### 2. **Performance Prediction** (Supervised ML)
- **理論**: Resource-Based View, Dynamic Capabilities
- **手法**: Random Forest, Gradient Boosting, XGBoost, LightGBM, Neural Networks
- **出力**: 予測精度、特徴量重要度、モデル比較

### 3. **Causal Forest** (Heterogeneous Treatment Effects)
- **理論**: Athey & Imbens (2016)
- **手法**: Causal Forest with DML
- **出力**: CATE（企業別処置効果）、異質性ドライバー

### 4. **Double Machine Learning** (DML)
- **理論**: Chernozhukov et al. (2018)
- **強み**: 高次元統制変数下での頑健推定
- **出力**: ATE、標準誤差、OLS比較

### 5. **Synthetic Control**
- **理論**: Abadie & Gardeazabal (2003)
- **用途**: 単一処置ユニットのケーススタディ
- **出力**: 合成統制重み、処置効果時系列

### 6. **Propensity Score Matching**
- **理論**: Rosenbaum & Rubin (1983)
- **手法**: Nearest Neighbor, Radius, Kernel
- **出力**: ATT、バランス診断、マッチングペア

---

## 🔧 Configuration

### 設定ファイル編集

```yaml
# datamining_config.yaml

project:
  output_dir: "./my_output/"
  random_seed: 42

data:
  firm_id: "gvkey"
  time_var: "year"

strategic_groups:
  features:
    - "rd_intensity"
    - "capital_intensity"
    - "advertising_intensity"
  n_clusters: 4

performance_prediction:
  target: "roa_lead1"
  model_type: "ensemble"
```

### プログラムから設定読み込み

```python
import yaml

with open('./scripts/datamining_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

dm = AdvancedStrategicDataMining(
    data=df,
    firm_id=config['data']['firm_id'],
    time_var=config['data']['time_var'],
    output_dir=config['project']['output_dir']
)
```

---

## 📚 Documentation

- **[DATAMINING_GUIDE.md](./DATAMINING_GUIDE.md)**: 詳細実践ガイド（70ページ）
- **[SKILL.md](./SKILL.md)**: スキル全体のドキュメント
- **API Documentation**: 各スクリプトのdocstringを参照

---

## 🎓 Research Applications

### トップジャーナル投稿向け

**適用可能な理論**:
- Resource-Based View (RBV)
- Dynamic Capabilities
- Transaction Cost Economics (TCE)
- Institutional Theory
- Configuration Theory

**適用可能な研究テーマ**:
1. 競争戦略と企業パフォーマンス
2. M&A・戦略的提携の効果
3. イノベーション戦略
4. 国際化戦略
5. 組織構造と業績
6. Corporate Governance
7. 制度環境と戦略

**ターゲットジャーナル**:
- Strategic Management Journal (SMJ)
- Academy of Management Journal (AMJ)
- Organization Science (OS)
- Administrative Science Quarterly (ASQ)
- Journal of Management Studies (JMS)

---

## ⚠️ Common Issues & Solutions

### Issue 1: `ImportError: No module named 'econml'`

**解決策**:
```bash
pip install econml
```

### Issue 2: `MemoryError: Unable to allocate`

**解決策**:
```python
# データをチャンク処理
chunk_size = 5000
for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    process_chunk(chunk)
```

### Issue 3: `ValueError: array contains NaN`

**解決策**:
```python
# 欠損値処理
df_clean = df.dropna(subset=required_columns)

# または補完
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy='median')
X_imputed = imputer.fit_transform(X)
```

---

## 📊 Output Format for Papers

### Tables (LaTeX)

```python
# 特徴量重要度をLaTeX形式でエクスポート
importance_df.to_latex(
    './tables/table_importance.tex',
    index=False,
    float_format="%.3f",
    caption="Feature Importance Rankings"
)
```

### Figures (High Resolution)

```python
# 出版用図表（600 dpi）
plt.savefig(
    './figures/strategic_groups.pdf',
    dpi=600,
    bbox_inches='tight',
    format='pdf'
)
```

---

## 🚀 Next Steps

1. **チュートリアル完走**: `quick_datamining_demo.py`を実行
2. **詳細ガイド読了**: `DATAMINING_GUIDE.md`を熟読
3. **自データで分析**: 自分の研究データで実行
4. **論文執筆**: `academic-paper-creation` skillで文書化
5. **再現パッケージ作成**: Phase 8のドキュメント化

---

## 📞 Support

質問・バグ報告は、`strategic-management-research-hub` skillに問い合わせてください。

---

## 📄 License

MIT License - 学術・商用利用可

---

## 📖 Citation

このツールを使用した研究では、以下のように謝辞に記載してください:

```
データ分析は、Strategic Management Research Hub v3.1のデータマイニング
システムを使用して実施された。このシステムは、戦略経営研究における
定量分析の再現性と信頼性を確保するために設計されている。
```

---

**Last Updated**: 2025-11-01  
**Version**: 3.1  
**Status**: Production Ready ✅

**Happy Data Mining! 📊🚀🎓**

#戦略経営研究 #データマイニング #機械学習 #因果推論 #トップジャーナル
