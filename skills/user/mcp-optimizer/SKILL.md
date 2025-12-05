---
name: mcp-optimizer
description: |
  MCPツール利用の効率化・最適化スキル。以下の機能を提供：
  (1) Prompt Optimizer：通常プロンプトをコンテキスト効率化版に変換
  (2) Workflow Integrator：複数ステップタスクを最適化ワークフローに統合
  (3) Context Monitor：コンテキスト消費評価と改善提案
  トリガー：「MCP最適化」「コンテキスト効率化」「トークン節約」「結果をファイルに」「ワークフロー効率化」「動的ツール選択」
  大量データ処理、複数ツール呼び出し、反復タスク時に自動適用推奨。
  tool-search-hubの補完スキル（何を使うか→どう効率的に使うか）。
---

# MCP Optimizer

MCPツール利用を最適化し、コンテキスト消費を50-80%削減するスキル。

## クイックスタート

### 即座に使える3つのコマンド

```
「このプロンプトをMCP最適化して」
→ Mode 1: Prompt Optimizer が起動

「このタスクのワークフローを効率化して」
→ Mode 2: Workflow Integrator が起動

「現在のコンテキスト効率を評価して」
→ Mode 3: Context Monitor が起動
```

## 解決する3つの問題

| 問題 | 原因 | 解決策 |
|------|------|--------|
| コンテキスト窓の圧迫 | 使わないツール定義の常時ロード | 動的ツール選択パターン |
| 中間結果の肥大化 | 全データがコンテキストに返却 | 結果のファイル保存パターン |
| 非効率なツール呼び出し | 個別・反復的な呼び出し | ワークフロー統合パターン |

## Mode 1: Prompt Optimizer

通常のプロンプトをコンテキスト効率化版に変換。

### 変換ルール

1. **ファイル保存指示の追加**: 検索・収集結果は必ずファイルに保存
2. **返却情報の限定**: 必要最小限の情報のみ返却指示
3. **段階的実行への分割**: 大きなタスクはフェーズ分割

### 変換例

**Before（非効率）**:
```
dynamic capabilitiesの論文を10件検索して分析して
```

**After（最適化）**:
```
dynamic capabilitiesの論文を10件検索して、
/home/claude/papers/dc_search.csv に以下の形式で保存：
| タイトル | 著者 | 年 | 引用数 | DOI |

私には「○件発見。引用数トップ3は...」とだけ報告。
詳細分析は私が「分析して」と言ったら実行。
```

### 適用パターン一覧

| 元のパターン | 最適化パターン |
|-------------|---------------|
| 「〇〇を検索して」 | 「〇〇を検索して{path}に保存。件数だけ報告」 |
| 「〇〇を分析して」 | 「〇〇を分析して{path}に保存。結論だけ報告」 |
| 「〇〇について調べて」 | 「〇〇を調査して{path}に保存。要点3つだけ報告」 |
| 「〇〇のリストを作って」 | 「〇〇のリストを{path}に保存。総数だけ報告」 |

詳細パターン → references/patterns.md



## Mode 2: Workflow Integrator

複数ステップのタスクを最適化されたワークフローに変換。

### 統合原則

1. **フェーズ分割**: 収集→分析→出力の3フェーズ構造
2. **中間保存**: 各フェーズ結果はファイルに保存
3. **最小報告**: 進捗は完了通知のみ、詳細は最終フェーズで

### ワークフロー変換例

**Before（非効率）**:
```
5社の企業情報を調べて比較表を作成して
```

**After（最適化ワークフロー）**:
```
以下のワークフローで実行してください：

【Phase 1: データ収集】
対象: Alibaba, Coupang, Sea Limited, Flipkart, Tokopedia
保存: /home/claude/companies/{企業名}.json
報告: 「5社収集完了」のみ

【Phase 2: 比較分析】※Phase 1完了後に「続けて」で実行
保存: /home/claude/analysis/comparison.md
報告: 「分析完了。主要差異は○○」のみ

【Phase 3: 表作成】※Phase 2完了後に「続けて」で実行
出力: アーティファクトで比較表生成
```

### ワークフローテンプレート

#### 文献レビュー用
```
【Phase 1: 検索】
キーワード: {keywords}
保存: /home/claude/literature/{topic}.csv
報告: 件数のみ

【Phase 2: スクリーニング】
基準: 引用数{n}以上、{year}年以降
保存: /home/claude/literature/{topic}_filtered.csv
報告: 絞り込み後件数のみ

【Phase 3: 詳細分析】
対象: 上位{n}件のアブストラクト取得
保存: /home/claude/literature/{topic}_abstracts.md
報告: 主要テーマ3つ
```

