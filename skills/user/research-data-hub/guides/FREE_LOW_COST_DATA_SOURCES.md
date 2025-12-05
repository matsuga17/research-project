# 無料・低コストデータソース完全ガイド
## アジア・ビジネス研究特化版

**最終更新**: 2025-10-31  
**対象地域**: 日本、韓国、中国、台湾、ASEAN（シンガポール、ベトナム、マレーシア、タイ、インドネシア、フィリピン）

---

## 目次

1. [日本](#1-日本)
2. [韓国](#2-韓国)
3. [中国](#3-中国本土)
4. [台湾](#4-台湾)
5. [シンガポール](#5-シンガポール)
6. [ベトナム](#6-ベトナム)
7. [マレーシア](#7-マレーシア)
8. [タイ](#8-タイ)
9. [インドネシア](#9-インドネシア)
10. [フィリピン](#10-フィリピン)
11. [香港](#11-香港)
12. [グローバル・国際機関](#12-グローバル国際機関データソース)
13. [クロスカントリー研究のための統合戦略](#13-クロスカントリー研究のための統合戦略)
14. [無料データを使った研究テーマ例](#14-無料データを使った研究テーマ例)

---

## 1. 日本

### 1.1 政府統計・公式データ

#### **e-Stat（政府統計ポータル）**
- **URL**: https://www.e-stat.go.jp/
- **提供元**: 総務省統計局
- **内容**: 
  - 経済センサス（全産業の事業所・企業統計）
  - 工業統計調査
  - 商業統計
  - 企業活動基本調査
  - 法人企業統計調査
  - GDP統計、産業連関表
- **データ形式**: CSV、Excel、API（REST API利用可能）
- **更新頻度**: 調査により異なる（年次、四半期）
- **言語**: 日本語（一部英語）
- **API**: あり（https://www.e-stat.go.jp/api/）
- **費用**: 完全無料

**活用例**:
- 産業別・地域別の企業パフォーマンス分析
- 企業規模分布の研究
- 地域経済の実証分析

#### **EDINET（金融商品取引法に基づく有価証券報告書等の開示システム）**
- **URL**: https://disclosure2.edinet-fsa.go.jp/
- **提供元**: 金融庁
- **内容**:
  - 有価証券報告書（年次・四半期）
  - 内部統制報告書
  - 大量保有報告書
  - 公開買付報告書
  - コーポレートガバナンス報告書
- **データ形式**: XBRL、PDF、HTML
- **更新頻度**: リアルタイム（提出後即公開）
- **言語**: 日本語
- **API**: あり（EDINET API）
- **費用**: 完全無料

**取得可能な財務データ**:
- 連結・個別財務諸表（BS、PL、CF）
- セグメント情報
- 役員報酬
- 大株主情報
- 研究開発費
- 従業員数

**Pythonでの利用例**:
```python
import requests
import pandas as pd

# EDINET API（書類一覧取得）
date = "2024-03-31"
api_url = f"https://disclosure.edinet-fsa.go.jp/api/v1/documents.json?date={date}&type=2"
response = requests.get(api_url)
data = response.json()

# 有価証券報告書のダウンロード
doc_id = data['results'][0]['docID']
xbrl_url = f"https://disclosure.edinet-fsa.go.jp/api/v1/documents/{doc_id}?type=1"
```

#### **日本取引所グループ（JPX）公開データ**
- **URL**: https://www.jpx.co.jp/markets/statistics-equities/index.html
- **提供元**: 日本取引所グループ
- **内容**:
  - 東証・名証の全銘柄データ
  - 日次株価・出来高
  - 上場企業一覧
  - 業種分類
  - TOPIX構成銘柄
  - 信用取引残高
  - 空売り比率
- **データ形式**: CSV、Excel
- **更新頻度**: 日次
- **言語**: 日本語・英語
- **費用**: 完全無料

**ダウンロード可能データ**:
- 個別銘柄株価（OHLC、出来高）: https://www.jpx.co.jp/markets/statistics-equities/misc/01.html
- 市場区分別時価総額: https://www.jpx.co.jp/markets/statistics-equities/misc/02.html

#### **内閣府 経済社会総合研究所（ESRI）**
- **URL**: https://www.esri.cao.go.jp/
- **内容**:
  - 企業行動アンケート調査
  - 景気動向指数
  - 消費動向調査
  - 法人企業景気予測調査
- **データ形式**: Excel、CSV
- **費用**: 完全無料

### 1.2 産業団体・業界統計

#### **日本銀行 統計データ**
- **URL**: https://www.stat-search.boj.or.jp/
- **内容**:
  - 企業短期経済観測調査（短観）
  - 貸出・預金動向
  - 資金循環統計
  - 物価指数
- **データ形式**: CSV、Excel、API
- **費用**: 完全無料

#### **経済産業省 企業データ**
- **URL**: https://www.meti.go.jp/statistics/index.html
- **内容**:
  - 企業活動基本調査（親会社・子会社関係含む）
  - 海外事業活動基本調査
  - 特定サービス産業実態調査
- **データ形式**: Excel、CSV
- **費用**: 完全無料

### 1.3 特許・イノベーションデータ

#### **J-PlatPat（特許情報プラットフォーム）**
- **URL**: https://www.j-platpat.inpit.go.jp/
- **提供元**: 特許庁
- **内容**:
  - 特許・実用新案・意匠・商標の検索
  - 出願人別統計
  - 技術分野別統計
- **データ形式**: HTML、CSV（一括ダウンロード制限あり）
- **費用**: 完全無料

**注意**: 大量データ取得には特許庁の承認が必要な場合あり

#### **NISTEP（科学技術・学術政策研究所）データベース**
- **URL**: https://www.nistep.go.jp/research/scisip/data-and-information-infrastructure
- **内容**:
  - 日本企業のイノベーション調査
  - 産学連携データ
  - 研究開発投資データ
- **費用**: 一部無料

### 1.4 ESG・サステナビリティデータ

#### **環境省 環境報告書データベース**
- **URL**: https://www.env.go.jp/policy/hairyo_report/
- **内容**:
  - 企業の環境報告書・統合報告書
  - GHG排出量データ
- **データ形式**: PDF
- **費用**: 完全無料

---

## 2. 韓国

### 2.1 政府・証券取引所データ

#### **DART（Data Analysis, Retrieval and Transfer System）**
- **URL**: https://dart.fss.or.kr/
- **提供元**: 金融監督院（FSS）
- **内容**:
  - 上場企業財務諸表（年次・四半期）
  - 監査報告書
  - 事業報告書
  - 주요사항보고（重要事項報告）
- **データ形式**: HTML、XBRL、API
- **言語**: 韓国語（一部英語）
- **API**: あり（Open DART API - https://opendart.fss.or.kr/）
- **費用**: 完全無料

**Open DART API 使用例**:
```python
import requests

# API Key取得: https://opendart.fss.or.kr/ でユーザー登録
API_KEY = "your_api_key"

# 企業情報取得
corp_code = "00126380"  # サムスン電子
url = f"https://opendart.fss.or.kr/api/company.json?crtfc_key={API_KEY}&corp_code={corp_code}"
response = requests.get(url)
data = response.json()
```

**取得可能データ**:
- 財務諸表（BS、PL、CF）
- 関係会社情報
- 最大株主情報
- 役員・従業員報酬
- 配当情報

#### **韓国取引所（KRX - Korea Exchange）**
- **URL**: http://data.krx.co.kr/
- **内容**:
  - KOSPI・KOSDAQ全銘柄株価データ
  - 時価総額
  - 外国人持株比率
  - 信用取引
- **データ形式**: Excel、CSV
- **言語**: 韓国語・英語
- **費用**: 完全無料

**データダウンロード手順**:
1. http://data.krx.co.kr/contents/MDC/MAIN/main/index.cmd
2. メニュー選択: 株式 > 個別銘柄 > 株価推移
3. 期間・銘柄指定してExcelダウンロード

#### **韓国統計庁（KOSTAT）**
- **URL**: https://kostat.go.kr/
- **英語版**: https://kostat.go.kr/portal/eng/index.action
- **内容**:
  - 経済センサス
  - 企業構造統計
  - 鉱工業生産指数
- **データ形式**: Excel、CSV
- **API**: あり（KOSIS API）
- **費用**: 完全無料

### 2.2 韓国銀行（BOK）経済統計

#### **韓国銀行 経済統計システム**
- **URL**: https://ecos.bok.or.kr/
- **内容**:
  - 企業経営分析（業種別財務比率）
  - GDP統計
  - 金融統計
  - 物価指数
- **API**: あり（ECOS API）
- **費用**: 完全無料

---

## 3. 中国本土

### 3.1 政府・証券取引所データ

#### **中国証券監督管理委員会（CSRC）情報開示**
- **URL**: http://www.csrc.gov.cn/
- **内容**:
  - 上場企業公告
  - 監督管理情報
- **言語**: 中国語
- **費用**: 完全無料

#### **上海証券取引所（SSE）**
- **URL**: http://www.sse.com.cn/
- **英語版**: http://english.sse.com.cn/
- **内容**:
  - 上海A株・B株全銘柄データ
  - 上場企業年報・定期報告
  - 財務諸表（中国会計基準）
  - コーポレートガバナンス情報
- **データ形式**: PDF、Excel、HTML
- **API**: 限定的（一部データのみ）
- **費用**: 完全無料

**データ所在**:
- 年報: http://www.sse.com.cn/disclosure/listedinfo/announcement/
- 株価データ: http://www.sse.com.cn/market/stockdata/overview/day/

#### **深圳証券取引所（SZSE）**
- **URL**: http://www.szse.cn/
- **英語版**: http://www.szse.cn/English/
- **内容**:
  - 深圳A株・B株・ChiNext全銘柄データ
  - 財務諸表
  - 公司公告
- **データ形式**: PDF、Excel
- **費用**: 完全無料

**データダウンロード**:
- 統計データ: http://www.szse.cn/market/overview/index.html

#### **中国国家統計局（NBS）**
- **URL**: http://www.stats.gov.cn/
- **英語版**: http://www.stats.gov.cn/english/
- **内容**:
  - 工業企業統計
  - 小売・卸売統計
  - GDP統計
  - 固定資産投資
- **データ形式**: Excel、CSV
- **費用**: 完全無料

**国家データポータル**:
- https://data.stats.gov.cn/

### 3.2 代替データソース

#### **巨潮資訊網（CNINFO）**
- **URL**: http://www.cninfo.com.cn/
- **内容**:
  - 上海・深圳両取引所の公式開示プラットフォーム
  - 年報、中間報告、四半期報告
  - 重大事項公告
- **データ形式**: PDF、HTML
- **費用**: 完全無料

**特徴**: 
- 中国上場企業の最も包括的な公開データソース
- 企業検索機能が充実
- 過去データへのアクセスも可能

#### **Tushare（中国金融データAPI）**
- **URL**: https://tushare.pro/
- **内容**:
  - A株全銘柄の日次株価（無料は500銘柄/日まで）
  - 財務データ（年報・四半期）
  - 指数データ
- **データ形式**: Python API
- **費用**: 基本無料（登録必要）、有料プランで制限解除
- **言語**: 中国語・英語（ドキュメント）

**Pythonでの利用**:
```python
import tushare as ts

# ユーザー登録後トークン取得: https://tushare.pro/register
ts.set_token('your_token')
pro = ts.pro_api()

# 株価データ取得
df = pro.daily(ts_code='600519.SH', start_date='20240101', end_date='20241031')
print(df.head())
```

#### **AKShare（オープンソース金融データライブラリ）**
- **GitHub**: https://github.com/akfamily/akshare
- **ドキュメント**: https://akshare.akfamily.xyz/
- **内容**:
  - A株株価データ
  - マクロ経済指標
  - 商品先物
  - 仮想通貨
- **データ形式**: Python API
- **費用**: 完全無料（オープンソース）
- **特徴**: 登録不要、制限なし

**使用例**:
```python
import akshare as ak

# A株日次データ
stock_zh_a_daily_df = ak.stock_zh_a_daily(symbol="sh600519", start_date="20240101", end_date="20241031")
print(stock_zh_a_daily_df)
```

---

## 4. 台湾

### 4.1 証券取引所・政府データ

#### **台湾証券取引所（TWSE）**
- **URL**: https://www.twse.com.tw/
- **英語版**: https://www.twse.com.tw/en/
- **内容**:
  - 上場企業株価データ（日次・分単位）
  - 財務諸表
  - 配当情報
  - 外資持株比率
- **データ形式**: CSV、Excel、JSON
- **API**: あり（REST API）
- **費用**: 完全無料

**API例**:
```python
import requests
import pandas as pd

# 日次株価データ取得
date = "20241031"
url = f"https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date={date}&type=ALL"
response = requests.get(url)
data = response.json()
```

**データ所在**:
- 統計資料: https://www.twse.com.tw/zh/page/trading/exchange/MI_INDEX.html
- 上場企業情報: https://www.twse.com.tw/zh/page/listed/company/companyBasic.html

#### **公開資訊觀測站（MOPS）**
- **URL**: https://mops.twse.com.tw/
- **提供元**: 台湾証券取引所
- **内容**:
  - 上場・上櫃企業の財務諸表（年次・四半期）
  - 年報・中間報告
  - 重大事項公告
  - 董事會議事録
  - 関係企業情報
- **データ形式**: HTML、PDF、CSV
- **言語**: 中国語（繁体字）
- **費用**: 完全無料

**財務データ抽出手順**:
1. https://mops.twse.com.tw/mops/web/index にアクセス
2. メニュー: 財務報表 > 採IFRSs財務報表 > 資產負債表
3. 企業コード入力してダウンロード

#### **中華民國統計資訊網**
- **URL**: https://www.stat.gov.tw/
- **英語版**: https://eng.stat.gov.tw/
- **内容**:
  - 工商普查（工商業センサス）
  - GDP統計
  - 産業別統計
- **データ形式**: Excel、CSV
- **費用**: 完全無料

### 4.2 台湾中央銀行

#### **中央銀行経済統計**
- **URL**: https://www.cbc.gov.tw/tw/mp-1.html
- **英語版**: https://www.cbc.gov.tw/en/mp-1.html
- **内容**:
  - 金融統計
  - 企業融資データ
  - 物価指数
- **費用**: 完全無料

---

## 5. シンガポール

### 5.1 証券取引所・政府データ

#### **シンガポール証券取引所（SGX）**
- **URL**: https://www.sgx.com/
- **内容**:
  - 上場企業株価データ
  - 企業公告
  - 財務報告
- **データ形式**: CSV、Excel、PDF
- **費用**: 基本データ無料（リアルタイムは有料）

**データダウンロード**:
- 株価データ: https://www.sgx.com/securities/securities-prices
- 企業情報: https://www.sgx.com/securities/company-announcements

#### **ACRA（会計・企業規制庁）BizFile**
- **URL**: https://www.acra.gov.sg/
- **内容**:
  - 企業登記情報
  - 財務諸表（公開企業）
  - 役員情報
- **費用**: 基本情報無料、詳細レポートは有料（S$20程度）

#### **シンガポール統計局（SingStat）**
- **URL**: https://www.singstat.gov.sg/
- **内容**:
  - 企業統計
  - GDP統計
  - 産業別売上高
  - 雇用統計
- **データ形式**: Excel、CSV、API
- **API**: あり（SingStat Table Builder API）
- **費用**: 完全無料

**データポータル**:
- https://tablebuilder.singstat.gov.sg/

---

## 6. ベトナム

### 6.1 証券取引所・政府データ

#### **ホーチミン証券取引所（HOSE）**
- **URL**: https://www.hsx.vn/
- **英語版**: https://www.hsx.vn/English
- **内容**:
  - 上場企業株価データ
  - 財務諸表
  - 企業公告
- **データ形式**: Excel、PDF
- **費用**: 完全無料

**データダウンロード**:
- 市場データ: https://www.hsx.vn/Modules/Listed/Web/SymbolList
- 財務報告: 各企業ページから個別ダウンロード

#### **ハノイ証券取引所（HNX）**
- **URL**: https://www.hnx.vn/
- **英語版**: https://www.hnx.vn/en-gb/
- **内容**:
  - 上場企業データ
  - 財務情報
- **費用**: 完全無料

#### **ベトナム統計総局（GSO）**
- **URL**: https://www.gso.gov.vn/
- **英語版**: https://www.gso.gov.vn/en/homepage/
- **内容**:
  - 企業センサス
  - 産業統計
  - GDP統計
- **データ形式**: Excel
- **費用**: 完全無料

#### **FiinTrade（ベトナム金融データプロバイダー）**
- **URL**: https://fiintrade.vn/
- **内容**:
  - 株価データAPI
  - 財務データ
- **費用**: 一部無料（登録必要）、詳細データは有料

---

## 7. マレーシア

### 7.1 証券取引所・政府データ

#### **マレーシア証券取引所（Bursa Malaysia）**
- **URL**: https://www.bursamalaysia.com/
- **内容**:
  - 上場企業株価データ
  - 財務諸表
  - 企業公告
- **データ形式**: PDF、Excel
- **費用**: 基本データ無料

**データ所在**:
- 市場データ: https://www.bursamalaysia.com/market_information/equities_prices
- 企業情報: https://www.bursamalaysia.com/listing/company-listing

#### **マレーシア企業委員会（SSM）**
- **URL**: https://www.ssm.com.my/
- **内容**:
  - 企業登記情報
  - 財務諸表（提出義務企業）
- **費用**: 一部有料（RM数十程度）

#### **マレーシア統計局（DOSM）**
- **URL**: https://www.dosm.gov.my/
- **英語版**: https://www.dosm.gov.my/v1/index.php?r=column/ctheme&menu_id=L0pheU43NWJwRWVSZklWdzQ4TlhUUT09&bul_id=
- **内容**:
  - 経済センサス
  - GDP統計
  - 産業統計
- **データ形式**: Excel、PDF
- **費用**: 完全無料

**OpenDOSM（オープンデータポータル）**:
- **URL**: https://open.dosm.gov.my/
- **内容**: マレーシア統計局データのAPIアクセス
- **API**: あり
- **費用**: 完全無料

---

## 8. タイ

### 8.1 証券取引所・政府データ

#### **タイ証券取引所（SET）**
- **URL**: https://www.set.or.th/
- **英語版**: https://www.set.or.th/en/
- **内容**:
  - SET・mai上場企業データ
  - 株価データ
  - 財務諸表
  - コーポレートガバナンス情報
- **データ形式**: Excel、PDF
- **費用**: 完全無料

**データダウンロード**:
- 株価: https://www.set.or.th/en/market/product/stock/quote/price/historical
- 財務データ: https://www.set.or.th/en/market/product/stock/quote/financials/financials-highlight

#### **タイ証券取引委員会（SEC Thailand）**
- **URL**: https://www.sec.or.th/
- **英語版**: https://www.sec.or.th/EN/Pages/HOME.aspx
- **内容**:
  - 上場企業の法定開示書類
  - 年次報告書（56-1 One Report）
  - 財務諸表
- **費用**: 完全無料

#### **タイ国家統計局（NSO）**
- **URL**: http://www.nso.go.th/
- **英語版**: http://statbbi.nso.go.th/staticreport/page/sector/en/index.aspx
- **内容**:
  - 企業統計
  - 産業統計
  - GDP統計
- **データ形式**: Excel
- **費用**: 完全無料

---

## 9. インドネシア

### 9.1 証券取引所・政府データ

#### **インドネシア証券取引所（IDX）**
- **URL**: https://www.idx.co.id/
- **英語版**: https://www.idx.co.id/en/
- **内容**:
  - 上場企業株価データ
  - 財務諸表
  - 企業公告
- **データ形式**: Excel、PDF
- **費用**: 完全無料

**データダウンロード**:
- 株価: https://www.idx.co.id/en/market-data/trading-data/stock/
- 財務報告: https://www.idx.co.id/en/listed-companies/financial-statements/

#### **インドネシア統計局（BPS）**
- **URL**: https://www.bps.go.id/
- **英語版**: https://www.bps.go.id/en
- **内容**:
  - 経済センサス
  - 大中規模企業統計
  - 製造業統計
- **データ形式**: Excel、PDF
- **費用**: 完全無料

---

## 10. フィリピン

### 10.1 証券取引所・政府データ

#### **フィリピン証券取引所（PSE）**
- **URL**: https://www.pse.com.ph/
- **内容**:
  - 上場企業株価データ
  - 財務諸表
  - 企業開示
- **データ形式**: PDF、Excel
- **費用**: 完全無料

**データダウンロード**:
- 株価: https://www.pse.com.ph/stockMarket/home.html
- 企業情報: https://edge.pse.com.ph/

#### **フィリピン統計庁（PSA）**
- **URL**: https://psa.gov.ph/
- **内容**:
  - 国民経済計算
  - 企業統計
- **データ形式**: Excel
- **費用**: 完全無料

---

## 11. 香港

### 11.1 証券取引所・政府データ

#### **香港証券取引所（HKEX）**
- **URL**: https://www.hkex.com.hk/
- **英語版**: https://www.hkex.com.hk/?sc_lang=en
- **内容**:
  - 上場企業株価データ
  - 財務諸表
  - 公告
- **データ形式**: Excel、PDF、API
- **費用**: 基本データ無料

**データダウンロード**:
- 株価: https://www.hkex.com.hk/Market-Data/Statistics/Consolidated-Reports/Securities-Statistics-Archive/Trading_Statistics?sc_lang=en
- 企業情報: https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities?sc_lang=en

#### **HKEXnews（開示プラットフォーム）**
- **URL**: https://www.hkexnews.hk/
- **内容**:
  - 上場企業の法定開示書類
  - 年報・中間報告
  - 公告
- **データ形式**: PDF、HTML
- **費用**: 完全無料

#### **香港政府統計処**
- **URL**: https://www.censtatd.gov.hk/
- **英語版**: https://www.censtatd.gov.hk/en/
- **内容**:
  - GDP統計
  - 企業統計
  - 対外貿易統計
- **データ形式**: Excel
- **費用**: 完全無料

---

## 12. グローバル・国際機関データソース

### 12.1 世界銀行グループ

#### **World Bank Open Data**
- **URL**: https://data.worldbank.org/
- **内容**:
  - 200以上の国・地域のマクロ経済指標
  - GDP、インフレ率、貿易統計
  - ガバナンス指標
  - ビジネス環境指標（Doing Business - 2021年以降停止）
- **データ形式**: CSV、Excel、API
- **API**: あり（World Bank API - https://datahelpdesk.worldbank.org/knowledgebase/articles/889392）
- **費用**: 完全無料

**Pythonでの利用**:
```python
import wbgapi as wb

# GDP per capita data
df = wb.data.DataFrame('NY.GDP.PCAP.CD', ['JPN', 'KOR', 'CHN', 'TWN'], 
                        range(2000, 2024))
print(df)
```

#### **World Bank Enterprise Surveys**
- **URL**: https://www.enterprisesurveys.org/
- **内容**:
  - 企業レベルの調査データ
  - ビジネス環境、インフラ、ファイナンス
  - 150以上の国、19万社以上
- **データ形式**: Stata、CSV、Excel
- **費用**: 完全無料（登録必要）

**対象アジア諸国**:
- 中国、インドネシア、フィリピン、ベトナム、マレーシア、タイ等

### 12.2 国際通貨基金（IMF）

#### **IMF Data**
- **URL**: https://data.imf.org/
- **内容**:
  - 国際収支統計
  - 財政統計
  - 金融統計
  - 為替レート
- **データ形式**: CSV、Excel、API
- **API**: あり（IMF Data API）
- **費用**: 完全無料

### 12.3 OECD

#### **OECD.Stat**
- **URL**: https://stats.oecd.org/
- **内容**:
  - OECD加盟国・パートナー国の経済統計
  - 産業統計
  - 貿易統計
  - R&D統計
- **データ形式**: CSV、Excel、API
- **API**: あり（OECD.Stat API）
- **費用**: 完全無料

**対象アジア諸国**:
- 日本、韓国、中国（パートナー）、インドネシア（パートナー）

### 12.4 アジア開発銀行（ADB）

#### **ADB Data Library**
- **URL**: https://data.adb.org/
- **内容**:
  - アジア太平洋地域の経済・社会指標
  - インフラ投資データ
  - 貧困統計
- **データ形式**: CSV、Excel
- **費用**: 完全無料

### 12.5 UN Comtrade（国連商品貿易統計）

#### **UN Comtrade Database**
- **URL**: https://comtradeplus.un.org/
- **内容**:
  - 世界200カ国の貿易統計（1962年～）
  - 輸出入額、品目別データ
  - 相手国別統計
- **データ形式**: CSV、Excel、API
- **API**: あり（UN Comtrade API）
- **費用**: 完全無料（APIは登録必要）

### 12.6 WTO（世界貿易機関）

#### **WTO Statistics Database**
- **URL**: https://stats.wto.org/
- **内容**:
  - 国際貿易統計
  - 関税統計
  - サービス貿易
- **データ形式**: CSV、Excel
- **費用**: 完全無料

### 12.7 グローバル・イノベーション

#### **WIPO IP Statistics**
- **URL**: https://www.wipo.int/ipstats/en/
- **提供元**: 世界知的所有権機関
- **内容**:
  - グローバル特許出願統計
  - 国別・技術分野別統計
  - PCT国際出願データ
- **データ形式**: Excel、CSV
- **費用**: 完全無料

#### **PATSTAT（欧州特許庁）**
- **URL**: https://www.epo.org/en/searching-for-patents/business/patstat
- **内容**:
  - 世界90以上の特許庁データ
  - 特許引用ネットワーク
- **費用**: 有料（ただし学術機関割引あり）

### 12.8 ESG・サステナビリティ

#### **CDP Open Data**
- **URL**: https://data.cdp.net/
- **内容**:
  - 13,000社以上の気候変動データ
  - 水資源データ
  - 森林データ
- **データ形式**: CSV、Excel
- **費用**: 研究者向け無料（申請必要）

**対象アジア企業**:
- 日本、韓国、中国、台湾、シンガポール等の大手企業

#### **Global Reporting Initiative (GRI) Database**
- **URL**: https://database.globalreporting.org/
- **内容**:
  - 企業のサステナビリティレポート
  - GRI基準準拠レポート
- **データ形式**: PDF（個別ダウンロード）
- **費用**: 完全無料

---

## 13. クロスカントリー研究のための統合戦略

### 13.1 企業識別子の統一

**課題**: 各国・各データベースで異なる企業識別子が使用されている

**ソリューション**:

1. **LEI（Legal Entity Identifier）の活用**
   - **URL**: https://www.gleif.org/
   - グローバル企業識別コード
   - 200万以上の企業が登録
   - 無料で検索・ダウンロード可能

2. **企業名+登記番号によるマッチング**
   - 各国の企業登記番号を取得
   - 名称の標準化（Inc., Ltd., Corp.等を除去）
   - ファジーマッチングの活用

3. **市場コード（Ticker + Exchange）の利用**
   - 例: 2330.TW（台積電、台湾）、005930.KS（サムスン、韓国）
   - Yahoo Finance、Google Financeで相互参照可能

### 13.2 財務データの標準化

**課題**: 会計基準の違い（US GAAP、IFRS、各国GAAP）

**対応策**:

1. **比率分析を重視**
   - ROA、ROE、レバレッジ等は会計基準の影響を受けにくい
   - 絶対額ではなく相対指標を使用

2. **業種内比較**
   - 同一業種内での比較分析
   - 業種固有の特性を考慮

3. **マクロ調整**
   - 購買力平価（PPP）での調整
   - GDPデフレーターによる実質化

### 13.3 為替レート変換

**無料データソース**:

#### **FRED（Federal Reserve Economic Data）**
- **URL**: https://fred.stlouisfed.org/
- **内容**: 主要通貨の日次・月次・年次為替レート
- **API**: あり（FRED API）
- **費用**: 完全無料

**Pythonでの利用**:
```python
from fredapi import Fred

fred = Fred(api_key='your_api_key')
# JPY/USD exchange rate
jpy_usd = fred.get_series('DEXJPUS')
```

#### **ECB（欧州中央銀行）為替レート**
- **URL**: https://www.ecb.europa.eu/stats/policy_and_exchange_rates/
- **API**: あり（ECB SDW API）
- **費用**: 完全無料

### 13.4 データ統合の実践例

**例: 日韓台中の製造業比較研究**

```python
import pandas as pd
import requests

# 1. 各国データの取得
# 日本: e-Stat API
japan_data = get_japan_estat_data()

# 韓国: DART API
korea_data = get_korea_dart_data()

# 台湾: TWSE/MOPS
taiwan_data = get_taiwan_mops_data()

# 中国: Tushare
china_data = get_china_tushare_data()

# 2. 業種分類の統一（ISIC Rev.4に変換）
japan_data['isic'] = convert_jsic_to_isic(japan_data['jsic'])
korea_data['isic'] = convert_ksic_to_isic(korea_data['ksic'])
# ...

# 3. 財務変数の標準化
for df in [japan_data, korea_data, taiwan_data, china_data]:
    df['roa'] = df['net_income'] / df['total_assets']
    df['leverage'] = df['total_debt'] / df['total_assets']

# 4. 為替調整（全てUSDに統一）
japan_data['sales_usd'] = japan_data['sales_jpy'] / jpy_usd_rate
korea_data['sales_usd'] = korea_data['sales_krw'] / krw_usd_rate
# ...

# 5. データ結合
combined_data = pd.concat([
    japan_data[['firm_id', 'year', 'country', 'isic', 'roa', 'leverage', 'sales_usd']],
    korea_data[['firm_id', 'year', 'country', 'isic', 'roa', 'leverage', 'sales_usd']],
    taiwan_data[['firm_id', 'year', 'country', 'isic', 'roa', 'leverage', 'sales_usd']],
    china_data[['firm_id', 'year', 'country', 'isic', 'roa', 'leverage', 'sales_usd']]
], ignore_index=True)
```

---

## 14. 無料データを使った研究テーマ例

### 14.1 コーポレートガバナンス研究

**テーマ**: 「東アジアにおける取締役会構成と企業パフォーマンス」

**使用データ**:
- **日本**: EDINET（有価証券報告書から取締役会情報抽出）
- **韓国**: DART（사업보고서から取締役情報）
- **台湾**: MOPS（年報から董事會資料）
- **財務データ**: 各国証券取引所の公開データ

**分析可能な変数**:
- 独立取締役比率
- 取締役会規模
- 女性取締役比率
- ROA、ROE、Tobin's Q

**推定費用**: ¥0（完全無料）

### 14.2 イノベーション研究

**テーマ**: 「アジア企業の特許活動と市場パフォーマンス」

**使用データ**:
- **特許**: 
  - 日本: J-PlatPat
  - 韓国: KIPRIS（https://www.kipris.or.kr/）
  - 中国: CNIPA（https://www.cnipa.gov.cn/）
  - グローバル: WIPO PATSTAT Online（無料版）
- **財務**: 各国証券取引所データ
- **R&D支出**: 財務諸表から抽出

**分析可能な変数**:
- 特許出願数、取得数
- 特許引用数
- 技術分野多様性
- R&D強度

**推定費用**: ¥0（完全無料）

### 14.3 ESG研究

**テーマ**: 「ASEAN企業の環境開示と資本コスト」

**使用データ**:
- **ESG開示**: 各企業のサステナビリティレポート（企業ウェブサイト、GRIデータベース）
- **財務**: ASEAN各国証券取引所データ
- **資本コスト**: 株価データから計算（CAPM）

**分析可能な変数**:
- 環境開示スコア（自作）
- GHG排出量（開示企業のみ）
- Beta、資本コスト
- 業種、企業規模

**推定費用**: ¥0（完全無料、ただし手作業での開示スコアリング必要）

### 14.4 国際化研究

**テーマ**: 「東アジア製造業の海外展開パターン」

**使用データ**:
- **親子会社関係**: 
  - 日本: e-Stat 企業活動基本調査、EDINET
  - 韓国: DART
  - 台湾: MOPS
- **貿易データ**: UN Comtrade
- **FDI**: 各国中央銀行・統計局

**分析可能な変数**:
- 海外子会社数
- 海外売上高比率
- 地域別展開パターン
- 輸出依存度

**推定費用**: ¥0（完全無料）

### 14.5 企業再編研究

**テーマ**: 「アジア新興国のM&A活動の決定要因」

**使用データ**:
- **M&A**: 各国証券取引所の重大事項公告
  - シンガポール: SGX announcements
  - マレーシア: Bursa Malaysia announcements
  - タイ: SET announcements
- **財務**: 証券取引所データ
- **マクロ**: World Bank、IMF

**分析可能な変数**:
- M&A件数・金額
- 買収企業・被買収企業の財務指標
- 業種、国内/クロスボーダー区分

**推定費用**: ¥0（完全無料）

---

## 15. データ取得の実践的ヒント

### 15.1 APIキー取得手順（主要サービス）

| サービス | 登録URL | 承認時間 | 利用制限 |
|---------|---------|---------|---------|
| EDINET API | https://disclosure2.edinet-fsa.go.jp/ | 即時 | なし |
| Open DART (韓国) | https://opendart.fss.or.kr/ | 1-2日 | 10,000回/日 |
| Tushare (中国) | https://tushare.pro/register | 即時 | ポイント制 |
| World Bank API | https://datahelpdesk.worldbank.org/ | 不要 | なし |
| FRED API | https://fred.stlouisfed.org/docs/api/api_key.html | 即時 | なし |

### 15.2 大量データ取得時の注意点

1. **レート制限の遵守**
   - 各APIのレート制限を確認
   - 必要に応じてtime.sleep()を挿入
   - 並列処理は慎重に

2. **robots.txtの確認**
   - Webスクレイピング前に必ずチェック
   - 禁止されている場合は代替手段を探す

3. **利用規約の遵守**
   - 商用利用の可否を確認
   - データ再配布の制限に注意
   - 適切な引用を行う

### 15.3 データ品質チェックリスト

- [ ] 欠損値の割合は許容範囲か？（目安: 主要変数で<20%）
- [ ] 財務数値が異常値を含んでいないか？（例: ROA>100%）
- [ ] 時系列データに不自然な断絶がないか？
- [ ] 複数ソース統合時のマッチング率は十分か？（目安: >80%）
- [ ] 為替換算は適切な日付のレートを使用しているか？
- [ ] 業種分類は統一されているか？

---

## 16. 推奨データ収集ツール

### 16.1 Pythonライブラリ

```bash
# データ取得
pip install requests pandas openpyxl
pip install fredapi wbgapi  # World Bank, FRED
pip install tushare akshare  # 中国市場データ

# データ処理
pip install numpy scipy statsmodels

# Webスクレイピング（必要な場合）
pip install beautifulsoup4 selenium

# 財務分析
pip install yfinance  # Yahoo Financeから株価取得
```

### 16.2 便利なツール

#### **Yahoo Finance（yfinance）**
- アジア証券取引所対応
- 無料で株価データ取得可能

```python
import yfinance as yf

# サムスン電子（韓国）
samsung = yf.Ticker("005930.KS")
hist = samsung.history(period="1y")

# トヨタ（日本）
toyota = yf.Ticker("7203.T")
info = toyota.info
```

**対応取引所記号**:
- 日本: .T（東証）
- 韓国: .KS（KOSPI）、.KQ（KOSDAQ）
- 台湾: .TW（TWSE）、.TWO（TPEx）
- 香港: .HK（HKEX）

---

## 17. データ取得のロードマップ（4週間プラン）

### Week 1: 環境構築・データソース調査
- [ ] Python環境セットアップ
- [ ] 必要なライブラリインストール
- [ ] 各国APIキー取得（DART、Tushare等）
- [ ] データソースの利用規約確認

### Week 2: データ収集スクリプト作成
- [ ] 単一国データ取得スクリプト作成
- [ ] エラーハンドリング実装
- [ ] 小サンプルでテスト実行
- [ ] データ保存形式の決定（CSV、Parquet等）

### Week 3: データクリーニング・統合
- [ ] 欠損値処理
- [ ] 異常値検出・処理
- [ ] 業種分類統一
- [ ] 為替換算（必要な場合）
- [ ] データ品質チェック

### Week 4: 最終データセット作成
- [ ] 全データソース統合
- [ ] パネル構造確認
- [ ] 変数構築（ROA、レバレッジ等）
- [ ] データディクショナリ作成
- [ ] 記述統計量の確認

---

## 18. よくある質問（FAQ）

### Q1: 有料データベースなしで査読論文は書けますか？

**A**: はい、可能です。特にアジア地域研究では、政府統計と証券取引所の公開データで十分なクオリティの研究が可能です。実際、近年のトップジャーナルでも無料データソースを使った研究が増えています。

**成功のポイント**:
- 独自のデータ収集・処理プロセスを詳細に記述
- 複数の無料ソースを組み合わせて独自性を出す
- データの限界を正直に記述し、ロバストネスチェックを実施

### Q2: データ取得に最も時間がかかるのはどの部分ですか？

**A**: 経験上、以下の順で時間がかかります：

1. **企業マッチング**（異なるデータソース間の企業識別）: 全体の30-40%
2. **データクリーニング**（欠損値、異常値処理）: 20-30%
3. **実際のダウンロード**: 15-20%
4. **業種分類統一**: 10-15%
5. **文書化**: 10-15%

### Q3: APIの利用制限に引っかかった場合は？

**A**: 対処法：

1. **レート制限の場合**: スクリプトにsleep()を追加して間隔を空ける
2. **日次制限の場合**: 複数日に分けてダウンロード
3. **総量制限の場合**: サンプル期間・対象企業を絞る、または代替データソースを探す

### Q4: 中国語・韓国語のデータをどう扱えば良いですか？

**A**: 
- **機械翻訳**: Google Translate API（有料だが低コスト）
- **英語版データ**: 多くの大手企業は英語版の財務報告も公開
- **コラボレーション**: 現地の研究者と共同研究を検討

**数値データは言語に依存しない**ので、変数名さえ理解できればOK。

### Q5: データの更新はどのくらいの頻度で行うべきですか？

**A**: 
- **年次財務データ**: 年1回（会計年度終了後3-4ヶ月）
- **株価データ**: 研究ニーズに応じて（日次、週次、月次）
- **マクロデータ**: 四半期または年次

**ポイント**: 最初に完全なデータセットを構築しておけば、追加年度のデータ追加は比較的容易。

---

## 19. さらなる学習リソース

### オンラインコース（無料）

1. **Coursera: Financial Markets (Yale University)**
   - URL: https://www.coursera.org/learn/financial-markets-global
   - 金融市場の基礎理解

2. **edX: Data Science for Business (MIT)**
   - URL: https://www.edx.org/
   - データサイエンス手法の学習

### 推奨書籍

1. **"Empirical Corporate Finance"** by Ghosh & Hilary
   - 実証コーポレートファイナンスの方法論

2. **"Panel Data Econometrics"** by Baltagi
   - パネルデータ分析の標準テキスト

### オープンソースプロジェクト

1. **FinanceDatabase (GitHub)**
   - URL: https://github.com/JerBouma/FinanceDatabase
   - 20,000以上の金融商品データ

2. **awesome-quant (GitHub)**
   - URL: https://github.com/wilsonfreitas/awesome-quant
   - 金融データソースのキュレーションリスト

---

## 20. まとめ：低コスト研究の成功戦略

### ✅ Do's（すべきこと）

1. **早期開始**: データアクセス取得に時間がかかる場合がある
2. **小サンプルテスト**: 全データダウンロード前に手法を検証
3. **文書化の徹底**: 再現性のため、すべてのステップを記録
4. **バックアップ**: 3-2-1ルール（3コピー、2種類のメディア、1つはオフサイト）
5. **コミュニティ活用**: GitHub、研究者フォーラムで情報交換

### ❌ Don'ts（避けるべきこと）

1. **利用規約違反**: 法的リスクを冒さない
2. **過度のスクレイピング**: サーバーに負荷をかけない
3. **データ検証の省略**: 異常値を見逃すと研究全体が無効に
4. **単一データソース依存**: 複数ソースでクロスバリデーション
5. **文書化の後回し**: 後から思い出すのは困難

### 💡 最重要ポイント

**無料データでも世界トップレベルの研究は可能です。**

重要なのは：
- データの質
- 独創的な研究設計
- 厳密な分析手法
- 透明性のある文書化

このガイドが、予算制約のある研究者の皆様の一助となれば幸いです。

---

**最終更新**: 2025-10-31  
**バージョン**: 1.0  
**ライセンス**: このガイドは教育・研究目的で自由に利用可能です。

#無料データソース #アジア企業研究 #低コスト研究 #実証研究 #データ収集