"""
Event Study Template for Strategic & Organizational Research
=============================================================

Comprehensive event study methodology for analyzing stock market reactions
to corporate events (M&A, CEO succession, strategic announcements, etc.)

Features:
- Market model abnormal returns
- Cumulative abnormal returns (CAR)
- Statistical significance tests
- Cross-sectional regression
- Visualization

Author: Strategic & Organizational Research Hub
License: Apache 2.0
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
from datetime import datetime, timedelta

# ============================================================================
# Configuration
# ============================================================================

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

EVENT_STUDY_CONFIG = {
    "estimation_window": (-250, -11),  # Days before event
    "event_window": (-10, 10),         # Days around event
    "min_estimation_obs": 100,         # Minimum observations for estimation
    "significance_levels": [0.01, 0.05, 0.10]
}

# ============================================================================
# Data Preparation
# ============================================================================

class EventStudyData:
    """
    Prepare data for event study analysis
    """
    
    def __init__(self, stock_returns: pd.DataFrame, market_returns: pd.DataFrame,
                 event_dates: pd.DataFrame):
        """
        Initialize event study data
        
        Args:
            stock_returns: DataFrame with columns ['date', 'ticker', 'return']
            market_returns: DataFrame with columns ['date', 'market_return']
            event_dates: DataFrame with columns ['ticker', 'event_date']
        """
        self.stock_returns = stock_returns.copy()
        self.market_returns = market_returns.copy()
        self.event_dates = event_dates.copy()
        
        # Ensure date columns are datetime
        self.stock_returns['date'] = pd.to_datetime(self.stock_returns['date'])
        self.market_returns['date'] = pd.to_datetime(self.market_returns['date'])
        self.event_dates['event_date'] = pd.to_datetime(self.event_dates['event_date'])
        
        print("✅ Event study data initialized")
        print(f"   - Firms: {self.stock_returns['ticker'].nunique()}")
        print(f"   - Events: {len(self.event_dates)}")
        print(f"   - Date range: {self.stock_returns['date'].min()} to {self.stock_returns['date'].max()}")
    
    def merge_data(self) -> pd.DataFrame:
        """
        Merge stock returns with market returns
        """
        merged = self.stock_returns.merge(self.market_returns, on='date', how='left')
        
        print(f"\n✅ Data merged: {len(merged)} observations")
        return merged
    
    def create_event_windows(self, data: pd.DataFrame, 
                            estimation_window: Tuple[int, int],
                            event_window: Tuple[int, int]) -> Dict:
        """
        Create estimation and event windows for each event
        
        Args:
            data: Merged stock and market returns
            estimation_window: (start_day, end_day) relative to event
            event_window: (start_day, end_day) relative to event
        
        Returns:
            Dictionary with ticker as key, windows as value
        """
        event_windows = {}
        
        for _, row in self.event_dates.iterrows():
            ticker = row['ticker']
            event_date = row['event_date']
            
            # Filter firm data
            firm_data = data[data['ticker'] == ticker].copy()
            firm_data = firm_data.sort_values('date')
            
            # Find event date index
            event_idx = firm_data[firm_data['date'] == event_date].index
            
            if len(event_idx) == 0:
                print(f"⚠️  Event date not found for {ticker} on {event_date}")
                continue
            
            event_idx = event_idx[0]
            all_dates = firm_data['date'].values
            event_position = np.where(all_dates == event_date)[0]
            
            if len(event_position) == 0:
                continue
            
            event_position = event_position[0]
            
            # Calculate window boundaries
            est_start_idx = max(0, event_position + estimation_window[0])
            est_end_idx = max(0, event_position + estimation_window[1])
            evt_start_idx = max(0, event_position + event_window[0])
            evt_end_idx = min(len(firm_data), event_position + event_window[1] + 1)
            
            event_windows[ticker] = {
                'event_date': event_date,
                'estimation_data': firm_data.iloc[est_start_idx:est_end_idx],
                'event_data': firm_data.iloc[evt_start_idx:evt_end_idx],
                'event_position': event_position
            }
        
        print(f"\n✅ Event windows created for {len(event_windows)} events")
        return event_windows

# ============================================================================
# Market Model Estimation
# ============================================================================

class MarketModel:
    """
    Estimate market model parameters for each firm
    """
    
    @staticmethod
    def estimate_parameters(estimation_data: pd.DataFrame) -> Dict:
        """
        Estimate market model: R_it = α_i + β_i * R_mt + ε_it
        
        Args:
            estimation_data: DataFrame with 'return' and 'market_return'
        
        Returns:
            Dictionary with alpha, beta, and residual variance
        """
        if len(estimation_data) < EVENT_STUDY_CONFIG['min_estimation_obs']:
            return {
                'alpha': np.nan,
                'beta': np.nan,
                'sigma_squared': np.nan,
                'r_squared': np.nan,
                'n_obs': len(estimation_data)
            }
        
        # Prepare data
        y = estimation_data['return'].values
        X = estimation_data['market_return'].values
        X = sm.add_constant(X)
        
        # OLS regression
        model = sm.OLS(y, X, missing='drop')
        results = model.fit()
        
        alpha = results.params[0]
        beta = results.params[1]
        sigma_squared = results.scale  # Residual variance
        r_squared = results.rsquared
        
        return {
            'alpha': alpha,
            'beta': beta,
            'sigma_squared': sigma_squared,
            'r_squared': r_squared,
            'n_obs': len(estimation_data)
        }

# ============================================================================
# Abnormal Returns Calculation
# ============================================================================

class AbnormalReturns:
    """
    Calculate abnormal returns and cumulative abnormal returns
    """
    
    @staticmethod
    def calculate_ar(event_data: pd.DataFrame, alpha: float, beta: float) -> pd.DataFrame:
        """
        Calculate abnormal returns: AR_it = R_it - (α_i + β_i * R_mt)
        
        Args:
            event_data: DataFrame with actual returns and market returns
            alpha: Estimated alpha from market model
            beta: Estimated beta from market model
        
        Returns:
            DataFrame with abnormal returns
        """
        ar_data = event_data.copy()
        
        # Calculate expected returns
        ar_data['expected_return'] = alpha + beta * ar_data['market_return']
        
        # Calculate abnormal returns
        ar_data['abnormal_return'] = ar_data['return'] - ar_data['expected_return']
        
        return ar_data
    
    @staticmethod
    def calculate_car(ar_data: pd.DataFrame, event_window: Tuple[int, int]) -> pd.DataFrame:
        """
        Calculate cumulative abnormal returns (CAR)
        
        Args:
            ar_data: DataFrame with abnormal returns
            event_window: (start, end) days relative to event
        
        Returns:
            DataFrame with CAR
        """
        car_data = ar_data.copy()
        car_data['car'] = car_data['abnormal_return'].cumsum()
        
        return car_data

# ============================================================================
# Statistical Tests
# ============================================================================

class EventStudyTests:
    """
    Statistical significance tests for event study
    """
    
    @staticmethod
    def t_test_ar(ar: float, sigma_squared: float, n_estimation: int) -> Dict:
        """
        t-test for single-day abnormal return
        
        Args:
            ar: Abnormal return
            sigma_squared: Residual variance from estimation
            n_estimation: Number of observations in estimation period
        
        Returns:
            Dictionary with t-statistic and p-value
        """
        # Standard error of AR
        se_ar = np.sqrt(sigma_squared * (1 + 1/n_estimation))
        
        # t-statistic
        t_stat = ar / se_ar
        
        # p-value (two-tailed)
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), n_estimation - 2))
        
        return {
            't_statistic': t_stat,
            'p_value': p_value,
            'se': se_ar
        }
    
    @staticmethod
    def t_test_car(car: float, sigma_squared: float, n_estimation: int, 
                   window_length: int) -> Dict:
        """
        t-test for cumulative abnormal return
        
        Args:
            car: Cumulative abnormal return
            sigma_squared: Residual variance from estimation
            n_estimation: Number of observations in estimation period
            window_length: Length of event window
        
        Returns:
            Dictionary with t-statistic and p-value
        """
        # Standard error of CAR
        se_car = np.sqrt(sigma_squared * window_length * (1 + window_length/n_estimation))
        
        # t-statistic
        t_stat = car / se_car
        
        # p-value (two-tailed)
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), n_estimation - 2))
        
        return {
            't_statistic': t_stat,
            'p_value': p_value,
            'se': se_car
        }
    
    @staticmethod
    def cross_sectional_test(cars: np.ndarray) -> Dict:
        """
        Cross-sectional t-test (average CAR across events)
        
        Args:
            cars: Array of CARs across all events
        
        Returns:
            Dictionary with test results
        """
        mean_car = np.mean(cars)
        std_car = np.std(cars, ddof=1)
        n = len(cars)
        
        se = std_car / np.sqrt(n)
        t_stat = mean_car / se
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), n - 1))
        
        return {
            'mean_car': mean_car,
            'std_car': std_car,
            'n_events': n,
            't_statistic': t_stat,
            'p_value': p_value
        }

# ============================================================================
# Event Study Execution
# ============================================================================

class EventStudy:
    """
    Main event study class
    """
    
    def __init__(self, event_study_data: EventStudyData):
        """
        Initialize event study
        
        Args:
            event_study_data: EventStudyData object
        """
        self.data = event_study_data
        self.results = {}
    
    def run_analysis(self, estimation_window: Tuple[int, int] = None,
                    event_window: Tuple[int, int] = None) -> Dict:
        """
        Run complete event study analysis
        
        Args:
            estimation_window: (start, end) days for parameter estimation
            event_window: (start, end) days for event analysis
        
        Returns:
            Dictionary with results for all events
        """
        if estimation_window is None:
            estimation_window = EVENT_STUDY_CONFIG['estimation_window']
        if event_window is None:
            event_window = EVENT_STUDY_CONFIG['event_window']
        
        print("\n" + "="*70)
        print("RUNNING EVENT STUDY ANALYSIS")
        print("="*70)
        print(f"Estimation window: [{estimation_window[0]}, {estimation_window[1]}] days")
        print(f"Event window: [{event_window[0]}, {event_window[1]}] days")
        
        # 1. Merge data
        merged_data = self.data.merge_data()
        
        # 2. Create event windows
        event_windows = self.data.create_event_windows(merged_data, estimation_window, event_window)
        
        # 3. Analyze each event
        results = {}
        
        for ticker, windows in event_windows.items():
            # Estimate market model
            params = MarketModel.estimate_parameters(windows['estimation_data'])
            
            if np.isnan(params['alpha']):
                print(f"⚠️  Insufficient data for {ticker}")
                continue
            
            # Calculate abnormal returns
            ar_data = AbnormalReturns.calculate_ar(
                windows['event_data'], 
                params['alpha'], 
                params['beta']
            )
            
            # Calculate CAR
            car_data = AbnormalReturns.calculate_car(ar_data, event_window)
            
            # Statistical tests
            final_car = car_data['car'].iloc[-1]
            window_length = len(car_data)
            
            car_test = EventStudyTests.t_test_car(
                final_car, 
                params['sigma_squared'],
                params['n_obs'],
                window_length
            )
            
            results[ticker] = {
                'event_date': windows['event_date'],
                'market_model': params,
                'ar_data': ar_data,
                'car_data': car_data,
                'car': final_car,
                'car_test': car_test
            }
            
            print(f"✅ {ticker}: CAR = {final_car:.4f} (t = {car_test['t_statistic']:.2f}, p = {car_test['p_value']:.4f})")
        
        self.results = results
        
        # 4. Cross-sectional analysis
        all_cars = [r['car'] for r in results.values()]
        cross_sect_test = EventStudyTests.cross_sectional_test(np.array(all_cars))
        
        print("\n" + "="*70)
        print("CROSS-SECTIONAL RESULTS")
        print("="*70)
        print(f"Mean CAR: {cross_sect_test['mean_car']:.4f}")
        print(f"Std Dev: {cross_sect_test['std_car']:.4f}")
        print(f"t-statistic: {cross_sect_test['t_statistic']:.2f}")
        print(f"p-value: {cross_sect_test['p_value']:.4f}")
        
        if cross_sect_test['p_value'] < 0.05:
            print("✅ Significant market reaction detected")
        else:
            print("⚠️  No significant market reaction")
        
        return {
            'individual_results': results,
            'cross_sectional': cross_sect_test
        }

# ============================================================================
# Visualization
# ============================================================================

class EventStudyVisualization:
    """
    Visualize event study results
    """
    
    @staticmethod
    def plot_average_car(results: Dict, save_path: Optional[str] = None):
        """
        Plot average CAR across all events
        """
        # Extract CAR time series for each event
        all_car_series = []
        
        for ticker, result in results['individual_results'].items():
            car_data = result['car_data'].copy()
            car_data['event_time'] = range(len(car_data))
            car_data['ticker'] = ticker
            all_car_series.append(car_data[['event_time', 'car', 'ticker']])
        
        # Combine and calculate average
        combined = pd.concat(all_car_series)
        avg_car = combined.groupby('event_time')['car'].agg(['mean', 'std', 'count']).reset_index()
        avg_car['se'] = avg_car['std'] / np.sqrt(avg_car['count'])
        avg_car['ci_lower'] = avg_car['mean'] - 1.96 * avg_car['se']
        avg_car['ci_upper'] = avg_car['mean'] + 1.96 * avg_car['se']
        
        # Plot
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(avg_car['event_time'], avg_car['mean'], 
               color='blue', linewidth=2, label='Average CAR')
        ax.fill_between(avg_car['event_time'], avg_car['ci_lower'], avg_car['ci_upper'],
                       alpha=0.3, color='blue', label='95% Confidence Interval')
        ax.axhline(y=0, color='red', linestyle='--', alpha=0.5)
        ax.axvline(x=len(avg_car)//2, color='green', linestyle='--', alpha=0.5, label='Event Date')
        
        ax.set_xlabel("Event Time (Days)", fontsize=12)
        ax.set_ylabel("Cumulative Abnormal Return", fontsize=12)
        ax.set_title("Average Cumulative Abnormal Returns", fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ CAR plot saved: {save_path}")
        
        plt.show()
    
    @staticmethod
    def plot_car_distribution(results: Dict, save_path: Optional[str] = None):
        """
        Plot distribution of CARs across events
        """
        cars = [r['car'] for r in results['individual_results'].values()]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.hist(cars, bins=30, edgecolor='black', alpha=0.7, color='steelblue')
        ax.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Zero')
        ax.axvline(x=np.mean(cars), color='green', linestyle='--', linewidth=2, label='Mean CAR')
        
        ax.set_xlabel("Cumulative Abnormal Return", fontsize=12)
        ax.set_ylabel("Frequency", fontsize=12)
        ax.set_title("Distribution of CARs Across Events", fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Distribution plot saved: {save_path}")
        
        plt.show()

# ============================================================================
# Cross-Sectional Regression
# ============================================================================

class CrossSectionalAnalysis:
    """
    Analyze determinants of abnormal returns
    """
    
    @staticmethod
    def run_regression(results: Dict, firm_characteristics: pd.DataFrame) -> sm.regression.linear_model.RegressionResultsWrapper:
        """
        Regress CARs on firm characteristics
        
        Args:
            results: Event study results
            firm_characteristics: DataFrame with firm-level variables
        
        Returns:
            OLS regression results
        """
        # Extract CARs
        cars_df = pd.DataFrame([
            {'ticker': ticker, 'car': result['car']}
            for ticker, result in results['individual_results'].items()
        ])
        
        # Merge with firm characteristics
        analysis_data = cars_df.merge(firm_characteristics, on='ticker', how='left')
        
        # Regression
        y = analysis_data['car']
        X = analysis_data.drop(['ticker', 'car'], axis=1)
        X = sm.add_constant(X)
        
        model = sm.OLS(y, X, missing='drop')
        results = model.fit()
        
        print("\n" + "="*70)
        print("CROSS-SECTIONAL REGRESSION RESULTS")
        print("="*70)
        print(results.summary())
        
        return results

# ============================================================================
# Example Workflow
# ============================================================================

def example_event_study():
    """
    Example workflow for event study
    """
    print("="*70)
    print("EVENT STUDY EXAMPLE: CEO Succession Announcements")
    print("="*70)
    
    # 1. Generate synthetic data
    np.random.seed(42)
    
    # Stock returns
    dates = pd.date_range('2020-01-01', '2023-12-31', freq='D')
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'FB']
    
    stock_data = []
    for ticker in tickers:
        for date in dates:
            stock_data.append({
                'date': date,
                'ticker': ticker,
                'return': np.random.normal(0.001, 0.02)  # Daily return
            })
    
    stock_returns = pd.DataFrame(stock_data)
    
    # Market returns
    market_returns = pd.DataFrame({
        'date': dates,
        'market_return': np.random.normal(0.0008, 0.015, len(dates))
    })
    
    # Event dates (CEO successions)
    event_dates = pd.DataFrame({
        'ticker': tickers,
        'event_date': pd.to_datetime([
            '2022-03-15', '2022-06-20', '2022-09-10', '2022-11-05', '2023-01-25'
        ])
    })
    
    print(f"\n✅ Synthetic data generated")
    print(f"   - Stocks: {len(tickers)}")
    print(f"   - Events: {len(event_dates)}")
    print(f"   - Date range: {dates.min()} to {dates.max()}")
    
    # 2. Initialize event study
    es_data = EventStudyData(stock_returns, market_returns, event_dates)
    
    # 3. Run event study
    es = EventStudy(es_data)
    results = es.run_analysis()
    
    # 4. Visualization
    viz = EventStudyVisualization()
    viz.plot_average_car(results)
    viz.plot_car_distribution(results)
    
    # 5. Export results
    cars_df = pd.DataFrame([
        {
            'ticker': ticker,
            'event_date': result['event_date'],
            'car': result['car'],
            't_statistic': result['car_test']['t_statistic'],
            'p_value': result['car_test']['p_value']
        }
        for ticker, result in results['individual_results'].items()
    ])
    
    cars_df.to_csv('event_study_results.csv', index=False)
    print(f"\n✅ Results exported: event_study_results.csv")
    
    print("\n" + "="*70)
    print("EVENT STUDY COMPLETE")
    print("="*70)

# ============================================================================
# Main Function
# ============================================================================

def main():
    """
    Main execution function
    """
    example_event_study()

if __name__ == "__main__":
    main()
