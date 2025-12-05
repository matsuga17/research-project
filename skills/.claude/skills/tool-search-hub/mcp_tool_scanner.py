#!/usr/bin/env python3
"""
MCP Tool Scanner - 利用可能なMCPツールを動的に検索・フィルタリング

Usage:
    python mcp_tool_scanner.py --query "file"
    python mcp_tool_scanner.py --category "filesystem"
    python mcp_tool_scanner.py --list-all
    python mcp_tool_scanner.py --export json
"""

import argparse
import json
import re
from dataclasses import dataclass, asdict
from typing import Optional
from difflib import SequenceMatcher

# ============================================================
# MCP Tool Registry (現在接続中のツール定義)
# ============================================================

MCP_TOOLS = [
    # Filesystem (User's Computer)
    {"name": "Filesystem:read_file", "category": "filesystem", "description": "Read file contents from user's computer", "server": "Filesystem"},
    {"name": "Filesystem:read_text_file", "category": "filesystem", "description": "Read text file with encoding support", "server": "Filesystem"},
    {"name": "Filesystem:read_media_file", "category": "filesystem", "description": "Read image or audio file as base64", "server": "Filesystem"},
    {"name": "Filesystem:write_file", "category": "filesystem", "description": "Create or overwrite file", "server": "Filesystem"},
    {"name": "Filesystem:edit_file", "category": "filesystem", "description": "Make line-based edits to text file", "server": "Filesystem"},
    {"name": "Filesystem:list_directory", "category": "filesystem", "description": "List files and directories", "server": "Filesystem"},
    {"name": "Filesystem:search_files", "category": "filesystem", "description": "Recursively search for files", "server": "Filesystem"},
    {"name": "Filesystem:create_directory", "category": "filesystem", "description": "Create new directory", "server": "Filesystem"},
    {"name": "Filesystem:move_file", "category": "filesystem", "description": "Move or rename files", "server": "Filesystem"},
    {"name": "Filesystem:get_file_info", "category": "filesystem", "description": "Get file metadata", "server": "Filesystem"},
    {"name": "Filesystem:copy_file_user_to_claude", "category": "filesystem", "description": "Copy file from user to Claude's computer", "server": "Filesystem"},
    
    # Desktop Commander
    {"name": "desktop-commander:read_file", "category": "filesystem", "description": "Read file with offset/length support", "server": "desktop-commander"},
    {"name": "desktop-commander:write_file", "category": "filesystem", "description": "Write file with append mode", "server": "desktop-commander"},
    {"name": "desktop-commander:list_directory", "category": "filesystem", "description": "List directory with depth control", "server": "desktop-commander"},
    {"name": "desktop-commander:start_process", "category": "execution", "description": "Start terminal process (Python, Node, bash)", "server": "desktop-commander"},
    {"name": "desktop-commander:interact_with_process", "category": "execution", "description": "Send input to running process", "server": "desktop-commander"},
    {"name": "desktop-commander:read_process_output", "category": "execution", "description": "Read output from process", "server": "desktop-commander"},
    {"name": "desktop-commander:start_search", "category": "search", "description": "Start streaming file/content search", "server": "desktop-commander"},
    {"name": "desktop-commander:edit_block", "category": "filesystem", "description": "Surgical text replacement in files", "server": "desktop-commander"},
    
    # Search APIs
    {"name": "omnisearch:tavily_search", "category": "search", "description": "Web search with citations (academic/technical)", "server": "omnisearch"},
    {"name": "omnisearch:brave_search", "category": "search", "description": "Privacy-focused search with operators", "server": "omnisearch"},
    {"name": "omnisearch:jina_reader_process", "category": "extraction", "description": "Convert URL to clean text", "server": "omnisearch"},
    {"name": "omnisearch:tavily_extract_process", "category": "extraction", "description": "Extract web page content", "server": "omnisearch"},
    {"name": "omnisearch:firecrawl_scrape_process", "category": "extraction", "description": "Scrape with markdown/structured output", "server": "omnisearch"},
    {"name": "omnisearch:firecrawl_crawl_process", "category": "extraction", "description": "Deep crawl website subpages", "server": "omnisearch"},
    {"name": "omnisearch:firecrawl_map_process", "category": "extraction", "description": "Fast URL collection from websites", "server": "omnisearch"},
    {"name": "web_search", "category": "search", "description": "General web search", "server": "anthropic"},
    {"name": "web_fetch", "category": "extraction", "description": "Fetch web page contents", "server": "anthropic"},
    
    # Playwright Browser
    {"name": "playwright:browser_navigate", "category": "browser", "description": "Navigate to URL", "server": "playwright"},
    {"name": "playwright:browser_click", "category": "browser", "description": "Click element on page", "server": "playwright"},
    {"name": "playwright:browser_type", "category": "browser", "description": "Type text into element", "server": "playwright"},
    {"name": "playwright:browser_snapshot", "category": "browser", "description": "Capture accessibility snapshot", "server": "playwright"},
    {"name": "playwright:browser_take_screenshot", "category": "browser", "description": "Take screenshot of page", "server": "playwright"},
    {"name": "playwright:browser_evaluate", "category": "browser", "description": "Execute JavaScript on page", "server": "playwright"},
    
    # Academic Search
    {"name": "google-scholar:search_google_scholar_key_words", "category": "research", "description": "Search Google Scholar by keywords", "server": "google-scholar"},
    {"name": "google-scholar:search_google_scholar_advanced", "category": "research", "description": "Advanced Google Scholar search", "server": "google-scholar"},
    {"name": "google-scholar:get_author_info", "category": "research", "description": "Get author information", "server": "google-scholar"},
    {"name": "semantic-scholar:search_semantic_scholar", "category": "research", "description": "Semantic paper search", "server": "semantic-scholar"},
    {"name": "semantic-scholar:get_semantic_scholar_paper_details", "category": "research", "description": "Get paper details", "server": "semantic-scholar"},
    {"name": "semantic-scholar:get_semantic_scholar_citations_and_references", "category": "research", "description": "Get citations and references", "server": "semantic-scholar"},
    {"name": "semantic-scholar:get_semantic_scholar_paper_recommendations", "category": "research", "description": "Get paper recommendations", "server": "semantic-scholar"},
    
    # Think Tank / Memory
    {"name": "think-tank:think", "category": "analysis", "description": "Structured reasoning and thinking", "server": "think-tank"},
    {"name": "think-tank:upsert_entities", "category": "database", "description": "Create/update knowledge graph entities", "server": "think-tank"},
    {"name": "think-tank:create_relations", "category": "database", "description": "Create entity relations", "server": "think-tank"},
    {"name": "think-tank:search_nodes", "category": "database", "description": "Search knowledge graph", "server": "think-tank"},
    {"name": "think-tank:exa_search", "category": "search", "description": "Exa semantic web search", "server": "think-tank"},
    {"name": "think-tank:exa_answer", "category": "search", "description": "Get sourced answers via Exa", "server": "think-tank"},
    {"name": "think-tank:plan_tasks", "category": "task", "description": "Create multiple tasks from plan", "server": "think-tank"},
    {"name": "think-tank:list_tasks", "category": "task", "description": "List tasks with filters", "server": "think-tank"},
    {"name": "memory:create_entities", "category": "database", "description": "Create knowledge graph entities", "server": "memory"},
    {"name": "memory:search_nodes", "category": "database", "description": "Search memory nodes", "server": "memory"},
    
    # Sequential Thinking
    {"name": "sequential-thinking:sequentialthinking", "category": "analysis", "description": "Dynamic problem-solving through thoughts", "server": "sequential-thinking"},
    
    # Coupler.io
    {"name": "Coupler.io:get-data", "category": "database", "description": "Get data from data flow", "server": "Coupler.io"},
    {"name": "Coupler.io:get-dataflow", "category": "database", "description": "Get data flow by ID", "server": "Coupler.io"},
    {"name": "Coupler.io:get-schema", "category": "database", "description": "Get data table schema", "server": "Coupler.io"},
    {"name": "Coupler.io:list-dataflows", "category": "database", "description": "List all data flows", "server": "Coupler.io"},
    
    # YouTube
    {"name": "youtube-transcript:youtube_get_transcript", "category": "extraction", "description": "Extract YouTube transcript", "server": "youtube-transcript"},
    {"name": "youtube-transcript:youtube_search_transcript", "category": "extraction", "description": "Search within transcript", "server": "youtube-transcript"},
    {"name": "youtube-transcript:youtube_get_channel_videos", "category": "extraction", "description": "Get channel video list", "server": "youtube-transcript"},
    
    # Task Master
    {"name": "taskmaster-ai:get_tasks", "category": "task", "description": "Get all tasks", "server": "taskmaster-ai"},
    {"name": "taskmaster-ai:add_task", "category": "task", "description": "Add new task with AI", "server": "taskmaster-ai"},
    {"name": "taskmaster-ai:expand_task", "category": "task", "description": "Expand task into subtasks", "server": "taskmaster-ai"},
    {"name": "taskmaster-ai:next_task", "category": "task", "description": "Find next task to work on", "server": "taskmaster-ai"},
    {"name": "taskmaster-ai:parse_prd", "category": "task", "description": "Parse PRD to generate tasks", "server": "taskmaster-ai"},
    
    # Context7
    {"name": "Context7:resolve-library-id", "category": "research", "description": "Resolve package to library ID", "server": "Context7"},
    {"name": "Context7:get-library-docs", "category": "research", "description": "Fetch library documentation", "server": "Context7"},
    
    # Claude Core
    {"name": "view", "category": "filesystem", "description": "View files, images, directories on Claude's computer", "server": "claude"},
    {"name": "create_file", "category": "filesystem", "description": "Create new file on Claude's computer", "server": "claude"},
    {"name": "str_replace", "category": "filesystem", "description": "Replace string in file", "server": "claude"},
    {"name": "bash_tool", "category": "execution", "description": "Run bash command in container", "server": "claude"},
]

