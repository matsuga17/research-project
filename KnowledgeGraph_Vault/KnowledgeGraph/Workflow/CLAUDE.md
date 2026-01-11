# Workflow フォルダ

## 目的
研究プロセス、分析手順、作業フローを体系化。
再現可能な研究方法論の蓄積。

## 命名規則
- **形式**: `WFL_{DOMAIN}_{IDENTIFIER}_{YYYYMMDD}.md`
- **例**: `WFL_LITERATURE_REVIEW_PROCESS_20260111.md`

## Frontmatter形式
```yaml
---
entity_type: Workflow
name: WFL_{IDENTIFIER}_{YYYYMMDD}
project_id: {PROJECT_ID}
created_at: YYYY-MM-DD
human_verified: false
workflow_type: research | analysis | writing | data_collection
automation_level: manual | semi-automated | fully-automated
tools_required: []
tags: []
---
```

## コンテンツ構造
```markdown
# {ワークフロー名}

## 目的
{このワークフローの目的}

## 前提条件
{必要なツール、データ、準備}

## 手順
### Step 1: {ステップ名}
{詳細}

### Step 2: {ステップ名}
{詳細}

## 出力物
{このワークフローの成果物}

## 注意点
{よくある問題と対処法}
```

## AIへの指示
1. 手順は再現可能なレベルで具体的に
2. 使用ツールを明記
3. 自動化可能な部分を明示
