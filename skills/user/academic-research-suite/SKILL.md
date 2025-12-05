---
name: academic-research-suite
description: |
  学術研究の全工程を支援する統合スキル。以下の機能を包括：
  (1) 系統的文献レビュー（PRISMA 2020準拠、学術API統合）
  (2) 論文構造設計・執筆支援（30,000字対応）
  (3) 東京大学スタイル準拠の引用・参考文献管理（Tokyo-Cite）
  (4) 情報信頼性検証・品質保証（TrustGuard）
  トリガー：「文献レビュー」「論文作成」「引用管理」「参考文献」「PRISMA」「系統的レビュー」
allowed-tools: Bash,Read,Write,WebFetch,WebSearch
---

# Academic Research Suite - 学術研究統合スキル

## 概要

学術研究プロセスを包括的に支援する統合スキルです。文献レビューから論文執筆、引用管理、品質検証までの全工程をカバーします。

**統合元スキル**：
- literature-review-engine（系統的文献レビュー）
- academic-paper-30k-creator（論文構造・執筆）
- academic-paper-creation（論文作成支援）
- tokyo-cite（引用・参考文献管理）
- trust-guard（信頼性検証・品質保証）

## When to Use This Skill

以下の場合にこのスキルを使用：

- 系統的文献レビューの実施
- 先行研究サーベイの作成
- 学術論文の構造設計・執筆
- 引用・参考文献の管理と検証
- 情報の信頼性検証・ファクトチェック

**トリガーキーワード**：
- 「文献レビュー」「系統的レビュー」「Systematic Review」「PRISMA」
- 「論文作成」「論文執筆」「アカデミックライティング」
- 「引用管理」「参考文献」「Citation」「Tokyo-Cite」
- 「信頼性検証」「ファクトチェック」「TrustGuard」

---

# Part 1: 系統的文献レビュー

## 1.1 PICO/PICOSフレームワーク

### 研究課題の構造化

```
P - Population/Problem（対象集団/問題）
    誰について？どのような問題？
    例：「日本の製造業企業」「スタートアップ」

I - Intervention/Exposure（介入/曝露）
    どのような介入/要因？
    例：「デジタルトランスフォーメーション」「CEO交代」

C - Comparison（比較対照）
    何と比較？
    例：「DX未実施企業」「内部昇進CEO」

O - Outcome（アウトカム）
    どのような結果？
    例：「企業業績」「イノベーション成果」

S - Study Design（研究デザイン）[オプション]
    どのような研究デザイン？
    例：「パネルデータ分析」「ケーススタディ」
```

### PICO定義テンプレート

```
研究課題: [リサーチクエスチョン]

PICO要素：
┌─────────────┬──────────────────────────────────┐
│ P (対象)    │                                  │
├─────────────┼──────────────────────────────────┤
│ I (介入)    │                                  │
├─────────────┼──────────────────────────────────┤
│ C (比較)    │                                  │
├─────────────┼──────────────────────────────────┤
│ O (結果)    │                                  │
└─────────────┴──────────────────────────────────┘

検索キーワード候補：
- P関連: [キーワードリスト]
- I関連: [キーワードリスト]
- O関連: [キーワードリスト]
```

## 1.2 検索式の構築

### ブール演算子の使用

```
基本構造：
(P関連キーワード) AND (I関連キーワード) AND (O関連キーワード)

例：戦略的人的資源管理と企業業績
("strategic human resource management" OR "SHRM" OR "high performance work system*")
AND
("firm performance" OR "organizational performance" OR "financial performance")
AND
("empirical" OR "quantitative" OR "panel data")
```

### 主要学術データベース

| データベース | 対象分野 | アクセス | 特徴 |
|-------------|---------|---------|------|
| Web of Science | 全分野 | 有料 | 引用分析に強い |
| Scopus | 全分野 | 有料 | 広いカバレッジ |
| EBSCO Business Source | 経営学 | 有料 | 経営学専門 |
| Google Scholar | 全分野 | 無料 | 網羅的だが質にばらつき |
| OpenAlex | 全分野 | 無料API | オープンアクセス |
| Semantic Scholar | 全分野 | 無料API | AI活用、引用分析 |
| CiNii | 日本語文献 | 無料 | 日本学術文献 |

## 1.3 PRISMAフローダイアグラム（PRISMA 2020）

```
┌─────────────────────────────────────────────────────────┐
│                    IDENTIFICATION                        │
├─────────────────────────────────────────────────────────┤
│ データベース検索による特定 (n = ____)                     │
│ その他の情報源から特定                                   │
│ ├── 引用検索 (n = ____)                                │
│ ├── ハンドサーチ (n = ____)                            │
│ └── その他 (n = ____)                                  │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                     SCREENING                            │
├─────────────────────────────────────────────────────────┤
│ 重複除去後の文献 (n = ____)                             │
│                           ↓                             │
│ タイトル・抄録スクリーニング (n = ____)                  │
│ → 除外 (n = ____)                                       │
│                           ↓                             │
│ 全文評価対象 (n = ____)                                 │
│ → 除外 (n = ____) [除外理由を記録]                       │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                      INCLUDED                            │
├─────────────────────────────────────────────────────────┤
│ 最終採用文献 (n = ____)                                 │
│ ├── 定量研究 (n = ____)                                │
│ └── 定性研究 (n = ____)                                │
└─────────────────────────────────────────────────────────┘
```

