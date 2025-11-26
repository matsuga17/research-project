"""
causal_forest.py

Causal Forest for Heterogeneous Treatment Effect Estimation

This module implements Causal Forest analysis for strategic management research,
enabling the estimation of heterogeneous treatment effects (CATE) - how the
impact of a strategic decision varies across different firm characteristics.

Key Features:
- Causal Forest estimation using EconML
- CATE (Conditional Average Treatment Effect) calculation
- Feature importance analysis
- Heterogeneity visualization
- Policy tree generation

Common Applications in Strategic Research:
- M&A effects varying by firm size, industry, or capabilities
- R&D investment returns differing by organizational structure
- Digital transformation impact across firm characteristics
- Alliance effectiveness conditional on partner attributes

Usage:
    from causal_forest import CausalForestAnalyzer
    
    # Initialize analyzer
    analyzer = CausalForestAnalyzer(
        df=panel_data,
        treatment='merger_dummy',
        outcome='roa',
        features=['firm_size', 'rd_intensity', 'leverage'],
        firm_id='firm_id',
        time_id='year'
    )
    
    # Estimate CATE
    cate_results = analyzer.estimate_cate()
    
    # Analyze heterogeneity
    heterogeneity = analyzer.analyze_heterogeneity()
    
    # Visualize results
    analyzer.plot_cate_distribution()
    analyzer.plot_feature_importance()

References:
- Athey, S., & Imbens, G. (2016). Recursive partitioning for heterogeneous 
  causal effects. PNAS, 113(27), 7353-7360.
- Wager, S., & Athey, S. (2018). Estimation and inference of heterogeneous 
  treatment effects using random forests. JASA, 113(523), 1228-1242.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple, Any
import logging
from pathlib import Path

# Causal ML libraries
try:
    from econml.dml import CausalForestDML
    from econml.policy import PolicyTree
    ECONML_AVAILABLE = True
except ImportError:
    ECONML_AVAILABLE = False
    logging.warning("EconML not available. Install with: pip install econml")

# Statistical libraries
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CausalForestAnalyzer:
    """
    Causal Forest analyzer for heterogeneous treatment effect estimation
    
    This class provides comprehensive Causal Forest analysis functionality,
    including CATE estimation, heterogeneity analysis, and visualization.
    
    Attributes:
        df: Input panel DataFrame
        treatment: Treatment variable name
        outcome: Outcome variable name
        features: List of feature column names for heterogeneity
        controls: Optional control variables
        firm_id: Firm identifier column
        time_id: Time identifier column
        model: Fitted Causal Forest model
        cate_: Estimated CATE for each observation
    """
    
    def __init__(self,
                 df: pd.DataFrame,
                 treatment: str,
                 outcome: str,
                 features: List[str],
                 controls: Optional[List[str]] = None,
                 firm_id: str = 'firm_id',
                 time_id: str = 'year'):
        """
        Initialize Causal Forest analyzer
        
        Args:
            df: Panel dataset
            treatment: Binary treatment variable (0/1)
            outcome: Continuous outcome variable
            features: Features for effect heterogeneity
            controls: Optional control variables
            firm_id: Firm identifier
            time_id: Time identifier
        """
        if not ECONML_AVAILABLE:
            raise ImportError(
                "EconML is required for Causal Forest. "
                "Install with: pip install econml"
            )
        
        self.df = df.copy()
        self.treatment = treatment
        self.outcome = outcome
        self.features = features
        self.controls = controls or []
        self.firm_id = firm_id
        self.time_id = time_id
        
        self.model = None
        self.cate_ = None
        self.feature_importance_ = None
        
        logger.info(f"Initialized CausalForestAnalyzer:")
        logger.info(f"  Treatment: {treatment}")
        logger.info(f"  Outcome: {outcome}")
        logger.info(f"  Features: {len(features)}")
        logger.info(f"  Controls: {len(self.controls)}")
        logger.info(f"  Observations: {len(df):,}")
    
    def preprocess_data(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray, Optional[np.ndarray]]:
        """
        Preprocess data for Causal Forest
        
        Returns:
            Tuple of (Y, T, X, W) where:
                Y: Outcome array
                T: Treatment array
                X: Features for heterogeneity
                W: Controls (None if no controls)
        """
        logger.info("Preprocessing data...")
        
        # Remove missing values
        cols = [self.outcome, self.treatment] + self.features + self.controls
        df_clean = self.df[cols].dropna()
        
        logger.info(f"  After removing missing: {len(df_clean):,} observations")
        
        # Extract arrays
        Y = df_clean[self.outcome].values
        T = df_clean[self.treatment].values
        X = df_clean[self.features].values
        W = df_clean[self.controls].values if self.controls else None
        
        # Validate treatment is binary
        unique_t = np.unique(T)
        if not np.array_equal(unique_t, [0, 1]) and not np.array_equal(unique_t, [0.0, 1.0]):
            logger.warning(f"Treatment values: {unique_t}")
            logger.warning("Treatment should be binary (0/1). Converting...")
            T = (T > 0).astype(int)
        
        logger.info(f"  Treatment prevalence: {T.mean():.1%}")
        logger.info(f"  Outcome range: [{Y.min():.3f}, {Y.max():.3f}]")
        
        return Y, T, X, W
    
    def estimate_cate(self,
                     n_estimators: int = 100,
                     max_depth: int = None,
                     min_samples_leaf: int = 10,
                     random_state: int = 42) -> pd.DataFrame:
        """
        Estimate Conditional Average Treatment Effect (CATE) using Causal Forest
        
        Args:
            n_estimators: Number of trees
            max_depth: Maximum tree depth
            min_samples_leaf: Minimum samples per leaf
            random_state: Random seed
        
        Returns:
            DataFrame with CATE estimates
        """
        logger.info("Estimating CATE using Causal Forest...")
        
        # Preprocess data
        Y, T, X, W = self.preprocess_data()
        
        # Initialize Causal Forest
        self.model = CausalForestDML(
            model_y=RandomForestRegressor(
                n_estimators=n_estimators,
                max_depth=max_depth,
                min_samples_leaf=min_samples_leaf,
                random_state=random_state
            ),
            model_t=RandomForestClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                min_samples_leaf=min_samples_leaf,
                random_state=random_state
            ),
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_leaf=min_samples_leaf,
            random_state=random_state,
            verbose=0
        )
        
        # Fit model
        logger.info("  Fitting Causal Forest...")
        self.model.fit(Y=Y, T=T, X=X, W=W)
        
        # Estimate CATE
        logger.info("  Estimating CATE...")
        self.cate_ = self.model.effect(X)
        
        # Get feature importance
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importance_ = pd.DataFrame({
                'feature': self.features,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)
        
        # Create results DataFrame
        cols = [self.outcome, self.treatment] + self.features + self.controls
        df_clean = self.df[cols].dropna()
        
        results = df_clean.copy()
        results['cate'] = self.cate_
        results['cate_lower'], results['cate_upper'] = self.model.effect_interval(X, alpha=0.05)
        
        logger.info(f"✓ CATE estimation completed")
        logger.info(f"  Mean CATE: {self.cate_.mean():.4f}")
        logger.info(f"  Std CATE: {self.cate_.std():.4f}")
        logger.info(f"  Range: [{self.cate_.min():.4f}, {self.cate_.max():.4f}]")
        
        return results
    
    def analyze_heterogeneity(self, quantiles: List[float] = [0.25, 0.5, 0.75]) -> Dict[str, Any]:
        """
        Analyze treatment effect heterogeneity
        
        Args:
            quantiles: Quantiles for analysis
        
        Returns:
            Dictionary with heterogeneity statistics
        """
        if self.cate_ is None:
            raise ValueError("Must run estimate_cate() first")
        
        logger.info("Analyzing treatment effect heterogeneity...")
        
        # Calculate statistics
        cate_stats = {
            'mean': float(np.mean(self.cate_)),
            'std': float(np.std(self.cate_)),
            'min': float(np.min(self.cate_)),
            'max': float(np.max(self.cate_)),
            'quantiles': {f'q{int(q*100)}': float(np.quantile(self.cate_, q)) 
                         for q in quantiles}
        }
        
        # Test for heterogeneity
        # Null hypothesis: No heterogeneity (all CATEs are equal)
        from scipy.stats import f_oneway
        
        # Split into groups based on median CATE
        median_cate = np.median(self.cate_)
        low_cate_group = self.cate_[self.cate_ <= median_cate]
        high_cate_group = self.cate_[self.cate_ > median_cate]
        
        f_stat, p_value = f_oneway(low_cate_group, high_cate_group)
        
        cate_stats['heterogeneity_test'] = {
            'f_statistic': float(f_stat),
            'p_value': float(p_value),
            'significant': bool(p_value < 0.05)
        }
        
        # Feature importance
        if self.feature_importance_ is not None:
            cate_stats['feature_importance'] = self.feature_importance_.to_dict('records')
        
        logger.info(f"✓ Heterogeneity analysis completed")
        logger.info(f"  Heterogeneity significant: {cate_stats['heterogeneity_test']['significant']}")
        
        return cate_stats
    
    def plot_cate_distribution(self, save_path: Optional[Path] = None) -> plt.Figure:
        """
        Plot CATE distribution
        
        Args:
            save_path: Optional path to save figure
        
        Returns:
            Matplotlib figure
        """
        if self.cate_ is None:
            raise ValueError("Must run estimate_cate() first")
        
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        
        # Histogram
        axes[0].hist(self.cate_, bins=30, edgecolor='black', alpha=0.7)
        axes[0].axvline(self.cate_.mean(), color='red', linestyle='--', 
                       label=f'Mean: {self.cate_.mean():.3f}')
        axes[0].axvline(0, color='gray', linestyle=':', alpha=0.5)
        axes[0].set_xlabel('CATE')
        axes[0].set_ylabel('Frequency')
        axes[0].set_title('Distribution of Conditional Average Treatment Effects')
        axes[0].legend()
        
        # Box plot
        axes[1].boxplot(self.cate_, vert=True)
        axes[1].axhline(0, color='gray', linestyle=':', alpha=0.5)
        axes[1].set_ylabel('CATE')
        axes[1].set_title('CATE Distribution')
        axes[1].set_xticks([])
        
        plt.tight_layout()
        
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"  Saved figure: {save_path}")
        
        return fig
    
    def plot_feature_importance(self, top_n: int = 10, 
                               save_path: Optional[Path] = None) -> plt.Figure:
        """
        Plot feature importance for CATE heterogeneity
        
        Args:
            top_n: Number of top features to plot
            save_path: Optional path to save figure
        
        Returns:
            Matplotlib figure
        """
        if self.feature_importance_ is None:
            raise ValueError("Feature importance not available")
        
        top_features = self.feature_importance_.head(top_n)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(range(len(top_features)), top_features['importance'])
        ax.set_yticks(range(len(top_features)))
        ax.set_yticklabels(top_features['feature'])
        ax.set_xlabel('Importance')
        ax.set_title('Feature Importance for Treatment Effect Heterogeneity')
        ax.invert_yaxis()
        
        plt.tight_layout()
        
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"  Saved figure: {save_path}")
        
        return fig
    
    def plot_cate_by_feature(self, feature: str, bins: int = 5,
                           save_path: Optional[Path] = None) -> plt.Figure:
        """
        Plot CATE across feature bins
        
        Args:
            feature: Feature to analyze
            bins: Number of bins
            save_path: Optional path to save figure
        
        Returns:
            Matplotlib figure
        """
        if self.cate_ is None:
            raise ValueError("Must run estimate_cate() first")
        
        cols = [self.outcome, self.treatment] + self.features + self.controls
        df_clean = self.df[cols].dropna()
        df_clean['cate'] = self.cate_
        
        # Create bins
        df_clean[f'{feature}_bin'] = pd.qcut(df_clean[feature], q=bins, 
                                              labels=[f'Q{i+1}' for i in range(bins)])
        
        # Calculate mean CATE by bin
        bin_stats = df_clean.groupby(f'{feature}_bin')['cate'].agg(['mean', 'std', 'count'])
        bin_stats['se'] = bin_stats['std'] / np.sqrt(bin_stats['count'])
        
        # Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        x = range(len(bin_stats))
        ax.bar(x, bin_stats['mean'], yerr=1.96*bin_stats['se'], 
              capsize=5, alpha=0.7, edgecolor='black')
        ax.axhline(0, color='gray', linestyle='--', alpha=0.5)
        ax.set_xticks(x)
        ax.set_xticklabels(bin_stats.index)
        ax.set_xlabel(f'{feature} (Quintiles)')
        ax.set_ylabel('Average CATE')
        ax.set_title(f'Treatment Effect Heterogeneity by {feature}')
        
        plt.tight_layout()
        
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"  Saved figure: {save_path}")
        
        return fig
    
    def estimate_policy_tree(self, depth: int = 2) -> Dict[str, Any]:
        """
        Estimate policy tree for treatment assignment
        
        Args:
            depth: Maximum tree depth
        
        Returns:
            Dictionary with policy tree results
        """
        if self.cate_ is None:
            raise ValueError("Must run estimate_cate() first")
        
        logger.info("Estimating policy tree...")
        
        Y, T, X, W = self.preprocess_data()
        
        # Initialize policy tree
        policy_tree = PolicyTree(
            policy_learner=self.model,
            max_depth=depth
        )
        
        # Fit policy tree
        policy_tree.fit(X=X)
        
        # Get policy recommendations
        policy_rec = policy_tree.predict(X)
        
        # Calculate value of recommended policy
        value = self.model.score(Y=Y, T=policy_rec, X=X, W=W)
        
        results = {
            'policy_tree': policy_tree,
            'recommendations': policy_rec,
            'value': float(value),
            'treatment_rate': float(policy_rec.mean())
        }
        
        logger.info(f"✓ Policy tree estimated")
        logger.info(f"  Policy value: {value:.4f}")
        logger.info(f"  Treatment rate under policy: {policy_rec.mean():.1%}")
        
        return results
    
    def generate_report(self, output_dir: Path) -> str:
        """
        Generate comprehensive Causal Forest analysis report
        
        Args:
            output_dir: Directory to save report and figures
        
        Returns:
            Report text
        """
        if self.cate_ is None:
            raise ValueError("Must run estimate_cate() first")
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Analyze heterogeneity
        het_stats = self.analyze_heterogeneity()
        
        # Generate plots
        self.plot_cate_distribution(output_dir / 'cate_distribution.png')
        if self.feature_importance_ is not None:
            self.plot_feature_importance(save_path=output_dir / 'feature_importance.png')
        
        # Generate report
        report = f"""