@dataclass
class ToolMatch:
    name: str
    category: str
    description: str
    server: str
    relevance: float

def calculate_relevance(query: str, tool: dict) -> float:
    """クエリとツールの関連度を計算"""
    query_lower = query.lower()
    name_lower = tool["name"].lower()
    desc_lower = tool["description"].lower()
    
    # 完全一致
    if query_lower in name_lower:
        return 1.0
    
    # 説明に含まれる
    if query_lower in desc_lower:
        return 0.8
    
    # 部分一致（SequenceMatcher）
    name_ratio = SequenceMatcher(None, query_lower, name_lower).ratio()
    desc_ratio = SequenceMatcher(None, query_lower, desc_lower).ratio()
    
    return max(name_ratio * 0.7, desc_ratio * 0.5)

def search_tools(query: Optional[str] = None, category: Optional[str] = None, 
                 min_relevance: float = 0.3) -> list[ToolMatch]:
    """ツール検索"""
    results = []
    
    for tool in MCP_TOOLS:
        # カテゴリフィルタ
        if category and tool["category"] != category:
            continue
        
        # クエリマッチング
        if query:
            relevance = calculate_relevance(query, tool)
            if relevance < min_relevance:
                continue
        else:
            relevance = 1.0
        
        results.append(ToolMatch(
            name=tool["name"],
            category=tool["category"],
            description=tool["description"],
            server=tool["server"],
            relevance=relevance
        ))
    
    # 関連度でソート
    results.sort(key=lambda x: x.relevance, reverse=True)
    return results

