#!/usr/bin/env python3
"""
Construct Validation System for Strategic & Organizational Research

測定理論の認識論的基盤に基づく構成概念の包括的検証システム。
Churchill (1979), Nunnally & Bernstein (1994), Fornell & Larcker (1981)の
古典的測定論を実装し、現代的なCFA手法と統合する。

Philosophical Foundation:
測定とは、理論的概念を経験的世界に接続する知的営為である。
その妥当性は、単なる統計的基準を超えて、理論的意味の真正性に関わる。

Usage:
    python construct_validator.py <data_file> \\
        --constructs-config <config.yaml> \\
        --validation-level "comprehensive" \\
        --cfa-method "ml" \\
        -o <output_dir>

Author: Strategic Research Lab
License: MIT
Version: 1.0.0
"""

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler
import json
import argparse
import os
import warnings
import yaml
warnings.filterwarnings('ignore')

try:
    import semopy
    SEMOPY_AVAILABLE = True
except ImportError:
    SEMOPY_AVAILABLE = False
    print("⚠️  semopy not available. CFA analysis will be limited.")


class ConstructValidator:
    """構成概念の測定品質を包括的に検証するクラス"""
    
    def __init__(self, data_path, constructs_config, validation_level="comprehensive",
                 cfa_method="ml", output_dir="./output"):
        """
        Parameters:
        -----------
        data_path : str
            データファイルのパス
        constructs_config : str or dict
            構成概念の設定（YAMLファイルまたは辞書）
        validation_level : str
            検証レベル ("basic", "standard", "comprehensive")
        cfa_method : str
            確認的因子分析の推定法 ("ml", "gls", "wls")
        output_dir : str
            出力ディレクトリ
        """
        self.data_path = data_path
        self.validation_level = validation_level
        self.cfa_method = cfa_method
        self.output_dir = output_dir
        
        # 構成概念設定の読み込み
        if isinstance(constructs_config, str):
            with open(constructs_config, 'r', encoding='utf-8') as f:
                self.constructs_config = yaml.safe_load(f)
        else:
            self.constructs_config = constructs_config
        
        # データ読み込み
        self.df = self._load_data()
        
        # 結果格納
        self.results = {
            "metadata": {
                "validation_level": validation_level,
                "cfa_method": cfa_method,
                "sample_size": len(self.df),
                "n_constructs": len(self.constructs_config.get("constructs", {}))
            },
            "reliability": {},
            "convergent_validity": {},
            "discriminant_validity": {},
            "predictive_validity": {},
            "cfa_results": {},
            "overall_assessment": {}
        }
    
    def _load_data(self):
        """データファイルの読み込み"""
        ext = os.path.splitext(self.data_path)[1].lower()
        
        if ext == '.csv':
            return pd.read_csv(self.data_path)
        elif ext in ['.xlsx', '.xls']:
            return pd.read_excel(self.data_path)
        elif ext == '.dta':
            return pd.read_stata(self.data_path)
        elif ext == '.sav':
            return pd.read_spss(self.data_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
    
    def assess_reliability(self):
        """信頼性分析：内的整合性の評価"""
        print("🔒 Assessing reliability (internal consistency)...")
        
        constructs = self.constructs_config.get("constructs", {})
        
        for construct_name, construct_info in constructs.items():
            items = construct_info.get("items", [])
            
            if not items:
                continue
            
            # 項目データの取得
            item_data = self.df[items].dropna()
            
            if len(item_data) < 10:
                self.results["reliability"][construct_name] = {
                    "status": "insufficient_data",
                    "n_valid": len(item_data)
                }
                continue
            
            # Cronbach's α の計算
            cronbach_alpha = self._calculate_cronbach_alpha(item_data)
            
            # 項目間相関
            item_correlations = item_data.corr()
            avg_inter_item_corr = (item_correlations.sum().sum() - len(items)) / (len(items) * (len(items) - 1))
            
            # 項目削除時のα
            alpha_if_deleted = {}
            for item in items:
                temp_items = [i for i in items if i != item]
                alpha_if_deleted[item] = float(self._calculate_cronbach_alpha(item_data[temp_items]))
            
            # 項目-合計相関
            item_total_correlations = {}
            total_score = item_data.sum(axis=1)
            for item in items:
                corrected_total = total_score - item_data[item]
                corr, _ = stats.pearsonr(item_data[item], corrected_total)
                item_total_correlations[item] = float(corr)
            
            # 複合信頼性（Composite Reliability）の計算
            composite_reliability = self._calculate_composite_reliability(item_data)
            
            # 結果の格納
            self.results["reliability"][construct_name] = {
                "cronbach_alpha": float(cronbach_alpha),
                "composite_reliability": float(composite_reliability),
                "n_items": len(items),
                "n_valid_responses": len(item_data),
                "avg_inter_item_correlation": float(avg_inter_item_corr),
                "item_total_correlations": item_total_correlations,
                "alpha_if_item_deleted": alpha_if_deleted,
                "interpretation": self._interpret_reliability(cronbach_alpha, composite_reliability),
                "problematic_items": self._identify_problematic_items(item_total_correlations, alpha_if_deleted, cronbach_alpha)
            }
    
    def _calculate_cronbach_alpha(self, data):
        """Cronbach's α の計算"""
        n_items = len(data.columns)
        if n_items < 2:
            return np.nan
        
        item_variances = data.var(axis=0, ddof=1)
        total_variance = data.sum(axis=1).var(ddof=1)
        
        alpha = (n_items / (n_items - 1)) * (1 - item_variances.sum() / total_variance)
        return alpha
    
    def _calculate_composite_reliability(self, data):
        """複合信頼性（Composite Reliability）の計算"""
        # 簡易版：標準化負荷量の平均的近似
        n_items = len(data.columns)
        avg_corr = data.corr().values[np.triu_indices_from(data.corr().values, k=1)].mean()
        
        cr = (n_items * avg_corr) / (1 + (n_items - 1) * avg_corr)
        return cr
    
    def _interpret_reliability(self, alpha, cr):
        """信頼性指標の解釈"""
        interpretations = []
        
        # Cronbach's α の評価
        if alpha >= 0.90:
            interpretations.append("Excellent internal consistency (α ≥ 0.90)")
        elif alpha >= 0.80:
            interpretations.append("Good internal consistency (α ≥ 0.80)")
        elif alpha >= 0.70:
            interpretations.append("Acceptable internal consistency (α ≥ 0.70)")
        elif alpha >= 0.60:
            interpretations.append("Questionable internal consistency (α ≥ 0.60). Consider item revision.")
        else:
            interpretations.append("Poor internal consistency (α < 0.60). Significant revision needed.")
        
        # CR の評価
        if cr >= 0.70:
            interpretations.append("Adequate composite reliability (CR ≥ 0.70)")
        else:
            interpretations.append("Low composite reliability (CR < 0.70). May indicate heterogeneity.")
        
        return interpretations
    
    def _identify_problematic_items(self, item_total_corr, alpha_if_deleted, current_alpha):
        """問題のある項目の特定"""
        problematic = []
        
        for item, corr in item_total_corr.items():
            if corr < 0.30:
                problematic.append({
                    "item": item,
                    "issue": "low_item_total_correlation",
                    "value": corr,
                    "recommendation": "Consider removing: weak contribution to scale"
                })
            
            if alpha_if_deleted[item] > current_alpha + 0.05:
                problematic.append({
                    "item": item,
                    "issue": "alpha_increases_if_deleted",
                    "alpha_gain": alpha_if_deleted[item] - current_alpha,
                    "recommendation": "Consider removing: may improve scale reliability"
                })
        
        return problematic
    
    def assess_convergent_validity(self):
        """収束的妥当性：構成概念内の項目の収束"""
        print("🎯 Assessing convergent validity...")
        
        constructs = self.constructs_config.get("constructs", {})
        
        for construct_name, construct_info in constructs.items():
            items = construct_info.get("items", [])
            
            if not items:
                continue
            
            item_data = self.df[items].dropna()
            
            if len(item_data) < 10:
                continue
            
            # 因子負荷量の平均（簡易版）
            corr_matrix = item_data.corr()
            avg_factor_loading = np.sqrt(corr_matrix.values[np.triu_indices_from(corr_matrix.values, k=1)].mean())
            
            # AVE（Average Variance Extracted）の計算（簡易版）
            ave = avg_factor_loading ** 2
            
            # 結果の格納
            self.results["convergent_validity"][construct_name] = {
                "average_variance_extracted": float(ave),
                "avg_factor_loading_proxy": float(avg_factor_loading),
                "interpretation": self._interpret_convergent_validity(ave, avg_factor_loading)
            }
    
    def _interpret_convergent_validity(self, ave, avg_loading):
        """収束的妥当性の解釈"""
        interpretations = []
        
        if ave >= 0.50:
            interpretations.append("Good convergent validity (AVE ≥ 0.50)")
        else:
            interpretations.append(f"Weak convergent validity (AVE = {ave:.3f} < 0.50). Items may not converge well.")
        
        if avg_loading >= 0.70:
            interpretations.append("Strong item loadings (λ̄ ≥ 0.70)")
        elif avg_loading >= 0.50:
            interpretations.append("Acceptable item loadings (λ̄ ≥ 0.50)")
        else:
            interpretations.append("Weak item loadings (λ̄ < 0.50). Consider item revision.")
        
        return interpretations
    
    def assess_discriminant_validity(self):
        """弁別的妥当性：構成概念間の区別"""
        print("🔍 Assessing discriminant validity...")
        
        constructs = self.constructs_config.get("constructs", {})
        
        # 各構成概念の平均スコアを計算
        construct_scores = {}
        construct_aves = {}
        
        for construct_name, construct_info in constructs.items():
            items = construct_info.get("items", [])
            if not items:
                continue
            
            item_data = self.df[items].dropna()
            if len(item_data) < 10:
                continue
            
            construct_scores[construct_name] = item_data.mean(axis=1)
            
            # AVEの取得（すでに計算済み）
            ave = self.results["convergent_validity"].get(construct_name, {}).get("average_variance_extracted", 0)
            construct_aves[construct_name] = ave
        
        if len(construct_scores) < 2:
            self.results["discriminant_validity"]["status"] = "insufficient_constructs"
            return
        
        # 構成概念間の相関行列
        corr_df = pd.DataFrame(construct_scores)
        inter_construct_corr = corr_df.corr()
        
        # Fornell-Larcker基準の検証
        fornell_larcker_results = {}
        for i, construct1 in enumerate(inter_construct_corr.columns):
            for j, construct2 in enumerate(inter_construct_corr.columns):
                if i >= j:
                    continue
                
                corr_value = inter_construct_corr.loc[construct1, construct2]
                ave1 = construct_aves.get(construct1, 0)
                ave2 = construct_aves.get(construct2, 0)
                
                sqrt_ave1 = np.sqrt(ave1)
                sqrt_ave2 = np.sqrt(ave2)
                
                fl_satisfied = (abs(corr_value) < sqrt_ave1) and (abs(corr_value) < sqrt_ave2)
                
                fornell_larcker_results[f"{construct1}_vs_{construct2}"] = {
                    "correlation": float(corr_value),
                    "sqrt_ave_construct1": float(sqrt_ave1),
                    "sqrt_ave_construct2": float(sqrt_ave2),
                    "fornell_larcker_satisfied": bool(fl_satisfied),
                    "concern_level": "high" if abs(corr_value) > 0.85 else "moderate" if abs(corr_value) > 0.70 else "low"
                }
        
        # HTMT（Heterotrait-Monotrait Ratio）の計算（簡易版）
        htmt_results = {}
        for i, construct1 in enumerate(constructs.keys()):
            for j, construct2 in enumerate(constructs.keys()):
                if i >= j:
                    continue
                
                items1 = constructs[construct1].get("items", [])
                items2 = constructs[construct2].get("items", [])
                
                if not items1 or not items2:
                    continue
                
                # 異質特性間相関の平均
                hetero_corr = []
                for item1 in items1:
                    for item2 in items2:
                        if item1 in self.df.columns and item2 in self.df.columns:
                            corr, _ = stats.pearsonr(self.df[item1].dropna(), self.df[item2].dropna())
                            hetero_corr.append(abs(corr))
                
                # 同質特性内相関の平均
                mono_corr1 = []
                for i1 in range(len(items1)):
                    for i2 in range(i1+1, len(items1)):
                        if items1[i1] in self.df.columns and items1[i2] in self.df.columns:
                            corr, _ = stats.pearsonr(self.df[items1[i1]].dropna(), self.df[items1[i2]].dropna())
                            mono_corr1.append(abs(corr))
                
                mono_corr2 = []
                for i1 in range(len(items2)):
                    for i2 in range(i1+1, len(items2)):
                        if items2[i1] in self.df.columns and items2[i2] in self.df.columns:
                            corr, _ = stats.pearsonr(self.df[items2[i1]].dropna(), self.df[items2[i2]].dropna())
                            mono_corr2.append(abs(corr))
                
                if hetero_corr and mono_corr1 and mono_corr2:
                    avg_hetero = np.mean(hetero_corr)
                    avg_mono = np.sqrt(np.mean(mono_corr1) * np.mean(mono_corr2))
                    htmt = avg_hetero / avg_mono if avg_mono > 0 else np.nan
                    
                    htmt_results[f"{construct1}_vs_{construct2}"] = {
                        "htmt_ratio": float(htmt),
                        "threshold_0.85": bool(htmt < 0.85),
                        "threshold_0.90": bool(htmt < 0.90),
                        "interpretation": "good" if htmt < 0.85 else "acceptable" if htmt < 0.90 else "problematic"
                    }
        
        self.results["discriminant_validity"] = {
            "inter_construct_correlations": inter_construct_corr.to_dict(),
            "fornell_larcker_criterion": fornell_larcker_results,
            "htmt_ratios": htmt_results,
            "overall_discriminant_validity": self._assess_overall_discriminant_validity(fornell_larcker_results, htmt_results)
        }
    
    def _assess_overall_discriminant_validity(self, fl_results, htmt_results):
        """弁別的妥当性の総合評価"""
        concerns = []
        
        # Fornell-Larcker基準の違反
        fl_violations = [k for k, v in fl_results.items() if not v["fornell_larcker_satisfied"]]
        if fl_violations:
            concerns.append(f"Fornell-Larcker criterion violated for: {', '.join(fl_violations)}")
        
        # HTMT基準の違反
        htmt_violations = [k for k, v in htmt_results.items() if v["interpretation"] == "problematic"]
        if htmt_violations:
            concerns.append(f"HTMT ratio exceeds 0.90 for: {', '.join(htmt_violations)}")
        
        if not concerns:
            return {"status": "good", "concerns": []}
        else:
            return {"status": "problematic", "concerns": concerns}
    
    def assess_predictive_validity(self):
        """予測的妥当性：理論的結果変数との関連"""
        print("🔮 Assessing predictive validity...")
        
        constructs = self.constructs_config.get("constructs", {})
        criterion_vars = self.constructs_config.get("criterion_variables", [])
        
        if not criterion_vars:
            self.results["predictive_validity"]["status"] = "no_criterion_variables_specified"
            return
        
        for construct_name, construct_info in constructs.items():
            items = construct_info.get("items", [])
            if not items:
                continue
            
            construct_score = self.df[items].mean(axis=1)
            
            construct_predictive = {}
            for criterion in criterion_vars:
                if criterion not in self.df.columns:
                    continue
                
                criterion_data = self.df[criterion].dropna()
                
                # 相関分析
                valid_indices = construct_score.dropna().index.intersection(criterion_data.index)
                if len(valid_indices) < 10:
                    continue
                
                corr, p_value = stats.pearsonr(construct_score[valid_indices], criterion_data[valid_indices])
                
                construct_predictive[criterion] = {
                    "correlation": float(corr),
                    "p_value": float(p_value),
                    "significant": bool(p_value < 0.05),
                    "effect_size": self._interpret_effect_size(abs(corr))
                }
            
            self.results["predictive_validity"][construct_name] = construct_predictive
    
    def _interpret_effect_size(self, abs_corr):
        """効果サイズの解釈"""
        if abs_corr < 0.1:
            return "negligible"
        elif abs_corr < 0.3:
            return "small"
        elif abs_corr < 0.5:
            return "medium"
        else:
            return "large"
    
    def perform_cfa(self):
        """確認的因子分析（CFA）"""
        if not SEMOPY_AVAILABLE:
            self.results["cfa_results"]["status"] = "semopy_not_available"
            print("⚠️  Skipping CFA: semopy package not installed")
            return
        
        print("📐 Performing Confirmatory Factor Analysis...")
        
        constructs = self.constructs_config.get("constructs", {})
        
        # モデル記述の生成
        model_desc = []
        for construct_name, construct_info in constructs.items():
            items = construct_info.get("items", [])
            if items:
                model_desc.append(f"{construct_name} =~ " + " + ".join(items))
        
        if not model_desc:
            self.results["cfa_results"]["status"] = "no_constructs_to_analyze"
            return
        
        model_specification = "\n".join(model_desc)
        
        try:
            # CFAモデルの推定
            from semopy import Model
            
            # 必要な変数のみ抽出
            all_items = []
            for construct_info in constructs.values():
                all_items.extend(construct_info.get("items", []))
            
            cfa_data = self.df[all_items].dropna()
            
            if len(cfa_data) < 50:
                self.results["cfa_results"]["status"] = "insufficient_sample_for_cfa"
                return
            
            model = Model(model_specification)
            model.fit(cfa_data)
            
            # 適合度指標の取得
            fit_indices = {
                "chi_square": float(model.mx_fit.fun),
                "df": int(model.mx_fit.df),
                "chi_square_df_ratio": float(model.mx_fit.fun / model.mx_fit.df) if model.mx_fit.df > 0 else np.nan,
                "n_parameters": int(model.mx_fit.n_params),
                "n_observations": len(cfa_data)
            }
            
            # CFI, TLI, RMSEA等の計算（簡易版）
            # 注：semopyのバージョンによって利用可能な指標が異なる
            
            self.results["cfa_results"] = {
                "model_specification": model_specification,
                "fit_indices": fit_indices,
                "parameter_estimates": model.inspect().to_dict() if hasattr(model, 'inspect') else {},
                "interpretation": self._interpret_cfa_fit(fit_indices)
            }
            
        except Exception as e:
            self.results["cfa_results"] = {
                "status": "cfa_failed",
                "error": str(e)
            }
            print(f"⚠️  CFA failed: {str(e)}")
    
    def _interpret_cfa_fit(self, fit_indices):
        """CFA適合度の解釈"""
        interpretations = []
        
        chi_df_ratio = fit_indices.get("chi_square_df_ratio", np.nan)
        if not np.isnan(chi_df_ratio):
            if chi_df_ratio < 2.0:
                interpretations.append("Excellent model fit (χ²/df < 2.0)")
            elif chi_df_ratio < 3.0:
                interpretations.append("Good model fit (χ²/df < 3.0)")
            elif chi_df_ratio < 5.0:
                interpretations.append("Acceptable model fit (χ²/df < 5.0)")
            else:
                interpretations.append("Poor model fit (χ²/df ≥ 5.0). Model revision recommended.")
        
        return interpretations
    
    def generate_overall_assessment(self):
        """総合的な測定品質評価"""
        print("📋 Generating overall measurement quality assessment...")
        
        # 各側面の評価を集約
        reliability_issues = []
        validity_issues = []
        recommendations = []
        
        # 信頼性の評価
        for construct, rel_info in self.results.get("reliability", {}).items():
            alpha = rel_info.get("cronbach_alpha", 0)
            if alpha < 0.70:
                reliability_issues.append(f"{construct}: Low Cronbach's α ({alpha:.3f})")
                recommendations.append(f"Consider revising items for {construct} to improve internal consistency")
        
        # 収束的妥当性の評価
        for construct, cv_info in self.results.get("convergent_validity", {}).items():
            ave = cv_info.get("average_variance_extracted", 0)
            if ave < 0.50:
                validity_issues.append(f"{construct}: Low AVE ({ave:.3f})")
                recommendations.append(f"Review items for {construct} to enhance convergence")
        
        # 弁別的妥当性の評価
        dv_assessment = self.results.get("discriminant_validity", {}).get("overall_discriminant_validity", {})
        if dv_assessment.get("status") == "problematic":
            validity_issues.extend(dv_assessment.get("concerns", []))
            recommendations.append("Consider theoretical distinction between constructs with high inter-correlations")
        
        # 総合評価
        overall_status = "excellent" if not (reliability_issues or validity_issues) else \
                        "good" if len(reliability_issues) + len(validity_issues) <= 2 else \
                        "needs_improvement"
        
        self.results["overall_assessment"] = {
            "measurement_quality_status": overall_status,
            "reliability_issues": reliability_issues,
            "validity_issues": validity_issues,
            "recommendations": recommendations,
            "summary": self._generate_summary()
        }
    
    def _generate_summary(self):
        """測定品質の要約"""
        n_constructs = len(self.results.get("reliability", {}))
        
        avg_alpha = np.mean([v.get("cronbach_alpha", 0) for v in self.results.get("reliability", {}).values()])
        avg_ave = np.mean([v.get("average_variance_extracted", 0) for v in self.results.get("convergent_validity", {}).values()])
        
        return {
            "n_constructs_analyzed": n_constructs,
            "average_cronbach_alpha": float(avg_alpha),
            "average_ave": float(avg_ave),
            "sample_size": self.results["metadata"]["sample_size"]
        }
    
    def run_complete_validation(self):
        """完全な検証パイプラインの実行"""
        print("🚀 Starting Comprehensive Construct Validation...")
        
        # 検証レベルに応じた分析
        self.assess_reliability()
        self.assess_convergent_validity()
        
        if self.validation_level in ["standard", "comprehensive"]:
            self.assess_discriminant_validity()
            self.assess_predictive_validity()
        
        if self.validation_level == "comprehensive":
            self.perform_cfa()
        
        self.generate_overall_assessment()
        
        # 結果の保存
        os.makedirs(self.output_dir, exist_ok=True)
        output_path = os.path.join(self.output_dir, "construct_validation.json")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Validation complete! Results saved to: {output_path}")
        print(f"📊 Key findings:")
        print(f"   - Constructs validated: {self.results['metadata']['n_constructs']}")
        print(f"   - Overall quality: {self.results['overall_assessment']['measurement_quality_status']}")
        print(f"   - Issues identified: {len(self.results['overall_assessment']['reliability_issues']) + len(self.results['overall_assessment']['validity_issues'])}")
        
        return self.results


def main():
    parser = argparse.ArgumentParser(
        description="Construct Validation System for Strategic Research",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("data_file", help="Path to data file")
    parser.add_argument("--constructs-config", required=True,
                       help="Path to constructs configuration YAML file")
    parser.add_argument("--validation-level", default="comprehensive",
                       choices=["basic", "standard", "comprehensive"],
                       help="Level of validation analysis")
    parser.add_argument("--cfa-method", default="ml",
                       choices=["ml", "gls", "wls"],
                       help="CFA estimation method")
    parser.add_argument("-o", "--output", default="./output",
                       help="Output directory")
    
    args = parser.parse_args()
    
    # 検証の実行
    validator = ConstructValidator(
        data_path=args.data_file,
        constructs_config=args.constructs_config,
        validation_level=args.validation_level,
        cfa_method=args.cfa_method,
        output_dir=args.output
    )
    
    validator.run_complete_validation()


if __name__ == "__main__":
    main()
