# Corporate Research Data Hub v2.0

企業経営の実証研究に特化した包括的データ収集・管理スキル

**Version 2.0 - Publication-Grade Research Ready**

## 🎯 v2.0の主要アップデート

- ✅ **Advanced Quality Assurance**: トップジャーナル基準の統計的品質保証
- ✅ **Research Checklist Manager**: 7フェーズの進捗管理システム
- ✅ **Data Lineage Tracker**: 完全な系譜追跡と再現性担保
- ✅ **Test Suite**: pytest based comprehensive testing
- ✅ **Docker Support**: 環境完全再現性
- ✅ **Enhanced Error Handling**: 本番環境対応のロバストなエラー処理

**🆕 アジア地域の無料・低コストデータソースを大幅拡充（11カ国・地域）**

---

## 📋 目次

1. [概要](#概要)
2. [🌟 新機能: 無料データソース](#新機能-無料データソース)
3. [主要機能](#主要機能)
4. [ディレクトリ構造](#ディレクトリ構造)
5. [クイックスタート](#クイックスタート)
6. [使用例](#使用例)
7. [データソース一覧](#データソース一覧)
8. [研究分野別ガイド](#研究分野別ガイド)
9. [トラブルシューティング](#トラブルシューティング)

---

## 概要

このスキルは、企業財務、戦略経営、コーポレートガバナンス、組織研究における実証研究のデータライフサイクル全体を管理します。

### 対象研究者

- ✅ **予算制約のある研究者**: 無料データソースで世界水準の研究が可能
- ✅ **アジア企業研究者**: 日本、韓国、中国、台湾、ASEAN諸国を完全カバー
- ✅ **博士課程・若手研究者**: 再現可能な研究プロセスの構築
- ✅ **実務家研究者**: 効率的なデータ収集と分析

---

## 🌟 新機能: 無料データソース

### アジア地域完全カバー

**11カ国・地域の無料データソースを詳細ガイド**:

| 国・地域 | 主要データソース | 取得可能データ | API |
|---------|----------------|-------------|-----|
| 🇯🇵 日本 | EDINET、JPX、e-Stat | 財務諸表、株価、統計 | ✓ |
| 🇰🇷 韓国 | Open DART、KRX | 財務諸表、株価、ガバナンス | ✓ |
| 🇨🇳 中国 | 巨潮資訊、Tushare | 財務諸表、株価 | ✓ |
| 🇹🇼 台湾 | TWSE、MOPS | 財務諸表、株価 | ✓ |
| 🇸🇬 シンガポール | SGX、SingStat | 株価、企業統計 | ✓ |
| 🇻🇳 ベトナム | HOSE、HNX | 株価、財務諸表 | - |
| 🇲🇾 マレーシア | Bursa Malaysia | 株価、財務諸表 | 部分 |
| 🇹🇭 タイ | SET | 株価、財務諸表 | - |
| 🇮🇩 インドネシア | IDX | 株価、財務諸表 | - |
| 🇵🇭 フィリピン | PSE | 株価、財務諸表 | - |
| 🇭🇰 香港 | HKEX、HKEXnews | 株価、財務諸表 | 部分 |

### グローバルデータソース

- 🌍 **World Bank**: 200カ国のマクロ経済指標
- 💱 **IMF**: 国際収支、為替レート
- 📊 **OECD**: 産業統計、R&D統計
- 🌱 **CDP**: ESG・サステナビリティデータ
- 📄 **完全無料**: すべて登録のみで利用可能

**詳細ガイド**: [FREE_LOW_COST_DATA_SOURCES.md](FREE_LOW_COST_DATA_SOURCES.md)

---

## 主要機能

### 1. データソース発見と評価
- **有料データベース**: Compustat、CRSP、ORBIS等（大学経由）
- **無料データソース**: 政府統計、証券取引所、国際機関
- 70以上のデータソースを詳細解説

### 2. パネルデータ構築
- 企業-年度観測値の構造化
- 複数データソースの統合
- サバイバルバイアスの処理
- 企業識別子の統一

### 3. 財務データ標準化
- 通貨単位の統一
- 会計恒等式の検証
- 異常値処理（ウィンソライズ）
- 業種分類の統一

### 4. 品質保証 (v2.0強化)
- **基本QA**: 自動化された品質チェック、パネル構造の検証
- **Advanced QA (NEW)**:
  - 多変量異常値検出（Mahalanobis、Isolation Forest、LOF）
  - Benford's Law テスト（不正検出）
  - 回帰ベース異常検出
  - 構造的ブレーク検出（Chow test）
  - 影響力観測値検出（Cook's distance）
  - サンプル選択バイアステスト
- **統計的検出力分析**: サンプルサイズ計算（t検定、回帰、パネル）
- HTML/Markdown形式の詳細レポート生成

### 5. 再現性担保 (v2.0新規)
- **Data Lineage Tracker**: データソースから最終データセットまでの完全な系譜記録
- **Environment Reproducibility**: Docker完全対応
- **Code Quality**: pytest ベーステストスイート（カバレッジ80%+目標）
- **Version Control**: 全変換処理のバージョン管理

### 6. プロジェクト管理 (v2.0新規)
- **Research Checklist Manager**: 7フェーズ28タスクの進捗管理
- **Progress Tracking**: リアルタイム進捗可視化
- **Markdown Export**: 進捗レポート自動生成
- 時系列一貫性の確認
- 包括的QAレポート生成

### 5. 実用的ツール
- **Pythonスクリプト**: すぐに使えるデータ収集・処理ツール
- **テンプレート**: データ収集計画、QAチェックリスト
- **サンプルプロジェクト**: 実践的な研究例

---

## ディレクトリ構造 (v2.0)

```
corporate-research-data-hub/
├── SKILL.md                              # メインスキルドキュメント（7段階ワークフロー）
├── README.md                             # このファイル
├── FREE_LOW_COST_DATA_SOURCES.md        # 無料データソース完全ガイド
├── Dockerfile                            # 🆕 v2.0: Docker環境定義
├── .dockerignore                         # 🆕 v2.0: Docker除外ファイル
├── requirements.txt                      # Python依存パッケージ
│
├── scripts/                              # 実行可能スクリプト
│   ├── asian_data_collectors.py         # アジアデータ収集（v2.0強化版）
│   ├── corporate_data_utils.py          # データ処理ユーティリティ
│   ├── data_quality_checker.py          # 🆕 v2.0: Advanced QA含む
│   ├── data_lineage_tracker.py          # 🆕 v2.0: データ系譜追跡
│   └── research_checklist_manager.py    # 🆕 v2.0: 進捗管理システム
│
├── tests/                                # 🆕 v2.0: テストスイート
│   ├── __init__.py
│   └── test_asian_data_collectors.py    # データ収集モジュールテスト
│
├── tutorials/                            # チュートリアル
│   └── complete_workflow_example.md     # 🆕 エンドツーエンド実例
│
├── templates/                            # テンプレート集
│   ├── data_collection_plan.md          # データ収集計画テンプレート
│   ├── quality_assurance_checklist.md   # 品質保証チェックリスト
│   └── sample_project_asian_roa.md      # サンプルプロジェクト
└── scripts/                              # Pythonスクリプト
    ├── corporate_data_utils.py          # 企業データ処理ユーティリティ
    └── asian_data_collectors.py         # 🆕 アジアデータ収集ツール
```

---

## クイックスタート

### 前提条件

**方法1: ローカル環境**
```bash
# Python 3.10以上推奨
python --version

# 依存パッケージインストール
pip install -r requirements.txt
```

**方法2: Docker環境（推奨・完全再現性）** 🆕 v2.0
```bash
# Dockerイメージビルド
docker build -t corporate-research-hub:2.0 .

# コンテナ起動
docker run -it -v $(pwd)/data:/workspace/data corporate-research-hub:2.0

# テスト実行
docker run corporate-research-hub:2.0 pytest tests/ -v
```

### 5分で始める

#### 1. スキルの起動

研究テーマを説明:
```
「日本と韓国の製造業における取締役会多様性と企業パフォーマンスの関係を研究したい」
```

#### 2. 無料データソースの確認

```bash
# FREE_LOW_COST_DATA_SOURCES.md を開く
# → 日本: EDINET API
# → 韓国: Open DART API
```

#### 3. APIキー取得（無料）

- **Open DART（韓国）**: https://opendart.fss.or.kr/
  - 登録 → メール認証 → APIキー即時発行
  
- **Tushare（中国、オプション）**: https://tushare.pro/register
  - 登録 → ポイント制（基本無料）

#### 4. データ収集開始

```python
# スクリプトをインポート
from scripts.asian_data_collectors import JapanDataCollector, KoreaDataCollector

# 日本データ
jp_collector = JapanDataCollector()
documents = jp_collector.get_edinet_documents('2024-10-31')

# 韓国データ
kr_collector = KoreaDataCollector(api_key='your_dart_api_key')
financials = kr_collector.get_financial_statements(
    corp_code='00126380',  # サムスン電子
    bsns_year='2023'
)
```

#### 5. データ分析

```python
from scripts.corporate_data_utils import *

# データ読み込み
df = pd.read_csv('your_data.csv')

# 財務比率作成
df = create_financial_ratios(df)

# ウィンソライズ
df = winsorize_variables(df, ['roa', 'leverage'])

# 品質チェック
report = run_quality_checks(df)
```

---

## 使用例

### 例1: 無料データのみで論文を書く

**研究テーマ**: 「東アジア3カ国の製造業収益性比較」

**使用データ**:
- 日本: EDINET（無料）
- 韓国: Open DART（無料）
- 台湾: TWSE/MOPS（無料）
- マクロ: World Bank（無料）

**推定費用**: ¥0

**詳細**: [templates/sample_project_asian_roa.md](templates/sample_project_asian_roa.md)

### 例2: ESG研究

**研究テーマ**: 「ASEAN企業の環境開示と資本コスト」

**使用データ**:
- ESG開示: CDP Open Data（研究者向け無料）
- 財務: 各国証券取引所（無料）
- 株価: Yahoo Finance API（無料）

**推定費用**: ¥0

### 例3: イノベーション研究

**研究テーマ**: 「アジア企業の特許活動と市場パフォーマンス」

**使用データ**:
- 特許: 各国特許庁（無料）
- 財務: 証券取引所（無料）
- グローバル特許: WIPO（無料）

**推定費用**: ¥0

---

## データソース一覧

### 日本 🇯🇵

#### 政府・公式データ
- **EDINET**: 有価証券報告書（API ✓）
- **e-Stat**: 政府統計ポータル（API ✓）
- **JPX**: 株価データ（CSV）
- **日本銀行**: 企業短観（API ✓）

#### アクセス方法
```python
from asian_data_collectors import JapanDataCollector
collector = JapanDataCollector()
data = collector.get_edinet_documents('2024-10-31')
```

### 韓国 🇰🇷

#### 政府・公式データ
- **Open DART**: 財務諸表、ガバナンス（API ✓）
- **KRX**: 株価データ（CSV）
- **KOSTAT**: 企業統計（API ✓）

#### アクセス方法
```python
from asian_data_collectors import KoreaDataCollector
collector = KoreaDataCollector(api_key='your_key')
data = collector.get_financial_statements('00126380', '2023')
```

### 中国 🇨🇳

#### 政府・公式データ
- **巨潮資訊（CNINFO）**: 財務諸表（HTML）
- **上海・深圳証券取引所**: 株価、公告（PDF）
- **Tushare**: 株価・財務API（基本無料）
- **AKShare**: 完全無料API（登録不要）

#### アクセス方法
```python
from asian_data_collectors import ChinaDataCollector
collector = ChinaDataCollector(tushare_token='your_token')
data = collector.get_stock_daily('600519.SH', '20240101', '20241031')
```

### 台湾 🇹🇼

#### 政府・公式データ
- **TWSE**: 株価データ（API ✓）
- **MOPS**: 財務諸表（HTML）
- **中華民國統計資訊網**: 企業統計（CSV）

#### アクセス方法
```python
from asian_data_collectors import TaiwanDataCollector
collector = TaiwanDataCollector()
data = collector.get_stock_daily('20241031')
```

### ASEAN諸国

| 国 | 取引所 | データ形式 | API |
|----|-------|----------|-----|
| シンガポール | SGX | CSV, Excel | 部分 |
| ベトナム | HOSE, HNX | Excel, PDF | - |
| マレーシア | Bursa Malaysia | PDF, Excel | 部分 |
| タイ | SET | Excel, PDF | - |
| インドネシア | IDX | Excel, PDF | - |
| フィリピン | PSE | PDF, Excel | - |

**詳細**: [FREE_LOW_COST_DATA_SOURCES.md](FREE_LOW_COST_DATA_SOURCES.md)

### グローバルデータ

#### 国際機関（すべて無料）
- **World Bank**: マクロ経済指標（API ✓）
- **IMF**: 国際収支、為替（API ✓）
- **OECD**: 産業統計（API ✓）
- **UN Comtrade**: 貿易統計（API ✓）
- **WIPO**: 特許統計（CSV）

#### アクセス方法
```python
from asian_data_collectors import GlobalDataCollector
collector = GlobalDataCollector()
data = collector.get_world_bank_data(
    indicator='NY.GDP.PCAP.CD',
    countries=['JPN', 'KOR', 'CHN'],
    start_year=2010,
    end_year=2023
)
```

---

## 研究分野別ガイド

### コーポレートファイナンス

**重要変数**: 資本構成、配当政策、投資、キャッシュ保有

**推奨データソース**:
- 財務: 各国証券取引所の財務諸表
- 市場: Yahoo Finance（yfinance）
- マクロ: World Bank、FRED

**サンプル研究**:
- 「資本構造の国際比較」
- 「配当政策の決定要因」

### 戦略経営

**重要変数**: 多角化、国際化、イノベーション（特許、R&D）

**推奨データソース**:
- 財務: 証券取引所
- 特許: 各国特許庁、WIPO
- セグメント情報: 財務諸表

**サンプル研究**:
- 「企業の国際化と業績」
- 「特許活動とイノベーション成果」

### コーポレートガバナンス

**重要変数**: 取締役会構成、所有構造、役員報酬

**推奨データソース**:
- ガバナンス: 有価証券報告書、事業報告書
- 所有構造: 大量保有報告
- 財務: 証券取引所

**サンプル研究**:
- 「取締役会多様性と企業パフォーマンス」
- 「所有構造とコーポレートガバナンス」

### ESG・サステナビリティ

**重要変数**: 炭素排出、ESG評価、サステナビリティ報告

**推奨データソース**:
- ESG: CDP Open Data（研究者向け無料）
- 環境報告: 企業ウェブサイト、GRIデータベース
- 財務: 証券取引所

**サンプル研究**:
- 「環境開示と資本コスト」
- 「ESGパフォーマンスと企業価値」

---

## ベストプラクティス

### ✅ Do's（すべきこと）

1. **早期開始**: データアクセス取得に時間がかかる
2. **小サンプルテスト**: 全データ収集前に手法を検証
3. **文書化の徹底**: すべてのステップを記録
4. **バックアップ**: 3-2-1ルール（3コピー、2種類のメディア、1つはオフサイト）
5. **API制限を守る**: レート制限を遵守、必要に応じてsleep()を挿入

### ❌ Don'ts（避けるべきこと）

1. **利用規約違反**: 法的リスクを冒さない
2. **過度のスクレイピング**: サーバーに負荷をかけない
3. **データ検証の省略**: 異常値を見逃すと研究全体が無効に
4. **単一ソース依存**: 複数ソースでクロスバリデーション
5. **文書化の後回し**: 後から思い出すのは困難

---

## よくある質問（FAQ）

### Q1: 有料データベースなしで査読論文は書けますか？

**A**: はい、可能です。特にアジア地域研究では、政府統計と証券取引所の公開データで十分なクオリティの研究が可能です。

**成功のポイント**:
- 独自のデータ収集・処理プロセスを詳細に記述
- 複数の無料ソースを組み合わせて独自性を出す
- データの限界を正直に記述し、ロバストネスチェックを実施

### Q2: データ収集にどのくらい時間がかかりますか？

**A**: プロジェクト規模により異なりますが、目安：

- **小規模**（1カ国、5年間、100社）: 1-2週間
- **中規模**（2-3カ国、10年間、500社）: 1-2ヶ月
- **大規模**（多国間、15年間、1000社以上）: 3-6ヶ月

**時間配分**:
- データ収集: 30-40%
- クリーニング: 30-40%
- 統合: 15-20%
- 品質チェック: 10-15%

### Q3: 中国語・韓国語のデータをどう扱えば良いですか？

**A**:
- **数値データ**: 言語に依存しないのでそのまま使用可能
- **テキストデータ**: Google Translate API（低コスト）、または現地研究者と協力
- **英語版**: 多くの大手企業は英語版財務報告も公開

### Q4: APIの利用制限に引っかかった場合は？

**A**: 対処法：

1. **レート制限**: スクリプトにsleep()を追加
2. **日次制限**: 複数日に分けてダウンロード
3. **総量制限**: サンプル期間・対象を絞る、または代替ソース

### Q5: 無料データの品質は大丈夫ですか？

**A**: はい。政府機関・証券取引所の公式データは高品質です。

**品質確保のポイント**:
- 複数ソースでクロスバリデーション
- 会計恒等式などの論理チェック
- 異常値の検出と処理
- 外れ値のマニュアル確認

---

## トラブルシューティング

### 問題1: API接続エラー

```python
# 解決策: リトライ機能付きダウンロード
def download_with_retry(func, *args, max_retries=3, delay=2):
    for attempt in range(max_retries):
        try:
            return func(*args)
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(delay * (attempt + 1))
            else:
                raise e
```

### 問題2: エンコードエラー（日本語・韓国語・中国語）

```python
# UTF-8 with BOMを使用
df.to_csv('file.csv', encoding='utf-8-sig')

# 読み込み時
df = pd.read_csv('file.csv', encoding='utf-8-sig')
```

### 問題3: メモリ不足

```python
# チャンク処理
chunk_size = 10000
for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    process(chunk)
```

### 問題4: データマッチング率が低い

**原因**:
- 企業名の表記揺れ
- 時系列のズレ
- データベースのカバレッジ違い

**解決策**:
```python
# ファジーマッチング
from fuzzywuzzy import fuzz, process

def fuzzy_match(name, choices, threshold=85):
    match, score = process.extractOne(name, choices)
    return match if score >= threshold else None
```

---

## サポートとフィードバック

### 使い方

1. **スキル起動**: 研究テーマを説明
   ```
   「ベトナムとタイの上場企業の資本構造を比較したい」
   ```

2. **データソース相談**: 
   ```
   「無料でベトナム企業の財務データを取得する方法は？」
   ```

3. **品質チェック依頼**:
   ```
   「収集したデータの品質をチェックして」
   ```

### リソース

- **メインガイド**: [SKILL.md](SKILL.md)
- **無料データソース**: [FREE_LOW_COST_DATA_SOURCES.md](FREE_LOW_COST_DATA_SOURCES.md)
- **サンプルプロジェクト**: [templates/sample_project_asian_roa.md](templates/sample_project_asian_roa.md)

---

## バージョン履歴

**v2.0** (2025-10-31) - **Publication-Grade Research Ready**
- 🚀 **Advanced Quality Assurance**: トップジャーナル基準の統計的品質保証
  - 多変量異常値検出（3手法アンサンブル）
  - Benford's Law テスト（不正検出）
  - 回帰ベース異常検出、構造的ブレーク検出
  - 影響力観測値検出、サンプル選択バイアステスト
- 📊 **Statistical Power Analysis**: サンプルサイズ計算機能（t検定、回帰、パネル）
- 🔄 **Data Lineage Tracker**: 完全な系譜追跡と再現性担保（AEA準拠）
- ✅ **Research Checklist Manager**: 7フェーズ28タスクの進捗管理システム
- 🧪 **Test Suite**: pytest ベース包括的テスト（カバレッジ80%+目標）
- 🐳 **Docker Support**: 環境完全再現性の担保
- 🛡️ **Enhanced Error Handling**: 本番環境対応のロバストなエラー処理
  - リトライロジック、詳細ログ、型安全性

**v1.1** (2025-10-31)
- 🆕 アジア11カ国・地域の無料データソース追加
- 🆕 実用的なPythonスクリプト追加（asian_data_collectors.py）
- 🆕 サンプルプロジェクト追加（アジア製造業ROA分析）
- 🆕 70以上の無料データソース詳細ガイド

**v1.0** (2025-10-31)
- 初回リリース
- 7段階ワークフロー
- 企業研究特化の包括的機能
- Pythonユーティリティスクリプト
- テンプレートとチェックリスト

---

## ライセンスと利用規約

このスキルは研究計画と実行のためのツールです。研究者は以下の責任を負います：

1. すべてのデータ提供者の利用規約の遵守
2. 必要な機関承認の取得（IRB、データ利用契約）
3. 出版物でのデータソースの適切な引用
4. データの倫理的使用の確保
5. 研究に対するデータの正確性と適切性の検証

---

## 🎯 今すぐ始めよう！

### 研究テーマを教えてください

```
「台湾とシンガポールのハイテク企業のイノベーション活動を比較したい」
```

または

```
「無料データでアジアのESG研究をしたい。どこから始めれば良い？」
```

**無料データで世界水準の研究を実現しましょう！**

---

#企業研究 #無料データソース #アジア企業 #実証研究 #データ収集 #パネルデータ #財務分析 #品質保証