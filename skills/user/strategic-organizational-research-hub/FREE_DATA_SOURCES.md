# 無料データソース完全ガイド

**予算ゼロで戦略・組織研究を実現するための実践的データソースカタログ**

---

## 📌 このガイドの使い方

### 対象ユーザー
- 大学のデータベース契約がない研究者
- 独立研究者、フリーランス研究者
- 予算が限られた修士・博士課程学生
- 新興国の研究者

### 到達目標
このガイドを使えば、以下がすべて**無料**で実現できます：

✅ 企業レベルの財務データ収集（米国・日本）  
✅ 特許データによるイノベーション測定  
✅ ESG・サステナビリティデータ  
✅ マクロ経済・産業レベルデータ  
✅ トップジャーナル（SMJ、AMJ）掲載水準の研究

---

## 🌍 地域別データソースマップ

### 北米（アメリカ・カナダ）

#### 1. SEC EDGAR（米国証券取引委員会）
- **URL**: https://www.sec.gov/edgar
- **登録**: 不要
- **カバレッジ**: 米国上場企業約7,000社、1994年～現在
- **更新頻度**: リアルタイム（提出から数時間）

**入手可能データ**:
| データ種類 | フォーム | 内容 |
|----------|---------|------|
| 年次財務諸表 | 10-K | 貸借対照表、損益計算書、キャッシュフロー、セグメント情報 |
| 四半期財務諸表 | 10-Q | 四半期財務データ |
| 臨時報告 | 8-K | M&A、CEO交代、重要イベント |
| 株主総会資料 | DEF 14A | 取締役会情報、役員報酬、株主提案 |
| 大株主報告 | 13D/13G | 5%以上保有する大株主情報 |
| インサイダー取引 | Form 4 | 役員・取締役の株式売買 |

**データ取得方法**:

**方法1: Webインターフェース（初心者向け）**
1. https://www.sec.gov/edgar/searchedgar/companysearch.html にアクセス
2. 企業名またはティッカーシンボールで検索（例："Apple" or "AAPL"）
3. 目的のフォーム（10-K、DEF 14Aなど）を選択
4. PDFまたはHTMLでダウンロード

**方法2: 一括ダウンロード（上級者向け）**
```python
# SEC EDGARクローラーの例
import requests
from bs4 import BeautifulSoup
import time

def get_10k_url(ticker, year):
    """
    指定企業の10-Kファイルへの直接リンクを取得
    """
    # CIKコード取得
    cik_lookup_url = "https://www.sec.gov/cgi-bin/browse-edgar"
    params = {
        'action': 'getcompany',
        'ticker': ticker,
        'type': '10-K',
        'dateb': f'{year}1231',
        'count': '1',
        'output': 'xml'
    }
    
    headers = {
        'User-Agent': 'YourUniversity Research yourname@university.edu'
    }
    
    response = requests.get(cik_lookup_url, params=params, headers=headers)
    
    # レスポンスを解析して10-KのURLを抽出
    # （実際にはXMLパーサーを使用）
    time.sleep(0.1)  # レート制限遵守（1秒に10リクエスト以下）
    return response

# 使用例
# url = get_10k_url('AAPL', 2023)
```

**重要な注意事項**:
- **User-Agent必須**: リクエスト時に所属機関とメールアドレスを含むUser-Agentヘッダーを設定
- **レート制限**: 1秒に10リクエスト以下に抑える
- **robots.txt遵守**: https://www.sec.gov/robots.txt を確認

**研究活用例**:
- **財務パフォーマンス**: 10-Kから総資産、売上高、純利益を抽出 → ROA、ROE計算
- **セグメント分析**: 10-Kの「Segment Information」から事業多角化度を測定
- **ガバナンス研究**: DEF 14Aから取締役会構成（独立取締役比率、女性取締役比率）を抽出
- **イベントスタディ**: 8-Kから重要イベント日を特定 → 株価への影響を分析

#### 2. Yahoo Finance（市場データ）
- **URL**: https://finance.yahoo.com
- **登録**: 不要
- **カバレッジ**: 世界中の主要市場、過去20年以上

**入手可能データ**:
- 日次・週次・月次株価（始値、高値、安値、終値、出来高）
- 調整済み終値（株式分割・配当考慮）
- 基本的な財務指標（時価総額、PER、配当利回り）
- ESG Risk Ratings（Sustainalyticsデータ、無料版は簡易）

**データ取得方法**:

