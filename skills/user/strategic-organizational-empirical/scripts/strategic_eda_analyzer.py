#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Strategic EDA Analyzer: Theory-Driven Exploratory Data Analysis

Philosophical/Theoretical Foundation:
    Exploratory Data Analysis (EDA), as conceived by Tukey (1977), is not mere
    descriptive statistics but a process of detective work - seeking patterns,
    anomalies, and theoretical insights in data. In strategy and organization
    research, EDA serves a dual purpose:
    
    1. Data Familiarization: Understanding distributions, relationships, and
       quality issues before confirmatory analysis
       
    2. Theory Development: Generating new theoretical insights through pattern
       recognition and anomaly detection (Eisenhardt, 1989)
    
    This analyzer transcends generic EDA by incorporating strategic and
    organizational theory into the exploratory process, asking theoretically
    informed questions of the data.

Theoretical Perspectives Integrated:
    - Resource heterogeneity (RBV): Distribution of resource endowments
    - Transaction characteristics (TCE): Patterns in governance choices
    - Institutional pressures (Institutional): Isomorphic tendencies
    - Capability evolution (Dynamic Capabilities): Temporal patterns

Usage:
    python strategic_eda_analyzer.py --data dataset.csv --config framework_config.yaml
    python strategic_eda_analyzer.py --data dataset.csv --theory rbv --output-dir ./eda_results/

Author: Strategic Research Lab
License: MIT
Version: 1.0.0
Date: 2025-11-08
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yaml
import json
import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field

# Statistical analysis
from scipy import stats
from scipy.stats import pearsonr, spearmanr, kendalltau
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


# Set style for academic quality plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


@dataclass
class EDAInsight:
    """Represents a single analytical insight"""
    category: str
    title: str
    description: str
    theoretical_interpretation: str
    evidence: Dict[str, Any] = field(default_factory=dict)
    visualization_path: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'category': self.category,
            'title': self.title,
            'description': self.description,
            'theoretical_interpretation': self.theoretical_interpretation,
            'evidence': self.evidence,
            'visualization': self.visualization_path
        }


@dataclass
class EDAReport:
    """Complete EDA report"""
    timestamp: str
    dataset_info: Dict[str, Any]
    theory_context: Optional[str]
    insights: List[EDAInsight] = field(default_factory=list)
    visualizations: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'timestamp': self.timestamp,
            'dataset_info': self.dataset_info,
            'theory_context': self.theory_context,
            'insights': [insight.to_dict() for insight in self.insights],
            'visualizations': self.visualizations
        }


