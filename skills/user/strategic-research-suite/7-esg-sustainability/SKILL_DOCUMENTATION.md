---
name: strategic-research-esg-sustainability
description: ESG and sustainability data sources for strategic management research including MSCI, CDP, Refinitiv, EPA, EU ETS with variable construction for carbon intensity, ESG scores, and disclosure quality.
version: 4.0
part_of: strategic-research-suite
related_skills:
  - core-workflow: Phase 2 (Data Source Discovery), Phase 6 (Variable Construction)
  - data-sources: Additional data sources
  - statistical-methods: ESG variables in regression
---

# ESG Sustainability Data v4.0

**Part of**: [Strategic Research Suite v4.0](../README.md)

---

## 🎯 このスキルについて

**ESG/サステナビリティ研究**のためのデータソースと変数構築手法を提供します。

### いつ使うか

- ✅ ESG戦略とパフォーマンスの関係を研究
- ✅ 環境規制の影響を分析
- ✅ CSR活動の効果を測定
- ✅ サステナビリティ開示の決定要因を調査

### 前提条件

- ESG概念の基礎理解
- 環境・社会・ガバナンス指標の知識
- Python基礎（API、データ処理）

### 他スキルとの連携

- **データソース** → `2-data-sources`（財務データと統合）
- **理論** → `_shared/THEORY_FRAMEWORKS.md`（Stakeholder Theory等）
- **統計分析** → `3-statistical-methods`

---

## 📋 目次

