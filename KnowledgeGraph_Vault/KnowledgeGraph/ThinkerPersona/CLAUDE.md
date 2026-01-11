# ThinkerPersona フォルダ

## 目的
研究に影響を与える思想家、研究者のペルソナを記録。
理論的系譜の可視化。

## 命名規則
- **形式**: `THP_{NAME}_PERSONA.md` または `{NAME}_PERSONA.md`
- **例**: `THP_TEECE_PERSONA.md`, `JENSEN_HUANG_PERSONA.md`

## Frontmatter形式
```yaml
---
entity_type: ThinkerPersona
name: THP_{NAME}_PERSONA
project_id: {PROJECT_ID}
created_at: YYYY-MM-DD
human_verified: false
persona_type: academic | practitioner | thought_leader
affiliation: ""
key_contributions: []
key_papers: []
theoretical_tradition: ""
tags: []
influenced_theories: []
---
```

## コンテンツ構造
```markdown
# {人物名}

## 略歴
{簡潔な経歴}

## 主要な貢献
- {貢献1}
- {貢献2}

## 代表的著作/発言
{重要な著作や発言}

## 思想的特徴
{その人物の思想的立場}

## 関連リンク
- [[THR_xxx]] - 提唱した理論
```

## AIへの指示
1. 学術的貢献を重視
2. 代表的著作を必ず含める
3. 思想的系譜を意識
