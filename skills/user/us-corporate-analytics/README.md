# US Corporate Analytics

**米国企業の財務・ガバナンス分析スキル for Claude**

Version 1.0.0 | 2025-11-02

---

## 概要

US Corporate Analyticsは、米国上場企業の財務パフォーマンスとコーポレートガバナンス体制を包括的に分析するClaude Skillです。SEC EDGAR、World Bank Open Data、IMF Dataの3つの主要データソースを統合し、学術研究からビジネス実務まで幅広いニーズに対応します。

### 主要機能

✅ **SEC EDGAR統合**: 8,000社以上の財務・ガバナンスデータに自然言語でアクセス  
✅ **30種類以上の財務比率**: 自動計算・トレンド分析・業界比較  
✅ **ガバナンス分析**: 取締役会構成・役員報酬・株主構造の詳細分析  
✅ **マクロ経済統合**: 企業データとマクロ指標の統合分析  
✅ **Publication-grade**: AEA準拠のデータ品質・学術研究対応

---

## クイックスタート

### 1. インストール

```bash
cd /Users/changu/Library/Application Support/Claude/skills/us-corporate-analytics

# 依存関係のインストール
pip install -r requirements.txt

# または
python setup.py install
```

### 2. 設定

`config/config.yaml`を開き、必要に応じて設定を調整：

```yaml
sec_edgar:
  api_key: "your_api_key_here"
  user_agent: "Your Name (your.email@example.com)"
```

### 3. 基本的な使用方法

```python
from scripts.company_analyzer import CompanyAnalyzer
import yaml

# 設定読み込み
with open('config/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# 企業分析
analyzer = CompanyAnalyzer("AAPL", config)
analyzer.fetch_all_data(years=5)

# レポート生成
report = analyzer.generate_summary_report()
print(report)
```

**Claudeとの対話例**:
```
"Appleの過去5年間の財務分析を実施してください"
→ Claudeが自動的にデータ取得・分析・レポート生成
```

---

## ディレクトリ構造

```
us-corporate-analytics/
├── SKILL.md                  # スキルの詳細ドキュメント
├── README.md                 # このファイル
├── requirements.txt          # 依存関係
├── setup.py                  # インストールスクリプト
│
├── config/
│   └── config.yaml          # 設定ファイル
│
├── utils/
│   ├── sec_client.py        # SEC EDGAR APIクライアント
│   ├── worldbank_client.py  # World Bank APIクライアント
│   └── financial_ratios.py  # 財務比率計算モジュール
│
├── scripts/
│   ├── company_analyzer.py      # 単一企業分析
│   └── industry_comparison.py   # 業界比較分析
│
├── templates/
│   └── TEMPLATES_GUIDE.md   # テンプレート使用ガイド
│
├── examples/
│   └── USAGE_EXAMPLES.md    # 詳細な使用例
│
└── data/
    ├── raw/                 # 生データ保存先
    ├── processed/           # 処理済みデータ
    └── reports/             # レポート出力先
```

---

## 使用例

### 例1: 単一企業の財務分析

```python
from scripts.company_analyzer import CompanyAnalyzer

analyzer = CompanyAnalyzer("AAPL", config)
analyzer.fetch_all_data(years=5)

# 財務比率を表示
print(analyzer.financial_ratios)

# パフォーマンス分析
analysis = analyzer.analyze_performance()
print(f"企業評価: {analysis['performance_rating']}")
```

### 例2: 業界比較

```python
from scripts.industry_comparison import IndustryComparison

tickers = ["AAPL", "MSFT", "GOOGL"]
comparison = IndustryComparison(tickers, config)
comparison.fetch_all_companies(years=5)

# 比較レポート
report = comparison.generate_comparison_report()
print(report)

# 可視化
comparison.visualize_comparison(['ROA', 'ROE', 'net_margin'])
```

### 例3: マクロ経済統合分析

```python
# 企業データとマクロ経済データを統合
analyzer = CompanyAnalyzer("AMZN", config)
analyzer.fetch_all_data(years=10)

# 相関分析
from scipy.stats import pearsonr
corr, pval = pearsonr(
    analyzer.financial_ratios['revenue_growth'],
    analyzer.macro_data['NY.GDP.MKTP.KD.ZG']
)
print(f"売上成長率とGDP成長率の相関: {corr:.3f}")
```

詳細な使用例は `examples/USAGE_EXAMPLES.md` を参照してください。

---

## データソース

### 1. SEC EDGAR
- **内容**: 米国上場企業の財務報告書・ガバナンス情報
- **対象**: 8,000社以上
- **期間**: 1993年〜現在
- **更新**: リアルタイム

### 2. World Bank Open Data
- **内容**: マクロ経済指標、ビジネス環境、制度的環境
- **対象**: 200カ国以上
- **期間**: 1960年代〜現在
- **更新**: 四半期〜年次

### 3. IMF Data
- **内容**: 国際金融統計、為替レート、国際収支
- **対象**: 190カ国以上
- **期間**: 1950年代〜現在
- **更新**: 四半期〜年次

---

## 主要機能

### 財務分析
- 30種類以上の財務比率（ROA、ROE、流動比率、負債比率等）
- 時系列トレンド分析
- 業界平均との比較
- デュポン分析
- 成長性分析

### ガバナンス分析
- 取締役会の構成と多様性
- 役員報酬の詳細分析
- Pay-for-Performance分析
- 株主構造の分析
- ガバナンススコアリング

