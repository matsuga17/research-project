# クイックスタートガイド

**所要時間: 15分で最初のデータ収集を開始**

---

## ステップ1: 研究テーマの明確化（3分）

### 質問に答えてください

**Q1: 研究の中心的な問い（Research Question）は何ですか？**

例:
- 「取締役会の女性比率は企業パフォーマンスに影響するか？」
- 「アジア企業の国際化は収益性を高めるか？」
- 「ESG評価は資本コストを下げるか？」

あなたの答え:
```
_____________________________________________________________
```

**Q2: 対象地域・国はどこですか？**

選択肢:
- [ ] 日本のみ
- [ ] 韓国のみ
- [ ] 中国のみ
- [ ] 台湾のみ
- [ ] ASEAN（どの国？）
- [ ] アジア複数国（どの国？）
- [ ] グローバル

あなたの答え:
```
_____________________________________________________________
```

**Q3: 対象企業の特徴は？**

- [ ] 上場企業のみ
- [ ] 製造業
- [ ] サービス業
- [ ] ハイテク産業
- [ ] 特定業種: ___________
- [ ] 企業規模: 大企業/中小企業/すべて

**Q4: 時期・期間は？**

- 開始年: _______
- 終了年: _______
- 理由: _____________________________________________

---

## ステップ2: データソースの選択（5分）

### あなたの研究に必要なデータは？

**財務データ**
- [ ] 損益計算書（売上高、純利益など）
- [ ] 貸借対照表（総資産、負債、純資産）
- [ ] キャッシュフロー計算書
- [ ] セグメント情報

**市場データ**
- [ ] 株価（日次・週次・月次）
- [ ] 市場指数
- [ ] 取引高

**ガバナンスデータ**
- [ ] 取締役会構成
- [ ] 所有構造
- [ ] 役員報酬

**ESG・サステナビリティ**
- [ ] 環境開示
- [ ] ESG評価
- [ ] GHG排出量

**その他**
- [ ] 特許・R&D
- [ ] M&A
- [ ] ___________

### 推奨データソース

あなたの選択に基づいて、以下を確認:

#### 日本企業の場合

| 必要データ | 無料ソース | APIあり | 取得方法 |
|----------|----------|--------|---------|
| 財務諸表 | EDINET | ✓ | [SKILL.md](SKILL.md) 参照 |
| 株価 | JPX, Yahoo Finance | 部分的 | CSV, yfinance |
| ガバナンス | EDINET | ✓ | 有価証券報告書 |

詳細: [FREE_LOW_COST_DATA_SOURCES.md](FREE_LOW_COST_DATA_SOURCES.md)

#### 韓国企業の場合

| 必要データ | 無料ソース | APIあり | 取得方法 |
|----------|----------|--------|---------|
| 財務諸表 | Open DART | ✓ | Pythonスクリプト |
| 株価 | KRX, Yahoo Finance | 部分的 | CSV, API |
| ガバナンス | Open DART | ✓ | API |

#### 中国企業の場合

| 必要データ | 無料ソース | APIあり | 取得方法 |
|----------|----------|--------|---------|
| 財務諸表 | 巨潮資訊, Tushare | ✓ | HTML, API |
| 株価 | Tushare, AKShare | ✓ | Python |
| 公告 | 証券取引所 | - | PDF |

#### その他の国

[FREE_LOW_COST_DATA_SOURCES.md](FREE_LOW_COST_DATA_SOURCES.md) の該当セクションを参照

---

## ステップ3: 環境構築（5分）

### 3.1 必要なソフトウェア

**Python環境**（推奨: Python 3.8以上）

```bash
# バージョン確認
python --version

# まだインストールしていない場合
# Windows: https://www.python.org/downloads/
# Mac: brew install python3
# Linux: sudo apt-get install python3
```

### 3.2 必要なパッケージのインストール

```bash
# 基本パッケージ
pip install pandas numpy scipy

# データ収集
pip install requests beautifulsoup4

# 分析・可視化
pip install statsmodels matplotlib seaborn

# オプション: 中国データ用
pip install tushare akshare

# オプション: 株価データ用
pip install yfinance
```

**インストール確認**:
```python
import pandas as pd
import numpy as np
import requests
print("✓ インストール成功")
```

### 3.3 APIキー取得（必要な場合のみ）

**韓国 - Open DART**（5分で取得可能）

1. https://opendart.fss.or.kr/ にアクセス
2. 「API 신청」をクリック
3. 基本情報を入力（メールアドレス必須）
4. メール認証
5. APIキー即時発行

**中国 - Tushare**（オプション）

1. https://tushare.pro/register にアクセス
2. アカウント登録（メール/携帯番号）
3. トークン取得
4. ポイント制（基本機能は無料）

**グローバル - World Bank**

- 登録不要、誰でも使用可能

---

## ステップ4: 最初のデータ収集（2分）

### サンプルコード: 日本の財務データ

```python
from scripts.asian_data_collectors import JapanDataCollector
from datetime import datetime

# コレクター初期化
collector = JapanDataCollector()

# 今日の提出書類を取得
today = datetime.now().strftime('%Y-%m-%d')
documents = collector.get_edinet_documents(today)

# 結果表示
print(f"取得件数: {len(documents)}")
print(documents[['filerName', 'docDescription']].head())
```

### サンプルコード: 韓国の財務データ

