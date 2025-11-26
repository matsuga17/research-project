#!/usr/bin/env python3
"""
Causal Inference Explorer for Strategic & Organizational Research

因果推論の哲学的・方法論的基盤に基づく探索的分析システム。
Pearl (2009)の因果階層、Rubin (1974)の潜在結果枠組み、
そして準実験的デザインの現代的手法を統合する。

Epistemological Foundation:
相関は因果を意味しない。しかし、適切な方法論と理論的洞察により、
観察データから因果的洞察を抽出することは可能である。
本スクリプトは、この知的冒険への道筋を提供する。

Usage:
    python causal_explorer.py <data_file> \\
        --treatment "innovation_investment" \\
        --outcome "firm_performance" \\
        --controls "firm_size,industry_dummies" \\
        --methods "ols,iv,psm,did" \\
        -o <output_dir>

Author: Strategic Research Lab
License: MIT
Version: 1.0.0
"""

import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
import json
import argparse
import os
import warnings
warnings.filterwarnings('ignore')

try:
    from sklearn.linear_model import LinearRegression
    from sklearn.neighbors import NearestNeighbors
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class CausalExplorer:
    """因果関係を探索的に分析するクラス"""
    
    def __init__(self, data_path, treatment_vars, outcome_vars, control_vars=None,
                 methods=None, iv_instruments=None, psm_caliper=0.1, output_dir="./output"):
        """
        Parameters:
        -----------
        data_path : str
            データファイルのパス
        treatment_vars : str or list
            処置変数（独立変数）
        outcome_vars : str or list
            結果変数（従属変数）
        control_vars : str or list, optional
            統制変数
        methods : str or list, optional
            分析手法 ("ols", "iv", "psm", "did")
        iv_instruments : str or list, optional
            操作変数（IVに使用）
        psm_caliper : float
            傾向スコアマッチングのキャリパー幅
        output_dir : str
            出力ディレクトリ
        """
        self.data_path = data_path
        self.treatment_vars = self._parse_vars(treatment_vars)
        self.outcome_vars = self._parse_vars(outcome_vars)
        self.control_vars = self._parse_vars(control_vars) if control_vars else []
        self.methods = self._parse_vars(methods) if methods else ["ols"]
        self.iv_instruments = self._parse_vars(iv_instruments) if iv_instruments else []
        self.psm_caliper = psm_caliper
        self.output_dir = output_dir
        
        # データ読み込み
        self.df = self._load_data()
        
        # 結果格納
        self.results = {
            "metadata": {
                "treatment_variables": self.treatment_vars,
                "outcome_variables": self.outcome_vars,
                "control_variables": self.control_vars,
                "methods": self.methods,
                "sample_size": len(self.df)
            },
            "ols_results": {},
            "iv_results": {},
            "psm_results": {},
            "did_results": {},
            "endogeneity_tests": {},
            "robustness_checks": {},
            "causal_interpretations": []
        }
    
    def _parse_vars(self, vars_input):
        """変数リストのパース"""
        if isinstance(vars_input, str):
            return [v.strip() for v in vars_input.split(',')]
        elif isinstance(vars_input, list):
            return vars_input
        else:
            return []
    
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
    
    def perform_ols_analysis(self):
        """OLS回帰分析：基本的な関係性の探索"""
        print("📊 Performing OLS regression analysis...")
        
        for treatment in self.treatment_vars:
            for outcome in self.outcome_vars:
                if treatment not in self.df.columns or outcome not in self.df.columns:
                    continue
                
                # データ準備
                analysis_df = self.df[[treatment, outcome] + self.control_vars].dropna()
                
                if len(analysis_df) < 30:
                    continue
                
                # モデル1：統制変数なし
                X1 = sm.add_constant(analysis_df[treatment])
                y = analysis_df[outcome]
                
                model1 = sm.OLS(y, X1).fit()
                
                # モデル2：統制変数あり
                if self.control_vars:
                    X2 = sm.add_constant(analysis_df[[treatment] + self.control_vars])
                    model2 = sm.OLS(y, X2).fit()
                else:
                    model2 = model1
                
                # 残差診断
                residuals = model2.resid
                normality_stat, normality_p = stats.shapiro(residuals) if len(residuals) < 5000 else (np.nan, np.nan)
                
                # Breusch-Pagan検定（等分散性）
                from statsmodels.stats.diagnostic import het_breuschpagan
                bp_stat, bp_p, _, _ = het_breuschpagan(model2.resid, model2.model.exog)
                
                # 結果の格納
                result_key = f"{treatment}_to_{outcome}"
                self.results["ols_results"][result_key] = {
                    "model1_no_controls": {
                        "coefficient": float(model1.params[treatment]),
                        "std_error": float(model1.bse[treatment]),
                        "t_statistic": float(model1.tvalues[treatment]),
                        "p_value": float(model1.pvalues[treatment]),
                        "r_squared": float(model1.rsquared),
                        "adj_r_squared": float(model1.rsquared_adj),
                        "n_obs": int(model1.nobs)
                    },
                    "model2_with_controls": {
                        "coefficient": float(model2.params[treatment]),
                        "std_error": float(model2.bse[treatment]),
                        "t_statistic": float(model2.tvalues[treatment]),
                        "p_value": float(model2.pvalues[treatment]),
                        "r_squared": float(model2.rsquared),
                        "adj_r_squared": float(model2.rsquared_adj),
                        "n_obs": int(model2.nobs),
                        "f_statistic": float(model2.fvalue),
                        "f_pvalue": float(model2.f_pvalue)
                    },
                    "diagnostics": {
                        "residual_normality_pvalue": float(normality_p) if not np.isnan(normality_p) else None,
                        "heteroscedasticity_bp_pvalue": float(bp_p),
                        "durbin_watson": float(sm.stats.stattools.durbin_watson(residuals))
                    },
                    "interpretation": self._interpret_ols(model2, treatment)
                }
    
    def _interpret_ols(self, model, treatment):
        """OLS結果の解釈"""
        coef = model.params[treatment]
        pval = model.pvalues[treatment]
        
        interpretations = []
        
        # 統計的有意性
        if pval < 0.001:
            interpretations.append(f"Highly significant effect (p < 0.001)")
        elif pval < 0.01:
            interpretations.append(f"Significant effect (p < 0.01)")
        elif pval < 0.05:
            interpretations.append(f"Significant effect (p < 0.05)")
        else:
            interpretations.append(f"No significant effect (p = {pval:.3f})")
        
        # 方向性
        if coef > 0:
            interpretations.append("Positive relationship")
        else:
            interpretations.append("Negative relationship")
        
        # 注意事項
        interpretations.append("⚠️ Correlation does not imply causation. Consider endogeneity.")
        
        return interpretations
    
    def test_endogeneity(self):
        """内生性の診断：Durbin-Wu-Hausman検定"""
        print("🔍 Testing for endogeneity...")
        
        if not self.iv_instruments or "iv" not in self.methods:
            self.results["endogeneity_tests"]["status"] = "no_instruments_specified"
            return
        
        for treatment in self.treatment_vars:
            for outcome in self.outcome_vars:
                if treatment not in self.df.columns or outcome not in self.df.columns:
                    continue
                
                # 第1段階：操作変数で処置変数を回帰
                valid_instruments = [iv for iv in self.iv_instruments if iv in self.df.columns]
                if not valid_instruments:
                    continue
                
                analysis_df = self.df[[treatment, outcome] + self.control_vars + valid_instruments].dropna()
                
                if len(analysis_df) < 50:
                    continue
                
                # 第1段階の回帰
                X_stage1 = sm.add_constant(analysis_df[valid_instruments + self.control_vars])
                y_stage1 = analysis_df[treatment]
                
                stage1_model = sm.OLS(y_stage1, X_stage1).fit()
                residuals_stage1 = stage1_model.resid
                
                # 弱操作変数検定（第1段階のF統計量）
                f_stat_stage1 = stage1_model.fvalue
                
                # 第2段階：残差を含めたOLS
                X_stage2 = sm.add_constant(analysis_df[[treatment] + self.control_vars])
                X_stage2_with_resid = X_stage2.copy()
                X_stage2_with_resid['stage1_residuals'] = residuals_stage1
                
                y_stage2 = analysis_df[outcome]
                
                stage2_model = sm.OLS(y_stage2, X_stage2_with_resid).fit()
                
                # 残差の係数のt検定 → 内生性の検定
                resid_coef = stage2_model.params['stage1_residuals']
                resid_pval = stage2_model.pvalues['stage1_residuals']
                
                result_key = f"{treatment}_to_{outcome}"
                self.results["endogeneity_tests"][result_key] = {
                    "instruments_used": valid_instruments,
                    "first_stage_f_statistic": float(f_stat_stage1),
                    "weak_instrument_concern": bool(f_stat_stage1 < 10),
                    "durbin_wu_hausman": {
                        "residual_coefficient": float(resid_coef),
                        "p_value": float(resid_pval),
                        "endogeneity_detected": bool(resid_pval < 0.05)
                    },
                    "interpretation": self._interpret_endogeneity(f_stat_stage1, resid_pval)
                }
    
    def _interpret_endogeneity(self, f_stat, dwh_p):
        """内生性検定の解釈"""
        interpretations = []
        
        # 弱操作変数
        if f_stat < 10:
            interpretations.append("⚠️ Weak instrument problem (F < 10). IV estimates may be unreliable.")
        else:
            interpretations.append(f"✓ Strong instrument (F = {f_stat:.2f})")
        
        # 内生性
        if dwh_p < 0.05:
            interpretations.append(f"⚠️ Endogeneity detected (p = {dwh_p:.4f}). OLS is inconsistent. Use IV/2SLS.")
        else:
            interpretations.append(f"✓ No endogeneity detected (p = {dwh_p:.4f}). OLS is consistent.")
        
        return interpretations
    
    def perform_iv_analysis(self):
        """操作変数法（IV/2SLS）による因果推論"""
        print("🎯 Performing Instrumental Variables analysis...")
        
        if "iv" not in self.methods or not self.iv_instruments:
            return
        
        for treatment in self.treatment_vars:
            for outcome in self.outcome_vars:
                if treatment not in self.df.columns or outcome not in self.df.columns:
                    continue
                
                valid_instruments = [iv for iv in self.iv_instruments if iv in self.df.columns]
                if not valid_instruments:
                    continue
                
                analysis_df = self.df[[treatment, outcome] + self.control_vars + valid_instruments].dropna()
                
                if len(analysis_df) < 50:
                    continue
                
                # 第1段階：操作変数で処置変数を回帰
                X_stage1 = sm.add_constant(analysis_df[valid_instruments + self.control_vars])
                y_stage1 = analysis_df[treatment]
                
                stage1_model = sm.OLS(y_stage1, X_stage1).fit()
                treatment_hat = stage1_model.predict(X_stage1)
                
                # 第2段階：予測された処置変数で結果変数を回帰
                X_stage2 = sm.add_constant(pd.DataFrame({
                    treatment: treatment_hat,
                    **{col: analysis_df[col] for col in self.control_vars}
                }))
                y_stage2 = analysis_df[outcome]
                
                stage2_model = sm.OLS(y_stage2, X_stage2).fit()
                
                # 標準誤差の調整（2SLS用）
                # 注：正確な2SLSにはlinearmodelsパッケージ推奨
                
                result_key = f"{treatment}_to_{outcome}"
                self.results["iv_results"][result_key] = {
                    "first_stage": {
                        "f_statistic": float(stage1_model.fvalue),
                        "r_squared": float(stage1_model.rsquared),
                        "instrument_strength": "strong" if stage1_model.fvalue > 10 else "weak"
                    },
                    "second_stage": {
                        "coefficient": float(stage2_model.params[treatment]),
                        "std_error": float(stage2_model.bse[treatment]),
                        "t_statistic": float(stage2_model.tvalues[treatment]),
                        "p_value": float(stage2_model.pvalues[treatment])
                    },
                    "interpretation": self._interpret_iv(stage1_model, stage2_model, treatment)
                }
    
    def _interpret_iv(self, stage1_model, stage2_model, treatment):
        """IV推定の解釈"""
        interpretations = []
        
        f_stat = stage1_model.fvalue
        coef = stage2_model.params[treatment]
        pval = stage2_model.pvalues[treatment]
        
        # 第1段階
        if f_stat < 10:
            interpretations.append("⚠️ Weak instrument: IV estimates may be biased")
        else:
            interpretations.append(f"✓ Strong instrument (F = {f_stat:.2f})")
        
        # 第2段階
        if pval < 0.05:
            direction = "positive" if coef > 0 else "negative"
            interpretations.append(f"Significant {direction} causal effect (p = {pval:.4f})")
            interpretations.append(f"LATE (Local Average Treatment Effect) = {coef:.4f}")
        else:
            interpretations.append(f"No significant causal effect (p = {pval:.4f})")
        
        interpretations.append("Note: IV estimates represent local average treatment effect (LATE)")
        
        return interpretations
    
    def perform_psm_analysis(self):
        """傾向スコアマッチング（PSM）による因果推論"""
        print("🎲 Performing Propensity Score Matching...")
        
        if "psm" not in self.methods or not SKLEARN_AVAILABLE:
            return
        
        for treatment in self.treatment_vars:
            for outcome in self.outcome_vars:
                if treatment not in self.df.columns or outcome not in self.df.columns:
                    continue
                
                # 二値処置変数の確認
                if self.df[treatment].nunique() > 2:
                    continue
                
                analysis_df = self.df[[treatment, outcome] + self.control_vars].dropna()
                
                if len(analysis_df) < 50:
                    continue
                
                # 傾向スコアの推定（ロジスティック回帰）
                from sklearn.linear_model import LogisticRegression
                
                X_ps = analysis_df[self.control_vars]
                y_ps = analysis_df[treatment]
                
                ps_model = LogisticRegression(max_iter=1000)
                ps_model.fit(X_ps, y_ps)
                
                propensity_scores = ps_model.predict_proba(X_ps)[:, 1]
                analysis_df['propensity_score'] = propensity_scores
                
                # 処置群と対照群
                treated = analysis_df[analysis_df[treatment] == 1]
                control = analysis_df[analysis_df[treatment] == 0]
                
                # マッチング（最近傍法）
                matches = []
                for idx, row in treated.iterrows():
                    ps_treated = row['propensity_score']
                    
                    # キャリパー内の対照群を検索
                    candidates = control[
                        (control['propensity_score'] >= ps_treated - self.psm_caliper) &
                        (control['propensity_score'] <= ps_treated + self.psm_caliper)
                    ]
                    
                    if len(candidates) > 0:
                        # 最も近い対照を選択
                        distances = np.abs(candidates['propensity_score'] - ps_treated)
                        matched_idx = distances.idxmin()
                        matches.append((idx, matched_idx))
                
                if len(matches) < 10:
                    continue
                
                # ATT（Average Treatment Effect on the Treated）の計算
                treated_outcomes = [treated.loc[t_idx, outcome] for t_idx, _ in matches]
                matched_control_outcomes = [control.loc[c_idx, outcome] for _, c_idx in matches]
                
                att = np.mean(treated_outcomes) - np.mean(matched_control_outcomes)
                att_se = np.sqrt(
                    np.var(treated_outcomes) / len(treated_outcomes) +
                    np.var(matched_control_outcomes) / len(matched_control_outcomes)
                )
                att_tstat = att / att_se
                att_pval = 2 * (1 - stats.norm.cdf(abs(att_tstat)))
                
                # バランステスト
                balance_tests = {}
                for control_var in self.control_vars:
                    treated_mean = treated.loc[[m[0] for m in matches], control_var].mean()
                    control_mean = control.loc[[m[1] for m in matches], control_var].mean()
                    pooled_std = np.sqrt(
                        (treated.loc[[m[0] for m in matches], control_var].var() +
                         control.loc[[m[1] for m in matches], control_var].var()) / 2
                    )
                    std_diff = (treated_mean - control_mean) / pooled_std if pooled_std > 0 else 0
                    
                    balance_tests[control_var] = {
                        "standardized_difference": float(std_diff),
                        "balanced": bool(abs(std_diff) < 0.10)
                    }
                
                result_key = f"{treatment}_to_{outcome}"
                self.results["psm_results"][result_key] = {
                    "n_matches": len(matches),
                    "n_treated": len(treated),
                    "n_control": len(control),
                    "common_support_rate": float(len(matches) / len(treated)),
                    "att": {
                        "estimate": float(att),
                        "std_error": float(att_se),
                        "t_statistic": float(att_tstat),
                        "p_value": float(att_pval)
                    },
                    "balance_tests": balance_tests,
                    "interpretation": self._interpret_psm(att, att_pval, balance_tests, len(matches))
                }
    
    def _interpret_psm(self, att, pval, balance_tests, n_matches):
        """PSM結果の解釈"""
        interpretations = []
        
        # マッチング品質
        if n_matches < 20:
            interpretations.append("⚠️ Limited matches: Results may be unstable")
        else:
            interpretations.append(f"✓ Sufficient matches (n = {n_matches})")
        
        # バランステスト
        unbalanced = [k for k, v in balance_tests.items() if not v["balanced"]]
        if unbalanced:
            interpretations.append(f"⚠️ Covariate imbalance detected: {', '.join(unbalanced)}")
        else:
            interpretations.append("✓ Good covariate balance achieved")
        
        # ATT
        if pval < 0.05:
            direction = "positive" if att > 0 else "negative"
            interpretations.append(f"Significant {direction} treatment effect (ATT = {att:.4f}, p = {pval:.4f})")
        else:
            interpretations.append(f"No significant treatment effect (ATT = {att:.4f}, p = {pval:.4f})")
        
        interpretations.append("Note: PSM assumes selection on observables (no unobserved confounders)")
        
        return interpretations
    
    def perform_did_analysis(self):
        """差分の差分法（DID）による因果推論"""
        print("📈 Performing Difference-in-Differences analysis...")
        
        if "did" not in self.methods:
            return
        
        # DIDには時間変数と処置変数が必要
        required_cols = ["time_period", "treatment_group"]
        if not all(col in self.df.columns for col in required_cols):
            self.results["did_results"]["status"] = "missing_required_columns"
            return
        
        for outcome in self.outcome_vars:
            if outcome not in self.df.columns:
                continue
            
            # 処置前後のデータ
            analysis_df = self.df[["time_period", "treatment_group", outcome] + self.control_vars].dropna()
            
            # DID推定
            # Y = β₀ + β₁*Treat + β₂*Post + β₃*(Treat×Post) + Controls + ε
            analysis_df['post'] = (analysis_df['time_period'] > analysis_df['time_period'].median()).astype(int)
            analysis_df['treat_x_post'] = analysis_df['treatment_group'] * analysis_df['post']
            
            X_did = sm.add_constant(analysis_df[['treatment_group', 'post', 'treat_x_post'] + self.control_vars])
            y_did = analysis_df[outcome]
            
            did_model = sm.OLS(y_did, X_did).fit()
            
            # β₃がDID推定量
            did_estimate = did_model.params['treat_x_post']
            did_se = did_model.bse['treat_x_post']
            did_t = did_model.tvalues['treat_x_post']
            did_p = did_model.pvalues['treat_x_post']
            
            self.results["did_results"][outcome] = {
                "did_estimate": float(did_estimate),
                "std_error": float(did_se),
                "t_statistic": float(did_t),
                "p_value": float(did_p),
                "r_squared": float(did_model.rsquared),
                "interpretation": self._interpret_did(did_estimate, did_p)
            }
    
    def _interpret_did(self, did_est, pval):
        """DID結果の解釈"""
        interpretations = []
        
        if pval < 0.05:
            direction = "positive" if did_est > 0 else "negative"
            interpretations.append(f"Significant {direction} treatment effect (DiD = {did_est:.4f}, p = {pval:.4f})")
        else:
            interpretations.append(f"No significant treatment effect (DiD = {did_est:.4f}, p = {pval:.4f})")
        
        interpretations.append("Note: DiD assumes parallel trends between treatment and control groups")
        interpretations.append("Consider: Placebo tests, event study, dynamic effects")
        
        return interpretations
    
    def generate_causal_interpretations(self):
        """因果的洞察の統合的生成"""
        print("💡 Generating causal interpretations...")
        
        insights = []
        
        # 内生性の評価
        for key, test_result in self.results.get("endogeneity_tests", {}).items():
            if isinstance(test_result, dict) and "durbin_wu_hausman" in test_result:
                if test_result["durbin_wu_hausman"]["endogeneity_detected"]:
                    insights.append({
                        "type": "endogeneity_warning",
                        "relationship": key,
                        "message": f"Endogeneity detected for {key}. OLS estimates are biased. IV or experimental design recommended.",
                        "severity": "high"
                    })
        
        # 手法間の一貫性
        for treatment in self.treatment_vars:
            for outcome in self.outcome_vars:
                result_key = f"{treatment}_to_{outcome}"
                
                ols_sig = self.results.get("ols_results", {}).get(result_key, {}).get("model2_with_controls", {}).get("p_value", 1) < 0.05
                iv_sig = self.results.get("iv_results", {}).get(result_key, {}).get("second_stage", {}).get("p_value", 1) < 0.05
                psm_sig = self.results.get("psm_results", {}).get(result_key, {}).get("att", {}).get("p_value", 1) < 0.05
                
                consistency = sum([ols_sig, iv_sig, psm_sig])
                
                if consistency >= 2:
                    insights.append({
                        "type": "consistent_evidence",
                        "relationship": result_key,
                        "message": f"Consistent evidence across multiple methods for {result_key}",
                        "severity": "informative"
                    })
                elif consistency == 1:
                    insights.append({
                        "type": "mixed_evidence",
                        "relationship": result_key,
                        "message": f"Mixed evidence across methods for {result_key}. Interpret with caution.",
                        "severity": "medium"
                    })
        
        self.results["causal_interpretations"] = insights
    
    def run_complete_analysis(self):
        """完全な因果推論パイプラインの実行"""
        print("🚀 Starting Causal Inference Exploration...")
        
        # 分析の実行
        if "ols" in self.methods:
            self.perform_ols_analysis()
        
        self.test_endogeneity()
        
        if "iv" in self.methods:
            self.perform_iv_analysis()
        
        if "psm" in self.methods:
            self.perform_psm_analysis()
        
        if "did" in self.methods:
            self.perform_did_analysis()
        
        self.generate_causal_interpretations()
        
        # 結果の保存
        os.makedirs(self.output_dir, exist_ok=True)
        output_path = os.path.join(self.output_dir, "causal_inference_results.json")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Causal analysis complete! Results saved to: {output_path}")
        print(f"📊 Methods applied: {', '.join(self.methods)}")
        print(f"💡 Insights generated: {len(self.results['causal_interpretations'])}")
        
        return self.results


