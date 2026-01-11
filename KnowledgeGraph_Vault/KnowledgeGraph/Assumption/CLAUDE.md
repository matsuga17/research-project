# Assumption フォルダ

## 目的
研究の前提条件、仮定を明示的に記録。
理論・分析の適用範囲を明確化。

## 命名規則
- **形式**: `ASM_{DOMAIN}_{IDENTIFIER}_{YYYYMMDD}.md`
- **例**: `ASM_AI_MARKET_ASSUMPTIONS_20260111.md`

## Frontmatter形式
```yaml
---
entity_type: Assumption
name: ASM_{IDENTIFIER}_{YYYYMMDD}
project_id: {PROJECT_ID}
created_at: YYYY-MM-DD
human_verified: false
assumption_type: theoretical | empirical | methodological
validity: verified | assumed | questionable
tags: []
used_in_theories: []
---
```

## AIへの指示
1. 暗黙の前提を明示化
2. validityを正直に評価
3. 前提が崩れた場合の影響を考慮
