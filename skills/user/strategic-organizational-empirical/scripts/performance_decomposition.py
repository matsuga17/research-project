#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Performance Decomposition Analysis: パフォーマンスの多層的分解分析システム

Philosophical and Theoretical Foundation:
=========================================
企業パフォーマンスの分解は、Rumelt (1991), McGahan & Porter (1997)の
分散分解研究、そしてBarney & Hesterly (1996)の資源ベース分析という
理論的伝統に基づく。パフォーマンスは単一要因ではなく、産業効果、
企業効果、年次効果、そして残差の階層的構造として理解される。

Core Theoretical Questions:
---------------------------
1. **Variance Decomposition (分散分解)**
   - Industry Effects vs. Firm Effects vs. Year Effects
   - Rumelt (1991): 企業効果 > 産業効果
   - McGahan & Porter (1997): 産業効果の再評価

2. **Resource-Based Decomposition (資源ベース分解)**
   - Tangible vs. Intangible Resources
   - Human Capital vs. Social Capital vs. Organizational Capital
   - Barney (1991): VRIOフレームワーク

3. **Operational Decomposition (オペレーション分解)**
   - DuPont分析: ROA = Profit Margin × Asset Turnover
   - Porter's Value Chain: Primary vs. Support Activities

Analytical Capabilities:
========================
1. ANOVAベースの分散分解
2. 階層線形モデル（HLM）による多層分解
3. DuPont分析による財務分解
4. 相対的貢献度の定量化
5. 時系列的パフォーマンス変動の分析

Usage:
======
    python performance_decomposition.py \\
        --data performance_data.csv \\
        --method variance \\
        --output decomposition_results.json

Author: Strategic Management Research Lab
Version: 1.0.0
License: MIT
Date: 2025-11-08

References:
-----------
- Rumelt, R. P. (1991). How much does industry matter? SMJ, 12(3), 167-185.
- McGahan, A. M., & Porter, M. E. (1997). How much does industry matter, really?
  SMJ, 18(S1), 15-30.
- Barney, J. B. (1991). Firm resources and sustained competitive advantage.
  Journal of Management, 17(1), 99-120.
- Barney, J. B., & Hesterly, W. (1996). Organizational economics. In S. Clegg et al. (Eds.),
  Handbook of Organization Studies (pp. 115-147). Sage.