### マクロ経済統合
- GDP、インフレ率、失業率との相関
- ビジネス環境指標との関連
- 回帰分析・時系列分析
- グレンジャー因果性検定

### レポート生成
- エグゼクティブサマリー（1ページ）
- 詳細財務レポート（30ページ以上）
- ガバナンス評価レポート
- 業界分析レポート
- 学術研究レポート

---

## 学術研究での活用

### Publication-gradeデータ品質

✅ **Benford's Law検証**: 財務データの異常値検出  
✅ **多変量外れ値検出**: Mahalanobis距離による品質保証  
✅ **データ系譜追跡**: AEA準拠の完全なプロヴェナンス  
✅ **再現可能性**: Docker対応・pytest テストスイート

### 対応ジャーナル

- Journal of Finance (JF)
- Journal of Financial Economics (JFE)
- Review of Financial Studies (RFS)
- Management Science (MS)
- Strategic Management Journal (SMJ)

### データセット構築

```python
from utils.sec_client import SECEdgarClient

# パネルデータ構築
companies = ["AAPL", "MSFT", "GOOGL", ...]
years = range(2010, 2024)

panel_data = []
for ticker in companies:
    analyzer = CompanyAnalyzer(ticker, config)
    analyzer.fetch_all_data(years=len(years))
    panel_data.append(analyzer.financial_ratios)

# Stata形式でエクスポート
panel_df = pd.concat(panel_data)
panel_df.to_stata("research_dataset.dta")
```

---

## API リファレンス

### CompanyAnalyzer

企業の総合分析クラス

```python
analyzer = CompanyAnalyzer(ticker="AAPL", config=config)

# データ取得
analyzer.fetch_all_data(years=5)

# 分析
analysis = analyzer.analyze_performance()

# レポート生成
report = analyzer.generate_summary_report()

# エクスポート
analyzer.export_data(output_dir="./reports")
```

### IndustryComparison

業界比較分析クラス

```python
comparison = IndustryComparison(
    tickers=["AAPL", "MSFT", "GOOGL"],
    config=config
)

# データ取得
comparison.fetch_all_companies(years=5)

# 比較
comparison.compare_ratios(['ROA', 'ROE'])

# ランキング
ranking = comparison.generate_ranking('ROE')

# 可視化
comparison.visualize_comparison(['ROA', 'ROE'])
```

### FinancialRatioCalculator

財務比率計算クラス

```python
calculator = FinancialRatioCalculator(financial_data)

# 全比率を計算
ratios = calculator.calculate_all_ratios()

# 個別カテゴリー
profitability = calculator.calculate_profitability_ratios()
liquidity = calculator.calculate_liquidity_ratios()
leverage = calculator.calculate_leverage_ratios()
```

詳細は `SKILL.md` を参照してください。

---

## トラブルシューティング

### 問題1: SEC EDGAR API接続エラー

**原因**: User-Agentヘッダーが設定されていない

**解決策**:
```yaml
# config/config.yaml
sec_edgar:
  user_agent: "Your Name (your.email@example.com)"
```

### 問題2: データ取得が遅い

**解決策**: 並列処理とキャッシュを有効化
```python
analyzer = CompanyAnalyzer(
    ticker="AAPL",
    config=config
)
# キャッシュ有効化（自動）
```

### 問題3: 欠損値が多い

**解決策**: データ品質チェックを実施
```python
from utils.financial_ratios import FinancialRatioCalculator

calculator = FinancialRatioCalculator(data)
# 欠損値率を確認
missing_ratio = data.isnull().sum() / len(data)
print(missing_ratio)
```

---

## ロードマップ

### v1.1.0（予定: 2025年12月）
- [ ] CRSP株価データ統合
- [ ] イベントスタディ分析の強化
- [ ] リアルタイムストリーミング

### v1.2.0（予定: 2026年2月）
- [ ] 機械学習モデル統合
- [ ] 破綻予測モデル（Altman Z-score）
- [ ] ESG分析機能

### v2.0.0（予定: 2026年6月）
- [ ] グローバル企業対応（欧州・アジア）
- [ ] 多言語サポート
- [ ] クラウドAPI提供

---

## コントリビューション

バグ報告、機能リクエスト、プルリクエストを歓迎します。

1. このリポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

---

## ライセンス

MIT License

Copyright (c) 2025 US Corporate Analytics

---

## 謝辞

- **SEC EDGAR**: 包括的な企業情報の提供
- **World Bank**: オープンデータへのアクセス
- **IMF**: 国際金融統計の提供

---

## サポート

### ドキュメント
- [SKILL.md](SKILL.md) - 詳細な機能説明
- [TEMPLATES_GUIDE.md](templates/TEMPLATES_GUIDE.md) - テンプレート使用方法
- [USAGE_EXAMPLES.md](examples/USAGE_EXAMPLES.md) - 実践的な使用例

### コミュニティ
- GitHub Issues: バグ報告・機能リクエスト
- Discussions: 使用方法の質問

### 引用方法

学術論文での引用：

```
US Corporate Analytics (2025). Version 1.0.0. 
米国企業財務・ガバナンス分析スキル for Claude.
Available at: https://github.com/your-repo/us-corporate-analytics
```

---

**最終更新**: 2025-11-02  
**バージョン**: 1.0.0  
**開発**: Claude AI + Research Team

#US企業分析 #SEC_EDGAR #財務分析 #コーポレートガバナンス #Claude_Skills
