# Framework フォルダ

## 目的
分析フレームワーク、概念的枠組みを保管。
Theoryより実践的、分析ツールとしての性格が強い。

## 命名規則
- **形式**: `FRW_{NAME}_{YYYYMMDD}.md`
- **例**: `FRW_PORTER_FIVE_FORCES_20260111.md`

## Frontmatter形式
```yaml
---
entity_type: Framework
name: FRW_{NAME}_{YYYYMMDD}
project_id: {PROJECT_ID}
created_at: YYYY-MM-DD
human_verified: true
framework_type: analytical | strategic | diagnostic | prescriptive
origin: established | proprietary | adapted
key_author: ""
tags: []
based_on_theories: []
applied_in_cases: []
---
```

## コンテンツ構造
```markdown
# {フレームワーク名}

## 概要
{フレームワークの目的と概要}

## 構成要素
### {要素1}
{説明}

### {要素2}
{説明}

## 使用方法
{どう使うか}

## 適用例
{適用事例}

## 限界
{フレームワークの限界}
```

## AIへの指示
1. Frameworkは実践的分析ツール
2. 使用方法を具体的に
3. Theoryとの違いを意識（より実践的）
