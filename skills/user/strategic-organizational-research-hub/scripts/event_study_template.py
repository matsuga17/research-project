"""
Event Study Template for Strategic & Organizational Research
=============================================================

This script provides a comprehensive framework for conducting event studies
in strategy research (M&A, CEO succession, regulatory changes, etc.).

Author: Strategic & Organizational Research Hub
Version: 1.0
License: Apache 2.0

Requirements:
    pip install pandas numpy scipy matplotlib seaborn yfinance

Event Study Methodology:
1. Define event window (e.g., [-1, +1] days around announcement)
2. Define estimation window (e.g., [-250, -11] days before event)
3. Estimate normal returns using market model: R_it = α_i + β_i*R_mt + ε_it
4. Calculate abnormal returns: AR_it = R_it - (α_i + β_i*R_mt)
5. Aggregate: Average Abnormal Return (AAR), Cumulative Abnormal Return (CAR)
6. Test significance: t-test, cross-sectional regression
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import yfinance as yf
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# Event Study Calculator
# ============================================================================

class EventStudy:
    """
    Main class for event study analysis
    """
    
    def __init__(self, events_df, event_date_col, ticker_col):
        """
        Initialize event study
        
        Args:
            events_df: DataFrame with events (must have event_date and ticker columns)
            event_date_col: Name of column with event dates
            ticker_col: Name of column with ticker symbols
        """
        self.events = events_df.copy()
        self.event_date_col = event_date_col
        self.ticker_col = ticker_col
        
        # Convert dates to datetime
        self.events[event_date_col] = pd.to_datetime(self.events[event_date_col])
        
        print("="*70)
        print("EVENT STUDY INITIALIZED")
        print("="*70)
        print(f"Number of events: {len(self.events)}")
        print(f"Date range: {self.events[event_date_col].min()} to {self.events[event_date_col].max()}")
        print(f"Unique firms: {self.events[ticker_col].nunique()}")
    
    def download_stock_data(self, start_date, end_date, market_index='^GSPC'):
        """
        Download stock price data for all events
        
        Args:
            start_date: Start date for data download
            end_date: End date for data download
            market_index: Market index ticker (default: ^GSPC = S&P 500)
            
        Returns:
            Dictionary with stock price data for each ticker
        """
        print("\n" + "="*70)
        print("DOWNLOADING STOCK PRICE DATA")
        print("="*70)
        
        tickers = self.events[self.ticker_col].unique().tolist()
        tickers.append(market_index)
        
        print(f"Downloading data for {len(tickers)} tickers...")
        
        # Download data
        data = yf.download(tickers, start=start_date, end=end_date, 
                          progress=False, threads=True)['Adj Close']
        
        if isinstance(data, pd.Series):
            data = data.to_frame(name=tickers[0])
        
        # Calculate returns
        returns = data.pct_change().dropna()
        
        print(f"✅ Downloaded data: {len(returns)} trading days")
        
        return returns, market_index
    
    def estimate_market_model(self, returns, ticker, market_index, 
                             estimation_start, estimation_end):
        """
        Estimate market model parameters (α, β) for a firm
        
        Model: R_it = α_i + β_i*R_mt + ε_it
        
        Args:
            returns: DataFrame with returns
            ticker: Stock ticker
            market_index: Market index ticker
            estimation_start: Start date of estimation window
            estimation_end: End date of estimation window
            
        Returns:
            Dictionary with α, β, and regression statistics
        """
        # Get estimation window data
        estimation_data = returns.loc[estimation_start:estimation_end, [ticker, market_index]]
        estimation_data = estimation_data.dropna()
        
        if len(estimation_data) < 50:
            print(f"⚠️ Warning: Only {len(estimation_data)} observations for {ticker} estimation")
        
        # Run regression: R_i = α + β*R_m
        y = estimation_data[ticker]
        X = estimation_data[market_index]
        
        # Add constant
        X_with_const = np.column_stack([np.ones(len(X)), X])
        
        # OLS estimation
        beta_hat = np.linalg.lstsq(X_with_const, y, rcond=None)[0]
        alpha = beta_hat[0]
        beta = beta_hat[1]
        
        # Calculate R-squared
        y_pred = alpha + beta * X
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - y.mean()) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        
        return {
            'alpha': alpha,
            'beta': beta,
            'r_squared': r_squared,
            'n_obs': len(estimation_data)
        }
    
    def calculate_abnormal_returns(self, returns, ticker, market_index, 
                                   event_date, event_window, 
                                   market_model_params):
        """
        Calculate abnormal returns around event
        
        Args:
            returns: DataFrame with returns
            ticker: Stock ticker
            market_index: Market index ticker
            event_date: Event date
            event_window: Tuple of (start_day, end_day) relative to event (e.g., (-1, 1))
            market_model_params: Dictionary with α and β
            
        Returns:
            DataFrame with abnormal returns
        """
        # Define event window dates
        event_window_start = event_date + timedelta(days=event_window[0])
        event_window_end = event_date + timedelta(days=event_window[1])
        
        # Get event window data
        event_data = returns.loc[event_window_start:event_window_end, [ticker, market_index]]
        event_data = event_data.dropna()
        
        if len(event_data) == 0:
            print(f"⚠️ Warning: No data for {ticker} in event window")
            return pd.DataFrame()
        
        # Calculate expected returns using market model
        alpha = market_model_params['alpha']
        beta = market_model_params['beta']
        
        event_data['expected_return'] = alpha + beta * event_data[market_index]
        
        # Calculate abnormal returns
        event_data['abnormal_return'] = event_data[ticker] - event_data['expected_return']
        
        # Add relative day (0 = event date)
        event_data['relative_day'] = (event_data.index - event_date).days
        
        return event_data[['relative_day', 'abnormal_return', 'expected_return']]
    
    def run_event_study(self, event_window=(-1, 1), estimation_window=(-250, -11),
                       market_index='^GSPC'):
        """
        Run complete event study for all events
        
        Args:
            event_window: Tuple (start, end) in days relative to event
            estimation_window: Tuple (start, end) in days relative to event
            market_index: Market index ticker
            
        Returns:
            DataFrame with abnormal returns for all events
        """
        print("\n" + "="*70)
        print("RUNNING EVENT STUDY")
        print("="*70)
        print(f"Event window: {event_window}")
        print(f"Estimation window: {estimation_window}")
        
        # Determine data download range
        min_event_date = self.events[self.event_date_col].min()
        max_event_date = self.events[self.event_date_col].max()
        
        start_date = min_event_date + timedelta(days=estimation_window[0] - 10)
        end_date = max_event_date + timedelta(days=event_window[1] + 10)
        
        # Download stock data
        returns, market_idx = self.download_stock_data(start_date, end_date, market_index)
        
        # Run event study for each event
        all_results = []
        
        for idx, row in self.events.iterrows():
            ticker = row[self.ticker_col]
            event_date = row[self.event_date_col]
            
            print(f"\nProcessing: {ticker} on {event_date.date()}")
            
            # Check if ticker data available
            if ticker not in returns.columns:
                print(f"⚠️ Skipping {ticker}: No data available")
                continue
            
            # Define estimation window dates
            est_start = event_date + timedelta(days=estimation_window[0])
            est_end = event_date + timedelta(days=estimation_window[1])
            
            # Estimate market model
            try:
                mm_params = self.estimate_market_model(returns, ticker, market_idx,
                                                       est_start, est_end)
                
                print(f"  Market model: α={mm_params['alpha']:.6f}, β={mm_params['beta']:.4f}, R²={mm_params['r_squared']:.4f}")
                
                # Calculate abnormal returns
                ar_data = self.calculate_abnormal_returns(returns, ticker, market_idx,
                                                          event_date, event_window, mm_params)
                
                if len(ar_data) > 0:
                    ar_data['ticker'] = ticker
                    ar_data['event_date'] = event_date
                    
                    # Merge with event characteristics
                    for col in row.index:
                        if col not in [self.ticker_col, self.event_date_col]:
                            ar_data[col] = row[col]
                    
                    all_results.append(ar_data)
                    
                    # Print CAR
                    car = ar_data['abnormal_return'].sum()
                    print(f"  CAR[{event_window[0]}, {event_window[1]}]: {car*100:.2f}%")
            
            except Exception as e:
                print(f"⚠️ Error processing {ticker}: {e}")
                continue
        
        if len(all_results) == 0:
            print("\n❌ No successful event studies")
            return pd.DataFrame()
        
        # Combine all results
        results_df = pd.concat(all_results, ignore_index=True)
        
        print("\n" + "="*70)
        print("EVENT STUDY COMPLETE")
        print("="*70)
        print(f"✅ Successful events: {len(all_results)}")
        print(f"✅ Total abnormal return observations: {len(results_df)}")
        
        return results_df
    
    @staticmethod
    def calculate_car(ar_data, group_by_cols=['ticker', 'event_date']):
        """
        Calculate Cumulative Abnormal Returns (CAR)
        
        Args:
            ar_data: DataFrame with abnormal returns
            group_by_cols: Columns to group by
            
        Returns:
            DataFrame with CAR for each event
        """
        car_df = ar_data.groupby(group_by_cols).agg({
            'abnormal_return': 'sum'
        }).reset_index()
        
        car_df.rename(columns={'abnormal_return': 'car'}, inplace=True)
        
        return car_df
    
    @staticmethod
    def test_significance(car_data, car_col='car'):
        """
        Test significance of CARs
        
        H0: Mean CAR = 0
        H1: Mean CAR ≠ 0
        
        Args:
            car_data: DataFrame with CAR
            car_col: Name of CAR column
            
        Returns:
            Dictionary with test statistics
        """
        cars = car_data[car_col].dropna()
        
        # One-sample t-test
        t_stat, p_value = stats.ttest_1samp(cars, 0)
        
        # Calculate mean and SE
        mean_car = cars.mean()
        se_car = cars.std() / np.sqrt(len(cars))
        
        # 95% CI
        ci_lower = mean_car - 1.96 * se_car
        ci_upper = mean_car + 1.96 * se_car
        
        print("\n" + "="*70)
        print("SIGNIFICANCE TEST")
        print("="*70)
        print(f"Mean CAR: {mean_car*100:.4f}%")
        print(f"Std. Error: {se_car*100:.4f}%")
        print(f"t-statistic: {t_stat:.4f}")
        print(f"p-value: {p_value:.4f}")
        print(f"95% CI: [{ci_lower*100:.4f}%, {ci_upper*100:.4f}%]")
        
        if p_value < 0.001:
            print("Significance: *** (p < 0.001)")
        elif p_value < 0.01:
            print("Significance: ** (p < 0.01)")
        elif p_value < 0.05:
            print("Significance: * (p < 0.05)")
        else:
            print("Significance: Not significant (p >= 0.05)")
        
        # Proportion of positive CARs
        pct_positive = (cars > 0).sum() / len(cars) * 100
        print(f"\nPositive CARs: {pct_positive:.1f}%")
        
        return {
            'mean_car': mean_car,
            'se_car': se_car,
            't_stat': t_stat,
            'p_value': p_value,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'n': len(cars),
            'pct_positive': pct_positive
        }
    
    @staticmethod
    def cross_sectional_regression(car_data, car_col='car', explanatory_vars=[]):
        """
        Cross-sectional regression to explain CAR variation
        
        Model: CAR_i = β0 + β1*X1_i + β2*X2_i + ... + ε_i
        
        Args:
            car_data: DataFrame with CAR and explanatory variables
            car_col: Name of CAR column
            explanatory_vars: List of explanatory variable names
            
        Returns:
            Regression results
        """
        import statsmodels.api as sm
        
        print("\n" + "="*70)
        print("CROSS-SECTIONAL REGRESSION")
        print("="*70)
        
        # Prepare data
        data_clean = car_data[[car_col] + explanatory_vars].dropna()
        
        y = data_clean[car_col]
        X = data_clean[explanatory_vars]
        X = sm.add_constant(X)
        
        # Run OLS
        model = sm.OLS(y, X)
        results = model.fit(cov_type='HC1')  # Robust SE
        
        print(results.summary())
        
        return results

# ============================================================================
# Visualization
# ============================================================================

class EventStudyPlots:
    """
    Visualization tools for event studies
    """
    
    @staticmethod
    def plot_average_abnormal_returns(ar_data):
        """
        Plot Average Abnormal Returns (AAR) over event window
        """
        # Calculate AAR by relative day
        aar = ar_data.groupby('relative_day')['abnormal_return'].mean()
        
        # Calculate standard error
        aar_se = ar_data.groupby('relative_day')['abnormal_return'].sem()
        
        # Plot
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.axhline(y=0, color='black', linestyle='--', alpha=0.3)
        ax.axvline(x=0, color='red', linestyle='--', alpha=0.3, label='Event Day')
        
        ax.plot(aar.index, aar.values * 100, marker='o', linewidth=2, label='AAR')
        ax.fill_between(aar.index, 
                        (aar - 1.96*aar_se) * 100, 
                        (aar + 1.96*aar_se) * 100, 
                        alpha=0.2, label='95% CI')
        
        ax.set_xlabel('Days Relative to Event', fontsize=12)
        ax.set_ylabel('Average Abnormal Return (%)', fontsize=12)
        ax.set_title('Average Abnormal Returns Around Event', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('aar_plot.png', dpi=300)
        print("✅ Saved plot: aar_plot.png")
        
        return fig
    
    @staticmethod
    def plot_cumulative_abnormal_returns(ar_data):
        """
        Plot Cumulative Average Abnormal Returns (CAAR)
        """
        # Calculate CAAR
        aar = ar_data.groupby('relative_day')['abnormal_return'].mean()
        caar = aar.cumsum()
        
        # Plot
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.axhline(y=0, color='black', linestyle='--', alpha=0.3)
        ax.axvline(x=0, color='red', linestyle='--', alpha=0.3, label='Event Day')
        
        ax.plot(caar.index, caar.values * 100, marker='o', linewidth=2, 
               color='darkblue', label='CAAR')
        
        ax.set_xlabel('Days Relative to Event', fontsize=12)
        ax.set_ylabel('Cumulative Average Abnormal Return (%)', fontsize=12)
        ax.set_title('Cumulative Abnormal Returns', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('caar_plot.png', dpi=300)
        print("✅ Saved plot: caar_plot.png")
        
        return fig
    
    @staticmethod
    def plot_car_distribution(car_data, car_col='car'):
        """
        Plot distribution of CARs
        """
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Histogram
        axes[0].hist(car_data[car_col] * 100, bins=30, edgecolor='black', alpha=0.7)
        axes[0].axvline(x=0, color='red', linestyle='--', linewidth=2)
        axes[0].axvline(x=car_data[car_col].mean() * 100, color='blue', 
                       linestyle='--', linewidth=2, label=f'Mean: {car_data[car_col].mean()*100:.2f}%')
        axes[0].set_xlabel('CAR (%)', fontsize=12)
        axes[0].set_ylabel('Frequency', fontsize=12)
        axes[0].set_title('Distribution of CARs', fontsize=14, fontweight='bold')
        axes[0].legend()
        axes[0].grid(alpha=0.3)
        
        # Box plot
        axes[1].boxplot(car_data[car_col] * 100, vert=True)
        axes[1].axhline(y=0, color='red', linestyle='--', linewidth=2)
        axes[1].set_ylabel('CAR (%)', fontsize=12)
        axes[1].set_title('Box Plot of CARs', fontsize=14, fontweight='bold')
        axes[1].grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('car_distribution.png', dpi=300)
        print("✅ Saved plot: car_distribution.png")
        
        return fig

# ============================================================================
# Example Workflow
# ============================================================================

def example_workflow():
    """
    Demonstrate event study with sample M&A announcements
    """
    print("="*70)
    print("EVENT STUDY EXAMPLE: M&A ANNOUNCEMENTS")
    print("="*70)
    
    # Sample events: Major M&A announcements in tech sector
    events_data = {
        'ticker': ['MSFT', 'CRM', 'AMD', 'ADBE', 'ORCL'],
        'event_date': [
            '2023-01-18',  # Microsoft-Activision (regulatory news)
            '2022-08-25',  # Salesforce-Slack
            '2022-02-14',  # AMD-Xilinx
            '2022-09-15',  # Adobe-Figma
            '2022-12-19'   # Oracle-Cerner
        ],
        'deal_value': [68.7, 27.7, 49.0, 20.0, 28.3],  # Billion USD
        'payment_method': ['Cash', 'Cash', 'Stock', 'Mixed', 'Cash']
    }
    
    events_df = pd.DataFrame(events_data)
    
    print("\nSample Events:")
    print(events_df)
    
    # Initialize event study
    es = EventStudy(events_df, event_date_col='event_date', ticker_col='ticker')
    
    # Run event study
    ar_data = es.run_event_study(event_window=(-2, 2), estimation_window=(-250, -11))
    
    if len(ar_data) == 0:
        print("\n❌ Event study failed. Check ticker symbols and dates.")
        return
    
    # Calculate CAR
    car_data = es.calculate_car(ar_data)
    
    # Merge with event characteristics
    car_data = car_data.merge(events_df, on=['ticker', 'event_date'], how='left')
    
    print("\n" + "="*70)
    print("CAR SUMMARY")
    print("="*70)
    print(car_data[['ticker', 'event_date', 'car', 'deal_value']])
    
    # Test significance
    test_results = es.test_significance(car_data, car_col='car')
    
    # Cross-sectional regression
    # Model: CAR = f(deal_value, payment_method)
    car_data['cash_dummy'] = (car_data['payment_method'] == 'Cash').astype(int)
    
    cs_results = es.cross_sectional_regression(car_data, car_col='car', 
                                               explanatory_vars=['deal_value', 'cash_dummy'])
    
    # Plots
    plots = EventStudyPlots()
    plots.plot_average_abnormal_returns(ar_data)
    plots.plot_cumulative_abnormal_returns(ar_data)
    plots.plot_car_distribution(car_data)
    
    print("\n" + "="*70)
    print("EVENT STUDY COMPLETE")
    print("="*70)
    print("Outputs:")
    print("  - aar_plot.png: Average Abnormal Returns")
    print("  - caar_plot.png: Cumulative Abnormal Returns")
    print("  - car_distribution.png: Distribution of CARs")
    
    return ar_data, car_data

# ============================================================================
# Main Function
# ============================================================================

def main():
    """
    Main execution
    """
    example_workflow()

if __name__ == "__main__":
    main()
