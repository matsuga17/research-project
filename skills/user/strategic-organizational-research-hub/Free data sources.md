# 無料・低コストデータソース完全ガイド

**予算ゼロでも実施可能な戦略・組織研究のためのデータソース集**

---

## 目次

1. [企業財務・市場データ](#企業財務市場データ)
2. [特許・イノベーションデータ](#特許イノベーションデータ)
3. [ESG・サステナビリティデータ](#esgサステナビリティデータ)
4. [M&A・アライアンスデータ](#maアライアンスデータ)
5. [マクロ経済・産業データ](#マクロ経済産業データ)
6. [地域別データソース（アジア太平洋）](#地域別データソース)
7. [予算ゼロ研究の実例](#予算ゼロ研究の実例)

---

## 企業財務・市場データ

### 1. SEC EDGAR（米国）🇺🇸

**URL**: https://www.sec.gov/edgar

**カバレッジ**: 米国上場企業（1994年以降）

**提供データ**:
- **10-K**（年次報告書）：財務諸表、経営陣の議論と分析（MD&A）、リスク要因
- **10-Q**（四半期報告書）：四半期財務諸表
- **8-K**（重要事象報告）：M&A、CEO交代、製品リコール等
- **DEF 14A**（委任状）：役員報酬、取締役会構成、株主提案
- **Form 4**（インサイダー取引）：役員・大株主の株式取引
- **Schedule 13D/13G**（5%以上保有報告）：大株主情報

**取得方法**:
1. **手動ダウンロード**: EDGAR検索インターフェース
2. **API**: `edgartools`（Python）、`edgar`（R）
3. **バルクダウンロード**: EDGAR Full Index Files

**使用例**:
```python
# edgartools (Python)を使用
from edgar import Company

apple = Company("AAPL")
filings = apple.get_filings(form="10-K")
latest_10k = filings[0]
text = latest_10k.text()  # 全文テキスト取得
```

**研究での活用**:
- 財務指標：総資産、売上高、純利益、R&D費用、広告費
- ガバナンス：役員報酬、取締役会規模、独立性
- リスク開示：10-Kの「Risk Factors」セクション（テキスト分析）
- イベントスタディ：8-K発表日

---

### 2. EDINET（日本）🇯🇵

**URL**: https://disclosure2.edinet-fsa.go.jp/

**カバレッジ**: 日本の上場企業・開示企業（1999年以降）

**提供データ**:
- **有価証券報告書**（年次）：財務諸表、事業概況、役員状況
- **四半期報告書**：四半期財務
- **臨時報告書**：重要事象（M&A、CEO交代等）
- **大量保有報告書**：5%以上保有者

**取得方法**:
1. **手動ダウンロード**: EDINET検索
2. **API**: EDINET API（開発者登録不要、無料）
3. **Python**: `xbrr-edinet`パッケージ

**使用例**:
```python
# EDINET APIを使用
import requests

# 書類一覧取得（例：2024年10月の有価証券報告書）
url = "https://disclosure2.edinet-fsa.go.jp/api/v2/documents.json"
params = {
    "date": "2024-10-01",
    "type": 2  # 2 = 有価証券報告書
}
response = requests.get(url, params=params)
documents = response.json()
```

**研究での活用**:
- 財務データ：総資産、売上高、営業利益、従業員数
- 役員情報：役員の状況（氏名、年齢、保有株式）
- セグメント情報：事業別・地域別売上
- R&D費用：研究開発費

**注意点**: 日本語データなので、翻訳ツールや日本語処理ライブラリが必要

---

### 3. OpenCorporates（グローバル）🌍

**URL**: https://opencorporates.com/

**カバレッジ**: 200M+企業、130+管轄区域

**提供データ**:
- 企業登記情報：設立年、本社所在地、登録番号
- 役員情報：取締役、代表者
- 企業ステータス：active / dissolved

**取得方法**:
1. **無料検索**: ウェブインターフェース
2. **API**: 無料プラン（月500リクエスト）、有料プラン（unlimited）

**研究での活用**:
- 企業年齢：設立年から計算
- 企業所在地：地域研究
- 役員ネットワーク：複数企業に関与する役員

---

### 4. Yahoo Finance（グローバル）💹

**URL**: https://finance.yahoo.com/

**カバレッジ**: グローバル株式市場

**提供データ**:
- 株価：日次、週次、月次
- 財務諸表：簡易版（収益・費用、バランスシート）
- ESGスコア：Sustainalytics提供（限定的）

**取得方法**:
- **Python**: `yfinance`パッケージ

**使用例**:
```python
import yfinance as yf

# Appleの株価取得
aapl = yf.Ticker("AAPL")
hist = aapl.history(period="5y")  # 過去5年の株価
financials = aapl.financials  # 財務諸表

# ESGスコア
esg = aapl.sustainability  # Sustainalytics ESGスコア
```

**研究での活用**:
- 市場パフォーマンス：株価リターン、ボラティリティ
- Tobin's Q：市場価値 / 簿価
- イベントスタディ：異常リターン計算

---

## 特許・イノベーションデータ

### 1. USPTO PatentsView（米国）🇺🇸

**URL**: https://patentsview.org/

**カバレッジ**: 全米国特許（1976年以降）、10M+特許

**提供データ**:
- 特許情報：特許番号、タイトル、要約、出願日、登録日
- 引用情報：被引用数、引用特許
- 発明者・譲受人：企業名、発明者名、所在地
- 技術分類：CPC、IPC、USPC

**取得方法**:
1. **バルクダウンロード**: TSVファイル（全データ）
2. **API**: RESTful API（無制限、無料）
3. **ウェブ検索**: 検索インターフェース

**使用例**（API）:
```python
import requests

# 特定企業の特許検索
url = "https://api.patentsview.org/patents/query"
query = {
    "q": {"assignee_organization": "Apple Inc"},
    "f": ["patent_number", "patent_title", "patent_date", "cited_patent_count"],
    "o": {"per_page": 100}
}
response = requests.post(url, json=query)
patents = response.json()
```

**研究での活用**:
- **イノベーション産出**: 特許数
- **イノベーション品質**: 引用重み付き特許数
- **技術多様性**: 異なるCPCクラス数
- **企業マッチング**: 企業名を用いてCompustatとマッチング

**企業マッチングの課題**:
- 企業名の表記揺れ（"Apple Inc" vs "Apple Computer, Inc"）
- 解決策：Fuzzy matching、手動検証、NBER Patent-Compustat Linkage使用

---

### 2. Google Patents（グローバル）🌍

**URL**: https://patents.google.com/

**カバレッジ**: 米国、欧州、日本、中国、韓国等の特許

**提供データ**:
- 特許全文、図面
- 引用関係
- 特許ファミリー（同一発明の各国出願）
- 法的ステータス（有効/失効）

**取得方法**:
- **ウェブ検索**: 高度な検索機能
- **バルクダウンロード**: 公開データセット（Google Cloud BigQuery）

**研究での活用**:
- グローバル特許戦略：特許ファミリー分析
- 特許有効性：失効特許の除外

---

### 3. WIPO PatentScope（グローバル）🌍

**URL**: https://patentscope.wipo.int/

**カバレッジ**: 90+国の特許庁データ、PCT出願

**提供データ**:
- 国際特許出願（PCT）
- 各国特許データ

**取得方法**:
- **ウェブ検索**: 多言語対応
- **API**: SOAP API

---

### 4. NBER Patent Data Project（米国・無料研究者向け）🇺🇸

**URL**: https://sites.google.com/site/patentdataproject/

**カバレッジ**: 米国特許（1976-2006）+ Compustatリンク

**提供データ**:
- 特許とCompustat企業のマッチング（GVKEY付き）
- 引用データ
- 技術分類

**ダウンロード**: CSVファイル（無料）

**引用**: Hall, Jaffe, & Trajtenberg (2001, 2005)

**研究での活用**:
- 企業レベルイノベーション分析（特許数、引用数）
- Compustatとの直接統合

---

## ESG・サステナビリティデータ

### 1. CDP (Carbon Disclosure Project)（グローバル・研究者向け無料）🌍

**URL**: https://www.cdp.net/en/academic-research

**カバレッジ**: 13,000+企業の気候変動対応データ

**提供データ**:
- **炭素排出量**: Scope 1, 2, 3
- **気候変動戦略**: 削減目標、再生可能エネルギー使用
- **リスク・機会**: 気候変動関連リスクの開示
- **水・森林**: 水管理、森林保護活動

**アクセス方法**:
1. 学術研究ライセンス申請（無料）
2. 承認後、データダウンロード

**研究での活用**:
- ESGパフォーマンス：炭素排出量、削減率
- 気候変動開示：開示品質スコア
- 環境戦略：再エネ使用率

---

### 2. GRI Sustainability Disclosure Database（グローバル）🌍

**URL**: https://database.globalreporting.org/

**カバレッジ**: 60,000+サステナビリティ報告書、15,000+組織

**提供データ**:
- GRI準拠のサステナビリティ報告書（PDF）
- 環境・社会・ガバナンス指標

**アクセス方法**:
- 無料検索・ダウンロード

**研究での活用**:
- サステナビリティ報告の有無（binary variable）
- GRI準拠レベル（Core / Comprehensive）
- 報告書のテキスト分析

---

### 3. Sustainalytics ESG Risk Ratings（限定的・無料）🌍

**URL**: Yahoo Finance経由（https://finance.yahoo.com/）

**カバレッジ**: 主要上場企業

**提供データ**:
- ESGリスクスコア（0-100）: 低いほど良い
- カテゴリー別スコア（E, S, G）
- 論争事例

**アクセス方法**:
- Yahoo Finance API (`yfinance`パッケージ)

**使用例**:
```python
import yfinance as yf

ticker = yf.Ticker("AAPL")
esg_data = ticker.sustainability
print(esg_data)  # ESGスコア、論争レベル等
```

**制限**: 詳細な履歴データなし（最新データのみ）

---

### 4. 企業のESG報告書（個別企業ウェブサイト）🌍

**アクセス方法**:
- 各企業のIRサイト → サステナビリティ / ESG / CSRセクション

**提供データ**:
- 炭素排出量（Scope 1, 2, 3）
- エネルギー使用量
- ダイバーシティ指標（女性役員比率等）
- 従業員関連指標

**研究での活用**:
- 手動データ収集（サンプルが小さい場合）
- テキスト分析（ESG報告書の質）

---

## M&A・アライアンスデータ

### 1. SEC EDGAR 8-K（M&A発表）🇺🇸

**URL**: https://www.sec.gov/edgar

**Form 8-K, Item 1.01**: 重要な契約締結（M&A、アライアンス）

**研究での活用**:
- M&A発表日の特定（イベントスタディ）
- ディール条件（一部開示）

---

### 2. 企業プレスリリース（グローバル）🌍

**アクセス方法**:
- 企業のIRサイト → Press Releases / News
- PR Newswire、Business Wire（一部無料）

**研究での活用**:
- M&A、アライアンス、製品発表の日付特定
- イベントスタディのイベント日

---

### 3. Crunchbase（スタートアップ・一部無料）🌍

**URL**: https://www.crunchbase.com/

**カバレッジ**: スタートアップ、VC投資、M&A

**提供データ（無料プラン）**:
- 企業基本情報（設立年、業種、本社）
- 資金調達履歴（ラウンド、金額、投資家）
- M&A情報（買収企業、買収価格）

**制限**: エクスポート機能なし、手動収集のみ

**研究での活用**:
- スタートアップのVC投資パターン
- M&Aターゲット特性

---

## マクロ経済・産業データ

### 1. World Bank Open Data（グローバル）🌍

**URL**: https://data.worldbank.org/

**カバレッジ**: 200+国、1960年以降

**提供データ**:
- **経済指標**: GDP、GDP成長率、インフレ、失業率
- **ガバナンス**: Worldwide Governance Indicators（WGI）
  - 政府の有効性、規制の質、法の支配、汚職抑制
- **ビジネス環境**: Doing Business指標（2020年まで）
- **貿易**: 輸出入額、貿易相手国

**アクセス方法**:
1. **ウェブインターフェース**: データブラウザ
2. **API**: REST API（無料、無制限）
3. **Pythonパッケージ**: `wbdata`、`pandas_datareader`
4. **Rパッケージ**: `WDI`

**使用例（Python）**:
```python
import wbdata

# GDP per capita（日本、2010-2023）
indicator = "NY.GDP.PCAP.CD"  # GDP per capita (current US$)
data = wbdata.get_dataframe({indicator: "GDP_per_capita"}, 
                             country="JPN", 
                             date=(2010, 2023))
print(data)
```

**研究での活用**:
- **国レベル制御変数**: GDP成長率、インフレ、失業率
- **制度的要因**: WGI指標（制度の質、汚職）
- **国際戦略研究**: 進出国の経済環境

---

### 2. OECD Data（OECD諸国）🌍

**URL**: https://data.oecd.org/

**カバレッジ**: OECD加盟国+パートナー国

**提供データ**:
- **産業統計**: 産業別付加価値、雇用、R&D
- **労働市場**: 賃金、労働生産性
- **貿易**: 産業別輸出入
- **R&D**: 国・産業別R&D支出

**アクセス方法**:
1. **ウェブインターフェース**: データエクスプローラー
2. **API**: SDMX REST API

**研究での活用**:
- **産業レベル制御変数**: 産業成長率、R&D集約度
- **国際比較**: OECD諸国間の産業構造比較

---

### 3. FRED (Federal Reserve Economic Data)（米国）🇺🇸

**URL**: https://fred.stlouisfed.org/

**カバレッジ**: 米国経済データ（1776年以降）

**提供データ**:
- **金利**: Federal Funds Rate、Treasury Rates
- **マクロ**: GDP、インフレ（CPI）、失業率
- **産業**: 産業別生産指数

**アクセス方法**:
1. **ウェブインターフェース**: 検索・グラフ作成
2. **API**: `fredapi`（Python）

**使用例**:
```python
from fredapi import Fred

fred = Fred(api_key='your_api_key')  # 無料登録
gdp = fred.get_series('GDP')  # 米国GDP
```

**研究での活用**:
- **リスクフリーレート**: 10年国債利回り
- **マクロ制御変数**: GDP成長率、インフレ率

---

### 4. IMF Data（グローバル）🌍

**URL**: https://data.imf.org/

**カバレッジ**: IMF加盟国

**提供データ**:
- 国際金融統計（IFS）
- 国際収支（BOP）
- 世界経済見通し（WEO）

**アクセス方法**:
- ウェブインターフェース（無料）
- API（SDMXフォーマット）

---

### 5. Fama-French Data Library（市場ファクター・米国）🇺🇸

**URL**: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html

**カバレッジ**: 米国（1926年以降）、グローバル（1990年以降）

**提供データ**:
- **市場ファクター**: Mkt-RF（市場超過リターン）、SMB（規模）、HML（バリュー）
- **追加ファクター**: RMW（収益性）、CMA（投資）、Momentum

**アクセス方法**:
- CSVダウンロード（無料）
- Pythonパッケージ: `pandas_datareader`

**使用例**:
```python
import pandas_datareader as pdr

# Fama-French 5 factors（月次）
ff5 = pdr.get_data_famafrench('F-F_Research_Data_5_Factors_2x3', 
                               start='2010')[0]
print(ff5.head())
```

**研究での活用**:
- **リスク調整後リターン**: 株価パフォーマンス分析
- **ファクターモデル**: 企業パフォーマンスの説明

---

## 地域別データソース（アジア太平洋）

### 日本 🇯🇵

#### 1. EDINET（開示書類）
- **URL**: https://disclosure2.edinet-fsa.go.jp/
- **データ**: 有価証券報告書、四半期報告書、大量保有報告書
- **アクセス**: 無料、API有り

#### 2. e-Stat（政府統計）
- **URL**: https://www.e-stat.go.jp/
- **データ**: 企業統計、産業統計、経済センサス
- **アクセス**: 無料、API有り

#### 3. 法人番号公表サイト
- **URL**: https://www.houjin-bangou.nta.go.jp/
- **データ**: 企業基本情報（法人名、本社所在地、法人番号）
- **アクセス**: 無料、ダウンロード可

#### 4. 特許情報プラットフォーム J-PlatPat
- **URL**: https://www.j-platpat.inpit.go.jp/
- **データ**: 日本特許、商標、意匠
- **アクセス**: 無料検索

---

### 中国 🇨🇳

#### 1. CNRDS (China Research Data Service)
- **URL**: https://www.cnrds.com/
- **データ**: 上場企業財務、市場データ
- **アクセス**: **無料プラン有り**（制限あり）

#### 2. CSMAR (一部データ無料)
- **URL**: https://www.gtarsc.com/
- **データ**: 財務、市場、ガバナンス
- **アクセス**: 大学契約 or 有料、一部データ無料トライアル

#### 3. 中国国家統計局
- **URL**: http://www.stats.gov.cn/english/
- **データ**: マクロ経済、産業統計
- **アクセス**: 無料

---

### 韓国 🇰🇷

#### 1. DART (Data Analysis, Retrieval and Transfer System)
- **URL**: https://dart.fss.or.kr/
- **データ**: 韓国上場企業開示書類（財務諸表、事業報告書）
- **アクセス**: 無料、API有り（韓国語・一部英語）

#### 2. Bank of Korea Economic Statistics System
- **URL**: https://ecos.bok.or.kr/
- **データ**: マクロ経済、金融データ
- **アクセス**: 無料

---

### 台湾 🇹🇼

#### 1. Taiwan Stock Exchange (TWSE) Market Observation Post System
- **URL**: https://mops.twse.com.tw/mops/web/index
- **データ**: 上場企業財務諸表、市場データ
- **アクセス**: 無料（中国語・一部英語）

#### 2. National Statistics, Taiwan
- **URL**: https://eng.stat.gov.tw/
- **データ**: マクロ経済、産業統計
- **アクセス**: 無料

---

### インド 🇮🇳

#### 1. BSE (Bombay Stock Exchange) / NSE (National Stock Exchange)
- **URL**: https://www.bseindia.com/, https://www.nseindia.com/
- **データ**: 株価、財務諸表（限定的）
- **アクセス**: 無料

#### 2. Reserve Bank of India Database
- **URL**: https://www.rbi.org.in/Scripts/Statistics.aspx
- **データ**: マクロ経済、金融統計
- **アクセス**: 無料

---

## 予算ゼロ研究の実例

### 実例1: 日本製造業におけるR&D投資と企業パフォーマンス

**研究質問**: R&D投資は企業パフォーマンスを向上させるか？

**データソース（すべて無料）**:
1. **財務データ**: EDINET（有価証券報告書）
   - 変数: 総資産、売上高、純利益、R&D費用、従業員数
2. **特許データ**: USPTO PatentsView
   - 変数: 特許数（日本企業が米国出願）
3. **産業データ**: OECD STAN Database
   - 変数: 産業別R&D集約度
4. **マクロデータ**: World Bank
   - 変数: 日本のGDP成長率、為替レート

**サンプル**: 日本の製造業上場企業、2010-2023年

**分析手法**: パネルデータ回帰（固定効果モデル）

**モデル**:
```
ROA_it = β0 + β1*RD_Intensity_it-1 + β2*log(Assets)_it + β3*Leverage_it + 
         α_i + δ_t + ε_it
```

**予想される結果**: R&D集約度（R&D費用/売上高）が高いほど、翌年のROAが高い

**合計コスト**: **$0**（時間のみ）

---

### 実例2: 米国テック企業のCEO交代がイノベーションに与える影響

**研究質問**: CEO交代はイノベーション産出（特許）に影響を与えるか？

**データソース（すべて無料）**:
1. **CEO交代データ**: SEC EDGAR 8-K（Item 5.02: Director or Officer Changes）
2. **企業財務**: SEC EDGAR 10-K
   - 変数: 総資産、売上高、R&D費用
3. **特許データ**: USPTO PatentsView
   - 変数: 特許数、引用重み付き特許数
4. **株価データ**: Yahoo Finance (`yfinance`)
   - 変数: 株価リターン

**サンプル**: S&P 500のテクノロジー企業、2010-2023年

**分析手法**: 差分の差分法（DiD）

**モデル**:
```
Patent_Count_it = β0 + β1*CEO_Change_i + β2*Post_t + β3*(CEO_Change × Post) + 
                   Controls + ε_it
```

**合計コスト**: **$0**

---

### 実例3: アジア新興国における取締役会の多様性とESGパフォーマンス

**研究質問**: 取締役会の女性比率はESGパフォーマンスを向上させるか？

**データソース（すべて無料）**:
1. **取締役会データ**:
   - 日本: EDINET（有価証券報告書、役員の状況）
   - 韓国: DART（사업보고서）
   - 台湾: MOPS（公開資訊觀測站）
2. **ESGデータ**: CDP（研究者ライセンス）
   - 変数: 炭素排出量、ESG開示スコア
3. **財務データ**: 各国証券取引所
   - 日本: EDINET
   - 韓国: DART
   - 台湾: MOPS
4. **マクロデータ**: World Bank
   - 変数: GDP成長率、ガバナンス指標（WGI）

**サンプル**: 日本、韓国、台湾の製造業上場企業、2015-2023年

**分析手法**: パネルデータ回帰（固定効果）

**合計コスト**: **$0** + 翻訳ツール（Google Translate無料版）

---

## データ収集の実践ガイド

### ステップ1: データソースの選択
1. 研究質問に基づき必要な変数をリストアップ
2. 各変数に対応する無料データソースを特定
3. カバレッジ（時期、地域）を確認

### ステップ2: パイロットデータ収集
1. 10-20企業の1-2年分のデータを試験的に収集
2. データの入手可能性を確認
3. 欠損値の程度を評価

### ステップ3: フルデータ収集
1. API、バルクダウンロード、Webスクレイピングを活用
2. 生データを保存（変更しない）
3. データ収集ログを記録（日付、ソース、クエリ）

### ステップ4: データクリーニング
1. 欠損値の処理
2. 外れ値の検出と処理（ウィンソライズ）
3. 変数の構築（log変換、ラグ変数等）

### ステップ5: データ統合
1. 複数ソースのデータをマージ（企業ID、年で結合）
2. マッチング率を確認
3. データ辞書を作成

---

## よくある質問（FAQ）

### Q1: 英語のデータソースしかない場合、日本企業の研究はできますか？
**A**: はい。多くの日本企業は米国でも特許出願（USPTO）しており、また、米国上場ADR（American Depositary Receipt）として財務情報がSEC EDGARにあります。ただし、カバレッジは限定的です。

### Q2: 無料データの品質は有料データと比べてどうですか？
**A**: 公的機関が提供する無料データ（SEC、USPTO、World Bank等）は高品質です。ただし、有料データベース（Compustat、CRSP）は以下の利点があります：
- クリーニング済み、標準化された形式
- ユーザーフレンドリーなインターフェース
- 長期の履歴データ

**結論**: 無料データで十分高品質な研究が可能。時間をかけて丁寧にクリーニングすれば、有料データと遜色ない結果が得られます。

### Q3: データ収集にどれくらい時間がかかりますか？
**A**: プロジェクトにより異なりますが：
- **小規模**（100企業×5年）: 1-2週間
- **中規模**（500企業×10年）: 4-6週間
- **大規模**（2000企業×15年）: 8-12週間

自動化（API、スクリプト）を活用すれば大幅に短縮可能。

### Q4: データの使用許可は必要ですか？
**A**: 公的データ（SEC、USPTO、World Bank等）は基本的に自由に使用可能。ただし：
- **引用**: データソースを論文で適切に引用
- **利用規約**: 各ウェブサイトの Terms of Service を確認
- **Webスクレイピング**: 過度なリクエストは避ける（robots.txt確認）

---

## まとめ

予算ゼロでも、以下の組み合わせで高品質な戦略・組織研究が可能：

1. **企業財務**: SEC EDGAR、EDINET、Yahoo Finance
2. **特許**: USPTO PatentsView、Google Patents
3. **ESG**: CDP、GRI Database、企業報告書
4. **マクロ**: World Bank、OECD、FRED
5. **地域別**: EDINET（日本）、DART（韓国）、MOPS（台湾）

**成功の鍵**:
- 計画的なデータ収集（パイロット → フル収集）
- 自動化（API、スクリプト）
- 丁寧なクリーニングとドキュメンテーション
- 複数ソースの統合

**予算がなくても、情熱と時間があれば世界レベルの研究が可能です！**

---

**次のステップ**:
- 実例を参考に、自分の研究計画を立てる
- パイロットデータ収集を開始
- データクリーニングスクリプトを作成

**質問・提案**: GitHub Issues または Email で受付中