## 1.4 品質評価ツール

### Newcastle-Ottawa Scale (NOS) - 観察研究用

```
評価領域           最大スコア
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Selection           ★★★★ (4点)
Comparability       ★★ (2点)
Outcome             ★★★ (3点)
━━━━━━━━━━━━━━━━━━━━━━━━━━━
合計               9点満点

品質判定：高品質(7-9点)、中品質(4-6点)、低品質(0-3点)
```

### GRADE評価フレームワーク

```
⊕⊕⊕⊕ 高い確実性
⊕⊕⊕◯ 中程度の確実性
⊕⊕◯◯ 低い確実性
⊕◯◯◯ 非常に低い確実性
```

## 1.5 学術データベースAPI統合

### OpenAlex API

```python
import requests

def search_openalex(query, filters=None, max_results=100):
    """OpenAlex APIで文献検索"""
    base_url = "https://api.openalex.org/works"
    params = {
        "search": query,
        "per_page": 25,
        "mailto": "your-email@university.edu"
    }
    if filters:
        params["filter"] = filters

    results = []
    cursor = "*"
    while len(results) < max_results:
        params["cursor"] = cursor
        response = requests.get(base_url, params=params)
        data = response.json()
        if not data.get("results"):
            break
        results.extend(data["results"])
        cursor = data["meta"].get("next_cursor")
        if not cursor:
            break
    return results[:max_results]
```

### Semantic Scholar API

```python
def search_semantic_scholar(query, year_range=None, limit=100):
    """Semantic Scholar APIで文献検索"""
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": min(limit, 100),
        "fields": "paperId,title,abstract,year,citationCount,authors,venue"
    }
    if year_range:
        params["year"] = year_range
    response = requests.get(base_url, params=params)
    return response.json()
```

## 1.6 引用ネットワーク分析

```python
import networkx as nx

def analyze_citation_network(papers):
    """引用ネットワークの分析"""
    G = nx.DiGraph()
    for paper in papers:
        G.add_node(paper["id"], title=paper["title"], year=paper["year"])
    for paper in papers:
        for ref in paper.get("references", []):
            if ref in G.nodes():
                G.add_edge(paper["id"], ref)

    return {
        "total_papers": G.number_of_nodes(),
        "pagerank": nx.pagerank(G),
        "betweenness": nx.betweenness_centrality(G)
    }
```

---

# Part 2: 論文構造設計・執筆支援

## 2.1 学術論文の基本構造

### IMRaD形式（科学論文標準）

```
1. Introduction（序論）
   - 研究背景・問題設定
   - 先行研究レビュー
   - 研究目的・リサーチクエスチョン
   - 論文構成の予告

2. Methods（方法）
   - 研究デザイン
   - データ収集方法
   - 分析手法
   - 倫理的配慮

3. Results（結果）
   - 記述統計
   - 分析結果
   - 図表の提示

4. Discussion（考察）
   - 結果の解釈
   - 理論的含意
   - 実践的含意
   - 限界と今後の課題

5. Conclusion（結論）
   - 主要発見のまとめ
   - 貢献
```

## 2.2 30,000字論文の分量配分

```
セクション          推奨比率    文字数目安
-------------------------------------------
序論                10-15%      3,000-4,500字
理論・先行研究      20-25%      6,000-7,500字
方法                10-15%      3,000-4,500字
結果・分析          25-30%      7,500-9,000字
考察                15-20%      4,500-6,000字
結論                5-10%       1,500-3,000字
```

## 2.3 執筆プロセス

```
[Phase 1: 計画]
├── リサーチクエスチョン設定
├── 文献レビュー（Part 1を使用）
└── アウトライン作成

[Phase 2: 執筆]
├── 各セクションのドラフト作成
├── 引用の配置（Tokyo-Cite形式）
└── 図表の作成・配置

[Phase 3: 検証]
├── TrustGuard信頼性検証
├── 引用の完全性チェック
└── 論理的整合性の確認

[Phase 4: 完成]
├── 推敲・編集
├── 最終フォーマット調整
└── 参考文献リスト生成
```

---

# Part 3: 引用・参考文献管理（Tokyo-Cite）

## 3.1 東京大学スタイル引用形式

### 日本語文献の基本形式

**書籍**：
```
著者名（出版年）『書名』出版社。
例：山田太郎（2020）『経営戦略論』東京大学出版会。
```

**論文（学術誌）**：
```
著者名（出版年）「論文タイトル」『雑誌名』巻（号）、開始ページ-終了ページ。
例：佐藤花子（2021）「組織変革の実証分析」『組織科学』54（3）、45-62。
```

### 英語文献の基本形式

