# 研究計画書テンプレート
# Research Plan Template

**作成日 / Date**: [YYYY-MM-DD]  
**研究者 / Researcher**: [氏名 / Name]  
**所属 / Affiliation**: [大学・機関名 / Institution]  
**バージョン / Version**: [v1.0]

---

## 1. 研究タイトル / Research Title

### 日本語タイトル
[30-40字程度で研究の核心を表現]

### 英語タイトル
[Main Title: Subtitle format, approximately 10-15 words]

**キーワード / Keywords**: [5-7 keywords in Japanese and English]

---

## 2. 研究背景と動機 / Background and Motivation

### 2.1 研究領域の重要性
**Why does this research domain matter?**

- [産業界・社会における重要性]
- [学術的重要性]
- [政策的含意]

### 2.2 先行研究の限界
**What gaps exist in prior literature?**

| 先行研究 / Prior Study | 貢献 / Contribution | 限界 / Limitation |
|---|---|---|
| [著者, 年] | [主要な発見] | [残された問題] |
| [著者, 年] | [主要な発見] | [残された問題] |
| [著者, 年] | [主要な発見] | [残された問題] |

### 2.3 本研究の位置づけ
**How does this study fill the gap?**

[本研究の独自性と貢献を2-3文で簡潔に説明]

---

## 3. 理論フレームワークと仮説 / Theoretical Framework and Hypotheses

### 3.1 適用理論
**Theoretical Foundation**

**主要理論 / Main Theory**: [RBV, Dynamic Capabilities, TCE, Agency Theory, etc.]

**理論の説明**:
- [理論の核心的主張]
- [本研究への適用方法]
- [なぜこの理論が適切か]

**参考文献**:
- [理論の原典]
- [重要な発展研究]

### 3.2 概念モデル
**Conceptual Model**

```
独立変数 (X)          調整変数 (M)          従属変数 (Y)
───────────>        ┌─────┐         ───────────>
[具体的変数名]       │      │        [具体的変数名]
                    └──┬──┘
                       │
                    調整効果

統制変数 (Control Variables):
- [CV1: 企業規模]
- [CV2: 企業年齢]
- [CV3: 産業]
- [CV4: 年次]
```

### 3.3 仮説
**Hypotheses**

#### H1: [主効果仮説 / Main Effect Hypothesis]
**仮説文**:
- 日本語: [X は Y に正（負）の影響を与える]
- English: [X is positively (negatively) associated with Y]

**理論的根拠 / Theoretical Rationale**:
[なぜこの関係が予測されるか、理論に基づいて説明（3-5文）]

#### H2: [調整効果仮説 / Moderation Hypothesis]
**仮説文**:
- 日本語: [M は X と Y の正の関係を強化（弱化）する]
- English: [M strengthens (weakens) the positive relationship between X and Y]

**理論的根拠**:
[調整変数がなぜこの効果を持つか（3-5文）]

#### H3: [非線形・媒介仮説 / Nonlinear/Mediation Hypothesis]
**仮説文**:
- [必要に応じて追加]

**理論的根拠**:
- [説明]

---

## 4. 研究デザイン / Research Design

### 4.1 研究手法
**Research Method**

- **研究タイプ**: 
  - [ ] 横断研究 / Cross-sectional study
  - [ ] パネルデータ研究 / Panel data study
  - [ ] イベントスタディ / Event study
  - [ ] ケーススタディ / Case study
  - [ ] 実験・準実験 / Experimental/Quasi-experimental

- **分析手法**: 
  - [ ] OLS回帰 / OLS regression
  - [ ] 固定効果モデル / Fixed effects
  - [ ] 変量効果モデル / Random effects
  - [ ] 差分の差分法 / Difference-in-differences
  - [ ] 操作変数法 / Instrumental variables
  - [ ] 傾向スコアマッチング / Propensity score matching
  - [ ] 生存分析 / Survival analysis

