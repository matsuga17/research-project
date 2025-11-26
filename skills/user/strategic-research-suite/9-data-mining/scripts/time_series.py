"""
time_series.py

Time Series Analysis for Strategic Research

This module provides time series forecasting and analysis methods for
strategic management research, including trend analysis, seasonality detection,
and forecasting.

Key Features:
- ARIMA/SARIMA modeling
- Exponential smoothing (Holt-Winters)
- Trend decomposition
- Stationarity testing
- Forecast evaluation
- Intervention analysis

Common Applications in Strategic Research:
- Sales forecasting
- Performance trend analysis
- Market demand prediction
- Industry cycle analysis
- Event impact assessment (mergers, policy changes)

Usage:
    from time_series import TimeSeriesAnalyzer
    
    # Initialize analyzer
    analyzer = TimeSeriesAnalyzer(
        data=sales_data,
        time_col='date',
        value_col='sales'
    )
    
    # Test stationarity
    stationarity = analyzer.test_stationarity()
    
    # Fit ARIMA model
    model = analyzer.fit_arima(order=(1, 1, 1))
    
    # Forecast
    forecast = analyzer.forecast(steps=12)
    
    # Evaluate
    metrics = analyzer.evaluate_forecast()

References:
- Box, G. E., & Jenkins, G. M. (1976). Time series analysis: Forecasting and control.
- Hyndman, R. J., & Athanasopoulos, G. (2021). Forecasting: Principles and practice.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple, Any
import logging
from pathlib import Path
import warnings

# Statistical libraries
from scipy import stats
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, kpss, acf, pacf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TimeSeriesAnalyzer:
    """
    Time series analyzer for forecasting and trend analysis
    
    This class provides comprehensive time series analysis functionality
    for strategic research applications.
    
    Attributes:
        data: Time series DataFrame
        time_col: Time/date column name
        value_col: Value column name
        ts: Time series (pandas Series with datetime index)
        model: Fitted time series model
        forecast_: Forecast values
    """
    
    def __init__(self,
                 data: pd.DataFrame,
                 time_col: str = 'date',
                 value_col: str = 'value',
                 freq: Optional[str] = None):
        """
        Initialize time series analyzer
        
        Args:
            data: DataFrame with time series data
            time_col: Time/date column
            value_col: Value column to analyze
            freq: Frequency string (e.g., 'MS' for month start, 'Q' for quarter)
        """
        self.data = data.copy()
        self.time_col = time_col
        self.value_col = value_col
        
        # Convert to time series
        self.data[time_col] = pd.to_datetime(self.data[time_col])
        self.data = self.data.sort_values(time_col)
        self.data = self.data.set_index(time_col)
        
        self.ts = self.data[value_col]
        
        # Infer frequency if not provided
        if freq:
            self.ts.index.freq = freq
        else:
            self.ts = self.ts.asfreq(pd.infer_freq(self.ts.index))
        
        self.model = None
        self.forecast_ = None
        self.residuals_ = None
        
        logger.info(f"Initialized TimeSeriesAnalyzer:")
        logger.info(f"  Time series length: {len(self.ts)}")
        logger.info(f"  Date range: {self.ts.index.min()} to {self.ts.index.max()}")
        logger.info(f"  Frequency: {self.ts.index.freq}")
    
    # =========================================================================
    # Stationarity Testing
    # =========================================================================
    
    def test_stationarity(self,
                         method: str = 'adf',
                         significance: float = 0.05) -> Dict[str, Any]:
        """
        Test for stationarity
        
        Args:
            method: 'adf' (Augmented Dickey-Fuller) or 'kpss' (KPSS test)
            significance: Significance level
        
        Returns:
            Dictionary with test results
        """
        logger.info(f"Testing stationarity using {method.upper()} test...")
        
        if method == 'adf':
            result = adfuller(self.ts.dropna(), autolag='AIC')
            
            output = {
                'test_statistic': result[0],
                'p_value': result[1],
                'lags_used': result[2],
                'n_obs': result[3],
                'critical_values': result[4],
                'is_stationary': result[1] < significance
            }
            
            logger.info(f"  ADF Statistic: {result[0]:.4f}")
            logger.info(f"  p-value: {result[1]:.4f}")
            logger.info(f"  Stationary: {output['is_stationary']}")
            
        elif method == 'kpss':
            result = kpss(self.ts.dropna(), regression='c')
            
            output = {
                'test_statistic': result[0],
                'p_value': result[1],
                'lags_used': result[2],
                'critical_values': result[3],
                'is_stationary': result[1] > significance  # KPSS null: stationary
            }
            
            logger.info(f"  KPSS Statistic: {result[0]:.4f}")
            logger.info(f"  p-value: {result[1]:.4f}")
            logger.info(f"  Stationary: {output['is_stationary']}")
        
        else:
            raise ValueError(f"Unknown method: {method}")
        
        return output
    
    def make_stationary(self,
                       method: str = 'diff',
                       order: int = 1) -> pd.Series:
        """
        Transform series to achieve stationarity
        
        Args:
            method: 'diff' (differencing) or 'log' (log transform)
            order: Differencing order
        
        Returns:
            Stationary time series
        """
        logger.info(f"Making series stationary using {method} method...")
        
        if method == 'diff':
            stationary = self.ts.diff(order).dropna()
        elif method == 'log':
            stationary = np.log(self.ts)
            if order > 0:
                stationary = stationary.diff(order).dropna()
        else:
            raise ValueError(f"Unknown method: {method}")
        
        logger.info(f"✓ Transformed series length: {len(stationary)}")
        
        return stationary
    
    # =========================================================================
    # Decomposition
    # =========================================================================
    
    def decompose(self,
                 model: str = 'additive',
                 period: Optional[int] = None) -> Dict[str, pd.Series]:
        """
        Decompose time series into trend, seasonal, and residual components
        
        Args:
            model: 'additive' or 'multiplicative'
            period: Seasonal period (auto-detected if None)
        
        Returns:
            Dictionary with trend, seasonal, residual components
        """
        logger.info(f"Decomposing time series ({model} model)...")
        
        decomposition = seasonal_decompose(
            self.ts,
            model=model,
            period=period,
            extrapolate_trend='freq'
        )
        
        components = {
            'trend': decomposition.trend,
            'seasonal': decomposition.seasonal,
            'residual': decomposition.resid,
            'observed': decomposition.observed
        }
        
        logger.info("✓ Decomposition complete")
        
        return components
    
    # =========================================================================
    # ARIMA Modeling
    # =========================================================================
    
    def fit_arima(self,
                 order: Tuple[int, int, int] = (1, 1, 1),
                 seasonal_order: Optional[Tuple[int, int, int, int]] = None) -> Any:
        """
        Fit ARIMA or SARIMA model
        
        Args:
            order: (p, d, q) for ARIMA
            seasonal_order: (P, D, Q, s) for SARIMA (None for non-seasonal)
        
        Returns:
            Fitted model results
        """
        logger.info(f"Fitting ARIMA{order} model...")
        
        if seasonal_order:
            logger.info(f"  Seasonal order: {seasonal_order}")
            model = SARIMAX(
                self.ts,
                order=order,
                seasonal_order=seasonal_order
            )
        else:
            model = ARIMA(self.ts, order=order)
        
        self.model = model.fit()
        self.residuals_ = self.model.resid
        
        logger.info("✓ Model fitted successfully")
        logger.info(f"  AIC: {self.model.aic:.2f}")
        logger.info(f"  BIC: {self.model.bic:.2f}")
        
        return self.model
    
    def auto_arima(self,
                  max_p: int = 5,
                  max_d: int = 2,
                  max_q: int = 5,
                  seasonal: bool = False) -> Any:
        """
        Automatic ARIMA order selection using AIC
        
        Args:
            max_p: Maximum AR order
            max_d: Maximum differencing order
            max_q: Maximum MA order
            seasonal: Include seasonal ARIMA
        
        Returns:
            Best fitted model
        """
        logger.info("Performing automatic ARIMA selection...")
        
        best_aic = np.inf
        best_order = None
        best_model = None
        
        # Grid search over orders
        for p in range(max_p + 1):
            for d in range(max_d + 1):
                for q in range(max_q + 1):
                    try:
                        model = ARIMA(self.ts, order=(p, d, q))
                        fitted = model.fit()
                        
                        if fitted.aic < best_aic:
                            best_aic = fitted.aic
                            best_order = (p, d, q)
                            best_model = fitted
                    
                    except:
                        continue
        
        self.model = best_model
        self.residuals_ = self.model.resid
        
        logger.info(f"✓ Best model: ARIMA{best_order}")
        logger.info(f"  AIC: {best_aic:.2f}")
        
        return self.model
    
    # =========================================================================
    # Exponential Smoothing
    # =========================================================================
    
    def fit_exponential_smoothing(self,
                                 seasonal: Optional[str] = None,
                                 seasonal_periods: Optional[int] = None) -> Any:
        """
        Fit Exponential Smoothing (Holt-Winters) model
        
        Args:
            seasonal: None, 'add' (additive), or 'mul' (multiplicative)
            seasonal_periods: Number of periods in season
        
        Returns:
            Fitted model
        """
        logger.info("Fitting Exponential Smoothing model...")
        
        model = ExponentialSmoothing(
            self.ts,
            seasonal=seasonal,
            seasonal_periods=seasonal_periods
        )
        
        self.model = model.fit()
        
        logger.info("✓ Model fitted successfully")
        
        return self.model
    
    # =========================================================================
    # Forecasting
    # =========================================================================
    
    def forecast(self,
                steps: int = 12,
                alpha: float = 0.05) -> pd.DataFrame:
        """
        Generate forecast with confidence intervals
        
        Args:
            steps: Number of steps ahead to forecast
            alpha: Significance level for confidence intervals
        
        Returns:
            DataFrame with forecast and confidence intervals
        """
        if self.model is None:
            raise ValueError("Model not fitted. Call fit_arima() or fit_exponential_smoothing() first.")
        
        logger.info(f"Generating {steps}-step forecast...")
        
        # Get forecast
        if hasattr(self.model, 'get_forecast'):
            forecast_obj = self.model.get_forecast(steps=steps)
            forecast_mean = forecast_obj.predicted_mean
            conf_int = forecast_obj.conf_int(alpha=alpha)
        else:
            # For ExponentialSmoothing
            forecast_mean = self.model.forecast(steps=steps)
            conf_int = None
        
        # Build results DataFrame
        forecast_df = pd.DataFrame({
            'forecast': forecast_mean
        })
        
        if conf_int is not None:
            forecast_df['lower'] = conf_int.iloc[:, 0]
            forecast_df['upper'] = conf_int.iloc[:, 1]
        
        self.forecast_ = forecast_df
        
        logger.info("✓ Forecast generated")
        
        return forecast_df
    
    def evaluate_forecast(self,
                         actual: Optional[pd.Series] = None) -> Dict[str, float]:
        """
        Evaluate forecast accuracy
        
        Args:
            actual: Actual values for comparison (if available)
        
        Returns:
            Dictionary with error metrics
        """
        if self.forecast_ is None:
            raise ValueError("No forecast available. Call forecast() first.")
        
        logger.info("Evaluating forecast accuracy...")
        
        metrics = {}
        
        # In-sample fit
        fitted_values = self.model.fittedvalues
        residuals = self.ts - fitted_values
        
        metrics['mae'] = np.mean(np.abs(residuals))
        metrics['rmse'] = np.sqrt(np.mean(residuals ** 2))
        metrics['mape'] = np.mean(np.abs(residuals / self.ts)) * 100
        
        # Out-of-sample if actual provided
        if actual is not None:
            forecast_values = self.forecast_['forecast']
            errors = actual - forecast_values
            
            metrics['forecast_mae'] = np.mean(np.abs(errors))
            metrics['forecast_rmse'] = np.sqrt(np.mean(errors ** 2))
        
        logger.info("✓ Evaluation metrics:")
        for key, value in metrics.items():
            logger.info(f"  {key.upper()}: {value:.4f}")
        
        return metrics
    
    # =========================================================================
    # Visualization
    # =========================================================================
    
    def plot_series(self, figsize: Tuple[int, int] = (12, 6)):
        """Plot time series"""
        fig, ax = plt.subplots(figsize=figsize)
        
        self.ts.plot(ax=ax, label='Observed')
        
        if self.forecast_ is not None:
            self.forecast_['forecast'].plot(ax=ax, label='Forecast', color='red')
            
            if 'lower' in self.forecast_.columns:
                ax.fill_between(
                    self.forecast_.index,
                    self.forecast_['lower'],
                    self.forecast_['upper'],
                    color='red',
                    alpha=0.2,
                    label='95% CI'
                )
        
        ax.set_xlabel('Time')
        ax.set_ylabel(self.value_col)
        ax.set_title('Time Series with Forecast')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_diagnostics(self, figsize: Tuple[int, int] = (12, 10)):
        """Plot diagnostic plots for residuals"""
        if self.residuals_ is None:
            raise ValueError("Model not fitted")
        
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        
        # Residuals plot
        axes[0, 0].plot(self.residuals_)
        axes[0, 0].axhline(y=0, color='r', linestyle='--')
        axes[0, 0].set_title('Residuals over Time')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Histogram
        axes[0, 1].hist(self.residuals_, bins=30, edgecolor='black')
        axes[0, 1].set_title('Residuals Distribution')
        axes[0, 1].set_xlabel('Residuals')
        
        # Q-Q plot
        stats.probplot(self.residuals_, dist="norm", plot=axes[1, 0])
        axes[1, 0].set_title('Q-Q Plot')
        
        # ACF of residuals
        plot_acf(self.residuals_.dropna(), ax=axes[1, 1], lags=20)
        axes[1, 1].set_title('ACF of Residuals')
        
        plt.tight_layout()
        return fig


# =============================================================================
# Example Usage
# =============================================================================

if __name__ == '__main__':
    # Generate sample time series data
    print("=" * 80)
    print("Time Series Analysis Example")
    print("=" * 80)
    
    # Create sample data
    np.random.seed(42)
    dates = pd.date_range('2010-01-01', periods=120, freq='MS')
    
    # Trend + Seasonality + Noise
    trend = np.linspace(100, 200, 120)
    seasonality = 20 * np.sin(np.arange(120) * 2 * np.pi / 12)
    noise = np.random.normal(0, 5, 120)
    
    values = trend + seasonality + noise
    
    df = pd.DataFrame({
        'date': dates,
        'sales': values
    })
    
    print("\nSample data:")
    print(df.head())
    
    # Initialize analyzer
    analyzer = TimeSeriesAnalyzer(df, time_col='date', value_col='sales', freq='MS')
    
    # Test stationarity
    print("\n" + "=" * 80)
    print("Stationarity Test")
    print("=" * 80)
    stationarity = analyzer.test_stationarity(method='adf')
    
    # Decompose
    print("\n" + "=" * 80)
    print("Decomposition")
    print("=" * 80)
    components = analyzer.decompose(model='additive', period=12)
    
    # Fit ARIMA
    print("\n" + "=" * 80)
    print("ARIMA Modeling")
    print("=" * 80)
    model = analyzer.fit_arima(order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    
    # Forecast
    print("\n" + "=" * 80)
    print("Forecasting")
    print("=" * 80)
    forecast = analyzer.forecast(steps=12)
    print("\nForecast:")
    print(forecast)
    
    # Evaluate
    metrics = analyzer.evaluate_forecast()
    
    print("\n✓ Time series analysis complete!")
