#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Competitive Strategy Analyzer: 競争戦略の理論駆動型分析システム

Philosophical and Theoretical Foundation:
=========================================
競争戦略の分析は、Porter (1980, 1985)の競争優位論、Miles & Snow (1978)の
戦略類型論、そしてMintzberg (1978)の創発的戦略論という三大理論的潮流に
基づく。戦略は単なる計画ではなく、意図的選択と創発的パターンの弁証法的
統一として理解されるべきである（Mintzberg & Waters, 1985）。

Core Theoretical Frameworks:
----------------------------
1. **Porter's Generic Strategies (Porter, 1980, 1985)**
   - Cost Leadership (コストリーダーシップ)
   - Differentiation (差別化)
   - Focus (集中)
   - Stuck-in-the-Middle (中途半端)

2. **Miles & Snow's Strategic Types (Miles & Snow, 1978)**
   - Prospector (先駆者)
   - Defender (防衛者)
   - Analyzer (分析者)
   - Reactor (反応者)

3. **Mintzberg's Strategy Process (Mintzberg, 1978)**
   - Deliberate vs. Emergent Strategies
   - Realized Strategy = Deliberate + Emergent

Analytical Capabilities:
========================
1. 戦略類型の判別と分類
2. 戦略的ポジショニングの評価
3. 戦略の一貫性（coherence）分析
4. 戦略-環境適合性の検証
5. 戦略とパフォーマンスの関係分析

Usage:
======
    python competitive_strategy_analyzer.py \\
        --data strategy_data.csv \\
        --framework porter \\
        --output strategy_analysis.json

Author: Strategic Management Research Lab
Version: 1.0.0
License: MIT
Date: 2025-11-08

References:
-----------
- Porter, M. E. (1980). Competitive Strategy. Free Press.
- Porter, M. E. (1985). Competitive Advantage. Free Press.
- Miles, R. E., & Snow, C. C. (1978). Organizational Strategy, Structure, and Process.
  McGraw-Hill.
- Mintzberg, H. (1978). Patterns in strategy formation. MS, 24(9), 934-948.
- Mintzberg, H., & Waters, J. A. (1985). Of strategies, deliberate and emergent.
  SMJ, 6(3), 257-272.
"""

import argparse
import yaml
import json
import pandas as pd
import numpy as np
from scipy import stats
from scipy.cluster import hierarchy
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.cluster import KMeans
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import sys
import warnings

warnings.filterwarnings('ignore')

# ==============================================================================
# Strategy Type Enums
# ==============================================================================

class PorterStrategy(Enum):
    """Porter's Generic Strategies"""
    COST_LEADERSHIP = "コストリーダーシップ"
    DIFFERENTIATION = "差別化"
    COST_FOCUS = "コスト集中"
    DIFFERENTIATION_FOCUS = "差別化集中"
    STUCK_IN_MIDDLE = "中途半端"

class MilesSnowStrategy(Enum):
    """Miles & Snow's Strategic Types"""
    PROSPECTOR = "先駆者 (Prospector)"
    DEFENDER = "防衛者 (Defender)"
    ANALYZER = "分析者 (Analyzer)"
    REACTOR = "反応者 (Reactor)"

# ==============================================================================
# Strategic Profile Data Classes
# ==============================================================================

@dataclass
class PorterProfile:
    """Porter's framework における戦略プロファイル"""
    cost_position: float  # コストポジション (低い方が有利)
    differentiation: float  # 差別化度 (高い方が有利)
    market_scope: float  # 市場範囲 (広い vs 狭い)
    
    def classify_strategy(self) -> PorterStrategy:
        """戦略類型の分類"""
        # Normalize scores (0-1 range)
        cost_advantage = 1 - self.cost_position  # Invert: lower cost = higher advantage
        
        # Classification logic
        if self.market_scope > 0.6:  # Broad scope
            if cost_advantage > 0.7 and self.differentiation < 0.5:
                return PorterStrategy.COST_LEADERSHIP
            elif self.differentiation > 0.7 and cost_advantage < 0.5:
                return PorterStrategy.DIFFERENTIATION
            else:
                return PorterStrategy.STUCK_IN_MIDDLE
        else:  # Narrow scope (Focus)
            if cost_advantage > self.differentiation:
                return PorterStrategy.COST_FOCUS
            else:
                return PorterStrategy.DIFFERENTIATION_FOCUS
    
    def compute_strategic_coherence(self) -> float:
        """戦略的一貫性の計算"""
        strategy_type = self.classify_strategy()
        
        if strategy_type == PorterStrategy.STUCK_IN_MIDDLE:
            # Low coherence for stuck-in-the-middle
            return 0.3
        else:
            # High coherence for clear strategies
            cost_adv = 1 - self.cost_position
            
            if strategy_type in [PorterStrategy.COST_LEADERSHIP, PorterStrategy.COST_FOCUS]:
                return cost_adv
            else:
                return self.differentiation

