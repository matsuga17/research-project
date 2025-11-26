# Strategic Research Suite - Skill Selection Guide

**どのスキルを使うべきか？このガイドで即座に判断できます**

---

## 🎯 Quick Decision Tree

### あなたの状況はどれ？

#### ❶ 初めての戦略研究 → **1-core-workflow**
- 「Phase 1-8の全体像を理解したい」
- 「研究プロセスの基本を学びたい」
- 「どこから始めればいいかわからない」

➡️ **読み込み**: `1-core-workflow` skill のみ (15k tokens)

---

#### ❷ データ収集が必要 → **2-data-sources**
- 「日本企業の財務データが欲しい」
- 「欧米のガバナンスデータを探している」
- 「無料で使えるグローバルデータソースは？」

➡️ **読み込み**: `1-core-workflow` + `2-data-sources` (15k + 18k = 33k tokens)

---

#### ❸ 統計分析の実装 → **3-statistical-methods**
- 「パネル回帰を実装したい」
- 「内生性の問題をどう対処する？」
- 「IV回帰・PSM・DiDの実装方法は？」

➡️ **読み込み**: `1-core-workflow` + `3-statistical-methods` (15k + 14k = 29k tokens)

---

#### ❹ テキストデータ分析 → **4-text-analysis**
- 「MD&Aのセンチメント分析をしたい」
- 「決算説明会のテキストから戦略テーマを抽出」
- 「Innovation言及と実際のR&D投資の関係」

➡️ **読み込み**: `1-core-workflow` + `4-text-analysis` (15k + 12k = 27k tokens)

---

#### ❺ ネットワーク分析 → **5-network-analysis**
- 「取締役ネットワークの影響を調べたい」
- 「戦略的提携ポートフォリオの測定」
- 「特許引用ネットワークの構築」

➡️ **読み込み**: `1-core-workflow` + `5-network-analysis` (15k + 11k = 26k tokens)

---

#### ❻ 因果推論・機械学習 → **6-causal-ml**
- 「処置効果の異質性を調べたい」
- 「Causal Forest・DMLの実装」
- 「Synthetic Control Methodでイベント分析」

➡️ **読み込み**: `1-core-workflow` + `6-causal-ml` (15k + 10k = 25k tokens)

---

#### ❼ ESG・サステナビリティ研究 → **7-esg-sustainability**
- 「ESG戦略とパフォーマンスの関係」
- 「CDPの気候変動データを使いたい」
- 「環境規制の影響を分析」

➡️ **読み込み**: `1-core-workflow` + `7-esg-sustainability` (15k + 12k = 27k tokens)

---

#### ❽ 完全自動化実行 → **8-automation**
- 「研究プロセス全体を自動化したい」
- 「Phase 1-8を一括実行」
- 「再現可能なパイプラインを構築」

➡️ **読み込み**: `8-automation` skill (8k tokens)
※ automation skillは他のスキルを内部で呼び出すため、単独でOK

---

## 📊 研究テーマ別推奨スキル組み合わせ

### 【テーマ1】競争戦略研究
**例**: 「差別化戦略 vs. コストリーダーシップ戦略のパフォーマンス比較」

**推奨スキル**:
```
1. core-workflow (15k) → 研究設計
2. data-sources (18k) → Compustat財務データ
3. statistical-methods (14k) → 調整効果分析

合計: 47k tokens (旧版比 52%削減)
```

---

### 【テーマ2】イノベーション能力研究
**例**: 「R&D投資とイノベーション成果の関係（日本企業）」

**推奨スキル**:
```
1. core-workflow (15k) → 研究設計
2. data-sources (18k) → EDINET・特許データ
4. text-analysis (12k) → 特許テキスト分析
3. statistical-methods (14k) → パネル回帰

合計: 59k tokens (旧版比 40%削減)
```

---

### 【テーマ3】取締役ネットワークと戦略
**例**: 「Board Interlockが戦略的意思決定に与える影響」

**推奨スキル**:
```
1. core-workflow (15k) → 研究設計
2. data-sources (18k) → ガバナンスデータ
5. network-analysis (11k) → Board Interlock構築
3. statistical-methods (14k) → 統計分析

合計: 58k tokens (旧版比 41%削減)
```

---

### 【テーマ4】ESG戦略のパフォーマンス効果
**例**: 「ESG開示が企業価値に与える因果効果」

**推奨スキル**:
```
1. core-workflow (15k) → 研究設計
7. esg-sustainability (12k) → CDPデータ収集
2. data-sources (18k) → 財務データ
6. causal-ml (10k) → Causal Forest分析

合計: 55k tokens (旧版比 44%削減)
```

---

### 【テーマ5】国際化戦略研究
**例**: 「新興市場参入タイミングと成功要因（アジア市場）」

**推奨スキル**:
```
1. core-workflow (15k) → 研究設計
2. data-sources (18k) → アジア11国データ
3. statistical-methods (14k) → 生存分析

合計: 47k tokens (旧版比 52%削減)
```

---

### 【テーマ6】M&A戦略研究
**例**: 「買収プレミアムとシナジー実現の関係」