### 4.2 サンプル
**Sample**

- **母集団 / Population**: [例: 日本の東証一部上場製造業企業]
- **サンプリング基準 / Sampling Criteria**:
  1. [基準1: 業種]
  2. [基準2: 期間]
  3. [基準3: データ利用可能性]
  4. [基準4: その他の除外基準]

- **サンプルサイズ目標 / Target Sample Size**:
  - 企業数 / Number of firms: [N = XXX]
  - 観測値数 / Number of observations: [N*T = XXX]
  - 期間 / Time period: [YYYY to YYYY]

- **サンプリング戦略 / Sampling Strategy**:
  - [ ] 全数調査 / Complete enumeration
  - [ ] ランダムサンプリング / Random sampling
  - [ ] 層化サンプリング / Stratified sampling
  - [ ] マッチングサンプル / Matched sample

### 4.3 変数の定義と測定
**Variable Definitions and Measurement**

#### 従属変数 / Dependent Variable(s)

| 変数名 | 定義 | 測定方法 | データソース |
|--------|------|----------|--------------|
| Y1: [例: ROA] | [純利益/総資産] | [連続変数、%] | [Compustat/EDINET] |
| Y2: [例: イノベーション] | [特許出願数] | [カウントデータ] | [USPTO] |

#### 独立変数 / Independent Variable(s)

| 変数名 | 定義 | 測定方法 | データソース |
|--------|------|----------|--------------|
| X1: [例: R&D強度] | [R&D支出/売上高] | [連続変数、%] | [Compustat] |
| X2: [例: 取締役会多様性] | [女性取締役比率] | [連続変数、0-1] | [ExecuComp/有価証券報告書] |

#### 調整変数 / Moderator Variable(s)

| 変数名 | 定義 | 測定方法 | データソース |
|--------|------|----------|--------------|
| M1: [例: 環境動態性] | [産業売上の標準偏差] | [連続変数] | [Compustat] |

#### 統制変数 / Control Variables

| 変数名 | 定義 | 測定方法 | データソース |
|--------|------|----------|--------------|
| CV1: 企業規模 | log(総資産) | 連続変数 | Compustat/EDINET |
| CV2: 企業年齢 | 現在年 - 設立年 | 連続変数 | Compustat/EDINET |
| CV3: レバレッジ | 総負債/総資産 | 連続変数、0-1 | Compustat/EDINET |
| CV4: 産業ダミー | 2桁SIC | ダミー変数 | Compustat |
| CV5: 年次ダミー | 年 | ダミー変数 | - |

---

## 5. データソースと収集戦略 / Data Sources and Collection Strategy

### 5.1 データソース一覧
**Data Sources**

| データタイプ | データソース | アクセス方法 | コスト | データ範囲 |
|--------------|--------------|--------------|--------|------------|
| 財務データ | [Compustat/EDINET] | [WRDS/無料DL] | [有料/無料] | [1980-2024] |
| ガバナンスデータ | [ExecuComp/有報] | [WRDS/EDINET] | [有料/無料] | [1992-2024] |
| 特許データ | [USPTO PatentsView] | [API/ダウンロード] | [無料] | [1976-2024] |
| 産業データ | [Compustat Segments] | [WRDS] | [有料] | [1980-2024] |
| マクロデータ | [World Bank/OECD] | [API/ウェブ] | [無料] | [1960-2024] |

### 5.2 データ収集計画
**Data Collection Plan**

#### フェーズ1: パイロット収集（1週間）
- **目的**: データアクセスの確認、変数の利用可能性検証
- **サンプル**: 10-20企業
- **タスク**:
  1. [データベースへのアクセス確認]
  2. [変数の利用可能性確認]
  3. [欠損値の割合確認]
  4. [データ品質の初期評価]

#### フェーズ2: フルデータ収集（3-6週間）
- **Week 1-2**: [財務データ収集]
- **Week 3-4**: [ガバナンスデータ収集]
- **Week 5-6**: [特許・産業データ収集]

