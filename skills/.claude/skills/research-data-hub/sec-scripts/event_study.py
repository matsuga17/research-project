"""
US Corporate Analytics - イベントスタディ分析スクリプト

このスクリプトはM&A、CEO交代等の重要イベントの効果を分析します。
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.sec_client import SECEdgarClient


class EventStudy:
    """イベントスタディ分析クラス"""
    
    def __init__(self, config: Dict):
        """
        初期化
        
        Parameters:
            config: 設定辞書
        """
        self.config = config
        self.sec_client = SECEdgarClient(
            api_key=config['sec_edgar']['api_key'],
            user_agent=config['sec_edgar']['user_agent']
        )
        
        self.events = []
        self.returns = pd.DataFrame()
        self.results = {}
    
    def extract_events_from_8k(self, 
                               tickers: List[str],
                               start_date: str,
                               end_date: str,
                               item_types: Optional[List[str]] = None) -> pd.DataFrame:
        """
        8-Kから重要イベントを抽出
        
        Parameters:
            tickers: ティッカーシンボルのリスト
            start_date: 開始日（YYYY-MM-DD）
            end_date: 終了日（YYYY-MM-DD）
            item_types: Itemタイプのリスト（Noneの場合は全Item）
                例: ["Item 5.02"] (役員の異動)
                    ["Item 2.01"] (重要な資産の取得・処分)
            
        Returns:
            イベントリストのDataFrame
        """
        events = []
        
        for ticker in tickers:
            try:
                print(f"Extracting events for {ticker}...")
                
                cik = self.sec_client.get_company_cik(ticker)
                if not cik:
                    print(f"  CIK not found for {ticker}")
                    continue
                
                # 8-K取得
                filings = self.sec_client.get_filing_urls(
                    cik, "8-K",
                    start_date=start_date,
                    end_date=end_date
                )
                
                for filing in filings:
                    # 実際の実装では、8-KのHTMLをパースしてItemを抽出
                    # ここでは簡略化
                    events.append({
                        'ticker': ticker,
                        'cik': cik,
                        'event_date': filing['filing_date'],
                        'filing_url': filing['url'],
                        'event_type': 'Unknown'  # 実際はパースして判定
                    })
                
                print(f"  Found {len(filings)} 8-K filings")
                
            except Exception as e:
                print(f"  Error: {e}")
        
        events_df = pd.DataFrame(events)
        if not events_df.empty:
            events_df['event_date'] = pd.to_datetime(events_df['event_date'])
            events_df = events_df.sort_values('event_date')
        
        self.events = events_df
        return events_df
    
    def calculate_abnormal_returns(self,
                                   ticker: str,
                                   event_date: str,
                                   event_window: Tuple[int, int] = (-5, 5),
                                   estimation_window: Tuple[int, int] = (-250, -11),
                                   market_return: Optional[pd.Series] = None) -> Dict:
        """
        異常リターン（AR）と累積異常リターン（CAR）を計算
        
        Parameters:
            ticker: ティッカーシンボル
            event_date: イベント日（YYYY-MM-DD）
            event_window: イベントウィンドウ（日数）
            estimation_window: 推定ウィンドウ（日数）
            market_return: 市場リターン（Noneの場合はS&P 500を使用）
            
        Returns:
            分析結果の辞書
        """
        # 注: 実際の実装では株価データ（CRSP等）が必要
        # ここでは疑似データで説明
        
        event_dt = pd.to_datetime(event_date)
        
        # 株価データの取得（疑似）
        # 実際の実装では、CRSPやYahoo Financeから取得
        date_range = pd.date_range(
            start=event_dt + timedelta(days=estimation_window[0]),
            end=event_dt + timedelta(days=event_window[1]),
            freq='D'
        )
        
        np.random.seed(42)
        stock_prices = pd.Series(
            100 * np.exp(np.cumsum(np.random.normal(0.001, 0.02, len(date_range)))),
            index=date_range
        )
        
        # リターンを計算
        stock_returns = stock_prices.pct_change().dropna()
        
        # 市場リターン（疑似）
        if market_return is None:
            market_return = pd.Series(
                np.random.normal(0.0005, 0.01, len(stock_returns)),
                index=stock_returns.index
            )
        
        # 推定期間のデータ
        est_start = event_dt + timedelta(days=estimation_window[0])
        est_end = event_dt + timedelta(days=estimation_window[1])
        
        est_stock_returns = stock_returns[
            (stock_returns.index >= est_start) &
            (stock_returns.index <= est_end)
        ]
        est_market_returns = market_return[
            (market_return.index >= est_start) &
            (market_return.index <= est_end)
        ]
        
        # マーケットモデルの推定（OLS回帰）
        from scipy import stats
        
        # NaNを除外
        valid_idx = est_stock_returns.notna() & est_market_returns.notna()
        est_stock_returns_clean = est_stock_returns[valid_idx]
        est_market_returns_clean = est_market_returns[valid_idx]
        
        if len(est_stock_returns_clean) < 10:
            return {'error': 'Insufficient data for estimation'}
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            est_market_returns_clean,
            est_stock_returns_clean
        )
        
        # イベントウィンドウのデータ
        event_start = event_dt + timedelta(days=event_window[0])
        event_end = event_dt + timedelta(days=event_window[1])
        
        event_stock_returns = stock_returns[
            (stock_returns.index >= event_start) &
            (stock_returns.index <= event_end)
        ]
        event_market_returns = market_return[
            (market_return.index >= event_start) &
            (market_return.index <= event_end)
        ]
        
        # 期待リターンを計算
        expected_returns = intercept + slope * event_market_returns
        
        # 異常リターン（AR）
        abnormal_returns = event_stock_returns - expected_returns
        
        # 累積異常リターン（CAR）
        cumulative_abnormal_returns = abnormal_returns.cumsum()
        
        # 統計的検定
        ar_mean = abnormal_returns.mean()
        ar_std = abnormal_returns.std()
        n = len(abnormal_returns)
        
        t_stat = ar_mean / (ar_std / np.sqrt(n))
        p_value_ar = 2 * (1 - stats.t.cdf(abs(t_stat), df=n-1))
        
        # CAR
        car = cumulative_abnormal_returns.iloc[-1]
        car_std = ar_std * np.sqrt(n)
        car_t_stat = car / car_std
        car_p_value = 2 * (1 - stats.t.cdf(abs(car_t_stat), df=n-1))
        
        return {
            'ticker': ticker,
            'event_date': event_date,
            'event_window': event_window,
            'alpha': intercept,
            'beta': slope,
            'r_squared': r_value**2,
            'abnormal_returns': abnormal_returns.to_dict(),
            'cumulative_abnormal_returns': cumulative_abnormal_returns.to_dict(),
            'average_ar': ar_mean,
            'car': car,
            'ar_t_stat': t_stat,
            'ar_p_value': p_value_ar,
            'car_t_stat': car_t_stat,
            'car_p_value': car_p_value,
            'significant_5pct': car_p_value < 0.05,
            'significant_1pct': car_p_value < 0.01
        }
    
    def aggregate_analysis(self, results_list: List[Dict]) -> Dict:
        """
        複数イベントの集計分析
        
        Parameters:
            results_list: 個別イベント分析結果のリスト
            
        Returns:
            集計分析結果の辞書
        """
        # CARを抽出
        cars = [r['car'] for r in results_list if 'car' in r]
        
        if not cars:
            return {'error': 'No valid CAR data'}
        
        # 集計統計
        avg_car = np.mean(cars)
        median_car = np.median(cars)
        std_car = np.std(cars)
        
        # t検定
        n = len(cars)
        t_stat = avg_car / (std_car / np.sqrt(n))
        
        from scipy import stats
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=n-1))
        
        # 成功率（正のCAR）
        positive_cars = sum(1 for car in cars if car > 0)
        success_rate = positive_cars / n
        
        return {
            'n_events': n,
            'average_car': avg_car,
            'median_car': median_car,
            'std_car': std_car,
            't_statistic': t_stat,
            'p_value': p_value,
            'significant_5pct': p_value < 0.05,
            'significant_1pct': p_value < 0.01,
            'positive_cars': positive_cars,
            'success_rate': success_rate,
            'min_car': min(cars),
            'max_car': max(cars)
        }
    
    def generate_event_study_report(self, 
                                    results_list: List[Dict],
                                    aggregate: Dict) -> str:
        """
        イベントスタディレポートを生成
        
        Parameters:
            results_list: 個別イベント分析結果のリスト
            aggregate: 集計分析結果
            
        Returns:
            レポート文字列
        """
        report = f"""
{'='*70}
イベントスタディ分析レポート
{'='*70}

