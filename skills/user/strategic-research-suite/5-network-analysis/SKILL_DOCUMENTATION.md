---
name: strategic-research-network-analysis
description: Network analysis toolkit for strategic management research including board interlock networks, strategic alliance networks, and patent citation networks with centrality measures and visualization.
version: 4.0
part_of: strategic-research-suite
related_skills:
  - core-workflow: Phase 6 (Variable Construction)
  - data-sources: Network data collection
  - statistical-methods: Network variables in regression
---

# Network Analysis Toolkit v4.0

**Part of**: [Strategic Research Suite v4.0](../README.md)

---

## 🎯 このスキルについて

戦略研究における**ネットワーク分析手法**を提供します。取締役ネットワーク、戦略的提携ネットワーク、特許引用ネットワークの構築と分析をカバーします。

### いつ使うか

- ✅ 企業間関係を変数化したい時
- ✅ Board Interlock（取締役兼任）の影響を研究
- ✅ Strategic Alliance（戦略的提携）の効果を分析
- ✅ 知識スピルオーバー（特許引用）を測定

### 前提条件

- Python基礎（pandas, networkx）
- グラフ理論の基本概念
- ネットワーク可視化の理解

### 他スキルとの連携

- **変数構築** → `1-core-workflow` Phase 6
- **統計分析** → `3-statistical-methods`
- **データ収集** → `2-data-sources`

---

## 📋 目次