#### フェーズ3: データ統合とクリーニング（2-4週間）
- **Week 1**: [データマージ、識別子の確認]
- **Week 2**: [欠損値処理]
- **Week 3**: [外れ値処理]
- **Week 4**: [最終データセット作成]

### 5.3 データ品質管理
**Data Quality Control**

- **識別子の整合性**: [企業識別コードの統一（CUSIP, GVKEY, etc.）]
- **時系列の整合性**: [決算期の統一、タイムラグの確認]
- **欠損値の対処**: 
  - [戦略1: リストワイズ削除]
  - [戦略2: インディケータ法]
  - [戦略3: 多重代入法]
- **外れ値の対処**: 
  - [基準1: ±3標準偏差]
  - [基準2: ウィンソライズ（1%/99%）]
  - [基準3: 業界標準からの乖離]

---

## 6. 分析計画 / Analysis Plan

### 6.1 記述統計
**Descriptive Statistics**

- **要約統計量**: 平均、標準偏差、最小値、最大値、中央値
- **相関行列**: すべての主要変数間の相関係数
- **多重共線性チェック**: VIF（Variance Inflation Factor）< 10

### 6.2 メイン分析
**Main Analysis**

#### モデル1: ベースラインモデル（統制変数のみ）
```
Y = β0 + β1(Firm Size) + β2(Firm Age) + β3(Leverage) 
    + Industry FE + Year FE + ε
```

#### モデル2: 主効果モデル（H1のテスト）
```
Y = β0 + β1(X) + β2(Firm Size) + β3(Firm Age) + β4(Leverage)
    + Industry FE + Year FE + ε
```

#### モデル3: 調整効果モデル（H2のテスト）
```
Y = β0 + β1(X) + β2(M) + β3(X × M) + Controls
    + Industry FE + Year FE + ε
```

#### モデル4: フルモデル（すべての仮説）
```
Y = β0 + β1(X1) + β2(X2) + β3(M1) + β4(X1 × M1) + β5(X2 × M1) 
    + Controls + Industry FE + Year FE + ε
```

### 6.3 ロバストネスチェック
**Robustness Checks**

1. **代替従属変数**: [ROE, ROSを使用]
2. **代替サンプル**: 
   - [特定産業を除外]
   - [大企業のみ]
   - [小企業のみ]
3. **代替推定方法**: 
   - [ロバスト標準誤差]
   - [クラスター標準誤差（企業レベル）]
   - [2段階推定（Heckman）]
4. **内生性への対処**: 
   - [ラグ付きIV]
   - [操作変数法]
   - [固定効果モデル]

### 6.4 追加分析
**Additional Analyses**

- **サブサンプル分析**: [産業別、規模別、期間別]
- **媒介分析**: [必要に応じて]
- **非線形効果**: [二次項の追加]

---

## 7. 予想される結果と含意 / Expected Results and Implications

### 7.1 予想される発見
**Expected Findings**

- **H1**: [予想される効果の方向と大きさ]
- **H2**: [予想される調整効果]
- **H3**: [予想される結果]

### 7.2 理論的貢献
**Theoretical Contributions**

1. [理論への貢献1]
2. [理論への貢献2]
3. [理論への貢献3]

### 7.3 実務的含意
**Practical Implications**

1. [経営者への示唆]
2. [政策立案者への示唆]
3. [ステークホルダーへの示唆]

### 7.4 限界と今後の研究
**Limitations and Future Research**

- **限界1**: [例: 因果関係の特定の困難さ]
- **限界2**: [例: サンプルの地域的限界]
- **限界3**: [例: 測定の限界]

- **今後の研究方向性**:
  1. [提案1]
  2. [提案2]
  3. [提案3]

---

## 8. タイムラインと進捗管理 / Timeline and Progress Management

