---
name: strategic-research-data-sources
description: Comprehensive data source catalog for strategic management research covering North America (Compustat, CRSP, WRDS), Europe (Orbis, Worldscope), Asia-11 countries (Japan-EDINET, Korea-DART, China-CNINFO, ASEAN), and global free sources (World Bank, IMF, OECD, SEC EDGAR) with API implementation examples.
version: 4.0
part_of: strategic-research-suite
related_skills:
  - core-workflow: Phase 2 (Data Source Discovery)
  - statistical-methods: Data analysis integration
  - text-analysis: Text data sources (SEC EDGAR, earnings calls)
  - esg-sustainability: ESG data sources
  - automation: Automated data collection
---

# Data Sources Catalog v4.0

**Part of**: [Strategic Research Suite v4.0](../README.md)

---

## 🎯 このスキルについて

戦略経営・組織論研究で使用する**世界中のデータソース**を網羅的にカタログ化し、アクセス方法・API実装例を提供します。

### カバレッジ

```
地域別データソース:
├─ 北米（米国・カナダ）: 5大データベース
├─ 欧州: 3大データベース
├─ アジア11カ国:
│  ├─ 日本（4ソース）
│  ├─ 韓国（2ソース）
│  ├─ 中国（3ソース）
│  ├─ ASEAN 6カ国
│  └─ インド（2ソース）
└─ グローバル無料: 10+ソース
```

**合計**: 40以上のデータソース

---

### いつ使うか

✅ **Phase 2: Data Source Discovery**
- RQに適したデータソースを探す
- 各ソースの特徴・費用を比較
- アクセス方法を確認

✅ **Phase 3: Data Collection**
- API実装例を参照
- データ収集スクリプトを作成

✅ **研究計画段階**
- サンプルの実現可能性確認
- データ利用可能性の事前調査

---

### 前提条件

**必須スキル**:
- Python基礎（requests, pandas）
- API基礎（REST API, 認証）

**推奨スキル**:
- SQL基礎（WRDS等で必要）
- データクリーニング経験

**技術環境**:
- Python 3.8以上
- インターネット接続
- API認証情報（ソースによる）

---

### 他スキルとの連携

| 用途 | 連携スキル | 目的 |
|------|-----------|------|
| データ収集計画 | `1-core-workflow` Phase 2-3 | ソース選択・収集戦略 |
| テキストデータ | `4-text-analysis` | SEC EDGAR, 決算説明会 |
| ESGデータ | `7-esg-sustainability` | ESG専門ソース |
| 自動収集 | `8-automation` | 大規模自動収集 |

---

## 📋 目次