**方法1: CSVダウンロード**
1. 企業ページに移動（例：https://finance.yahoo.com/quote/AAPL/）
2. 「Historical Data」タブをクリック
3. 期間を設定（例：2020-01-01 to 2023-12-31）
4. 「Download」ボタンでCSV取得

**方法2: Python API（`yfinance`）**
```python
import yfinance as yf
import pandas as pd

# 単一銘柄のデータ取得
ticker = yf.Ticker("AAPL")
hist = ticker.history(start="2020-01-01", end="2023-12-31")

# 基本情報
info = ticker.info
print(f"時価総額: ${info['marketCap']:,}")
print(f"従業員数: {info.get('fullTimeEmployees', 'N/A'):,}")

# 複数銘柄の一括取得
tickers = ["AAPL", "MSFT", "GOOGL"]
data = yf.download(tickers, start="2020-01-01", end="2023-12-31")

# 日次リターン計算
returns = data['Adj Close'].pct_change()
```

**研究活用例**:
- **イベントスタディ**: 異常リターンの計算（実際のリターン - 期待リターン）
- **市場リスク**: ベータ係数の推定（個別株とS&P500の回帰）
- **ボラティリティ**: 株価の標準偏差を計算 → リスク指標

---

### 日本

#### 3. EDINET（金融商品取引法に基づく有価証券報告書等の開示システム）
- **URL**: https://disclosure2.edinet-fsa.go.jp/
- **登録**: 不要
- **カバレッジ**: 日本の上場企業約3,800社、1961年～現在（電子化は2000年代）

**入手可能データ**:
| 書類種類 | 内容 |
|---------|------|
| 有価証券報告書 | 年次財務諸表、セグメント情報、従業員数、研究開発費 |
| 四半期報告書 | 四半期財務データ |
| 臨時報告書 | 重要事実（M&A、組織再編、災害損失等） |
| 大量保有報告書 | 5%以上の株式保有者情報 |

**データ取得方法**:

**方法1: Webインターフェース**
1. https://disclosure2.edinet-fsa.go.jp/ にアクセス
2. 「書類検索」→「会社名」で検索
3. 有価証券報告書を選択
4. HTML版またはPDF版をダウンロード

**方法2: EDINET API（JSON）**
```python
import requests
import pandas as pd

def get_edinet_documents(date):
    """
    指定日に提出された書類リストを取得
    
    Args:
        date: YYYY-MM-DD形式（例："2024-06-28"）
    """
    url = "https://disclosure2.edinet-fsa.go.jp/api/v2/documents.json"
    params = {
        "date": date,
        "type": 2  # 2=有価証券報告書、3=四半期報告書
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        documents = data.get("results", [])
        return pd.DataFrame(documents)
    return pd.DataFrame()

# 2024年6月28日提出書類を取得
docs = get_edinet_documents("2024-06-28")
print(f"取得書類数: {len(docs)}")
print(docs[['edinetCode', 'filerName', 'docDescription']].head())
```

**XBRLデータの解析**（上級）:
```python
# EDINETから財務データ（XBRL）を取得
def download_xbrl(doc_id):
    """
    書類IDからXBRLファイルをダウンロード
    """
    url = f"https://disclosure2.edinet-fsa.go.jp/api/v2/documents/{doc_id}"
    params = {"type": 1}  # 1=提出本文書及び監査報告書
    
    response = requests.get(url, params=params)
    
    # ZIPファイルとして保存・解凍
    with open(f"{doc_id}.zip", "wb") as f:
        f.write(response.content)
    
    # XBRL解析（arelle、xbrlなどのライブラリを使用）
    # ※複雑なため、財務諸表抽出には専用ツールが推奨
```

**財務データ抽出の現実的な方法**:
1. **手動入力**（10-20社程度ならこれが最速）:
   - 有価証券報告書PDF → Excelに手入力
   - 主要指標：総資産、売上高、純利益、従業員数、研究開発費
   
2. **IRサイトからの決算短信利用**:
   - 各社のIR情報ページ → 決算短信PDFをダウンロード
   - 財務サマリーが見やすい形式で掲載

3. **外部ツール**:
   - **Japan Corporate Number公表サイト**（法人番号検索）: https://www.houjin-bangou.nta.go.jp/
   - 基本情報（本店所在地、設立年月日、資本金等）を無料取得可能

**研究活用例**:
- **日本企業のR&D投資**: 有価証券報告書「研究開発費」セクションから抽出
- **取締役会構成**: 有価証券報告書「役員の状況」から女性取締役比率を計算
- **セグメント多角化**: 有価証券報告書「セグメント情報」から事業多角化度を測定