1. [Board Interlock Network](#1-board-interlock-network)
2. [Strategic Alliance Network](#2-strategic-alliance-network)
3. [Patent Citation Network](#3-patent-citation-network)
4. [Quick Reference](#4-quick-reference)

---

## 1. Board Interlock Network

### 1.1 概念

**Board Interlock**: 複数企業の取締役を兼任する人物を通じた企業間リンク

**理論的根拠**:
- Resource Dependence Theory: 外部資源へのアクセス
- Social Network Theory: 情報・知識の流通
- Institutional Theory: 慣行の模倣・拡散

### 1.2 データ収集

```python
import pandas as pd
import networkx as nx

# 取締役データ（例: EDINETから）
directors = pd.DataFrame({
    'director_id': [1, 1, 2, 2, 3],
    'firm_id': ['A', 'B', 'B', 'C', 'C'],
    'director_name': ['Tanaka', 'Tanaka', 'Suzuki', 'Suzuki', 'Sato'],
    'year': [2020, 2020, 2020, 2020, 2020]
})

print(directors)
```

### 1.3 ネットワーク構築

```python
def build_board_network(director_df, year):
    """取締役兼任ネットワークを構築
    
    Args:
        director_df: DataFrame with columns ['director_id', 'firm_id', 'year']
        year: Target year
        
    Returns:
        networkx.Graph: 企業間ネットワーク、エラー時は空グラフ
        
    Raises:
        ValueError: Required columns missing
    """
    # Input validation
    required_cols = ['director_id', 'firm_id', 'year']
    missing_cols = set(required_cols) - set(director_df.columns)
    
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # 指定年のデータ
    df_year = director_df[director_df['year'] == year]
    
    if len(df_year) == 0:
        print(f"Warning: No data for year {year}. Returning empty graph.")
        return nx.Graph()
    
    try:
        # Bipartite graph: 取締役 - 企業
        B = nx.Graph()
        
        for _, row in df_year.iterrows():
            # Check for null values
            if pd.isna(row['director_id']) or pd.isna(row['firm_id']):
                continue
                
            B.add_node(row['director_id'], bipartite=0)  # 取締役
            B.add_node(row['firm_id'], bipartite=1)      # 企業
            B.add_edge(row['director_id'], row['firm_id'])
        
        # Projection: 企業間ネットワーク
        firm_nodes = {n for n, d in B.nodes(data=True) if d.get('bipartite') == 1}
        
        if len(firm_nodes) < 2:
            print(f"Warning: Only {len(firm_nodes)} firm(s) found. Network may be sparse.")
        
        G = nx.bipartite.weighted_projected_graph(B, firm_nodes)
        
        print(f"Network built: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
        
        return G
        
    except Exception as e:
        print(f"Error building network: {type(e).__name__}: {e}")
        return nx.Graph()

# 実行
G_board = build_board_network(directors, 2020)
print(f"Nodes: {G_board.number_of_nodes()}, Edges: {G_board.number_of_edges()}")
```

### 1.4 中心性指標

```python
# Degree Centrality: 直接リンク数
degree_cent = nx.degree_centrality(G_board)

# Betweenness Centrality: 媒介性
between_cent = nx.betweenness_centrality(G_board)

# Eigenvector Centrality: 影響力
eigen_cent = nx.eigenvector_centrality(G_board, max_iter=1000)

# データフレーム化
centrality_df = pd.DataFrame({
    'firm_id': list(degree_cent.keys()),
    'degree_centrality': list(degree_cent.values()),
    'betweenness_centrality': list(between_cent.values()),
    'eigenvector_centrality': list(eigen_cent.values())
})

print(centrality_df)
```

### 1.5 変数構築

```python
# Panel data用に変数追加
df_firms = df_firms.merge(centrality_df, on='firm_id', how='left')

# 欠損値処理（ネットワーク未参加企業 = 0）
df_firms[['degree_centrality', 'betweenness_centrality', 'eigenvector_centrality']] = \
    df_firms[['degree_centrality', 'betweenness_centrality', 'eigenvector_centrality']].fillna(0)
```

### 1.6 可視化

```python
import matplotlib.pyplot as plt

# Spring layout
pos = nx.spring_layout(G_board, seed=42)

# ノードサイズ = Degree Centrality
node_sizes = [degree_cent[node] * 5000 for node in G_board.nodes()]

# 描画
nx.draw_networkx(
    G_board, pos, 
    node_size=node_sizes,
    node_color='lightblue',
    with_labels=True,
    font_size=8
)
plt.title('Board Interlock Network')
plt.axis('off')
plt.show()
```

---

## 2. Strategic Alliance Network

### 2.1 概念

**Strategic Alliance**: 企業間の戦略的提携（合弁、R&D協力、ライセンス等）

**理論的根拠**:
- Transaction Cost Economics: 市場 vs 階層の中間形態
- Resource-Based View: 補完的資源の獲得
- Learning Theory: 知識移転

### 2.2 データ収集

```python
# 提携データ（例: SDC, LexisNexis）
alliances = pd.DataFrame({
    'firm_a': ['A', 'A', 'B', 'C'],
    'firm_b': ['B', 'C', 'C', 'D'],
    'alliance_type': ['R&D', 'JV', 'Marketing', 'R&D'],
    'year': [2020, 2020, 2020, 2020]
})
```

### 2.3 ネットワーク構築

```python
def build_alliance_network(alliance_df, year):
    """提携ネットワークを構築"""
    df_year = alliance_df[alliance_df['year'] == year]
    
    G = nx.Graph()
    
    for _, row in df_year.iterrows():
        G.add_edge(row['firm_a'], row['firm_b'], 
                   alliance_type=row['alliance_type'])
    
    return G

G_alliance = build_alliance_network(alliances, 2020)
```

### 2.4 提携ポートフォリオ指標

```python
def calculate_alliance_metrics(G, firm_id):
    """提携ポートフォリオ指標を計算
    
    Args:
        G: NetworkX graph
        firm_id: Target firm ID
        
    Returns:
        dict: 提携指標、エラー時はデフォルト値
    """
    if G is None or G.number_of_nodes() == 0:
        print("Warning: Empty graph provided.")
        return {
            'alliance_count': 0,
            'partner_diversity': 0,
            'network_constraint': None
        }
    
    if firm_id not in G.nodes():
        return {
            'alliance_count': 0,
            'partner_diversity': 0,
            'network_constraint': None
        }
    
    try:
        # 提携数
        alliance_count = G.degree(firm_id)
        
        # Partner Diversity
        partners = list(G.neighbors(firm_id))
        partner_diversity = len(partners)
        
        # Network Constraint (Burt's Structural Holes)
        try:
            constraint = nx.constraint(G, firm_id)
        except:
            constraint = None
        
        return {
            'alliance_count': alliance_count,
            'partner_diversity': partner_diversity,
            'network_constraint': constraint
        }
        
    except Exception as e:
        print(f"Error calculating alliance metrics for {firm_id}: {type(e).__name__}: {e}")
        return {
            'alliance_count': 0,
            'partner_diversity': 0,
            'network_constraint': None
        }

# 全企業の指標計算
metrics = []
for firm in G_alliance.nodes():
    m = calculate_alliance_metrics(G_alliance, firm)
    m['firm_id'] = firm
    metrics.append(m)

alliance_metrics = pd.DataFrame(metrics)
print(alliance_metrics)
```

---

## 3. Patent Citation Network

### 3.3 概念

**Patent Citation**: 特許Aが特許Bを引用 → 知識フロー

**理論的根拠**:
- Knowledge-Based View: 知識スピルオーバー
- Innovation Theory: 技術軌道の追跡
- Absorptive Capacity: 外部知識の吸収

### 3.2 データ収集

```python
# 特許引用データ（例: USPTO, JPO）
citations = pd.DataFrame({
    'citing_patent': ['P1', 'P2', 'P3', 'P4'],
    'cited_patent': ['P0', 'P0', 'P1', 'P2'],
    'citing_firm': ['A', 'B', 'A', 'C'],
    'cited_firm': ['X', 'X', 'A', 'B'],
    'year': [2020, 2020, 2020, 2020]
})
```

### 3.3 ネットワーク構築

```python
def build_citation_network(citation_df, year):
    """特許引用ネットワークを構築（有向グラフ）"""
    df_year = citation_df[citation_df['year'] == year]
    
    G = nx.DiGraph()
    
    for _, row in df_year.iterrows():
        # 企業レベルのネットワーク
        if row['citing_firm'] != row['cited_firm']:  # 自己引用除外
            G.add_edge(row['citing_firm'], row['cited_firm'])
    
    return G

G_patent = build_citation_network(citations, 2020)
```

### 3.4 知識フロー指標

```python
def calculate_knowledge_flow(G, firm_id):
    """知識フロー指標を計算
    
    Args:
        G: NetworkX DiGraph (有向グラフ)
        firm_id: Target firm ID
        
    Returns:
        dict: 知識フロー指標、エラー時はデフォルト値
    """
    if G is None or G.number_of_nodes() == 0:
        print("Warning: Empty graph provided.")
        return {
            'knowledge_inflow': 0,
            'knowledge_outflow': 0,
            'knowledge_diversity': 0
        }
    
    if not isinstance(G, nx.DiGraph):
        print("Warning: Graph is not directed. Converting to DiGraph.")
        G = G.to_directed()
    
    if firm_id not in G.nodes():
        return {
            'knowledge_inflow': 0,
            'knowledge_outflow': 0,
            'knowledge_diversity': 0
        }
    
    try:
        # Inflow: 当該企業が他社を引用（out-degree）
        inflow = G.out_degree(firm_id)
        
        # Outflow: 他社が当該企業を引用（in-degree）
        outflow = G.in_degree(firm_id)
        
        # Diversity: 引用元企業の多様性
        sources = list(G.predecessors(firm_id))
        diversity = len(set(sources))
        
        return {
            'knowledge_inflow': inflow,
            'knowledge_outflow': outflow,
            'knowledge_diversity': diversity
        }
        
    except Exception as e:
        print(f"Error calculating knowledge flow for {firm_id}: {type(e).__name__}: {e}")
        return {
            'knowledge_inflow': 0,
            'knowledge_outflow': 0,
            'knowledge_diversity': 0
        }

# 計算
kf_metrics = []
for firm in G_patent.nodes():
    m = calculate_knowledge_flow(G_patent, firm)
    m['firm_id'] = firm
    kf_metrics.append(m)

kf_df = pd.DataFrame(kf_metrics)
print(kf_df)
```

### 3.5 Self-Citation率

```python
def calculate_self_citation_rate(citation_df, firm_id, year):
    """自己引用率を計算"""
    df_firm = citation_df[
        (citation_df['citing_firm'] == firm_id) &
        (citation_df['year'] == year)
    ]
    
    if len(df_firm) == 0:
        return 0
    
    self_citations = len(df_firm[df_firm['cited_firm'] == firm_id])
    total_citations = len(df_firm)
    
    return self_citations / total_citations

# 例
rate = calculate_self_citation_rate(citations, 'A', 2020)
print(f"Self-citation rate: {rate:.2%}")
```

---

## 4. Quick Reference

### ネットワーク指標サマリー

| 指標 | 意味 | 解釈 |
|------|------|------|
| **Degree Centrality** | 直接リンク数 | 高い = 多くの企業と接続 |
| **Betweenness Centrality** | 媒介性 | 高い = ブローカー的位置 |
| **Eigenvector Centrality** | 影響力 | 高い = 重要企業と接続 |
| **Network Constraint** | 制約度 | 低い = Structural Holes |
| **Clustering Coefficient** | クラスタ性 | 高い = 密なグループ |

### ネットワークタイプ別変数

| ネットワーク | 主要変数 | 理論的意味 |
|------------|---------|-----------|
| **Board Interlock** | Degree, Betweenness | 情報アクセス、影響力 |
| **Alliance** | Alliance Count, Diversity | 資源アクセス、学習機会 |
| **Patent Citation** | Inflow, Outflow | 知識吸収、知識拡散 |

### 戦略研究での使用例

**仮説例1**: Board Interlock → Strategic Change
```python
# H: 取締役ネットワーク中心性が高い企業は、戦略変更が早い
model = PanelOLS.from_formula(
    'strategy_change ~ degree_centrality + controls + EntityEffects',
    data=df.set_index(['firm_id', 'year'])
).fit(cov_type='clustered', cluster_entity=True)
```

**仮説例2**: Alliance Diversity → Innovation
```python
# H: 提携先の多様性が高い企業は、イノベーション成果が高い
model = PanelOLS.from_formula(
    'patent_count ~ partner_diversity + controls + EntityEffects',
    data=df.set_index(['firm_id', 'year'])
).fit(cov_type='clustered', cluster_entity=True)
```

**仮説例3**: Knowledge Inflow → Performance
```python
# H: 外部知識の流入が多い企業は、パフォーマンスが高い
model = PanelOLS.from_formula(
    'roa ~ knowledge_inflow + knowledge_outflow + controls + EntityEffects',
    data=df.set_index(['firm_id', 'year'])
).fit(cov_type='clustered', cluster_entity=True)
```

---

## パッケージインストール

```bash
pip install networkx pandas numpy matplotlib
```

---

## 参考文献

- Borgatti, S. P., & Foster, P. C. (2003). "The network paradigm in organizational research." *Journal of Management*, 29(6), 991-1013.
- Gulati, R. (1999). "Network location and learning." *Strategic Management Journal*, 20(5), 397-420.
- Brass, D. J., et al. (2004). "Taking stock of networks and organizations." *Academy of Management Journal*, 47(6), 795-817.

---

**Version**: 4.0  
**Last Updated**: 2025-11-01  
**Next**: `6-causal-ml`, `7-esg-sustainability` skills
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

## 5. 動的ネットワーク分析（時系列変化）

### 5.1 概念

**Dynamic Network Analysis**: ネットワーク構造の時系列変化を追跡

**研究での活用**:
- ネットワーク安定性の測定
- 新規tie形成パターン
- Centrality変化と企業戦略の関係
- ネットワーク進化の予測

### 5.2 時系列ネットワーク構築

```python
import networkx as nx
import pandas as pd

def build_temporal_networks(director_df, year_range):
    """複数年度のネットワークを構築
    
    Args:
        director_df: Director data with 'year' column
        year_range: List of years to analyze
        
    Returns:
        dict: {year: NetworkX graph}
    """
    networks = {}
    
    for year in year_range:
        G = build_board_network(director_df, year)
        networks[year] = G
        
        print(f"{year}: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    
    return networks

# 使用例: 2018-2023の6年間
temporal_networks = build_temporal_networks(
    directors,
    year_range=range(2018, 2024)
)

# 結果例:
# 2018: 245 nodes, 389 edges
# 2019: 251 nodes, 412 edges
# 2020: 248 nodes, 398 edges
# 2021: 253 nodes, 425 edges
# 2022: 256 nodes, 441 edges
# 2023: 259 nodes, 456 edges
```

---

### 5.3 ネットワーク変化の測定

#### 5.3.1 Jaccard係数（ネットワーク安定性）

```python
def calculate_network_stability(G1, G2):
    """2時点間のネットワーク安定性を測定
    
    Args:
        G1: Network at time t
        G2: Network at time t+1
        
    Returns:
        dict: Stability metrics
    """
    edges_t1 = set(G1.edges())
    edges_t2 = set(G2.edges())
    
    # Jaccard similarity
    intersection = edges_t1 & edges_t2
    union = edges_t1 | edges_t2
    
    jaccard = len(intersection) / len(union) if union else 0
    
    # Edge persistence rate
    persistence = len(intersection) / len(edges_t1) if edges_t1 else 0
    
    # New tie formation rate
    new_ties = edges_t2 - edges_t1
    new_tie_rate = len(new_ties) / len(edges_t2) if edges_t2 else 0
    
    # Lost tie rate
    lost_ties = edges_t1 - edges_t2
    lost_tie_rate = len(lost_ties) / len(edges_t1) if edges_t1 else 0
    
    return {
        'jaccard_similarity': jaccard,
        'edge_persistence_rate': persistence,
        'new_tie_formation_rate': new_tie_rate,
        'lost_tie_rate': lost_tie_rate,
        'new_ties_count': len(new_ties),
        'lost_ties_count': len(lost_ties)
    }

# 年度間の安定性を計算
stability_metrics = []

for year in range(2018, 2023):
    G_t = temporal_networks[year]
    G_t1 = temporal_networks[year + 1]
    
    stability = calculate_network_stability(G_t, G_t1)
    stability['year_from'] = year
    stability['year_to'] = year + 1
    
    stability_metrics.append(stability)

df_stability = pd.DataFrame(stability_metrics)
print(df_stability)

# 結果例:
#    year_from  year_to  jaccard  persistence  new_tie_rate  lost_tie_rate
# 0       2018     2019    0.756        0.823         0.167          0.177
# 1       2019     2020    0.742        0.809         0.191          0.191
# 2       2020     2021    0.768        0.831         0.169          0.169
# 3       2021     2022    0.771        0.835         0.165          0.165
# 4       2022     2023    0.779        0.841         0.159          0.159

# 発見: Jaccard係数が高い（0.75+）→ Board Interlock networkは比較的安定
```

---

#### 5.3.2 Centrality変化率

```python
def calculate_centrality_change(temporal_networks, year_range):
    """Centrality指標の経年変化を計算
    
    Returns:
        DataFrame: Panel data with centrality changes
    """
    records = []
    
    for year in year_range:
        G = temporal_networks[year]
        
        # Centrality計算
        degree_cent = nx.degree_centrality(G)
        between_cent = nx.betweenness_centrality(G)
        
        try:
            eigen_cent = nx.eigenvector_centrality(G, max_iter=1000)
        except:
            eigen_cent = {node: 0 for node in G.nodes()}
        
        for node in G.nodes():
            records.append({
                'firm_id': node,
                'year': year,
                'degree_centrality': degree_cent.get(node, 0),
                'betweenness_centrality': between_cent.get(node, 0),
                'eigenvector_centrality': eigen_cent.get(node, 0)
            })
    
    df_panel = pd.DataFrame(records)
    df_panel = df_panel.sort_values(['firm_id', 'year'])
    
    # Year-over-year change
    for metric in ['degree_centrality', 'betweenness_centrality', 'eigenvector_centrality']:
        df_panel[f'{metric}_change'] = df_panel.groupby('firm_id')[metric].diff()
        df_panel[f'{metric}_pct_change'] = df_panel.groupby('firm_id')[metric].pct_change()
    
    return df_panel

# 実行
df_centrality_panel = calculate_centrality_change(
    temporal_networks,
    year_range=range(2018, 2024)
)

print(df_centrality_panel[['firm_id', 'year', 'degree_centrality', 'degree_centrality_change']].head(10))

# 結果例:
#   firm_id  year  degree_centrality  degree_centrality_change
# 0    AAPL  2018              0.145                      NaN
# 1    AAPL  2019              0.152                    0.007
# 2    AAPL  2020              0.148                   -0.004
# 3    AAPL  2021              0.156                    0.008
# 4    AAPL  2022              0.161                    0.005
```

---

#### 5.3.3 ネットワーク密度の変化

```python
def calculate_network_density_trend(temporal_networks, year_range):
    """ネットワーク密度の経年変化"""
    
    density_metrics = []
    
    for year in year_range:
        G = temporal_networks[year]
        
        density = nx.density(G)
        avg_degree = sum(dict(G.degree()).values()) / G.number_of_nodes() if G.number_of_nodes() > 0 else 0
        
        # Clustering coefficient
        try:
            clustering = nx.average_clustering(G)
        except:
            clustering = 0
        
        # Connected components
        num_components = nx.number_connected_components(G)
        largest_component_size = len(max(nx.connected_components(G), key=len)) if G.number_of_nodes() > 0 else 0
        
        density_metrics.append({
            'year': year,
            'nodes': G.number_of_nodes(),
            'edges': G.number_of_edges(),
            'density': density,
            'avg_degree': avg_degree,
            'clustering_coef': clustering,
            'num_components': num_components,
            'largest_component_size': largest_component_size,
            'largest_component_pct': largest_component_size / G.number_of_nodes() * 100 if G.number_of_nodes() > 0 else 0
        })
    
    return pd.DataFrame(density_metrics)

df_density = calculate_network_density_trend(temporal_networks, range(2018, 2024))

print(df_density)

# 可視化
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Density
axes[0, 0].plot(df_density['year'], df_density['density'], marker='o')
axes[0, 0].set_title('Network Density')
axes[0, 0].set_ylabel('Density')

# Average Degree
axes[0, 1].plot(df_density['year'], df_density['avg_degree'], marker='s', color='orange')
axes[0, 1].set_title('Average Degree')
axes[0, 1].set_ylabel('Avg Degree')

# Clustering Coefficient
axes[1, 0].plot(df_density['year'], df_density['clustering_coef'], marker='^', color='green')
axes[1, 0].set_title('Clustering Coefficient')
axes[1, 0].set_ylabel('Clustering')
axes[1, 0].set_xlabel('Year')

# Largest Component %
axes[1, 1].plot(df_density['year'], df_density['largest_component_pct'], marker='d', color='red')
axes[1, 1].set_title('Largest Component Size')
axes[1, 1].set_ylabel('% of Network')
axes[1, 1].set_xlabel('Year')

plt.tight_layout()
plt.savefig('network_evolution.png', dpi=300)
plt.show()
```

---

### 5.4 動的可視化

```python
def create_network_animation(temporal_networks, year_range, output_file='network_evolution.gif'):
    """ネットワークの時系列アニメーション作成
    
    Requires: matplotlib, imageio
    """
    import matplotlib.pyplot as plt
    import imageio
    import os
    
    # Consistent layout（全年度で同じ位置）
    all_nodes = set()
    for G in temporal_networks.values():
        all_nodes.update(G.nodes())
    
    # Kamada-Kawai layout（安定的）
    G_combined = nx.Graph()
    G_combined.add_nodes_from(all_nodes)
    for G in temporal_networks.values():
        G_combined.add_edges_from(G.edges())
    
    pos = nx.kamada_kawai_layout(G_combined)
    
    # 各年度のフレーム作成
    filenames = []
    
    for year in year_range:
        G = temporal_networks[year]
        
        plt.figure(figsize=(10, 8))
        
        # Node size = Degree Centrality
        degree_cent = nx.degree_centrality(G)
        node_sizes = [degree_cent.get(node, 0) * 3000 for node in G.nodes()]
        
        # Draw
        nx.draw_networkx_nodes(
            G, pos,
            node_size=node_sizes,
            node_color='lightblue',
            alpha=0.7
        )
        
        nx.draw_networkx_edges(
            G, pos,
            alpha=0.3,
            width=0.5
        )
        
        # Labels（主要ノードのみ）
        top_nodes = sorted(degree_cent.items(), key=lambda x: x[1], reverse=True)[:10]
        labels = {node: node for node, _ in top_nodes}
        nx.draw_networkx_labels(G, pos, labels, font_size=8)
        
        plt.title(f'Board Interlock Network - {year}', fontsize=16)
        plt.axis('off')
        
        # Save frame
        filename = f'frame_{year}.png'
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()
        
        filenames.append(filename)
    
    # Create GIF
    images = [imageio.imread(filename) for filename in filenames]
    imageio.mimsave(output_file, images, duration=1.0)  # 1秒/フレーム
    
    # Clean up
    for filename in filenames:
        os.remove(filename)
    
    print(f"Animation saved: {output_file}")

# 実行
create_network_animation(temporal_networks, range(2018, 2024))
```

---

### 5.5 戦略研究での活用

#### 仮説1: Centrality変化 → 戦略変更

```python
from linearmodels.panel import PanelOLS

# Centrality change dataとstrategy change dataをマージ
df_merged = df_centrality_panel.merge(df_strategy, on=['firm_id', 'year'])

# Panel regression
model = PanelOLS.from_formula(
    'strategy_change ~ degree_centrality_change + betweenness_centrality_change + controls + EntityEffects + TimeEffects',
    data=df_merged.set_index(['firm_id', 'year'])
).fit(cov_type='clustered', cluster_entity=True)

print(model.summary)

# 期待: Centrality急増 → Strategic repositioning
```

#### 仮説2: ネットワーク安定性 → Performance volatility

```python
# 企業別ネットワーク安定性（平均Jaccard）
firm_stability = []

for firm_id in df_centrality_panel['firm_id'].unique():
    # その企業が関与するedgeの安定性
    # （簡略版: 企業のCentrality変動性で代用）
    
    firm_data = df_centrality_panel[df_centrality_panel['firm_id'] == firm_id]
    
    if len(firm_data) > 2:
        cent_volatility = firm_data['degree_centrality'].std()
        
        firm_stability.append({
            'firm_id': firm_id,
            'centrality_volatility': cent_volatility
        })

df_firm_stability = pd.DataFrame(firm_stability)

# Merge with performance data
df_analysis = df_firm_stability.merge(df_performance, on='firm_id')

# Correlation
print(df_analysis[['centrality_volatility', 'roa_volatility']].corr())

# 仮説: ネットワーク位置が不安定 → パフォーマンスも不安定
```

---

### 5.6 Network Event Analysis

```python
def detect_network_events(temporal_networks, year_range, threshold=0.1):
    """重要なネットワークイベントを検出
    
    Args:
        threshold: Centrality変化の閾値（10%以上で「重要」）
        
    Returns:
        DataFrame: Detected events
    """
    events = []
    
    df_cent = calculate_centrality_change(temporal_networks, year_range)
    
    for firm_id in df_cent['firm_id'].unique():
        firm_data = df_cent[df_cent['firm_id'] == firm_id].copy()
        firm_data = firm_data.sort_values('year')
        
        for idx in range(1, len(firm_data)):
            row = firm_data.iloc[idx]
            
            # Degree centralityの大幅変化
            if abs(row['degree_centrality_pct_change']) > threshold:
                event_type = 'Centrality Surge' if row['degree_centrality_pct_change'] > 0 else 'Centrality Drop'
                
                events.append({
                    'firm_id': firm_id,
                    'year': row['year'],
                    'event_type': event_type,
                    'centrality_change_pct': row['degree_centrality_pct_change'] * 100,
                    'centrality_before': firm_data.iloc[idx-1]['degree_centrality'],
                    'centrality_after': row['degree_centrality']
                })
    
    return pd.DataFrame(events)

# イベント検出
df_events = detect_network_events(temporal_networks, range(2018, 2024), threshold=0.15)

print(f"Detected {len(df_events)} significant network events")
print(df_events.sort_values('centrality_change_pct', ascending=False).head(10))

# これらのイベントと企業戦略・業績の関係を分析
# 例: Centrality急増の翌年にM&Aや新規事業参入が多いか？
```

---

**Version**: 4.0  
**Last Updated**: 2025-11-01
