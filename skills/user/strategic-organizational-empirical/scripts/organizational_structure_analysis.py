#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Organizational Structure Analysis: 組織構造の多次元的分析システム

Philosophical and Theoretical Foundation:
=========================================
組織構造の分析は、Mintzberg (1979)の構造類型論、Pugh et al. (1968)の
Aston研究、Burns & Stalker (1961)の機械的・有機的組織論という
三大理論的伝統に基づく。構造は単なる公式的配置ではなく、権限、調整、
標準化の複雑な相互作用として理解されるべきである（Galbraith, 1973）。

Core Theoretical Dimensions:
- Complexity (複雑性): 水平的・垂直的・空間的分化
- Formalization (公式化): 規則・手順の標準化度合い
- Centralization (集権化): 意思決定権限の集中度
- Specialization (専門化): 職務の細分化度合い
- Configuration (形態): 構造の全体的パターン

Analytical Capabilities:
========================
1. 構造次元の測定と診断
2. 構造類型の判別（機械的 vs 有機的、官僚制 vs アドホクラシー）
3. 構造的適合性の評価（環境・戦略・技術との整合性）
4. 構造変革の分析（再編・分権化・統合）
5. パフォーマンスへの影響評価

Supported Frameworks:
- Mintzberg's Structural Configurations
- Aston Group's Dimensions
- Burns & Stalker's Mechanistic-Organic Continuum
- Galbraith's Information Processing View

Usage:
======
    python organizational_structure_analysis.py \\
        --data organizational_data.csv \\
        --config structure_config.yaml \\
        --output structure_analysis_results.json

Author: Strategic Management Research Lab
Version: 1.0.0
License: MIT
Date: 2025-11-08