"""

import argparse
import yaml
import json
import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from sklearn.preprocessing import StandardScaler
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, field
import sys
import warnings

warnings.filterwarnings('ignore')

# ==============================================================================
# Performance Components Data Classes
# ==============================================================================

@dataclass
class PerformanceComponents:
    """パフォーマンス構成要素"""
    industry_effect: float = 0.0
    firm_effect: float = 0.0
    year_effect: float = 0.0
    interaction_effect: float = 0.0
    residual: float = 0.0
    
    def total_explained_variance(self) -> float:
        """説明される分散の合計"""
        return (self.industry_effect + self.firm_effect + 
                self.year_effect + self.interaction_effect)
    
    def relative_importance(self) -> Dict[str, float]:
        """相対的重要性の計算"""
        total = self.total_explained_variance()
        if total == 0:
            return {}
        
        return {
            'industry': self.industry_effect / total,
            'firm': self.firm_effect / total,
            'year': self.year_effect / total,
            'interaction': self.interaction_effect / total
        }

@dataclass
class DuPontComponents:
    """DuPont分析の構成要素"""
    profit_margin: float = 0.0  # 利益率
    asset_turnover: float = 0.0  # 資産回転率
    equity_multiplier: float = 1.0  # 財務レバレッジ
    
    def compute_roa(self) -> float:
        """ROAの計算"""
        return self.profit_margin * self.asset_turnover
    
    def compute_roe(self) -> float:
        """ROEの計算"""
        return self.profit_margin * self.asset_turnover * self.equity_multiplier
    
    def decompose_contribution(self, target_metric: str = 'ROA') -> Dict[str, float]:
        """各要素の貢献度分解"""
        if target_metric == 'ROA':
            total = self.compute_roa()
            return {
                'profit_margin': (self.profit_margin / total) if total != 0 else 0,
                'asset_turnover': (self.asset_turnover / total) if total != 0 else 0
            }
        elif target_metric == 'ROE':
            total = self.compute_roe()
            return {
                'profit_margin': (self.profit_margin / total) if total != 0 else 0,
                'asset_turnover': (self.asset_turnover / total) if total != 0 else 0,
                'equity_multiplier': (self.equity_multiplier / total) if total != 0 else 0
            }
        else:
            return {}

# ==============================================================================
# Core Analyzer Class
# ==============================================================================

class PerformanceDecompositionAnalyzer:
    """
    パフォーマンス分解分析の中核クラス
    
    Methodological Philosophy:
    -------------------------
    パフォーマンスの因果的理解には、多層的分解が不可欠である。
    単一の説明変数による回帰では、パフォーマンスの複雑な生成メカニズムを
    捉えきれない。本分析器は、ANOVAによる分散分解と回帰による要因分解を
    統合し、理論的に意味のある分解を提供する。
    """
    
    def __init__(self, method: str = 'variance', config_path: Optional[str] = None):
        """
        初期化
        
        Parameters:
        -----------
        method : str
            分解手法 ('variance', 'dupont', 'resource', 'all')
        config_path : str, optional
            設定ファイルパス
        """
        self.method = method.lower()
        self.config = self._load_config(config_path) if config_path else {}
        self.data: Optional[pd.DataFrame] = None
        self.results: Dict[str, Any] = {}
    
    def _load_config(self, config_path: str) -> Dict:
        """設定ファイルの読み込み"""
        path = Path(config_path)
        with open(path, 'r', encoding='utf-8') as f:
            if path.suffix in ['.yaml', '.yml']:
                return yaml.safe_load(f)
            else:
                return json.load(f)
    
    def load_performance_data(self, data_path: str, 
                             performance_var: str = 'performance') -> pd.DataFrame:
        """
        パフォーマンスデータの読み込み
        
        Expected columns:
        - firm_id, industry, year
        - performance (or custom name via performance_var)
        - For DuPont: profit_margin, asset_turnover, equity_multiplier
        - For Resource: tangible_resources, intangible_resources, etc.
        """
        self.data = pd.read_csv(data_path)
        self.performance_var = performance_var
        
        # Validate required columns
        required = ['firm_id', 'industry', 'year', performance_var]
        missing = [col for col in required if col not in self.data.columns]
        if missing and self.method == 'variance':
            raise ValueError(f"Missing required columns: {missing}")
        
        return self.data
    
    def perform_variance_decomposition(self) -> Dict[str, Any]:
        """
        分散分解分析（Rumelt, 1991; McGahan & Porter, 1997）
        
        Decomposes total variance in performance into:
        - Industry effects
        - Firm effects (within industry)
        - Year effects
        - Interaction effects
        - Residual
        
        Uses ANOVA framework with nested design.
        """
        if self.data is None:
            raise ValueError("Data not loaded. Call load_performance_data() first.")
        
        # Prepare data
        df = self.data.copy()
        
        # Convert to categorical
        df['industry'] = df['industry'].astype('category')
        df['firm_id'] = df['firm_id'].astype('category')
        df['year'] = df['year'].astype('category')
        
        # Fit nested ANOVA model
        # Model: Performance ~ Industry + Firm(Industry) + Year + Residual
        
        # Method 1: Sequential ANOVA
        # Fit models incrementally to calculate R² changes
        
        # Null model (grand mean)
        y = df[self.performance_var]
        grand_mean = y.mean()
        ss_total = np.sum((y - grand_mean) ** 2)
        
        # Industry model
        model_industry = smf.ols(f'{self.performance_var} ~ C(industry)', data=df).fit()
        ss_industry = model_industry.ess
        
        # Firm model (nested within industry)
        model_firm = smf.ols(f'{self.performance_var} ~ C(industry) + C(firm_id)', data=df).fit()
        ss_firm = model_firm.ess - ss_industry
        
        # Year model
        model_year = smf.ols(
            f'{self.performance_var} ~ C(industry) + C(firm_id) + C(year)', 
            data=df
        ).fit()
        ss_year = model_year.ess - (ss_industry + ss_firm)
        
        # Residual
        ss_residual = model_year.ssr
        
        # Convert to proportions
        components = PerformanceComponents(
            industry_effect=ss_industry / ss_total,
            firm_effect=ss_firm / ss_total,
            year_effect=ss_year / ss_total,
            interaction_effect=0.0,  # Can be computed with more complex models
            residual=ss_residual / ss_total
        )
        
        # Relative importance
        rel_importance = components.relative_importance()
        
        # Statistical tests
        anova_results = anova_lm(model_year, typ=2)
        
        result = {
            'total_variance': float(ss_total),
            'variance_components': {
                'industry_effect': float(components.industry_effect),
                'firm_effect': float(components.firm_effect),
                'year_effect': float(components.year_effect),
                'residual': float(components.residual)
            },
            'relative_importance': rel_importance,
            'r_squared': float(model_year.rsquared),
            'anova_table': anova_results.to_dict(),
            'interpretation': self._interpret_variance_decomposition(rel_importance)
        }
        
        self.results['variance_decomposition'] = result
        return result
    
    def _interpret_variance_decomposition(self, rel_importance: Dict[str, float]) -> str:
        """分散分解結果の理論的解釈"""
        interpretation = ""
        
        if rel_importance.get('firm', 0) > rel_importance.get('industry', 0):
            interpretation += ("企業効果が産業効果を上回る。これはRumelt (1991)の知見と整合し、"
                             "企業固有の資源・能力がパフォーマンスの主要決定要因であることを示唆する。"
                             "資源ベース理論の実証的支持。")
        else:
            interpretation += ("産業効果が企業効果を上回る。これはMcGahan & Porter (1997)の"
                             "再評価と整合し、産業構造がパフォーマンスに強い影響を持つことを示す。"
                             "産業組織論・ポジショニング理論の支持。")
        
        if rel_importance.get('year', 0) > 0.1:
            interpretation += ("\n\n年次効果が顕著であり、マクロ経済要因や時代的変化が"
                             "パフォーマンスに影響していることを示す。")
        
        return interpretation
    
    def perform_dupont_decomposition(self) -> Dict[str, Any]:
        """
        DuPont分析によるパフォーマンス分解
        
        Decomposes ROA/ROE into operational components:
        - ROA = Profit Margin × Asset Turnover
        - ROE = ROA × Equity Multiplier
        
        Identifies whether performance differences stem from profitability
        or efficiency.
        """
        if self.data is None:
            raise ValueError("Data not loaded. Call load_performance_data() first.")
        
        df = self.data.copy()
        
        # Validate DuPont columns
        required_cols = ['profit_margin', 'asset_turnover']
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise ValueError(f"Missing DuPont columns: {missing}")
        
        # Calculate DuPont components for each firm
        dupont_results = []
        
        for _, row in df.iterrows():
            components = DuPontComponents(
                profit_margin=row['profit_margin'],
                asset_turnover=row['asset_turnover'],
                equity_multiplier=row.get('equity_multiplier', 1.0)
            )
            
            roa_computed = components.compute_roa()
            roe_computed = components.compute_roe()
            
            dupont_results.append({
                'firm_id': row['firm_id'],
                'year': row.get('year', 'N/A'),
                'profit_margin': float(components.profit_margin),
                'asset_turnover': float(components.asset_turnover),
                'equity_multiplier': float(components.equity_multiplier),
                'roa_computed': float(roa_computed),
                'roe_computed': float(roe_computed)
            })
        
        # Aggregate analysis
        df_dupont = pd.DataFrame(dupont_results)
        
        # Compute average contributions
        avg_profit_margin = df_dupont['profit_margin'].mean()
        avg_asset_turnover = df_dupont['asset_turnover'].mean()
        avg_roa = df_dupont['roa_computed'].mean()
        
        # Identify primary driver
        pm_contribution = avg_profit_margin / avg_roa if avg_roa != 0 else 0
        at_contribution = avg_asset_turnover / avg_roa if avg_roa != 0 else 0
        
        result = {
            'average_components': {
                'profit_margin': float(avg_profit_margin),
                'asset_turnover': float(avg_asset_turnover),
                'roa': float(avg_roa)
            },
            'relative_contributions': {
                'profit_margin': float(pm_contribution),
                'asset_turnover': float(at_contribution)
            },
            'primary_driver': ('Profit Margin' if pm_contribution > at_contribution 
                             else 'Asset Turnover'),
            'firm_level_results': dupont_results,
            'interpretation': self._interpret_dupont_analysis(pm_contribution, at_contribution)
        }
        
        self.results['dupont_decomposition'] = result
        return result
    
    def _interpret_dupont_analysis(self, pm_contrib: float, at_contrib: float) -> str:
        """DuPont分析の解釈"""
        if pm_contrib > at_contrib:
            return ("パフォーマンスは主に利益率（Profit Margin）によって駆動される。"
                   "これは差別化戦略やプライシング・パワーの重要性を示唆する。")
        else:
            return ("パフォーマンスは主に資産回転率（Asset Turnover）によって駆動される。"
                   "これはオペレーショナル効率性やコストリーダーシップ戦略の重要性を示す。")
    
    def perform_resource_decomposition(self) -> Dict[str, Any]:
        """
        資源ベース分解（Barney, 1991）
        
        Decomposes performance into contributions from:
        - Tangible resources (physical, financial)
        - Intangible resources (brand, patents, knowledge)
        - Human capital
        - Organizational capabilities
        
        Uses regression-based decomposition.
        """
        if self.data is None:
            raise ValueError("Data not loaded. Call load_performance_data() first.")
        
        df = self.data.copy()
        
        # Identify resource variables
        resource_vars = []
        potential_vars = [
            'tangible_resources', 'intangible_resources',
            'human_capital', 'organizational_capital',
            'brand_value', 'rd_intensity', 'patent_count'
        ]
        
        for var in potential_vars:
            if var in df.columns:
                resource_vars.append(var)
        
        if not resource_vars:
            return {'error': 'No resource variables found in data'}
        
        # Regression model: Performance ~ Resources + Controls
        formula = f"{self.performance_var} ~ " + " + ".join(resource_vars)
        
        # Add controls if available
        controls = ['firm_size', 'firm_age', 'industry']
        for control in controls:
            if control in df.columns:
                if control == 'industry':
                    formula += " + C(industry)"
                else:
                    formula += f" + {control}"
        
        model = smf.ols(formula, data=df).fit()
        
        # Extract coefficients and standardized effects
        coeffs = model.params.to_dict()
        pvalues = model.pvalues.to_dict()
        
        # Standardize to compute relative importance
        X = df[resource_vars]
        y = df[self.performance_var]
        
        X_std = StandardScaler().fit_transform(X)
        y_std = StandardScaler().fit_transform(y.values.reshape(-1, 1)).flatten()
        
        model_std = sm.OLS(y_std, sm.add_constant(X_std)).fit()
        std_coeffs = dict(zip(resource_vars, model_std.params[1:]))
        
        # Relative importance (absolute standardized coefficients)
        total_effect = sum(abs(v) for v in std_coeffs.values())
        rel_importance = {k: abs(v) / total_effect for k, v in std_coeffs.items()}
        
        result = {
            'resource_variables': resource_vars,
            'coefficients': {k: float(v) for k, v in coeffs.items() if k in resource_vars},
            'p_values': {k: float(v) for k, v in pvalues.items() if k in resource_vars},
            'standardized_effects': {k: float(v) for k, v in std_coeffs.items()},
            'relative_importance': {k: float(v) for k, v in rel_importance.items()},
            'r_squared': float(model.rsquared),
            'interpretation': self._interpret_resource_decomposition(rel_importance)
        }
        
        self.results['resource_decomposition'] = result
        return result
    
    def _interpret_resource_decomposition(self, rel_importance: Dict[str, float]) -> str:
        """資源分解の解釈"""
        # Identify most important resource
        top_resource = max(rel_importance, key=rel_importance.get)
        top_value = rel_importance[top_resource]
        
        interpretation = f"最も重要な資源は{top_resource}である（相対重要度: {top_value:.2%}）。"
        
        # Check if intangible > tangible
        intangible_vars = [k for k in rel_importance.keys() 
                          if 'intangible' in k.lower() or 'brand' in k.lower() 
                          or 'patent' in k.lower()]
        tangible_vars = [k for k in rel_importance.keys() if 'tangible' in k.lower()]
        
        if intangible_vars and tangible_vars:
            intangible_sum = sum(rel_importance.get(k, 0) for k in intangible_vars)
            tangible_sum = sum(rel_importance.get(k, 0) for k in tangible_vars)
            
            if intangible_sum > tangible_sum:
                interpretation += ("\n\n無形資源が有形資源よりも重要であり、"
                                 "Barney (1991)のVRIOフレームワークと整合する。"
                                 "模倣困難な無形資産が持続的競争優位の源泉である。")
        
        return interpretation
    
    def perform_comprehensive_decomposition(self) -> Dict[str, Any]:
        """包括的分解分析"""
        comprehensive_results = {}
        
        # Run all applicable decompositions
        if self.method in ['variance', 'all']:
            try:
                comprehensive_results['variance'] = self.perform_variance_decomposition()
            except Exception as e:
                comprehensive_results['variance'] = {'error': str(e)}
        
        if self.method in ['dupont', 'all']:
            try:
                comprehensive_results['dupont'] = self.perform_dupont_decomposition()
            except Exception as e:
                comprehensive_results['dupont'] = {'error': str(e)}
        
        if self.method in ['resource', 'all']:
            try:
                comprehensive_results['resource'] = self.perform_resource_decomposition()
            except Exception as e:
                comprehensive_results['resource'] = {'error': str(e)}
        
        return comprehensive_results
    
    def generate_report(self) -> Dict[str, Any]:
        """包括的報告書の生成"""
        if not self.results:
            self.results = self.perform_comprehensive_decomposition()
        
        report = {
            'metadata': {
                'n_observations': len(self.data) if self.data is not None else 0,
                'method': self.method,
                'performance_variable': self.performance_var,
                'analysis_date': pd.Timestamp.now().isoformat()
            },
            'decomposition_results': self.results,
            'executive_summary': self._generate_executive_summary()
        }
        
        return report
    
    def _generate_executive_summary(self) -> str:
        """エグゼクティブ・サマリーの生成"""
        summary = "## パフォーマンス分解分析：エグゼクティブ・サマリー\n\n"
        
        if 'variance_decomposition' in self.results:
            var_decomp = self.results['variance_decomposition']
            if 'variance_components' in var_decomp:
                comps = var_decomp['variance_components']
                summary += "### 分散分解\n"
                summary += f"- 産業効果: {comps['industry_effect']:.1%}\n"
                summary += f"- 企業効果: {comps['firm_effect']:.1%}\n"
                summary += f"- 年次効果: {comps['year_effect']:.1%}\n\n"
                
                if 'interpretation' in var_decomp:
                    summary += var_decomp['interpretation'] + "\n\n"
        
        if 'dupont_decomposition' in self.results:
            dupont = self.results['dupont_decomposition']
            if 'primary_driver' in dupont:
                summary += f"### DuPont分析\n主要ドライバー: {dupont['primary_driver']}\n\n"
        
        return summary
    
    def save_results(self, output_path: str) -> None:
        """結果の保存"""
        report = self.generate_report()
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ Decomposition results saved to: {output_path}")

# ==============================================================================
# Command-Line Interface
# ==============================================================================

def main():
    """
    メインエントリポイント
    
    Example Usage:
    -------------
    python performance_decomposition.py \\
        --data performance_data.csv \\
        --method variance \\
        --performance roa \\
        --output results/decomposition.json
    """
    parser = argparse.ArgumentParser(
        description="Performance Decomposition Analysis: パフォーマンスの多層的分解分析",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--data', type=str, required=True,
                       help='Performance data file (CSV)')
    parser.add_argument('--method', type=str, default='all',
                       choices=['variance', 'dupont', 'resource', 'all'],
                       help='Decomposition method')
    parser.add_argument('--performance', type=str, default='performance',
                       help='Performance variable name')
    parser.add_argument('--output', type=str, required=True,
                       help='Output file path (JSON)')
    parser.add_argument('--config', type=str,
                       help='Configuration file (YAML/JSON)')
    
    args = parser.parse_args()
    
    try:
        # Initialize analyzer
        analyzer = PerformanceDecompositionAnalyzer(
            method=args.method,
            config_path=args.config
        )
        
        # Load data
        print(f"Loading performance data...")
        analyzer.load_performance_data(args.data, performance_var=args.performance)
        
        # Run decomposition
        print(f"\nPerforming {args.method} decomposition...")
        analyzer.perform_comprehensive_decomposition()
        
        # Save results
        analyzer.save_results(args.output)
        
        print("\n" + "="*70)
        print("Performance Decomposition Analysis Complete")
        print("="*70)
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
