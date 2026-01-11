# Handoff フォルダ

## 目的
Claude Desktop/Code間のセッション引き継ぎ情報を保管。
マクロレベルのコンテキスト継続を実現。

## 命名規則
- **形式**: `HND_{TASK}_{YYYYMMDD}_{HHMMSS}.md`
- **例**: `HND_SKILL_IMPROVEMENT_20260111_100000.md`

## Frontmatter形式
```yaml
---
entity_type: Handoff
name: HND_{TASK}_{YYYYMMDD}_{HHMMSS}
project_id: {PROJECT_ID}
created_at: YYYY-MM-DDTHH:MM:SS
from_client: claude_desktop | claude_code
to_client: claude_code | claude_desktop
status: pending | in_progress | completed
priority: high | medium | low
tags: []
related_entities: []
---
```

## コンテンツ構造
```markdown
# Handoff: {タスク概要}

## コンテキスト
{現在の状況、背景}

## 完了した作業
- {作業1}
- {作業2}

## 次のステップ
1. {ステップ1}
2. {ステップ2}

## 必要なリソース
- {リソース/ファイルパス}

## 注意事項
{引き継ぎ時の注意点}
```

## AIへの指示
1. Handoffはセッション終了時に作成を検討
2. from_client/to_clientを正確に記録
3. 次のセッションで必要な情報を漏れなく記載
4. FalkorDBのHandoffエンティティとも連携

## dual-client-orchestrationとの関係
このフォルダはdual-client-orchestrationスキルと連動。
Claude Desktop（対話・分析）とClaude Code（実装・コード）間の
シームレスな引き継ぎを実現する。
