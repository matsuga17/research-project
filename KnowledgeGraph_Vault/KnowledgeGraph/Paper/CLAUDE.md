# Paper フォルダ

## 目的
学術論文の要約、分析、メモを保管。
文献レビューの基盤となる学術文献データベース。

## 命名規則
- **形式**: `PAP_{AUTHOR}_{KEYWORD}_{YYYY}.md`
- **例**: `PAP_TEECE_DYNAMIC_CAPABILITIES_2007.md`

## Frontmatter形式
```yaml
---
entity_type: Paper
name: PAP_{AUTHOR}_{KEYWORD}_{YYYY}
project_id: {PROJECT_ID}
created_at: YYYY-MM-DD
human_verified: false
paper_type: journal | conference | working_paper | book_chapter
authors: []
year: YYYY
journal: ""
doi: ""
citation_key: ""
impact_factor: 
times_cited: 
tags: []
key_theories: []
methodology: ""
---
```

## コンテンツ構造
```markdown
# {論文タイトル}

## 書誌情報
- **著者**: 
- **年**: 
- **ジャーナル**: 
- **DOI**: 

## 要約
{論文の主要な主張と貢献}

## 理論的フレームワーク
{使用している理論}

## 方法論
{研究方法}

## 主要な発見
1. {発見1}
2. {発見2}

## 貢献
{学術的貢献}

## 限界
{論文の限界}

## 引用メモ
> "{重要な引用}" (p. XX)

## 関連リンク
- [[THR_xxx]] - 関連理論
- [[PAP_xxx]] - 関連論文
```

## AIへの指示
1. 著者名はLast Nameで統一
2. DOIがある場合は必ず記録
3. 引用は原文ママで、ページ番号付き
4. 引用スタイル: 東京大学形式に準拠
