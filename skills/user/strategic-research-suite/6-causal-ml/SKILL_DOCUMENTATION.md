---
name: strategic-research-causal-ml
description: Causal inference with machine learning for strategic management research including Causal Forest for heterogeneous treatment effects, Double Machine Learning for high-dimensional confounding, and Synthetic Control Method for comparative case studies.
version: 4.0
part_of: strategic-research-suite
related_skills:
  - core-workflow: Phase 7 (Statistical Analysis)
  - statistical-methods: Traditional causal inference
  - automation: ML pipeline automation
---

# Causal ML Toolkit v4.0

**Part of**: [Strategic Research Suite v4.0](../README.md)

---

## 🎯 このスキルについて

**因果推論×機械学習**の最新手法を提供します。処置効果の異質性、高次元交絡、比較事例研究に対応します。

### いつ使うか

- ✅ 処置効果が企業によって異なる（Heterogeneous Treatment Effects）
- ✅ 統制変数が多すぎる（高次元交絡）
- ✅ 少数処置ユニットのイベント研究（比較事例）
- ✅ 従来手法（IV, PSM）が機能しない時

### 前提条件

- 因果推論の基礎（処置・アウトカム・交絡）
- 機械学習の基本（決定木、正則化）
- Python（scikit-learn, econml）

### 他スキルとの連携

- **基本因果推論** → `3-statistical-methods`（IV, PSM, DiD）
- **データ準備** → `1-core-workflow` Phase 6
- **標準分析** → `3-statistical-methods`

---

## 📋 目次

