#!/usr/bin/env python3
"""
context_estimator.py - コンテキスト消費推定スクリプト

タスクのコンテキスト消費量を推定し、最適化提案を生成
"""

import json
import sys
from typing import Dict, List

# トークン推定値（概算）
TOKEN_ESTIMATES = {
    "tool_definition": {
        "small": 100,      # 小規模ツール
        "medium": 300,     # 中規模ツール
        "large": 500       # 大規模ツール
    },
    "search_result": {
        "title_only": 20,
        "with_abstract": 150,
        "full_record": 300
    },
    "data_record": {
        "minimal": 50,
        "standard": 150,
        "detailed": 400
    },
    "analysis_output": {
        "summary": 100,
        "standard": 500,
        "detailed": 1500
    }
}

# 非効率パターンの検出ルール
INEFFICIENCY_PATTERNS = [
    {
        "name": "excessive_tool_calls",
        "description": "ツール呼び出し回数が多すぎる",
        "threshold": 3,
        "suggestion": "複数のツール呼び出しを1つのバッチ処理に統合"
    },
    {
        "name": "full_data_return",
        "description": "全データがコンテキストに返却されている",
        "threshold": 1000,  # tokens
        "suggestion": "結果をファイルに保存し、要約のみ返却"
    },
    {
        "name": "repeated_similar_calls",
        "description": "類似したツール呼び出しが繰り返されている",
        "threshold": 2,
        "suggestion": "ループ処理をバッチ処理に変換"
    },
    {
        "name": "unused_tool_definitions",
        "description": "使用されないツール定義がロードされている",
        "threshold": 5,
        "suggestion": "動的ツール選択を使用し、必要なツールのみロード"
    }
]

def estimate_tokens(text: str) -> int:
    """テキストのトークン数を概算"""
    # 日本語: 約1.5文字/トークン、英語: 約4文字/トークン
    jp_chars = sum(1 for c in text if ord(c) > 127)
    en_chars = len(text) - jp_chars
    return int(jp_chars / 1.5 + en_chars / 4)

def estimate_context_usage(task_config: Dict) -> Dict:
    """タスクのコンテキスト使用量を推定"""
    
    # デフォルト値
    config = {
        "num_tools": 5,
        "tool_size": "medium",
        "num_results": 10,
        "result_detail": "full_record",
        "num_data_records": 0,
        "data_detail": "standard",
        "analysis_detail": "standard"
    }
    config.update(task_config)
    
    # 各要素のトークン数を計算
    tool_tokens = config["num_tools"] * TOKEN_ESTIMATES["tool_definition"][config["tool_size"]]
    result_tokens = config["num_results"] * TOKEN_ESTIMATES["search_result"][config["result_detail"]]
    data_tokens = config["num_data_records"] * TOKEN_ESTIMATES["data_record"][config["data_detail"]]
    analysis_tokens = TOKEN_ESTIMATES["analysis_output"][config["analysis_detail"]]
    
    total_tokens = tool_tokens + result_tokens + data_tokens + analysis_tokens
    
    return {
        "breakdown": {
            "tool_definitions": tool_tokens,
            "search_results": result_tokens,
            "data_records": data_tokens,
            "analysis_output": analysis_tokens
        },
        "total_tokens": total_tokens,
        "percentage_of_context": round(total_tokens / 200000 * 100, 2)  # 200k context assumed
    }

def estimate_optimized_usage(original_estimate: Dict) -> Dict:
    """最適化後のコンテキスト使用量を推定"""
    
    breakdown = original_estimate["breakdown"]
    
    # 最適化による削減
    optimized = {
        "tool_definitions": int(breakdown["tool_definitions"] * 0.2),  # 80%削減
        "search_results": int(breakdown["search_results"] * 0.1),      # 90%削減（要約のみ）
        "data_records": int(breakdown["data_records"] * 0.1),          # 90%削減（ファイル保存）
        "analysis_output": int(breakdown["analysis_output"] * 0.3)     # 70%削減
    }
    
    total_optimized = sum(optimized.values())
    
    return {
        "breakdown": optimized,
        "total_tokens": total_optimized,
        "percentage_of_context": round(total_optimized / 200000 * 100, 2),
        "reduction_percentage": round((1 - total_optimized / original_estimate["total_tokens"]) * 100, 1)
    }

def detect_inefficiencies(task_config: Dict) -> List[Dict]:
    """非効率パターンを検出"""
    
    detected = []
    
    if task_config.get("num_tool_calls", 0) >= 3:
        detected.append({
            "pattern": "excessive_tool_calls",
            "current_value": task_config["num_tool_calls"],
            "suggestion": "複数のツール呼び出しを1つのバッチ処理に統合"
        })
    
    if task_config.get("result_detail") == "full_record":
        detected.append({
            "pattern": "full_data_return",
            "suggestion": "結果をファイルに保存し、要約のみ返却"
        })
    
    if task_config.get("num_tools", 0) > 5 and task_config.get("tools_actually_used", 0) < 3:
        detected.append({
            "pattern": "unused_tool_definitions",
            "suggestion": "動的ツール選択を使用し、必要なツールのみロード"
        })
    
    return detected

def generate_report(task_config: Dict) -> Dict:
    """コンテキスト効率レポートを生成"""
    
    original = estimate_context_usage(task_config)
    optimized = estimate_optimized_usage(original)
    inefficiencies = detect_inefficiencies(task_config)
    
    return {
        "current_state": {
            "estimated_tokens": original["total_tokens"],
            "context_usage_percentage": original["percentage_of_context"],
            "breakdown": original["breakdown"]
        },
        "after_optimization": {
            "estimated_tokens": optimized["total_tokens"],
            "context_usage_percentage": optimized["percentage_of_context"],
            "reduction": f"{optimized['reduction_percentage']}%",
            "breakdown": optimized["breakdown"]
        },
        "detected_inefficiencies": inefficiencies,
        "recommendations": [
            "結果をファイルに保存し、要約のみ返却",
            "フェーズ分割で中間結果の蓄積を防止",
            "動的ツール選択で不要なツール定義を削減"
        ]
    }

def main():
    # サンプル設定
    sample_config = {
        "num_tools": 10,
        "tool_size": "medium",
        "num_results": 20,
        "result_detail": "full_record",
        "num_data_records": 5,
        "data_detail": "detailed",
        "analysis_detail": "detailed",
        "num_tool_calls": 5,
        "tools_actually_used": 2
    }
    
    if len(sys.argv) > 1:
        try:
            sample_config = json.loads(sys.argv[1])
        except json.JSONDecodeError:
            print("Error: Invalid JSON configuration", file=sys.stderr)
            sys.exit(1)
    
    report = generate_report(sample_config)
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
