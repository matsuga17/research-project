# Dataset フォルダ

## 目的
収集・作成したデータセットの情報を管理。
データ管理の体系化。

## 命名規則
- **形式**: `DST_{NAME}_{VERSION}.md`
- **例**: `DST_KOREAN_FIRMS_2020_2024_v1.md`

## Frontmatter形式
```yaml
---
entity_type: Dataset
name: DST_{NAME}_{VERSION}
project_id: {PROJECT_ID}
created_at: YYYY-MM-DD
human_verified: false
data_type: panel | cross_sectional | time_series | qualitative
sample_size: 
time_period: ""
variables: []
storage_location: ""
tags: []
source_datasources: []
---
```

## AIへの指示
1. サンプルサイズと期間を明記
2. 変数リストを含める
3. 保存場所を記録