1. [Causal Forest](#1-causal-forest)
2. [Double Machine Learning](#2-double-machine-learning-dml)
3. [Synthetic Control Method](#3-synthetic-control-method)
4. [Quick Reference](#4-quick-reference)

---

## 1. Causal Forest

### 1.1 概念

**Causal Forest**: ランダムフォレストで個別処置効果（CATE）を推定

```
CATE(X) = E[Y(1) - Y(0) | X]

Y(1): 処置時のアウトカム
Y(0): 非処置時のアウトカム
X: 企業特性
```

**いつ使うか**:
- R&D投資の効果が企業規模で異なる
- M&Aの効果が産業で異なる
- CSR活動の効果が地域で異なる

### 1.2 実装: EconML

```python
from econml.dml import CausalForestDML
import pandas as pd
import numpy as np

# データ準備
# Y: アウトカム（ROA）
# T: 処置変数（R&D投資高=1）
# X: 効果修正変数（firm_size, industry等）
# W: 交絡変数（統制変数）

df = pd.read_csv('firm_data.csv')

Y = df['roa'].values
T = df['high_rd'].values  # R&D高=1
X = df[['firm_size', 'firm_age', 'leverage']].values
W = df[['industry', 'year']].values

# Causal Forest推定
cf = CausalForestDML(
    model_y=None,  # Auto: Random Forest
    model_t=None,  # Auto: Random Forest
    n_estimators=1000,
    random_state=42
)

cf.fit(Y, T, X=X, W=W)

# 個別処置効果（CATE）
cate = cf.effect(X)

print(f"Mean CATE: {cate.mean():.4f}")
print(f"CATE std: {cate.std():.4f}")
print(f"CATE range: [{cate.min():.4f}, {cate.max():.4f}]")

# 企業別CATE
df['cate'] = cate
print(df[['firm_id', 'firm_size', 'cate']].head(10))
```

### 1.3 異質性の分析

```python
# CATEと企業特性の関係
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.scatter(df['firm_size'], df['cate'], alpha=0.5)
plt.xlabel('Firm Size (log)')
plt.ylabel('CATE (R&D Effect)')
plt.title('Treatment Effect Heterogeneity by Firm Size')
plt.axhline(y=0, color='r', linestyle='--')
plt.show()

# 統計的検定: CATE分散が有意か
from scipy import stats

# H0: 全企業で処置効果が同じ（分散=0）
# H1: 処置効果が異質的（分散>0）

# Best Linear Projection (BLP) test
blp_model = cf.effect_inference(X)
print(blp_model.summary_frame())
```

### 1.4 戦略研究への応用

**仮説**: R&D効果は企業規模で異なる

```python
# 大企業 vs 小企業のCATE比較
large_firms = df[df['firm_size'] > df['firm_size'].median()]
small_firms = df[df['firm_size'] <= df['firm_size'].median()]

cate_large = large_firms['cate'].mean()
cate_small = small_firms['cate'].mean()

print(f"CATE (Large firms): {cate_large:.4f}")
print(f"CATE (Small firms): {cate_small:.4f}")
print(f"Difference: {cate_large - cate_small:.4f}")

# t検定
t_stat, p_value = stats.ttest_ind(large_firms['cate'], small_firms['cate'])
print(f"t-statistic: {t_stat:.4f}, p-value: {p_value:.4f}")
```

---

## 2. Double Machine Learning (DML)

### 2.1 概念

**DML**: 高次元交絡下での因果効果推定

**問題**: 統制変数が100+ある → 通常のOLSは破綻

**解決**: 
1. ML（Lasso, RF等）で Y ~ W, T ~ W を予測
2. 残差で因果効果推定

### 2.2 実装

```python
from econml.dml import LinearDML
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

# 高次元統制変数（100+）
W_high_dim = df[[col for col in df.columns if 'control_' in col]].values

# DML推定
dml = LinearDML(
    model_y=RandomForestRegressor(n_estimators=100),
    model_t=RandomForestClassifier(n_estimators=100),
    discrete_treatment=True,
    random_state=42
)

dml.fit(Y, T, X=None, W=W_high_dim)

# 平均処置効果（ATE）
ate = dml.effect().mean()
print(f"Average Treatment Effect: {ate:.4f}")

# 信頼区間
ate_inference = dml.effect_inference()
ci = ate_inference.conf_int()
print(f"95% CI: [{ci[0][0]:.4f}, {ci[1][0]:.4f}]")
```

### 2.3 DML vs 通常回帰の比較

```python
from sklearn.linear_model import LogisticRegression
from linearmodels.panel import PanelOLS

# 通常のOLS（参考: 高次元でバイアス）
# （実装は簡略化）

print("=== Comparison ===")
print(f"DML ATE: {ate:.4f}")
print("DML handles high-dimensional confounding robustly")
```

---

## 3. Synthetic Control Method

### 3.1 概念

**Synthetic Control**: 処置ユニットの「合成対照群」を構築

**例**: 
- 企業A（処置: M&A実施）
- 企業B, C, D...（対照: M&A未実施）
- 合成A' = 0.3×B + 0.5×C + 0.2×D（処置前のAに類似）

**いつ使うか**:
- 処置ユニットが1社のみ（ケーススタディ）
- 少数の処置ユニット（< 10社）
- DiDのParallel Trends仮定が疑わしい

### 3.2 実装

```python
from sklearn.linear_model import Ridge

def synthetic_control(treated_id, control_ids, df, outcome_var, treatment_year):
    """Synthetic Control推定
    
    Args:
        treated_id: 処置企業ID
        control_ids: 対照企業IDのリスト
        df: パネルデータ
        outcome_var: アウトカム変数名
        treatment_year: 処置年
    
    Returns:
        weights: 合成ウェイト
        synthetic_control: 合成対照群の時系列
        att: 処置後の平均処置効果
    """
    
    # 処置前期間
    pre_period = df[df['year'] < treatment_year]
    post_period = df[df['year'] >= treatment_year]
    
    # 処置企業の処置前アウトカム
    y_treated_pre = pre_period[pre_period['firm_id'] == treated_id][outcome_var].values
    
    # 対照企業の処置前アウトカム（行列）
    X_control_pre = []
    for cid in control_ids:
        y_c = pre_period[pre_period['firm_id'] == cid][outcome_var].values
        X_control_pre.append(y_c)
    X_control_pre = np.array(X_control_pre).T
    
    # ウェイト推定（Ridge回帰、非負制約）
    ridge = Ridge(alpha=0.01, fit_intercept=False, positive=True)
    ridge.fit(X_control_pre, y_treated_pre)
    weights = ridge.coef_
    weights = weights / weights.sum()  # 正規化
    
    # 合成対照群の構築（全期間）
    synthetic = []
    for year in df['year'].unique():
        df_year = df[df['year'] == year]
        y_controls = [df_year[df_year['firm_id'] == cid][outcome_var].values[0] 
                      for cid in control_ids]
        synthetic.append(np.dot(weights, y_controls))
    
    synthetic = pd.Series(synthetic, index=df['year'].unique())
    
    # 処置後の平均処置効果（ATT）
    y_treated_post = post_period[post_period['firm_id'] == treated_id][outcome_var].values
    y_synthetic_post = synthetic[synthetic.index >= treatment_year].values
    
    att = (y_treated_post - y_synthetic_post).mean()
    
    return weights, synthetic, att

# 使用例
treated_firm = 'A'
control_firms = ['B', 'C', 'D', 'E', 'F']

weights, synthetic, att = synthetic_control(
    treated_id=treated_firm,
    control_ids=control_firms,
    df=df,
    outcome_var='roa',
    treatment_year=2018
)

print(f"\n=== Synthetic Control Weights ===")
for i, firm in enumerate(control_firms):
    print(f"{firm}: {weights[i]:.3f}")

print(f"\nAverage Treatment Effect on Treated: {att:.4f}")
```

### 3.3 可視化

```python
import matplotlib.pyplot as plt

# 処置企業と合成対照群の比較
df_treated = df[df['firm_id'] == treated_firm].set_index('year')['roa']

plt.figure(figsize=(12, 6))
plt.plot(df_treated.index, df_treated.values, 'b-', linewidth=2, label='Treated')
plt.plot(synthetic.index, synthetic.values, 'r--', linewidth=2, label='Synthetic Control')
plt.axvline(x=2018, color='gray', linestyle=':', label='Treatment')
plt.xlabel('Year')
plt.ylabel('ROA')
plt.title('Synthetic Control: Treated vs Synthetic')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

### 3.4 Placebo Test（妥当性検証）

```python
def placebo_test(control_ids, df, outcome_var, treatment_year, n_placebo=100):
    """Placebo test: ランダム企業を「偽処置」"""
    
    placebo_effects = []
    
    for _ in range(n_placebo):
        # ランダムに1社を偽処置企業に
        pseudo_treated = np.random.choice(control_ids)
        pseudo_controls = [c for c in control_ids if c != pseudo_treated]
        
        _, _, pseudo_att = synthetic_control(
            treated_id=pseudo_treated,
            control_ids=pseudo_controls,
            df=df,
            outcome_var=outcome_var,
            treatment_year=treatment_year
        )
        
        placebo_effects.append(pseudo_att)
    
    return placebo_effects

# 実行
placebo_effects = placebo_test(control_firms, df, 'roa', 2018, n_placebo=100)

# p値計算
p_value = np.mean([abs(pe) >= abs(att) for pe in placebo_effects])
print(f"\nPlacebo test p-value: {p_value:.4f}")

# 分布プロット
plt.figure(figsize=(10, 6))
plt.hist(placebo_effects, bins=30, alpha=0.7, label='Placebo ATTs')
plt.axvline(x=att, color='r', linestyle='--', linewidth=2, label=f'Actual ATT: {att:.4f}')
plt.xlabel('Treatment Effect')
plt.ylabel('Frequency')
plt.title('Placebo Test: Distribution of Pseudo-Treatment Effects')
plt.legend()
plt.show()
```

---

## 4. Quick Reference

### 手法選択ガイド

| 状況 | 推奨手法 | 理由 |
|------|---------|------|
| 処置効果の異質性を調べたい | **Causal Forest** | 個別CATE推定 |
| 統制変数が100+ | **Double ML** | 高次元対応 |
| 処置ユニットが1-10社 | **Synthetic Control** | 少数ケース対応 |
| 標準的パネル研究 | `3-statistical-methods` | FE, IV, PSM |

### Causal ML vs 従来手法

| 手法 | 処置効果 | 統制変数数 | 処置ユニット数 |
|------|---------|-----------|--------------|
| **OLS/FE** | 平均のみ | < 20 | 任意 |
| **IV/PSM** | 平均のみ | < 50 | 50+ |
| **Causal Forest** | 異質的（個別） | < 100 | 100+ |
| **Double ML** | 平均のみ | 100+ | 100+ |
| **Synthetic Control** | 個別 | 任意 | 1-10 |

### 戦略研究での使用例

**研究1**: R&D投資効果の異質性
```python
# Causal Forest → 企業規模別のCATE
cf = CausalForestDML()
cf.fit(Y=roa, T=high_rd, X=firm_characteristics, W=controls)
cate_by_size = analyze_heterogeneity(cf, by='firm_size')
```

**研究2**: 複雑な交絡構造
```python
# DML → 100+統制変数
dml = LinearDML(model_y=RandomForest, model_t=RandomForest)
dml.fit(Y=performance, T=csr_initiative, W=high_dim_controls)
```

**研究3**: Apple社のiPhone発売効果
```python
# Synthetic Control → 単一ケース
weights, synthetic, att = synthetic_control(
    treated_id='Apple',
    control_ids=tech_firms,
    treatment_year=2007
)
```

---

## 理論的注意点

### Causal Forest
- **仮定**: Unconfoundedness（交絡変数をすべて観測）
- **限界**: 観測不可能な交絡は対応不可

### Double ML
- **仮定**: Neyman orthogonality（直交性）
- **強み**: モデル誤指定に頑健

### Synthetic Control
- **仮定**: Convex hull（処置企業が対照群の凸包内）
- **限界**: 処置前期間が短いと精度低下

---

## パッケージインストール

```bash
# EconML（Causal ML toolkit）
pip install econml

# 依存関係
pip install scikit-learn pandas numpy scipy matplotlib

# オプション: CausalML（代替ライブラリ）
pip install causalml
```

---

## 参考文献

**Causal Forest**:
- Wager, S., & Athey, S. (2018). "Estimation and inference of heterogeneous treatment effects using random forests." *JASA*, 113(523), 1228-1242.

**Double ML**:
- Chernozhukov, V., et al. (2018). "Double/debiased machine learning for treatment and structural parameters." *Econometrics Journal*, 21(1), C1-C68.

**Synthetic Control**:
- Abadie, A., & Gardeazabal, J. (2003). "The economic costs of conflict: A case study of the Basque Country." *American Economic Review*, 93(1), 113-132.

---

**Version**: 4.0  
**Last Updated**: 2025-11-01  
**Next**: `7-esg-sustainability`, `8-automation` skills
**症状**:
```
HTTPError 403: Forbidden
ConnectionError: Failed to establish connection
```

**原因**:
- User-Agent未設定
- API key無効またはexpired
- IP制限・Rate limit
- ネットワーク接続問題

**解決策**:

#### 1. User-Agentを設定:
```python
headers = {
    'User-Agent': 'YourUniversity research@email.edu'
}
response = requests.get(url, headers=headers)
```

#### 2. API keyを確認:
```python
import os
api_key = os.getenv('API_KEY')
if not api_key:
    print("API key not set. Export it: export API_KEY='your_key'")
```

#### 3. Rate limitに対処:
```python
import time
from functools import wraps

def rate_limited(max_calls=10, period=60):
    """Rate limiting decorator"""
    calls = []
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            calls[:] = [c for c in calls if c > now - period]
            
            if len(calls) >= max_calls:
                sleep_time = period - (now - calls[0])
                print(f"Rate limit: sleeping {sleep_time:.1f}s")
                time.sleep(sleep_time)
            
            calls.append(time.time())
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limited(max_calls=10, period=60)
def call_api(url):
    return requests.get(url)
```

#### 4. リトライロジック:
```python
def fetch_with_retry(url, max_retries=3, backoff=5):
    """Exponential backoff retry"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                wait_time = backoff * (2 ** attempt)
                print(f"Retry {attempt + 1}/{max_retries} after {wait_time}s")
                time.sleep(wait_time)
            else:
                raise
```

---

### 🟠 Problem 2: Memory Error with Large Dataset

**症状**:
```
MemoryError: Unable to allocate array
Killed (OOM)
```

**原因**:
- データを一度に全てメモリにロード
- `float64`の過度な使用
- 不要なカラムの保持
- データのコピーが多い

**解決策**:

#### 1. Chunk processingを使用:
```python
# Instead of:
df = pd.read_csv('large_file.csv')

# Use:
chunk_size = 10000
chunks = []

for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    # Process each chunk
    processed = process_chunk(chunk)
    chunks.append(processed)

df = pd.concat(chunks, ignore_index=True)
```

#### 2. dtypeを最適化:
```python
# Memory optimization
df['year'] = df['year'].astype('int16')       # int64 → int16 (4x less)
df['firm_id'] = df['firm_id'].astype('category')  # string → category
df['industry'] = df['industry'].astype('category')

# Check memory usage
print(df.memory_usage(deep=True))
```

#### 3. 不要なカラムを削除:
```python
# Only load needed columns
df = pd.read_csv('file.csv', usecols=['col1', 'col2', 'col3'])

# Drop columns after use
df = df.drop(columns=['temp_col1', 'temp_col2'])
```

#### 4. In-place操作を使用:
```python
# Bad: creates copy
df = df.fillna(0)

# Good: in-place
df.fillna(0, inplace=True)
```

#### 5. Daskを使用（超大規模データ）:
```python
import dask.dataframe as dd

# Lazy loading
ddf = dd.read_csv('huge_file.csv')

# Parallel processing
result = ddf.groupby('firm_id').mean().compute()
```

---

### 🟡 Problem 3: Text Encoding Issues

**症状**:
```
UnicodeDecodeError: 'utf-8' codec can't decode byte
UnicodeEncodeError: 'ascii' codec can't encode character
```

**原因**:
- ファイルがUTF-8以外のエンコーディング
- 特殊文字・絵文字の処理
- HTML entities

**解決策**:

#### 1. エンコーディングを検出:
```python
import chardet

# Detect encoding
with open('file.txt', 'rb') as f:
    result = chardet.detect(f.read(10000))
    encoding = result['encoding']
    print(f"Detected encoding: {encoding}")

# Read with detected encoding
df = pd.read_csv('file.csv', encoding=encoding)
```

#### 2. エンコーディングエラーを処理:
```python
# Ignore errors
df = pd.read_csv('file.csv', encoding='utf-8', errors='ignore')

# Replace errors
df = pd.read_csv('file.csv', encoding='utf-8', errors='replace')

# Best: specify correct encoding
df = pd.read_csv('file.csv', encoding='shift_jis')  # For Japanese
```

#### 3. テキストをクリーニング:
```python
import unicodedata

def clean_text(text):
    """Remove special characters"""
    # Normalize unicode
    text = unicodedata.normalize('NFKD', text)
    # Remove non-ASCII
    text = text.encode('ascii', 'ignore').decode('ascii')
    return text

df['text'] = df['text'].apply(clean_text)
```

---

### 🟢 Problem 4: Missing Data Handling

**症状**:
- モデルが収束しない
- 統計検定で奇妙な結果
- サンプルサイズが大幅に減少

**原因**:
- 欠損値の不適切な処理
- Listwise deletion（完全データのみ使用）
- 欠損パターンの無視

**解決策**:

#### 1. 欠損値を確認:
```python
# Missing value summary
missing_summary = pd.DataFrame({
    'column': df.columns,
    'missing_count': df.isnull().sum(),
    'missing_pct': (df.isnull().sum() / len(df) * 100).round(2)
})

print(missing_summary[missing_summary['missing_count'] > 0])

# Visualize missing pattern
import missingno as msno
msno.matrix(df)
plt.show()
```

#### 2. 適切な補完方法を選択:
```python
# Mean imputation (連続変数)
df['revenue'].fillna(df['revenue'].mean(), inplace=True)

# Median imputation (外れ値がある場合)
df['revenue'].fillna(df['revenue'].median(), inplace=True)

# Forward fill (時系列データ)
df['price'] = df.groupby('firm_id')['price'].fillna(method='ffill')

# Industry mean (グループ別平均)
df['leverage'] = df.groupby('industry')['leverage'].transform(
    lambda x: x.fillna(x.mean())
)
```

#### 3. 欠損フラグを作成:
```python
# Create missing indicator
df['revenue_missing'] = df['revenue'].isnull().astype(int)

# Then impute
df['revenue'].fillna(0, inplace=True)
```

---

### 🔵 Problem 5: Slow Processing / Performance

**症状**:
- コードが数時間かかる
- CPUが100%で固まる
- プログレスバーが動かない

**解決策**:

#### 1. ボトルネックを特定:
```python
import time

# Simple timing
start = time.time()
result = slow_function()
print(f"Elapsed: {time.time() - start:.2f}s")

# Line profiler
%load_ext line_profiler
%lprun -f slow_function slow_function()
```

#### 2. Vectorization を使用:
```python
# Bad: Loop
for i in range(len(df)):
    df.loc[i, 'result'] = df.loc[i, 'a'] * df.loc[i, 'b']

# Good: Vectorized
df['result'] = df['a'] * df['b']
```

#### 3. 並列処理:
```python
from multiprocessing import Pool

def process_firm(firm_id):
    # Heavy computation
    return result

# Parallel processing
with Pool(processes=4) as pool:
    results = pool.map(process_firm, firm_ids)
```

#### 4. プログレスバー:
```python
from tqdm import tqdm

# Add progress bar
for item in tqdm(items, desc="Processing"):
    process(item)
```

---

### 📚 General Debugging Tips

#### 1. データの品質確認:
```python
# Quick data check
def check_data_quality(df):
    print(f"Shape: {df.shape}")
    print(f"\nData types:\n{df.dtypes}")
    print(f"\nMissing:\n{df.isnull().sum()}")
    print(f"\nDuplicates: {df.duplicated().sum()}")
    print(f"\nSummary:\n{df.describe()}")

check_data_quality(df)
```

#### 2. Small sampleでテスト:
```python
# Test with small sample first
df_sample = df.head(100)
result = your_function(df_sample)

# If works, run on full data
result = your_function(df)
```

#### 3. ログを出力:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

logger.info("Starting process...")
logger.warning("Missing data detected")
logger.error("API call failed")
```

---

### 🆘 When to Ask for Help

**Stack Overflow前のチェックリスト**:
1. ✅ エラーメッセージを完全に読んだか？
2. ✅ Google検索したか？
3. ✅ 公式ドキュメントを確認したか？
4. ✅ Small exampleで再現できるか？
5. ✅ パッケージバージョンを確認したか？

**質問テンプレート**:
```
【環境】
- OS: macOS 14.0
- Python: 3.11.5
- pandas: 2.0.3

【問題】
[簡潔な説明]

【再現コード】
[最小限の実行可能コード]

【エラーメッセージ】
[完全なトレースバック]

【試したこと】
1. [試した対処法1] → [結果]
2. [試した対処法2] → [結果]
```

---

**Version**: 4.0  
**Last Updated**: 2025-11-01