### 地域別データソース
1. [北米データソース](#1-北米データソース)
2. [欧州データソース](#2-欧州データソース)
3. [日本データソース](#3-日本データソース)
4. [韓国データソース](#4-韓国データソース)
5. [中国データソース](#5-中国データソース)
6. [ASEAN諸国](#6-asean諸国)
7. [インド](#7-インド)
8. [グローバル無料ソース](#8-グローバル無料ソース)

### 実用ガイド
9. [データソース選択マトリックス](#9-データソース選択マトリックス)
10. [API実装パターン](#10-api実装パターン)
11. [データ品質比較](#11-データ品質比較)
12. [コスト比較](#12-コスト比較)

---

## 1. 北米データソース

### 1.1 Compustat (Standard & Poor's)

**提供元**: S&P Global Market Intelligence  
**カバレッジ**: 米国・カナダ上場企業（1950年代〜現在）  
**企業数**: 25,000社以上（米国）、3,000社以上（カナダ）

#### 主要データ

**財務データ**:
- 損益計算書（Income Statement）
- 貸借対照表（Balance Sheet）
- キャッシュフロー計算書（Cash Flow）
- セグメント情報（Segment Data）

**変数例**:
```python
key_variables = {
    'at': '総資産 (Total Assets)',
    'sale': '売上高 (Sales)',
    'ni': '純利益 (Net Income)',
    'xrd': 'R&D支出 (R&D Expense)',
    'capx': '設備投資 (Capital Expenditure)',
    'dltt': '長期負債 (Long-term Debt)',
    'sich': '業界コード (SIC Code)',
    'fyear': '会計年度 (Fiscal Year)'
}
```

#### アクセス方法

**WRDS経由（推奨）**:
```python
import wrds

# WRDS接続
db = wrds.Connection(wrds_username='your_username')

# Compustat North America
query = """
SELECT 
    gvkey AS firm_id,
    fyear AS year,
    conm AS company_name,
    sich AS industry_code,
    at AS total_assets,
    sale AS sales,
    ni AS net_income,
    xrd AS rd_expense,
    capx AS capex,
    dltt AS long_term_debt,
    dlc AS short_term_debt,
    che AS cash
FROM 
    comp.funda
WHERE 
    fyear BETWEEN 2010 AND 2023
    AND indfmt = 'INDL'    -- Industrial format
    AND datafmt = 'STD'    -- Standardized data
    AND popsrc = 'D'       -- Domestic companies
    AND consol = 'C'       -- Consolidated
    AND sich BETWEEN 2000 AND 3999  -- Manufacturing
ORDER BY 
    gvkey, fyear
"""

df_compustat = db.raw_sql(query)

print(f"取得企業数: {df_compustat['firm_id'].nunique():,}社")
print(f"観測数: {len(df_compustat):,}")

# 保存
df_compustat.to_csv('data/compustat_manufacturing.csv', index=False)

db.close()
```

#### データ品質

**長所**:
- ✅ 長期時系列（70年以上）
- ✅ 標準化された変数
- ✅ 高い信頼性
- ✅ 学術研究で標準

**短所**:
- ❌ 有料（大学契約が必要）
- ❌ 小規模企業のカバレッジ限定的
- ❌ 非上場企業なし

**使用例（論文）**:
- SMJ: 80%以上がCompustat使用
- AMJ: 70%以上
- OS: 60%以上

---

### 1.2 CRSP (Center for Research in Security Prices)

**提供元**: University of Chicago Booth School of Business  
**カバレッジ**: 米国株式市場（NYSE, NASDAQ, AMEX）（1926年〜現在）

#### 主要データ

**株価・リターンデータ**:
- 日次株価（Daily Stock Prices）
- 月次リターン（Monthly Returns）
- 株式分割調整後価格（Split-adjusted Prices）
- 配当利回り（Dividend Yield）
- 市場時価総額（Market Capitalization）

#### 実装例

```python
import wrds

db = wrds.Connection(wrds_username='your_username')

# 月次株価リターン取得
query = """
SELECT 
    a.permno AS stock_id,
    a.date,
    b.ticker,
    b.comnam AS company_name,
    a.ret AS monthly_return,
    a.prc AS price,
    a.shrout AS shares_outstanding,
    a.vol AS volume
FROM 
    crsp.msf AS a
LEFT JOIN 
    crsp.msenames AS b
ON 
    a.permno = b.permno 
    AND b.namedt <= a.date 
    AND a.date <= b.nameendt
WHERE 
    a.date BETWEEN '2010-01-01' AND '2023-12-31'
    AND b.exchcd IN (1, 2, 3)  -- NYSE, AMEX, NASDAQ
ORDER BY 
    a.permno, a.date
"""

df_crsp = db.raw_sql(query)

# 市場時価総額計算
df_crsp['market_cap'] = df_crsp['price'].abs() * df_crsp['shares_outstanding']

print(f"取得銘柄数: {df_crsp['stock_id'].nunique():,}")

db.close()
```

#### Compustatとのリンク

**CRSP-Compustat Merged Database (CCM)**:
```python
# CCM Link Table
query = """
SELECT 
    lpermno AS permno,
    gvkey,
    linkdt AS link_start_date,
    linkenddt AS link_end_date
FROM 
    crsp.ccmxpf_linktable
WHERE 
    linktype IN ('LU', 'LC')
    AND linkprim IN ('P', 'C')
"""

df_link = db.raw_sql(query)

# Merge Compustat & CRSP
df_merged = df_compustat.merge(
    df_link, 
    on='gvkey', 
    how='left'
).merge(
    df_crsp,
    on='permno',
    how='left'
)
```

---

### 1.3 ExecuComp (役員報酬データ)

**提供元**: S&P Global  
**カバレッジ**: S&P 1500企業のトップ5役員（1992年〜現在）

#### 主要データ

**報酬データ**:
- 基本給（Salary）
- ボーナス（Bonus）
- ストックオプション（Stock Options）
- 制限付株式（Restricted Stock）
- 総報酬（Total Compensation）

#### 実装例

```python
import wrds

db = wrds.Connection(wrds_username='your_username')

# CEO報酬データ取得
query = """
SELECT 
    gvkey,
    year,
    exec_fullname AS ceo_name,
    salary,
    bonus,
    option_awards_blk_value AS stock_options,
    stock_awards_fv AS restricted_stock,
    tdc1 AS total_compensation,
    ceoann AS is_ceo
FROM 
    comp.execcomp
WHERE 
    year BETWEEN 2010 AND 2023
    AND ceoann = 'CEO'  -- CEOのみ
ORDER BY 
    gvkey, year
"""

df_execcomp = db.raw_sql(query)

# CEO報酬の記述統計
print("CEO報酬の記述統計（USD）:")
print(df_execcomp[['salary', 'total_compensation']].describe())

db.close()
```

#### 研究用途

**Agency Theory研究**:
- CEO報酬とパフォーマンスの関係
- Pay-performance sensitivity
- Equity-based compensation効果

---

### 1.4 Thomson Reuters SDC (M&A・IPOデータ)

**提供元**: Refinitiv (Thomson Reuters)  
**カバレッジ**: グローバルM&A、IPO、Joint Venture（1970年代〜現在）

#### 主要データ

**M&Aデータ**:
- 取引金額（Deal Value）
- 買収者・対象企業（Acquirer & Target）
- 取引形態（Deal Type）
- 支払方法（Payment Method）
- アドバイザー（Advisors）

#### アクセス（WRDS経由）

```python
import wrds

db = wrds.Connection(wrds_username='your_username')

# M&A取引データ
query = """
SELECT 
    dealnum AS deal_id,
    da AS announcement_date,
    dt AS completion_date,
    an AS acquirer_name,
    tn AS target_name,
    ams AS acquirer_macro_industry,
    tms AS target_macro_industry,
    dv AS deal_value,
    pctacq AS percent_acquired,
    datype AS deal_attitude,
    paymeth AS payment_method
FROM 
    sdc.ma
WHERE 
    da BETWEEN '2010-01-01' AND '2023-12-31'
    AND ams = 'United States'  -- 米国買収者
    AND dv IS NOT NULL  -- 取引金額あり
ORDER BY 
    da
"""

df_ma = db.raw_sql(query)

print(f"M&A取引数: {len(df_ma):,}件")
print(f"総取引額: ${df_ma['deal_value'].sum()/1000:.1f}B")

db.close()
```

#### 研究用途

**M&A戦略研究**:
- 買収プレミアム決定要因
- M&A announcement効果
- Post-merger performance

---

### 1.5 BoardEx (取締役ネットワークデータ)

**提供元**: BoardEx (ISS)  
**カバレッジ**: グローバル企業の役員・取締役（2000年〜現在）

#### 主要データ

**取締役データ**:
- 取締役個人ID（Director ID）
- 氏名・経歴（Name & Background）
- 現職・過去職（Current & Past Positions）
- 学歴（Education）
- 他社取締役兼任（Board Interlocks）

#### アクセス

**WRDS経由**:
```python
import wrds

db = wrds.Connection(wrds_username='your_username')

# 取締役データ取得
query = """
SELECT 
    companyid AS company_id,
    companyname AS company_name,
    directorid AS director_id,
    directorname AS director_name,
    datestartrole AS start_date,
    dateendrole AS end_date,
    rolename AS position,
    seniority
FROM 
    boardex.na_wrds_company_profile
WHERE 
    datestartrole BETWEEN '2010-01-01' AND '2023-12-31'
ORDER BY 
    companyid, datestartrole
"""

df_board = db.raw_sql(query)

print(f"企業数: {df_board['company_id'].nunique():,}")
print(f"取締役数: {df_board['director_id'].nunique():,}")

db.close()
```

#### Board Interlock Network構築

```python
import pandas as pd
import networkx as nx

# 同じ取締役が複数企業に所属 = Board Interlock
director_companies = df_board.groupby('director_id')['company_id'].apply(list)

# ネットワーク構築
G = nx.Graph()

for director, companies in director_companies.items():
    if len(companies) > 1:
        # 同じ取締役を共有する企業間にエッジ
        for i in range(len(companies)):
            for j in range(i+1, len(companies)):
                G.add_edge(companies[i], companies[j])

print(f"ネットワークノード数（企業）: {G.number_of_nodes()}")
print(f"ネットワークエッジ数（Interlock）: {G.number_of_edges()}")

# Centrality計算
degree_centrality = nx.degree_centrality(G)
betweenness = nx.betweenness_centrality(G)
```

詳細: [`5-network-analysis` skill](../5-network-analysis/SKILL.md)

---

## 2. 欧州データソース

### 2.1 Orbis (Bureau van Dijk)

**提供元**: Moody's Analytics (Bureau van Dijk)  
**カバレッジ**: 世界400百万社以上（欧州が最も充実）

#### 主要データ

**財務データ**:
- 損益計算書
- 貸借対照表
- キャッシュフロー
- 財務比率

**非財務データ**:
- 企業概要・住所
- 業界分類（NACE, SIC）
- 所有権構造
- 子会社情報

#### 特徴

**長所**:
- ✅ 欧州企業の最も包括的なデータ
- ✅ 非上場企業も含む
- ✅ 所有権データが充実

**短所**:
- ❌ 高額（企業ライセンス必要）
- ❌ データ標準化がCompustatより劣る
- ❌ 歴史的データが限定的

#### アクセス方法

**Webインターフェース**（APIなし）:
1. Orbisポータルにログイン
2. 検索条件設定（国、業界、期間等）
3. CSVエクスポート

**推奨ワークフロー**:
```python
# 1. Orbisから手動エクスポート（CSV）
# 2. Pythonで読み込み・クリーニング

import pandas as pd

df_orbis = pd.read_csv('orbis_export.csv', encoding='latin-1')

# 変数名標準化
df_orbis = df_orbis.rename(columns={
    'Operating revenue\nEUR': 'sales',
    'Total assets\nEUR': 'total_assets',
    'P/L before tax\nEUR': 'pretax_income'
})

# 通貨換算（EURからUSD）
eur_usd_rate = 1.10  # 適切なレート使用
df_orbis['sales_usd'] = df_orbis['sales'] * eur_usd_rate
```

---

### 2.2 Amadeus (Bureau van Dijk)

**提供元**: Moody's Analytics  
**カバレッジ**: 欧州企業特化版Orbis（21百万社）

**Orbisとの違い**:
- 欧州に特化
- より詳細な欧州企業データ
- Orbisより安価（欧州研究のみの場合）

---

### 2.3 Datastream (Refinitiv)

**提供元**: Refinitiv (LSEG)  
**カバレッジ**: グローバル株価・財務データ（175カ国、2000年〜現在）

#### 主要データ

**株価データ**:
- 日次株価
- 取引量
- 市場時価総額

**財務データ**:
- P/L, B/S, C/F
- 財務比率

#### Pythonアクセス（Refinitiv Eikon API）

```python
import eikon as ek

# API Key設定
ek.set_app_key('YOUR_APP_KEY')

# 株価データ取得
df_price, err = ek.get_data(
    instruments=['AAPL.O', 'MSFT.O', 'GOOGL.O'],
    fields=['TR.PriceClose', 'TR.Volume'],
    parameters={'SDate': '2020-01-01', 'EDate': '2023-12-31'}
)

print(df_price)

# 財務データ取得
df_financials, err = ek.get_data(
    instruments=['AAPL.O'],
    fields=['TR.Revenue', 'TR.NetIncome', 'TR.TotalAssets'],
    parameters={'Period': 'FY0', 'SDate': '2010', 'EDate': '2023'}
)
```

---

## 3. 日本データソース

### 3.1 EDINET (金融庁 有価証券報告書)

**提供元**: 金融庁  
**カバレッジ**: 日本上場企業（2008年〜現在、一部2004年〜）  
**企業数**: 約4,000社（上場企業）

#### 主要データ

**有価証券報告書**:
- 企業概況
- 事業の状況
- 設備の状況
- 提出会社の状況
- 経理の状況（財務諸表）
- 株式の状況

#### API実装（完全版）

```python
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

class EDINETCollector:
    """EDINET APIから有価証券報告書データを収集"""
    
    def __init__(self):
        self.base_url = "https://disclosure.edinet-fsa.go.jp/api/v1"
        
    def get_document_list(self, date):
        """指定日の提出書類一覧を取得
        
        Args:
            date: 'YYYY-MM-DD'形式
        """
        url = f"{self.base_url}/documents.json"
        params = {'date': date, 'type': 2}  # type=2: メタデータのみ
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
    
    def get_financials(self, start_date, end_date, doc_type='120'):
        """期間内の有価証券報告書を収集
        
        Args:
            start_date: 'YYYY-MM-DD'
            end_date: 'YYYY-MM-DD'
            doc_type: '120'=有価証券報告書
        """
        date_range = pd.date_range(start_date, end_date, freq='D')
        
        all_docs = []
        
        for date in date_range:
            date_str = date.strftime('%Y-%m-%d')
            print(f"取得中: {date_str}")
            
            data = self.get_document_list(date_str)
            
            if data and 'results' in data:
                for doc in data['results']:
                    if doc['docTypeCode'] == doc_type:
                        all_docs.append({
                            'edinetCode': doc['edinetCode'],
                            'secCode': doc.get('secCode'),
                            'filerName': doc['filerName'],
                            'docID': doc['docID'],
                            'submitDateTime': doc['submitDateTime'],
                            'periodStart': doc.get('periodStart'),
                            'periodEnd': doc.get('periodEnd')
                        })
            
            time.sleep(0.5)  # API負荷軽減
        
        return pd.DataFrame(all_docs)

# 使用例
collector = EDINETCollector()

# 2023年の有価証券報告書一覧取得
df_edinet = collector.get_financials('2023-01-01', '2023-12-31')

print(f"取得書類数: {len(df_edinet)}")
print(f"企業数: {df_edinet['edinetCode'].nunique()}")

# 上場企業のみ（証券コードあり）
df_listed = df_edinet[df_edinet['secCode'].notna()]
print(f"上場企業数: {df_listed['secCode'].nunique()}")
```

#### XBRL財務データ抽出

```python
import requests
import zipfile
import io
from lxml import etree

def download_xbrl(doc_id):
    """XBRLファイルダウンロード"""
    url = f"https://disclosure.edinet-fsa.go.jp/api/v1/documents/{doc_id}"
    params = {'type': 1}  # type=1: 提出本文書及び監査報告書
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        # ZIPファイル展開
        zip_file = zipfile.ZipFile(io.BytesIO(response.content))
        return zip_file
    return None

def extract_financials_from_xbrl(zip_file):
    """XBRLから財務データ抽出"""
    # XBRLパース（簡略版）
    xbrl_files = [f for f in zip_file.namelist() if f.endswith('.xbrl')]
    
    if xbrl_files:
        with zip_file.open(xbrl_files[0]) as f:
            tree = etree.parse(f)
            root = tree.getroot()
            
            # 名前空間
            ns = {'xbrli': 'http://www.xbrl.org/2003/instance',
                  'jpcrp': 'http://disclosure.edinet-fsa.go.jp/taxonomy/jpcrp/2023-11-01'}
            
            # 総資産の抽出例
            total_assets = root.find('.//jpcrp:Assets', ns)
            if total_assets is not None:
                return {'total_assets': total_assets.text}
    
    return {}

# 使用例
doc_id = df_edinet.iloc[0]['docID']
zip_file = download_xbrl(doc_id)
if zip_file:
    financials = extract_financials_from_xbrl(zip_file)
    print(financials)
```

**注意**: XBRL解析は複雑。実用にはライブラリ（arelle等）推奨。

---

### 3.2 JPX (日本取引所グループ - 株価データ)

**提供元**: 日本取引所グループ  
**カバレッジ**: 東証上場企業（1949年〜現在）

#### データ取得方法

**Option 1: 公式サイトから手動ダウンロード**
- 日次株価: https://www.jpx.co.jp/markets/statistics-equities/misc/01.html

**Option 2: Yahoo Finance Japan API（非公式）**
```python
import pandas as pd
import yfinance as yf

# トヨタ自動車（7203.T）の株価取得
ticker = yf.Ticker("7203.T")

# 日次株価
df_price = ticker.history(start="2020-01-01", end="2023-12-31")

print(df_price.head())
print(f"取得期間: {df_price.index[0]} ~ {df_price.index[-1]}")

# 財務データ
financials = ticker.financials
balance_sheet = ticker.balance_sheet
cashflow = ticker.cashflow

print("総資産:", balance_sheet.loc['Total Assets'].iloc[0])
```

**Option 3: Nikkei NEEDS（有料）**
- 最も包括的な日本株価データ
- 大学・研究機関向けライセンス

---

### 3.3 e-Stat (政府統計ポータル)

**提供元**: 総務省統計局  
**カバレッジ**: 日本の官公庁統計（無料）

#### 主要統計

- 経済センサス
- 工業統計
- 商業統計
- GDP統計
- 人口統計

#### API実装

```python
import requests
import pandas as pd

class EStatAPI:
    """e-Stat APIクライアント"""
    
    def __init__(self, app_id):
        """
        Args:
            app_id: e-Stat API利用登録で取得（無料）
        """
        self.base_url = "https://api.e-stat.go.jp/rest/3.0/app/json"
        self.app_id = app_id
    
    def get_stats_list(self, search_word):
        """統計表検索"""
        url = f"{self.base_url}/getStatsList"
        params = {
            'appId': self.app_id,
            'searchWord': search_word,
            'limit': 100
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return None
    
    def get_stats_data(self, stats_data_id):
        """統計データ取得"""
        url = f"{self.base_url}/getStatsData"
        params = {
            'appId': self.app_id,
            'statsDataId': stats_data_id,
            'metaGetFlg': 'Y'
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            # データフレーム変換
            return self._parse_stats_data(data)
        return None
    
    def _parse_stats_data(self, data):
        """統計データをDataFrameに変換"""
        # 簡略化版（実際はより複雑）
        values = data['GET_STATS_DATA']['STATISTICAL_DATA']['DATA_INF']['VALUE']
        
        df = pd.DataFrame(values)
        return df

# 使用例
api = EStatAPI(app_id='YOUR_APP_ID')  # e-Statサイトで登録

# GDP統計検索
results = api.get_stats_list('GDP')
print(f"検索結果: {len(results)}件")

# 統計データ取得（例: 統計表ID）
df_gdp = api.get_stats_data(stats_data_id='0003410379')
```

---

### 3.4 NEEDS (日本経済新聞社)

**提供元**: 日本経済新聞社  
**カバレッジ**: 日本企業（1970年代〜現在）

#### 主要データ

**財務データ**:
- 有価証券報告書ベース
- 連結・単体財務諸表
- セグメント情報

**株価データ**:
- 日次・週次・月次
- 調整後価格
- 株式分割考慮

**企業情報**:
- 企業概要
- 役員情報
- 株主構成

#### アクセス

**大学契約が必要**（WRDS的な位置づけ）

```python
# NEEDS-Financial QUESTからのデータ取得例（概念）
# 実際のAPIは契約先による

import pandas as pd

# NEEDSデータ読み込み（通常はCSVエクスポート）
df_needs = pd.read_csv('needs_export.csv', encoding='shift-jis')

# 変数名標準化
df_needs = df_needs.rename(columns={
    '証券コード': 'sec_code',
    '会社名': 'company_name',
    '決算期': 'fiscal_year',
    '売上高': 'sales',
    '総資産': 'total_assets',
    '純利益': 'net_income'
})
```

---

## 4. 韓国データソース

### 4.1 DART (韓国金融監督院 電子公示システム)

**提供元**: 韓国金融監督院 (FSS)  
**カバレッジ**: 韓国上場企業（2000年〜現在）  
**企業数**: 約2,500社

#### 主要データ

**事業報告書**:
- 財務諸表
- 監査報告書
- 重要事項報告

#### API実装（Open DART API）

```python
import requests
import pandas as pd

class DARTCollector:
    """韓国 DART API クライアント"""
    
    def __init__(self, api_key):
        """
        Args:
            api_key: DART API Key（無料登録）
                    https://opendart.fss.or.kr/
        """
        self.base_url = "https://opendart.fss.or.kr/api"
        self.api_key = api_key
    
    def get_corp_list(self):
        """企業リスト取得"""
        url = f"{self.base_url}/corpCode.xml"
        params = {'crtfc_key': self.api_key}
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            # XMLパース（簡略化）
            return response.content
        return None
    
    def get_financial_statements(self, corp_code, bsns_year, reprt_code='11011'):
        """財務諸表取得
        
        Args:
            corp_code: 企業コード
            bsns_year: 사업연도 (YYYY)
            reprt_code: '11011'=사업보고서(年次)
        """
        url = f"{self.base_url}/fnlttSinglAcntAll.json"
        params = {
            'crtfc_key': self.api_key,
            'corp_code': corp_code,
            'bsns_year': bsns_year,
            'reprt_code': reprt_code,
            'fs_div': 'CFS'  # 連結財務諸表
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data['status'] == '000':
                return pd.DataFrame(data['list'])
        return None

# 使用例
dart = DARTCollector(api_key='YOUR_API_KEY')

# サムスン電子（例: corp_code='00126380'）の財務諸表
df_samsung = dart.get_financial_statements(
    corp_code='00126380',
    bsns_year='2023'
)

if df_samsung is not None:
    print("財務データ取得成功:")
    print(df_samsung[['account_nm', 'thstrm_amount']].head(10))
```

---

### 4.2 KRX (韓国取引所 - 株価データ)

**提供元**: 韓国取引所  
**カバレッジ**: KOSPI, KOSDAQ上場企業

#### データ取得

**Option 1: KRX公式サイト**
- http://data.krx.co.kr/

**Option 2: pykrx ライブラリ（非公式）**
```python
from pykrx import stock
import pandas as pd

# サムスン電子（005930）の株価
df_price = stock.get_market_ohlcv_by_date(
    fromdate="20200101", 
    todate="20231231", 
    ticker="005930"
)

print(df_price.head())

# 全KOSPI銘柄リスト
tickers = stock.get_market_ticker_list("20231231", market="KOSPI")
print(f"KOSPI上場企業数: {len(tickers)}")

# 時価総額
market_cap = stock.get_market_cap_by_ticker("20231231", market="KOSPI")
print(market_cap.head())
```

---

## 5. 中国データソース

### 5.1 CNINFO (巨潮資訊網)

**提供元**: 深圳証券取引所  
**カバレッジ**: 上海・深圳上場企業（1990年代〜現在）

#### データ取得

**公式サイト**: http://www.cninfo.com.cn/

**Python実装（スクレイピング）**:
```python
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_cninfo_announcement_list(stock_code, start_date, end_date):
    """CNINFOから公告リスト取得
    
    Args:
        stock_code: 股票代码 (例: '000001'=平安銀行)
        start_date: 'YYYY-MM-DD'
        end_date: 'YYYY-MM-DD'
    """
    url = "http://www.cninfo.com.cn/new/disclosure/stock"
    params = {
        'stockCode': stock_code,
        'plate': '',  # 板块
        'category': '',  # 类别
        'pageNum': 1,
        'pageSize': 30
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json'
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data['announcements'])
    return None

# 使用例
df_announcements = get_cninfo_announcement_list(
    stock_code='000001',
    start_date='2023-01-01',
    end_date='2023-12-31'
)

if df_announcements is not None:
    print(f"公告件数: {len(df_announcements)}")
```

**注意**: CNINFOの公式APIは限定的。スクレイピングはレート制限・規約に注意。

---

### 5.2 Tushare (Python Financial Data Interface)

**提供元**: Tushare.pro (民間)  
**カバレッジ**: 中国A株・香港株（1990年〜現在）

#### API実装

```python
import tushare as ts

# API Token設定（登録必要: https://tushare.pro/）
ts.set_token('YOUR_TOKEN')
pro = ts.pro_api()

# 上場企業リスト
df_stock_basic = pro.stock_basic(
    exchange='',
    list_status='L',
    fields='ts_code,symbol,name,area,industry,list_date'
)

print(f"上場企業数: {len(df_stock_basic)}")

# 平安銀行（000001.SZ）の日次株価
df_daily = pro.daily(
    ts_code='000001.SZ',
    start_date='20200101',
    end_date='20231231'
)

print(df_daily.head())

# 財務指標
df_fina_indicator = pro.fina_indicator(
    ts_code='000001.SZ',
    start_date='20200101',
    end_date='20231231'
)

print("財務指標:")
print(df_fina_indicator[['end_date', 'roe', 'roa', 'debt_to_assets']].head())
```

#### 長所・短所

**長所**:
- ✅ Pythonネイティブ
- ✅ APIが充実
- ✅ 無料プラン�り

**短所**:
- ❌ レート制限（有料プランで緩和）
- ❌ 英語ドキュメント限定的

---

### 5.3 AKShare (Another Knowledge Share)

**提供元**: オープンソース  
**カバレッジ**: 中国・グローバル財務データ

```python
import akshare as ak

# A株リスト
stock_info_a_code_name_df = ak.stock_info_a_code_name()
print(f"A株数: {len(stock_info_a_code_name_df)}")

# 平安銀行の株価
stock_zh_a_hist_df = ak.stock_zh_a_hist(
    symbol="000001",
    period="daily",
    start_date="20200101",
    end_date="20231231",
    adjust=""
)

print(stock_zh_a_hist_df.head())

# 財務諸表
stock_financial_report_sina_df = ak.stock_financial_report_sina(
    stock="000001",
    symbol="资产负债表"
)

print("資産負債表:")
print(stock_financial_report_sina_df)
```

---

## 6. ASEAN諸国

### 6.1 シンガポール

**SGX (Singapore Exchange)**
- 公式サイト: https://www.sgx.com/
- 上場企業数: 約700社
- データ取得: Yahoo Finance, Bloomberg

```python
import yfinance as yf

# DBS銀行（シンガポール最大手）
dbs = yf.Ticker("D05.SI")
df_dbs = dbs.history(start="2020-01-01", end="2023-12-31")
```

---

### 6.2 タイ

**SET (Stock Exchange of Thailand)**
- 公式サイト: https://www.set.or.th/
- 上場企業数: 約800社
- API: SET Market Data API（有料）

---

### 6.3 マレーシア

**Bursa Malaysia**
- 公式サイト: https://www.bursamalaysia.com/
- 上場企業数: 約900社

---

### 6.4 インドネシア

**IDX (Indonesia Stock Exchange)**
- 公式サイト: https://www.idx.co.id/
- 上場企業数: 約800社

---

### 6.5 ベトナム

**HOSE (Ho Chi Minh Stock Exchange)**
- 公式サイト: https://www.hsx.vn/
- 上場企業数: 約400社

---

### 6.6 フィリピン

**PSE (Philippine Stock Exchange)**
- 公式サイト: https://www.pse.com.ph/
- 上場企業数: 約270社

---

## 7. インド

### 7.1 BSE (Bombay Stock Exchange)

**カバレッジ**: 約5,000社

```python
import yfinance as yf

# Reliance Industries（インド最大手）
reliance = yf.Ticker("RELIANCE.BO")  # .BO = BSE
df_reliance = reliance.history(start="2020-01-01")
```

---

### 7.2 NSE (National Stock Exchange)

**カバレッジ**: 約2,000社

```python
# Reliance Industries（NSE）
reliance_nse = yf.Ticker("RELIANCE.NS")  # .NS = NSE
```

---

## 8. グローバル無料ソース

### 8.1 World Bank Open Data

**提供元**: 世界銀行  
**カバレッジ**: 世界各国のマクロ経済データ

```python
import wbdata
import pandas as pd

# GDP per capita取得
gdp_indicator = {'NY.GDP.PCAP.CD': 'gdp_per_capita'}

df_gdp = wbdata.get_dataframe(
    gdp_indicator,
    country=['USA', 'CHN', 'JPN', 'DEU'],
    convert_date=True
)

print(df_gdp)

# 全指標リスト
indicators = wbdata.get_indicator(source=2)
print(f"利用可能指標数: {len(indicators)}")
```

---

### 8.2 IMF Data

**提供元**: 国際通貨基金  
**カバレッジ**: 世界経済見通し、金融データ

```python
import requests
import pandas as pd

# IMF API
url = "http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/IFS/A.US.NGDP_R_K_IX"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    # JSONパース（複雑）
    print("IMFデータ取得成功")
```

---

### 8.3 OECD.Stat

**提供元**: 経済協力開発機構  
**カバレッジ**: OECD加盟国統計

```python
import pandas as pd

# OECD API
url = "https://stats.oecd.org/SDMX-JSON/data/QNA/JPN+USA+DEU.B1_GE.GPSA.Q/all"

response = requests.get(url, params={'startTime': '2010-Q1', 'endTime': '2023-Q4'})

if response.status_code == 200:
    data = response.json()
    # パース...
```

---

### 8.4 SEC EDGAR (米国企業開示)

**提供元**: 米国証券取引委員会  
**カバレッジ**: 米国上場企業の全開示書類

詳細: [`4-text-analysis` skill](../4-text-analysis/SKILL.md) - SEC EDGARセクション

---

### 8.5 Yahoo Finance

**カバレッジ**: グローバル株価データ

```python
import yfinance as yf

# 複数銘柄一括取得
tickers = ['AAPL', 'MSFT', 'GOOGL', '7203.T', '005930.KS']
df = yf.download(tickers, start='2020-01-01', end='2023-12-31')

print(df['Close'].head())
```

---

## 9. データソース選択マトリックス

### 9.1 地域×変数タイプ

| 地域/国 | 財務データ | 株価データ | ガバナンス | M&A | ESG | 無料? |
|---------|-----------|-----------|-----------|-----|-----|-------|
| **北米** | Compustat | CRSP | ExecuComp, BoardEx | SDC | MSCI, CDP | ❌ |
| **欧州** | Orbis, Datastream | Datastream | BoardEx | Zephyr | Refinitiv | ❌ |
| **日本** | EDINET, NEEDS | JPX, Yahoo | EDINET | RECOF | - | ✅/❌ |
| **韓国** | DART | KRX | DART | - | - | ✅ |
| **中国** | Tushare, AKShare | Tushare | CNINFO | - | - | ✅ |
| **ASEAN** | 各国取引所 | Yahoo Finance | - | - | - | 部分的 |
| **グローバル** | World Bank | Yahoo Finance | - | - | CDP | ✅ |

---

### 9.2 研究テーマ別推奨ソース

**イノベーション研究（R&D→パフォーマンス）**:
```
米国: Compustat (R&D) + CRSP (株価)
日本: EDINET (R&D) + JPX (株価)
欧州: Orbis (R&D) + Datastream (株価)
```

**ガバナンス研究（Board構成→戦略）**:
```
米国: ExecuComp + BoardEx + Compustat
日本: EDINET (役員情報) + NEEDS
欧州: BoardEx + Orbis
```

**M&A研究**:
```
グローバル: SDC Platinum (Thomson Reuters)
日本: RECOF M&Aデータベース
```

**ESG研究**:
```
グローバル: MSCI ESG, Refinitiv ESG, CDP
無料: CDP Climate Change, EPA TRI

詳細: 7-esg-sustainability skill
```

---

## 10. API実装パターン

### 10.1 レート制限対策

```python
import time
import requests
from functools import wraps

def rate_limited(max_per_second=1):
    """レート制限デコレータ"""
    min_interval = 1.0 / max_per_second
    
    def decorator(func):
        last_called = [0.0]
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        
        return wrapper
    return decorator

# 使用例
@rate_limited(max_per_second=2)  # 1秒に2リクエストまで
def fetch_data(url):
    return requests.get(url)
```

---

### 10.2 エラーハンドリング

```python
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def create_robust_session():
    """リトライ機能付きセッション"""
    session = requests.Session()
    
    retry = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504]
    )
    
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    return session

# 使用例
session = create_robust_session()
response = session.get('https://api.example.com/data')
```

---

### 10.3 認証パターン

**Basic Auth**:
```python
import requests

response = requests.get(
    'https://api.example.com/data',
    auth=('username', 'password')
)
```

**API Key（Header）**:
```python
headers = {'Authorization': f'Bearer {api_key}'}
response = requests.get(url, headers=headers)
```

**OAuth 2.0**:
```python
from requests_oauthlib import OAuth2Session

client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'

oauth = OAuth2Session(client_id)
token = oauth.fetch_token(
    'https://api.example.com/oauth/token',
    client_secret=client_secret
)

response = oauth.get('https://api.example.com/data')
```

---

## 11. データ品質比較

### 11.1 信頼性ランキング

| データソース | 信頼性 | カバレッジ | 更新頻度 | 学術使用実績 |
|------------|--------|----------|---------|-------------|
| Compustat | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 四半期 | ⭐⭐⭐⭐⭐ |
| CRSP | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 日次 | ⭐⭐⭐⭐⭐ |
| Orbis | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 年次 | ⭐⭐⭐⭐ |
| EDINET | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 即時 | ⭐⭐⭐⭐ |
| DART | ⭐⭐⭐⭐ | ⭐⭐⭐ | 即時 | ⭐⭐⭐ |
| Tushare | ⭐⭐⭐ | ⭐⭐⭐⭐ | 日次 | ⭐⭐⭐ |
| Yahoo Finance | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 日次 | ⭐⭐ |

---

## 12. コスト比較

### 12.1 費用レベル

**無料**:
- ✅ EDINET (日本)
- ✅ DART (韓国)
- ✅ Tushare (中国、基本プラン)
- ✅ World Bank Open Data
- ✅ IMF Data
- ✅ OECD.Stat
- ✅ SEC EDGAR (米国)
- ✅ Yahoo Finance

**大学契約（学生は実質無料）**:
- 🟡 WRDS (Compustat, CRSP含む): $2,000-5,000/年
- 🟡 NEEDS (日本): 大学による
- 🟡 BoardEx: WRDS経由

**高額**:
- 🔴 Bloomberg Terminal: $24,000/年
- 🔴 Refinitiv Eikon: $20,000/年
- 🔴 Orbis: €数千〜数万/年
- 🔴 SDC Platinum: $数千/年

---

## 📊 Quick Reference

### 初心者向け推奨開始点

**米国企業研究**:
1. WRDS契約確認（大学）
2. Compustat + CRSP
3. 代替: Yahoo Finance（無料）

**日本企業研究**:
1. EDINET API（無料）
2. Yahoo Finance Japan
3. 予算あり: NEEDS

**中国企業研究**:
1. Tushare（無料プラン）
2. AKShare（オープンソース）

**グローバル比較研究**:
1. World Bank Open Data
2. Yahoo Finance
3. Orbis（予算あり）

---

### Pythonパッケージ

```bash
# 必須
pip install pandas numpy requests

# データソース別
pip install wrds  # WRDS用
pip install yfinance  # Yahoo Finance
pip install wbdata  # World Bank
pip install tushare  # 中国
pip install akshare  # 中国
pip install pykrx  # 韓国

# ユーティリティ
pip install beautifulsoup4 lxml  # スクレイピング
pip install openpyxl xlrd  # Excel読み込み
```

---

## 参考文献

- Fama, E. F., & French, K. R. (2015). A five-factor asset pricing model. *Journal of Financial Economics*, 116(1), 1-22.
  - Compustat & CRSP使用例

- Fan, J. P., Wong, T. J., & Zhang, T. (2007). Politically connected CEOs, corporate governance, and Post-IPO performance of China's newly partially privatized firms. *Journal of Financial Economics*, 84(2), 330-357.
  - 中国データ使用例

---

## 次のステップ

### データ収集後
→ [`1-core-workflow` skill](../1-core-workflow/SKILL.md) Phase 4 (Dataset Construction)

### テキストデータ分析
→ [`4-text-analysis` skill](../4-text-analysis/SKILL.md)

### 自動収集パイプライン
→ [`8-automation` skill](../8-automation/SKILL.md)

---

**このスキルで、世界中のデータソースにアクセスし、研究データを収集できます。**  
**RQに最適なソースを選択し、効率的にデータを構築しましょう。**

---

**最終更新**: 2025-11-01  
**バージョン**: 4.0.0  
**次回メンテナンス予定**: 2025-12-01
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
