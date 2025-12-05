---
name: research-data-hub
description: |
  研究データの収集・管理・品質保証のための統合ハブ。以下の機能を包括：
  (1) データ収集ワークフロー管理
  (2) 企業データ収集（日本・グローバル）
  (3) 米国企業分析（SEC EDGAR、World Bank、IMF統合）
  (4) データ品質保証・検証
  トリガー：「データ収集」「企業データ」「SEC EDGAR」「財務データ」「データベース」
---

# Research Data Hub - 研究データ収集・管理統合ハブ

## 概要

学術研究に必要なデータの収集、管理、品質保証を包括的に支援する統合システムです。企業財務データ、ガバナンスデータ、マクロ経済データなど、多様なソースからのデータを効率的に収集・統合します。

**統合元スキル**：
- research-data-collection
- corporate-research-data-hub
- us-corporate-analytics

## When to Use This Skill

以下の場合にこのスキルを使用：

- 研究用データの収集計画立案
- 企業財務・市場データの取得
- 複数データソースの統合
- データ品質の検証・保証
- SEC EDGARからの米国企業データ取得

**トリガーキーワード**：
- 「データ収集」「データ取得」「データベース」
- 「企業データ」「財務データ」「市場データ」
- 「SEC EDGAR」「Compustat」「WRDS」
- 「データ品質」「データ検証」

---

# Part 1: データ収集ワークフロー

## 1.1 研究データ収集プロセス

```
[Phase 1: 要件定義]
├── 研究クエスチョンの明確化
├── 必要変数の特定
├── 時間範囲・地理範囲の決定
└── データソースの候補リスト作成

[Phase 2: ソース評価]
├── 各ソースのカバレッジ確認
├── データ品質の事前評価
├── コスト・アクセス可能性の確認
└── 最適ソースの選定

[Phase 3: データ取得]
├── アクセス権の確保（契約、申請等）
├── クエリ設計・データ抽出
├── ダウンロード・保存
└── バックアップ作成

[Phase 4: 品質検証]
├── 欠損値の確認・処理
├── 外れ値の検出・処理
├── クロスチェック（複数ソース）
└── ドキュメント作成

[Phase 5: 統合・整備]
├── 変数の標準化
├── マッチング（企業ID等）
├── パネルデータ構築
└── 最終データセット作成
```

## 1.2 データ要件定義テンプレート

```
研究プロジェクト: [プロジェクト名]
研究クエスチョン: [RQ]
分析単位: [企業/産業/国/etc.]

必要変数：
| 変数名 | 定義 | 測定 | 優先データソース |
|--------|------|------|------------------|
| [DV] | | | |
| [IV1] | | | |
| [Control] | | | |

サンプル要件：
- 地理的範囲: [国/地域]
- 産業範囲: [SIC/NAICS]
- 時間範囲: [開始年-終了年]
- 最小サンプルサイズ: [N]

データ制約：
- 予算: [金額/無料のみ]
- アクセス: [WRDS有/無]
- 期限: [日付]
```

---

# Part 2: 主要データソース

## 2.1 企業財務データ

### 北米（米国・カナダ）

**Compustat North America（WRDS経由）**
```
カバレッジ：米国・カナダ上場企業 20,000社以上
期間：1950年代〜現在
アクセス：大学WRDS契約

主要テーブル：
- comp.funda：年次財務データ
- comp.fundaq：四半期財務データ
- comp.seg_annual：セグメントデータ
- comp.co_hdr：企業ヘッダー情報

主要変数：
- at：総資産
- sale：売上高
- ni：純利益
- xrd：R&D支出
- emp：従業員数
```

**CRSP（株式市場データ）**
```
カバレッジ：米国株式市場（全取引所）
期間：1926年〜現在
アクセス：WRDS経由

用途：
- 株価リターン計算
- 市場価値（Tobin's Q）
- イベントスタディ
- リスク指標（Beta、Volatility）
```

### 日本

**NEEDS-FinancialQUEST（日経）**
```
カバレッジ：日本上場企業3,800社以上
期間：1950年代〜現在

特徴：
- 日本会計基準対応
- 系列データ
- 株式持ち合いデータ
```

**eol（日本ユニシス）**
```
カバレッジ：日本企業（上場・非上場）
特徴：
- 有価証券報告書データ
- セグメント情報
```

### グローバル

**Worldscope（Refinitiv）**
```
カバレッジ：70カ国、70,000社以上
特徴：標準化された財務データ
用途：国際比較研究
```

**Orbis（Bureau van Dijk）**
```
カバレッジ：4億社以上（上場・非上場）
特徴：
- 所有構造データ
- 非上場企業データ
- 欧州に強い
```