def main():
    parser = argparse.ArgumentParser(
        description="Causal Inference Explorer for Strategic Research",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("data_file", help="Path to data file")
    parser.add_argument("--treatment", "--treatment-vars", dest="treatment_vars", required=True,
                       help="Comma-separated treatment variables")
    parser.add_argument("--outcome", "--outcome-vars", dest="outcome_vars", required=True,
                       help="Comma-separated outcome variables")
    parser.add_argument("--controls", "--control-vars", dest="control_vars",
                       help="Comma-separated control variables")
    parser.add_argument("--methods", default="ols",
                       help="Analysis methods: ols,iv,psm,did")
    parser.add_argument("--iv-instruments", dest="iv_instruments",
                       help="Comma-separated instrumental variables")
    parser.add_argument("--psm-caliper", type=float, default=0.1,
                       help="Caliper width for PSM (default: 0.1)")
    parser.add_argument("-o", "--output", default="./output",
                       help="Output directory")
    
    args = parser.parse_args()
    
    # 分析の実行
    explorer = CausalExplorer(
        data_path=args.data_file,
        treatment_vars=args.treatment_vars,
        outcome_vars=args.outcome_vars,
        control_vars=args.control_vars,
        methods=args.methods,
        iv_instruments=args.iv_instruments,
        psm_caliper=args.psm_caliper,
        output_dir=args.output
    )
    
    explorer.run_complete_analysis()


if __name__ == "__main__":
    main()