---

### 欧州

#### 4. Companies House（英国企業登記所）
- **URL**: https://www.gov.uk/government/organisations/companies-house
- **登録**: 無料アカウント作成（API利用時）
- **カバレッジ**: 英国企業500万社以上

**入手可能データ**:
- 会社の基本情報（設立年、住所、業種）
- 年次会計報告書（Accounts）
- 取締役情報（Directors）
- 株主情報（Shareholders）

**データ取得**:
- **Web検索**: 会社名で検索 → PDFダウンロード
- **Bulk Data Product**: 全企業データのスナップショット（月次更新、£数千の有料）
- **API**: https://developer.company-information.service.gov.uk/

---

### グローバル

#### 5. OpenCorporates（世界最大の企業データベース）
- **URL**: https://opencorporates.com
- **登録**: 不要（基本検索）、API利用は有料
- **カバレッジ**: 200M+企業、140以上の管轄区域

**無料版の制限**:
- Web検索は無料
- 1日500リクエストまでのAPI無料枠あり

**入手可能データ**:
- 企業名、登記番号、設立国
- 住所、ステータス（活動中/解散）
- 取締役情報（一部の国）

**使用例**:
```python
# OpenCorporates API（無料枠）
import requests

def search_company(name, jurisdiction="us"):
    url = "https://api.opencorporates.com/v0.4/companies/search"
    params = {
        "q": name,
        "jurisdiction_code": jurisdiction
    }
    response = requests.get(url, params=params)
    return response.json()

results = search_company("Apple")
```

---

## 📊 専門データソース

### 特許・イノベーション

#### 6. USPTO PatentsView（米国特許商標庁）
- **URL**: https://patentsview.org/
- **登録**: 不要
- **カバレッジ**: 米国特許1,000万件以上（1976年～）

**データ内容**:
- 特許番号、出願日、付与日
- 特許タイトル、要約
- 発明者、譲受人（企業・組織）
- 引用情報（forward citations, backward citations）
- 技術分類（CPC、IPC）

**データ取得**:

**方法1: Bulk Download**
- https://patentsview.org/download/data-download-tables
- CSV形式で全データダウンロード可能（数GB）
- テーブル: patents, applications, assignees, citations, cpc_current

**方法2: API**
```python
import requests

def get_patents_by_assignee(company_name):
    """
    企業名で特許を検索
    """
    url = "https://api.patentsview.org/patents/query"
    query = {
        "q": {"assignee_organization": company_name},
        "f": ["patent_number", "patent_title", "patent_date", 
              "cited_patent_count"],
        "o": {"per_page": 10000}
    }
    
    response = requests.post(url, json=query)
    if response.status_code == 200:
        data = response.json()
        return data.get("patents", [])
    return []

# 使用例
apple_patents = get_patents_by_assignee("Apple Inc")
print(f"Apple特許数: {len(apple_patents)}")
```

**研究活用**:
- **イノベーション出力**: 特許件数、引用加重特許件数
- **技術多様性**: CPCセクション（A-H）の分散度
- **知識フロー**: 特許引用ネットワーク分析

**企業名マッチングの注意**:
- 企業名の表記揺れ対応（"Apple Inc" vs "Apple Computer"）
- 子会社・事業部門の統合
- **NBER Patent-Compustat Link**（2006年まで）を参照

#### 7. Google Patents
- **URL**: https://patents.google.com
- **カバレッジ**: 世界中の特許（USPTO、EPO、WIPOなど）

**利点**:
- UIが使いやすい
- 全文検索が強力
- 特許ファミリー（同一発明の各国出願）の可視化

**使い方**:
1. キーワードまたは企業名で検索
2. フィルタ（出願日、譲受人、CPC分類）を適用
3. CSVエクスポート（検索結果1,000件まで）

#### 8. WIPO PatentScope（世界知的所有権機関）
- **URL**: https://patentscope.wipo.int/
- **カバレッジ**: PCTの国際出願、一部の国内特許

**利点**:
- グローバル特許検索
- 多言語対応（英語、日本語、中国語等）

---

### ESG・サステナビリティ

#### 9. CDP（Carbon Disclosure Project）- 研究者ライセンス
- **URL**: https://www.cdp.net/en/academic-research
- **登録**: 研究目的での申請（大学メールアドレス必要）
- **カバレッジ**: 13,000社以上の気候変動データ

