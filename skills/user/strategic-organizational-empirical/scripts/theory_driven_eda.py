#!/usr/bin/env python3
"""
Theory-Driven Exploratory Data Analysis for Strategic & Organizational Research

理論的枠組みに基づく探索的データ分析エンジン。
戦略・組織論の主要理論（RBV、Dynamic Capabilities、Institutional Theory等）を
データ分析に統合し、理論的予測と実証的発見の対話を促進する。

Philosophy:
データは理論の言語で語られるべきであり、理論はデータによって試練を受けるべきである。
本スクリプトは、この弁証法的プロセスを実装する。

Usage:
    python theory_driven_eda.py <data_file> \\
        --theory-framework "Dynamic_Capabilities" \\
        --constructs "sensing,seizing,reconfiguring" \\
        --outcome-vars "roa,tobin_q" \\
        --contextual-factors "industry,firm_age" \\
        -o <output_dir>

Author: Strategic Research Lab
License: MIT
Version: 1.0.0
"""

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.decomposition import FactorAnalysis
from sklearn.preprocessing import StandardScaler
import json
import argparse
import os
import warnings
warnings.filterwarnings('ignore')

# 理論的枠組みのカタログ（主要な戦略・組織論理論）
THEORY_FRAMEWORKS = {
    "RBV": {
        "full_name": "Resource-Based View",
        "key_constructs": ["valuable", "rare", "inimitable", "organized"],
        "theoretical_predictions": {
            "performance_relationship": "positive",
            "moderation": "competitive_intensity"
        },
        "foundational_papers": [
            "Barney, J. (1991). Firm resources and sustained competitive advantage. JOM."
        ]
    },
    "Dynamic_Capabilities": {
        "full_name": "Dynamic Capabilities Theory",
        "key_constructs": ["sensing", "seizing", "reconfiguring"],
        "theoretical_predictions": {
            "performance_relationship": "positive",
            "moderation": "environmental_dynamism"
        },
        "foundational_papers": [
            "Teece, D. J., Pisano, G., & Shuen, A. (1997). Dynamic capabilities. SMJ.",
            "Teece, D. J. (2007). Explicating dynamic capabilities. SMJ."
        ]
    },
    "Institutional_Theory": {
        "full_name": "Institutional Theory",
        "key_constructs": ["regulative", "normative", "cultural_cognitive"],
        "theoretical_predictions": {
            "isomorphism": "coercive,mimetic,normative",
            "legitimacy": "survival_advantage"
        },
        "foundational_papers": [
            "DiMaggio, P. J., & Powell, W. W. (1983). The iron cage revisited. ASR."
        ]
    },
    "Transaction_Cost_Economics": {
        "full_name": "Transaction Cost Economics",
        "key_constructs": ["asset_specificity", "uncertainty", "frequency"],
        "theoretical_predictions": {
            "governance_choice": "hierarchy_vs_market"
        },
        "foundational_papers": [
            "Williamson, O. E. (1985). The economic institutions of capitalism."
        ]
    }
}