#### データ収集用
```
【Phase 1: ソース特定】
対象: {data_sources}
保存: /home/claude/data/sources.md
報告: 利用可能ソース数

【Phase 2: データ取得】
保存: /home/claude/data/{source_name}/
報告: 取得成功/失敗の件数

【Phase 3: 統合・検証】
保存: /home/claude/data/integrated.csv
報告: 総レコード数と欠損率
```

詳細テンプレート → references/templates.md

## Mode 3: Context Monitor

現在のタスクのコンテキスト効率を評価し、改善提案を生成。

### 評価チェックリスト

```
□ ツール呼び出し回数: 3回以上 → 統合検討
□ 返却データサイズ: 大量 → ファイル保存検討
□ 反復パターン: 検出 → バッチ処理検討
□ 未使用情報: 多い → 返却情報の限定検討
```

### コンテキスト消費推定

| 要素 | 推定トークン | 最適化後 |
|------|-------------|---------|
| ツール定義（10ツール） | ~5,000 | ~500（使用ツールのみ） |
| 検索結果（10件全文） | ~8,000 | ~800（タイトルのみ） |
| 中間分析結果 | ~3,000 | ~300（要約のみ） |
| **合計** | **~16,000** | **~1,600（90%削減）** |

### 改善提案の出力形式

```
【現状評価】
- 推定コンテキスト消費: XX,XXXトークン
- 非効率パターン検出: Y件

【改善提案】
1. {具体的な改善アクション1}
2. {具体的な改善アクション2}

【最適化後の推定】
- 推定コンテキスト消費: X,XXXトークン
- 削減率: XX%
```



## 既存スキルとの連携

### 連携アーキテクチャ

```
ユーザータスク
      ↓
tool-search-hub: 「どのツール/スキルを使うか」
      ↓
mcp-optimizer: 「どう効率的に使うか」 ← 本スキル
      ↓
各ドメインスキル: 最適化パターンで実行
```

### スキル別最適化パターン

| 連携スキル | 最適化内容 |
|-----------|-----------|
| **academic-research-suite** | 論文検索結果をCSV保存、アブストラクトは選択的取得 |
| **research-data-hub** | 企業データをJSON保存、サマリーのみ返却 |
| **strategic-research-platform** | 分析結果をファイル保存、結論のみ返却 |
| **document-design-suite** | 素材をファイル収集後、一括で文書生成 |

詳細 → references/tool-combinations.md

## ファイル保存の命名規則

### 標準ディレクトリ構造

```
/home/claude/
├── papers/          # 論文関連
├── companies/       # 企業データ
├── data/            # 一般データ
├── analysis/        # 分析結果
├── literature/      # 文献レビュー
└── temp/            # 一時ファイル
```

### 命名パターン

| データ種別 | 命名規則 | 例 |
|-----------|---------|-----|
| 検索結果 | `{topic}_search.csv` | `dc_search.csv` |
| 企業データ | `{company_name}.json` | `alibaba.json` |
| 分析結果 | `{topic}_analysis.md` | `market_analysis.md` |
| 比較表 | `{topic}_comparison.md` | `platform_comparison.md` |
| 統合データ | `integrated_{date}.csv` | `integrated_20251204.csv` |

## クイックリファレンス：最適化フレーズ

### 検索系タスク
```
「{対象}を検索して/home/claude/{path}に保存。{要約}だけ教えて」
```

### 収集系タスク
```
「{N}件の{対象}を収集して/home/claude/{folder}/に個別保存。完了報告だけ」
```

### 分析系タスク
```
「{対象}を分析して/home/claude/{path}に保存。結論を3点で報告」
```

### 複合タスク
```
「以下をフェーズ実行：
Phase 1: {収集} → {path1} → 完了報告のみ
Phase 2: {分析} → {path2} → 完了報告のみ
Phase 3: {出力} → アーティファクト
各フェーズは「続けて」で進行」
```

## 参照ファイル

| ファイル | 内容 |
|---------|------|
| references/patterns.md | 最適化パターン詳細集 |
| references/templates.md | プロンプトテンプレート集 |
| references/workflows.md | ワークフロー最適化例 |
| references/tool-combinations.md | ツール組み合わせガイド |

## スクリプト

| スクリプト | 機能 |
|-----------|------|
| scripts/optimize_prompt.py | プロンプト最適化変換 |
| scripts/context_estimator.py | コンテキスト消費推定 |
| scripts/workflow_generator.py | ワークフローテンプレート生成 |
