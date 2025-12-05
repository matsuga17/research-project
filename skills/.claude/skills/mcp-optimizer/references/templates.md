# プロンプトテンプレート集

## 基本テンプレート

### Template 1: 検索＋保存

```
{検索対象}について{ソース}で{件数}件検索して、
結果を{ファイルパス}に以下の形式で保存：
{保存形式}

私には{要約情報}だけ教えて。
```

**使用例**:
```
platform strategyについてSemantic Scholarで20件検索して、
結果を/home/claude/papers/platform_strategy.csvに以下の形式で保存：
| タイトル | 著者 | 年 | 引用数 | DOI |

私には「○件発見。引用数トップ3は...」だけ教えて。
```

### Template 2: 複数対象バッチ処理

```
以下の{N}件について{処理内容}を実行：
{対象リスト}

各結果は{保存先}/{命名規則}で保存。
私には{サマリー情報}だけ報告。
```

**使用例**:
```
以下の5社について基本情報を収集：
1. Alibaba
2. Coupang
3. Sea Limited
4. Flipkart
5. Tokopedia

各結果は/home/claude/companies/{企業名}.jsonで保存。
私には「5社完了。売上規模順は...」だけ報告。
```

### Template 3: フェーズ分割実行

```
{タスク}を以下のフェーズで実行：

【Phase 1: {フェーズ1名}】
処理: {処理内容1}
保存: {保存先1}
報告: {報告内容1}

【Phase 2: {フェーズ2名}】※「続けて」で開始
処理: {処理内容2}
保存: {保存先2}
報告: {報告内容2}

【Phase 3: {フェーズ3名}】※「続けて」で開始
処理: {処理内容3}
出力: {出力形式}
```

### Template 4: 複数ソース統合

```
{テーマ}について以下のソースから情報収集：

1. {ソース1}
   → 保存: {保存先1}
   → 取得項目: {項目1}

2. {ソース2}
   → 保存: {保存先2}
   → 取得項目: {項目2}

3. {ソース3}
   → 保存: {保存先3}
   → 取得項目: {項目3}

各ソースから{最低件数}件以上収集後、統合分析。
私には主要な発見を{N}点で報告。詳細は各ファイル参照。
```

### Template 5: 条件付き処理

```
{処理内容}を実行。以下の条件で分岐：

条件A（{条件A}の場合）:
→ {処理A}
→ 報告: {報告A}

条件B（{条件B}の場合）:
→ {処理B}
→ 報告: {報告B}

条件C（{条件C}の場合）:
→ {処理C}
→ 報告: {報告C}
```

## 研究タスク向けテンプレート

### Template R1: 文献レビュー

```
{研究テーマ}に関する文献レビューを実行：

【Phase 1: 文献検索】
キーワード: {keyword1}, {keyword2}, {keyword3}
ソース: Semantic Scholar, Google Scholar
期間: {start_year}-{end_year}
保存: /home/claude/literature/{topic}_search.csv
報告: 総件数のみ

【Phase 2: スクリーニング】※「続けて」で開始
基準: 引用数{min_citations}以上
保存: /home/claude/literature/{topic}_filtered.csv
報告: 絞り込み後件数のみ

【Phase 3: 詳細分析】※「続けて」で開始
対象: 上位{N}件のアブストラクト
保存: /home/claude/literature/{topic}_analysis.md
報告: 主要テーマ3つ
```

### Template R2: 企業データ収集

```
{企業リスト}の企業データを収集：

【収集項目】
- 基本情報: 設立年、本社所在地、従業員数
- 財務情報: 売上高、営業利益、時価総額
- 事業情報: 主要サービス、市場シェア

【保存形式】
各社: /home/claude/companies/{企業名}.json
統合: /home/claude/companies/summary.csv

【報告形式】
「{N}社収集完了。売上規模トップ3: {企業1}, {企業2}, {企業3}」
```

### Template R3: 市場調査

```
{市場/業界}の調査を実行：

【Phase 1: データ収集】
1. 市場規模データ → /home/claude/market/size.md
2. 競合分析 → /home/claude/market/competitors.md
3. トレンド → /home/claude/market/trends.md
報告: 各カテゴリの情報源数のみ

【Phase 2: 統合分析】※「続けて」で開始
保存: /home/claude/market/analysis.md
報告: 主要インサイト3点

【Phase 3: レポート作成】※「続けて」で開始
出力: アーティファクト（構造化レポート）
```

### Template R4: 比較分析

```
{比較対象リスト}の比較分析を実行：

【比較項目】
{比較項目1}, {比較項目2}, {比較項目3}, ...

【処理手順】
1. 各対象のデータ収集 → /home/claude/comparison/data/
2. 比較マトリックス作成 → /home/claude/comparison/matrix.md
3. 分析・考察 → /home/claude/comparison/analysis.md

【報告形式】
「比較完了。最も{評価軸}が高いのは{対象}。主要差異は{差異}」
```

## 日常タスク向けテンプレート

### Template D1: 情報収集

```
{トピック}について最新情報を収集：

ソース: {Web検索/Exa/特定サイト}
件数: {N}件
保存: /home/claude/info/{topic}_{date}.md

報告: 「{N}件収集。注目ポイント: {要点}」
```

### Template D2: URL内容取得

```
以下のURL群からコンテンツを取得：
{URLリスト}

各URLの内容:
→ /home/claude/urls/{識別子}.md に保存

報告: 「{N}件取得完了。取得失敗: {失敗数}件」
```

### Template D3: 定期更新

```
前回結果（{前回ファイルパス}）と比較して{対象}を更新：

1. 新規検索実行
2. 差分抽出（新規追加/削除/変更）
3. 結果保存: {保存先}

報告: 「更新完了。新規{N}件、削除{M}件、変更{K}件」
```

## テンプレート選択ガイド

| タスク種別 | 推奨テンプレート |
|-----------|-----------------|
| 論文検索 | Template 1 or R1 |
| 企業調査 | Template 2 or R2 |
| 複合調査 | Template 3 or 4 |
| 市場調査 | Template R3 |
| 比較分析 | Template R4 |
| 日常の情報収集 | Template D1 |
| URL群の処理 | Template D2 |
| 定期更新 | Template D3 |