@dataclass
class MilesSnowProfile:
    """Miles & Snow framework における戦略プロファイル"""
    innovation_orientation: float  # イノベーション志向
    market_aggressiveness: float  # 市場攻撃性
    risk_tolerance: float  # リスク許容度
    planning_orientation: float  # 計画志向
    
    def classify_strategy(self) -> MilesSnowStrategy:
        """戦略類型の分類"""
        # Prospector: high innovation, high aggression, high risk
        prospector_score = (self.innovation_orientation + 
                          self.market_aggressiveness + 
                          self.risk_tolerance) / 3
        
        # Defender: low innovation, low aggression, low risk
        defender_score = (3 - self.innovation_orientation - 
                         self.market_aggressiveness - 
                         self.risk_tolerance) / 3
        
        # Analyzer: moderate on all, high planning
        analyzer_score = self.planning_orientation - np.std([
            self.innovation_orientation,
            self.market_aggressiveness,
            self.risk_tolerance
        ])
        
        scores = {
            'prospector': prospector_score,
            'defender': defender_score,
            'analyzer': analyzer_score
        }
        
        max_type = max(scores, key=scores.get)
        
        # Check for Reactor (inconsistent pattern)
        if max(scores.values()) < 0.5:
            return MilesSnowStrategy.REACTOR
        
        return {
            'prospector': MilesSnowStrategy.PROSPECTOR,
            'defender': MilesSnowStrategy.DEFENDER,
            'analyzer': MilesSnowStrategy.ANALYZER
        }[max_type]

@dataclass
class CompetitiveProfile:
    """統合的競争プロファイル"""
    firm_id: str
    firm_name: str
    porter_profile: PorterProfile
    miles_snow_profile: MilesSnowProfile
    industry: str
    performance: float = 0.0
    environment_uncertainty: float = 0.0
    
    def to_dict(self) -> Dict:
        """辞書形式への変換"""
        return {
            'firm_id': self.firm_id,
            'firm_name': self.firm_name,
            'industry': self.industry,
            'performance': self.performance,
            'environment_uncertainty': self.environment_uncertainty,
            **vars(self.porter_profile),
            **vars(self.miles_snow_profile)
        }

# ==============================================================================
# Core Analyzer Class
# ==============================================================================