class StrategicEDAAnalyzer:
    """
    Theory-Driven Exploratory Data Analysis System
    
    Implements exploratory analysis with strategic and organizational theory
    integration, generating both statistical summaries and theoretical insights.
    """
    
    # Theory-specific analytical focus
    THEORY_FOCUS = {
        'rbv': {
            'key_questions': [
                'Are resources heterogeneously distributed across firms?',
                'Do resource-advantaged firms show superior performance?',
                'Are valuable resources rare and difficult to imitate?',
                'What complementarities exist among resources?'
            ],
            'key_variables': ['resources', 'capabilities', 'performance', 'heterogeneity'],
            'analytical_emphasis': 'distribution_inequality'
        },
        'tce': {
            'key_questions': [
                'How do transaction characteristics relate to governance choices?',
                'Is there evidence of adaptation to transaction conditions?',
                'What patterns exist in vertical integration decisions?',
                'Are governance choices consistent with efficiency logic?'
            ],
            'key_variables': ['asset_specificity', 'uncertainty', 'governance', 'transaction_costs'],
            'analytical_emphasis': 'categorical_patterns'
        },
        'institutional': {
            'key_questions': [
                'Do organizations show evidence of isomorphic tendencies?',
                'How do institutional pressures vary across fields?',
                'What legitimacy-seeking behaviors are evident?',
                'Are there patterns of decoupling?'
            ],
            'key_variables': ['institutional_pressure', 'legitimacy', 'conformity', 'practices'],
            'analytical_emphasis': 'convergence_patterns'
        },
        'dynamic_capabilities': {
            'key_questions': [
                'How do capabilities evolve over time?',
                'What triggers capability development?',
                'Are there path dependencies in capability evolution?',
                'How do sensing, seizing, and transforming relate?'
            ],
            'key_variables': ['sensing', 'seizing', 'transforming', 'adaptability', 'time'],
            'analytical_emphasis': 'temporal_patterns'
        }
    }
    
    def __init__(self, data: pd.DataFrame, config: Optional[Dict[str, Any]] = None,
                 output_dir: str = './eda_results'):
        """
        Initialize EDA analyzer
        
        Args:
            data: DataFrame to analyze
            config: Optional theoretical framework configuration
            output_dir: Directory for output files
        """
        self.data = data.copy()
        self.config = config
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.theory_key = config['metadata']['theory_framework'] if config else None
        self.theory_focus = self.THEORY_FOCUS.get(self.theory_key, {})
        
        self.report = EDAReport(
            timestamp=datetime.now().isoformat(),
            dataset_info=self._get_dataset_info(),
            theory_context=self.theory_key
        )
    
    def _get_dataset_info(self) -> Dict[str, Any]:
        """Get basic dataset information"""
        return {
            'n_observations': len(self.data),
            'n_variables': len(self.data.columns),
            'variables': list(self.data.columns),
            'numeric_variables': list(self.data.select_dtypes(include=[np.number]).columns),
            'categorical_variables': list(self.data.select_dtypes(include=['object', 'category']).columns)
        }
    
    def _save_figure(self, fig, filename: str) -> str:
        """Save figure and return path"""
        filepath = self.output_dir / filename
        fig.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close(fig)
        self.report.visualizations.append(str(filepath))
        return str(filepath)
    
    def _add_insight(self, category: str, title: str, description: str,
                    theoretical_interpretation: str, evidence: Dict[str, Any] = None,
                    visualization_path: str = None):
        """Add insight to report"""
        insight = EDAInsight(
            category=category,
            title=title,
            description=description,
            theoretical_interpretation=theoretical_interpretation,
            evidence=evidence or {},
            visualization_path=visualization_path
        )
        self.report.insights.append(insight)
    
    # ========================================================================
    # UNIVARIATE ANALYSIS
    # ========================================================================
    
    def analyze_distributions(self) -> None:
        """
        Analyze variable distributions with theoretical interpretation
        
        Theoretical note: In RBV, resource distributions should show positive
        skew (few firms with superior resources). In institutional theory,
        distributions should show central tendency (isomorphism).
        """
        print("Analyzing variable distributions...")
        
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        for var in numeric_cols:
            data = self.data[var].dropna()
            
            if len(data) < 10:
                continue
            
            # Calculate distribution statistics
            mean_val = data.mean()
            median_val = data.median()
            std_val = data.std()
            skew_val = stats.skew(data)
            kurt_val = stats.kurtosis(data)
            
            # Create distribution plot
            fig, axes = plt.subplots(1, 2, figsize=(12, 4))
            
            # Histogram with KDE
            axes[0].hist(data, bins=30, density=True, alpha=0.7, edgecolor='black')
            data.plot(kind='kde', ax=axes[0], linewidth=2)
            axes[0].axvline(mean_val, color='r', linestyle='--', label=f'Mean: {mean_val:.2f}')
            axes[0].axvline(median_val, color='g', linestyle='--', label=f'Median: {median_val:.2f}')
            axes[0].set_title(f'Distribution of {var}')
            axes[0].set_xlabel(var)
            axes[0].set_ylabel('Density')
            axes[0].legend()
            
            # Q-Q plot for normality assessment
            stats.probplot(data, dist="norm", plot=axes[1])
            axes[1].set_title(f'Q-Q Plot: {var}')
            
            fig.tight_layout()
            viz_path = self._save_figure(fig, f'dist_{var}.png')
            
            # Theoretical interpretation based on distribution shape
            if abs(skew_val) > 1:
                if self.theory_key == 'rbv' and skew_val > 0:
                    interpretation = (
                        f"Positive skew (γ={skew_val:.2f}) suggests resource heterogeneity - "
                        f"few firms possess superior {var}, consistent with RBV's assumption "
                        f"of heterogeneous resource distributions (Barney, 1991)."
                    )
                elif self.theory_key == 'institutional' and abs(skew_val) < 0.5:
                    interpretation = (
                        f"Near-symmetric distribution suggests institutional isomorphism - "
                        f"organizations cluster around similar {var} values, reflecting "
                        f"mimetic or normative pressures (DiMaggio & Powell, 1983)."
                    )
                else:
                    interpretation = (
                        f"Skewed distribution (γ={skew_val:.2f}) indicates asymmetry in {var}. "
                        f"This may reflect competitive advantages or environmental constraints."
                    )
            else:
                interpretation = (
                    f"Relatively symmetric distribution (γ={skew_val:.2f}) suggests {var} "
                    f"is normally distributed across observations, possibly indicating "
                    f"standardized or widely available attributes."
                )
            
            self._add_insight(
                category="Distribution Analysis",
                title=f"Distribution of {var}",
                description=f"Mean={mean_val:.2f}, Median={median_val:.2f}, SD={std_val:.2f}, "
                           f"Skewness={skew_val:.2f}, Kurtosis={kurt_val:.2f}",
                theoretical_interpretation=interpretation,
                evidence={
                    'mean': float(mean_val),
                    'median': float(median_val),
                    'std': float(std_val),
                    'skewness': float(skew_val),
                    'kurtosis': float(kurt_val),
                    'n': int(len(data))
                },
                visualization_path=viz_path
            )
    
    def analyze_heterogeneity(self) -> None:
        """
        Analyze resource/capability heterogeneity
        
        Critical for RBV: Resources must be heterogeneously distributed
        for competitive advantage to exist (Barney, 1991).
        """
        if self.theory_key != 'rbv':
            return
        
        print("Analyzing resource heterogeneity...")
        
        # Identify resource/capability variables
        if self.config:
            resource_vars = [c['name'] for c in self.config.get('constructs', [])
                           if 'resource' in c.get('name', '').lower() or
                              'capability' in c.get('name', '').lower()]
        else:
            resource_vars = [col for col in self.data.columns 
                           if any(term in col.lower() for term in ['resource', 'capability', 'asset'])]
        
        if not resource_vars:
            return
        
        for var in resource_vars:
            if var not in self.data.columns or not np.issubdtype(self.data[var].dtype, np.number):
                continue
            
            data = self.data[var].dropna()
            
            # Calculate heterogeneity measures
            cv = data.std() / data.mean() if data.mean() != 0 else 0  # Coefficient of variation
            gini = self._calculate_gini(data)
            
            # Quartile analysis
            q1, q2, q3 = data.quantile([0.25, 0.5, 0.75])
            top_10_mean = data.nlargest(int(len(data) * 0.1)).mean()
            overall_mean = data.mean()
            advantage_ratio = top_10_mean / overall_mean if overall_mean != 0 else 0
            
            # Visualization
            fig, axes = plt.subplots(1, 2, figsize=(12, 5))
            
            # Box plot with individual points
            axes[0].boxplot([data], labels=[var])
            axes[0].scatter(np.ones(min(len(data), 100)) + np.random.normal(0, 0.02, min(len(data), 100)),
                          data.sample(min(len(data), 100)), alpha=0.3)
            axes[0].set_title(f'Distribution of {var}')
            axes[0].set_ylabel('Value')
            
            # Lorenz curve for inequality
            sorted_data = np.sort(data)
            cumsum = np.cumsum(sorted_data)
            lorenz = cumsum / cumsum[-1]
            axes[1].plot(np.linspace(0, 1, len(lorenz)), lorenz, label='Lorenz Curve')
            axes[1].plot([0, 1], [0, 1], 'r--', label='Perfect Equality')
            axes[1].fill_between(np.linspace(0, 1, len(lorenz)), lorenz, np.linspace(0, 1, len(lorenz)), alpha=0.3)
            axes[1].set_title(f'Resource Inequality: {var}')
            axes[1].set_xlabel('Cumulative % of Firms')
            axes[1].set_ylabel('Cumulative % of Resource')
            axes[1].legend()
            axes[1].text(0.5, 0.3, f'Gini: {gini:.3f}', transform=axes[1].transAxes, fontsize=12)
            
            fig.tight_layout()
            viz_path = self._save_figure(fig, f'heterogeneity_{var}.png')
            
            # Theoretical interpretation
            if gini > 0.4:
                interpretation = (
                    f"High inequality (Gini={gini:.3f}) in {var} distribution supports RBV's "
                    f"heterogeneity assumption. Top 10% firms possess {advantage_ratio:.2f}x "
                    f"the average firm's {var}, suggesting potential for sustained competitive "
                    f"advantage (Barney, 1991; Peteraf, 1993)."
                )
            elif gini < 0.2:
                interpretation = (
                    f"Low inequality (Gini={gini:.3f}) suggests {var} is relatively homogeneous. "
                    f"This challenges RBV assumptions and may indicate this resource is widely "
                    f"available or easily imitable, limiting its strategic value."
                )
            else:
                interpretation = (
                    f"Moderate inequality (Gini={gini:.3f}) in {var} suggests partial heterogeneity. "
                    f"Some firms may derive advantage, but not to the extent predicted by "
                    f"strong-form RBV."
                )
            
            self._add_insight(
                category="Resource Heterogeneity (RBV)",
                title=f"Heterogeneity Analysis: {var}",
                description=f"CV={cv:.3f}, Gini={gini:.3f}, Top 10% advantage ratio={advantage_ratio:.2f}",
                theoretical_interpretation=interpretation,
                evidence={
                    'coefficient_of_variation': float(cv),
                    'gini_coefficient': float(gini),
                    'advantage_ratio': float(advantage_ratio),
                    'q1': float(q1), 'q2': float(q2), 'q3': float(q3)
                },
                visualization_path=viz_path
            )
    
    def _calculate_gini(self, data: pd.Series) -> float:
        """Calculate Gini coefficient"""
        sorted_data = np.sort(data)
        n = len(data)
        index = np.arange(1, n + 1)
        return (2 * np.sum(index * sorted_data)) / (n * np.sum(sorted_data)) - (n + 1) / n
    
    # ========================================================================
    # BIVARIATE ANALYSIS
    # ========================================================================
    
    def analyze_correlations(self) -> None:
        """
        Analyze correlations between variables with theoretical interpretation
        
        Theoretical note: Expected correlations vary by theory:
        - RBV: Resources → Performance (positive)
        - TCE: Asset specificity → Integration (positive)
        - Institutional: Pressure → Conformity (positive)
        """
        print("Analyzing correlations...")
        
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            return
        
        # Calculate correlation matrix
        corr_matrix = self.data[numeric_cols].corr()
        
        # Create correlation heatmap
        fig, ax = plt.subplots(figsize=(12, 10))
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r',
                   center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
        ax.set_title('Correlation Matrix', fontsize=14, fontweight='bold')
        fig.tight_layout()
        viz_path = self._save_figure(fig, 'correlation_matrix.png')
        
        # Identify strong correlations
        strong_corrs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if abs(corr_val) > 0.3:  # Threshold for "notable" correlation
                    strong_corrs.append({
                        'var1': corr_matrix.columns[i],
                        'var2': corr_matrix.columns[j],
                        'correlation': corr_val
                    })
        
        # Sort by absolute correlation
        strong_corrs.sort(key=lambda x: abs(x['correlation']), reverse=True)
        
        # Generate theoretical interpretation
        if self.theory_key and self.config:
            iv_vars = [c['name'] for c in self.config.get('constructs', []) 
                      if c.get('role') == 'independent']
            dv_vars = [c['name'] for c in self.config.get('constructs', []) 
                      if c.get('role') == 'dependent']
            
            # Check theoretically expected correlations
            for iv in iv_vars:
                for dv in dv_vars:
                    if iv in corr_matrix.columns and dv in corr_matrix.columns:
                        corr_val = corr_matrix.loc[iv, dv]
                        
                        if self.theory_key == 'rbv':
                            interpretation = (
                                f"RBV predicts positive relationship between {iv} and {dv}. "
                                f"Observed r={corr_val:.3f}. "
                                f"{'Consistent with theory.' if corr_val > 0.2 else 'Weaker than expected - may indicate measurement issues or moderating factors.'}"
                            )
                        elif self.theory_key == 'tce':
                            interpretation = (
                                f"TCE predicts relationship between {iv} and {dv}. "
                                f"Observed r={corr_val:.3f}. "
                                f"{'Supports transaction cost logic.' if abs(corr_val) > 0.2 else 'Weak relationship may suggest additional governance mechanisms at play.'}"
                            )
                        else:
                            interpretation = (
                                f"Observed correlation between {iv} and {dv}: r={corr_val:.3f}. "
                                f"{'Suggests meaningful relationship.' if abs(corr_val) > 0.3 else 'Weak correlation may indicate need for multivariate analysis.'}"
                            )
                        
                        self._add_insight(
                            category="Bivariate Correlations",
                            title=f"Correlation: {iv} - {dv}",
                            description=f"Pearson r = {corr_val:.3f}",
                            theoretical_interpretation=interpretation,
                            evidence={'correlation': float(corr_val), 'n': int(len(self.data[[iv, dv]].dropna()))}
                        )
        
        # General insight about correlation patterns
        avg_corr = np.abs(corr_matrix.values[np.triu_indices_from(corr_matrix.values, k=1)]).mean()
        interpretation = (
            f"Average absolute correlation: {avg_corr:.3f}. "
            f"{'High intercorrelations may indicate common method variance or overlapping constructs.' if avg_corr > 0.5 else ''}"
            f"{'Low intercorrelations suggest constructs are distinct.' if avg_corr < 0.2 else ''}"
        )
        
        self._add_insight(
            category="Bivariate Correlations",
            title="Overall Correlation Structure",
            description=f"Average |r| = {avg_corr:.3f}, {len(strong_corrs)} strong correlations (|r| > 0.3)",
            theoretical_interpretation=interpretation,
            evidence={'average_correlation': float(avg_corr), 'strong_correlations': strong_corrs},
            visualization_path=viz_path
        )
    
    def analyze_group_differences(self) -> None:
        """
        Analyze differences across categorical groups
        
        Theoretical note: In institutional theory, we expect convergence across
        groups (isomorphism). In RBV, we expect divergence based on resources.
        """
        print("Analyzing group differences...")
        
        categorical_cols = self.data.select_dtypes(include=['object', 'category']).columns
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        for cat_var in categorical_cols:
            groups = self.data[cat_var].value_counts()
            
            # Only analyze if 2-5 groups with reasonable sample sizes
            if not (2 <= len(groups) <= 5 and groups.min() >= 10):
                continue
            
            for num_var in numeric_cols:
                # Prepare data
                group_data = {group: self.data[self.data[cat_var] == group][num_var].dropna() 
                             for group in groups.index}
                
                if any(len(g) < 10 for g in group_data.values()):
                    continue
                
                # Statistical test
                if len(groups) == 2:
                    stat, p_value = stats.ttest_ind(*group_data.values())
                    test_name = "t-test"
                else:
                    stat, p_value = stats.f_oneway(*group_data.values())
                    test_name = "ANOVA"
                
                # Effect size (Cohen's d for 2 groups, eta-squared for >2)
                if len(groups) == 2:
                    g1, g2 = list(group_data.values())
                    pooled_std = np.sqrt(((len(g1)-1)*g1.std()**2 + (len(g2)-1)*g2.std()**2) / (len(g1)+len(g2)-2))
                    effect_size = abs(g1.mean() - g2.mean()) / pooled_std if pooled_std > 0 else 0
                    effect_label = "Cohen's d"
                else:
                    ss_between = sum(len(g) * (g.mean() - self.data[num_var].mean())**2 for g in group_data.values())
                    ss_total = sum((self.data[num_var] - self.data[num_var].mean())**2)
                    effect_size = ss_between / ss_total if ss_total > 0 else 0
                    effect_label = "η²"
                
                # Visualization
                fig, ax = plt.subplots(figsize=(10, 6))
                self.data.boxplot(column=num_var, by=cat_var, ax=ax)
                ax.set_title(f'{num_var} by {cat_var}')
                ax.set_xlabel(cat_var)
                ax.set_ylabel(num_var)
                plt.suptitle('')  # Remove default title
                fig.tight_layout()
                viz_path = self._save_figure(fig, f'group_diff_{cat_var}_{num_var}.png')
                
                # Theoretical interpretation
                if p_value < 0.05:
                    if self.theory_key == 'institutional':
                        interpretation = (
                            f"Significant differences in {num_var} across {cat_var} groups (p={p_value:.4f}, {effect_label}={effect_size:.3f}). "
                            f"This heterogeneity challenges institutional isomorphism theory - "
                            f"organizations in the same field show divergent {num_var}, suggesting "
                            f"limited mimetic or normative pressures (DiMaggio & Powell, 1983)."
                        )
                    elif self.theory_key == 'rbv':
                        interpretation = (
                            f"Significant differences in {num_var} across {cat_var} groups (p={p_value:.4f}, {effect_label}={effect_size:.3f}). "
                            f"This heterogeneity supports RBV's assumption of resource differences "
                            f"leading to performance variation (Barney, 1991)."
                        )
                    else:
                        interpretation = (
                            f"Significant differences detected (p={p_value:.4f}, {effect_label}={effect_size:.3f}). "
                            f"{'Large effect' if effect_size > 0.8 else 'Medium effect' if effect_size > 0.5 else 'Small effect'} "
                            f"suggests {cat_var} is meaningfully associated with {num_var}."
                        )
                else:
                    interpretation = (
                        f"No significant differences in {num_var} across {cat_var} groups (p={p_value:.4f}). "
                        f"{'This convergence supports institutional isomorphism.' if self.theory_key == 'institutional' else ''}"
                    )
                
                self._add_insight(
                    category="Group Differences",
                    title=f"{num_var} by {cat_var}",
                    description=f"{test_name}: statistic={stat:.3f}, p={p_value:.4f}, {effect_label}={effect_size:.3f}",
                    theoretical_interpretation=interpretation,
                    evidence={
                        'test': test_name,
                        'statistic': float(stat),
                        'p_value': float(p_value),
                        'effect_size': float(effect_size),
                        'effect_measure': effect_label,
                        'group_means': {group: float(data.mean()) for group, data in group_data.items()}
                    },
                    visualization_path=viz_path
                )
    
    # ========================================================================
    # MULTIVARIATE ANALYSIS
    # ========================================================================
    
    def analyze_dimensionality(self) -> None:
        """
        Exploratory dimensionality reduction using PCA
        
        Useful for understanding latent structure in data and identifying
        potential composite variables or measurement issues.
        """
        print("Analyzing data dimensionality...")
        
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 3:
            return
        
        # Prepare data
        data_clean = self.data[numeric_cols].dropna()
        
        if len(data_clean) < 50:
            return
        
        # Standardize
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data_clean)
        
        # PCA
        pca = PCA()
        pca.fit(data_scaled)
        
        # Determine number of components (Kaiser criterion: eigenvalue > 1)
        n_components = sum(pca.explained_variance_ > 1)
        
        # Visualization
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Scree plot
        axes[0].plot(range(1, len(pca.explained_variance_ratio_)+1), 
                    pca.explained_variance_ratio_, 'bo-')
        axes[0].axhline(y=1/len(numeric_cols), color='r', linestyle='--', 
                       label='Average eigenvalue')
        axes[0].set_xlabel('Principal Component')
        axes[0].set_ylabel('Proportion of Variance Explained')
        axes[0].set_title('Scree Plot')
        axes[0].legend()
        axes[0].grid(True)
        
        # Cumulative variance
        cumsum = np.cumsum(pca.explained_variance_ratio_)
        axes[1].plot(range(1, len(cumsum)+1), cumsum, 'ro-')
        axes[1].axhline(y=0.8, color='g', linestyle='--', label='80% threshold')
        axes[1].set_xlabel('Number of Components')
        axes[1].set_ylabel('Cumulative Variance Explained')
        axes[1].set_title('Cumulative Variance Explained')
        axes[1].legend()
        axes[1].grid(True)
        
        fig.tight_layout()
        viz_path = self._save_figure(fig, 'pca_analysis.png')
        
        # Theoretical interpretation
        variance_by_first_pc = pca.explained_variance_ratio_[0]
        
        if variance_by_first_pc > 0.5:
            interpretation = (
                f"First principal component explains {variance_by_first_pc*100:.1f}% of variance. "
                f"High first-factor loading may indicate common method variance or a dominant "
                f"latent construct underlying measurements (Podsakoff et al., 2003)."
            )
        else:
            interpretation = (
                f"First principal component explains {variance_by_first_pc*100:.1f}% of variance. "
                f"{n_components} components have eigenvalues > 1 (Kaiser criterion), suggesting "
                f"multidimensional structure. This may indicate distinct theoretical constructs "
                f"or need for multi-item measurement models."
            )
        
        self._add_insight(
            category="Dimensionality Analysis",
            title="Principal Component Analysis",
            description=f"First PC: {variance_by_first_pc*100:.1f}% variance, "
                       f"{n_components} components with eigenvalue > 1",
            theoretical_interpretation=interpretation,
            evidence={
                'n_components_eigenvalue_gt_1': int(n_components),
                'variance_explained_first_pc': float(variance_by_first_pc),
                'cumulative_variance_3_pcs': float(cumsum[2]) if len(cumsum) > 2 else None,
                'eigenvalues': pca.explained_variance_.tolist()[:5]
            },
            visualization_path=viz_path
        )
    
    # ========================================================================
    # REPORT GENERATION
    # ========================================================================
    
    def run_complete_eda(self) -> EDAReport:
        """
        Run complete exploratory data analysis
        
        Returns:
            Complete EDA report
        """
        print("\n" + "="*80)
        print("STRATEGIC EDA: Theory-Driven Exploratory Data Analysis")
        print("="*80)
        print(f"\nDataset: {len(self.data)} observations × {len(self.data.columns)} variables")
        if self.theory_key:
            print(f"Theoretical framework: {self.theory_key.upper()}")
            print(f"Key questions: {len(self.theory_focus.get('key_questions', []))}")
        print()
        
        # Run analyses
        self.analyze_distributions()
        self.analyze_heterogeneity()
        self.analyze_correlations()
        self.analyze_group_differences()
        self.analyze_dimensionality()
        
        print(f"\n✓ Analysis complete: {len(self.report.insights)} insights generated")
        print(f"✓ Visualizations created: {len(self.report.visualizations)}")
        
        return self.report
    
    def save_report(self, output_path: str = 'eda_report.json') -> None:
        """Save EDA report to JSON"""
        report_path = self.output_dir / output_path
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.report.to_dict(), f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Report saved to: {report_path.absolute()}")
    
    def generate_markdown_report(self, output_path: str = 'eda_report.md') -> None:
        """Generate human-readable markdown report"""
        report_path = self.output_dir / output_path
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Strategic Exploratory Data Analysis Report\n\n")
            f.write(f"**Generated**: {self.report.timestamp}\n\n")
            
            f.write("## Dataset Information\n\n")
            f.write(f"- **Observations**: {self.report.dataset_info['n_observations']}\n")
            f.write(f"- **Variables**: {self.report.dataset_info['n_variables']}\n")
            if self.theory_key:
                f.write(f"- **Theoretical Framework**: {self.theory_key.upper()}\n")
            f.write("\n")
            
            # Group insights by category
            categories = {}
            for insight in self.report.insights:
                if insight.category not in categories:
                    categories[insight.category] = []
                categories[insight.category].append(insight)
            
            # Write insights
            f.write("## Key Insights\n\n")
            for category, insights in categories.items():
                f.write(f"### {category}\n\n")
                for i, insight in enumerate(insights, 1):
                    f.write(f"#### {i}. {insight.title}\n\n")
                    f.write(f"**Description**: {insight.description}\n\n")
                    f.write(f"**Theoretical Interpretation**: {insight.theoretical_interpretation}\n\n")
                    if insight.visualization_path:
                        f.write(f"![{insight.title}]({Path(insight.visualization_path).name})\n\n")
                    f.write("---\n\n")
        
        print(f"✓ Markdown report saved to: {report_path.absolute()}")