1. [ESGデータソース](#1-esgデータソース)
2. [環境データ](#2-環境データ)
3. [ESG変数構築](#3-esg変数構築)
4. [Quick Reference](#4-quick-reference)

---

## 1. ESGデータソース

### 1.1 Premium データソース

**MSCI ESG Ratings**
- **費用**: 高額（機関契約）
- **カバレッジ**: グローバル上場企業
- **評価**: AAA-CCC（7段階）
- **強み**: 業界標準、学術研究で広く使用

**Refinitiv ESG Scores**
- **費用**: 高額（WRDS経由可能）
- **カバレッジ**: 9,000+企業
- **スコア**: 0-100
- **強み**: 詳細な項目別スコア

**Sustainalytics ESG Risk Ratings**
- **費用**: 高額
- **カバレッジ**: 13,000+企業
- **評価**: Low-Severe（5段階）

**Bloomberg ESG Data**
- **費用**: Bloomberg Terminal
- **カバレッジ**: 包括的
- **強み**: リアルタイム更新

### 1.2 Free/低コストデータソース

**CDP (Carbon Disclosure Project)**
```python
import requests
import pandas as pd

# CDP API（要登録、無料）
def get_cdp_data(company_id, year, max_retries=3):
    """CDP気候変動データ取得
    
    Args:
        company_id: CDP company ID
        year: Target year
        max_retries: 最大リトライ回数
        
    Returns:
        dict: CDPデータ、エラー時はNone
    """
    import os
    import time
    
    api_key = os.getenv('CDP_API_KEY', 'YOUR_CDP_API_KEY')
    
    if api_key == 'YOUR_CDP_API_KEY':
        print("Warning: CDP_API_KEY not set. Set with: export CDP_API_KEY='your_key'")
        print("Register at: https://www.cdp.net/")
        return None
    
    url = f"https://api.cdp.net/{year}/companies/{company_id}/climate"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'company_id': company_id,
                    'year': year,
                    'carbon_emissions': data.get('scope1_emissions', None),
                    'energy_consumption': data.get('total_energy', None),
                    'cdp_score': data.get('climate_score', None)
                }
            elif response.status_code == 404:
                print(f"Company {company_id} not found in CDP database for {year}")
                return None
            elif response.status_code == 401:
                print("Authentication failed. Check your CDP API key.")
                return None
            elif response.status_code == 429:
                print(f"Rate limit hit. Waiting 60 seconds...")
                time.sleep(60)
            else:
                print(f"HTTP Error {response.status_code}: {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            print(f"Attempt {attempt + 1}/{max_retries}: Request timed out")
            if attempt < max_retries - 1:
                time.sleep(5)
            else:
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Network error: {type(e).__name__}: {e}")
            return None
            
        except ValueError as e:
            print(f"JSON parsing error: {e}")
            return None
    
    return None

# 使用例
cdp_data = get_cdp_data('COMP001', 2023)
print(cdp_data)
```

**GRI (Global Reporting Initiative)**
- **費用**: 無料
- **内容**: サステナビリティ報告書のデータベース
- **URL**: https://database.globalreporting.org/

**EPA TRI (Toxic Release Inventory, 米国)**
```python
# EPA TRI API
def get_epa_tri_data(facility_id, year, max_retries=3):
    """EPA有害物質排出データ取得
    
    Args:
        facility_id: EPA facility ID
        year: Reporting year
        max_retries: 最大リトライ回数
        
    Returns:
        DataFrame: EPA TRIデータ、エラー時は空DataFrame
    """
    import time
    
    url = "https://data.epa.gov/efservice/tri_facility"
    
    params = {
        'FACILITY_ID': facility_id,
        'REPORTING_YEAR': year,
        'output': 'JSON'
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if not data:
                print(f"No data found for facility {facility_id} in year {year}")
                return pd.DataFrame()
            
            df = pd.DataFrame(data)
            print(f"Retrieved {len(df)} records for facility {facility_id}")
            return df
            
        except requests.exceptions.Timeout:
            print(f"Attempt {attempt + 1}/{max_retries}: Request timed out")
            if attempt < max_retries - 1:
                time.sleep(5)
            else:
                print("Max retries reached. Returning empty DataFrame.")
                return pd.DataFrame()
                
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            return pd.DataFrame()
            
        except ValueError as e:
            print(f"JSON parsing error: {e}")
            return pd.DataFrame()
            
        except Exception as e:
            print(f"Unexpected error: {type(e).__name__}: {e}")
            return pd.DataFrame()
    
    return pd.DataFrame()

# 使用例
tri_data = get_epa_tri_data('12345XMPLF', 2022)
print(tri_data[['CHEMICAL_NAME', 'TOTAL_RELEASES']].head())
```

**EU ETS (Emissions Trading System, 欧州)**
- **費用**: 無料
- **内容**: EU排出権取引データ
- **URL**: https://ec.europa.eu/clima/ets/

---

## 2. 環境データ

### 2.1 Carbon Emissions（炭素排出量）

**Scope定義**:
- **Scope 1**: 直接排出（工場、車両）
- **Scope 2**: 間接排出（購入電力）
- **Scope 3**: サプライチェーン排出

**データ構築**:
```python
def calculate_carbon_intensity(df):
    """炭素集約度を計算"""
    
    # Carbon Intensity = CO2排出量 / 売上高
    df['carbon_intensity'] = df['scope1_emissions'] / df['revenue']
    
    # Log transformation（分布の正規化）
    df['carbon_intensity_log'] = np.log(df['carbon_intensity'] + 1)
    
    return df

# 使用例
df = calculate_carbon_intensity(df)
```

### 2.2 Environmental Performance Indicators

```python
def construct_environmental_vars(df):
    """環境パフォーマンス変数構築"""
    
    # Energy Efficiency
    df['energy_efficiency'] = df['revenue'] / df['total_energy_consumption']
    
    # Waste Reduction Rate
    df['waste_reduction'] = (df['waste_t_minus1'] - df['waste_t']) / df['waste_t_minus1']
    
    # Water Consumption per Revenue
    df['water_intensity'] = df['water_consumption'] / df['revenue']
    
    # Renewable Energy Ratio
    df['renewable_ratio'] = df['renewable_energy'] / df['total_energy']
    
    return df

df = construct_environmental_vars(df)
```

---

## 3. ESG変数構築

### 3.1 ESG Composite Score

```python
def create_esg_score(df):
    """ESG総合スコア作成（複数ソースの統合）"""
    
    # 標準化（0-100スケールに）
    from sklearn.preprocessing import MinMaxScaler
    
    scaler = MinMaxScaler(feature_range=(0, 100))
    
    # 各柱を標準化
    df['e_score_std'] = scaler.fit_transform(df[['environmental_score']])
    df['s_score_std'] = scaler.fit_transform(df[['social_score']])
    df['g_score_std'] = scaler.fit_transform(df[['governance_score']])
    
    # 総合スコア（等重み）
    df['esg_score'] = (df['e_score_std'] + df['s_score_std'] + df['g_score_std']) / 3
    
    # 代替: 主成分分析（PCA）
    from sklearn.decomposition import PCA
    
    pca = PCA(n_components=1)
    df['esg_score_pca'] = pca.fit_transform(df[['e_score_std', 's_score_std', 'g_score_std']])
    
    return df

df = create_esg_score(df)
```

### 3.2 ESG Disclosure Quality

```python
def measure_disclosure_quality(df):
    """ESG開示品質を測定"""
    
    # 開示項目数（例: GRI基準）
    gri_indicators = [
        'ghg_emissions', 'energy_consumption', 'water_usage',
        'waste_generated', 'employee_diversity', 'board_diversity'
    ]
    
    # 開示率
    df['disclosure_rate'] = df[gri_indicators].notna().sum(axis=1) / len(gri_indicators)
    
    # 開示の詳細度（文字数、簡易版）
    # 実際はレポートのテキスト分析
    df['disclosure_detail'] = df['esg_report_length'] / 1000  # KB単位
    
    # 第三者保証の有無
    df['assurance'] = df['third_party_assurance'].astype(int)
    
    return df

df = measure_disclosure_quality(df)
```

### 3.3 ESG Controversy Score

```python
def calculate_controversy_score(df, controversies_df):
    """ESG論争スコア（ネガティブイベント）
    
    Args:
        df: 企業データ
        controversies_df: 論争データ（firm_id, year, controversy_type, severity）
    
    Returns:
        df: controversy_scoreを追加
    """
    
    # 各企業・年の論争件数
    controversy_counts = controversies_df.groupby(['firm_id', 'year']).size().reset_index(name='controversy_count')
    
    # 重大度加重
    severity_weights = {'Low': 1, 'Medium': 3, 'High': 5, 'Severe': 10}
    controversies_df['severity_score'] = controversies_df['severity'].map(severity_weights)
    
    controversy_severity = controversies_df.groupby(['firm_id', 'year'])['severity_score'].sum().reset_index()
    
    # マージ
    df = df.merge(controversy_counts, on=['firm_id', 'year'], how='left')
    df = df.merge(controversy_severity, on=['firm_id', 'year'], how='left')
    
    df['controversy_count'] = df['controversy_count'].fillna(0)
    df['severity_score'] = df['severity_score'].fillna(0)
    
    return df

df = calculate_controversy_score(df, controversies_df)
```

---

## 4. Quick Reference

### ESGデータソース比較

| ソース | 費用 | カバレッジ | 品質 | 学術利用 |
|--------|------|-----------|------|---------|
| **MSCI** | 高額 | グローバル | ⭐⭐⭐⭐⭐ | 最多 |
| **Refinitiv** | 高額 | グローバル | ⭐⭐⭐⭐⭐ | 多 |
| **CDP** | 無料 | グローバル | ⭐⭐⭐⭐ | 中 |
| **EPA TRI** | 無料 | 米国 | ⭐⭐⭐⭐ | 中 |
| **EU ETS** | 無料 | 欧州 | ⭐⭐⭐⭐ | 中 |

### 主要ESG変数

| 変数 | 定義 | データソース |
|------|------|-------------|
| **Carbon Intensity** | CO2排出量/売上高 | CDP, EPA |
| **ESG Score** | 総合スコア（0-100） | MSCI, Refinitiv |
| **Disclosure Quality** | 開示項目率 | GRI, CDP |
| **Controversy Score** | ネガティブ事象の重大度 | RepRisk, Refinitiv |
| **Board Diversity** | 女性取締役比率 | 有価証券報告書 |

### 戦略研究での仮説例

**H1**: ESG → Financial Performance
```python
model = PanelOLS.from_formula(
    'roa ~ esg_score + controls + EntityEffects + TimeEffects',
    data=df.set_index(['firm_id', 'year'])
).fit(cov_type='clustered', cluster_entity=True)
```

**H2**: Environmental Regulation → Innovation
```python
# EU ETS導入（2005年）の効果
model = PanelOLS.from_formula(
    'patent_count ~ eu_ets_regulated + post_2005 + eu_ets_regulated:post_2005 + controls + EntityEffects',
    data=df.set_index(['firm_id', 'year'])
).fit(cov_type='clustered', cluster_entity=True)
```

**H3**: Disclosure Quality → Cost of Capital
```python
model = PanelOLS.from_formula(
    'wacc ~ disclosure_quality + esg_score + controls + EntityEffects + TimeEffects',
    data=df.set_index(['firm_id', 'year'])
).fit(cov_type='clustered', cluster_entity=True)
```

### 理論フレームワーク

**Stakeholder Theory**:
- ESG活動 → ステークホルダー関係改善 → パフォーマンス向上

**Legitimacy Theory**:
- ESG開示 → 社会的正当性獲得 → 資源アクセス

**Resource-Based View**:
- ESG能力 → 独自の組織資源 → 競争優位

→ 詳細: `_shared/THEORY_FRAMEWORKS.md`

---

## データ収集のベストプラクティス

### 1. 複数ソースの統合
```python
# MSCI + CDP + 財務データ
df_integrated = df_financial.merge(
    df_msci, on=['firm_id', 'year'], how='left'
).merge(
    df_cdp, on=['firm_id', 'year'], how='left'
)

# 欠損値の補完（階層的）
df_integrated['esg_score'] = df_integrated['msci_esg'].fillna(df_integrated['cdp_score'])
```

### 2. 時差効果の考慮
```python
# ESG投資の効果は2-3年後に現れる
df['esg_score_lag2'] = df.groupby('firm_id')['esg_score'].shift(2)

model = PanelOLS.from_formula(
    'roa ~ esg_score_lag2 + controls + EntityEffects',
    data=df.set_index(['firm_id', 'year'])
).fit(cov_type='clustered', cluster_entity=True)
```

### 3. 内生性への対処
```python
# ESG Score → Performance の内生性
# 逆因果: Performance → ESG投資増加

# 対策: Instrumental Variable
# IV候補: 産業平均ESGスコア、地域環境規制厳格度

from linearmodels.iv import IV2SLS

iv_model = IV2SLS.from_formula(
    'roa ~ [esg_score ~ industry_avg_esg] + controls + EntityEffects + TimeEffects',
    data=df.set_index(['firm_id', 'year'])
).fit(cov_type='clustered', clusters=df['firm_id'])
```

---

## パッケージインストール

```bash
pip install pandas numpy requests scikit-learn
```

---

## 参考文献

**ESG研究**:
- Friede, G., Busch, T., & Bassen, A. (2015). "ESG and financial performance: aggregated evidence from more than 2000 empirical studies." *Journal of Sustainable Finance & Investment*, 5(4), 210-233.

**開示研究**:
- Dhaliwal, D. S., et al. (2011). "Voluntary nonfinancial disclosure and the cost of equity capital." *The Accounting Review*, 86(1), 59-100.

---

**Version**: 4.0  
**Last Updated**: 2025-11-01  
**Next**: `8-automation` skill
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
