# KnowledgeGraph Vault

## 概要
研究ナレッジグラフのObsidianインターフェース。
FalkorDB (research_kg) と双方向同期し、人間可読な知識資産を管理。

## システムアーキテクチャ
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   think-tank    │────▶│    FalkorDB     │────▶│   Obsidian      │
│  (一時記憶)      │     │  (research_kg)   │     │   (この Vault)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                      │                      │
         └──────────────────────┴──────────────────────┘
                    リアルタイム同期
```

## フォルダ構成

### 知識エンティティ（永続的知識資産）
| フォルダ | プレフィックス | 目的 |
|----------|--------------|------|
| Discovery/ | DIS_ | 発見・洞察 |
| Theory/ | THR_ | 理論・フレームワーク |
| Case/ | CAS_ | 事例分析 |
| Evidence/ | EVD_ | エビデンス・データ |
| Argument/ | ARG_ | 主張・命題 |
| Concept/ | CPT_ | 概念・定義 |
| Conclusion/ | CON_ | 結論・総括 |
| Contribution/ | CTR_ | 理論的貢献 |
| Paper/ | PAP_ | 文献メモ |
| Framework/ | FRW_ | 分析フレームワーク |

### 研究支援
| フォルダ | プレフィックス | 目的 |
|----------|--------------|------|
| Question/ | QST_/RQ | 研究課題 |
| Assumption/ | ASM_ | 前提条件 |
| Variable/ | VAR_ | 変数定義 |
| Workflow/ | WFL_ | 作業フロー |
| Task/ | TSK_ | タスク管理 |

### データ管理
| フォルダ | プレフィックス | 目的 |
|----------|--------------|------|
| DataSource/ | DS_ | データソース |
| Dataset/ | DST_ | データセット |

### システム
| フォルダ | プレフィックス | 目的 |
|----------|--------------|------|
| Handoff/ | HND_ | セッション引き継ぎ |
| ThinkerPersona/ | THP_ | 思想家ペルソナ |
| QualityNote/ | QN_ | 品質管理記録 |

### 特殊フォルダ
- `_Templates/` - テンプレートファイル
- `_Index/` - インデックス・ダッシュボード
- `_Archive/` - アーカイブ
- `Daily Notes/` - 日次ノート
- `Inbox/` - 未整理ノート

## 命名規則

### 標準形式
```
{PREFIX}_{DOMAIN}_{IDENTIFIER}_{YYYYMMDD}.md
```

### 例
- `DIS_AI_TRANSFORMER_ATTENTION_20260111.md`
- `THR_DYNAMIC_CAPABILITIES_20260111.md`
- `CAS_NVIDIA_CUDA_ECOSYSTEM_20260111.md`

## Frontmatter標準 (v2.2)
```yaml
---
entity_type: {EntityType}
name: {PREFIX}_{IDENTIFIER}_{YYYYMMDD}
project_id: {PROJECT_ID}
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
human_verified: false
session_client: claude_desktop | claude_code
tags: []
---
```

## AIへの指示

### 基本ルール
1. **各フォルダのCLAUDE.mdを参照**: 作成前に対象フォルダのCLAUDE.mdを確認
2. **命名規則を厳守**: プレフィックス + ドメイン + 識別子 + 日付
3. **Frontmatter必須**: v2.2形式に準拠
4. **リンク設定**: 関連エンティティはWikiリンク `[[xxx]]` で接続

### FalkorDB連携
- 重要なエンティティはFalkorDB (research_kg)にも登録
- graphName: `research_kg`
- ツール: `falkordb:query_graph`

### 同期スクリプト
- 場所: `/Users/changu/Desktop/研究/kg-sync/`
- 自動同期: LaunchDで定期実行

## 関連スキル
- `/mnt/skills/user/research-knowledge-platform/SKILL.md`
- `/mnt/skills/user/dual-client-orchestration/SKILL.md`
- `/mnt/skills/user/context-engineering/SKILL.md`

## 品質基準
- 孤立ノード率: <3%
- project_id設定率: 100%
- human_verified率: >90%（重要エンティティ）

---
*Last Updated: 2026-01-11*
*Version: 2.2*