def load_config(config_path: str) -> Optional[Dict[str, Any]]:
    """Load theoretical framework configuration"""
    if not config_path:
        return None
    
    config_file = Path(config_path)
    if not config_file.exists():
        print(f"Warning: Configuration file not found: {config_path}")
        return None
    
    with open(config_file, 'r', encoding='utf-8') as f:
        if config_file.suffix in ['.yaml', '.yml']:
            return yaml.safe_load(f)
        elif config_file.suffix == '.json':
            return json.load(f)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Strategic EDA: Theory-Driven Exploratory Data Analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Basic EDA
    python strategic_eda_analyzer.py --data dataset.csv
    
    # Theory-driven EDA with framework
    python strategic_eda_analyzer.py --data dataset.csv --config framework_config.yaml
    
    # Specify output directory
    python strategic_eda_analyzer.py --data dataset.csv --output-dir ./my_eda_results/

Theoretical Frameworks:
    RBV: Focus on resource heterogeneity and performance
    TCE: Focus on transaction characteristics and governance
    Institutional: Focus on isomorphism and conformity
    Dynamic Capabilities: Focus on capability evolution
        """
    )
    
    parser.add_argument('--data', type=str, required=True,
                       help='Path to dataset (CSV format)')
    parser.add_argument('--config', type=str,
                       help='Path to theoretical framework configuration (YAML/JSON)')
    parser.add_argument('--output-dir', type=str, default='./eda_results',
                       help='Output directory for results (default: ./eda_results)')
    
    args = parser.parse_args()
    
    try:
        # Load data
        print(f"Loading dataset: {args.data}")
        data = pd.read_csv(args.data)
        print(f"✓ Loaded: {len(data)} observations × {len(data.columns)} variables")
        
        # Load configuration
        config = load_config(args.config) if args.config else None
        
        # Create analyzer and run
        analyzer = StrategicEDAAnalyzer(data, config, output_dir=args.output_dir)
        report = analyzer.run_complete_eda()
        
        # Save reports
        analyzer.save_report()
        analyzer.generate_markdown_report()
        
        print("\n" + "="*80)
        print("✓ EDA complete!")
        print(f"  Results saved to: {analyzer.output_dir.absolute()}")
        print(f"  Insights generated: {len(report.insights)}")
        print(f"  Visualizations created: {len(report.visualizations)}")
        print("="*80 + "\n")
        
        sys.exit(0)
    
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
