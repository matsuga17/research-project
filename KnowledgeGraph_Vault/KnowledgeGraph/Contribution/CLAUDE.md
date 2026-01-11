# Contribution フォルダ

## 目的
研究の理論的・実践的貢献を明示的に記録。
論文執筆時のContributionセクションの基盤。

## 命名規則
- **形式**: `CTR_{DOMAIN}_{IDENTIFIER}_{YYYYMMDD}.md`
- **例**: `CTR_MATE_THEORY_EXTENSION_20260111.md`

## Frontmatter形式
```yaml
---
entity_type: Contribution
name: CTR_{IDENTIFIER}_{YYYYMMDD}
project_id: {PROJECT_ID}
created_at: YYYY-MM-DD
human_verified: true
contribution_type: theoretical | empirical | methodological | practical
novelty_level: incremental | substantial | breakthrough
target_journal: ""
tags: []
extends_theories: []
builds_on_papers: []
---
```

## コンテンツ構造
```markdown
# {貢献タイトル}

## 貢献の要約
{1-2文で核心を記述}

## 貢献の詳細
{詳細な説明}

## 既存研究との関係
{何を拡張/修正/統合するか}

## 新規性の根拠
{なぜこれが新しいか}

## 対象読者
{誰にとって価値があるか}

## 関連リンク
- [[THR_xxx]] - 拡張する理論
- [[DIS_xxx]] - 基盤となる発見
```

## AIへの指示
1. Contributionは最も重要な知識資産
2. human_verifiedはデフォルトtrue
3. novelty_levelは控えめに評価
4. target_journalがあれば記入