## 2.2 SEC EDGARデータ

### 基本情報
```
URL: https://www.sec.gov/cgi-bin/browse-edgar
アクセス：無料（APIあり）
レート制限：10リクエスト/秒

対応書類：
| 書類 | 内容 | 用途 |
|------|------|------|
| 10-K | 年次報告書 | 財務データ、リスク開示 |
| 10-Q | 四半期報告書 | 四半期財務 |
| 8-K | 臨時報告書 | イベント検出（M&A等） |
| DEF 14A | 委任状説明書 | ガバナンスデータ |
| Form 4 | 内部者取引 | インサイダー分析 |
```

### データ取得スクリプト例

```python
import requests
import time

def fetch_10k(cik, year):
    """10-K年次報告書の取得"""
    base_url = "https://www.sec.gov/cgi-bin/browse-edgar"
    params = {
        "action": "getcompany",
        "CIK": cik,
        "type": "10-K",
        "dateb": f"{year}1231",
        "owner": "include",
        "count": "1",
        "output": "atom"
    }

    headers = {
        "User-Agent": "Research Bot (your-email@university.edu)"
    }

    response = requests.get(base_url, params=params, headers=headers)
    time.sleep(0.1)  # Rate limiting

    return response.text
```

## 2.3 イノベーション・特許データ

**USPTO PatentsView（無料）**
```
URL: https://patentsview.org/
カバレッジ：米国特許全件（1976〜）

変数例：
- 特許件数
- 被引用数
- IPC分類
- 発明者・出願人情報

データ取得：
- Bulk Download（全データ）
- API（選択的取得）
```

**PATSTAT（EPO）**
```
カバレッジ：グローバル特許（90カ国以上）
アクセス：有料（年間約€1,500）
```

## 2.4 マクロ経済データ

**World Bank Open Data（無料）**
```
URL: https://api.worldbank.org/v2/
主要指標：
- NY.GDP.MKTP.CD：GDP（名目）
- NY.GDP.MKTP.KD.ZG：GDP成長率
- FP.CPI.TOTL.ZG：インフレ率
- IC.BUS.EASE.XQ：Doing Business Index
```

**IMF Data（無料）**
```
URL: https://www.imf.org/external/datamapper/api/v1/
主要データ：
- 国際金融統計（IFS）
- 為替レート
- 国際収支
```

## 2.5 ESG・サステナビリティデータ

**CDP（申請で無料）**
```
URL: https://www.cdp.net/en/academic-research
カバレッジ：13,000社以上
データ：炭素排出量、気候戦略
```

**GRI Database（無料）**
```
URL: https://database.globalreporting.org/
カバレッジ：60,000+サステナビリティ報告書
```

---

# Part 3: データ品質保証

## 3.1 欠損値処理

### 欠損パターンの確認
```python
import pandas as pd
import missingno as msno

# 欠損パターンの可視化
msno.matrix(df)

# 欠損率の計算
missing_rate = df.isnull().sum() / len(df) * 100
```

### 処理方法
```
1. 完全ケース分析（Listwise deletion）
   - 欠損率 < 5%の場合に適用

2. 単一代入（Mean/Median imputation）
   - 探索的分析向け
   - ロバストネスチェック用

3. 多重代入（Multiple imputation）
   - 欠損がランダム（MAR）の場合
   - mice、Amelia IIパッケージ使用

4. 除外基準の設定
   - 主要変数の欠損 → 除外
   - コントロール変数の欠損 → 代入検討
```

## 3.2 外れ値処理

### 検出方法
```python
# IQR法
Q1 = df['var'].quantile(0.25)
Q3 = df['var'].quantile(0.75)
IQR = Q3 - Q1
outliers = (df['var'] < Q1 - 1.5*IQR) | (df['var'] > Q3 + 1.5*IQR)

# Z-score法
from scipy import stats
z_scores = stats.zscore(df['var'])
outliers = abs(z_scores) > 3
```

### 処理方法
```
1. Winsorization（推奨）
   - 1%/99%または5%/95%でトリミング
   - 情報を保持しつつ影響を軽減

2. Truncation
   - 外れ値を除外
   - サンプルサイズ減少に注意

3. ロバスト推定
   - 外れ値に強い推定量を使用
   - Huber推定、中央値回帰
```

## 3.3 データ検証チェックリスト

