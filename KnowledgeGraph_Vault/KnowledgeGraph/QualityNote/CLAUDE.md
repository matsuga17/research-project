# QualityNote フォルダ

## 目的
KG品質監査、データクリーニング、メンテナンスの記録を保管。
システム運用の履歴管理。

## 命名規則
- **形式**: `QN_{TYPE}_{YYYYMMDD}.md`
- **例**: `QN_WEEKLY_AUDIT_20260111.md`

## Frontmatter形式
```yaml
---
entity_type: QualityNote
name: QN_{TYPE}_{YYYYMMDD}
project_id: SYSTEM_MAINTENANCE
created_at: YYYY-MM-DD
human_verified: true
note_type: audit | cleanup | migration | backup
status: completed | in_progress | planned
entities_affected: 
tags: []
---
```

## コンテンツ構造
```markdown
# {品質ノートタイトル}

## 概要
{何を行ったか}

## 実行内容
- {作業1}
- {作業2}

## 結果
{Before/After指標}

## 次回アクション
{次に必要な作業}
```

## AIへの指示
1. 品質監査は定期的に実施
2. Before/After指標を必ず記録
3. スクリプト実行ログを含める
