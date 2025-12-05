#!/usr/bin/env python3
"""
Cross-Country Comparison: Board Diversity and ESG Performance in East Asia
===========================================================================

Research Question:
How does board gender diversity affect corporate ESG performance across 
Japan, South Korea, and Taiwan?

Hypotheses:
H1: Board gender diversity is positively associated with ESG performance
H2: The relationship is stronger in countries with stronger governance institutions
H3: The effect varies by industry (stronger in consumer-facing industries)

Data Sources (All Free):
1. EDINET (Japan): Board composition from 有価証券報告書 (Annual Securities Reports)
2. DART (South Korea): Board data from 사업보고서 (Business Reports)
3. MOPS (Taiwan): Board data from 公開資訊觀測站
4. CDP: ESG performance data (research license - free)
5. World Bank WGI: Country-level governance indicators

Sample:
- Listed manufacturing firms in Japan, South Korea, Taiwan
- 2015-2023 (9 years)
- ~300 firms (100 per country) × 9 years = 2,700 firm-years

Methods:
- Panel regression with country fixed effects
- Clustered standard errors at firm level
- Country × Board diversity interaction

Expected Results:
- Positive main effect (β ≈ 0.10-0.20)
- Stronger in countries with higher WGI scores
- Heterogeneous effects across industries

Author: Strategic Management Research Hub
Version: 1.0
Date: 2025-10-31
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Statistical analysis
import statsmodels.api as sm
import statsmodels.formula.api as smf
from linearmodels import PanelOLS
from scipy.stats.mstats import winsorize

# Configuration
sns.set_style('whitegrid')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ============================================================================
# DATA COLLECTION FROM MULTIPLE COUNTRIES
# ============================================================================

class MultiCountryCollector:
    """
    Collect data from Japan, South Korea, and Taiwan.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def collect_all_countries(self) -> pd.DataFrame:
        """
        Collect board and financial data from all three countries.
        
        Returns:
            Combined DataFrame
        """
        self.logger.info("Collecting data from Japan, South Korea, and Taiwan...")
        
        # Collect from each country
        japan_df = self._collect_japan()
        korea_df = self._collect_korea()
        taiwan_df = self._collect_taiwan()
        
        # Combine
        df = pd.concat([japan_df, korea_df, taiwan_df], ignore_index=True)
        
        self.logger.info(f"Total: {len(df)} firm-year observations across {df['firm_id'].nunique()} firms")
        
        return df
    
    def _collect_japan(self) -> pd.DataFrame:
        """
        Collect data from EDINET (Japan).
        
        In practice, extract from 有価証券報告書 → 役員の状況 (Officers)
        """
        self.logger.info("  Collecting from Japan (EDINET)...")
        
        # Simulated Japanese firms
        firms = [
            "トヨタ自動車", "ソニー", "パナソニック", "日立製作所", "三菱電機",
            "キーエンス", "ファナック", "ダイキン", "オムロン", "村田製作所"
        ]
        
        data = []
        for firm_id, firm_name in enumerate(firms, 1):
            for year in range(2015, 2024):
                # Simulate board data
                np.random.seed(firm_id * 1000 + year)
                
                total_directors = np.random.randint(8, 15)
                female_directors = np.random.binomial(total_directors, 0.15)  # Japan: ~15% female
                independent_directors = np.random.binomial(total_directors, 0.35)
                
                data.append({
                    'country': 'Japan',
                    'firm_id': f'JP_{firm_id:03d}',
                    'firm_name': firm_name,
                    'year': year,
                    'total_directors': total_directors,
                    'female_directors': female_directors,
                    'independent_directors': independent_directors,
                    'total_assets': np.random.uniform(1e6, 1e7),
                    'sales': np.random.uniform(5e5, 8e6),
                    'employees': np.random.randint(5000, 100000),
                })
        
        self.logger.info(f"    Japan: {len(data)} observations")
        return pd.DataFrame(data)
    
    def _collect_korea(self) -> pd.DataFrame:
        """
        Collect data from DART (South Korea).
        
        In practice, extract from 사업보고서 → 임원 및 직원 등에 관한 사항
        """
        self.logger.info("  Collecting from South Korea (DART)...")
        
        # Simulated Korean firms (chaebol + large firms)
        firms = [
            "삼성전자", "SK하이닉스", "LG전자", "현대자동차", "기아",
            "포스코", "한화", "롯데", "두산", "한국전력"
        ]
        
        data = []
        for firm_id, firm_name in enumerate(firms, 101):
            for year in range(2015, 2024):
                np.random.seed(firm_id * 1000 + year)
                
                total_directors = np.random.randint(9, 16)
                female_directors = np.random.binomial(total_directors, 0.10)  # Korea: ~10% female
                independent_directors = np.random.binomial(total_directors, 0.40)
                
                data.append({
                    'country': 'South Korea',
                    'firm_id': f'KR_{firm_id:03d}',
                    'firm_name': firm_name,
                    'year': year,
                    'total_directors': total_directors,
                    'female_directors': female_directors,
                    'independent_directors': independent_directors,
                    'total_assets': np.random.uniform(8e5, 1e7),
                    'sales': np.random.uniform(4e5, 9e6),
                    'employees': np.random.randint(3000, 120000),
                })
        
        self.logger.info(f"    South Korea: {len(data)} observations")
        return pd.DataFrame(data)
    
    def _collect_taiwan(self) -> pd.DataFrame:
        """
        Collect data from MOPS (Taiwan).
        
        In practice, extract from 公開資訊觀測站 → 董監事資料
        """
        self.logger.info("  Collecting from Taiwan (MOPS)...")
        
        # Simulated Taiwanese firms
        firms = [
            "台積電", "鴻海", "聯發科", "廣達", "和碩",
            "華碩", "台達電", "日月光", "南亞科", "群創"
        ]
        
        data = []
        for firm_id, firm_name in enumerate(firms, 201):
            for year in range(2015, 2024):
                np.random.seed(firm_id * 1000 + year)
                
                total_directors = np.random.randint(7, 13)
                female_directors = np.random.binomial(total_directors, 0.12)  # Taiwan: ~12% female
                independent_directors = np.random.binomial(total_directors, 0.38)
                
                data.append({
                    'country': 'Taiwan',
                    'firm_id': f'TW_{firm_id:03d}',
                    'firm_name': firm_name,
                    'year': year,
                    'total_directors': total_directors,
                    'female_directors': female_directors,
                    'independent_directors': independent_directors,
                    'total_assets': np.random.uniform(5e5, 8e6),
                    'sales': np.random.uniform(3e5, 7e6),
                    'employees': np.random.randint(2000, 80000),
                })
        
        self.logger.info(f"    Taiwan: {len(data)} observations")
        return pd.DataFrame(data)


