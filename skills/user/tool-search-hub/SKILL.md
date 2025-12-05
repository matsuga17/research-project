---
name: tool-search-hub
description: |
  統合型ツール検索・推薦システム。以下の機能を包括：
  (1) MCPツール動的検索：利用可能なMCPツールをクエリベースで検索・フィルタリング
  (2) スキル内ツール選択：ユーザーリクエストに基づく最適ツール推薦とパラメータ提示
  (3) 外部ライブラリ検索：npm/PyPI/GitHub/crates.io等から技術選定支援
  (4) 検索ツール最適化：Tavily/Brave/Exa等の効果的な使い分けガイド
  トリガー：「ツール検索」「どのツールを使う」「ライブラリ探して」「MCP一覧」「技術選定」「API検索」
---

# Tool Search Hub

統合型ツール検索・推薦システム。研究・開発ワークフローにおける最適ツール選択を支援。

## クイックスタート

### 1. MCPツール検索
```
search_mcp_tools("file")      → ファイル関連ツール一覧
search_mcp_tools("database")  → DB関連ツール一覧
```

### 2. タスクベース推薦
```
recommend_tools("PDFからテキスト抽出") → pdf skill + pdfplumber
recommend_tools("企業財務データ収集")  → research-data-hub + SEC EDGAR
```

### 3. ライブラリ検索
```
search_libraries("python pdf parsing")     → PyMuPDF, pdfplumber, PyPDF2
search_libraries("react state management") → Zustand, Jotai, Redux
```

## アーキテクチャ

```
┌─────────────────────────────────────────────────────────┐
│                   Tool Search Hub                        │
├─────────────┬─────────────┬─────────────┬───────────────┤
│  MCP Tools  │  Skills     │  Libraries  │  Search APIs  │
│  Discovery  │  Selector   │  Finder     │  Optimizer    │
├─────────────┴─────────────┴─────────────┴───────────────┤
│              Unified Query Interface                     │
└─────────────────────────────────────────────────────────┘
```

## モジュール詳細

### Module 1: MCP Tools Discovery

**目的**: 現在接続中のMCPサーバーから利用可能なツールを動的に検索

**実装パターン**:
```python
# scripts/mcp_tool_scanner.py を使用
python scripts/mcp_tool_scanner.py --query "file" --category "filesystem"
```

**カテゴリ分類**:
| カテゴリ | ツール例 | 用途 |
|---------|---------|------|
| filesystem | read_file, write_file, list_directory | ファイル操作 |
| search | web_search, tavily_search, brave_search | 情報検索 |
| database | Coupler.io:get-data, memory:* | データ管理 |
| browser | playwright:* | Web自動化 |
| analysis | sequential-thinking, think-tank:* | 思考支援 |
| research | google-scholar:*, semantic-scholar:* | 学術検索 |

**出力フォーマット**:
```json
{
  "query": "file",
  "matches": [
    {
      "tool": "Filesystem:read_file",
      "description": "Read file contents",
      "category": "filesystem",
      "relevance": 0.95
    }
  ],
  "total": 15
}
```

### Module 2: Skills Selector

**目的**: ユーザータスクに最適なClaudeスキルとツールの組み合わせを推薦

**スキルマッピング** (references/skill-mapping.md 参照):

| タスク種別 | 推奨スキル | 主要ツール |
|-----------|-----------|-----------|
| 文献レビュー | academic-research-suite | google-scholar, semantic-scholar |
| データ収集 | research-data-hub | SEC EDGAR, 企業DB |
| 文書作成 | document-design-suite | docx, pptx, xlsx |
| 戦略分析 | strategic-research-platform | パネル分析, 回帰 |
| 思考整理 | thinking-toolkit | think-tank:think |

**推薦ロジック**:
1. タスク意図解析（キーワード + コンテキスト）
2. スキル候補スコアリング
3. ツールチェーン構築
4. パラメータテンプレート生成

### Module 3: Libraries Finder

