#!/usr/bin/env python3
"""
Library Search - マルチプラットフォームライブラリ検索

Usage:
    python library_search.py --query "pdf parsing" --platform python
    python library_search.py --query "state management" --platform npm
    python library_search.py --compare "pdfplumber,PyMuPDF,PyPDF2"
"""

import argparse
import json
import urllib.request
import urllib.parse
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

# ============================================================
# Platform Configurations
# ============================================================

PLATFORMS = {
    "python": {
        "name": "PyPI",
        "search_url": "https://pypi.org/pypi/{package}/json",
        "search_api": "https://pypi.org/search/?q={query}&o=",
    },
    "npm": {
        "name": "npm",
        "search_url": "https://registry.npmjs.org/{package}",
        "search_api": "https://registry.npmjs.org/-/v1/search?text={query}&size=10",
    },
    "rust": {
        "name": "crates.io",
        "search_url": "https://crates.io/api/v1/crates/{package}",
        "search_api": "https://crates.io/api/v1/crates?q={query}&per_page=10",
    },
    "github": {
        "name": "GitHub",
        "search_api": "https://api.github.com/search/repositories?q={query}&sort=stars&per_page=10",
    }
}

# ============================================================
# Common Library Recommendations (キャッシュデータ)
# ============================================================

LIBRARY_CACHE = {
    "python": {
        "pdf": [
            {"name": "PyMuPDF", "aka": "fitz", "stars": 4200, "desc": "高速PDF/XPS処理、画像抽出", "best_for": "速度重視、多機能"},
            {"name": "pdfplumber", "stars": 6100, "desc": "テーブル抽出に最強", "best_for": "表データ抽出"},
            {"name": "PyPDF2", "stars": 7800, "desc": "基本操作、軽量", "best_for": "シンプルな操作"},
            {"name": "borb", "stars": 3200, "desc": "PDF作成・編集", "best_for": "PDF生成"},
            {"name": "pdfminer.six", "stars": 5500, "desc": "テキスト抽出", "best_for": "テキスト解析"},
        ],
        "excel": [
            {"name": "openpyxl", "stars": 4800, "desc": "xlsx読み書き", "best_for": "標準的なExcel操作"},
            {"name": "pandas", "stars": 43000, "desc": "データ分析", "best_for": "データ処理"},
            {"name": "xlwings", "stars": 2900, "desc": "Excel自動化", "best_for": "VBA代替"},
            {"name": "xlsxwriter", "stars": 3500, "desc": "xlsx作成", "best_for": "レポート生成"},
        ],
        "web_scraping": [
            {"name": "beautifulsoup4", "stars": 0, "desc": "HTML/XMLパース", "best_for": "静的ページ"},
            {"name": "scrapy", "stars": 52000, "desc": "スクレイピングフレームワーク", "best_for": "大規模収集"},
            {"name": "playwright", "stars": 66000, "desc": "ブラウザ自動化", "best_for": "動的ページ"},
            {"name": "httpx", "stars": 13000, "desc": "HTTP クライアント", "best_for": "API呼び出し"},
        ],
        "data_analysis": [
            {"name": "pandas", "stars": 43000, "desc": "データ操作", "best_for": "表形式データ"},
            {"name": "numpy", "stars": 27000, "desc": "数値計算", "best_for": "配列操作"},
            {"name": "polars", "stars": 30000, "desc": "高速DataFrame", "best_for": "大規模データ"},
            {"name": "duckdb", "stars": 23000, "desc": "組み込みOLAP", "best_for": "SQL分析"},
        ],
        "visualization": [
            {"name": "matplotlib", "stars": 20000, "desc": "2Dプロット", "best_for": "学術グラフ"},
            {"name": "seaborn", "stars": 12500, "desc": "統計可視化", "best_for": "統計グラフ"},
            {"name": "plotly", "stars": 16000, "desc": "インタラクティブ", "best_for": "Web可視化"},
            {"name": "altair", "stars": 9200, "desc": "宣言型可視化", "best_for": "探索的分析"},
        ],
        "machine_learning": [
            {"name": "scikit-learn", "stars": 60000, "desc": "ML基盤", "best_for": "古典的ML"},
            {"name": "xgboost", "stars": 26000, "desc": "勾配ブースティング", "best_for": "構造化データ"},
            {"name": "lightgbm", "stars": 17000, "desc": "高速ブースティング", "best_for": "大規模データ"},
            {"name": "statsmodels", "stars": 10000, "desc": "統計モデル", "best_for": "計量経済学"},
        ],
    },
    "npm": {
        "state_management": [
            {"name": "zustand", "stars": 48000, "desc": "軽量状態管理", "best_for": "シンプルな状態"},
            {"name": "jotai", "stars": 18000, "desc": "アトムベース", "best_for": "細粒度状態"},
            {"name": "@reduxjs/toolkit", "stars": 60000, "desc": "Redux標準", "best_for": "大規模アプリ"},
            {"name": "valtio", "stars": 9000, "desc": "プロキシベース", "best_for": "ミュータブル操作"},
        ],
        "ui_components": [
            {"name": "shadcn-ui", "stars": 75000, "desc": "コピペUI", "best_for": "カスタマイズ性"},
            {"name": "@radix-ui/react", "stars": 16000, "desc": "ヘッドレスUI", "best_for": "アクセシビリティ"},
            {"name": "@chakra-ui/react", "stars": 38000, "desc": "フルUIキット", "best_for": "迅速開発"},
            {"name": "antd", "stars": 92000, "desc": "エンタープライズUI", "best_for": "管理画面"},
        ],
        "http_client": [
            {"name": "axios", "stars": 105000, "desc": "HTTPクライアント", "best_for": "ブラウザ/Node"},
            {"name": "ky", "stars": 13000, "desc": "軽量fetch", "best_for": "モダンAPI"},
            {"name": "@tanstack/react-query", "stars": 42000, "desc": "データフェッチ", "best_for": "React状態同期"},
            {"name": "swr", "stars": 30000, "desc": "データフェッチ", "best_for": "Next.js"},
        ],
    }
}

