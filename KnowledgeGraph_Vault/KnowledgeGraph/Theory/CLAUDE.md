# Theory フォルダ

## 目的
検証済みの理論的枠組み、概念モデル、フレームワークを保管する知識資産の中核。
確立された学術理論と独自開発の理論フレームワーク両方を含む。

## 命名規則
- **形式**: `THR_{DOMAIN}_{IDENTIFIER}_{YYYYMMDD}.md`
- **例**: 
  - `THR_DYNAMIC_CAPABILITIES_20260111.md`
  - `THR_PLATFORM_THEORY_20260111.md`
  - `THR_MATE_COEVOLUTION_20260111.md`

## Frontmatter形式
```yaml
---
entity_type: Theory
name: THR_{DOMAIN}_{IDENTIFIER}_{YYYYMMDD}
project_id: {PROJECT_ID}
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
human_verified: true  # Theoryは検証済みが基本
session_client: claude_desktop
theory_type: established | emerging | proprietary
key_authors: []
key_papers: []
tags:
  - {domain}
  - {theoretical_tradition}
related_theories: []
applied_cases: []
---
```

## コンテンツ構造
```markdown
# {理論名}

## 理論の概要
{理論の核心的主張を1-2段落で}

## 主要概念
### {概念1}
{定義と説明}

### {概念2}
{定義と説明}

## 理論的前提
{この理論が成立するための前提条件}

## 核心的命題
1. {命題1}
2. {命題2}
3. {命題3}

## 実証的支持
{この理論を支持する実証研究}

## 批判と限界
{理論への批判、適用限界}

## 発展可能性
{理論の拡張方向、未解決の問い}

## 関連リンク
- [[THR_xxx]] - 関連・対立理論
- [[DIS_xxx]] - この理論から導かれた発見
- [[CAS_xxx]] - 適用事例
```

## AIへの指示
1. Theoryは知識資産の中核であり、慎重に作成してください
2. 確立された理論（RBV, Dynamic Capabilities等）は`theory_type: established`
3. 独自開発の理論（MATE等）は`theory_type: proprietary`
4. 必ずkey_authorsとkey_papersを可能な限り記入してください
5. human_verifiedはデフォルトtrueですが、仮説段階ならfalseに

## 品質基準
- [ ] 理論の核心的主張が明確
- [ ] 主要概念の定義が含まれている
- [ ] 理論的前提が明示されている
- [ ] 少なくとも1つの関連リンクがある

## 主要理論一覧（参考）
- THR_RESOURCE_BASED_VIEW_RBV
- THR_DYNAMIC_CAPABILITIES
- THR_PLATFORM_THEORY
- THR_ECOSYSTEM_THEORY
- THR_INSTITUTIONAL_THEORY
- THR_TRANSACTION_COST_ECONOMICS
- MATE_Theory_Cognitive_Foundation
