# Strategic Research Suite - Shared Utilities

このディレクトリには、すべてのスキルで共通して使用されるユーティリティとリファレンスが含まれています。

## 📚 共通リソース

### 1. Theory Framework Reference
- Resource-Based View (RBV)
- Dynamic Capabilities Theory
- Competitive Strategy (Porter Framework)
- Institutional Theory
- Transaction Cost Economics (TCE)
- Organizational Learning Theory

### 2. Variable Definitions
すべてのスキルで使用される標準的な変数定義を提供します。

### 3. Data Quality Standards
- Benford's Law test基準
- 外れ値処理基準（1%/99% winsorization）
- 欠損値許容率
- サバイバルバイアス対策基準

### 4. Statistical Conventions
- 有意水準: α = 0.05
- 検出力: β ≥ 0.80
- クラスター化標準誤差: firm-level clustering必須
- 固定効果 vs. ランダム効果: Hausman testで決定

### 5. Coding Standards
- Python 3.9+
- PEP 8準拠
- Type hints使用推奨
- Docstring必須

## 🔧 ユーティリティ関数

各スキルで共通して使用される関数は、このディレクトリの各モジュールに実装されています：

- `common_utils.py`: 汎用ヘルパー関数
- `data_quality.py`: データ品質チェック関数
- `variable_construction.py`: 変数構築ヘルパー
- `network_utils.py`: ネットワーク分析共通関数
- `text_utils.py`: テキスト処理共通関数

## 📖 使用方法

各スキルから共通ユーティリティを参照する場合：

```python
# スキル内のスクリプトから
from strategic_research_suite._shared import common_utils
from strategic_research_suite._shared.data_quality import AdvancedQualityAssurance
```

## 🌐 Cross-Skill References

スキル間で相互参照する際の標準フォーマット：

```markdown
**関連スキル**: `2-data-sources` - 日本企業データの詳細

この分析には、以下の専門スキルと併用してください：
- データ収集: `2-data-sources` skill
- 統計分析: `3-statistical-methods` skill
```

## 📊 Standard Tables & Figures

### Table Numbering
- Table 1: Descriptive Statistics
- Table 2: Correlation Matrix
- Table 3: Main Regression Results
- Table 4+: Robustness Checks

### Figure Numbering
- Figure 1: Conceptual Model
- Figure 2: Interaction Effects Plot
- Figure 3+: Additional visualizations

## 🎯 Quality Checklist Template

すべての研究プロジェクトで使用する品質チェックリスト：

- [ ] サバイバルバイアス対策済み
- [ ] 統計的検出力分析実施
- [ ] 外れ値処理documented
- [ ] 変数定義明確
- [ ] データソース明記
- [ ] 再現パッケージ作成

---

**バージョン**: 4.0  
**最終更新**: 2025-11-01  
**メンテナー**: Strategic Research Suite Team