References:
-----------
- Mintzberg, H. (1979). The Structuring of Organizations. Prentice Hall.
- Pugh, D. S., et al. (1968). Dimensions of organization structure. ASQ, 13(1), 65-105.
- Burns, T., & Stalker, G. M. (1961). The Management of Innovation. Tavistock.
- Galbraith, J. R. (1973). Designing Complex Organizations. Addison-Wesley.
"""

import argparse
import yaml
import json
import pandas as pd
import numpy as np
from scipy import stats
from scipy.cluster import hierarchy
from scipy.spatial.distance import pdist
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, field
import sys
import warnings

warnings.filterwarnings('ignore')

# ==============================================================================
# Structural Dimensions (構造次元)
# ==============================================================================

@dataclass
class StructuralDimensions:
    """
    組織構造の基本次元（Pugh et al., 1968; Mintzberg, 1979）
    """
    # Aston Group Dimensions
    specialization: float = 0.0  # 専門化度
    standardization: float = 0.0  # 標準化度
    formalization: float = 0.0  # 公式化度
    centralization: float = 0.0  # 集権化度
    configuration: float = 0.0  # 形態的複雑性
    
    # Additional Dimensions
    vertical_complexity: float = 0.0  # 垂直的複雑性（階層数）
    horizontal_complexity: float = 0.0  # 水平的複雑性（部門数）
    spatial_dispersion: float = 0.0  # 空間的分散
    
    def compute_overall_complexity(self) -> float:
        """全体的複雑性の計算"""
        return (self.vertical_complexity + 
                self.horizontal_complexity + 
                self.spatial_dispersion) / 3
    
    def compute_bureaucratic_score(self) -> float:
        """官僚制度合いの計算"""
        return (self.specialization + 
                self.standardization + 
                self.formalization + 
                self.centralization) / 4
    
    def classify_structure_type(self) -> str:
        """構造類型の分類"""
        bureau_score = self.compute_bureaucratic_score()
        complexity = self.compute_overall_complexity()
        
        if bureau_score > 0.7 and complexity > 0.6:
            return "Professional Bureaucracy"
        elif bureau_score > 0.7 and complexity <= 0.6:
            return "Machine Bureaucracy"
        elif bureau_score <= 0.4 and complexity > 0.6:
            return "Adhocracy"
        elif bureau_score <= 0.4 and complexity <= 0.6:
            return "Simple Structure"
        else:
            return "Divisional Form"

@dataclass
class OrganizationalProfile:
    """組織プロファイル"""
    org_id: str
    org_name: str
    dimensions: StructuralDimensions
    size: int
    age: int
    industry: str
    performance: float = 0.0
    
    def to_dict(self) -> Dict:
        """辞書形式への変換"""
        return {
            'org_id': self.org_id,
            'org_name': self.org_name,
            'size': self.size,
            'age': self.age,
            'industry': self.industry,
            'performance': self.performance,
            **vars(self.dimensions)
        }

# ==============================================================================
# Core Analyzer Class
# ==============================================================================

class OrganizationalStructureAnalyzer:
    """
    組織構造分析の中核クラス
    
    Analytical Philosophy:
    ---------------------
    構造は固定的実体ではなく、環境・戦略・技術との動的適合の産物である。
    Contingency Theory (Lawrence & Lorsch, 1967) が示すように、
    最適構造は文脈依存的である。本分析器は、構造の記述を超えて、
    その適合性と有効性を評価する。
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初期化
        
        Parameters:
        -----------
        config_path : str, optional
            設定ファイルパス
        """
        self.config = self._load_config(config_path) if config_path else {}
        self.org_profiles: List[OrganizationalProfile] = []
        self.analysis_results: Dict[str, Any] = {}
    
    def _load_config(self, config_path: str) -> Dict:
        """設定ファイルの読み込み"""
        path = Path(config_path)
        with open(path, 'r', encoding='utf-8') as f:
            if path.suffix in ['.yaml', '.yml']:
                return yaml.safe_load(f)
            else:
                return json.load(f)
    
    def load_organizational_data(self, data_path: str) -> pd.DataFrame:
        """
        組織データの読み込み
        
        Expected columns:
        - org_id, org_name
        - size, age, industry
        - specialization, standardization, formalization, centralization
        - vertical_complexity, horizontal_complexity, spatial_dispersion
        - performance (optional)
        """
        df = pd.read_csv(data_path)
        
        # Validate required columns
        required_cols = ['org_id', 'org_name', 'size', 'age', 'industry']
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        
        # Create organizational profiles
        for _, row in df.iterrows():
            dimensions = StructuralDimensions(
                specialization=row.get('specialization', 0.0),
                standardization=row.get('standardization', 0.0),
                formalization=row.get('formalization', 0.0),
                centralization=row.get('centralization', 0.0),
                configuration=row.get('configuration', 0.0),
                vertical_complexity=row.get('vertical_complexity', 0.0),
                horizontal_complexity=row.get('horizontal_complexity', 0.0),
                spatial_dispersion=row.get('spatial_dispersion', 0.0)
            )
            
            profile = OrganizationalProfile(
                org_id=str(row['org_id']),
                org_name=str(row['org_name']),
                dimensions=dimensions,
                size=int(row['size']),
                age=int(row['age']),
                industry=str(row['industry']),
                performance=float(row.get('performance', 0.0))
            )
            
            self.org_profiles.append(profile)
        
        return df
    
    def compute_descriptive_statistics(self) -> Dict[str, Any]:
        """
        記述統計量の計算
        
        Returns comprehensive descriptive statistics for all structural dimensions.
        """
        # Convert to DataFrame
        data = pd.DataFrame([p.to_dict() for p in self.org_profiles])
        
        # Dimension columns
        dim_cols = [
            'specialization', 'standardization', 'formalization', 
            'centralization', 'vertical_complexity', 'horizontal_complexity',
            'spatial_dispersion'
        ]
        
        descriptive_stats = {}
        
        for col in dim_cols:
            if col in data.columns:
                descriptive_stats[col] = {
                    'mean': float(data[col].mean()),
                    'std': float(data[col].std()),
                    'min': float(data[col].min()),
                    'max': float(data[col].max()),
                    'median': float(data[col].median()),
                    'q25': float(data[col].quantile(0.25)),
                    'q75': float(data[col].quantile(0.75))
                }
        
        # Overall metrics
        descriptive_stats['overall'] = {
            'n_organizations': len(self.org_profiles),
            'size_mean': float(data['size'].mean()),
            'age_mean': float(data['age'].mean()),
            'industries': data['industry'].nunique()
        }
        
        self.analysis_results['descriptive_stats'] = descriptive_stats
        return descriptive_stats
    
    def classify_structure_types(self) -> Dict[str, Any]:
        """
        構造類型の分類
        
        Applies Mintzberg's configurational taxonomy to classify each organization.
        """
        classifications = []
        
        for profile in self.org_profiles:
            struct_type = profile.dimensions.classify_structure_type()
            bureau_score = profile.dimensions.compute_bureaucratic_score()
            complexity = profile.dimensions.compute_overall_complexity()
            
            classifications.append({
                'org_id': profile.org_id,
                'org_name': profile.org_name,
                'structure_type': struct_type,
                'bureaucratic_score': bureau_score,
                'complexity_score': complexity
            })
        
        # Distribution of types
        types_df = pd.DataFrame(classifications)
        type_distribution = types_df['structure_type'].value_counts().to_dict()
        
        result = {
            'classifications': classifications,
            'type_distribution': type_distribution
        }
        
        self.analysis_results['structure_types'] = result
        return result
    
    def analyze_structural_fit(self, 
                               environment_var: Optional[str] = None,
                               strategy_var: Optional[str] = None) -> Dict[str, Any]:
        """
        構造的適合性の分析
        
        Evaluates structural fit with environmental and strategic contingencies.
        Based on Contingency Theory (Lawrence & Lorsch, 1967; Donaldson, 2001).
        
        Parameters:
        -----------
        environment_var : str, optional
            環境変数名（例：uncertainty, dynamism）
        strategy_var : str, optional
            戦略変数名（例：differentiation, cost_leadership）
        
        Returns:
        --------
        Dict[str, Any]
            適合性分析結果
        """
        data = pd.DataFrame([p.to_dict() for p in self.org_profiles])
        
        fit_analysis = {
            'environment_structure_fit': None,
            'strategy_structure_fit': None,
            'performance_implications': None
        }
        
        # Environment-Structure Fit
        if environment_var and environment_var in data.columns:
            # Burns & Stalker (1961): Mechanistic-Organic Fit
            # High uncertainty → Organic structure (low bureaucracy)
            # Low uncertainty → Mechanistic structure (high bureaucracy)
            
            data['bureau_score'] = data.apply(
                lambda row: StructuralDimensions(
                    specialization=row['specialization'],
                    standardization=row['standardization'],
                    formalization=row['formalization'],
                    centralization=row['centralization']
                ).compute_bureaucratic_score(),
                axis=1
            )
            
            # Compute fit as interaction
            data['env_struct_fit'] = -1 * data[environment_var] * data['bureau_score']
            
            # Correlation analysis
            corr = data[[environment_var, 'bureau_score']].corr().iloc[0, 1]
            
            fit_analysis['environment_structure_fit'] = {
                'correlation': float(corr),
                'expected_direction': 'negative',
                'interpretation': ('Negative correlation supports Burns & Stalker: '
                                  'uncertain environments require organic structures')
            }
        
        # Strategy-Structure Fit
        if strategy_var and strategy_var in data.columns:
            # Chandler (1962): Structure follows strategy
            # Differentiation → Organic/flexible structure
            # Cost leadership → Mechanistic/efficient structure
            
            if 'bureau_score' not in data.columns:
                data['bureau_score'] = data.apply(
                    lambda row: StructuralDimensions(
                        specialization=row['specialization'],
                        standardization=row['standardization'],
                        formalization=row['formalization'],
                        centralization=row['centralization']
                    ).compute_bureaucratic_score(),
                    axis=1
                )
            
            corr = data[[strategy_var, 'bureau_score']].corr().iloc[0, 1]
            
            fit_analysis['strategy_structure_fit'] = {
                'correlation': float(corr),
                'interpretation': 'Alignment between strategic orientation and structure'
            }
        
        # Performance implications
        if 'performance' in data.columns and 'bureau_score' in data.columns:
            # Interaction effects
            if environment_var and environment_var in data.columns:
                # Three-way interaction: Environment x Structure x Performance
                from scipy.stats import pearsonr
                
                # Fit index
                data['env_fit_index'] = np.abs(
                    data[environment_var] + data['bureau_score'] - data[environment_var].mean()
                )
                
                corr_fit_perf = data[['env_fit_index', 'performance']].corr().iloc[0, 1]
                
                fit_analysis['performance_implications'] = {
                    'fit_performance_correlation': float(corr_fit_perf),
                    'interpretation': ('Positive correlation suggests better fit '
                                     'leads to higher performance')
                }
        
        self.analysis_results['structural_fit'] = fit_analysis
        return fit_analysis
    
    def perform_cluster_analysis(self, n_clusters: int = 4) -> Dict[str, Any]:
        """
        クラスター分析による構造パターンの発見
        
        Uses K-means clustering to identify structural archetypes.
        """
        # Prepare data
        dim_cols = [
            'specialization', 'standardization', 'formalization', 
            'centralization', 'vertical_complexity', 'horizontal_complexity'
        ]
        
        data = pd.DataFrame([p.to_dict() for p in self.org_profiles])
        X = data[dim_cols].values
        
        # Standardize
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # K-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(X_scaled)
        
        data['cluster'] = clusters
        
        # Compute cluster centroids (in original scale)
        centroids = scaler.inverse_transform(kmeans.cluster_centers_)
        
        # Characterize each cluster
        cluster_profiles = []
        for i in range(n_clusters):
            cluster_data = data[data['cluster'] == i]
            
            profile = {
                'cluster_id': i,
                'n_organizations': len(cluster_data),
                'centroid': dict(zip(dim_cols, centroids[i])),
                'mean_performance': float(cluster_data['performance'].mean()),
                'dominant_industries': cluster_data['industry'].value_counts().head(3).to_dict()
            }
            
            # Infer cluster label
            centroid_dict = profile['centroid']
            if (centroid_dict['formalization'] > 0.7 and 
                centroid_dict['centralization'] > 0.7):
                profile['label'] = "機械的官僚制 (Machine Bureaucracy)"
            elif (centroid_dict['formalization'] < 0.4 and 
                  centroid_dict['centralization'] < 0.4):
                profile['label'] = "アドホクラシー (Adhocracy)"
            else:
                profile['label'] = f"混合型 Cluster {i}"
            
            cluster_profiles.append(profile)
        
        result = {
            'n_clusters': n_clusters,
            'cluster_assignments': clusters.tolist(),
            'cluster_profiles': cluster_profiles
        }
        
        self.analysis_results['cluster_analysis'] = result
        return result
    
    def analyze_structural_change(self, 
                                 time_var: str,
                                 org_id_var: str = 'org_id') -> Dict[str, Any]:
        """
        構造変革の分析（パネルデータ対応）
        
        Analyzes structural changes over time for panel data.
        """
        data = pd.DataFrame([p.to_dict() for p in self.org_profiles])
        
        if time_var not in data.columns:
            return {'error': 'Time variable not found in data'}
        
        # Calculate structural change rates
        dim_cols = [
            'specialization', 'standardization', 'formalization', 
            'centralization'
        ]
        
        data_sorted = data.sort_values([org_id_var, time_var])
        
        change_analysis = {
            'avg_change_rates': {},
            'organizations_with_major_changes': []
        }
        
        for col in dim_cols:
            if col in data.columns:
                data_sorted[f'{col}_change'] = data_sorted.groupby(org_id_var)[col].diff()
                avg_change = data_sorted[f'{col}_change'].abs().mean()
                change_analysis['avg_change_rates'][col] = float(avg_change)
        
        # Identify organizations with major changes
        data_sorted['total_change'] = data_sorted[[f'{col}_change' for col in dim_cols 
                                                   if col in data.columns]].abs().sum(axis=1)
        
        major_changes = data_sorted.nlargest(10, 'total_change')[[
            org_id_var, time_var, 'total_change'
        ]].to_dict('records')
        
        change_analysis['organizations_with_major_changes'] = major_changes
        
        self.analysis_results['structural_change'] = change_analysis
        return change_analysis
    
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """包括的分析報告書の生成"""
        if not self.analysis_results:
            raise ValueError("No analysis results available. Run analysis methods first.")
        
        report = {
            'metadata': {
                'n_organizations': len(self.org_profiles),
                'analysis_date': pd.Timestamp.now().isoformat()
            },
            'analyses': self.analysis_results,
            'summary': self._generate_executive_summary()
        }
        
        return report
    
    def _generate_executive_summary(self) -> str:
        """エグゼクティブ・サマリーの生成"""
        summary = "## 組織構造分析：エグゼクティブ・サマリー\n\n"
        
        if 'descriptive_stats' in self.analysis_results:
            stats = self.analysis_results['descriptive_stats']
            n_orgs = stats['overall']['n_organizations']
            summary += f"分析対象：{n_orgs}組織\n\n"
        
        if 'structure_types' in self.analysis_results:
            types = self.analysis_results['structure_types']['type_distribution']
            summary += "### 構造類型の分布\n"
            for stype, count in types.items():
                summary += f"- {stype}: {count}組織\n"
            summary += "\n"
        
        if 'structural_fit' in self.analysis_results:
            fit = self.analysis_results['structural_fit']
            if fit.get('performance_implications'):
                corr = fit['performance_implications']['fit_performance_correlation']
                summary += f"### 適合性とパフォーマンス\n"
                summary += f"構造的適合性とパフォーマンスの相関: {corr:.3f}\n\n"
        
        return summary
    
    def save_results(self, output_path: str) -> None:
        """結果の保存"""
        report = self.generate_comprehensive_report()
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ Analysis results saved to: {output_path}")

# ==============================================================================
# Command-Line Interface
# ==============================================================================

def main():
    """
    メインエントリポイント
    
    Example Usage:
    -------------
    python organizational_structure_analysis.py \\
        --data organizational_data.csv \\
        --config analysis_config.yaml \\
        --output results/structure_analysis.json \\
        --cluster 4
    """
    parser = argparse.ArgumentParser(
        description="Organizational Structure Analysis: 組織構造の多次元的分析",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--data', type=str, required=True,
                       help='Organizational data file (CSV)')
    parser.add_argument('--config', type=str,
                       help='Configuration file (YAML/JSON)')
    parser.add_argument('--output', type=str, required=True,
                       help='Output file path (JSON)')
    parser.add_argument('--cluster', type=int, default=4,
                       help='Number of clusters for cluster analysis')
    parser.add_argument('--environment', type=str,
                       help='Environment variable for fit analysis')
    parser.add_argument('--strategy', type=str,
                       help='Strategy variable for fit analysis')
    
    args = parser.parse_args()
    
    try:
        # Initialize analyzer
        analyzer = OrganizationalStructureAnalyzer(config_path=args.config)
        
        # Load data
        print("Loading organizational data...")
        analyzer.load_organizational_data(args.data)
        
        # Run analyses
        print("\nComputing descriptive statistics...")
        analyzer.compute_descriptive_statistics()
        
        print("Classifying structure types...")
        analyzer.classify_structure_types()
        
        print("Performing cluster analysis...")
        analyzer.perform_cluster_analysis(n_clusters=args.cluster)
        
        if args.environment or args.strategy:
            print("Analyzing structural fit...")
            analyzer.analyze_structural_fit(
                environment_var=args.environment,
                strategy_var=args.strategy
            )
        
        # Save results
        analyzer.save_results(args.output)
        
        print("\n" + "="*70)
        print("Organizational Structure Analysis Complete")
        print("="*70)
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
