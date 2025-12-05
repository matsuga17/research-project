#!/usr/bin/env python3
"""
Search Router - 統合クエリルーティング・検索最適化

Usage:
    python search_router.py --query "PDFからテキスト抽出"
    python search_router.py --query "最新のAI論文" --mode research
    python search_router.py --analyze "企業財務データ収集方法"
"""

import argparse
import json
import re
from dataclasses import dataclass, asdict
from typing import Optional
from enum import Enum

# ============================================================
# Query Classification
# ============================================================

class QueryType(Enum):
    MCP_TOOL = "mcp_tool"           # MCPツール検索
    SKILL = "skill"                  # スキル推薦
    LIBRARY = "library"              # ライブラリ検索
    WEB_SEARCH = "web_search"        # Web検索
    ACADEMIC = "academic"            # 学術検索
    CODE = "code"                    # コード検索
    DATA = "data"                    # データ収集
    COMPOSITE = "composite"          # 複合クエリ

@dataclass
class QueryAnalysis:
    original: str
    type: QueryType
    keywords: list[str]
    suggested_tools: list[str]
    suggested_skills: list[str]
    search_strategy: str
    confidence: float

# ============================================================
# Keyword Patterns
# ============================================================

PATTERNS = {
    QueryType.MCP_TOOL: [
        r"ツール.*検索", r"tool.*search", r"mcp.*一覧",
        r"どの.*ツール", r"利用可能な.*ツール",
    ],
    QueryType.SKILL: [
        r"スキル", r"skill", r"どうすれば", r"方法",
        r"やり方", r"手順", r"ワークフロー",
    ],
    QueryType.LIBRARY: [
        r"ライブラリ", r"パッケージ", r"library", r"package",
        r"npm", r"pip", r"インストール", r"比較",
    ],
    QueryType.ACADEMIC: [
        r"論文", r"研究", r"paper", r"research", r"引用",
        r"文献", r"学術", r"journal", r"scholar",
    ],
    QueryType.CODE: [
        r"コード", r"実装", r"code", r"スクリプト",
        r"python", r"javascript", r"typescript",
    ],
    QueryType.DATA: [
        r"データ.*収集", r"データセット", r"api.*取得",
        r"企業.*データ", r"財務.*データ", r"scraping",
    ],
}

# ============================================================
# Tool/Skill Mappings
# ============================================================

KEYWORD_TO_TOOLS = {
    "pdf": ["view", "desktop-commander:read_file", "omnisearch:jina_reader_process"],
    "excel": ["desktop-commander:start_process", "Filesystem:read_file"],
    "web": ["omnisearch:tavily_search", "omnisearch:brave_search", "web_search"],
    "browser": ["playwright:browser_navigate", "playwright:browser_click"],
    "file": ["Filesystem:read_file", "desktop-commander:read_file", "view"],
    "search": ["omnisearch:tavily_search", "think-tank:exa_search", "web_search"],
    "youtube": ["youtube-transcript:youtube_get_transcript"],
    "論文": ["google-scholar:search_google_scholar_key_words", "semantic-scholar:search_semantic_scholar"],
    "research": ["google-scholar:search_google_scholar_key_words", "semantic-scholar:search_semantic_scholar"],
    "memory": ["think-tank:upsert_entities", "memory:create_entities"],
    "task": ["taskmaster-ai:add_task", "think-tank:plan_tasks"],
    "think": ["think-tank:think", "sequential-thinking:sequentialthinking"],
    "データ": ["Coupler.io:get-data", "desktop-commander:start_process"],
}

KEYWORD_TO_SKILLS = {
    "論文": ["academic-research-suite"],
    "文献": ["academic-research-suite"],
    "research": ["academic-research-suite", "strategic-research-platform"],
    "データ収集": ["research-data-hub"],
    "企業": ["research-data-hub"],
    "財務": ["research-data-hub", "strategic-research-platform"],
    "スライド": ["document-design-suite"],
    "プレゼン": ["document-design-suite"],
    "表": ["document-design-suite"],
    "グラフ": ["document-design-suite"],
    "戦略": ["strategic-research-platform"],
    "分析": ["strategic-research-platform", "thinking-toolkit"],
    "考え": ["thinking-toolkit"],
    "youtube": ["content-extractor"],
    "url": ["content-extractor"],
    "pdf": ["document-design-suite"],
    "バイオ": ["scientific-databases"],
    "ゲノム": ["scientific-databases"],
}

# ============================================================
# Search API Recommendations
# ============================================================

SEARCH_STRATEGIES = {
    "academic": {
        "primary": ["google-scholar:search_google_scholar_key_words"],
        "secondary": ["semantic-scholar:search_semantic_scholar"],
        "fallback": ["think-tank:exa_search"],
        "description": "学術論文検索: Google Scholar → Semantic Scholar → Exa"
    },
    "technical": {
        "primary": ["omnisearch:brave_search"],
        "secondary": ["omnisearch:tavily_search"],
        "fallback": ["web_search"],
        "description": "技術ドキュメント検索: Brave (site:演算子) → Tavily → 汎用検索"
    },
    "news": {
        "primary": ["omnisearch:tavily_search"],
        "secondary": ["web_search"],
        "fallback": ["think-tank:exa_search"],
        "description": "最新ニュース: Tavily (高精度) → Web検索 → Exa"
    },
    "code": {
        "primary": ["omnisearch:brave_search"],
        "secondary": ["Context7:get-library-docs"],
        "fallback": ["web_search"],
        "description": "コード検索: Brave (site:github.com) → Context7 → 汎用検索"
    },
    "company": {
        "primary": ["omnisearch:tavily_search"],
        "secondary": ["web_search"],
        "fallback": ["research-data-hub (SEC EDGAR)"],
        "description": "企業情報: Tavily → Web検索 → SEC EDGAR API"
    },
    "general": {
        "primary": ["web_search"],
        "secondary": ["omnisearch:tavily_search"],
        "fallback": ["omnisearch:brave_search"],
        "description": "一般検索: 汎用検索 → Tavily → Brave"
    }
}