**データ内容**:
- Scope 1, 2, 3 温室効果ガス排出量
- 気候変動リスクと機会
- 削減目標とイニシアチブ
- 水資源管理、森林管理データ

**申請手順**:
1. https://www.cdp.net/en/academic-research にアクセス
2. 「Request Data」をクリック
3. 研究計画書を提出（1-2ページ）
4. 承認されれば無料でデータセット取得

**研究活用**:
- **ESGパフォーマンス**: カーボン排出量と財務パフォーマンスの関係
- **気候戦略**: 削減目標の野心度と企業価値
- **産業比較**: セクター別の排出量原単位

#### 10. GRI Sustainability Disclosure Database
- **URL**: https://database.globalreporting.org/
- **登録**: 不要
- **カバレッジ**: 60,000件以上のサステナビリティ報告書

**検索・ダウンロード**:
1. 企業名、国、業種でフィルタ
2. サステナビリティレポート（PDF）をダウンロード
3. 手動で指標を抽出（CO2排出量、女性従業員比率、労働安全指標等）

**テキスト分析への応用**:
- レポートのテキストマイニング（Python、NLP）
- キーワード頻度分析（"climate", "diversity", "ethics"）
- センチメント分析

#### 11. Yahoo Finance ESG Risk Ratings（簡易版）
- **URL**: https://finance.yahoo.com/ → 各企業ページの「Sustainability」タブ
- **データ提供**: Sustainalytics
- **カバレッジ**: 主要上場企業

**入手可能データ**:
- ESGリスクスコア（0-100、低いほど良い）
- Environment、Social、Governanceの各スコア
- 論争スコア（Controversy Score）

**取得方法**:
```python
import yfinance as yf

ticker = yf.Ticker("AAPL")
esg = ticker.sustainability

if esg is not None:
    print(f"Total ESG Score: {esg.loc['totalEsg']['Value']}")
    print(f"Environment Score: {esg.loc['environmentScore']['Value']}")
    print(f"Social Score: {esg.loc['socialScore']['Value']}")
    print(f"Governance Score: {esg.loc['governanceScore']['Value']}")
```

**制限**:
- 詳細指標は有料版のみ
- 時系列データは限定的

---

### マクロ経済・産業データ

#### 12. World Bank Open Data
- **URL**: https://data.worldbank.org/
- **登録**: 不要
- **カバレッジ**: 200以上の国・地域、1960年～

**主要指標**:
- GDP、GDP成長率、1人当たりGDP
- インフレ率、失業率
- 貿易収支、外国直接投資（FDI）
- ガバナンス指標（World Governance Indicators: 法の支配、汚職統制等）
- ビジネス環境（Doing Business indicators）

**データ取得**:

**方法1: Webダウンロード**
1. https://data.worldbank.org/indicator にアクセス
2. 指標を選択（例：NY.GDP.MKTP.CD = GDP）
3. 国と期間を選択
4. CSV、Excel、XMLでダウンロード

**方法2: Python API（`wbdata`）**
```python
import wbdata
import pandas as pd

# GDPデータ取得
countries = ['USA', 'JPN', 'CHN']
indicators = {'NY.GDP.MKTP.CD': 'gdp'}
data = wbdata.get_dataframe(indicators, country=countries)

# DataFrame変換
df = data.reset_index()
df['year'] = df['date'].str[:4]
```

**研究活用**:
- **国レベル制御変数**: GDP成長率、インフレ率
- **制度的要因**: ガバナンス指標（WGI）を企業レベルデータに結合
- **国際比較**: 国別の経済発展段階をコントロール

#### 13. OECD Data
- **URL**: https://data.oecd.org/
- **カバレッジ**: OECD加盟国38カ国 + パートナー国

**主要データセット**:
- **STAN Database**: 産業別統計（生産、雇用、R&D）
- **TiVA**: 貿易における付加価値（グローバルバリューチェーン分析）
- **R&D Statistics**: 国・産業別のR&D支出
- **生産性**: TFP（全要素生産性）、労働生産性

**データ取得**:
```python
# OECD APIを使用
import requests

def get_oecd_data(dataset, dimensions):
    url = f"https://stats.oecd.org/restsdmx/sdmx.ashx/GetData/{dataset}/{dimensions}/all"
    response = requests.get(url)
    # XML解析が必要（`pandasdmx`ライブラリ推奨）
    return response

# 使用例
# data = get_oecd_data('GERD', 'JPN+USA+CHN')  # 各国のR&D支出
```

