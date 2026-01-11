# Task フォルダ

## 目的
研究タスク、To-Do、アクションアイテムを管理。
プロジェクト管理の基盤。

## 命名規則
- **形式**: `TSK_{PROJECT}_{IDENTIFIER}_{YYYYMMDD}.md`
- **例**: `TSK_MATE_LITERATURE_REVIEW_20260111.md`

## Frontmatter形式
```yaml
---
entity_type: Task
name: TSK_{IDENTIFIER}_{YYYYMMDD}
project_id: {PROJECT_ID}
created_at: YYYY-MM-DD
human_verified: false
task_type: research | writing | analysis | admin
status: todo | in_progress | blocked | done
priority: high | medium | low
due_date: YYYY-MM-DD
assigned_to: ""
tags: []
depends_on: []
blocks: []
---
```

## AIへの指示
1. statusを適切に更新
2. depends_on/blocksで依存関係を管理
3. due_dateがあれば必ず設定
4. Things 3との連携も検討