@dataclass
class LibraryInfo:
    name: str
    platform: str
    description: str
    stars: int
    downloads: Optional[str]
    last_update: Optional[str]
    best_for: str
    url: str

def search_cached(query: str, platform: str) -> list[LibraryInfo]:
    """キャッシュから検索"""
    results = []
    query_lower = query.lower().replace(" ", "_").replace("-", "_")
    
    if platform not in LIBRARY_CACHE:
        return results
    
    for category, libs in LIBRARY_CACHE[platform].items():
        if query_lower in category or any(query_lower in lib["name"].lower() for lib in libs):
            for lib in libs:
                results.append(LibraryInfo(
                    name=lib["name"],
                    platform=platform,
                    description=lib["desc"],
                    stars=lib["stars"],
                    downloads=None,
                    last_update=None,
                    best_for=lib["best_for"],
                    url=get_package_url(lib["name"], platform)
                ))
    
    return results

def get_package_url(name: str, platform: str) -> str:
    """パッケージURLを生成"""
    if platform == "python":
        return f"https://pypi.org/project/{name}/"
    elif platform == "npm":
        return f"https://www.npmjs.com/package/{name}"
    elif platform == "rust":
        return f"https://crates.io/crates/{name}"
    elif platform == "github":
        return f"https://github.com/search?q={name}"
    return ""

def search_npm_api(query: str) -> list[LibraryInfo]:
    """npm APIで検索"""
    try:
        url = PLATFORMS["npm"]["search_api"].format(query=urllib.parse.quote(query))
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            results = []
            for obj in data.get("objects", [])[:10]:
                pkg = obj.get("package", {})
                results.append(LibraryInfo(
                    name=pkg.get("name", ""),
                    platform="npm",
                    description=pkg.get("description", "")[:100],
                    stars=0,
                    downloads=None,
                    last_update=pkg.get("date", "")[:10] if pkg.get("date") else None,
                    best_for="",
                    url=pkg.get("links", {}).get("npm", "")
                ))
            return results
    except Exception as e:
        print(f"npm API error: {e}")
        return []

def compare_libraries(names: list[str], platform: str) -> str:
    """ライブラリ比較表を生成"""
    output = [f"\n## {platform.upper()} Library Comparison\n"]
    output.append("| Library | Stars | Best For | Description |")
    output.append("|---------|-------|----------|-------------|")
    
    for name in names:
        found = False
        for category, libs in LIBRARY_CACHE.get(platform, {}).items():
            for lib in libs:
                if lib["name"].lower() == name.lower():
                    output.append(f"| **{lib['name']}** | {lib['stars']:,} | {lib['best_for']} | {lib['desc']} |")
                    found = True
                    break
            if found:
                break
        if not found:
            output.append(f"| {name} | - | - | (not in cache) |")
    
    return "\n".join(output)

def format_results(results: list[LibraryInfo], format: str = "table") -> str:
    """結果をフォーマット"""
    if format == "json":
        return json.dumps([{
            "name": r.name,
            "platform": r.platform,
            "description": r.description,
            "stars": r.stars,
            "best_for": r.best_for,
            "url": r.url
        } for r in results], indent=2, ensure_ascii=False)
    
    elif format == "markdown":
        output = ["| Library | Stars | Best For | Description |"]
        output.append("|---------|-------|----------|-------------|")
        for r in results:
            stars = f"{r.stars:,}" if r.stars else "-"
            output.append(f"| [{r.name}]({r.url}) | {stars} | {r.best_for} | {r.description} |")
        return "\n".join(output)
    
    else:  # table
        output = []
        for r in results:
            stars = f"⭐ {r.stars:,}" if r.stars else ""
            output.append(f"\n{r.name} {stars}")
            output.append(f"  {r.description}")
            output.append(f"  Best for: {r.best_for}")
            output.append(f"  {r.url}")
        return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description="Library Search")
    parser.add_argument("--query", "-q", help="Search query")
    parser.add_argument("--platform", "-p", choices=["python", "npm", "rust", "github", "all"], default="python")
    parser.add_argument("--compare", help="Compare libraries (comma-separated)")
    parser.add_argument("--format", choices=["json", "markdown", "table"], default="table")
    parser.add_argument("--list-categories", action="store_true", help="List available categories")
    
    args = parser.parse_args()
    
    if args.list_categories:
        print("\n=== Available Categories ===\n")
        for platform, categories in LIBRARY_CACHE.items():
            print(f"{platform.upper()}:")
            for cat in categories.keys():
                print(f"  - {cat}")
        return
    
    if args.compare:
        names = [n.strip() for n in args.compare.split(",")]
        print(compare_libraries(names, args.platform))
        return
    
    if not args.query:
        print("Error: --query is required")
        return
    
    results = search_cached(args.query, args.platform)
    
    if not results:
        print(f"No cached results for '{args.query}' in {args.platform}")
        print("Tip: Try --platform npm or broader query terms")
        return
    
    print(f"\n=== {args.platform.upper()} Libraries for '{args.query}' ===")
    print(format_results(results, args.format))

if __name__ == "__main__":
    main()