**推奨スキル**:
```
1. core-workflow (15k) → 研究設計
2. data-sources (18k) → M&Aデータ (SDC Platinum)
4. text-analysis (12k) → M&A発表テキスト分析
3. statistical-methods (14k) → イベントスタディ

合計: 59k tokens (旧版比 40%削減)
```

---

## 🔍 症状別トラブルシューティング

### 問題: 「どのデータを使えばいいかわからない」
**解決策**: `2-data-sources` skill を読む
- データソース選択マトリックス
- 地域別データカタログ
- 無料 vs. 有料の比較

---

### 問題: 「内生性の問題をどう対処すればいい？」
**解決策**: `3-statistical-methods` skill の「内生性対策」セクション
- Instrumental Variables (IV)
- Propensity Score Matching (PSM)
- Difference-in-Differences (DiD)
- Heckman Selection Model

---

### 問題: 「テキストデータをどう定量化する？」
**解決策**: `4-text-analysis` skill
- センチメント分析の実装
- トピックモデリング (LDA)
- テキスト×財務データの統合

---

### 問題: 「研究全体を効率化したい」
**解決策**: `8-automation` skill
- Phase 1-8の完全自動化
- 再現可能なパイプライン構築
- Docker環境セットアップ

---

## 📈 トークン消費の最適化

### パターン1: 最小構成（初心者）
```
1-core-workflow のみ
消費: 15k tokens
用途: 研究プロセスの理解
```

### パターン2: 標準構成（データ収集）
```
1-core-workflow + 2-data-sources
消費: 33k tokens
用途: データ探索と収集
```

### パターン3: 分析構成（統計実装）
```
1-core-workflow + 3-statistical-methods
消費: 29k tokens
用途: 統計分析の実装
```

### パターン4: 完全構成（複雑な研究）
```
1-core-workflow + 2-data-sources + 
3-statistical-methods + 4-text-analysis
消費: 59k tokens (旧版の60%)
用途: 複合的な分析
```

---

## 💡 使用例（実際のプロンプト）

### 例1: 日本企業データ収集
```
"strategic-research-suite/2-data-sources skillを使って、
EDINETから2020-2023年の製造業データを収集する方法を教えてください"
```

### 例2: パネル回帰の実装
```
"strategic-research-suite/3-statistical-methods skillで、
Fixed Effects回帰を実装してください。クラスタリング標準誤差も含めて"
```

### 例3: MD&A分析
```
"strategic-research-suite/4-text-analysis skillを使って、
SECのMD&Aからforward-looking statementsを抽出してください"
```

### 例4: 完全自動化
```
"strategic-research-suite/8-automation skillで、
R&D投資とパフォーマンスの研究を自動化してください"
```

---

## 🎓 学習経路（習熟度別）

### 【初級】戦略研究入門者
1. `1-core-workflow` を熟読
2. `2-data-sources` でデータ探索を練習
3. `3-statistical-methods` で基本的なパネル回帰を実装

**所要時間**: 1週間  
**トークン消費**: 47k tokens

---

### 【中級】論文執筆中
1. `1-core-workflow` で全体フローを確認
2. 必要な分析手法のスキルを選択的に読む
   - テキスト分析 → `4-text-analysis`
   - ネットワーク分析 → `5-network-analysis`
   - 因果推論 → `6-causal-ml`
3. `3-statistical-methods` でRobustness checks実装

**所要時間**: 2-3日  
**トークン消費**: 40-60k tokens

---

### 【上級】複数プロジェクト管理
1. `8-automation` で自動化パイプライン構築
2. 各プロジェクトに応じたスキルを組み合わせ
3. `_shared/` の共通定義を活用

**所要時間**: 1日  
**トークン消費**: プロジェクト次第

---

## 🔗 Related Resources

- **README.md**: Suite全体の概要
- **USAGE-GUIDE.md**: 詳細使用方法
- **_shared/common-definitions.md**: 共通用語定義
- **_shared/quality-checklist.md**: 品質チェックリスト
- **_shared/cross-references.md**: スキル間参照マップ

---

## ⚠️ よくある間違い

### ❌ 間違い1: すべてのスキルを一度に読み込む
**問題**: トークン消費が大きくなりすぎる  
**正解**: 必要なスキルのみを選択的に読み込む

---

### ❌ 間違い2: core-workflowをスキップ
**問題**: 全体の文脈が理解できず、個別スキルが活かせない  
**正解**: まず `1-core-workflow` を読んで全体像を把握

---

### ❌ 間違い3: データソースを確認せずに分析開始
**問題**: 適切なデータが見つからず、研究が頓挫  
**正解**: Phase 2でデータ探索を徹底（`2-data-sources` 活用）

---

## 📞 サポート

**質問・相談**:
- スキル選択に迷ったら → このガイドのDecision Treeを参照
- トークン消費を最小化したい → 「トークン消費の最適化」セクション参照
- 複雑な研究デザイン → `1-core-workflow` のFAQ参照

---

**最終更新**: 2025-11-01  
**バージョン**: 4.0.0