**書籍**：
```
Last, F. M. (Year). Title of book. Publisher.
例：Porter, M. E. (1980). Competitive strategy. Free Press.
```

**論文（学術誌）**：
```
Last, F. M. (Year). Title of article. Journal Name, Volume(Issue), pages.
例：Barney, J. B. (1991). Firm resources and sustained competitive advantage. Journal of Management, 17(1), 99-120.
```

## 3.2 本文中の引用

### 著者名・年方式

```
単著：山田（2020）は〜 / 〜である（山田, 2020）。
2名：山田・佐藤（2020）/ Barney & Hesterly (2020)
3名以上（初出）：山田・佐藤・田中（2020）
3名以上（2回目以降）：山田ほか（2020）/ Barney et al. (2020)
複数引用：（山田, 2020; 佐藤, 2021）
```

## 3.3 引用検証プロトコル

### 自動検証項目

1. **形式の一貫性** - 句読点、括弧、イタリック/ボールドの統一
2. **完全性チェック** - 本文中の引用 ↔ 参考文献の対応
3. **DOI/URL検証** - リンクの有効性確認

---

# Part 4: 情報信頼性検証（TrustGuard）

## 4.1 信頼性評価フレームワーク

### 5段階評価スケール

```
Level 5 (最高信頼性): 査読付き学術誌、政府統計
Level 4 (高信頼性): 学術書籍、主要研究機関レポート
Level 3 (中程度): 専門家ブログ、業界レポート
Level 2 (低信頼性): ニュース記事、一般Webサイト
Level 1 (要検証): SNS、ウィキペディア、未検証情報
```

### 情報源の評価基準

```
基準              チェック項目
------------------------------------------------
著者の専門性      学位、所属機関、研究実績
査読プロセス      ピアレビューの有無
データの透明性    方法論の開示、データアクセス
引用の質          一次資料への参照
更新性            情報の新しさ、最終更新日
利益相反          資金源、スポンサー開示
```

## 4.2 ファクトチェック手順

```
Step 1: 主張の特定 → 検証すべき事実的主張を抽出
Step 2: 一次資料の確認 → 原典にあたり、文脈を確認
Step 3: クロスリファレンス → 複数の独立した情報源で確認
Step 4: 結果の報告

[TrustGuard検証結果]
- 主張: [検証した主張]
- 判定: [正確/部分的に正確/不正確/検証不能]
- 根拠: [判定の理由]
- 信頼度: [Level 1-5]
- 推奨: [修正案または追加調査の必要性]
```

## 4.3 学術論文品質チェックリスト

### 内容面
- [ ] リサーチクエスチョンが明確
- [ ] 方法論が適切で再現可能
- [ ] 結果が主張を支持している
- [ ] 限界が適切に述べられている

### 形式面
- [ ] 引用形式の一貫性
- [ ] 参考文献の完全性
- [ ] 図表の適切な番号付け

### 倫理面
- [ ] 剽窃がない
- [ ] 適切な許可・承認の取得
- [ ] 利益相反の開示

---

# Part 5: 起動コマンド

## 文献レビューモード
```
Academic Research Suite起動

目的: 文献レビュー
研究課題: [リサーチクエスチョン]
PICO:
  P: [対象]
  I: [介入]
  C: [比較]
  O: [結果]
プロトコル: PRISMA 2020
出力: [PRISMAフロー/文献リスト/品質評価表]
```

## 論文作成モード
```
Academic Research Suite起動

目的: 論文作成
テーマ: [研究テーマ]
目標文字数: [30,000字など]
引用形式: 東京大学スタイル
出力: [論文ドラフト]
```

## 引用管理モード
```
Tokyo-Cite起動

入力: [引用リストまたは本文]
形式: 東京大学スタイル
検証: [はい/いいえ]
出力: [整形された参考文献リスト]
```

## 信頼性検証モード
```
TrustGuard起動

対象: [検証対象の文章・主張]
検証レベル: [簡易/標準/詳細]
出力: [検証レポート]
```

---

## 連携スキル

| スキル名 | 役割 |
|----------|------|
| strategic-research-platform | 戦略・組織論の実証研究支援 |
| research-data-hub | 研究データ収集・管理 |
| thinking-toolkit | 理論構築・批判的思考支援 |
| document-design-suite | 図表・可視化作成 |
| code-quality-guardian | 再現性パッケージ作成 |
| content-extractor | PDF論文のテキスト抽出 |

---

## 品質基準

### 文献レビュー基準
- [ ] 複数データベースを使用
- [ ] PRISMAフロー作成
- [ ] 品質評価ツール使用

### 論文執筆基準
- [ ] 引用形式の一貫性
- [ ] 参考文献の完全性
- [ ] 基本的なファクトチェック

### 卓越基準
- [ ] 査読論文レベルの品質
- [ ] 完全な再現可能性
- [ ] 包括的な信頼性検証

---

**バージョン**: 2.0.0
**統合日**: 2025-11-28
**統合元**: literature-review-engine, academic-paper-30k-creator, academic-paper-creation, tokyo-cite, trust-guard