class TheoryDrivenEDA:
    """理論駆動型探索的データ分析クラス"""
    
    def __init__(self, data_path, theory_framework, constructs, outcome_vars, 
                 contextual_factors=None, output_dir="./output"):
        """
        Parameters:
        -----------
        data_path : str
            データファイルのパス
        theory_framework : str
            理論的枠組み（例："Dynamic_Capabilities"）
        constructs : list
            分析対象の構成概念リスト
        outcome_vars : list
            結果変数リスト
        contextual_factors : list, optional
            文脈要因（産業、企業規模等）
        output_dir : str
            出力ディレクトリ
        """
        self.data_path = data_path
        self.theory_framework = theory_framework
        self.constructs = constructs if isinstance(constructs, list) else constructs.split(',')
        self.outcome_vars = outcome_vars if isinstance(outcome_vars, list) else outcome_vars.split(',')
        self.contextual_factors = contextual_factors.split(',') if isinstance(contextual_factors, str) else contextual_factors or []
        self.output_dir = output_dir
        
        # データ読み込み
        self.df = self._load_data()
        
        # 理論情報の取得
        self.theory_info = THEORY_FRAMEWORKS.get(theory_framework, {})
        
        # 結果格納
        self.results = {
            "metadata": {
                "theory_framework": theory_framework,
                "theory_full_name": self.theory_info.get("full_name", ""),
                "constructs_analyzed": self.constructs,
                "outcome_variables": self.outcome_vars,
                "contextual_factors": self.contextual_factors,
                "sample_size": len(self.df),
                "foundational_papers": self.theory_info.get("foundational_papers", [])
            },
            "descriptive_statistics": {},
            "construct_correlations": {},
            "contextual_analysis": {},
            "exploratory_factor_analysis": {},
            "theoretical_consistency": {},
            "data_quality": {},
            "theoretical_insights": []
        }
    
    def _load_data(self):
        """データファイルの読み込み（複数形式対応）"""
        ext = os.path.splitext(self.data_path)[1].lower()
        
        if ext == '.csv':
            return pd.read_csv(self.data_path)
        elif ext in ['.xlsx', '.xls']:
            return pd.read_excel(self.data_path)
        elif ext == '.dta':
            return pd.read_stata(self.data_path)
        elif ext == '.sav':
            return pd.read_spss(self.data_path)
        elif ext == '.json':
            return pd.read_json(self.data_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
    
    def analyze_descriptive_statistics(self):
        """構成概念の記述統計分析"""
        print("📊 Analyzing descriptive statistics for theoretical constructs...")
        
        for construct in self.constructs:
            # 構成概念に関連する列を検索
            construct_cols = [col for col in self.df.columns if construct.lower() in col.lower()]
            
            if not construct_cols:
                continue
            
            construct_data = self.df[construct_cols]
            
            # 記述統計
            desc_stats = {
                "mean": float(construct_data.mean().mean()),
                "std": float(construct_data.std().mean()),
                "min": float(construct_data.min().min()),
                "max": float(construct_data.max().max()),
                "skewness": float(stats.skew(construct_data.values.flatten(), nan_policy='omit')),
                "kurtosis": float(stats.kurtosis(construct_data.values.flatten(), nan_policy='omit')),
                "n_items": len(construct_cols),
                "missing_rate": float(construct_data.isnull().sum().sum() / (len(self.df) * len(construct_cols)))
            }
            
            # 正規性検定
            if len(construct_data.dropna()) > 3:
                try:
                    shapiro_stat, shapiro_p = stats.shapiro(construct_data.mean(axis=1).dropna())
                    desc_stats["normality_test"] = {
                        "test": "Shapiro-Wilk",
                        "statistic": float(shapiro_stat),
                        "p_value": float(shapiro_p),
                        "interpretation": "normal" if shapiro_p > 0.05 else "non-normal"
                    }
                except:
                    desc_stats["normality_test"] = {"status": "failed"}
            
            self.results["descriptive_statistics"][construct] = desc_stats
    
    def analyze_construct_correlations(self):
        """構成概念間の相関分析"""
        print("🔗 Analyzing inter-construct correlations...")
        
        construct_means = {}
        for construct in self.constructs:
            construct_cols = [col for col in self.df.columns if construct.lower() in col.lower()]
            if construct_cols:
                construct_means[construct] = self.df[construct_cols].mean(axis=1)
        
        if len(construct_means) > 1:
            # Pearson相関
            corr_matrix = pd.DataFrame(construct_means).corr()
            self.results["construct_correlations"]["pearson"] = corr_matrix.to_dict()
            
            # Spearman相関（頑健性確認）
            spearman_corr = pd.DataFrame(construct_means).corr(method='spearman')
            self.results["construct_correlations"]["spearman"] = spearman_corr.to_dict()
    
    def analyze_contextual_factors(self):
        """文脈要因による層別分析"""
        if not self.contextual_factors:
            return
        
        print("🌍 Analyzing contextual variations...")
        
        for factor in self.contextual_factors:
            if factor not in self.df.columns:
                continue
            
            # 各構成概念について文脈要因別の分析
            factor_analysis = {}
            for construct in self.constructs:
                construct_cols = [col for col in self.df.columns if construct.lower() in col.lower()]
                if not construct_cols:
                    continue
                
                construct_mean = self.df[construct_cols].mean(axis=1)
                grouped = self.df.groupby(factor)[construct_cols].mean()
                
                factor_analysis[construct] = {
                    "by_group": grouped.mean(axis=1).to_dict(),
                    "f_statistic": None,
                    "p_value": None
                }
                
                # ANOVA（群間差の検定）
                try:
                    groups = [self.df[construct_cols].loc[self.df[factor] == g].mean(axis=1).dropna() 
                             for g in self.df[factor].unique()]
                    if len(groups) > 1 and all(len(g) > 0 for g in groups):
                        f_stat, p_val = stats.f_oneway(*groups)
                        factor_analysis[construct]["f_statistic"] = float(f_stat)
                        factor_analysis[construct]["p_value"] = float(p_val)
                except:
                    pass
            
            self.results["contextual_analysis"][factor] = factor_analysis
    
    def exploratory_factor_analysis(self):
        """探索的因子分析（EFA）"""
        print("🔍 Conducting exploratory factor analysis...")
        
        # 全構成概念項目を収集
        all_items = []
        for construct in self.constructs:
            construct_cols = [col for col in self.df.columns if construct.lower() in col.lower()]
            all_items.extend(construct_cols)
        
        if len(all_items) < 3:
            self.results["exploratory_factor_analysis"]["status"] = "insufficient_items"
            return
        
        # データ準備
        efa_data = self.df[all_items].dropna()
        
        if len(efa_data) < 50:
            self.results["exploratory_factor_analysis"]["status"] = "insufficient_sample"
            return
        
        try:
            # 標準化
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(efa_data)
            
            # 因子数の決定（構成概念数を目安）
            n_factors = len(self.constructs)
            
            # Factor Analysis実行
            fa = FactorAnalysis(n_components=n_factors, random_state=42)
            fa.fit(scaled_data)
            
            # 因子負荷量
            loadings = pd.DataFrame(
                fa.components_.T,
                columns=[f"Factor{i+1}" for i in range(n_factors)],
                index=all_items
            )
            
            self.results["exploratory_factor_analysis"] = {
                "n_factors": n_factors,
                "factor_loadings": loadings.to_dict(),
                "explained_variance": float(np.sum(fa.explained_variance_ratio_)),
                "status": "completed"
            }
        except Exception as e:
            self.results["exploratory_factor_analysis"]["status"] = f"failed: {str(e)}"
    
    def assess_theoretical_consistency(self):
        """理論的予測との整合性評価"""
        print("🎯 Assessing theoretical consistency...")
        
        # 理論的予測の取得
        predictions = self.theory_info.get("theoretical_predictions", {})
        
        # 構成概念とアウトカムの関係性チェック
        if "performance_relationship" in predictions:
            predicted_direction = predictions["performance_relationship"]
            
            for construct in self.constructs:
                construct_cols = [col for col in self.df.columns if construct.lower() in col.lower()]
                if not construct_cols:
                    continue
                
                construct_mean = self.df[construct_cols].mean(axis=1)
                
                for outcome in self.outcome_vars:
                    if outcome not in self.df.columns:
                        continue
                    
                    try:
                        # 相関分析
                        valid_data = pd.DataFrame({
                            'construct': construct_mean,
                            'outcome': self.df[outcome]
                        }).dropna()
                        
                        if len(valid_data) > 3:
                            corr, p_value = stats.pearsonr(valid_data['construct'], valid_data['outcome'])
                            
                            consistency = {
                                "correlation": float(corr),
                                "p_value": float(p_value),
                                "predicted_direction": predicted_direction,
                                "observed_direction": "positive" if corr > 0 else "negative",
                                "consistent": (predicted_direction == "positive" and corr > 0) or 
                                            (predicted_direction == "negative" and corr < 0)
                            }
                            
                            self.results["theoretical_consistency"][f"{construct}_{outcome}"] = consistency
                    except:
                        pass
    
    def evaluate_data_quality(self):
        """データ品質の評価"""
        print("✅ Evaluating data quality...")
        
        quality_metrics = {
            "total_observations": len(self.df),
            "total_variables": len(self.df.columns),
            "missing_data_rate": float(self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns))),
            "duplicate_rows": int(self.df.duplicated().sum()),
            "construct_specific": {}
        }
        
        for construct in self.constructs:
            construct_cols = [col for col in self.df.columns if construct.lower() in col.lower()]
            if not construct_cols:
                continue
            
            construct_data = self.df[construct_cols]
            
            quality_metrics["construct_specific"][construct] = {
                "n_items": len(construct_cols),
                "missing_rate": float(construct_data.isnull().sum().sum() / (len(self.df) * len(construct_cols))),
                "response_variance": float(construct_data.std().mean())
            }
        
        self.results["data_quality"] = quality_metrics
    
    def generate_insights(self):
        """理論的洞察の自動生成"""
        print("💡 Generating theoretical insights...")
        
        insights = []
        
        # サンプルサイズの評価
        if len(self.df) < 100:
            insights.append({
                "type": "sample_size",
                "severity": "warning",
                "message": f"Sample size (n={len(self.df)}) is below recommended threshold (n≥100). "
                          "Statistical power may be limited. Consider using non-parametric methods."
            })
        
        # 欠損データの評価
        missing_rate = self.results["data_quality"]["missing_data_rate"]
        if missing_rate > 0.05:
            insights.append({
                "type": "missing_data",
                "severity": "warning" if missing_rate < 0.10 else "critical",
                "message": f"Missing data rate ({missing_rate:.1%}) exceeds acceptable threshold (5%). "
                          "Multiple imputation or FIML methods recommended."
            })
        
        # 理論的整合性の評価
        for key, consistency in self.results["theoretical_consistency"].items():
            if not consistency.get("consistent", False) and consistency.get("p_value", 1) < 0.05:
                insights.append({
                    "type": "theoretical_inconsistency",
                    "severity": "attention",
                    "message": f"{key}: Observed relationship contradicts theoretical prediction. "
                              f"Expected {consistency['predicted_direction']}, observed {consistency['observed_direction']}. "
                              f"Consider alternative theoretical explanations or measurement issues."
                })
        
        # 強い相関の検出
        if "pearson" in self.results["construct_correlations"]:
            corr_matrix = pd.DataFrame(self.results["construct_correlations"]["pearson"])
            for i in range(len(corr_matrix)):
                for j in range(i+1, len(corr_matrix)):
                    corr_val = corr_matrix.iloc[i, j]
                    if abs(corr_val) > 0.70:
                        insights.append({
                            "type": "high_correlation",
                            "severity": "info",
                            "message": f"Strong correlation ({corr_val:.2f}) between {corr_matrix.index[i]} and {corr_matrix.columns[j]}. "
                                      f"Consider discriminant validity issues or potential multicollinearity."
                        })
        
        self.results["theoretical_insights"] = insights
    
    def run_complete_analysis(self):
        """完全な理論駆動型分析の実行"""
        print("\n" + "="*70)
        print(f"THEORY-DRIVEN EDA: {self.theory_info.get('full_name', self.theory_framework)}")
        print("="*70 + "\n")
        
        # 出力ディレクトリの作成
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 各分析の実行
        self.analyze_descriptive_statistics()
        self.analyze_construct_correlations()
        self.analyze_contextual_factors()
        self.exploratory_factor_analysis()
        self.assess_theoretical_consistency()
        self.evaluate_data_quality()
        self.generate_insights()
        
        # 結果の保存
        output_file = os.path.join(self.output_dir, "theory_analysis.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print("\n" + "="*70)
        print(f"✅ Analysis complete! Results saved to: {output_file}")
        print("="*70 + "\n")
        
        # 主要な発見事項の要約
        self._print_summary()
    
    def _print_summary(self):
        """分析結果の要約表示"""
        print("\n📋 SUMMARY OF KEY FINDINGS:\n")
        
        # データ品質
        print(f"Sample Size: n = {self.results['data_quality']['total_observations']}")
        print(f"Missing Data Rate: {self.results['data_quality']['missing_data_rate']:.1%}")
        print()
        
        # 構成概念の記述統計
        print("Construct Descriptive Statistics:")
        for construct, stats in self.results["descriptive_statistics"].items():
            print(f"  {construct}: M = {stats['mean']:.2f}, SD = {stats['std']:.2f}, "
                  f"Skewness = {stats['skewness']:.2f}")
        print()
        
        # 理論的整合性
        consistent_count = sum(1 for c in self.results["theoretical_consistency"].values() 
                              if c.get("consistent", False) and c.get("p_value", 1) < 0.05)
        total_count = len(self.results["theoretical_consistency"])
        if total_count > 0:
            print(f"Theoretical Consistency: {consistent_count}/{total_count} relationships consistent with theory")
            print()
        
        # 洞察
        if self.results["theoretical_insights"]:
            print("Key Insights:")
            for insight in self.results["theoretical_insights"][:5]:  # Top 5
                print(f"  [{insight['severity'].upper()}] {insight['message']}")
        
        print()


def main():
    """メインエントリーポイント"""
    parser = argparse.ArgumentParser(
        description="Theory-Driven Exploratory Data Analysis for Strategic Research",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage:
  python theory_driven_eda.py firm_data.csv \\
    --theory-framework "Dynamic_Capabilities" \\
    --constructs "sensing,seizing,reconfiguring" \\
    --outcome-vars "roa,tobin_q" \\
    --contextual-factors "industry,firm_age" \\
    -o ./output

Supported theories:
  - RBV: Resource-Based View
  - Dynamic_Capabilities: Dynamic Capabilities Theory
  - Institutional_Theory: Institutional Theory
  - Transaction_Cost_Economics: Transaction Cost Economics
        """
    )
    
    parser.add_argument("data_file", help="Path to data file")
    parser.add_argument("--theory-framework", required=True, 
                       choices=list(THEORY_FRAMEWORKS.keys()),
                       help="Theoretical framework to apply")
    parser.add_argument("--constructs", required=True,
                       help="Comma-separated list of constructs")
    parser.add_argument("--outcome-vars", required=True,
                       help="Comma-separated list of outcome variables")
    parser.add_argument("--contextual-factors", default=None,
                       help="Comma-separated list of contextual factors")
    parser.add_argument("-o", "--output", default="./output",
                       help="Output directory")
    
    args = parser.parse_args()
    
    # 分析の実行
    analyzer = TheoryDrivenEDA(
        data_path=args.data_file,
        theory_framework=args.theory_framework,
        constructs=args.constructs,
        outcome_vars=args.outcome_vars,
        contextual_factors=args.contextual_factors,
        output_dir=args.output
    )
    
    analyzer.run_complete_analysis()


if __name__ == "__main__":
    main()