```python
from scripts.asian_data_collectors import KoreaDataCollector

# APIキーを設定
api_key = "your_dart_api_key_here"
collector = KoreaDataCollector(api_key)

# サムスン電子の2023年財務諸表
data = collector.get_financial_statements(
    corp_code='00126380',
    bsns_year='2023',
    reprt_code='11011'
)

print(f"取得項目数: {len(data)}")
print(data[['account_nm', 'thstrm_amount']].head(10))
```

### サンプルコード: World Bankマクロデータ

```python
from scripts.asian_data_collectors import GlobalDataCollector

collector = GlobalDataCollector()

# アジア主要国のGDP per capita
gdp_data = collector.get_world_bank_data(
    indicator='NY.GDP.PCAP.CD',
    countries=['JPN', 'KOR', 'CHN', 'TWN'],
    start_year=2010,
    end_year=2023
)

print(f"取得データポイント: {len(gdp_data)}")
print(gdp_data.head())
```

---

## ステップ5: 次のアクション

### ✅ データ収集が成功したら

**本格的なデータ収集計画を立てる**:
1. [templates/data_collection_plan.md](templates/data_collection_plan.md) を参考に計画書作成
2. [SKILL.md](SKILL.md) の7段階ワークフローに従う

**サンプルプロジェクトを参考にする**:
- [templates/sample_project_asian_roa.md](templates/sample_project_asian_roa.md)

### ❌ うまくいかなかったら

**よくある問題と解決法**:

**問題1: API接続エラー**
```
ConnectionError, TimeoutError
```
**解決策**:
- インターネット接続を確認
- URLが正しいか確認
- APIキーが正しいか確認（韓国の場合）
- しばらく待ってから再試行

**問題2: パッケージが見つからない**
```
ModuleNotFoundError: No module named 'pandas'
```
**解決策**:
```bash
pip install pandas
# または
pip install -r requirements.txt
```

**問題3: 文字化け（日本語・韓国語・中国語）**
```python
# 読み込み時
df = pd.read_csv('file.csv', encoding='utf-8-sig')

# 保存時
df.to_csv('file.csv', encoding='utf-8-sig', index=False)
```

**問題4: APIレート制限**
```
429 Too Many Requests
```
**解決策**:
```python
import time

# リクエスト間に待機時間を挿入
for item in items:
    data = get_data(item)
    time.sleep(2)  # 2秒待機
```

---

## チェックリスト

研究を開始する前に、以下を確認:

- [ ] 研究テーマが明確
- [ ] 必要なデータソースを特定
- [ ] Python環境が整っている
- [ ] 必要なパッケージがインストール済み
- [ ] APIキーを取得（必要な場合）
- [ ] サンプルコードが動作した
- [ ] データ保存場所を決定
- [ ] バックアップ計画を立てた

---

## 次のステップ: 本格的な研究へ

### フェーズ1: データ収集（1-2週間）

1. **データ収集計画の策定**
   - [templates/data_collection_plan.md](templates/data_collection_plan.md) を使用
   - 対象企業リスト作成
   - 収集スケジュール策定

2. **実装**
   - スクリプトの作成・調整
   - バッチ処理の実装
   - エラーハンドリング

3. **品質チェック**
   - [scripts/data_quality_checker.py](scripts/data_quality_checker.py) を実行
   - 異常値の確認
   - 欠損値の処理

### フェーズ2: データクリーニング（1週間）

1. **標準化**
   - 通貨単位の統一
   - 会計年度の調整
   - 業種分類の統一

2. **変数作成**
   - 財務比率の計算
   - ダミー変数の作成
   - ラグ変数の作成

3. **品質保証**
   - [templates/quality_assurance_checklist.md](templates/quality_assurance_checklist.md) を使用

### フェーズ3: 分析（1-2週間）

1. **記述統計**
2. **相関分析**
3. **回帰分析**
4. **ロバストネスチェック**

### フェーズ4: 執筆・投稿（継続的）

---

## サポート

### 質問がある場合

このスキルに質問を投げかけてください:

```
「韓国のOpen DART APIでガバナンスデータを取得する方法は？」
```

```
「パネルデータの不均衡をどう処理すればいい？」
```

```
「中国語の財務諸表をどう英語に変換する？」
```

### さらに詳しく学ぶ

- **メインガイド**: [SKILL.md](SKILL.md)
- **無料データソース**: [FREE_LOW_COST_DATA_SOURCES.md](FREE_LOW_COST_DATA_SOURCES.md)
- **実用スクリプト**: [scripts/](scripts/)
- **テンプレート**: [templates/](templates/)

---

## 成功のための3つのヒント

### 1. 小さく始める

最初から大規模プロジェクトを目指さない:
- **最初**: 10-20社、2-3年間
- **次**: 50社、5年間
- **最後**: 数百社、10年間以上

### 2. 文書化を徹底する

後から再現できるように:
- すべてのステップを記録
- スクリプトにコメントを追加
- データソースのURLとアクセス日を記録
- エラーと解決方法をメモ

### 3. 定期的にバックアップ

データ消失は致命的:
- 毎日: ローカルバックアップ
- 毎週: クラウドバックアップ
- 各マイルストーン: 外部HDD

---

## 準備完了！

**さあ、データ収集を始めましょう！**

次のステップ:
1. サンプルコードを実行してデータ取得を確認
2. [templates/data_collection_plan.md](templates/data_collection_plan.md) を使って計画を立てる
3. [SKILL.md](SKILL.md) の7段階ワークフローに従う

**質問があればいつでもこのスキルに聞いてください！**

---

#クイックスタート #初心者ガイド #データ収集 #実証研究 #無料データ