分析概要
--------
イベント数: {aggregate['n_events']}
イベントウィンドウ: {results_list[0]['event_window']}

集計結果
--------
平均CAR: {aggregate['average_car']:.4f} ({aggregate['average_car']*100:.2f}%)
中央値CAR: {aggregate['median_car']:.4f} ({aggregate['median_car']*100:.2f}%)
標準偏差: {aggregate['std_car']:.4f}

統計的検定
----------
t統計量: {aggregate['t_statistic']:.3f}
p値: {aggregate['p_value']:.4f}
有意性（5%水準）: {'はい' if aggregate['significant_5pct'] else 'いいえ'}
有意性（1%水準）: {'はい' if aggregate['significant_1pct'] else 'いいえ'}

成功率分析
----------
正のCAR件数: {aggregate['positive_cars']}/{aggregate['n_events']}
成功率: {aggregate['success_rate']:.1%}
CAR範囲: [{aggregate['min_car']:.4f}, {aggregate['max_car']:.4f}]

個別イベント詳細
----------------
"""
        
        for i, result in enumerate(results_list[:10], 1):  # 最初の10件
            if 'error' in result:
                report += f"\n{i}. {result.get('ticker', 'Unknown')}: エラー\n"
                continue
            
            report += f"""
{i}. {result['ticker']} - {result['event_date']}
   CAR: {result['car']:.4f} ({result['car']*100:.2f}%)
   p値: {result['car_p_value']:.4f}
   有意: {'***' if result['car_p_value'] < 0.01 else '**' if result['car_p_value'] < 0.05 else '*' if result['car_p_value'] < 0.10 else 'N.S.'}
