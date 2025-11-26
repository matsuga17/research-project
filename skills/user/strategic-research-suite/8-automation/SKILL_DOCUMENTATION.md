---
name: strategic-research-automation
description: End-to-end research automation pipeline for strategic management studies including data collection, preprocessing, analysis, and documentation with reproducibility package generation.
version: 4.0
part_of: strategic-research-suite
related_skills:
  - core-workflow: Phase 3 (Data Collection), Phase 8 (Documentation)
  - data-sources: Automated data collection
  - statistical-methods: Automated analysis
---

# Research Automation Pipeline v4.0

**Part of**: [Strategic Research Suite v4.0](../README.md)

---

## 🎯 このスキルについて

**Phase 1-8完全自動化**のためのスクリプトとベストプラクティスを提供します。

### いつ使うか

- ✅ 研究プロジェクト全体を一括実行したい
- ✅ 再現可能性を最大化したい
- ✅ 複数の研究を並行実行したい
- ✅ データ収集〜分析を自動化したい

### 前提条件

- Python中級（クラス設計、エラーハンドリング）
- プロジェクト管理の基礎
- Git基礎（バージョン管理）

### 他スキルとの連携

- すべてのスキルを統合

---

## 📋 目次

1. [プロジェクト構造](#1-プロジェクト構造)
2. [自動化パイプライン](#2-自動化パイプライン)
3. [再現パッケージ](#3-再現パッケージ)
4. [Quick Reference](#4-quick-reference)

---

## 1. プロジェクト構造

### 1.1 標準ディレクトリ構造

```
research_project/
├── data/
│   ├── raw/              # 生データ（変更厳禁）
│   ├── processed/        # 前処理済み
│   └── final/            # 分析用最終版
├── code/
│   ├── 01_collect.py     # データ収集
│   ├── 02_clean.py       # クリーニング
│   ├── 03_merge.py       # マージ
│   ├── 04_variables.py   # 変数構築
│   ├── 05_analysis.py    # 統計分析
│   └── 06_visualize.py   # 可視化
├── output/
│   ├── tables/           # 回帰結果表
│   ├── figures/          # 図
│   └── logs/             # 実行ログ
├── docs/
│   ├── data_dictionary.md
│   ├── codebook.md
│   └── README.md
├── config.yaml           # 設定ファイル
├── requirements.txt      # 依存パッケージ
├── run_all.sh            # 全スクリプト実行
└── README.md
```

### 1.2 自動生成スクリプト

```python
import os

def create_project_structure(project_name):
    """研究プロジェクト構造を自動生成"""
    
    dirs = [
        f'{project_name}/data/raw',
        f'{project_name}/data/processed',
        f'{project_name}/data/final',
        f'{project_name}/code',
        f'{project_name}/output/tables',
        f'{project_name}/output/figures',
        f'{project_name}/output/logs',
        f'{project_name}/docs'
    ]
    
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    
    # README生成
    readme = f"""# {project_name}

## Research Question
[記入してください]

## Data Sources
- Source 1: [詳細]
- Source 2: [詳細]

## Execution
```bash
bash run_all.sh
```

## Output
- Tables: `output/tables/`
- Figures: `output/figures/`
"""
    
    with open(f'{project_name}/README.md', 'w') as f:
        f.write(readme)
    
    print(f"Project structure created: {project_name}/")

# 使用例
create_project_structure('rd_performance_study')
```

---

## 2. 自動化パイプライン

### 2.1 StrategicResearchPipeline クラス

```python
import pandas as pd
import logging
from datetime import datetime

class StrategicResearchPipeline:
    """Phase 1-8完全自動化パイプライン"""
    
    def __init__(self, config):
        """
        Args:
            config: dict with keys:
                - research_question: str
                - data_sources: list of dict
                - sample_criteria: dict
                - output_dir: str
        """
        self.config = config
        self.setup_logging()
    
    def setup_logging(self):
        """ログ設定"""
        log_file = f"output/logs/run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def phase1_design(self):
        """Phase 1: Research Design"""
        self.logger.info("=== Phase 1: Research Design ===")
        self.logger.info(f"RQ: {self.config['research_question']}")
        
        # 仮説をログに記録
        for i, hyp in enumerate(self.config.get('hypotheses', []), 1):
            self.logger.info(f"H{i}: {hyp}")
    
    def phase2_collect_data(self):
        """Phase 2-3: Data Collection"""
        self.logger.info("=== Phase 2-3: Data Collection ===")
        
        dfs = []
        for source in self.config['data_sources']:
            self.logger.info(f"Collecting from: {source['name']}")
            
            # データソース別の収集ロジック
            if source['type'] == 'compustat':
                df = self._collect_compustat(source['params'])
            elif source['type'] == 'edinet':
                df = self._collect_edinet(source['params'])
            else:
                raise ValueError(f"Unknown source type: {source['type']}")
            
            dfs.append(df)
            self.logger.info(f"  Collected: {len(df)} records")
        
        return dfs
    
    def phase4_build_panel(self, dfs):
        """Phase 4: Panel Dataset Construction"""
        self.logger.info("=== Phase 4: Panel Construction ===")
        
        # マージ
        df_panel = dfs[0]
        for df in dfs[1:]:
            df_panel = df_panel.merge(df, on=['firm_id', 'year'], how='inner')
        
        # MultiIndex設定
        df_panel = df_panel.set_index(['firm_id', 'year']).sort_index()
        
        self.logger.info(f"Panel size: {len(df_panel)} firm-years")
        self.logger.info(f"Firms: {df_panel.index.get_level_values('firm_id').nunique()}")
        
        return df_panel
    
    def phase5_quality_check(self, df):
        """Phase 5: Quality Assurance"""
        self.logger.info("=== Phase 5: QA ===")
        
        # 欠損値チェック
        missing = df.isnull().sum()
        self.logger.info(f"Missing values:\n{missing[missing > 0]}")
        
        # 外れ値チェック
        from scipy.stats import zscore
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        
        for col in numeric_cols:
            outliers = (abs(zscore(df[col].dropna())) > 3).sum()
            if outliers > 0:
                self.logger.warning(f"{col}: {outliers} outliers detected")
        
        return df
    
    def phase6_construct_variables(self, df):
        """Phase 6: Variable Construction"""
        self.logger.info("=== Phase 6: Variables ===")
        
        # 標準変数構築
        df['roa'] = df['net_income'] / df['total_assets']
        df['rd_intensity'] = df['rd_expense'] / df['revenue']
        df['firm_size'] = np.log(df['total_assets'])
        df['leverage'] = df['total_debt'] / df['total_assets']
        
        # ラグ変数
        df = df.reset_index()
        df = df.sort_values(['firm_id', 'year'])
        df['rd_intensity_lag1'] = df.groupby('firm_id')['rd_intensity'].shift(1)
        df = df.set_index(['firm_id', 'year'])
        
        self.logger.info("Variables constructed")
        
        return df
    
    def phase7_analyze(self, df):
        """Phase 7: Statistical Analysis"""
        self.logger.info("=== Phase 7: Analysis ===")
        
        from linearmodels.panel import PanelOLS
        
        # メインモデル
        model = PanelOLS.from_formula(
            'roa ~ rd_intensity_lag1 + firm_size + leverage + EntityEffects + TimeEffects',
            data=df
        )
        
        result = model.fit(cov_type='clustered', cluster_entity=True)
        
        self.logger.info("Main model estimated")
        self.logger.info(f"R-squared: {result.rsquared:.4f}")
        
        # 結果保存
        with open('output/tables/main_results.txt', 'w') as f:
            f.write(result.summary.as_text())
        
        return result
    
    def phase8_document(self, df, result):
        """Phase 8: Documentation"""
        self.logger.info("=== Phase 8: Documentation ===")
        
        # Data Dictionary
        data_dict = {
            'variable': df.columns.tolist(),
            'description': ['...'] * len(df.columns),
            'mean': df.mean().values,
            'std': df.std().values
        }
        
        pd.DataFrame(data_dict).to_csv('docs/data_dictionary.csv', index=False)
        
        # 再現パッケージ
        self._create_replication_package(df, result)
        
        self.logger.info("Documentation completed")
    
    def run_full_pipeline(self):
        """完全パイプライン実行"""
        try:
            self.phase1_design()
            dfs = self.phase2_collect_data()
            df_panel = self.phase4_build_panel(dfs)
            df_panel = self.phase5_quality_check(df_panel)
            df_panel = self.phase6_construct_variables(df_panel)
            result = self.phase7_analyze(df_panel)
            self.phase8_document(df_panel, result)
            
            self.logger.info("=== PIPELINE COMPLETED ===")
            
            return {
                'data': df_panel,
                'result': result,
                'status': 'success'
            }
        
        except Exception as e:
            self.logger.error(f"Pipeline failed: {e}")
            return {'status': 'failed', 'error': str(e)}

# 使用例
config = {
    'research_question': "R&D投資は企業パフォーマンスに正の影響を与えるか？",
    'hypotheses': [
        "H1: R&D投資強度はROAに正の影響を与える"
    ],
    'data_sources': [
        {'name': 'Compustat', 'type': 'compustat', 'params': {...}},
    ],
    'sample_criteria': {
        'industry': 'manufacturing',
        'years': (2010, 2020)
    },
    'output_dir': './output/'
}

pipeline = StrategicResearchPipeline(config)
results = pipeline.run_full_pipeline()
```

---

## 3. 再現パッケージ

### 3.1 必須要素

```python
def create_replication_package(output_dir='replication_package'):
    """再現パッケージ生成"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. README
    readme = """# Replication Package

## Requirements
```bash
pip install -r requirements.txt
```

## Data
- Place raw data in `data/raw/`
- Data sources: [詳細]

## Execution
```bash
bash run_all.sh
```

## Expected Output
- Tables: `output/tables/`
- Figures: `output/figures/`
- Estimated time: 2 hours

## Contact
[Your Email]
"""
    
    with open(f'{output_dir}/README.md', 'w') as f:
        f.write(readme)
    
    # 2. requirements.txt
    requirements = """pandas==2.0.0
numpy==1.24.0
statsmodels==0.14.0
linearmodels==5.3
scikit-learn==1.3.0
matplotlib==3.7.0
"""
    
    with open(f'{output_dir}/requirements.txt', 'w') as f:
        f.write(requirements)
    
    # 3. run_all.sh
    run_script = """#!/bin/bash
echo "Starting replication..."

python code/01_collect.py
python code/02_clean.py
python code/03_merge.py
python code/04_variables.py
python code/05_analysis.py
python code/06_visualize.py

echo "Replication completed!"
"""
    
    with open(f'{output_dir}/run_all.sh', 'w') as f:
        f.write(run_script)
    
    os.chmod(f'{output_dir}/run_all.sh', 0o755)
    
    print(f"Replication package created: {output_dir}/")

create_replication_package()
```

### 3.2 Docker化（オプション）

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /research

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash", "run_all.sh"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  research:
    build: .
    volumes:
      - ./data:/research/data
      - ./output:/research/output
    environment:
      - WRDS_USERNAME=${WRDS_USERNAME}
      - WRDS_PASSWORD=${WRDS_PASSWORD}
```

---

## 4. Quick Reference

### 自動化レベル

| レベル | 内容 | 所要時間 |
|--------|------|---------|
| **Level 1** | データ収集のみ | 1-2時間 |
| **Level 2** | 収集 + 前処理 | 3-4時間 |
| **Level 3** | 収集 + 前処理 + 分析 | 1日 |
| **Level 4** | Phase 1-8完全自動化 | 1-2日 |

### エラーハンドリング

```python
import time
from functools import wraps

def retry_on_failure(max_retries=3, delay=5):
    """失敗時のリトライデコレータ"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                    time.sleep(delay)
        return wrapper
    return decorator

# 使用例
@retry_on_failure(max_retries=3, delay=10)
def collect_data_with_retry():
    # API呼び出し等
    pass
```

### 進捗モニタリング

```python
from tqdm import tqdm

def process_firms(firm_ids):
    """進捗バー付き処理"""
    results = []
    
    for firm_id in tqdm(firm_ids, desc="Processing firms"):
        result = process_single_firm(firm_id)
        results.append(result)
    
    return results
```

---

## ベストプラクティス

### 1. 設定ファイルの使用

```yaml
# config.yaml
research:
  question: "R&D投資の効果は企業規模で異なるか？"
  
data:
  sources:
    - name: compustat
      years: [2010, 2020]
    - name: crsp
      frequency: monthly

sample:
  industry_codes: [2000, 3999]
  min_observations: 5

analysis:
  dependent_var: roa
  independent_vars: [rd_intensity, firm_size, leverage]
  fixed_effects: [entity, time]
```

### 2. ログの活用

```python
import logging

logging.info("Data collection started")
logging.warning("Missing data detected for firm 123")
logging.error("API connection failed")
```

### 3. バージョン管理

```bash
# Git初期化
git init
git add .
git commit -m "Initial commit: Research project setup"

# .gitignore
data/raw/
output/
*.log
__pycache__/
```

---

## パッケージインストール

```bash
pip install pandas numpy statsmodels linearmodels scikit-learn matplotlib pyyaml tqdm
```

---

## 参考文献

- Christensen, G., & Miguel, E. (2018). "Transparency, reproducibility, and the credibility of economics research." *Journal of Economic Literature*, 56(3), 920-980.

---

**Version**: 4.0  
**Last Updated**: 2025-11-01  
**Complete**: All 8 skills finished! 🎉
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
