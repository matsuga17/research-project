#!/usr/bin/env python3
"""
optimize_prompt.py - プロンプト最適化変換スクリプト

通常のプロンプトをMCP効率化版に変換する
"""

import re
import json
import sys
from datetime import datetime
from typing import Dict, List, Tuple

# 最適化パターン定義
OPTIMIZATION_PATTERNS = {
    "search": {
        "triggers": ["検索して", "探して", "調べて", "search", "find"],
        "template": """
{original_task}
結果を {save_path} に保存。
私には{summary_type}だけ報告。
""".strip()
    },
    "collect": {
        "triggers": ["収集して", "集めて", "取得して", "collect", "gather"],
        "template": """
{original_task}
各結果を {save_path} に個別保存。
私には「完了。{count_type}」だけ報告。
""".strip()
    },
    "analyze": {
        "triggers": ["分析して", "解析して", "評価して", "analyze", "evaluate"],
        "template": """
{original_task}
分析結果を {save_path} に保存。
私には結論を{num_points}点で報告。
""".strip()
    },
    "compare": {
        "triggers": ["比較して", "対比して", "compare"],
        "template": """
{original_task}
比較データを {save_path} に保存。
私には主要な差異を{num_points}点で報告。
""".strip()
    },
    "list": {
        "triggers": ["リストを", "一覧を", "list"],
        "template": """
{original_task}
リストを {save_path} に保存。
私には総数と上位{top_n}件だけ報告。
""".strip()
    }
}

def detect_task_type(prompt: str) -> str:
    """プロンプトからタスクタイプを検出"""
    prompt_lower = prompt.lower()
    
    for task_type, config in OPTIMIZATION_PATTERNS.items():
        for trigger in config["triggers"]:
            if trigger in prompt_lower:
                return task_type
    
    return "general"

def generate_save_path(prompt: str, task_type: str) -> str:
    """保存パスを生成"""
    date_str = datetime.now().strftime("%Y%m%d")
    
    # トピックを抽出（簡易版）
    topic = "output"
    if "論文" in prompt or "paper" in prompt.lower():
        topic = "papers"
    elif "企業" in prompt or "company" in prompt.lower():
        topic = "companies"
    elif "データ" in prompt or "data" in prompt.lower():
        topic = "data"
    elif "市場" in prompt or "market" in prompt.lower():
        topic = "market"
    
    # ファイル形式を決定
    ext = "csv" if task_type in ["search", "list", "collect"] else "md"
    
    return f"/home/claude/{topic}/{task_type}_{date_str}.{ext}"

def optimize_prompt(original_prompt: str) -> Dict:
    """プロンプトを最適化"""
    task_type = detect_task_type(original_prompt)
    save_path = generate_save_path(original_prompt, task_type)
    
    if task_type == "general":
        # 一般的な最適化
        optimized = f"""
{original_prompt}

【最適化オプション】
- 結果をファイルに保存する場合: 「結果を{{path}}に保存して」を追加
- 要約だけ欲しい場合: 「要点を3つだけ報告して」を追加
- 段階的に実行する場合: フェーズ分割を指定
""".strip()
        
        return {
            "task_type": "general",
            "original": original_prompt,
            "optimized": optimized,
            "suggestions": [
                "タスクの種類が不明確です。より具体的なキーワードを使用してください。",
                "例: 「検索して」「収集して」「分析して」など"
            ]
        }
    
    # パターンに基づく最適化
    config = OPTIMIZATION_PATTERNS[task_type]
    
    # テンプレート変数
    template_vars = {
        "original_task": original_prompt,
        "save_path": save_path,
        "summary_type": "件数と上位3件の要約",
        "count_type": "収集件数と成功率",
        "num_points": "3",
        "top_n": "5"
    }
    
    optimized = config["template"].format(**template_vars)
    
    return {
        "task_type": task_type,
        "original": original_prompt,
        "optimized": optimized,
        "save_path": save_path,
        "context_reduction_estimate": "60-80%"
    }

def main():
    if len(sys.argv) > 1:
        # コマンドライン引数からプロンプトを取得
        prompt = " ".join(sys.argv[1:])
    else:
        # 標準入力から読み取り
        print("最適化するプロンプトを入力してください:")
        prompt = sys.stdin.read().strip()
    
    result = optimize_prompt(prompt)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