"""
        
        if len(results_list) > 10:
            report += f"\n... 他{len(results_list) - 10}件のイベント\n"
        
        report += f"\n{'='*70}\n"
        
        return report


def main():
    """メイン実行関数"""
    import yaml
    
    # 設定読み込み
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # イベントスタディ実行例
    print("Event Study Analysis Example")
    print("=" * 70)
    
    # M&Aイベントの分析例
    study = EventStudy(config)
    
    # 8-Kから M&A イベントを抽出
    tickers = ["AAPL", "MSFT", "GOOGL"]
    events_df = study.extract_events_from_8k(
        tickers,
        start_date="2020-01-01",
        end_date="2023-12-31"
    )
    
    print(f"\nExtracted {len(events_df)} events")
    
    # 各イベントを分析（最初の5件のみ）
    results_list = []
    
    for idx, event in events_df.head(5).iterrows():
        print(f"\nAnalyzing event: {event['ticker']} on {event['event_date'].strftime('%Y-%m-%d')}...")
        
        result = study.calculate_abnormal_returns(
            ticker=event['ticker'],
            event_date=event['event_date'].strftime('%Y-%m-%d'),
            event_window=(-5, 5),
            estimation_window=(-250, -11)
        )
        
        results_list.append(result)
        
        if 'car' in result:
            print(f"  CAR: {result['car']:.4f} (p={result['car_p_value']:.4f})")
    
    # 集計分析
    if results_list:
        aggregate = study.aggregate_analysis(results_list)
        
        # レポート生成
        report = study.generate_event_study_report(results_list, aggregate)
        print("\n" + report)
        
        # ファイル保存
        output_dir = "../reports/event_study"
        os.makedirs(output_dir, exist_ok=True)
        
        with open(f"{output_dir}/event_study_report.txt", 'w') as f:
            f.write(report)
        
        print(f"\nReport saved to {output_dir}/event_study_report.txt")


if __name__ == "__main__":
    main()
