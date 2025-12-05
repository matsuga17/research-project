#!/usr/bin/env python3
"""
workflow_generator.py - ワークフローテンプレート生成スクリプト

タスク種別に応じた最適化ワークフローを生成
"""

import json
import sys
from datetime import datetime
from typing import Dict, List

# ワークフローテンプレート
WORKFLOW_TEMPLATES = {
    "literature_review": {
        "name": "文献レビュー",
        "phases": [
            {
                "name": "Phase 1: 文献検索",
                "tasks": ["複数DBで検索", "結果をCSV保存"],
                "save_path": "/home/claude/literature/{topic}_search.csv",
                "report": "「{N}件発見。DB別内訳を報告」"
            },
            {
                "name": "Phase 2: スクリーニング",
                "tasks": ["基準による絞り込み", "除外理由の記録"],
                "save_path": "/home/claude/literature/{topic}_screened.csv",
                "report": "「{M}件に絞り込み」"
            },
            {
                "name": "Phase 3: 詳細分析",
                "tasks": ["アブストラクト取得", "テーマ抽出"],
                "save_path": "/home/claude/literature/{topic}_analysis.md",
                "report": "「主要テーマ3つを報告」"
            },
            {
                "name": "Phase 4: 統合・執筆",
                "tasks": ["文献レビュー執筆"],
                "save_path": None,
                "report": "アーティファクト出力"
            }
        ]
    },
    "company_research": {
        "name": "企業調査",
        "phases": [
            {
                "name": "Phase 1: 基本情報収集",
                "tasks": ["企業プロファイル取得"],
                "save_path": "/home/claude/companies/{company}/profile.json",
                "report": "「{N}社の基本情報収集完了」"
            },
            {
                "name": "Phase 2: 財務データ収集",
                "tasks": ["IR資料取得", "財務指標抽出"],
                "save_path": "/home/claude/companies/{company}/financials.json",
                "report": "「財務データ収集完了」"
            },
            {
                "name": "Phase 3: 戦略分析",
                "tasks": ["ニュース分析", "戦略抽出"],
                "save_path": "/home/claude/companies/{company}/strategy.md",
                "report": "「戦略分析完了」"
            },
            {
                "name": "Phase 4: クロス分析",
                "tasks": ["比較分析", "レポート作成"],
                "save_path": "/home/claude/companies/comparison.md",
                "report": "アーティファクト出力"
            }
        ]
    },
    "data_collection": {
        "name": "データ収集",
        "phases": [
            {
                "name": "Phase 1: ソース特定",
                "tasks": ["利用可能ソースの調査"],
                "save_path": "/home/claude/data/{project}/sources.md",
                "report": "「{N}ソースを特定」"
            },
            {
                "name": "Phase 2: データ取得",
                "tasks": ["各ソースからデータ取得"],
                "save_path": "/home/claude/data/{project}/raw/",
                "report": "「成功{a}件、失敗{b}件」"
            },
            {
                "name": "Phase 3: クレンジング",
                "tasks": ["欠損値処理", "外れ値検出"],
                "save_path": "/home/claude/data/{project}/cleaned/",
                "report": "「クレンジング完了」"
            },
            {
                "name": "Phase 4: 統合・検証",
                "tasks": ["データ統合", "整合性検証"],
                "save_path": "/home/claude/data/{project}/final.csv",
                "report": "「最終レコード数{N}」"
            }
        ]
    },
    "market_research": {
        "name": "市場調査",
        "phases": [
            {
                "name": "Phase 1: 情報収集",
                "tasks": ["業界レポート取得", "ニュース収集", "学術論文検索"],
                "save_path": "/home/claude/market/{topic}/",
                "report": "「3ソースから情報収集完了」"
            },
            {
                "name": "Phase 2: 統合分析",
                "tasks": ["情報統合", "トレンド分析"],
                "save_path": "/home/claude/market/{topic}/analysis.md",
                "report": "「主要インサイト3点」"
            },
            {
                "name": "Phase 3: レポート作成",
                "tasks": ["レポート執筆"],
                "save_path": None,
                "report": "アーティファクト出力"
            }
        ]
    },
    "statistical_analysis": {
        "name": "統計分析",
        "phases": [
            {
                "name": "Phase 1: 記述統計",
                "tasks": ["基本統計量算出", "分布確認"],
                "save_path": "/home/claude/analysis/descriptive.md",
                "report": "「記述統計完了」"
            },
            {
                "name": "Phase 2: 仮説検定",
                "tasks": ["検定実施"],
                "save_path": "/home/claude/analysis/tests.md",
                "report": "「有意な結果{N}件」"
            },
            {
                "name": "Phase 3: 回帰分析",
                "tasks": ["回帰モデル構築", "診断"],
                "save_path": "/home/claude/analysis/regression.md",
                "report": "「R²={value}」"
            },
            {
                "name": "Phase 4: 結果解釈",
                "tasks": ["解釈", "レポート作成"],
                "save_path": None,
                "report": "アーティファクト出力"
            }
        ]
    }
}

