# Theoretical Frameworks Reference

戦略経営・組織論研究で頻繁に使用される主要理論フレームワークの概要と適用例

---

## 1. Resource-Based View (RBV)

### 基本概念
企業の競争優位は、**貴重（Valuable）、稀少（Rare）、模倣困難（Inimitable）、組織的（Organized）** な経営資源（VRIO）から生まれる。

### 主要文献
- Barney, J. (1991). Firm resources and sustained competitive advantage. *Journal of Management*, 17(1), 99-120.
- Wernerfelt, B. (1984). A resource-based view of the firm. *Strategic Management Journal*, 5(2), 171-180.

### 典型的な仮説
- H1: 企業特有の資源蓄積 → 持続的競争優位 → 高業績
- H2: 模倣困難な知識資産 → イノベーション能力 → 市場優位性

### 測定例
```python
# 企業特有資源の代理変数
- R&D intensity (R&D支出/売上)
- Patent stock（特許ストック）
- Brand value（ブランド価値）
- Human capital（従業員スキル）
- Organizational routines（組織ルーチン）
```

---

## 2. Dynamic Capabilities

### 基本概念
変化する環境で、企業が資源を**感知（Sense）、捕捉（Seize）、再構成（Transform）** する能力。

### 主要文献
- Teece, D. J., Pisano, G., & Shuen, A. (1997). Dynamic capabilities and strategic management. *Strategic Management Journal*, 18(7), 509-533.
- Eisenhardt, K. M., & Martin, J. A. (2000). Dynamic capabilities: What are they? *Strategic Management Journal*, 21(10-11), 1105-1121.

### 典型的な仮説
- H1: Dynamic capabilities → 環境変化への適応 → 長期業績
- H2: 組織学習能力 → 資源再構成 → イノベーション

### 測定例
```python
# Dynamic capabilities代理変数
- R&D変動係数（CV of R&D spending）
- 組織構造変更頻度
- 新製品導入速度
- M&A活動（資源再構成）
- 戦略的提携数（外部知識獲得）
```

---

## 3. Institutional Theory

### 基本概念
組織は、**規制的（Regulative）、規範的（Normative）、文化認知的（Cultural-Cognitive）** な制度圧力に適応する。

### 主要文献
- DiMaggio, P. J., & Powell, W. W. (1983). The iron cage revisited: Institutional isomorphism. *American Sociological Review*, 48(2), 147-160.
- Scott, W. R. (2001). *Institutions and Organizations*. Sage Publications.

### 典型的な仮説
- H1: 制度圧力（規制・規範） → 同型化（Isomorphism） → 組織実践の標準化
- H2: 正統性（Legitimacy）追求 → ESG実践 → 利害関係者支持

### 測定例
```python
# 制度圧力の代理変数
- 政府規制強度（Government regulation）
- 業界規範遵守（Industry norm compliance）
- ISO認証取得（Certification）
- ESG開示スコア（ESG disclosure）
- 業界団体加入数（Association membership）
```

---

## 4. Transaction Cost Economics (TCE)

### 基本概念
企業は、**取引コスト（情報探索、交渉、履行監視）** を最小化するために、市場取引と内部化を選択する。

### 主要文献
- Williamson, O. E. (1985). *The Economic Institutions of Capitalism*. Free Press.
- Coase, R. H. (1937). The nature of the firm. *Economica*, 4(16), 386-405.

### 典型的な仮説
- H1: 資産特殊性（Asset specificity）↑ → 垂直統合
- H2: 不確実性↑ → 長期契約 or 内部化
- H3: 取引頻度↑ → 統合の経済性

### 測定例
```python
# 取引コストの代理変数
- 垂直統合度（Vertical integration）
- Make-or-buy比率
- 長期契約比率（Long-term contract ratio）
- サプライヤー数（Supplier count）
- 外注比率（Outsourcing ratio）
```

---

## 5. Agency Theory

### 基本概念
プリンシパル（株主）とエージェント（経営者）の利害不一致から生じる**エージェンシー問題**を、インセンティブとモニタリングで解決。

### 主要文献
- Jensen, M. C., & Meckling, W. H. (1976). Theory of the firm: Managerial behavior, agency costs and ownership structure. *Journal of Financial Economics*, 3(4), 305-360.
- Fama, E. F., & Jensen, M. C. (1983). Separation of ownership and control. *Journal of Law and Economics*, 26(2), 301-325.

### 典型的な仮説
- H1: 所有権分散 → エージェンシー問題 → 業績低下
- H2: インセンティブ報酬（Stock options）→ 利害一致 → 業績向上
- H3: 独立取締役比率 → モニタリング強化 → ガバナンス改善

### 測定例
```python
# Agency cost代理変数
- CEO報酬/従業員平均給与（CEO pay ratio）
- 株式報酬比率（Equity-based compensation）
- 独立取締役比率（Board independence）
- 機関投資家持株比率（Institutional ownership）
- 自由裁量支出（Discretionary spending）
```

---

## 6. Stakeholder Theory

### 基本概念
企業は、株主だけでなく、**従業員、顧客、サプライヤー、地域社会、環境**など多様なステークホルダーの利益を考慮すべき。

### 主要文献
- Freeman, R. E. (1984). *Strategic Management: A Stakeholder Approach*. Pitman.
- Donaldson, T., & Preston, L. E. (1995). The stakeholder theory of the corporation. *Academy of Management Review*, 20(1), 65-91.

### 典型的な仮説
- H1: ステークホルダー重視 → 正統性獲得 → 長期業績
- H2: CSR活動 → 従業員満足 → 生産性向上
- H3: 地域社会貢献 → ブランド価値 → 顧客ロイヤルティ