def list_categories() -> dict[str, int]:
    """カテゴリ一覧と件数"""
    categories = {}
    for tool in MCP_TOOLS:
        cat = tool["category"]
        categories[cat] = categories.get(cat, 0) + 1
    return dict(sorted(categories.items()))

def main():
    parser = argparse.ArgumentParser(description="MCP Tool Scanner")
    parser.add_argument("--query", "-q", help="Search query")
    parser.add_argument("--category", "-c", help="Filter by category")
    parser.add_argument("--list-all", action="store_true", help="List all tools")
    parser.add_argument("--list-categories", action="store_true", help="List categories")
    parser.add_argument("--export", choices=["json", "markdown", "table"], default="table")
    parser.add_argument("--min-relevance", type=float, default=0.3)
    
    args = parser.parse_args()
    
    if args.list_categories:
        categories = list_categories()
        print("\n=== MCP Tool Categories ===")
        for cat, count in categories.items():
            print(f"  {cat}: {count} tools")
        return
    
    if args.list_all:
        results = search_tools()
    else:
        results = search_tools(
            query=args.query, 
            category=args.category,
            min_relevance=args.min_relevance
        )
    
    if args.export == "json":
        output = {
            "query": args.query,
            "category": args.category,
            "matches": [asdict(r) for r in results],
            "total": len(results)
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    
    elif args.export == "markdown":
        print(f"\n## MCP Tools Search Results")
        print(f"Query: `{args.query or 'all'}` | Category: `{args.category or 'all'}`\n")
        print("| Tool | Category | Description | Relevance |")
        print("|------|----------|-------------|-----------|")
        for r in results[:20]:
            print(f"| `{r.name}` | {r.category} | {r.description} | {r.relevance:.2f} |")
    
    else:  # table
        print(f"\n=== MCP Tools ({len(results)} matches) ===")
        print(f"Query: {args.query or 'all'} | Category: {args.category or 'all'}\n")
        for r in results[:20]:
            print(f"[{r.relevance:.2f}] {r.name}")
            print(f"       {r.category} | {r.description}\n")

if __name__ == "__main__":
    main()
