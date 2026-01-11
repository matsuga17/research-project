# Variable フォルダ

## 目的
研究で使用する変数、指標、測定項目を定義。
実証研究の操作化の基盤。

## 命名規則
- **形式**: `VAR_{DOMAIN}_{IDENTIFIER}_{YYYYMMDD}.md`
- **例**: `VAR_AI_INFERENCE_METRICS_20260111.md`

## Frontmatter形式
```yaml
---
entity_type: Variable
name: VAR_{IDENTIFIER}_{YYYYMMDD}
project_id: {PROJECT_ID}
created_at: YYYY-MM-DD
human_verified: false
variable_type: dependent | independent | control | mediator | moderator
measurement_level: nominal | ordinal | interval | ratio
operationalization: ""
data_source: ""
tags: []
used_in_theories: []
---
```

## AIへの指示
1. 変数の操作的定義を明確に
2. 測定方法を具体的に記述
3. データソースを明記