**目的**: npm/PyPI/GitHub/crates.io等から最適ライブラリを検索・比較

**検索エンドポイント**:
```
# Python
https://pypi.org/search/?q={query}
https://libraries.io/api/search?q={query}&platforms=pypi

# JavaScript/TypeScript  
https://registry.npmjs.org/-/v1/search?text={query}
https://api.npms.io/v2/search?q={query}

# Rust
https://crates.io/api/v1/crates?q={query}

# GitHub
https://api.github.com/search/repositories?q={query}
```

**比較基準**:
- ⭐ GitHub Stars / Downloads
- 📅 最終更新日
- 📦 依存関係数
- 📖 ドキュメント品質
- 🔒 セキュリティ評価

**出力例**:
```markdown
## PDF Parsing Libraries (Python)

| Library | Stars | Downloads/mo | Last Update | Recommendation |
|---------|-------|--------------|-------------|----------------|
| PyMuPDF | 4.2k | 2.1M | 2025-05 | ⭐ 高速・多機能 |
| pdfplumber | 6.1k | 1.8M | 2025-04 | ⭐ テーブル抽出最強 |
| PyPDF2 | 7.8k | 3.2M | 2025-03 | 基本操作向け |
```

### Module 4: Search APIs Optimizer

**目的**: 複数の検索APIを目的別に最適化して使い分け

**検索API比較**:

| API | 強み | 弱み | 最適用途 |
|-----|------|------|---------|
| **Tavily** | 高精度、引用付き | レート制限 | 学術・技術クエリ |
| **Brave** | プライバシー、演算子対応 | 深さ限定 | 技術ドキュメント |
| **Exa** | セマンティック検索 | コスト高 | 研究論文発見 |
| **Google Scholar** | 学術網羅性 | API制限 | 文献調査 |
| **Semantic Scholar** | 引用ネットワーク | 最新論文遅延 | 引用分析 |

**クエリルーティング**:
```
学術論文 → google-scholar + semantic-scholar
技術ドキュメント → brave_search(site:docs.*)
最新ニュース → tavily_search
コード例 → brave_search(site:github.com OR site:stackoverflow.com)
企業情報 → tavily_search + research-data-hub
```

## 統合検索ワークフロー

### 基本フロー
```
1. クエリ解析
   ↓
2. 検索タイプ判定（MCP/Skill/Library/Web）
   ↓
3. 適切なモジュール呼び出し
   ↓
4. 結果統合・ランキング
   ↓
5. 推薦出力
```

### 複合クエリ例

**「Pythonでエクセルファイルを読み込んでグラフ作成」**:
```
→ Module 2 (Skills): document-design-suite/xlsx
→ Module 3 (Libraries): openpyxl, pandas, matplotlib
→ Module 1 (MCP): desktop-commander:start_process
→ 統合推薦: pandas + matplotlib, xlsx skill参照
```

## スクリプト

### scripts/mcp_tool_scanner.py
MCPツール動的スキャン・検索

### scripts/library_search.py  
マルチプラットフォームライブラリ検索

### scripts/search_router.py
クエリ解析・ルーティング

## 使用例

### 例1: MCPツール検索
```
User: ファイル関連のツールを探して
Claude: [mcp_tool_scanner実行]
→ Filesystem:*, desktop-commander:read_file等を表示
```

### 例2: タスクベース推薦
```
User: 論文のための企業データ収集方法を教えて
Claude: [skills_selector + search_router実行]
→ research-data-hub skill + SEC EDGAR API + データ収集テンプレート
```

### 例3: ライブラリ比較
```
User: Pythonの最新PDF処理ライブラリを比較して
Claude: [library_search実行]
→ PyMuPDF vs pdfplumber vs borb の詳細比較表
```

## 拡張ポイント

1. **カスタムMCPサーバー追加**: references/custom-mcp.md
2. **新規スキル統合**: references/skill-integration.md
3. **検索API追加**: scripts/search_router.py を編集
