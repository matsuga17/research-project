# Question フォルダ

## 目的
研究課題（RQ）、未解決の問い、調査すべき疑問を記録。
研究アジェンダの管理。

## 命名規則
- **形式**: `QST_{DOMAIN}_{IDENTIFIER}_{YYYYMMDD}.md` または `RQ{N}_{TOPIC}.md`
- **例**: `QST_AI_MOAT_SUSTAINABILITY_20260111.md`, `RQ1_Dynamic_Capabilities.md`

## Frontmatter形式
```yaml
---
entity_type: Question
name: QST_{IDENTIFIER}_{YYYYMMDD}
project_id: {PROJECT_ID}
created_at: YYYY-MM-DD
human_verified: false
question_type: research_question | exploratory | verification
status: open | investigating | answered | deferred
priority: high | medium | low
tags: []
related_theories: []
potential_methods: []
---
```

## コンテンツ構造
```markdown
# {問いのタイトル}

## 問いの定式化
{明確な問いの記述}

## 背景・動機
{なぜこの問いが重要か}

## 仮説（あれば）
{予想される答え}

## 調査アプローチ
{どう調べるか}

## 関連リンク
- [[THR_xxx]]
- [[DIS_xxx]]

## 進捗メモ
{調査の進捗}
```

## AIへの指示
1. RQ（Research Question）は研究の中核
2. statusを適切に更新
3. 仮説と検証方法を明記
