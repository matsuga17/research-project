# Discovery フォルダ

## 目的
研究過程で発見した洞察・事実・パターンを記録する永続的な知識資産。
新しい発見はまずここに登録され、検証を経てTheory/Framework/Contributionに昇格する可能性がある。

## 命名規則
- **形式**: `DIS_{DOMAIN}_{IDENTIFIER}_{YYYYMMDD}.md`
- **例**: 
  - `DIS_AI_TRANSFORMER_ATTENTION_20260111.md`
  - `DIS_PLATFORM_NETWORK_EFFECT_20260111.md`
  - `DIS_NVIDIA_CUDA_ECOSYSTEM_20260111.md`

## Frontmatter形式
```yaml
---
entity_type: Discovery
name: DIS_{DOMAIN}_{IDENTIFIER}_{YYYYMMDD}
project_id: {PROJECT_ID}  # 例: AI_RESEARCH_20260111
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
human_verified: false
session_client: claude_desktop  # または claude_code
tags:
  - {domain}
  - {subtopic}
related_theories: []
related_cases: []
source_url: ""
---
```

## コンテンツ構造
```markdown
# {発見のタイトル}

## 発見の概要
{1-2段落で発見の本質を記述}

## 詳細
{詳細な説明、背景、文脈}

## 理論的示唆
{この発見が既存理論にどう関連するか}

## 実践的示唆
{実務への応用可能性}

## エビデンス
{この発見を支持するデータ・事例}

## 限界・境界条件
{この発見が成り立つ条件、適用限界}

## 関連リンク
- [[THR_xxx]] - 関連理論
- [[CAS_xxx]] - 関連ケース
- [[EVD_xxx]] - 関連エビデンス
```

## AIへの指示
1. 新しいDiscoveryを作成する際は、必ず上記のfrontmatter形式とコンテンツ構造に従ってください
2. 命名は必ず `DIS_` プレフィックスで始め、日付を末尾に付けてください
3. 関連するTheory、Case、Evidenceがあれば、Wikiリンク形式で接続してください
4. project_idは現在のプロジェクトコンテキストに基づいて設定してください
5. 発見の重要度が高い場合は、FalkorDB (research_kg)にも登録を検討してください

## 品質基準
- [ ] 発見の新規性が明確に記述されている
- [ ] 理論的・実践的示唆が含まれている
- [ ] エビデンスまたは情報源が明記されている
- [ ] 適切なタグとリンクが設定されている