**研究活用**:
- **産業レベル制御変数**: 産業別R&D集約度
- **国際比較**: 先進国間の制度・政策比較

#### 14. FRED（Federal Reserve Economic Data）
- **URL**: https://fred.stlouisfed.org/
- **登録**: 不要（API利用時は要登録）
- **カバレッジ**: 米国経済データ、80万以上の時系列

**主要データ**:
- リスクフリーレート（10年国債利回り）
- S&P 500指数
- GDP、失業率、インフレ率（CPI）
- 産業別生産指数

**データ取得**:

**方法1: Webダウンロード**
- 指標を検索 → 「Download」→ CSV

**方法2: Python API（`fredapi`）**
```python
from fredapi import Fred

fred = Fred(api_key='your_api_key')  # https://fred.stlouisfed.org/docs/api/api_key.html で取得

# S&P 500指数
sp500 = fred.get_series('SP500', observation_start='2020-01-01')

# 10年国債利回り（リスクフリーレート）
rf_rate = fred.get_series('GS10')
```

**研究活用**:
- **市場リターン**: S&P 500をベンチマークとして使用
- **リスクフリーレート**: 資本コスト計算（CAPM）
- **マクロ制御変数**: GDP成長率、インフレ率

---

## 🔬 専門分野別データソース

### M&A・企業買収

#### 15. SEC EDGAR（Form 8-K、DEF 14A）
- M&A発表は8-K（臨時報告）に記載
- 議決権行使資料（DEF 14A）に買収の詳細

**手動収集手順**:
1. 対象企業のEDGARページを開く
2. 8-Kファイルを年代順に確認
3. "merger", "acquisition", "business combination"で検索
4. 発表日、買収金額、対象企業、支払方法（現金/株式）を記録

**イベント日の特定**:
- 8-Kの「Date of Report」= イベント日
- イベントスタディに使用

### 取締役会・ガバナンス

#### 16. SEC EDGAR（DEF 14A - Proxy Statement）
- **URL**: https://www.sec.gov/edgar
- **データ**: 取締役会構成、役員報酬、議決権行使

**抽出可能変数**:
- 取締役の氏名、年齢、在任期間
- 独立取締役比率 = 独立取締役数 / 総取締役数
- 女性取締役比率
- CEO兼会長（CEO Duality）: CEO=Chairmanの場合1
- 取締役会規模

**日本の場合（EDINET）**:
- 有価証券報告書「役員の状況」セクション
- 同様の情報を手動抽出

### 役員報酬

#### 17. SEC EDGAR（DEF 14A）
- Summary Compensation Table（役員報酬サマリー）
- 給与、ボーナス、株式報酬、ストックオプション、年金、その他報酬

**変数構築例**:
- **Total Compensation** = Salary + Bonus + Stock Awards + Option Awards + ...
- **Pay-Performance Sensitivity** = ΔCompensation / ΔShareholder Wealth

### アナリスト予想

#### 18. Yahoo Finance（コンセンサス予想・無料）
- **URL**: https://finance.yahoo.com/quote/AAPL/analysis
- **データ**: アナリストの目標株価、EPS予想、推奨レーティング

**制限**:
- 現在のコンセンサスのみ（時系列データなし）
- 詳細なアナリストレベルデータは有料（I/B/E/S）

---

## 💡 実践的研究戦略：ゼロ予算研究の設計

### 戦略1: 米国企業研究（財務 + 特許 + マクロ）

**研究テーマ例**: 「R&D投資が企業パフォーマンスに与える影響：技術多様性の調整効果」

**データ収集計画**:
| 変数 | データソース | 取得方法 | 所要時間 |
|-----|------------|----------|---------|
| 財務データ（資産、売上、純利益） | SEC EDGAR (10-K) | Python クローラー | 2週間 |
| 特許データ（件数、引用数） | USPTO PatentsView | API | 1週間 |
| 技術多様性（CPC分類） | USPTO PatentsView | API | 同上 |
| マクロ制御変数（GDP成長率） | FRED | Python API | 1日 |
| 産業制御変数（R&D集約度） | OECD STAN | ダウンロード | 1日 |

**サンプル**: S&P 500企業 × 10年 = 5,000 firm-years

**推定コスト**: $0（データはすべて無料）

**推定所要時間**: 4週間（データ収集 + クリーニング）

---

### 戦略2: 日本企業研究（財務 + ガバナンス + ESG）

**研究テーマ例**: 「取締役会の女性比率と企業の環境パフォーマンス」