### 測定例
```python
# Stakeholder engagement代理変数
- CSRスコア（CSR rating）
- 従業員満足度（Employee satisfaction）
- 顧客満足度（Customer satisfaction）
- サプライヤー関係（Supplier relationship）
- 地域貢献度（Community involvement）
```

---

## 7. Industrial Organization (IO)

### 基本概念
業界構造（Structure）が企業行動（Conduct）を決定し、それが業績（Performance）に影響する（**SCP paradigm**）。

### 主要文献
- Porter, M. E. (1980). *Competitive Strategy*. Free Press.
- Bain, J. S. (1956). *Barriers to New Competition*. Harvard University Press.

### 典型的な仮説
- H1: 業界集中度（HHI）↑ → 競争圧力↓ → 高収益性
- H2: 参入障壁↑ → 既存企業優位 → 超過利潤
- H3: 代替品脅威↑ → 価格競争 → 利益率低下

### 測定例
```python
# 業界構造の代理変数
- HHI（Herfindahl-Hirschman Index）
- 業界上位4社集中率（CR4）
- 参入障壁（Entry barrier）: 最小効率規模、R&D集約度
- 業界成長率（Industry growth rate）
- 規制強度（Regulatory intensity）
```

---

## 8. Knowledge-Based View (KBV)

### 基本概念
企業は**知識創造・統合・活用**のシステムであり、競争優位の源泉は知識にある。

### 主要文献
- Grant, R. M. (1996). Toward a knowledge-based theory of the firm. *Strategic Management Journal*, 17(S2), 109-122.
- Nonaka, I., & Takeuchi, H. (1995). *The Knowledge-Creating Company*. Oxford University Press.

### 典型的な仮説
- H1: 暗黙知（Tacit knowledge） → 模倣困難性 → 持続的優位
- H2: 知識統合能力 → イノベーション → 業績
- H3: 組織学習 → 知識蓄積 → 競争力

### 測定例
```python
# 知識関連変数
- R&D人員比率（R&D personnel ratio）
- 特許引用数（Patent citations）
- 従業員教育投資（Training investment）
- 知識労働者比率（Knowledge worker ratio）
- 共同研究数（Collaborative R&D）
```

---

## 理論選択ガイド

### 研究テーマ別推奨理論

| 研究テーマ | 推奨理論 |
|-----------|---------|
| イノベーション・R&D | RBV, Dynamic Capabilities, KBV |
| M&A・提携戦略 | TCE, Dynamic Capabilities, RBV |
| グローバル戦略 | Institutional Theory, TCE |
| コーポレートガバナンス | Agency Theory, Stakeholder Theory |
| ESG/サステナビリティ | Stakeholder Theory, Institutional Theory |
| 競争戦略 | IO, RBV, Dynamic Capabilities |
| 組織変革 | Dynamic Capabilities, Institutional Theory |

### 複数理論の統合例

**研究例**: 「R&Dアライアンスが企業イノベーションに与える影響」

1. **RBV**: R&D資源の補完性（Resource complementarity）
2. **KBV**: 知識統合能力（Knowledge integration）
3. **TCE**: アライアンスガバナンス（Alliance governance）
4. **Social Capital Theory**: ネットワーク効果（Network effects）

**仮説構築**:
```
H1 (RBV): パートナー間の資源補完性 → イノベーション成果
H2 (KBV): 知識統合能力の調整効果 → H1を強化
H3 (TCE): 契約ガバナンス → 機会主義抑制 → H1を強化
```

---

## 統計分析との対応

### 理論→変数→分析手法

**例: Dynamic Capabilities研究**

```python
# 理論的構成概念
dynamic_capabilities = ['sensing', 'seizing', 'transforming']

# 操作的定義（測定変数）
sensing = ['R&D_intensity', 'external_alliance', 'market_research']
seizing = ['new_product_launches', 'M&A_activity', 'strategic_investment']
transforming = ['organizational_restructuring', 'process_innovation']

# 従属変数
performance = ['ROA', 'tobin_q', 'sales_growth']

# 統計モデル
# Panel FE regression + Interaction effects
model = """
    Performance_it = β0 + β1*Dynamic_Cap_it + β2*Env_Dynamism_it
                   + β3*(Dynamic_Cap × Env_Dynamism)_it
                   + Controls + Firm_FE + Year_FE + ε_it
"""
```

---

## 参考: トップジャーナルの理論使用頻度

### Strategic Management Journal (2020-2024)

| 理論 | 使用頻度 |
|------|---------|
| RBV | 35% |
| Dynamic Capabilities | 28% |
| Institutional Theory | 18% |
| Agency Theory | 12% |
| TCE | 10% |
| Stakeholder Theory | 8% |
| KBV | 15% |
| IO | 7% |

*複数理論使用の場合、重複カウント

---

## 追加リソース

### 理論深堀り推奨書籍

1. **Strategic Management**
   - Barney, J. B., & Hesterly, W. S. (2015). *Strategic Management and Competitive Advantage*. Pearson.

2. **Organization Theory**
   - Scott, W. R., & Davis, G. F. (2015). *Organizations and Organizing*. Routledge.

3. **Research Methods**
   - Ketokivi, M., & McIntosh, C. N. (2017). Addressing the endogeneity dilemma in operations management research. *Journal of Operations Management*, 52, 1-14.

---

**最終更新**: 2025-11-01  
**参照元**: Strategic Research Suite v4.0

[← Back to Suite Home](../README.md)
