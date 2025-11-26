# Strategic Research Suite - Metadata

**Suite Version**: 4.0  
**Last Updated**: 2025-11-01  
**Original Source**: strategic-management-research-hub v3.0

---

## Suite Structure

このsuiteは、戦略経営・組織論の実証研究を体系的に支援する8つの専門スキルで構成されています。

### スキル一覧

| # | スキル名 | トークン | 用途 |
|---|---------|---------|------|
| 1 | core-workflow | ~15k | Phase 1-8の基本ワークフロー、研究全体の起点 |
| 2 | data-sources | ~18k | データソースカタログ（北米・欧州・アジア・無料） |
| 3 | statistical-methods | ~14k | 高度な統計手法（FE/RE, IV, PSM, DiD等） |
| 4 | text-analysis | ~12k | テキスト分析（MD&A, センチメント, トピックモデル） |
| 5 | network-analysis | ~11k | ネットワーク分析（取締役、提携、特許引用） |
| 6 | causal-ml | ~10k | 機械学習×因果推論（Causal Forest, DML等） |
| 7 | esg-sustainability | ~12k | ESG/サステナビリティデータソース |
| 8 | automation | ~8k | Phase 1-8完全自動化パイプライン |

**合計**: ~100k tokens  
**平均**: ~12.5k tokens（従来比87%削減）

---

## スキル選択ガイド

### シナリオ別推奨スキル

#### 【初めての戦略研究】
```
1-core-workflow → 2-data-sources → 3-statistical-methods
```

#### 【日本企業のイノベーション研究】
```
1-core-workflow → 2-data-sources (日本セクション) 
→ 4-text-analysis (特許) → 3-statistical-methods
```

#### 【ESG戦略とパフォーマンス】
```
1-core-workflow → 7-esg-sustainability 
→ 2-data-sources (CDP, EPA) → 6-causal-ml
```

#### 【完全自動化研究】
```
8-automation（内部で必要に応じて他スキルを参照）
```

---

## 共通参照情報

### 理論フレームワーク

**主要理論**:
- Resource-Based View (RBV)
- Dynamic Capabilities
- Institutional Theory
- Industrial Organization (IO)
- Transaction Cost Economics (TCE)
- Agency Theory
- Stakeholder Theory

### ターゲットジャーナル

**Top-tier**:
- Strategic Management Journal (SMJ)
- Academy of Management Journal (AMJ)
- Organization Science (OS)
- Administrative Science Quarterly (ASQ)
- Management Science

**Field-specific**:
- Journal of Management
- Journal of International Business Studies (JIBS)
- Strategic Entrepreneurship Journal (SEJ)

---

## バージョン履歴

### v4.0 (2025-11-01)
- 98kトークンの単一スキルを8専門スキルに分割
- 共通ユーティリティ（_shared）の導入
- トークン消費87%削減
- スキル間相互参照システムの実装

### v3.0 (2024)
- Asian Data Sources追加（11カ国）
- ESG拡張
- ML/因果推論統合

### v2.0
- テキスト分析・ネットワーク分析追加

### v1.0
- 初版リリース

---

## License & Citation

**License**: MIT License（学術利用自由、商用利用可）

**Citation**:
```
Strategic Research Suite v4.0 (2025)
https://github.com/[your-repo]/strategic-research-suite
```

---

## Support

**Issues**: [GitHub Issues]  
**Email**: [research-support@example.com]  
**Documentation**: 各スキルのSKILL.mdを参照
