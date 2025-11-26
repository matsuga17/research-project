"""
US Corporate Analytics - ガバナンス分析モジュール

このモジュールは企業のコーポレートガバナンス体制を分析します。
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import re
from datetime import datetime


class GovernanceAnalyzer:
    """ガバナンス分析クラス"""
    
    def __init__(self, sec_client):
        """
        初期化
        
        Parameters:
            sec_client: SECEdgarClient インスタンス
        """
        self.sec_client = sec_client
        self.governance_data = {}
        
    def analyze_board_composition(self, cik: str, year: int) -> Dict[str, Any]:
        """
        取締役会構成を分析
        
        Parameters:
            cik: CIKコード
            year: 分析年度
            
        Returns:
            取締役会分析結果の辞書
        """
        # DEF 14Aから取締役情報を抽出
        # 実際の実装では、DEF 14AのHTMLをパースして取締役情報を抽出
        
        # ダミーデータ（実装例）
        board_data = {
            'total_directors': 0,
            'independent_directors': 0,
            'independent_ratio': 0.0,
            'average_age': 0,
            'female_directors': 0,
            'gender_diversity_ratio': 0.0,
            'board_committees': [],
            'audit_committee_independence': True,
            'compensation_committee_independence': True,
            'analysis_year': year
        }
        
        try:
            # DEF 14Aの取得
            filings = self.sec_client.get_filing_urls(
                cik, "DEF 14A",
                start_date=f"{year}-01-01",
                end_date=f"{year}-12-31"
            )
            
            if filings:
                # 実際の実装では、ファイルをダウンロードしてパース
                # ここではプレースホルダー
                board_data['filing_date'] = filings[0]['filing_date']
                board_data['filing_url'] = filings[0]['url']
                
        except Exception as e:
            print(f"Error analyzing board composition: {e}")
        
        return board_data
    
    def analyze_executive_compensation(self, cik: str, year: int) -> pd.DataFrame:
        """
        役員報酬を分析
        
        Parameters:
            cik: CIKコード
            year: 分析年度
            
        Returns:
            役員報酬データのDataFrame
        """
        # DEF 14Aから役員報酬表を抽出
        
        # ダミーデータ（実装例）
        compensation_data = pd.DataFrame({
            'executive_name': [],
            'position': [],
            'base_salary': [],
            'bonus': [],
            'stock_awards': [],
            'option_awards': [],
            'non_equity_incentive': [],
            'other_compensation': [],
            'total_compensation': []
        })
        
        try:
            # DEF 14Aの取得と解析
            filings = self.sec_client.get_filing_urls(
                cik, "DEF 14A",
                start_date=f"{year}-01-01",
                end_date=f"{year}-12-31"
            )
            
            if filings:
                # 実際の実装では、Summary Compensation Tableを抽出
                pass
                
        except Exception as e:
            print(f"Error analyzing executive compensation: {e}")
        
        return compensation_data
    
    def calculate_pay_for_performance(self, 
                                     compensation_data: pd.DataFrame,
                                     performance_data: pd.DataFrame) -> Dict[str, float]:
        """
        Pay-for-Performance分析
        
        Parameters:
            compensation_data: 役員報酬データ
            performance_data: 業績データ（ROA、ROE等）
            
        Returns:
            分析結果の辞書
        """
        if compensation_data.empty or performance_data.empty:
            return {}
        
        # CEOの報酬を抽出
        ceo_comp = compensation_data[
            compensation_data['position'].str.contains('CEO|Chief Executive', 
                                                       case=False, 
                                                       na=False)
        ]
        
        if ceo_comp.empty:
            return {}
        
        results = {}
        
        # CEO報酬と業績の相関
        if 'total_compensation' in ceo_comp.columns:
            ceo_total = ceo_comp['total_compensation'].iloc[0]
            
            # ROAとの相関
            if 'ROA' in performance_data.columns:
                roa = performance_data['ROA'].mean()
                results['compensation_to_roa_ratio'] = ceo_total / (roa + 0.001)
            
            # ROEとの相関
            if 'ROE' in performance_data.columns:
                roe = performance_data['ROE'].mean()
                results['compensation_to_roe_ratio'] = ceo_total / (roe + 0.001)
            
            results['ceo_total_compensation'] = ceo_total
        
        return results
    
    def analyze_ownership_structure(self, cik: str) -> Dict[str, Any]:
        """
        株主構造を分析
        
        Parameters:
            cik: CIKコード
            
        Returns:
            株主構造分析結果の辞書
        """
        # Form 4（内部者取引）とForm 13F（機関投資家保有）から分析
        
        ownership_data = {
            'insider_ownership_pct': 0.0,
            'institutional_ownership_pct': 0.0,
            'top5_shareholders': [],
            'ownership_concentration_hhi': 0.0,
            'recent_insider_transactions': []
        }
        
        try:
            # Form 4の取得
            from datetime import datetime, timedelta
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
            
            form4_filings = self.sec_client.get_filing_urls(
                cik, "4",
                start_date=start_date,
                end_date=end_date
            )
            
            ownership_data['insider_transactions_count'] = len(form4_filings)
            
        except Exception as e:
            print(f"Error analyzing ownership structure: {e}")
        
        return ownership_data
    
    def calculate_governance_score(self, 
                                  board_data: Dict,
                                  compensation_data: pd.DataFrame,
                                  ownership_data: Dict) -> Dict[str, Any]:
        """
        ガバナンススコアを計算
        
        Parameters:
            board_data: 取締役会データ
            compensation_data: 役員報酬データ
            ownership_data: 株主構造データ
            
        Returns:
            ガバナンススコアの辞書
        """
        score = 0
        max_score = 100
        
        components = {}
        
        # 取締役会の独立性（30点）
        if board_data.get('independent_ratio', 0) >= 0.75:
            components['board_independence'] = 30
        elif board_data.get('independent_ratio', 0) >= 0.50:
            components['board_independence'] = 20
        else:
            components['board_independence'] = 10
        
        # 取締役会の多様性（20点）
        diversity_score = 0
        if board_data.get('gender_diversity_ratio', 0) >= 0.30:
            diversity_score += 10
        elif board_data.get('gender_diversity_ratio', 0) >= 0.20:
            diversity_score += 5
        
        # 年齢多様性（簡易版）
        if 30 <= board_data.get('average_age', 0) <= 65:
            diversity_score += 10
        
        components['board_diversity'] = diversity_score
        
        # 委員会の独立性（20点）
        committee_score = 0
        if board_data.get('audit_committee_independence', False):
            committee_score += 10
        if board_data.get('compensation_committee_independence', False):
            committee_score += 10
        
        components['committee_independence'] = committee_score
        
        # 株主構造（15点）
        ownership_score = 0
        institutional = ownership_data.get('institutional_ownership_pct', 0)
        if 40 <= institutional <= 70:  # 適度な機関投資家保有
            ownership_score = 15
        elif institutional > 70:
            ownership_score = 10
        else:
            ownership_score = 5
        
        components['ownership_structure'] = ownership_score
        
        # 報酬の透明性（15点）
        if not compensation_data.empty and 'total_compensation' in compensation_data.columns:
            # データが利用可能
            components['compensation_transparency'] = 15
        else:
            components['compensation_transparency'] = 5
        
        # 合計スコア
        total_score = sum(components.values())
        
        # 評価
        if total_score >= 85:
            rating = "Excellent"
        elif total_score >= 70:
            rating = "Good"
        elif total_score >= 50:
            rating = "Fair"
        else:
            rating = "Poor"
        
        return {
            'total_score': total_score,
            'max_score': max_score,
            'rating': rating,
            'components': components
        }
    
    def generate_governance_report(self,
                                  cik: str,
                                  ticker: str,
                                  year: int) -> str:
        """
        ガバナンスレポートを生成
        
        Parameters:
            cik: CIKコード
            ticker: ティッカーシンボル
            year: 分析年度
            
        Returns:
            レポート文字列
        """
        # データ収集
        board_data = self.analyze_board_composition(cik, year)
        compensation_data = self.analyze_executive_compensation(cik, year)
        ownership_data = self.analyze_ownership_structure(cik)
        
        # スコア計算
        governance_score = self.calculate_governance_score(
            board_data,
            compensation_data,
            ownership_data
        )
        
        # レポート生成
        report = f"""
{'='*70}
コーポレートガバナンス分析レポート
{'='*70}

