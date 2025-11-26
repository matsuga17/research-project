"""
研究プロジェクト進捗管理システム
================================
Research Project Checklist Manager

7フェーズの研究ワークフローを段階的に管理し、
各タスクの完了状況を追跡する

Author: Corporate Research Data Hub
Version: 2.0
Date: 2025-10-31
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
import os


class ResearchChecklistManager:
    """
    研究プロジェクトの進捗管理とチェックリスト
    
    使用例:
    -------
    >>> manager = ResearchChecklistManager('asian_roa_study')
    >>> manager.display_progress()
    >>> manager.mark_complete('1.1')
    >>> manager.get_next_tasks()
    """
    
    def __init__(self, project_name: str):
        """
        Parameters:
        -----------
        project_name : str
            プロジェクト名
        """
        self.project_name = project_name
        self.checklist_file = f'{project_name}_checklist.json'
        self.checklist = self._initialize_checklist()
        self.load_progress()
    
    def _initialize_checklist(self) -> dict:
        """チェックリストの初期化"""
        return {
            'phase1_design': {
                'name': 'Phase 1: Research Design',
                'items': [
                    {'id': '1.1', 'task': 'Research question defined', 'completed': False, 'required': True},
                    {'id': '1.2', 'task': 'Hypotheses formulated', 'completed': False, 'required': True},
                    {'id': '1.3', 'task': 'Sample scope determined', 'completed': False, 'required': True},
                    {'id': '1.4', 'task': 'Power analysis conducted', 'completed': False, 'required': True},
                    {'id': '1.5', 'task': 'Pre-analysis plan registered', 'completed': False, 'required': False}
                ]
            },
            'phase2_sources': {
                'name': 'Phase 2: Data Source Selection',
                'items': [
                    {'id': '2.1', 'task': 'Data sources identified', 'completed': False, 'required': True},
                    {'id': '2.2', 'task': 'Access credentials obtained', 'completed': False, 'required': True},
                    {'id': '2.3', 'task': 'API limits documented', 'completed': False, 'required': True},
                    {'id': '2.4', 'task': 'Data source evaluation completed', 'completed': False, 'required': True}
                ]
            },
            'phase3_collection': {
                'name': 'Phase 3: Data Collection',
                'items': [
                    {'id': '3.1', 'task': 'Collection scripts written', 'completed': False, 'required': True},
                    {'id': '3.2', 'task': 'Data downloaded and backed up', 'completed': False, 'required': True},
                    {'id': '3.3', 'task': 'Data lineage documented', 'completed': False, 'required': True},
                    {'id': '3.4', 'task': 'Raw data checksums computed', 'completed': False, 'required': True}
                ]
            },
            'phase4_cleaning': {
                'name': 'Phase 4: Data Cleaning',
                'items': [
                    {'id': '4.1', 'task': 'Financial variables standardized', 'completed': False, 'required': True},
                    {'id': '4.2', 'task': 'Missing data handled', 'completed': False, 'required': True},
                    {'id': '4.3', 'task': 'Outliers detected and treated', 'completed': False, 'required': True},
                    {'id': '4.4', 'task': 'Industry classifications standardized', 'completed': False, 'required': True}
                ]
            },
            'phase5_integration': {
                'name': 'Phase 5: Multi-Source Integration',
                'items': [
                    {'id': '5.1', 'task': 'Crosswalk table created', 'completed': False, 'required': True},
                    {'id': '5.2', 'task': 'Merges validated', 'completed': False, 'required': True},
                    {'id': '5.3', 'task': 'Duplicate records removed', 'completed': False, 'required': True}
                ]
            },
            'phase6_qa': {
                'name': 'Phase 6: Quality Assurance',
                'items': [
                    {'id': '6.1', 'task': 'Automated QA checks run', 'completed': False, 'required': True},
                    {'id': '6.2', 'task': 'Accounting identities verified', 'completed': False, 'required': True},
                    {'id': '6.3', 'task': 'Temporal consistency checked', 'completed': False, 'required': True},
                    {'id': '6.4', 'task': 'QA report reviewed', 'completed': False, 'required': True},
                    {'id': '6.5', 'task': 'Advanced QA (outliers, Benford) completed', 'completed': False, 'required': True}
                ]
            },
            'phase7_documentation': {
                'name': 'Phase 7: Documentation',
                'items': [
                    {'id': '7.1', 'task': 'Codebook generated', 'completed': False, 'required': True},
                    {'id': '7.2', 'task': 'README written', 'completed': False, 'required': True},
                    {'id': '7.3', 'task': 'Replication scripts organized', 'completed': False, 'required': True},
                    {'id': '7.4', 'task': 'Data backed up (3-2-1 rule)', 'completed': False, 'required': True}
                ]
            }
        }
    
    def display_progress(self):
        """進捗状況を表示"""
        total_items = sum(len(phase['items']) for phase in self.checklist.values())
        completed_items = sum(
            sum(1 for item in phase['items'] if item['completed'])
            for phase in self.checklist.values()
        )
        
        progress_pct = completed_items / total_items * 100
        
        print("=" * 70)
        print(f"Project: {self.project_name}")
        print(f"Overall Progress: {completed_items}/{total_items} ({progress_pct:.1f}%)")
        print("=" * 70)
        
        for phase_key, phase in self.checklist.items():
            phase_completed = sum(1 for item in phase['items'] if item['completed'])
            phase_total = len(phase['items'])
            status = "✓" if phase_completed == phase_total else "○"
            
            print(f"\n{status} {phase['name']} ({phase_completed}/{phase_total})")
            
            for item in phase['items']:
                check = "✓" if item['completed'] else "☐"
                required = "*" if item['required'] else " "
                print(f"  {check} {item['id']} {item['task']} {required}")
        
        print("\n* = Required for minimal viable dataset")
        print("\nLegend: ✓ = Completed, ☐ = Pending, ○ = In Progress")
    
    def mark_complete(self, item_id: str):
        """タスクを完了としてマーク"""
        for phase in self.checklist.values():
            for item in phase['items']:
                if item['id'] == item_id:
                    item['completed'] = True
                    item['completed_at'] = datetime.now().isoformat()
                    print(f"✓ Marked as complete: {item['task']}")
                    self.save_progress()
                    return
        
        print(f"Error: Item {item_id} not found")
    
    def mark_incomplete(self, item_id: str):
        """タスクを未完了に戻す"""
        for phase in self.checklist.values():
            for item in phase['items']:
                if item['id'] == item_id:
                    item['completed'] = False
                    if 'completed_at' in item:
                        del item['completed_at']
                    print(f"☐ Marked as incomplete: {item['task']}")
                    self.save_progress()
                    return
        
        print(f"Error: Item {item_id} not found")
    
    def get_next_tasks(self, limit: int = 5) -> List[str]:
        """次に実行すべきタスクを提案"""
        next_tasks = []
        
        for phase_key, phase in self.checklist.items():
            for item in phase['items']:
                if not item['completed']:
                    priority = "**REQUIRED**" if item['required'] else "Optional"
                    next_tasks.append(f"{item['id']} - {item['task']} ({priority})")
                    if len(next_tasks) >= limit:
                        return next_tasks
        
        return next_tasks if next_tasks else ["All tasks completed! 🎉"]
    
    def get_phase_summary(self) -> dict:
        """各フェーズの進捗サマリー"""
        summary = {}
        
        for phase_key, phase in self.checklist.items():
            completed = sum(1 for item in phase['items'] if item['completed'])
            total = len(phase['items'])
            percentage = (completed / total * 100) if total > 0 else 0
            
            summary[phase_key] = {
                'name': phase['name'],
                'completed': completed,
                'total': total,
                'percentage': percentage,
                'status': 'Complete' if completed == total else 'In Progress'
            }
        
        return summary
    
    def export_report(self, output_path: str = None):
        """進捗レポートをMarkdown形式で出力"""
        if output_path is None:
            output_path = f'{self.project_name}_progress_report.md'
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# Research Progress Report: {self.project_name}\n\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Overall progress
            total_items = sum(len(phase['items']) for phase in self.checklist.values())
            completed_items = sum(
                sum(1 for item in phase['items'] if item['completed'])
                for phase in self.checklist.values()
            )
            progress_pct = completed_items / total_items * 100
            
            f.write(f"## Overall Progress: {completed_items}/{total_items} ({progress_pct:.1f}%)\n\n")
            
            # Progress bar
            bar_length = 50
            filled = int(bar_length * completed_items / total_items)
            bar = '█' * filled + '░' * (bar_length - filled)
            f.write(f"[{bar}] {progress_pct:.1f}%\n\n")
            
            # Phase-by-phase breakdown
            f.write("## Phase Details\n\n")
            
            for phase_key, phase in self.checklist.items():
                phase_completed = sum(1 for item in phase['items'] if item['completed'])
                phase_total = len(phase['items'])
                status = "✅ Complete" if phase_completed == phase_total else "🔄 In Progress"
                
                f.write(f"### {phase['name']} ({phase_completed}/{phase_total}) {status}\n\n")
                
                for item in phase['items']:
                    check = "✅" if item['completed'] else "⬜"
                    required = "**[REQUIRED]**" if item['required'] else "[Optional]"
                    completed_date = f" (completed: {item.get('completed_at', '')})" if item['completed'] else ""
                    f.write(f"- {check} {item['id']} {item['task']} {required}{completed_date}\n")
                
                f.write("\n")
            
            # Next steps
            f.write("## Next Steps\n\n")
            next_tasks = self.get_next_tasks(limit=10)
            for task in next_tasks:
                f.write(f"- {task}\n")
        
        print(f"✓ Progress report exported: {output_path}")
    
    def save_progress(self):
        """進捗をJSONファイルに保存"""
        with open(self.checklist_file, 'w', encoding='utf-8') as f:
            json.dump({
                'project_name': self.project_name,
                'last_updated': datetime.now().isoformat(),
                'checklist': self.checklist
            }, f, indent=2, ensure_ascii=False)
    
    def load_progress(self):
        """保存された進捗を読み込み"""
        if os.path.exists(self.checklist_file):
            try:
                with open(self.checklist_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.checklist = data['checklist']
                print(f"✓ Loaded progress from: {self.checklist_file}")
            except Exception as e:
                print(f"Warning: Could not load progress file: {e}")
                print("Starting with fresh checklist")


# ============================================================================
# コマンドライン実行
# ============================================================================

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Research Project Checklist Manager')
    parser.add_argument('--project', required=True, help='Project name')
    parser.add_argument('--action', choices=['show', 'complete', 'incomplete', 'next', 'export'], 
                       default='show', help='Action to perform')
    parser.add_argument('--task-id', help='Task ID (e.g., 1.1, 2.3)')
    parser.add_argument('--output', help='Output file path (for export action)')
    
    args = parser.parse_args()
    
    # マネージャー初期化
    manager = ResearchChecklistManager(args.project)
    
    # アクション実行
    if args.action == 'show':
        manager.display_progress()
    
    elif args.action == 'complete':
        if not args.task_id:
            print("Error: --task-id required for complete action")
        else:
            manager.mark_complete(args.task_id)
            manager.display_progress()
    
    elif args.action == 'incomplete':
        if not args.task_id:
            print("Error: --task-id required for incomplete action")
        else:
            manager.mark_incomplete(args.task_id)
            manager.display_progress()
    
    elif args.action == 'next':
        print("\nNext Tasks:")
        for task in manager.get_next_tasks(limit=10):
            print(f"  - {task}")
    
    elif args.action == 'export':
        manager.export_report(args.output)