### 8.1 研究フェーズとタイムライン

| フェーズ | タスク | 期間 | 完了予定日 | ステータス |
|---------|--------|------|------------|-----------|
| Phase 1 | 文献レビュー | 2週間 | [YYYY-MM-DD] | [ ] |
| Phase 2 | 仮説開発 | 1週間 | [YYYY-MM-DD] | [ ] |
| Phase 3 | データソース特定 | 1週間 | [YYYY-MM-DD] | [ ] |
| Phase 4 | パイロット収集 | 1週間 | [YYYY-MM-DD] | [ ] |
| Phase 5 | フルデータ収集 | 4-6週間 | [YYYY-MM-DD] | [ ] |
| Phase 6 | データクリーニング | 2-4週間 | [YYYY-MM-DD] | [ ] |
| Phase 7 | 記述統計 | 1週間 | [YYYY-MM-DD] | [ ] |
| Phase 8 | メイン分析 | 2週間 | [YYYY-MM-DD] | [ ] |
| Phase 9 | ロバストネスチェック | 1週間 | [YYYY-MM-DD] | [ ] |
| Phase 10 | 論文執筆 | 4-8週間 | [YYYY-MM-DD] | [ ] |
| Phase 11 | 内部レビュー | 2週間 | [YYYY-MM-DD] | [ ] |
| Phase 12 | 投稿 | 1週間 | [YYYY-MM-DD] | [ ] |

**総所要期間 / Total Duration**: [20-30週間 / 5-7ヶ月]

### 8.2 マイルストーン
**Key Milestones**

- [ ] **M1**: 研究提案書完成（[日付]）
- [ ] **M2**: データ収集完了（[日付]）
- [ ] **M3**: 初期分析結果（[日付]）
- [ ] **M4**: 論文初稿完成（[日付]）
- [ ] **M5**: 査読コメント対応完了（[日付]）
- [ ] **M6**: 最終版投稿（[日付]）

---

## 9. リソースと予算 / Resources and Budget

### 9.1 必要リソース
**Required Resources**

#### データベースアクセス
| データベース | アクセス方法 | コスト | 代替案 |
|--------------|--------------|--------|--------|
| WRDS (Compustat, CRSP) | 大学契約 | [無料/¥XXX] | [SEC EDGAR] |
| Orbis | 大学契約 | [無料/¥XXX] | [OpenCorporates] |
| USPTO PatentsView | API | 無料 | - |

#### 分析ソフトウェア
- [ ] Stata/SE (¥XX,XXX)
- [ ] Python (無料、pandas, statsmodels, scikit-learn)
- [ ] R (無料、plm, lme4, survival)

#### 計算リソース
- [ ] 個人PC（十分）
- [ ] 大学のサーバー（パネルデータが大規模な場合）

### 9.2 予算見積もり
**Budget Estimate**

| 項目 | 金額 | 備考 |
|------|------|------|
| データベース利用料 | [¥0 - ¥XXX,XXX] | [大学契約利用] |
| ソフトウェアライセンス | [¥0 - ¥XX,XXX] | [無料ツール優先] |
| 学会発表費 | [¥XX,XXX] | [国内学会1回] |
| 論文投稿料 | [¥XX,XXX] | [オープンアクセス費] |
| その他 | [¥XX,XXX] | [予備費] |
| **合計** | **[¥XXX,XXX]** | - |

---

## 10. ターゲットジャーナルと投稿戦略 / Target Journals and Submission Strategy

### 10.1 ターゲットジャーナル（優先順）

#### 第1候補
**ジャーナル名**: [Strategic Management Journal (SMJ)]
- **Impact Factor**: [~10.0]
- **Acceptance Rate**: [~8-10%]
- **Fit Rationale**: [本研究の理論的貢献がSMJの基準に合致]
- **Recent Similar Papers**: [著者, 年, タイトル]