企業情報
--------
ティッカー: {ticker}
CIK: {cik}
分析年度: {year}

総合評価
--------
ガバナンススコア: {governance_score['total_score']}/{governance_score['max_score']}
評価: {governance_score['rating']}

スコア内訳
----------
"""
        
        for component, score in governance_score['components'].items():
            report += f"{component}: {score}点\n"
        
        report += f"""

取締役会構成
------------
取締役総数: {board_data.get('total_directors', 'N/A')}
独立取締役: {board_data.get('independent_directors', 'N/A')}
独立取締役比率: {board_data.get('independent_ratio', 0):.1%}
平均年齢: {board_data.get('average_age', 'N/A')}歳
女性取締役: {board_data.get('female_directors', 'N/A')}名
性別多様性: {board_data.get('gender_diversity_ratio', 0):.1%}

"""
        
        if not compensation_data.empty:
            report += """
役員報酬サマリー
----------------
"""
            for idx, row in compensation_data.iterrows():
                report += f"{row.get('executive_name', 'N/A')} ({row.get('position', 'N/A')})\n"
                report += f"  総報酬: ${row.get('total_compensation', 0):,.0f}\n"
        
        report += f"""

株主構造
--------
内部者保有: {ownership_data.get('insider_ownership_pct', 0):.1f}%
機関投資家保有: {ownership_data.get('institutional_ownership_pct', 0):.1f}%
内部者取引件数（過去1年）: {ownership_data.get('insider_transactions_count', 0)}件

{'='*70}
"""
        
        return report
    
    def export_governance_data(self, output_path: str) -> None:
        """
        ガバナンスデータをエクスポート
        
        Parameters:
            output_path: 出力ファイルパス
        """
        if not self.governance_data:
            print("No governance data to export")
            return
        
        # DataFrameに変換してエクスポート
        df = pd.DataFrame([self.governance_data])
        df.to_csv(output_path, index=False)
        print(f"Governance data exported to {output_path}")


def test_governance_analyzer():
    """テスト関数"""
    from utils.sec_client import SECEdgarClient
    import yaml
    
    # 設定読み込み
    with open('../config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # SEC クライアント初期化
    sec_client = SECEdgarClient(
        api_key=config['sec_edgar']['api_key'],
        user_agent=config['sec_edgar']['user_agent']
    )
    
    # ガバナンス分析
    analyzer = GovernanceAnalyzer(sec_client)
    
    cik = sec_client.get_company_cik("AAPL")
    print(f"Analyzing governance for AAPL (CIK: {cik})...")
    
    # レポート生成
    report = analyzer.generate_governance_report(cik, "AAPL", 2023)
    print(report)


if __name__ == "__main__":
    test_governance_analyzer()
