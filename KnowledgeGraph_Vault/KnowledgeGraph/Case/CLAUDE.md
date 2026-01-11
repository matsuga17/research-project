# Case フォルダ

## 目的
企業・組織・プロジェクトの事例分析を保管。
理論の実証、パターンの発見、比較分析の基盤となる実証的データ。

## 命名規則
- **形式**: `CAS_{COMPANY/DOMAIN}_{IDENTIFIER}_{YYYYMMDD}.md`
- **例**: 
  - `CAS_NVIDIA_CUDA_ECOSYSTEM_20260111.md`
  - `CAS_TESLA_VERTICAL_INTEGRATION_20260111.md`
  - `CAS_SAMSUNG_AI_TRANSFORMATION_20260111.md`

## Frontmatter形式
```yaml
---
entity_type: Case
name: CAS_{IDENTIFIER}_{YYYYMMDD}
project_id: {PROJECT_ID}
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
human_verified: false
session_client: claude_desktop
case_type: company | project | event | comparison
company_name: ""
industry: ""
country: ""
time_period: ""
tags:
  - {industry}
  - {theme}
applied_theories: []
related_discoveries: []
data_sources: []
---
```

## コンテンツ構造
```markdown
# {ケースタイトル}

## ケース概要
{1-2段落でケースの概要}

## 背景・文脈
{企業/組織の背景、業界状況}

## 主要な出来事・意思決定
### {フェーズ1/イベント1}
{詳細}

### {フェーズ2/イベント2}
{詳細}

## 分析
### 適用理論
{どの理論レンズで分析するか}

### 発見されたパターン
{ケースから抽出されたパターン}

### 成功/失敗要因
{キーとなった要因}

## 理論的示唆
{このケースが理論にどう貢献するか}

## 実践的示唆
{他の企業・実務家への教訓}

## データソース
- {ソース1}
- {ソース2}

## 関連リンク
- [[THR_xxx]] - 適用した理論
- [[DIS_xxx]] - ケースから得た発見
- [[CAS_xxx]] - 比較ケース
```

## AIへの指示
1. 企業ケースは必ずcompany_name, industry, countryを記入
2. 分析には少なくとも1つの理論フレームワークを適用
3. データソースは可能な限り具体的に（SEC filing, IR資料, 記事URL等）
4. 比較ケースがあれば`case_type: comparison`を使用
5. 日韓比較研究ではcountryフィールドを活用

## 品質基準
- [ ] 背景・文脈が十分に記述されている
- [ ] 少なくとも1つの理論的分析が含まれている
- [ ] データソースが明記されている
- [ ] 理論的・実践的示唆が導出されている

## 主要ケースカテゴリ
- **AI/Tech Giants**: NVIDIA, OpenAI, Google, Meta, Tesla
- **Korean Chaebols**: Samsung, Hyundai, SK
- **Japanese Manufacturers**: Toyota, Sony, Canon
- **Platform Companies**: Apple, Amazon, Microsoft
