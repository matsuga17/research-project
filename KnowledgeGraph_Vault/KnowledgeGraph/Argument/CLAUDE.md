# Argument フォルダ

## 目的
研究における主張、命題、仮説を体系的に記録。
理論構築の中間段階であり、検証を経てTheory/Contributionに発展する可能性。

## 命名規則
- **形式**: `ARG_{DOMAIN}_{IDENTIFIER}_{YYYYMMDD}.md`
- **例**: `ARG_AI_MOAT_SUSTAINABILITY_20260111.md`

## Frontmatter形式
```yaml
---
entity_type: Argument
name: ARG_{IDENTIFIER}_{YYYYMMDD}
project_id: {PROJECT_ID}
created_at: YYYY-MM-DD
human_verified: false
argument_type: proposition | hypothesis | claim | critique
status: proposed | testing | supported | refuted
confidence: high | medium | low
tags: []
supporting_evidence: []
counter_evidence: []
related_theories: []
---
```

## コンテンツ構造
```markdown
# {主張タイトル}

## 主張の要約
{1-2文で核心を記述}

## 詳細な論証
{主張の詳細な説明と論理展開}

## 支持するエビデンス
- [[EVD_xxx]]

## 反証・限界
{反証や境界条件}

## 理論的位置づけ
{既存理論との関係}

## 検証方法
{この主張をどう検証できるか}
```

## AIへの指示
1. ArgumentはTheoryの前段階として位置づけ
2. statusを適切に更新（proposed→testing→supported/refuted）
3. 反証可能性を意識した記述を心がける
