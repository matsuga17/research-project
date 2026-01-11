# Evidence フォルダ

## 目的
発見や理論を支持する実証的データ、統計、引用、事実を保管。
研究の信頼性を担保する客観的根拠の集積所。

## 命名規則
- **形式**: `EVD_{DOMAIN}_{IDENTIFIER}_{YYYYMMDD}.md`
- **例**: `EVD_AI_ADOPTION_RATE_2025_20260111.md`

## Frontmatter形式
```yaml
---
entity_type: Evidence
name: EVD_{IDENTIFIER}_{YYYYMMDD}
project_id: {PROJECT_ID}
created_at: YYYY-MM-DD
human_verified: false
evidence_type: statistical | qualitative | documentary | experimental
source_type: academic | industry_report | government | primary
source_url: ""
source_date: YYYY-MM-DD
reliability: high | medium | low
tags: []
supports_discoveries: []
supports_theories: []
---
```

## コンテンツ構造
```markdown
# {エビデンスタイトル}

## 概要
{何を証拠立てるデータか}

## データ内容
{具体的なデータ、統計、引用}

## 出典
- ソース: {具体的な出典}
- 日付: {データの日付}
- URL: {あれば}

## 信頼性評価
{データの信頼性についての評価}

## 支持する発見・理論
- [[DIS_xxx]]
- [[THR_xxx]]
```

## AIへの指示
1. エビデンスは必ず出典を明記
2. reliability（信頼性）を正直に評価
3. 統計データは数値を正確に記録
4. 古いデータの場合はsource_dateで明示
