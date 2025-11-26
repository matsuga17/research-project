# 分析テンプレート使用ガイド

このディレクトリには、US Corporate Analyticsで使用する各種分析テンプレートが格納されています。

---

## 利用可能なテンプレート

### 1. 財務分析テンプレート (financial_analysis_template.xlsx)

**用途**: 企業の包括的財務分析

**含まれるシート**:
1. **Summary（サマリー）**
   - 企業基本情報
   - 主要財務指標のダッシュボード
   - パフォーマンス評価

2. **Income Statement（損益計算書）**
   - 売上高、売上原価、売上総利益
   - 営業費用、営業利益
   - 純利益
   - 5年間の推移

3. **Balance Sheet（貸借対照表）**
   - 資産（流動資産、固定資産）
   - 負債（流動負債、固定負債）
   - 株主資本
   - 5年間の推移

4. **Cash Flow（キャッシュフロー）**
   - 営業キャッシュフロー
   - 投資キャッシュフロー
   - 財務キャッシュフロー
   - フリーキャッシュフロー

5. **Financial Ratios（財務比率）**
   - 収益性指標（ROA、ROE、利益率等）
   - 流動性指標（流動比率、当座比率等）
   - レバレッジ指標（負債比率、D/E比率等）
   - 効率性指標（回転率等）
   - 成長性指標

6. **Trend Analysis（トレンド分析）**
   - 主要指標の時系列チャート
   - 成長率の計算
   - 予測トレンドライン

**使用方法**:
```python
from scripts.company_analyzer import CompanyAnalyzer
import pandas as pd

# データ取得
analyzer = CompanyAnalyzer("AAPL", config)
analyzer.fetch_all_data(years=5)

# テンプレートに書き込み
with pd.ExcelWriter("financial_analysis_AAPL.xlsx") as writer:
    analyzer.financial_data.to_excel(writer, sheet_name="Raw Data")
    analyzer.financial_ratios.to_excel(writer, sheet_name="Financial Ratios")
```

---

### 2. ガバナンス評価テンプレート (governance_scorecard.xlsx)

**用途**: コーポレートガバナンスの包括的評価

**含まれるシート**:
1. **Board Composition（取締役会構成）**
   - 取締役リスト
   - 独立取締役比率
   - 多様性指標（性別、年齢、国籍、専門性）
   - 在任期間

2. **Executive Compensation（役員報酬）**
   - CEO報酬の構成（基本給、ボーナス、株式報酬）
   - 報酬委員会メンバー
   - Pay-for-Performance分析
   - 業界比較

3. **Ownership Structure（株主構造）**
   - 大株主リスト
   - 機関投資家の保有状況
   - 内部者保有比率
   - 株主の集中度（HHI指数）

4. **Governance Score（ガバナンススコア）**
   - 各項目の評価点
   - 総合スコア
   - ベンチマークとの比較

**スコアリング基準**:
- 取締役会の独立性（0-25点）
- 報酬の適切性（0-25点）
- 株主の権利保護（0-25点）
- 情報開示の透明性（0-25点）

**総合評価**:
- 90-100点: Excellent（優秀）
- 75-89点: Good（良好）
- 60-74点: Fair（標準）
- 60点未満: Poor（要改善）

---

### 3. 業界比較テンプレート (peer_comparison_template.xlsx)

**用途**: 同業他社との詳細比較

**含まれるシート**:
1. **Company List（企業リスト）**
   - 比較対象企業の基本情報
   - 業界分類（SICコード）
   - 企業規模（売上高、総資産、従業員数）

2. **Financial Comparison（財務比較）**
   - 主要財務指標の横比較
   - ランキング
   - 業界平均との差異

3. **Growth Comparison（成長性比較）**
   - 売上成長率
   - 利益成長率
   - 市場シェアの変化

4. **Efficiency Comparison（効率性比較）**
   - 資産回転率
   - 在庫回転率
   - 従業員一人当たり売上高

5. **Visual Dashboard（ビジュアルダッシュボード）**
   - レーダーチャート
   - 散布図（ROE vs 成長率等）
   - ヒートマップ

**使用方法**:
```python
from scripts.industry_comparison import IndustryComparison

tickers = ["AAPL", "MSFT", "GOOGL"]
comparison = IndustryComparison(tickers, config)
comparison.fetch_all_companies(years=5)

# Excel出力
comparison.export_comparison("./reports")
```

---

### 4. イベントスタディテンプレート (event_study_template.xlsx)

**用途**: 重要イベント（M&A、CEO交代等）の株価反応分析

**含まれるシート**:
1. **Event List（イベントリスト）**
   - イベント日
   - イベントタイプ
   - 企業名
   - イベント詳細