# ============================================================
# Query Analyzer
# ============================================================

def classify_query(query: str) -> QueryType:
    """クエリタイプを分類"""
    query_lower = query.lower()
    
    scores = {qt: 0 for qt in QueryType}
    
    for query_type, patterns in PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, query_lower, re.IGNORECASE):
                scores[query_type] += 1
    
    # 複数タイプが高スコアなら複合
    high_scores = [qt for qt, score in scores.items() if score > 0]
    if len(high_scores) > 1:
        return QueryType.COMPOSITE
    elif high_scores:
        return high_scores[0]
    
    # デフォルト判定
    if any(kw in query_lower for kw in ["論文", "研究", "paper"]):
        return QueryType.ACADEMIC
    elif any(kw in query_lower for kw in ["ライブラリ", "パッケージ", "pip", "npm"]):
        return QueryType.LIBRARY
    elif any(kw in query_lower for kw in ["ツール", "tool", "mcp"]):
        return QueryType.MCP_TOOL
    
    return QueryType.WEB_SEARCH

def extract_keywords(query: str) -> list[str]:
    """キーワード抽出"""
    # 日本語と英語の両方に対応
    words = re.findall(r'[a-zA-Z]+|[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff]+', query)
    return [w.lower() for w in words if len(w) > 1]

def suggest_tools(keywords: list[str]) -> list[str]:
    """キーワードからツール推薦"""
    tools = set()
    for kw in keywords:
        for pattern, tool_list in KEYWORD_TO_TOOLS.items():
            if pattern in kw or kw in pattern:
                tools.update(tool_list)
    return list(tools)[:5]

def suggest_skills(keywords: list[str]) -> list[str]:
    """キーワードからスキル推薦"""
    skills = set()
    for kw in keywords:
        for pattern, skill_list in KEYWORD_TO_SKILLS.items():
            if pattern in kw or kw in pattern:
                skills.update(skill_list)
    return list(skills)[:3]

def get_search_strategy(query_type: QueryType, keywords: list[str]) -> str:
    """検索戦略を決定"""
    if query_type == QueryType.ACADEMIC:
        return SEARCH_STRATEGIES["academic"]["description"]
    elif query_type == QueryType.CODE or "コード" in keywords:
        return SEARCH_STRATEGIES["code"]["description"]
    elif query_type == QueryType.DATA or "企業" in keywords:
        return SEARCH_STRATEGIES["company"]["description"]
    elif "ニュース" in keywords or "最新" in keywords:
        return SEARCH_STRATEGIES["news"]["description"]
    elif query_type == QueryType.LIBRARY:
        return "ライブラリ検索: PyPI/npm API → GitHub Stars → Context7"
    elif query_type == QueryType.MCP_TOOL:
        return "MCPツール検索: mcp_tool_scanner.py → カテゴリフィルタ"
    else:
        return SEARCH_STRATEGIES["general"]["description"]

def analyze_query(query: str) -> QueryAnalysis:
    """クエリを分析"""
    query_type = classify_query(query)
    keywords = extract_keywords(query)
    
    return QueryAnalysis(
        original=query,
        type=query_type,
        keywords=keywords,
        suggested_tools=suggest_tools(keywords),
        suggested_skills=suggest_skills(keywords),
        search_strategy=get_search_strategy(query_type, keywords),
        confidence=0.8 if query_type != QueryType.WEB_SEARCH else 0.5
    )

# ============================================================
# Output Formatters
# ============================================================

def format_analysis(analysis: QueryAnalysis, format: str = "detailed") -> str:
    """分析結果をフォーマット"""
    if format == "json":
        return json.dumps({
            "original": analysis.original,
            "type": analysis.type.value,
            "keywords": analysis.keywords,
            "suggested_tools": analysis.suggested_tools,
            "suggested_skills": analysis.suggested_skills,
            "search_strategy": analysis.search_strategy,
            "confidence": analysis.confidence
        }, indent=2, ensure_ascii=False)
    
    output = [
        f"\n{'='*60}",
        f"Query Analysis: {analysis.original}",
        f"{'='*60}",
        f"\n📋 Type: {analysis.type.value.upper()}",
        f"🎯 Confidence: {analysis.confidence:.0%}",
        f"\n🔑 Keywords: {', '.join(analysis.keywords)}",
        f"\n🔧 Suggested Tools:",
    ]
    for tool in analysis.suggested_tools:
        output.append(f"   • {tool}")
    
    if analysis.suggested_skills:
        output.append(f"\n📚 Suggested Skills:")
        for skill in analysis.suggested_skills:
            output.append(f"   • {skill}")
    
    output.append(f"\n🔍 Search Strategy:")
    output.append(f"   {analysis.search_strategy}")
    
    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description="Search Router")
    parser.add_argument("--query", "-q", required=True, help="Query to analyze")
    parser.add_argument("--format", choices=["detailed", "json", "brief"], default="detailed")
    parser.add_argument("--mode", choices=["auto", "research", "code", "data"], default="auto")
    
    args = parser.parse_args()
    
    analysis = analyze_query(args.query)
    print(format_analysis(analysis, args.format))

if __name__ == "__main__":
    main()
