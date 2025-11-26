---
name: strategic-research-data-mining
description: Data mining methods for strategic management research including clustering (firm grouping), dimensionality reduction (PCA, t-SNE), classification (bankruptcy prediction), anomaly detection (fraud detection), and time series analysis (strategy change points).
version: 4.0
part_of: strategic-research-suite
related_skills:
  - core-workflow: Phase 6 (Variable Construction)
  - statistical-methods: Feature engineering and model validation
  - text-analysis: Text features for clustering
  - network-analysis: Network features for classification
---

# Data Mining Toolkit for Strategic Research v4.0

**Part of**: [Strategic Research Suite v4.0](../README.md)

---

## 🎯 このスキルについて

戦略経営研究のための**データマイニング手法**を提供します。企業の類型化、破綻予測、異常検知、戦略転換点の特定など、パターン発見と予測に焦点を当てます。

### いつ使うか

✅ **企業グループの識別**
- 戦略グループの分類
- 類似企業の発見
- 市場セグメンテーション

✅ **予測モデル構築**
- 破綻・M&A予測
- パフォーマンス予測
- 戦略変更の予測

✅ **異常検知**
- 不正会計の検出
- 異常企業の識別
- リスク企業の早期発見

✅ **パターン発見**
- 戦略転換点の検出
- 時系列パターンの識別
- 高次元データの可視化

### 前提条件

**必須知識**:
- Python基礎（pandas, numpy）
- 基本的な統計知識
- 機械学習の基本概念

**推奨知識**:
- scikit-learn使用経験
- データの前処理・特徴量エンジニアリング
- モデル評価指標の理解

---

## 📋 目次