**データ収集計画**:
| 変数 | データソース | 取得方法 | 所要時間 |
|-----|------------|----------|---------|
| 財務データ | EDINET（有価証券報告書） | 手動抽出（50社×5年） | 2週間 |
| 取締役会構成（女性比率） | EDINET（役員の状況） | 手動抽出 | 1週間 |
| 環境パフォーマンス（CO2排出量） | 企業サステナビリティレポート | 手動抽出 | 1週間 |
| または CDP | CDP研究者ライセンス | ダウンロード | 1日（承認後） |
| マクロ制御変数 | World Bank | ダウンロード | 1日 |

**サンプル**: 東証プライム市場製造業50社 × 5年 = 250 firm-years

**推定コスト**: $0

**推定所要時間**: 5週間

---

### 戦略3: 国際比較研究（多国間）

**研究テーマ例**: 「制度的要因が企業の国際化戦略に与える影響：先進国 vs 新興国」

**データ収集計画**:
| 変数 | データソース | 取得方法 |
|-----|------------|----------|
| 企業データ（米国） | SEC EDGAR | Python |
| 企業データ（日本） | EDINET | 手動/API |
| 企業データ（英国） | Companies House | 手動 |
| 企業データ（その他） | OpenCorporates | 検索 |
| 制度的品質 | World Bank WGI | ダウンロード |
| ビジネス環境 | World Bank Doing Business | ダウンロード |

**サンプル**: 10カ国 × 各国30社 × 5年 = 1,500 firm-years

---

## ⚠️ データ利用上の注意事項

### 倫理・法的コンプライアンス

1. **利用規約の遵守**:
   - 各データソースの Terms of Service を必ず確認
   - 商用利用禁止のデータは研究目的のみで使用
   - データの再配布は通常禁止

2. **引用・出典明記**:
   - すべてのデータソースを論文に明記
   - 例：「財務データはSEC EDGARから取得（https://www.sec.gov/edgar）」
   - データセット固有の引用方法がある場合はそれに従う

3. **個人情報保護**:
   - 個人を特定できる情報は匿名化
   - 役員名等、公開情報であっても慎重に扱う

4. **Webスクレイピングの注意**:
   - robots.txt を確認
   - レート制限を守る（1秒に数リクエスト程度）
   - User-Agent に所属とメールアドレスを記載

### データ品質チェック

1. **欠損値の確認**:
   - 各変数の欠損率を計算
   - 欠損が多い変数（>30%）は使用を再検討

2. **外れ値の検出**:
   - 記述統計で異常値を確認
   - ウィンゾライズ（1%、99%パーセンタイルでキャップ）

3. **一貫性チェック**:
   - 複数ソースのデータを結合する際、整合性を確認
   - 例：総資産 > 総負債 + 純資産？（等式が成り立つか）

---

## 🎓 学習リソース

### データ取得を学ぶ

1. **Python for Finance**:
   - 書籍："Python for Finance" by Yves Hilpisch
   - オンライン：DataCamp、Coursera

2. **Web Scraping**:
   - Tutorial：Real Python "Web Scraping with Python"
   - ライブラリ：requests、BeautifulSoup、Selenium

3. **API利用**:
   - 各データソースの公式ドキュメント
   - GitHub：既存のスクリプト例を参照

### データクリーニング

1. **Pandas（Python）**:
   - 公式チュートリアル：https://pandas.pydata.org/docs/getting_started/tutorials.html

2. **dplyr（R）**:
   - R for Data Science: https://r4ds.had.co.nz/

---

## 📚 引用推奨

この無料データソースガイドを研究に活用した場合の謝辞例：

```
データ収集には、米国証券取引委員会EDGAR（https://www.sec.gov/edgar）、
USPTO PatentsView（https://patentsview.org/）、World Bank Open Data
（https://data.worldbank.org/）を使用した。本研究は、商用データベースを
使用せず、すべて公開データソースから収集したデータに基づいている。
```

---

## 🔄 このガイドの更新

**最終更新**: 2025-11-01  
**バージョン**: 1.0

**今後の追加予定**:
- 中国データソース（CSMAR代替）
- インド企業データ（CMIE Prowess代替）
- より多くの新興国データソース
- データ品質評価の詳細ガイド

---

## 💬 質問・フィードバック

このガイドに関する質問、追加してほしいデータソース、エラー報告は：
- GitHub Issues: [リンク]
- Email: [メールアドレス]

---

**あなたの研究を応援しています！予算ゼロでも、世界トップレベルの研究は可能です。** 🚀
