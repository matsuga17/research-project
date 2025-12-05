# Skill Mapping Reference

## 既存スキル → ツールマッピング

### academic-research-suite
**用途**: 学術研究の全工程支援
**関連ツール**:
- `google-scholar:search_google_scholar_key_words` - 文献検索
- `google-scholar:search_google_scholar_advanced` - 詳細検索
- `semantic-scholar:search_semantic_scholar` - セマンティック検索
- `semantic-scholar:get_semantic_scholar_citations_and_references` - 引用分析

**トリガーキーワード**: 文献レビュー, 論文作成, 引用管理, PRISMA

---

### research-data-hub
**用途**: 研究データの収集・管理
**関連ツール**:
- `desktop-commander:start_process` - Pythonスクリプト実行
- `Filesystem:*` - ローカルファイル操作
- `omnisearch:tavily_search` - Web検索

**外部API**:
- SEC EDGAR (米国企業)
- EDINET (日本企業)
- World Bank API
- IMF Data API

**トリガーキーワード**: データ収集, 企業データ, SEC EDGAR, 財務データ

---

### document-design-suite
**用途**: ドキュメント・可視化作成
**関連スキル**: /mnt/skills/public/docx, xlsx, pptx, pdf
**関連ツール**:
- `view` / `create_file` - ファイル操作
- `desktop-commander:write_file` - 大規模ファイル

**トリガーキーワード**: スライド作成, 表作成, データ可視化, チャート

---

### strategic-research-platform
**用途**: 戦略経営論・組織論の実証研究
**関連ツール**:
- `desktop-commander:start_process` - 統計分析実行
- `think-tank:think` - 理論構築支援
- `Coupler.io:get-data` - データフロー

**分析手法**:
- パネルデータ分析
- イベントスタディ
- 生存分析
- DID / RDD

**トリガーキーワード**: 戦略研究, 実証研究, パネルデータ, 回帰分析

---

### scientific-databases
**用途**: 26+科学データベースへのアクセス
**カテゴリ別DB**:
| カテゴリ | データベース |
|---------|-------------|
| 文献 | PubMed, bioRxiv |
| タンパク質 | UniProt, PDB, AlphaFold, STRING |
| ゲノム | NCBI Gene, Ensembl, ClinVar, COSMIC |
| 薬剤 | DrugBank, ChEMBL, PubChem |
| パスウェイ | KEGG, Reactome |

**トリガーキーワード**: バイオ, ゲノム, 薬剤, タンパク質

---

### thinking-toolkit
**用途**: 思考支援・理論構築
**関連ツール**:
- `think-tank:think` - 構造化推論
- `sequential-thinking:sequentialthinking` - 段階的思考
- `think-tank:exa_search` - 研究検索
- `think-tank:exa_answer` - 質問回答

**トリガーキーワード**: 深く考えて, 多角的分析, 理論構築, ブレインストーミング

---

### content-extractor
**用途**: URLからコンテンツ抽出
**関連ツール**:
- `omnisearch:jina_reader_process` - URL→テキスト
- `omnisearch:tavily_extract_process` - コンテンツ抽出
- `omnisearch:firecrawl_scrape_process` - スクレイピング
- `youtube-transcript:youtube_get_transcript` - YouTube字幕

**トリガーキーワード**: YouTube, 記事抽出, PDF抽出, tapestry

---

## タスク → スキル推薦マトリクス

| タスク | Primary Skill | Secondary | Tools |
|--------|--------------|-----------|-------|
| 文献調査 | academic-research-suite | thinking-toolkit | google-scholar, semantic-scholar |
| データ収集 | research-data-hub | scientific-databases | SEC EDGAR, APIs |
| 論文執筆 | academic-research-suite | document-design-suite | docx |
| プレゼン作成 | document-design-suite | - | pptx |
| 戦略分析 | strategic-research-platform | thinking-toolkit | Python統計 |
| コード開発 | brainstorming | project-planner | desktop-commander |
| Web調査 | content-extractor | - | omnisearch:* |

---

## MCP Server カテゴリ

### Filesystem系
```
Filesystem:read_file, write_file, list_directory, search_files
desktop-commander:read_file, write_file, start_process, edit_block
```

### 検索系
```
omnisearch:tavily_search, brave_search, jina_reader_process
web_search, web_fetch
```

### データベース系
```
Coupler.io:get-data, get-dataflow, get-schema
memory:*, think-tank:upsert_entities, search_nodes
```

### ブラウザ自動化
```
playwright:browser_navigate, browser_click, browser_type, browser_snapshot
```

### 学術検索
```
google-scholar:search_google_scholar_key_words, get_author_info
semantic-scholar:search_semantic_scholar, get_semantic_scholar_paper_details
```

### 思考支援
```
sequential-thinking:sequentialthinking
think-tank:think, exa_search, exa_answer
```

### タスク管理
```
taskmaster-ai:get_tasks, add_task, expand_task, next_task
think-tank:plan_tasks, list_tasks, complete_task
```