1. [Methods Overview](#methods-overview)
2. [Clustering](#clustering)
3. [Dimensionality Reduction](#dimensionality-reduction)
4. [Classification](#classification)
5. [Anomaly Detection](#anomaly-detection)
6. [Time Series Analysis](#time-series-analysis)
7. [Quick Start](#quick-start)
8. [Best Practices](#best-practices)
9. [Common Pitfalls](#common-pitfalls)
10. [FAQ](#faq)

---

## Methods Overview

### データマイニング手法の全体像

```
Data Mining Methods
│
├── Clustering (クラスタリング)
│   ├── K-means
│   ├── Hierarchical Clustering
│   ├── DBSCAN
│   └── Gaussian Mixture Models
│
├── Dimensionality Reduction (次元削減)
│   ├── PCA (Principal Component Analysis)
│   ├── Factor Analysis
│   ├── t-SNE
│   └── UMAP
│
├── Classification (分類)
│   ├── Random Forest
│   ├── Gradient Boosting (XGBoost, LightGBM)
│   ├── Support Vector Machine
│   └── Logistic Regression
│
├── Anomaly Detection (異常検知)
│   ├── Isolation Forest
│   ├── Local Outlier Factor (LOF)
│   ├── One-Class SVM
│   └── Statistical methods (Z-score, IQR)
│
└── Time Series Analysis (時系列分析)
    ├── ARIMA
    ├── VAR (Vector Autoregression)
    ├── Change Point Detection
    └── Trend decomposition
```


---

## Clustering

### 目的

類似した特徴を持つ企業をグループ化し、**戦略グループ**を識別します。

### 戦略研究での応用

- **Strategic Groups**: 同様の戦略を採用する企業群の識別
- **Market Segmentation**: 異質な市場セグメントの発見
- **Competitive Positioning**: 競争ポジションの可視化
- **Archetype Identification**: 企業タイプ（イノベーター、追随者等）の分類

### 手法比較

| 手法 | 適用場面 | 利点 | 欠点 |
|------|---------|------|------|
| **K-means** | クラスタ数が既知 | 高速、解釈容易 | 球状クラスタ前提 |
| **Hierarchical** | 階層構造の可視化 | デンドログラム | 計算コスト高 |
| **DBSCAN** | 任意形状クラスタ | ノイズ検出可能 | パラメータ調整困難 |
| **GMM** | 確率的クラスタ | 柔軟なクラスタ形状 | 計算コスト高 |

### K-means Clustering

**基本原理**: データを k 個のクラスタに分割し、各クラスタ内の分散を最小化

**実装例**:

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd

# データ準備
df = pd.read_csv('firm_financials.csv')
features = ['roa', 'sales_growth', 'rd_intensity', 'leverage']
X = df[features].dropna()

# 標準化（重要！）
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# K-means実行
kmeans = KMeans(
    n_clusters=3,           # クラスタ数
    random_state=42,        # 再現性確保
    n_init=10,              # 初期値試行回数
    max_iter=300            # 最大反復回数
)
labels = kmeans.fit_predict(X_scaled)

# 結果をDataFrameに追加
df['cluster'] = labels

# クラスタ特徴の確認
cluster_stats = df.groupby('cluster')[features].mean()
print(cluster_stats)
```

**最適なクラスタ数の決定**:

```python
from sklearn.metrics import silhouette_score

# エルボー法
inertias = []
silhouettes = []

for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(X_scaled)
    
    inertias.append(kmeans.inertia_)
    silhouettes.append(silhouette_score(X_scaled, labels))

# プロット
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

ax1.plot(range(2, 11), inertias, 'bo-')
ax1.set_xlabel('Number of clusters (k)')
ax1.set_ylabel('Inertia')
ax1.set_title('Elbow Method')

ax2.plot(range(2, 11), silhouettes, 'ro-')
ax2.set_xlabel('Number of clusters (k)')
ax2.set_ylabel('Silhouette Score')
ax2.set_title('Silhouette Analysis')

plt.tight_layout()
plt.show()
```

**評価指標**:

- **Silhouette Score**: -1 ~ 1（高いほど良い、>0.5が目安）
- **Davies-Bouldin Index**: 0 ~ ∞（低いほど良い）
- **Calinski-Harabasz Index**: 高いほど良い

### Hierarchical Clustering

**基本原理**: 階層的にクラスタを統合・分割

**実装例**:

```python
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

# 階層的クラスタリング
hc = AgglomerativeClustering(
    n_clusters=3,
    linkage='ward'  # ward, complete, average, single
)
labels = hc.fit_predict(X_scaled)

# デンドログラム作成
linkage_matrix = linkage(X_scaled, method='ward')

plt.figure(figsize=(12, 6))
dendrogram(linkage_matrix, truncate_mode='level', p=5)
plt.xlabel('Sample Index or (Cluster Size)')
plt.ylabel('Distance')
plt.title('Hierarchical Clustering Dendrogram')
plt.show()
```

**Linkage方法の選択**:
- **Ward**: クラスタ内分散最小化（推奨）
- **Complete**: 最大距離最小化（コンパクト）
- **Average**: 平均距離使用（バランス）
- **Single**: 最小距離使用（チェイン形成注意）

### DBSCAN

**基本原理**: 密度ベースのクラスタリング、任意形状対応

**実装例**:

```python
from sklearn.cluster import DBSCAN

# DBSCAN実行
dbscan = DBSCAN(
    eps=0.5,          # 近傍半径
    min_samples=5     # 最小サンプル数
)
labels = dbscan.fit_predict(X_scaled)

# ノイズ点の識別（label=-1）
n_noise = (labels == -1).sum()
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

print(f"Clusters: {n_clusters}, Noise points: {n_noise}")
```

**パラメータ調整**:
- `eps`: 小さい→多くの小クラスタ、大きい→少数の大クラスタ
- `min_samples`: データサイズの1-2%が目安


---

## Dimensionality Reduction

### 目的

高次元データを2-3次元に圧縮し、可視化・理解を容易にします。

### 手法比較

| 手法 | 目的 | 線形/非線形 | 計算速度 |
|------|------|------------|---------|
| **PCA** | 分散最大化 | 線形 | 高速 |
| **t-SNE** | 近傍保存 | 非線形 | 遅い |
| **UMAP** | トポロジー保存 | 非線形 | 中速 |
| **Factor Analysis** | 潜在因子発見 | 線形 | 中速 |

### PCA (Principal Component Analysis)

**実装例**:

```python
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# PCA実行
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# 説明される分散
print(f"Explained variance ratio: {pca.explained_variance_ratio_}")
print(f"Cumulative variance: {pca.explained_variance_ratio_.sum():.2%}")

# 可視化
plt.figure(figsize=(10, 8))
plt.scatter(X_pca[:, 0], X_pca[:, 1], alpha=0.6)
plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})')
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})')
plt.title('PCA Visualization')
plt.show()

# 主成分の解釈
components_df = pd.DataFrame(
    pca.components_,
    columns=features,
    index=['PC1', 'PC2']
)
print(components_df)
```

### t-SNE

**実装例**:

```python
from sklearn.manifold import TSNE

# t-SNE実行（時間がかかる）
tsne = TSNE(
    n_components=2,
    random_state=42,
    perplexity=30,      # 5-50が一般的
    learning_rate=200   # 10-1000
)
X_tsne = tsne.fit_transform(X_scaled)

# クラスタと組み合わせて可視化
plt.figure(figsize=(10, 8))
scatter = plt.scatter(
    X_tsne[:, 0], X_tsne[:, 1], 
    c=labels, cmap='viridis', alpha=0.6
)
plt.colorbar(scatter, label='Cluster')
plt.title('t-SNE Visualization with Clusters')
plt.show()
```

---

## Classification

### 目的

企業を予め定義されたカテゴリに分類（破綻予測、M&A予測等）。

### Random Forest

**実装例**:

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# データ準備
X = df[['roa', 'leverage', 'current_ratio', 'zscore']]
y = df['bankrupt']  # 0/1ラベル

# Train/Test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Random Forest
rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    class_weight='balanced'  # 不均衡データ対策
)
rf.fit(X_train, y_train)

# 予測と評価
y_pred = rf.predict(X_test)
print(classification_report(y_test, y_pred))

# 特徴量重要度
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)

print(feature_importance)
```

### XGBoost

**実装例**:

```python
import xgboost as xgb

# XGBoost
xgb_model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    random_state=42,
    scale_pos_weight=len(y_train[y_train==0]) / len(y_train[y_train==1])  # 不均衡対策
)
xgb_model.fit(X_train, y_train)

# 予測確率
y_proba = xgb_model.predict_proba(X_test)[:, 1]

# ROC-AUC
from sklearn.metrics import roc_auc_score, roc_curve

auc = roc_auc_score(y_test, y_proba)
print(f"AUC: {auc:.3f}")

# ROC曲線
fpr, tpr, thresholds = roc_curve(y_test, y_proba)
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f'AUC = {auc:.3f}')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.show()
```

---

## Anomaly Detection

### 目的

通常と異なるパターンを持つ企業を検出（不正会計、異常値等）。

### Isolation Forest

**実装例**:

```python
from sklearn.ensemble import IsolationForest

# Isolation Forest
iso_forest = IsolationForest(
    contamination=0.1,  # 異常値の割合（10%）
    random_state=42
)
anomaly_labels = iso_forest.fit_predict(X_scaled)

# 異常スコア
anomaly_scores = iso_forest.score_samples(X_scaled)

# 異常企業の抽出
df['anomaly'] = anomaly_labels
df['anomaly_score'] = anomaly_scores

anomalies = df[df['anomaly'] == -1].sort_values('anomaly_score')
print(f"Detected {len(anomalies)} anomalies")
print(anomalies[['firm_name', 'anomaly_score', 'roa', 'leverage']].head())
```

### Statistical Methods

**Z-score法**:

```python
from scipy import stats

# Z-score計算
z_scores = np.abs(stats.zscore(df[features]))

# 異常値フラグ（Z-score > 3）
df['is_outlier'] = (z_scores > 3).any(axis=1)

print(f"Outliers: {df['is_outlier'].sum()}")
```

---

## Time Series Analysis

### 目的

時系列データから戦略転換点を検出、トレンドを予測。

### Change Point Detection

**実装例**:

```python
import ruptures as rpt

# 企業の時系列データ
firm_data = df[df['firm_id'] == 1].sort_values('year')
signal = firm_data['roa'].values

# Change point detection
model = rpt.Pelt(model="rbf").fit(signal)
change_points = model.predict(pen=10)

# 可視化
plt.figure(figsize=(12, 4))
plt.plot(firm_data['year'], signal, label='ROA')
for cp in change_points[:-1]:
    plt.axvline(x=firm_data['year'].iloc[cp], color='r', 
                linestyle='--', label='Change Point' if cp == change_points[0] else '')
plt.xlabel('Year')
plt.ylabel('ROA')
plt.title('Strategy Change Point Detection')
plt.legend()
plt.show()
```

### ARIMA Forecasting

**実装例**:

```python
from statsmodels.tsa.arima.model import ARIMA

# ARIMAモデル
model = ARIMA(signal, order=(1, 1, 1))
fitted = model.fit()

# 予測
forecast = fitted.forecast(steps=3)
print(f"3-year forecast: {forecast}")
```

---

## Quick Start

### Example 1: 企業を3つの戦略グループに分類

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd

# データ読み込み
df = pd.read_csv('firm_financials.csv')

# 特徴量選択
features = ['roa', 'rd_intensity', 'leverage', 'firm_size']
X = df[features].dropna()

# 標準化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# クラスタリング
kmeans = KMeans(n_clusters=3, random_state=42)
df['strategic_group'] = kmeans.fit_predict(X_scaled)

# 結果確認
print(df.groupby('strategic_group')[features].mean())
```

### Example 2: 破綻企業を予測

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# データ準備
X = df[['zscore', 'current_ratio', 'leverage', 'profitability']]
y = df['bankrupt_next_year']

# Train/Test分割
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# モデル訓練
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# 評価
from sklearn.metrics import classification_report
y_pred = rf.predict(X_test)
print(classification_report(y_test, y_pred))
```


---

## Best Practices

### 1. Feature Engineering

**財務比率の計算**:
```python
# 収益性
df['roa'] = df['net_income'] / df['total_assets']
df['roe'] = df['net_income'] / df['total_equity']
df['profit_margin'] = df['net_income'] / df['sales']

# 効率性
df['asset_turnover'] = df['sales'] / df['total_assets']
df['inventory_turnover'] = df['cogs'] / df['inventory']

# 安全性
df['current_ratio'] = df['current_assets'] / df['current_liabilities']
df['debt_to_equity'] = df['total_debt'] / df['total_equity']

# 成長性
df['sales_growth'] = df.groupby('firm_id')['sales'].pct_change()
df['asset_growth'] = df.groupby('firm_id')['total_assets'].pct_change()
```

**業界調整**:
```python
# 業界平均との差分
industry_means = df.groupby(['industry', 'year'])[features].transform('mean')
df_adjusted = df[features] - industry_means
```

**時系列特徴量**:
```python
# ラグ変数
df['roa_lag1'] = df.groupby('firm_id')['roa'].shift(1)
df['roa_lag2'] = df.groupby('firm_id')['roa'].shift(2)

# 移動平均
df['roa_ma3'] = df.groupby('firm_id')['roa'].rolling(window=3).mean().reset_index(0, drop=True)

# 変動係数
df['roa_volatility'] = df.groupby('firm_id')['roa'].rolling(window=5).std().reset_index(0, drop=True)
```

### 2. Model Validation

**クロスバリデーション**:
```python
from sklearn.model_selection import cross_val_score

# K-fold CV
scores = cross_val_score(
    rf, X_train, y_train, 
    cv=5,  # 5-fold
    scoring='f1'
)
print(f"CV F1 scores: {scores}")
print(f"Mean F1: {scores.mean():.3f} (+/- {scores.std() * 2:.3f})")
```

**時系列データのCV**:
```python
from sklearn.model_selection import TimeSeriesSplit

# Time series split
tscv = TimeSeriesSplit(n_splits=5)

for train_idx, test_idx in tscv.split(X):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
    
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    print(f"Score: {score:.3f}")
```

**不均衡データ対策**:
```python
from imblearn.over_sampling import SMOTE

# SMOTE (Synthetic Minority Over-sampling)
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

print(f"Before SMOTE: {y_train.value_counts()}")
print(f"After SMOTE: {pd.Series(y_resampled).value_counts()}")
```

### 3. Interpretation

**SHAP Values**:
```python
import shap

# SHAP説明
explainer = shap.TreeExplainer(rf)
shap_values = explainer.shap_values(X_test)

# 要約プロット
shap.summary_plot(shap_values[1], X_test, feature_names=X.columns)

# 個別予測の説明
shap.force_plot(explainer.expected_value[1], shap_values[1][0], X_test.iloc[0])
```

**Partial Dependence Plot**:
```python
from sklearn.inspection import partial_dependence, PartialDependenceDisplay

# PDP作成
features_to_plot = [0, 1]  # Feature indices
PartialDependenceDisplay.from_estimator(rf, X_train, features_to_plot)
plt.show()
```

---

## Common Pitfalls

### 1. Look-ahead Bias (未来情報の使用)

❌ **悪い例**:
```python
# 年度tの倒産を予測するのに、年度tのデータを使用
X = df[df['year'] == 2020][features]
y = df[df['year'] == 2020]['bankrupt']  # 2020年の倒産
```

✅ **良い例**:
```python
# 年度t-1のデータで年度tの倒産を予測
df['bankrupt_next_year'] = df.groupby('firm_id')['bankrupt'].shift(-1)
X = df[df['year'] == 2019][features]
y = df[df['year'] == 2019]['bankrupt_next_year']
```

### 2. Data Leakage (情報漏洩)

❌ **悪い例**:
```python
# Train/Test分割前にスケーリング
X_scaled = scaler.fit_transform(X)
X_train, X_test = train_test_split(X_scaled)
```

✅ **良い例**:
```python
# Train/Test分割後にスケーリング
X_train, X_test = train_test_split(X)
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # fit不要
```

### 3. Ignoring Class Imbalance

❌ **悪い例**:
```python
# 不均衡データ（倒産1%）でデフォルト設定
rf = RandomForestClassifier()
rf.fit(X_train, y_train)
# → 全て非倒産と予測してAccuracy 99%達成
```

✅ **良い例**:
```python
# class_weight='balanced'を使用
rf = RandomForestClassifier(class_weight='balanced')
rf.fit(X_train, y_train)

# またはF1-scoreで評価
from sklearn.metrics import f1_score
f1 = f1_score(y_test, y_pred)
```

### 4. Overfitting

❌ **悪い例**:
```python
# 過度に複雑なモデル
rf = RandomForestClassifier(
    n_estimators=1000,
    max_depth=None,  # 制限なし
    min_samples_split=2
)
# Train accuracy: 100%, Test accuracy: 60%
```

✅ **良い例**:
```python
# 適切な正則化
rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=20,
    min_samples_leaf=10
)
# クロスバリデーションで検証
```

### 5. Ignoring Temporal Structure

❌ **悪い例**:
```python
# パネルデータをランダムシャッフル
X_train, X_test = train_test_split(X, shuffle=True)
```

✅ **良い例**:
```python
# 時系列構造を保持
train_years = [2010, 2011, 2012, 2013, 2014]
test_years = [2015, 2016]

X_train = df[df['year'].isin(train_years)][features]
X_test = df[df['year'].isin(test_years)][features]
```

---

## FAQ

### Q1: クラスタ数はどう決めればよいか？

**A**: 以下の方法を併用：

1. **エルボー法**: Inertiaの減少が緩やかになる点
2. **Silhouette Score**: 最大値を与えるk
3. **ドメイン知識**: 既存研究での戦略グループ数
4. **ビジネス判断**: 実務的に意味のある分割数

```python
# 複数指標で評価
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(X_scaled)
    
    silhouette = silhouette_score(X_scaled, labels)
    davies_bouldin = davies_bouldin_score(X_scaled, labels)
    
    print(f"k={k}: Silhouette={silhouette:.3f}, DB={davies_bouldin:.3f}")
```

### Q2: 財務データに適した特徴量は？

**A**: 4つのカテゴリから選択：

1. **収益性**: ROA, ROE, Profit Margin
2. **効率性**: Asset Turnover, Inventory Turnover
3. **安全性**: Current Ratio, Debt-to-Equity, Z-score
4. **成長性**: Sales Growth, Asset Growth

**推奨**: 各カテゴリから1-2変数ずつ選択（合計5-8変数）

### Q3: 標準化は必須か？

**A**: **必須**（距離ベースの手法では）

- K-means, Hierarchical, DBSCAN → 必須
- Random Forest, XGBoost → 不要（ツリーベース）
- PCA, t-SNE → 必須

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

### Q4: 不均衡データの基準は？

**A**: マイノリティクラスが**10%未満**の場合は対策必要

**対策方法**:
1. `class_weight='balanced'` 使用
2. SMOTE等のオーバーサンプリング
3. F1-score、AUC等の適切な評価指標使用
4. アンダーサンプリング（データが豊富な場合）

### Q5: 特徴量はいくつ必要か？

**A**: **サンプルサイズの10%程度**が目安

- サンプル100: 特徴量10個程度
- サンプル1,000: 特徴量100個程度

**多すぎる場合**:
- PCAで次元削減
- Feature Selection（重要度ベース）
- Regularization (Lasso, Ridge)

### Q6: テストデータの割合は？

**A**: 通常**20-30%**

- 小データ（n<500）: 30%
- 中データ（500<n<5000）: 20%
- 大データ（n>5000）: 10-20%

### Q7: ハイパーパラメータ調整は？

**A**: Grid SearchまたはRandom Searchを使用

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15],
    'min_samples_split': [10, 20, 30]
}

grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring='f1',
    n_jobs=-1
)
grid_search.fit(X_train, y_train)

print(f"Best params: {grid_search.best_params_}")
print(f"Best F1: {grid_search.best_score_:.3f}")
```

### Q8: PCAで何次元まで削減すべきか？

**A**: **累積寄与率80-90%**を目標

```python
from sklearn.decomposition import PCA

pca = PCA()
pca.fit(X_scaled)

# 累積寄与率
cumsum = np.cumsum(pca.explained_variance_ratio_)

# 90%達成に必要な次元数
n_components = np.argmax(cumsum >= 0.9) + 1
print(f"Components for 90% variance: {n_components}")
```

### Q9: 異常検知の閾値は？

**A**: **Contamination parameter**で調整

- 厳しい基準: 1-5%
- 標準的: 5-10%
- 緩い基準: 10-20%

```python
iso_forest = IsolationForest(contamination=0.05)  # 5%を異常とする
```

### Q10: 時系列予測の評価指標は？

**A**: **RMSE、MAE、MAPE**を使用

```python
from sklearn.metrics import mean_squared_error, mean_absolute_error

rmse = np.sqrt(mean_squared_error(y_true, y_pred))
mae = mean_absolute_error(y_true, y_pred)
mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100

print(f"RMSE: {rmse:.3f}, MAE: {mae:.3f}, MAPE: {mape:.1f}%")
```

---

## 🔗 Related Skills

- **core-workflow**: Phase 6 (Variable Construction)
- **statistical-methods**: Feature engineering and validation
- **text-analysis**: Text features for clustering
- **network-analysis**: Network features for classification

---

## 📚 References

### Books
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning*
- James, G., Witten, D., Hastie, T., & Tibshirani, R. (2013). *An Introduction to Statistical Learning*

### Papers
- Porter, M. E. (1980). Competitive Strategy (Strategic Groups)
- Altman, E. I. (1968). Financial Ratios, Discriminant Analysis and the Prediction of Corporate Bankruptcy

### Libraries
- scikit-learn: https://scikit-learn.org/
- XGBoost: https://xgboost.readthedocs.io/
- SHAP: https://github.com/slundberg/shap

---

**作成日**: 2025-11-01  
**バージョン**: 4.0  
**メンテナー**: Strategic Research Suite Team