class CompetitiveStrategyAnalyzer:
    """
    競争戦略分析の中核クラス
    
    Analytical Philosophy:
    ---------------------
    戦略の有効性は、内的一貫性（internal consistency）と外的適合性
    （external fit）の両方に依存する。Porter (1996)が「Strategic Fit」で
    論じたように、戦略的選択は相互補完的な活動システムを構成する。
    本分析器は、これらの多層的な整合性を定量的に評価する。
    """
    
    def __init__(self, framework: str = 'porter', config_path: Optional[str] = None):
        """
        初期化
        
        Parameters:
        -----------
        framework : str
            分析フレームワーク ('porter', 'miles_snow', 'both')
        config_path : str, optional
            設定ファイルパス
        """
        self.framework = framework.lower()
        self.config = self._load_config(config_path) if config_path else {}
        self.firm_profiles: List[CompetitiveProfile] = []
        self.analysis_results: Dict[str, Any] = {}
    
    def _load_config(self, config_path: str) -> Dict:
        """設定ファイルの読み込み"""
        path = Path(config_path)
        with open(path, 'r', encoding='utf-8') as f:
            if path.suffix in ['.yaml', '.yml']:
                return yaml.safe_load(f)
            else:
                return json.load(f)
    
    def load_strategy_data(self, data_path: str) -> pd.DataFrame:
        """
        戦略データの読み込み
        
        Expected columns:
        - firm_id, firm_name, industry
        - Porter variables: cost_position, differentiation, market_scope
        - Miles & Snow variables: innovation_orientation, market_aggressiveness,
          risk_tolerance, planning_orientation
        - performance, environment_uncertainty (optional)
        """
        df = pd.read_csv(data_path)
        
        # Validate required columns
        porter_cols = ['cost_position', 'differentiation', 'market_scope']
        miles_snow_cols = ['innovation_orientation', 'market_aggressiveness',
                          'risk_tolerance', 'planning_orientation']
        
        if self.framework in ['porter', 'both']:
            missing = [col for col in porter_cols if col not in df.columns]
            if missing:
                raise ValueError(f"Missing Porter columns: {missing}")
        
        if self.framework in ['miles_snow', 'both']:
            missing = [col for col in miles_snow_cols if col not in df.columns]
            if missing:
                raise ValueError(f"Missing Miles & Snow columns: {missing}")
        
        # Create competitive profiles
        for _, row in df.iterrows():
            porter_profile = PorterProfile(
                cost_position=row.get('cost_position', 0.5),
                differentiation=row.get('differentiation', 0.5),
                market_scope=row.get('market_scope', 0.5)
            )
            
            miles_snow_profile = MilesSnowProfile(
                innovation_orientation=row.get('innovation_orientation', 0.5),
                market_aggressiveness=row.get('market_aggressiveness', 0.5),
                risk_tolerance=row.get('risk_tolerance', 0.5),
                planning_orientation=row.get('planning_orientation', 0.5)
            )
            
            profile = CompetitiveProfile(
                firm_id=str(row['firm_id']),
                firm_name=str(row['firm_name']),
                porter_profile=porter_profile,
                miles_snow_profile=miles_snow_profile,
                industry=str(row['industry']),
                performance=float(row.get('performance', 0.0)),
                environment_uncertainty=float(row.get('environment_uncertainty', 0.0))
            )
            
            self.firm_profiles.append(profile)
        
        return df
    
    def classify_strategies(self) -> Dict[str, Any]:
        """
        戦略類型の分類
        
        Classifies each firm according to the selected theoretical framework.
        """
        classifications = []
        
        for profile in self.firm_profiles:
            classification = {
                'firm_id': profile.firm_id,
                'firm_name': profile.firm_name,
                'industry': profile.industry
            }
            
            if self.framework in ['porter', 'both']:
                porter_type = profile.porter_profile.classify_strategy()
                coherence = profile.porter_profile.compute_strategic_coherence()
                
                classification['porter_strategy'] = porter_type.value
                classification['porter_coherence'] = coherence
            
            if self.framework in ['miles_snow', 'both']:
                ms_type = profile.miles_snow_profile.classify_strategy()
                classification['miles_snow_strategy'] = ms_type.value
            
            classifications.append(classification)
        
        # Distribution analysis
        classifications_df = pd.DataFrame(classifications)
        
        result = {
            'classifications': classifications,
            'distributions': {}
        }
        
        if self.framework in ['porter', 'both']:
            porter_dist = classifications_df['porter_strategy'].value_counts().to_dict()
            result['distributions']['porter'] = porter_dist
        
        if self.framework in ['miles_snow', 'both']:
            ms_dist = classifications_df['miles_snow_strategy'].value_counts().to_dict()
            result['distributions']['miles_snow'] = ms_dist
        
        self.analysis_results['strategy_classifications'] = result
        return result
    
    def analyze_strategy_performance_relationship(self) -> Dict[str, Any]:
        """
        戦略とパフォーマンスの関係分析
        
        Examines the relationship between strategy type and firm performance.
        Tests core hypothesis: Does strategic clarity lead to superior performance?
        """
        data = pd.DataFrame([p.to_dict() for p in self.firm_profiles])
        
        analysis = {
            'porter_analysis': None,
            'miles_snow_analysis': None,
            'coherence_performance': None
        }
        
        # Porter framework analysis
        if self.framework in ['porter', 'both'] and 'performance' in data.columns:
            # Classify strategies
            data['porter_strategy'] = data.apply(
                lambda row: PorterProfile(
                    cost_position=row['cost_position'],
                    differentiation=row['differentiation'],
                    market_scope=row['market_scope']
                ).classify_strategy().value,
                axis=1
            )
            
            # Performance by strategy type
            perf_by_strategy = data.groupby('porter_strategy')['performance'].agg([
                'mean', 'std', 'count'
            ]).to_dict('index')
            
            # ANOVA test
            strategy_groups = [
                data[data['porter_strategy'] == strat]['performance'].values
                for strat in data['porter_strategy'].unique()
            ]
            f_stat, p_value = stats.f_oneway(*strategy_groups)
            
            # Coherence-Performance correlation
            data['coherence'] = data.apply(
                lambda row: PorterProfile(
                    cost_position=row['cost_position'],
                    differentiation=row['differentiation'],
                    market_scope=row['market_scope']
                ).compute_strategic_coherence(),
                axis=1
            )
            
            coherence_corr = data[['coherence', 'performance']].corr().iloc[0, 1]
            
            analysis['porter_analysis'] = {
                'performance_by_strategy': perf_by_strategy,
                'anova_f_statistic': float(f_stat),
                'anova_p_value': float(p_value),
                'significant_difference': p_value < 0.05
            }
            
            analysis['coherence_performance'] = {
                'correlation': float(coherence_corr),
                'interpretation': ('Positive correlation supports Porter: '
                                  'clear strategic positioning enhances performance')
            }
        
        # Miles & Snow framework analysis
        if self.framework in ['miles_snow', 'both'] and 'performance' in data.columns:
            data['ms_strategy'] = data.apply(
                lambda row: MilesSnowProfile(
                    innovation_orientation=row['innovation_orientation'],
                    market_aggressiveness=row['market_aggressiveness'],
                    risk_tolerance=row['risk_tolerance'],
                    planning_orientation=row['planning_orientation']
                ).classify_strategy().value,
                axis=1
            )
            
            perf_by_ms = data.groupby('ms_strategy')['performance'].agg([
                'mean', 'std', 'count'
            ]).to_dict('index')
            
            analysis['miles_snow_analysis'] = {
                'performance_by_strategy': perf_by_ms
            }
        
        self.analysis_results['strategy_performance'] = analysis
        return analysis
    
    def analyze_strategy_environment_fit(self) -> Dict[str, Any]:
        """
        戦略-環境適合性の分析
        
        Examines strategic fit with environmental conditions.
        Tests Contingency Theory hypothesis: Fit improves performance.
        """
        data = pd.DataFrame([p.to_dict() for p in self.firm_profiles])
        
        if 'environment_uncertainty' not in data.columns:
            return {'error': 'Environment uncertainty variable not available'}
        
        fit_analysis = {}
        
        # Porter framework: Test stuck-in-the-middle avoidance
        if self.framework in ['porter', 'both']:
            data['porter_strategy'] = data.apply(
                lambda row: PorterProfile(
                    cost_position=row['cost_position'],
                    differentiation=row['differentiation'],
                    market_scope=row['market_scope']
                ).classify_strategy().value,
                axis=1
            )
            
            # Check if uncertain environments punish stuck-in-the-middle more
            stuck_data = data[data['porter_strategy'] == PorterStrategy.STUCK_IN_MIDDLE.value]
            clear_data = data[data['porter_strategy'] != PorterStrategy.STUCK_IN_MIDDLE.value]
            
            if len(stuck_data) > 0 and len(clear_data) > 0:
                stuck_corr = stuck_data[['environment_uncertainty', 'performance']].corr().iloc[0, 1]
                clear_corr = clear_data[['environment_uncertainty', 'performance']].corr().iloc[0, 1]
                
                fit_analysis['porter_fit'] = {
                    'stuck_uncertainty_performance_corr': float(stuck_corr),
                    'clear_uncertainty_performance_corr': float(clear_corr),
                    'interpretation': ('Negative correlation for stuck-in-the-middle '
                                     'confirms Porter: unclear strategies suffer in '
                                     'uncertain environments')
                }
        
        # Miles & Snow: Prospectors thrive in uncertain environments
        if self.framework in ['miles_snow', 'both']:
            data['ms_strategy'] = data.apply(
                lambda row: MilesSnowProfile(
                    innovation_orientation=row['innovation_orientation'],
                    market_aggressiveness=row['market_aggressiveness'],
                    risk_tolerance=row['risk_tolerance'],
                    planning_orientation=row['planning_orientation']
                ).classify_strategy().value,
                axis=1
            )
            
            prospector_data = data[data['ms_strategy'] == MilesSnowStrategy.PROSPECTOR.value]
            defender_data = data[data['ms_strategy'] == MilesSnowStrategy.DEFENDER.value]
            
            if len(prospector_data) > 0:
                prosp_corr = prospector_data[['environment_uncertainty', 'performance']].corr().iloc[0, 1]
                
                fit_analysis['miles_snow_fit'] = {
                    'prospector_uncertainty_performance_corr': float(prosp_corr),
                    'interpretation': ('Positive correlation supports Miles & Snow: '
                                     'Prospectors excel in uncertain environments')
                }
        
        self.analysis_results['strategy_environment_fit'] = fit_analysis
        return fit_analysis
    
    def perform_strategic_group_analysis(self, n_groups: int = 3) -> Dict[str, Any]:
        """
        戦略グループ分析
        
        Identifies strategic groups using cluster analysis on strategic dimensions.
        """
        if self.framework not in ['porter', 'both']:
            return {'error': 'Strategic group analysis requires Porter framework'}
        
        data = pd.DataFrame([p.to_dict() for p in self.firm_profiles])
        
        # Porter dimensions
        X = data[['cost_position', 'differentiation', 'market_scope']].values
        
        # Standardize
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # K-means clustering
        kmeans = KMeans(n_clusters=n_groups, random_state=42, n_init=10)
        groups = kmeans.fit_predict(X_scaled)
        
        data['strategic_group'] = groups
        
        # Characterize each group
        group_profiles = []
        for i in range(n_groups):
            group_data = data[data['strategic_group'] == i]
            
            profile = {
                'group_id': i,
                'n_firms': len(group_data),
                'avg_cost_position': float(group_data['cost_position'].mean()),
                'avg_differentiation': float(group_data['differentiation'].mean()),
                'avg_market_scope': float(group_data['market_scope'].mean()),
                'avg_performance': float(group_data['performance'].mean()),
                'dominant_industries': group_data['industry'].value_counts().head(3).to_dict()
            }
            
            # Infer group strategy
            if profile['avg_cost_position'] < 0.4:
                profile['dominant_strategy'] = "コストリーダーシップ志向"
            elif profile['avg_differentiation'] > 0.6:
                profile['dominant_strategy'] = "差別化志向"
            else:
                profile['dominant_strategy'] = "混合戦略"
            
            group_profiles.append(profile)
        
        result = {
            'n_groups': n_groups,
            'group_assignments': groups.tolist(),
            'group_profiles': group_profiles
        }
        
        self.analysis_results['strategic_groups'] = result
        return result
    
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """包括的分析報告書の生成"""
        if not self.analysis_results:
            raise ValueError("No analysis results available. Run analysis methods first.")
        
        report = {
            'metadata': {
                'n_firms': len(self.firm_profiles),
                'framework': self.framework,
                'analysis_date': pd.Timestamp.now().isoformat()
            },
            'analyses': self.analysis_results,
            'executive_summary': self._generate_executive_summary()
        }
        
        return report
    
    def _generate_executive_summary(self) -> str:
        """エグゼクティブ・サマリーの生成"""
        summary = "## 競争戦略分析：エグゼクティブ・サマリー\n\n"
        
        if 'strategy_classifications' in self.analysis_results:
            classif = self.analysis_results['strategy_classifications']
            n_firms = len(classif['classifications'])
            summary += f"分析対象：{n_firms}企業\n\n"
            
            if 'porter' in classif['distributions']:
                summary += "### Porter戦略類型の分布\n"
                for strategy, count in classif['distributions']['porter'].items():
                    pct = (count / n_firms) * 100
                    summary += f"- {strategy}: {count}社 ({pct:.1f}%)\n"
                summary += "\n"
        
        if 'strategy_performance' in self.analysis_results:
            perf = self.analysis_results['strategy_performance']
            if perf.get('coherence_performance'):
                corr = perf['coherence_performance']['correlation']
                summary += f"### 戦略的一貫性とパフォーマンス\n"
                summary += f"相関係数: {corr:.3f}\n"
                summary += perf['coherence_performance']['interpretation'] + "\n\n"
        
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
    python competitive_strategy_analyzer.py \\
        --data strategy_data.csv \\
        --framework porter \\
        --output results/strategy_analysis.json
    """
    parser = argparse.ArgumentParser(
        description="Competitive Strategy Analyzer: 競争戦略の理論駆動型分析",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--data', type=str, required=True,
                       help='Strategy data file (CSV)')
    parser.add_argument('--framework', type=str, default='porter',
                       choices=['porter', 'miles_snow', 'both'],
                       help='Theoretical framework to use')
    parser.add_argument('--output', type=str, required=True,
                       help='Output file path (JSON)')
    parser.add_argument('--groups', type=int, default=3,
                       help='Number of strategic groups for cluster analysis')
    parser.add_argument('--config', type=str,
                       help='Configuration file (YAML/JSON)')
    
    args = parser.parse_args()
    
    try:
        # Initialize analyzer
        analyzer = CompetitiveStrategyAnalyzer(
            framework=args.framework,
            config_path=args.config
        )
        
        # Load data
        print(f"Loading strategy data with {args.framework} framework...")
        analyzer.load_strategy_data(args.data)
        
        # Run analyses
        print("\nClassifying strategies...")
        analyzer.classify_strategies()
        
        print("Analyzing strategy-performance relationship...")
        analyzer.analyze_strategy_performance_relationship()
        
        print("Analyzing strategy-environment fit...")
        analyzer.analyze_strategy_environment_fit()
        
        if args.framework in ['porter', 'both']:
            print("Performing strategic group analysis...")
            analyzer.perform_strategic_group_analysis(n_groups=args.groups)
        
        # Save results
        analyzer.save_results(args.output)
        
        print("\n" + "="*70)
        print("Competitive Strategy Analysis Complete")
        print("="*70)
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