def detect_workflow_type(task_description: str) -> str:
    """タスク記述からワークフロータイプを検出"""
    
    keywords = {
        "literature_review": ["文献", "論文", "レビュー", "literature", "paper"],
        "company_research": ["企業", "会社", "company", "corporate"],
        "data_collection": ["データ収集", "データ取得", "data collection"],
        "market_research": ["市場", "業界", "market", "industry"],
        "statistical_analysis": ["統計", "分析", "回帰", "statistical", "regression"]
    }
    
    task_lower = task_description.lower()
    
    for wf_type, kws in keywords.items():
        for kw in kws:
            if kw in task_lower:
                return wf_type
    
    return "general"

def generate_workflow(task_description: str, params: Dict = None) -> Dict:
    """ワークフローを生成"""
    
    wf_type = detect_workflow_type(task_description)
    
    if wf_type == "general":
        return {
            "type": "general",
            "task": task_description,
            "suggestion": "タスクの種類が特定できません。以下から選択してください:",
            "available_workflows": list(WORKFLOW_TEMPLATES.keys())
        }
    
    template = WORKFLOW_TEMPLATES[wf_type]
    params = params or {}
    
    # パラメータのデフォルト値
    defaults = {
        "topic": "research",
        "company": "company",
        "project": "project",
        "N": "X",
        "M": "Y",
        "a": "A",
        "b": "B",
        "value": "0.XX"
    }
    defaults.update(params)
    
    # テンプレートにパラメータを適用
    phases = []
    for phase in template["phases"]:
        phase_copy = phase.copy()
        if phase_copy["save_path"]:
            phase_copy["save_path"] = phase_copy["save_path"].format(**defaults)
        phase_copy["report"] = phase_copy["report"].format(**defaults)
        phases.append(phase_copy)
    
    return {
        "type": wf_type,
        "name": template["name"],
        "task": task_description,
        "phases": phases,
        "execution_instruction": "各フェーズは「続けて」で進行。途中停止は「一時停止」。",
        "estimated_context_reduction": "70-85%"
    }

def format_workflow_prompt(workflow: Dict) -> str:
    """ワークフローをプロンプト形式にフォーマット"""
    
    if workflow["type"] == "general":
        return json.dumps(workflow, ensure_ascii=False, indent=2)
    
    lines = [
        f"# {workflow['name']}ワークフロー",
        "",
        f"タスク: {workflow['task']}",
        "",
        "---",
        ""
    ]
    
    for i, phase in enumerate(workflow["phases"]):
        trigger = "" if i == 0 else "※「続けて」で開始"
        lines.append(f"【{phase['name']}】{trigger}")
        lines.append(f"処理: {', '.join(phase['tasks'])}")
        if phase["save_path"]:
            lines.append(f"保存: {phase['save_path']}")
        lines.append(f"報告: {phase['report']}")
        lines.append("")
    
    lines.append("---")
    lines.append(f"実行指示: {workflow['execution_instruction']}")
    lines.append(f"推定コンテキスト削減: {workflow['estimated_context_reduction']}")
    
    return "\n".join(lines)

def main():
    if len(sys.argv) > 1:
        task_description = " ".join(sys.argv[1:])
    else:
        print("タスクの説明を入力してください:")
        task_description = input().strip()
    
    workflow = generate_workflow(task_description)
    formatted = format_workflow_prompt(workflow)
    print(formatted)
    
    # JSON形式でも出力
    print("\n--- JSON形式 ---")
    print(json.dumps(workflow, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