class ESGCollector:
    """
    Collect ESG data from CDP (free research license).
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def collect_esg_scores(self, firm_list: pd.DataFrame) -> pd.DataFrame:
        """
        Collect ESG scores from CDP.
        
        In practice: Apply for academic research license, download data
        """
        self.logger.info("Collecting ESG scores from CDP...")
        
        esg_data = []
        
        for _, firm in firm_list.iterrows():
            for year in range(2015, 2024):
                # Simulate ESG score (0-100, higher is better)
                np.random.seed(hash(firm['firm_id'] + str(year)) % 2**32)
                
                # Base score varies by country (institutional quality)
                if firm['country'] == 'Japan':
                    base_score = 60
                elif firm['country'] == 'South Korea':
                    base_score = 55
                else:  # Taiwan
                    base_score = 58
                
                esg_score = base_score + np.random.uniform(-15, 20)
                
                esg_data.append({
                    'firm_id': firm['firm_id'],
                    'year': year,
                    'esg_score': esg_score,
                    'carbon_emissions': np.random.uniform(1000, 50000),  # tons CO2
                    'water_usage': np.random.uniform(100, 5000),  # m³
                })
        
        df = pd.DataFrame(esg_data)
        self.logger.info(f"Collected ESG data for {len(firm_list)} firms")
        
        return df


class WGICollector:
    """
    Collect World Governance Indicators from World Bank.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def collect_governance_indicators(self) -> pd.DataFrame:
        """
        Collect WGI for Japan, South Korea, Taiwan.
        
        Indicators:
        - Government Effectiveness
        - Regulatory Quality
        - Rule of Law
        - Control of Corruption
        """
        self.logger.info("Collecting World Governance Indicators...")
        
        # Simulated WGI scores (scale: -2.5 to +2.5, higher is better)
        wgi_data = []
        
        for year in range(2015, 2024):
            # Japan: High governance quality
            wgi_data.append({
                'country': 'Japan',
                'year': year,
                'govt_effectiveness': 1.5 + np.random.uniform(-0.1, 0.1),
                'regulatory_quality': 1.4 + np.random.uniform(-0.1, 0.1),
                'rule_of_law': 1.6 + np.random.uniform(-0.1, 0.1),
                'control_corruption': 1.7 + np.random.uniform(-0.1, 0.1),
            })
            
            # South Korea: Good but lower than Japan
            wgi_data.append({
                'country': 'South Korea',
                'year': year,
                'govt_effectiveness': 1.2 + np.random.uniform(-0.1, 0.1),
                'regulatory_quality': 1.1 + np.random.uniform(-0.1, 0.1),
                'rule_of_law': 1.3 + np.random.uniform(-0.1, 0.1),
                'control_corruption': 0.9 + np.random.uniform(-0.1, 0.1),
            })
            
            # Taiwan: Similar to South Korea
            wgi_data.append({
                'country': 'Taiwan',
                'year': year,
                'govt_effectiveness': 1.3 + np.random.uniform(-0.1, 0.1),
                'regulatory_quality': 1.2 + np.random.uniform(-0.1, 0.1),
                'rule_of_law': 1.4 + np.random.uniform(-0.1, 0.1),
                'control_corruption': 1.0 + np.random.uniform(-0.1, 0.1),
            })
        
        df = pd.DataFrame(wgi_data)
        self.logger.info("Collected WGI for 3 countries, 9 years")
        
        return df


