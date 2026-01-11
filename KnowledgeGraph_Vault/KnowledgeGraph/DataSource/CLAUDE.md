# DataSource フォルダ

## 目的
研究で使用するデータソースの情報を管理。
データ収集の体系化。

## 命名規則
- **形式**: `DS_{SOURCE_NAME}.md`
- **例**: `DS_SEC_EDGAR.md`, `DS_DART.md`

## Frontmatter形式
```yaml
---
entity_type: DataSource
name: DS_{SOURCE_NAME}
project_id: {PROJECT_ID}
created_at: YYYY-MM-DD
human_verified: false
source_type: api | database | report | website | primary
access_method: public | subscription | restricted
url: ""
update_frequency: ""
tags: []
---
```

## AIへの指示
1. アクセス方法を具体的に
2. データの更新頻度を記録
3. 利用条件・制限を明記