2. **Returns Calculation（リターン計算）**
   - 正常リターンの計算
   - 異常リターン（AR）
   - 累積異常リターン（CAR）

3. **Statistical Tests（統計的検定）**
   - t検定
   - 信頼区間
   - 有意性判定

4. **Visualization（可視化）**
   - CARプロット
   - イベント前後のリターン推移

**分析ウィンドウ**:
- 推定期間: イベント日の-250日～-11日
- イベントウィンドウ: -10日～+10日

---

### 5. デューデリジェンステンプレート (due_diligence_template.xlsx)

**用途**: M&A対象企業の詳細調査

**含まれるシート**:
1. **Executive Summary（エグゼクティブサマリー）**
   - 調査対象企業の概要
   - 主要発見事項
   - リスク評価
   - 推奨事項

2. **Financial Analysis（財務分析）**
   - 過去5年間の財務トレンド
   - 財務比率分析
   - 予測財務諸表

3. **Legal & Compliance（法務・コンプライアンス）**
   - 訴訟リスク
   - 規制遵守状況
   - 知的財産権

4. **Operational Assessment（業務評価）**
   - 事業プロセス
   - サプライチェーン
   - 人材・組織

5. **Valuation（企業価値評価）**
   - DCF法
   - 類似企業比較法
   - 取引事例法

6. **Risk Matrix（リスクマトリックス）**
   - リスク項目
   - 発生確率
   - 影響度
   - 対応策

---

## テンプレートのカスタマイズ

### 追加項目の挿入

すべてのテンプレートは拡張可能です。以下の手順で項目を追加：

1. Excelファイルを開く
2. 該当シートの最終列の次に新しい列を挿入
3. ヘッダーを記入
4. 必要に応じて数式を設定

### カスタム計算式の追加

例：独自の財務指標を追加する場合

```excel
=（セルA1）/（セルB1）* 100
```

### 条件付き書式の設定

パフォーマンスを視覚的に表現：

1. データ範囲を選択
2. [ホーム] > [条件付き書式] > [カラースケール]
3. 緑（高）→黄（中）→赤（低）を設定

---

## Pythonスクリプトとの統合

### データの自動入力

```python
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows

# Excelファイルを開く
wb = openpyxl.load_workbook('financial_analysis_template.xlsx')
ws = wb['Financial Ratios']

# DataFrameをExcelに書き込み
for r in dataframe_to_rows(financial_ratios, index=True, header=True):
    ws.append(r)

wb.save('financial_analysis_output.xlsx')
```

### チャートの自動生成

```python
from openpyxl.chart import LineChart, Reference

# チャートを作成
chart = LineChart()
chart.title = "Revenue Trend"
chart.x_axis.title = "Year"
chart.y_axis.title = "Revenue (USD)"

# データ範囲を指定
data = Reference(ws, min_col=2, min_row=1, max_row=6)
chart.add_data(data, titles_from_data=True)

# チャートを挿入
ws.add_chart(chart, "E2")
```

---

## ベストプラクティス

### 1. データ入力時の注意点

- **一貫した単位**: すべて千ドル単位、または百万ドル単位で統一
- **欠損値の扱い**: 欠損値は"N/A"または空白セル
- **日付形式**: YYYY-MM-DD形式を推奨

### 2. 数式の設定

- **絶対参照と相対参照**: 適切に使い分け
- **エラー処理**: IFERROR関数を活用
- **循環参照の回避**: 意図しない循環参照に注意

### 3. 可視化のガイドライン

- **カラーパレット**: 色覚多様性に配慮（ColorBrewer推奨）
- **チャートタイプ**: データの性質に応じて選択
  - トレンド → 折れ線グラフ
  - 比較 → 棒グラフ
  - 構成比 → 円グラフ
  - 相関 → 散布図

### 4. レポート作成

- **エグゼクティブサマリー**: 1ページに要約
- **重要発見事項**: ハイライト表示
- **アクションアイテム**: 具体的な推奨事項

---

## トラブルシューティング

### 問題1: 数式がエラーを返す

**原因**: 参照セルが空白または文字列

**解決策**:
```excel
=IFERROR(A1/B1, "N/A")
```

### 問題2: チャートが正しく表示されない

**原因**: データ範囲の設定ミス

**解決策**:
1. チャートを右クリック > [データの選択]
2. データ範囲を再設定

### 問題3: ファイルサイズが大きい

**原因**: 不要なデータや書式が残存

**解決策**:
1. 使用していないシートを削除
2. [ファイル] > [情報] > [問題のチェック] > [ドキュメント検査]

---

## サポート

テンプレートに関する質問や改善提案は以下まで：

- GitHub Issues: [プロジェクトURL]
- Email: support@example.com

---

**最終更新**: 2025-11-02  
**バージョン**: 1.0
