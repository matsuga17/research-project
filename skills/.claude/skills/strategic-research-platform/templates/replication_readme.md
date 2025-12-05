# Replication Package / 再現パッケージ

## Study Title / 研究タイトル
[Full Title of Your Study / 研究の完全なタイトル]

**Authors / 著者**: [Author Names and Affiliations]  
**Publication / 掲載誌**: [Journal Name, Year, Volume(Issue), Pages]  
**DOI**: [https://doi.org/XX.XXXX/XXXXX]  
**Date / 作成日**: [YYYY-MM-DD]  
**Version / バージョン**: [v1.0]

---

## Overview / 概要

### Purpose / 目的
This replication package contains all materials necessary to reproduce the results reported in [Study Title]. The package includes data, code, documentation, and instructions for complete replication.

この再現パッケージは、[研究タイトル]で報告された結果を再現するために必要なすべての資料を含んでいます。データ、コード、ドキュメント、および完全な再現のための手順が含まれています。

### Contents / 内容
- Raw data files / 生データファイル
- Cleaned/processed data / クリーニング済みデータ
- Analysis scripts / 分析スクリプト
- Output tables and figures / 出力表と図
- Data dictionary / データ辞書
- This README / このREADME

---

## 1. System Requirements / システム要件

### Software / ソフトウェア
- **Statistical Software / 統計ソフトウェア**:
  - [ ] Stata [Version 17 or higher]
  - [ ] R [Version 4.0 or higher]
  - [ ] Python [Version 3.8 or higher]
  
### Required Packages / 必要なパッケージ

#### If using Python:
```bash
pip install pandas numpy scipy statsmodels matplotlib seaborn openpyxl
```

Required versions / 必要なバージョン:
- pandas >= 1.3.0
- numpy >= 1.21.0
- scipy >= 1.7.0
- statsmodels >= 0.13.0
- matplotlib >= 3.4.0
- seaborn >= 0.11.0

#### If using R:
```r
install.packages(c("plm", "lme4", "stargazer", "ggplot2", "dplyr", "tidyr"))
```

#### If using Stata:
```stata
* Required user-written commands
ssc install reghdfe
ssc install estout
ssc install winsor2
```

### Hardware / ハードウェア
- **RAM**: Minimum 8GB (16GB recommended for large datasets)
- **Storage**: Minimum 1GB free space
- **Processing time / 処理時間**: Approximately 2-4 hours for complete replication

---

## 2. Directory Structure / ディレクトリ構造

```
replication_package/
│
├── README.md                          # このファイル / This file
├── data/                              # データディレクトリ / Data directory
│   ├── raw/                           # 生データ / Raw data
│   │   ├── financial_data.csv
│   │   ├── governance_data.csv
│   │   └── patent_data.csv
│   ├── processed/                     # 処理済みデータ / Processed data
│   │   ├── merged_dataset.csv
│   │   └── analysis_dataset.csv
│   └── data_dictionary.xlsx           # データ辞書 / Data dictionary
│
├── code/                              # コードディレクトリ / Code directory
│   ├── 01_data_collection.py          # データ収集 / Data collection
│   ├── 02_data_cleaning.py            # データクリーニング / Data cleaning
│   ├── 03_variable_construction.py    # 変数構築 / Variable construction
│   ├── 04_descriptive_statistics.py   # 記述統計 / Descriptive stats
│   ├── 05_main_analysis.py            # メイン分析 / Main analysis
│   ├── 06_robustness_checks.py        # 頑健性チェック / Robustness
│   └── 07_figures_tables.py           # 図表作成 / Figures & tables
│
├── output/                            # 出力ディレクトリ / Output directory
│   ├── tables/                        # 表 / Tables
│   │   ├── table1_descriptive.tex
│   │   ├── table2_correlation.tex
│   │   ├── table3_main_results.tex
│   │   └── table4_robustness.tex
│   ├── figures/                       # 図 / Figures
│   │   ├── figure1_conceptual_model.png
│   │   ├── figure2_descriptive.png
│   │   └── figure3_interaction.png
│   └── logs/                          # ログファイル / Log files
│       ├── 01_data_collection.log
│       ├── 02_data_cleaning.log
│       └── 05_main_analysis.log
│
├── documentation/                     # ドキュメント / Documentation
│   ├── data_sources.md                # データソース詳細
│   ├── variable_definitions.md        # 変数定義
│   └── methodology_notes.md           # 方法論ノート
│
└── LICENSE.txt                        # ライセンス / License
```

---

## 3. Data Description / データの説明

### 3.1 Data Sources / データソース

| File Name | Source | Description | Coverage | Access |
|-----------|--------|-------------|----------|--------|
| financial_data.csv | Compustat North America | Firm-level financial data | 2000-2023 | WRDS (Paid) |
| governance_data.csv | ExecuComp, ISS | Board and executive data | 2000-2023 | WRDS (Paid) |
| patent_data.csv | USPTO PatentsView | Patent filing and citation data | 2000-2023 | Free (API) |
| industry_data.csv | Compustat Segments | Industry-level aggregates | 2000-2023 | WRDS (Paid) |

### 3.2 Data Access Restrictions / データアクセス制限

**Publicly Available Data / 公開データ**:
- patent_data.csv: Freely available from USPTO PatentsView (https://patentsview.org/)
- industry_data.csv (aggregated): Can be shared under WRDS terms

**Restricted Data / 制限付きデータ**:
- financial_data.csv: Requires WRDS subscription (academic or commercial)
- governance_data.csv: Requires WRDS subscription

**Data Request / データリクエスト**:
If you do not have access to WRDS, you can:
1. Request temporary access from WRDS (https://wrds-www.wharton.upenn.edu/)
2. Contact the authors for aggregated/summary statistics
3. Use alternative free data sources (see data_sources.md)

### 3.3 Sample Construction / サンプル構築

**Initial Sample / 初期サンプル**:
- All firms in Compustat North America (2000-2023)
- N = 450,000 firm-year observations

**Exclusions / 除外基準**:
1. Financial firms (SIC 6000-6999): -80,000 observations
2. Utilities (SIC 4900-4999): -15,000 observations
3. Missing financial data (total assets, sales): -120,000 observations
4. Missing governance data (board composition): -95,000 observations
5. Outliers (winsorized at 1%/99%): -5,000 observations

**Final Sample / 最終サンプル**:
- N = 135,000 firm-year observations
- Unique firms = 8,500
- Time period = 2000-2023 (24 years)
- Average observations per firm = 15.9 years

---

## 4. Variable Definitions / 変数定義

### Dependent Variables / 従属変数

**ROA (Return on Assets)**:
- Definition: Net Income / Total Assets
- Source: Compustat (NI / AT)
- Transformation: Winsorized at 1%/99%
- Missing: 2.3% (listwise deletion)

**Innovation Output**:
- Definition: Number of patents granted in year t
- Source: USPTO PatentsView
- Transformation: log(Patents + 1)
- Missing: 42.7% (assigned 0 for non-patenting firms)

### Independent Variables / 独立変数

**R&D Intensity**:
- Definition: R&D Expenditure / Sales Revenue
- Source: Compustat (XRD / SALE)
- Transformation: Winsorized at 1%/99%
- Missing: 45.2% (indicator method: missing dummy + impute 0)

**Board Diversity (%Female Directors)**:
- Definition: Number of female directors / Total board size
- Source: ExecuComp, ISS
- Transformation: None (already 0-1 ratio)
- Missing: 8.3% (listwise deletion)

### Moderator Variables / 調整変数

**Environmental Dynamism**:
- Definition: Standard deviation of industry sales growth (5-year rolling window)
- Source: Compustat (industry-level aggregation)
- Transformation: Standardized (mean = 0, SD = 1)
- Missing: 0.5%

### Control Variables / 統制変数

See data_dictionary.xlsx for complete list of control variables.

Key controls:
- Firm Size: log(Total Assets)
- Firm Age: Current Year - Founding Year
- Leverage: Total Debt / Total Assets
- Industry: 2-digit SIC code dummies
- Year: Year fixed effects

---

## 5. Replication Instructions / 再現手順

### Step 1: Data Preparation / データ準備

#### Option A: If you have WRDS access
```bash
# Navigate to code directory
cd code/

# Run data collection script
python 01_data_collection.py

# This script will:
# - Connect to WRDS API
# - Download Compustat, CRSP, ExecuComp data
# - Save raw data to data/raw/
```

#### Option B: If you do NOT have WRDS access
```bash
# Use the provided processed data
# Skip to Step 2
```

**Note**: If using Option B, you are using pre-processed data and can only replicate Steps 2-5.

### Step 2: Data Cleaning / データクリーニング
```bash
python 02_data_cleaning.py
```

This script performs:
- Removes financial and utility firms (SIC exclusions)
- Handles missing values (indicator method for R&D, listwise for others)
- Winsorizes continuous variables at 1%/99%
- Checks for duplicates
- Outputs: data/processed/cleaned_dataset.csv

**Expected output / 期待される出力**:
- Console message: "Cleaned dataset saved: 135,000 observations, 8,500 firms"
- Log file: output/logs/02_data_cleaning.log

### Step 3: Variable Construction / 変数構築
```bash
python 03_variable_construction.py
```

This script:
- Constructs dependent variables (ROA, log(Patents+1))
- Constructs independent variables (R&D Intensity, Board Diversity)
- Constructs moderators (Environmental Dynamism)
- Constructs controls (Firm Size, Firm Age, Leverage)
- Creates interaction terms (mean-centered)
- Outputs: data/processed/analysis_dataset.csv

**Expected output**:
- Console: "Analysis dataset ready: 135,000 observations, 45 variables"
- Log file: output/logs/03_variable_construction.log

### Step 4: Descriptive Statistics / 記述統計
```bash
python 04_descriptive_statistics.py
```

This script generates:
- Table 1: Summary statistics (mean, SD, min, max)
- Table 2: Correlation matrix
- Table 3: VIF (multicollinearity check)
- Outputs: output/tables/table1_descriptive.tex

**Expected output**:
- 3 LaTeX table files in output/tables/
- Summary stats match Table 1 in the paper

### Step 5: Main Analysis / メイン分析
```bash
python 05_main_analysis.py
```

This script runs:
- Model 1: Baseline (controls only)
- Model 2: Main effect (H1)
- Model 3: Moderation (H2)
- Model 4: Full model
- Uses panel regression with firm and year fixed effects
- Clusters standard errors at firm level
- Outputs: output/tables/table3_main_results.tex

**Expected results / 期待される結果**:
| Hypothesis | Predicted | Result | Significance |
|------------|-----------|--------|--------------|
| H1: R&D Intensity → ROA (+) | + | β = 0.145 | p < 0.01 |
| H2: Env. Dynamism moderates (+) | + | β = 0.082 | p < 0.05 |

If your results match within ±0.01 for coefficients, replication is successful.

### Step 6: Robustness Checks / 頑健性チェック
```bash
python 06_robustness_checks.py
```

This script runs:
- Alternative DV: ROE instead of ROA
- Alternative sample: Large firms only (top quartile)
- Alternative specification: Lagged IVs (t-1)
- Alternative estimation: GMM (dynamic panel)
- Outputs: output/tables/table4_robustness.tex

**Expected**: Results remain qualitatively similar across all specifications.

### Step 7: Figures and Tables / 図表作成
```bash
python 07_figures_tables.py
```

This script generates:
- Figure 1: Conceptual model (from data)
- Figure 2: Distribution of key variables
- Figure 3: Interaction plot (Environmental Dynamism × R&D Intensity)
- Outputs: output/figures/*.png

---

## 6. Computational Time / 計算時間

Expected run time on a standard laptop (Intel i7, 16GB RAM):

| Script | Time | Notes |
|--------|------|-------|
| 01_data_collection.py | 30-60 min | Depends on internet speed |
| 02_data_cleaning.py | 5-10 min | |
| 03_variable_construction.py | 5-10 min | |
| 04_descriptive_statistics.py | 2-5 min | |
| 05_main_analysis.py | 10-15 min | Panel regression with FE |
| 06_robustness_checks.py | 15-20 min | Multiple specifications |
| 07_figures_tables.py | 5-10 min | |
| **Total** | **72-130 min** | **~2 hours** |

---

## 7. Expected Output / 期待される出力

After running all scripts, you should have:

### Tables / 表
- `output/tables/table1_descriptive.tex`: Summary statistics
- `output/tables/table2_correlation.tex`: Correlation matrix
- `output/tables/table3_main_results.tex`: Main regression results
- `output/tables/table4_robustness.tex`: Robustness checks

### Figures / 図
- `output/figures/figure1_conceptual_model.png`: Conceptual framework
- `output/figures/figure2_descriptive.png`: Histogram of key variables
- `output/figures/figure3_interaction.png`: Moderation plot

### Logs / ログ
- All scripts generate log files in `output/logs/` documenting:
  - Execution time
  - Sample size at each step
  - Any warnings or errors
  - Summary statistics

---

## 8. Troubleshooting / トラブルシューティング

### Issue 1: WRDS Connection Error
**Error**: `Connection to WRDS failed`

**Solution**:
1. Verify WRDS credentials: `wrds_username` and `wrds_password`
2. Check institutional access: https://wrds-www.wharton.upenn.edu/
3. Use VPN if required by your institution
4. If still failing, use pre-processed data (Option B)

### Issue 2: Missing Package Error
**Error**: `ModuleNotFoundError: No module named 'pandas'`

**Solution**:
```bash
pip install pandas numpy scipy statsmodels matplotlib seaborn
```

### Issue 3: Results Don't Match Paper
**Possible causes**:
1. **Different software version**: Stata 17 vs. Python may have slight numerical differences (< 0.01)
2. **Random seed**: For bootstrap/simulation, set `random.seed(42)` or `set seed 42`
3. **Data version**: Compustat updates historical data; use the snapshot date provided in data_sources.md

**How to check**:
- Compare sample size: Should be exactly 135,000 observations
- Compare means in Table 1: Should match within 0.01
- Compare coefficients in Table 3: Should match within 0.01
- If differences > 0.05, contact authors

### Issue 4: Script Takes Too Long
**If scripts run >3 hours**:

**Solution**:
1. Use a subset for testing: Modify `N_sample = 10000` in scripts
2. Use parallel processing (if applicable)
3. Check disk I/O speed (slow external drives may cause delays)

---

## 9. Citation / 引用

If you use this replication package, please cite the original paper:

### APA Format:
```
[Author Names]. ([Year]). [Title]. [Journal Name], [Volume]([Issue]), [Pages]. https://doi.org/XX.XXXX/XXXXX
```

### BibTeX Format:
```bibtex
@article{AuthorYear,
  author = {[Author Names]},
  title = {[Title]},
  journal = {[Journal Name]},
  year = {[Year]},
  volume = {[Volume]},
  number = {[Issue]},
  pages = {[Pages]},
  doi = {XX.XXXX/XXXXX}
}
```

---

## 10. Data Availability Statement / データ利用可能性宣言

The data used in this study come from multiple sources with different access restrictions:

**Publicly Available / 公開データ**:
- USPTO patent data: Freely available at https://patentsview.org/
- Aggregated industry data: Available upon request from the authors

**Restricted Access / 制限付きアクセス**:
- Compustat financial data: Requires WRDS subscription (https://wrds-www.wharton.upenn.edu/)
- ExecuComp governance data: Requires WRDS subscription

Due to licensing restrictions, we cannot redistribute the raw Compustat and ExecuComp data. Researchers with WRDS access can download the data using the provided scripts. Researchers without access can contact the authors for:
1. Summary statistics
2. Aggregated data (if permissible under license)
3. Code to replicate using alternative free data sources

---

## 11. Code Availability / コードの利用可能性

All code in this replication package is released under the MIT License (see LICENSE.txt). You are free to:
- Use the code for research
- Modify and distribute the code
- Use the code for commercial purposes

**Attribution**: Please cite the original paper when using this code.

---

## 12. Updates and Versioning / 更新とバージョン管理

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | [YYYY-MM-DD] | Initial release with paper publication |
| v1.1 | [YYYY-MM-DD] | [Bug fix: corrected variable construction in script 03] |
| v1.2 | [YYYY-MM-DD] | [Added alternative data source instructions] |

**Latest version**: Always available at [GitHub/OSF/Dataverse URL]

---

## 13. Contact Information / 連絡先

For questions about the replication package, please contact:

**Principal Investigator / 主任研究者**:
- Name: [First Last]
- Email: [email@university.edu]
- Institution: [University Name]

**Corresponding Author / 責任著者**:
- Name: [First Last]
- Email: [email@university.edu]

**Repository Maintainer / リポジトリ管理者**:
- GitHub: https://github.com/[username]/[repo]
- OSF: https://osf.io/[project_id]/
- Dataverse: https://dataverse.harvard.edu/dataverse/[name]

---

## 14. Acknowledgments / 謝辞

This replication package was created following best practices from:
- American Economic Association Data and Code Availability Policy
- Journal of Finance Data Sharing Guidelines
- Strategic Management Journal Replication Standards
- FAIR Data Principles (Findable, Accessible, Interoperable, Reusable)

We thank [Funding Agency] for financial support (Grant #XXXXX).

---

## 15. License / ライセンス

### Code License / コードライセンス
MIT License - See LICENSE.txt for details

### Data License / データライセンス
- Patent data: Public domain (USPTO)
- Compustat/ExecuComp: Restricted (WRDS terms apply)

---

**Replication Certification / 再現認証**:

- [ ] All code runs without errors
- [ ] Results match paper within tolerance (±0.01 for coefficients)
- [ ] All tables and figures reproduced
- [ ] Computational time < 3 hours
- [ ] Documentation is clear and complete

**Certified by / 認証者**: [Name, Date]

---

**End of Replication README / 再現READMEの終わり**

Last updated / 最終更新: [YYYY-MM-DD]