```
[ ] 変数の記述統計確認
    - 最小値、最大値の妥当性
    - 平均値、中央値の比較
    - 分布の形状確認

[ ] 欠損値の確認
    - 欠損率の計算
    - 欠損パターンの分析
    - 欠損の非ランダム性チェック

[ ] 外れ値の確認
    - 外れ値の特定
    - 外れ値の原因調査
    - 処理方法の決定

[ ] 一貫性チェック
    - 会計恒等式の確認（資産=負債+資本）
    - 時系列の連続性
    - クロスセクションの整合性

[ ] クロスバリデーション
    - 複数ソース間での比較
    - 公表データとの照合
    - 異常値の原因特定
```

## 3.4 Benford's Law検定

```python
import numpy as np
from scipy.stats import chisquare

def benfords_law_test(data):
    """
    財務データの信頼性をBenford's Lawで検証
    """
    # 最初の桁を抽出
    first_digits = []
    for x in data:
        if x != 0 and not np.isnan(x):
            first_digit = int(str(abs(x))[0])
            first_digits.append(first_digit)

    # 観測頻度
    observed = np.bincount(first_digits, minlength=10)[1:]

    # 理論頻度（Benford's Law）
    n = len(first_digits)
    expected = [n * np.log10(1 + 1/d) for d in range(1, 10)]

    # カイ二乗検定
    stat, p_value = chisquare(observed, expected)

    return {
        'chi_square': stat,
        'p_value': p_value,
        'is_valid': p_value > 0.05  # p > 0.05 ならデータは信頼できる
    }
```

---

# Part 4: データ統合

## 4.1 企業マッチング

### 識別子の種類
```
| 識別子 | データベース | 特徴 |
|--------|--------------|------|
| GVKEY | Compustat | 6桁数字、最も一般的 |
| PERMNO | CRSP | 株式識別、分割対応 |
| CIK | SEC EDGAR | 10桁、SEC提出用 |
| CUSIP | 多数 | 9桁、債券・株式 |
| ISIN | 国際 | 12桁、国際標準 |
| Ticker | 多数 | 変更可能、要注意 |
```

### マッチング手順
```python
# Compustat-CRSP マッチング（CCM Linkage Table使用）
ccm_link = """
SELECT a.gvkey, a.permno, a.linkdt, a.linkenddt
FROM crsp.ccmxpf_lnkhist a
WHERE a.linktype IN ('LU', 'LC')
  AND a.linkprim IN ('P', 'C')
"""

# 企業名によるFuzzy Matching
from fuzzywuzzy import fuzz

def fuzzy_match(name1, name2, threshold=85):
    score = fuzz.ratio(name1.upper(), name2.upper())
    return score >= threshold
```

## 4.2 パネルデータ構築

```python
import pandas as pd

def create_panel(df, entity_id, time_id):
    """
    パネルデータの構築
    """
    # 重複の確認
    duplicates = df.duplicated(subset=[entity_id, time_id], keep=False)
    if duplicates.any():
        print(f"Warning: {duplicates.sum()} duplicates found")

    # インデックス設定
    panel = df.set_index([entity_id, time_id]).sort_index()

    # バランスパネルかチェック
    n_entities = panel.index.get_level_values(0).nunique()
    n_periods = panel.index.get_level_values(1).nunique()
    is_balanced = len(panel) == n_entities * n_periods

    print(f"Entities: {n_entities}")
    print(f"Periods: {n_periods}")
    print(f"Observations: {len(panel)}")
    print(f"Balanced: {is_balanced}")

    return panel
```

---

# Part 5: 起動コマンド

## データ収集計画モード
```
Research Data Hub起動

目的: データ収集計画
研究テーマ: [テーマ]
必要変数: [変数リスト]
地理範囲: [国/地域]
期間: [開始年-終了年]
予算: [金額]
```

## データ取得モード
```
Research Data Hub起動

目的: データ取得
データソース: [Compustat/SEC EDGAR/etc.]
対象企業: [条件]
期間: [年]
出力形式: [CSV/Stata/etc.]
```

## 品質検証モード
```
Research Data Hub起動

目的: 品質検証
対象データ: [ファイルパス]
検証項目: [欠損値/外れ値/Benford]
出力: [検証レポート]
```

---

## 連携スキル

| スキル名 | 役割 |
|----------|------|
| strategic-research-platform | 研究デザイン・統計分析 |
| academic-research-suite | 文献レビュー・論文執筆・引用管理 |
| document-design-suite | データ可視化・図表作成 |
| thinking-toolkit | 理論構築・批判的分析 |
| code-quality-guardian | データ検証・品質保証 |

---

**バージョン**: 1.0.0
**統合日**: 2025-11-28
**統合元**: research-data-collection, corporate-research-data-hub, us-corporate-analytics
