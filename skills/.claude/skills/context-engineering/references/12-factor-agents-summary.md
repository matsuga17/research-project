# 12 Factor Agents 要約

**Source**: [HumanLayer 12 Factor Agents](https://github.com/humanlayer/12-factor-agents)

---

## 概要

12 Factor Agentsは、プロダクション品質のLLMアプリケーションを構築するための設計原則である。従来の「プロンプト + ツール + ループ」パターンを超え、**決定論的コードにLLM機能を戦略的に組み込む**アプローチを提唱。

> "優れたエージェントは、大部分がソフトウェアであり、LLMステップは戦略的に配置される"

---

## 12の原則

### Factor 1: Natural Language to Tool Calls
**自然言語を構造化ツール呼び出しに変換**

- ユーザー入力を構造化された関数呼び出しに変換
- LLMは「決定」を出力し、最終実行はコードが担当

### Factor 2: Own Your Prompts
**プロンプトを自分で管理**

- フレームワークの抽象化に頼らない
- プロンプトを直接制御し、最適化可能に保つ

### Factor 3: Own Your Context Window
**コンテキストウィンドウを戦略的に管理**

- 盲目的に追加せず、積極的に管理
- ダムゾーン（中央40-60%）を意識
- 使用率40-60%を目標

### Factor 4: Tools as Structured Outputs
**ツール呼び出しを構造化出力として扱う**

- ツール呼び出しは構造化データ生成
- 型安全性と検証を重視

### Factor 5: Unify Execution & Business State
**エージェント状態とアプリ状態を同期**

- エージェントの実行状態をビジネスロジックと統合
- 一貫した状態管理

### Factor 6: Launch/Pause/Resume APIs
**起動・一時停止・再開の設計**

- エージェントは他のプログラムと同様に扱う
- 開始、一時停止、再開が容易なAPI設計
- 長時間タスクや外部入力待ちに対応

### Factor 7: Contact Humans with Tool Calls
**人間への問い合わせをツール化**

- Human-in-the-loopを第一級の操作として扱う
- エッジケースではなくコア機能として設計

### Factor 8: Own Your Control Flow
**制御フローを明示的に管理**

- 暗黙的なエージェントループではなく明示的な制御
- Agent = プロンプト + switch + コンテキスト + ループ

### Factor 9: Compact Errors into Context
**エラーを効率的にコンテキストに圧縮**

- エラー情報を簡潔に表現
- LLMが理解・対応しやすい形式に

### Factor 10: Small, Focused Agents
**小さく焦点を絞ったエージェント**

- モノリシックより専門化
- 3-10ステップで完了するタスク設計
- 信頼性向上

### Factor 11: Trigger from Anywhere
**様々なトリガーに対応**

- Webhook、cron、ユーザーアクション、外部イベント
- 柔軟な起動メカニズム

### Factor 12: Stateless Reducer Pattern
**ステートレスなReducerパターン**

- エージェントを純粋関数として設計
- 入力状態 → 出力状態
- 水平スケーリングと一時停止/再開が容易

---

## 実装のポイント

### ハイブリッドシステムの推奨

効果的なLLMアプリケーションは完全に自律的ではなく、**ハイブリッドシステム**：

- **決定論的コード**: 構造とガードレールを提供
- **LLM**: 柔軟性と自然言語理解を戦略的ポイントで提供

### 70-80%の壁を超える

多くのチームが70-80%の信頼性で壁に直面：
- ループに陥る
- 不正なツール呼び出し
- 状態の追跡失敗

12 Factor Agentsはこれらの問題を構造的に解決。

### フレームワーク vs 原則

12 Factor Agentsは**フレームワークやSDKではない**：
- 言語非依存の設計原則
- 既存システムへの段階的適用が可能
- アーキテクトへのガイドライン

---

## Context Engineeringとの関係

特に重要な原則：

| Factor | Context Engineeringへの適用 |
|--------|---------------------------|
| Factor 3 | コンテキスト予算管理の基盤 |
| Factor 6 | フェーズ間の状態保存 |
| Factor 8 | Research-Plan-Implementフロー |
| Factor 9 | エラーコンパクション |
| Factor 10 | サブエージェントパターン |

---

**Last Updated**: 2025-12-06