# ============================================================================
# DATA PROCESSING
# ============================================================================

def process_and_merge_data(board_df: pd.DataFrame, esg_df: pd.DataFrame, wgi_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge all datasets and create analytical variables.
    """
    logger.info("Processing and merging datasets...")
    
    # Merge board + ESG
    df = board_df.merge(esg_df, on=['firm_id', 'year'], how='left')
    
    # Merge with WGI
    df = df.merge(wgi_df, on=['country', 'year'], how='left')
    
    # Create variables
    df['female_director_ratio'] = df['female_directors'] / df['total_directors']
    df['independent_ratio'] = df['independent_directors'] / df['total_directors']
    df['log_assets'] = np.log(df['total_assets'])
    df['log_employees'] = np.log(df['employees'])
    
    # Create country dummies
    df = pd.get_dummies(df, columns=['country'], prefix='country', drop_first=False)
    
    # Create interaction terms
    df['female_ratio_x_japan'] = df['female_director_ratio'] * df['country_Japan']
    df['female_ratio_x_korea'] = df['female_director_ratio'] * df['country_South Korea']
    df['female_ratio_x_taiwan'] = df['female_director_ratio'] * df['country_Taiwan']
    
    # Interaction with governance quality
    df['female_ratio_x_rule_of_law'] = df['female_director_ratio'] * df['rule_of_law']
    
    # Winsorize
    df['esg_score'] = winsorize(df['esg_score'], limits=[0.01, 0.01])
    df['female_director_ratio'] = winsorize(df['female_director_ratio'], limits=[0.01, 0.01])
    
    logger.info(f"Final dataset: {len(df)} observations")
    
    return df


# ============================================================================
# ANALYSIS
# ============================================================================

def run_cross_country_analysis(df: pd.DataFrame, output_dir: Path):
    """
    Run cross-country panel regressions.
    """
    logger.info("Running cross-country regression analysis...")
    
    # Prepare panel data
    df_panel = df.set_index(['firm_id', 'year'])
    
    # Model 1: Pooled (Country FE only)
    formula1 = 'esg_score ~ female_director_ratio + independent_ratio + log_assets + country_Japan + country_South_Korea'
    model1 = smf.ols(formula1, data=df).fit(cov_type='HC1')
    
    # Model 2: Panel FE (Firm + Year FE)
    formula2 = 'esg_score ~ female_director_ratio + independent_ratio + log_assets'
    model2 = PanelOLS.from_formula(
        formula2,
        data=df_panel,
        entity_effects=True,
        time_effects=True
    ).fit(cov_type='clustered', cluster_entity=True)
    
    # Model 3: Country × Female ratio interaction
    formula3 = '''esg_score ~ female_director_ratio + female_ratio_x_japan + female_ratio_x_korea + 
                  independent_ratio + log_assets + country_Japan + country_South_Korea'''
    model3 = smf.ols(formula3, data=df).fit(cov_type='HC1')
    
    # Model 4: Governance moderation
    formula4 = '''esg_score ~ female_director_ratio + female_ratio_x_rule_of_law + rule_of_law +
                  independent_ratio + log_assets + country_Japan + country_South_Korea'''
    model4 = smf.ols(formula4, data=df).fit(cov_type='HC1')
    
    # Print results
    print("\n" + "="*100)
    print("TABLE: CROSS-COUNTRY REGRESSION RESULTS")
    print("="*100)
    
    models = [model1, model2, model3, model4]
    model_names = ['Pooled OLS', 'Panel FE', 'Country Interaction', 'Governance Mod.']
    
    results_table = create_results_table(models, model_names)
    print(results_table)
    
    # Save
    with open(output_dir / 'regression_results.txt', 'w', encoding='utf-8') as f:
        f.write(results_table)
    
    return models


def create_results_table(models: List, model_names: List[str]) -> str:
    """
    Create regression results table.
    """
    lines = []
    lines.append("=" * 120)
    lines.append(f"{'Variable':<40}" + "".join([f"{name:>20}" for name in model_names]))
    lines.append("-" * 120)
    
    var_labels = {
        'female_director_ratio': 'Female Director Ratio',
        'female_ratio_x_japan': 'Female Ratio × Japan',
        'female_ratio_x_korea': 'Female Ratio × Korea',
        'female_ratio_x_rule_of_law': 'Female Ratio × Rule of Law',
        'independent_ratio': 'Independent Director Ratio',
        'log_assets': 'Log(Assets)',
        'rule_of_law': 'Rule of Law',
        'country_Japan': 'Japan',
        'country_South_Korea': 'South Korea',
    }
    
    for var, label in var_labels.items():
        line = f"{label:<40}"
        
        for model in models:
            if hasattr(model, 'params') and var in model.params.index:
                coef = model.params[var]
                
                if hasattr(model, 'pvalues'):
                    pval = model.pvalues[var]
                else:
                    pval = 0.5
                
                stars = ''
                if pval < 0.001:
                    stars = '***'
                elif pval < 0.01:
                    stars = '**'
                elif pval < 0.05:
                    stars = '*'
                
                line += f"{coef:>16.3f}{stars:<4}"
            else:
                line += " " * 20
        
        lines.append(line)
        
        # Standard errors
        line_se = f"{'':<40}"
        for model in models:
            if hasattr(model, 'params') and var in model.params.index:
                if hasattr(model, 'bse'):
                    se = model.bse[var]
                elif hasattr(model, 'std_errors'):
                    se = model.std_errors[var]
                else:
                    se = 0
                line_se += f"{'(' + f'{se:.3f}' + ')':>20}"
            else:
                line_se += " " * 20
        lines.append(line_se)
    
    lines.append("-" * 120)
    
    # Model stats
    line_fe = f"{'Firm FE':<40}" + f"{'No':>20}" + f"{'Yes':>20}" + f"{'No':>20}" + f"{'No':>20}"
    lines.append(line_fe)
    
    line_ye = f"{'Year FE':<40}" + f"{'No':>20}" + f"{'Yes':>20}" + f"{'No':>20}" + f"{'No':>20}"
    lines.append(line_ye)
    
    line_n = f"{'N':<40}" + "".join([f"{int(model.nobs):>20}" for model in models])
    lines.append(line_n)
    
    line_r2 = f"{'R²':<40}" + "".join([f"{model.rsquared:>20.3f}" for model in models])
    lines.append(line_r2)
    
    lines.append("=" * 120)
    lines.append("*** p<0.001, ** p<0.01, * p<0.05")
    
    return "\n".join(lines)


def create_country_comparison_plots(df: pd.DataFrame, output_dir: Path):
    """
    Create visualizations comparing countries.
    """
    logger.info("Creating country comparison visualizations...")
    
    fig_dir = output_dir / 'figures'
    fig_dir.mkdir(exist_ok=True)
    
    # Figure 1: Female director ratio by country over time
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for country in ['Japan', 'South Korea', 'Taiwan']:
        if f'country_{country}' in df.columns:
            country_data = df[df[f'country_{country}'] == 1]
        else:
            # Handle original 'country' column
            country_data = df[df['country'] == country] if 'country' in df.columns else df
        
        yearly_avg = country_data.groupby('year')['female_director_ratio'].mean()
        ax.plot(yearly_avg.index, yearly_avg.values * 100, marker='o', label=country, linewidth=2)
    
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Female Director Ratio (%)', fontsize=12)
    ax.set_title('Figure 1. Temporal Trend in Board Gender Diversity (2015-2023)', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(fig_dir / 'figure1_female_ratio_trend.png', dpi=300)
    plt.close()
    
    logger.info("  Saved: figure1_female_ratio_trend.png")
    
    # Figure 2: ESG score distribution by country
    fig, ax = plt.subplots(figsize=(10, 6))
    
    countries_data = []
    for country in ['Japan', 'South Korea', 'Taiwan']:
        if f'country_{country}' in df.columns:
            country_data = df[df[f'country_{country}'] == 1]['esg_score']
        else:
            country_data = df[df['country'] == country]['esg_score'] if 'country' in df.columns else df['esg_score']
        countries_data.append(country_data)
    
    ax.boxplot(countries_data, labels=['Japan', 'South Korea', 'Taiwan'])
    ax.set_ylabel('ESG Score', fontsize=12)
    ax.set_title('Figure 2. ESG Performance Distribution by Country', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(fig_dir / 'figure2_esg_by_country.png', dpi=300)
    plt.close()
    
    logger.info("  Saved: figure2_esg_by_country.png")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """
    Execute complete cross-country study.
    """
    start_time = datetime.now()
    
    print("\n" + "="*100)
    print("CROSS-COUNTRY STUDY: BOARD DIVERSITY AND ESG IN EAST ASIA")
    print("Japan, South Korea, Taiwan (2015-2023)")
    print("="*100)
    print(f"Start time: {start_time}\n")
    
    output_dir = Path("output_asian_comparison")
    output_dir.mkdir(exist_ok=True)
    
    try:
        # Phase 1: Data Collection
        logger.info("="*80)
        logger.info("PHASE 1: DATA COLLECTION")
        logger.info("="*80)
        
        collector = MultiCountryCollector()
        board_df = collector.collect_all_countries()
        
        # Get unique firms for ESG collection
        firms_list = board_df[['firm_id', 'country']].drop_duplicates()
        
        esg_collector = ESGCollector()
        esg_df = esg_collector.collect_esg_scores(firms_list)
        
        wgi_collector = WGICollector()
        wgi_df = wgi_collector.collect_governance_indicators()
        
        # Phase 2: Data Processing
        logger.info("\n" + "="*80)
        logger.info("PHASE 2: DATA PROCESSING")
        logger.info("="*80)
        
        df = process_and_merge_data(board_df, esg_df, wgi_df)
        
        # Save
        df.to_csv(output_dir / 'data_final.csv', index=False, encoding='utf-8-sig')
        logger.info(f"Saved final dataset: {len(df)} observations")
        
        # Phase 3: Analysis
        logger.info("\n" + "="*80)
        logger.info("PHASE 3: REGRESSION ANALYSIS")
        logger.info("="*80)
        
        models = run_cross_country_analysis(df, output_dir)
        
        # Phase 4: Visualization
        logger.info("\n" + "="*80)
        logger.info("PHASE 4: VISUALIZATION")
        logger.info("="*80)
        
        create_country_comparison_plots(df, output_dir)
        
        # Success
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print("\n" + "="*100)
        print("CROSS-COUNTRY STUDY COMPLETED")
        print("="*100)
        print(f"Duration: {duration:.1f} seconds")
        print(f"Output: {output_dir.absolute()}")
        print("\n" + "="*100)
        
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise


if __name__ == '__main__':
    main()
