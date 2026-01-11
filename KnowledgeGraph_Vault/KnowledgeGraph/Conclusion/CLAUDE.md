# Conclusion フォルダ

## 目的
研究から導出された結論、総括、要約を保管。
think-tankでの思考プロセスの最終結論を含む。

## 命名規則
- **形式**: `CON_{DOMAIN}_{IDENTIFIER}_{YYYYMMDD}.md`
- **例**: `CON_AI_PLATFORM_DYNAMICS_20260111.md`

## Frontmatter形式
```yaml
---
entity_type: Conclusion
name: CON_{IDENTIFIER}_{YYYYMMDD}
project_id: {PROJECT_ID}
created_at: YYYY-MM-DD
human_verified: false
conclusion_type: research | analysis | synthesis
confidence: high | medium | low
tags: []
based_on_discoveries: []
based_on_evidence: []
---
```

## AIへの指示
1. Conclusionは発見やエビデンスに基づく
2. confidenceレベルを正直に評価
3. based_onリンクを必ず設定