#### 第2候補
**ジャーナル名**: [Academy of Management Journal (AMJ)]
- **Impact Factor**: [~8.0]
- **Acceptance Rate**: [~6-8%]
- **Fit Rationale**: [組織論的視点が強い場合]

#### 第3候補
**ジャーナル名**: [Journal of International Business Studies (JIBS)]
- **Impact Factor**: [~6.0]
- **Acceptance Rate**: [~10-12%]
- **Fit Rationale**: [国際戦略研究の場合]

### 10.2 投稿前チェックリスト
**Pre-Submission Checklist**

- [ ] 理論的貢献が明確
- [ ] 実証分析が頑健
- [ ] サンプルサイズが十分
- [ ] 内生性への対処
- [ ] ロバストネスチェック完了
- [ ] 文献レビューが包括的
- [ ] 図表が高品質
- [ ] 英文校閲完了
- [ ] 共著者の承認取得
- [ ] カバーレター作成
- [ ] 利益相反の開示

---

## 11. 品質保証とコンプライアンス / Quality Assurance and Compliance

### 11.1 倫理審査
**Ethical Review**

- **IRB承認**: 
  - [ ] 必要
  - [ ] 不要（公開データのみ使用）
- **承認取得日**: [YYYY-MM-DD]
- **承認番号**: [IRB-XXXX-XXXX]

### 11.2 データ利用規約の遵守
**Data Terms of Service Compliance**

| データソース | 利用規約確認 | 学術利用可能 | 再配布制限 |
|--------------|--------------|--------------|------------|
| Compustat | ✓ | Yes | Yes |
| USPTO | ✓ | Yes | No |
| EDINET | ✓ | Yes | No |

### 11.3 再現性の確保
**Reproducibility**

- **データ保存**: [機関リポジトリ/Dataverse/OSF]
- **コード公開**: [GitHub/OSF]
- **ドキュメント**: [データ辞書、README]
- **バージョン管理**: [Git]

---

## 12. リスク管理 / Risk Management

### 12.1 予想されるリスクと対策

| リスク | 影響度 | 対策 |
|--------|--------|------|
| データアクセス不可 | 高 | 代替データソースの事前特定 |
| 欠損値が多い | 中 | サンプル基準の再考、代入法の適用 |
| 非有意な結果 | 中 | 理論の再検討、サンプル拡大 |
| 査読で却下 | 中 | 複数ジャーナルの準備、早期フィードバック |

### 12.2 コンティンジェンシープラン
**Contingency Plan**

- **Plan B**: [代替データソース、代替仮説]
- **Plan C**: [研究デザインの変更（横断研究→パネル研究）]

---

## 13. 参考文献 / References

### 13.1 理論文献
1. [理論の原典1]
2. [理論の原典2]
3. [理論の原典3]

### 13.2 方法論文献
1. [統計手法の参考文献1]
2. [統計手法の参考文献2]

### 13.3 実証研究
1. [類似研究1]
2. [類似研究2]
3. [類似研究3]

---

## 14. 付録 / Appendix

### A. 変数構築の詳細
[変数の計算式、データソース、処理方法の詳細]

### B. サンプル企業リスト
[パイロット段階での対象企業リスト]

### C. データ辞書の草案
[変数名、定義、データタイプ、ソースの一覧]

---

**このテンプレートの使い方 / How to Use This Template**:

1. [ ]にマークされた部分を埋める
2. 不要なセクションは削除
3. プロジェクト特有のセクションを追加
4. 定期的に更新（週次レビュー推奨）
5. アドバイザー・共同研究者と共有

**バージョン履歴 / Version History**:
- v1.0 (YYYY-MM-DD): 初版作成
- v1.1 (YYYY-MM-DD): [変更内容]

---

**承認 / Approval**:

- 主研究者 / Principal Investigator: [署名・日付]
- 指導教員 / Advisor: [署名・日付]
- 共同研究者 / Co-authors: [署名・日付]