# Causal Forest Analysis Report

## Model Specification
- **Treatment Variable**: {self.treatment}
- **Outcome Variable**: {self.outcome}
- **Features for Heterogeneity**: {', '.join(self.features)}
- **Control Variables**: {', '.join(self.controls) if self.controls else 'None'}
- **Observations**: {len(self.cate_):,}

## Results Summary

### Average Treatment Effect
- **Mean CATE**: {het_stats['mean']:.4f}
- **Std Dev**: {het_stats['std']:.4f}
- **Range**: [{het_stats['min']:.4f}, {het_stats['max']:.4f}]

### Heterogeneity Analysis
- **25th Percentile**: {het_stats['quantiles']['q25']:.4f}
- **Median**: {het_stats['quantiles']['q50']:.4f}
- **75th Percentile**: {het_stats['quantiles']['q75']:.4f}

### Statistical Test for Heterogeneity
- **F-statistic**: {het_stats['heterogeneity_test']['f_statistic']:.2f}
- **P-value**: {het_stats['heterogeneity_test']['p_value']:.4f}
- **Significant Heterogeneity**: {'Yes' if het_stats['heterogeneity_test']['significant'] else 'No'}

## Interpretation

{self._generate_interpretation(het_stats)}

## Feature Importance

Top drivers of treatment effect heterogeneity:
"""
        
        if 'feature_importance' in het_stats:
            for feat in het_stats['feature_importance'][:5]:
                report += f"\n- {feat['feature']}: {feat['importance']:.3f}"
        
        report += "\n\n## Visualizations\n\n"
        report += "- `cate_distribution.png`: Distribution of treatment effects\n"
        report += "- `feature_importance.png`: Feature importance for heterogeneity\n"
        
        # Save report
        report_path = output_dir / 'causal_forest_report.md'
        with open(report_path, 'w') as f:
            f.write(report)
        
        logger.info(f"✓ Report saved: {report_path}")
        
        return report
    
    def _generate_interpretation(self, het_stats: Dict) -> str:
        """Generate interpretation text"""
        mean_cate = het_stats['mean']
        is_heterogeneous = het_stats['heterogeneity_test']['significant']
        
        interpretation = f"The average treatment effect is {mean_cate:.4f}, "
        
        if mean_cate > 0:
            interpretation += "indicating a positive effect of the treatment on the outcome. "
        elif mean_cate < 0:
            interpretation += "indicating a negative effect of the treatment on the outcome. "
        else:
            interpretation += "indicating no average effect of the treatment. "
        
        if is_heterogeneous:
            interpretation += (
                "\n\nThere is statistically significant heterogeneity in treatment effects "
                "across the sample. This suggests that the treatment effect varies systematically "
                "with firm characteristics. Decision-makers should consider these heterogeneous "
                "effects when implementing the treatment strategy."
            )
        else:
            interpretation += (
                "\n\nThere is no statistically significant heterogeneity in treatment effects. "
                "The treatment effect appears relatively homogeneous across the sample."
            )
        
        return interpretation


# Example usage
if __name__ == "__main__":
    # Generate sample data for demonstration
    np.random.seed(42)
    n = 1000
    
    # Generate features
    firm_size = np.random.lognormal(10, 1, n)
    rd_intensity = np.random.uniform(0, 0.15, n)
    leverage = np.random.uniform(0.2, 0.8, n)
    
    # Treatment assignment (with some selection)
    treatment_prob = 0.3 + 0.2 * (firm_size > np.median(firm_size))
    treatment = np.random.binomial(1, treatment_prob, n)
    
    # Outcome with heterogeneous treatment effect
    # Effect is stronger for firms with higher R&D
    base_roa = 0.05 + 0.0001 * firm_size + 0.1 * rd_intensity - 0.05 * leverage
    treatment_effect = 0.02 + 0.3 * rd_intensity  # Heterogeneous effect
    roa = base_roa + treatment * treatment_effect + np.random.normal(0, 0.01, n)
    
    # Create DataFrame
    df = pd.DataFrame({
        'firm_id': range(n),
        'year': 2020,
        'merger_dummy': treatment,
        'roa': roa,
        'firm_size': firm_size,
        'rd_intensity': rd_intensity,
        'leverage': leverage
    })
    
    print("=" * 80)
    print("CAUSAL FOREST EXAMPLE")
    print("=" * 80)
    
    # Initialize analyzer
    analyzer = CausalForestAnalyzer(
        df=df,
        treatment='merger_dummy',
        outcome='roa',
        features=['firm_size', 'rd_intensity', 'leverage']
    )
    
    # Estimate CATE
    cate_results = analyzer.estimate_cate()
    
    # Analyze heterogeneity
    het_stats = analyzer.analyze_heterogeneity()
    
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    print(f"\nMean CATE: {het_stats['mean']:.4f}")
    print(f"Heterogeneity significant: {het_stats['heterogeneity_test']['significant']}")
    
    if ECONML_AVAILABLE:
        print("\n✓ Causal Forest analysis completed successfully")
        print("\nTo generate visualizations and full report:")
        print("  analyzer.plot_cate_distribution()")
        print("  analyzer.plot_feature_importance()")
        print("  analyzer.generate_report(Path('output/'))")
