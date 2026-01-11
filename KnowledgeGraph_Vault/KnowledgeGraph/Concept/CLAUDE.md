# Concept フォルダ

## 目的
研究で使用する重要な概念、用語、定義を保管。
共通言語としての概念辞書、オントロジーの基盤。

## 命名規則
- **形式**: `CPT_{DOMAIN}_{IDENTIFIER}_{YYYYMMDD}.md`
- **例**: `CPT_AI_DYNAMIC_MOAT_20260111.md`

## Frontmatter形式
```yaml
---
entity_type: Concept
name: CPT_{IDENTIFIER}_{YYYYMMDD}
project_id: {PROJECT_ID}
created_at: YYYY-MM-DD
human_verified: false
concept_type: technical | theoretical | operational
origin: established | coined | adapted
tags: []
related_concepts: []
used_in_theories: []
---
```

## コンテンツ構造
```markdown
# {概念名}

## 定義
{明確な定義}

## 起源・由来
{概念の出典、誰が提唱したか}

## 関連概念
- [[CPT_xxx]] - {関係性}

## 使用例
{この概念がどう使われるか}

## 類似・対立概念
{混同しやすい概念との違い}
```

## AIへの指示
1. 定義は可能な限り明確・簡潔に
2. 学術用語は出典を明記
3. 類似概念との違いを明確化
