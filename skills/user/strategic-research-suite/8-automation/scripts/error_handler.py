"""
error_handler.py

Comprehensive Error Handling and Recovery

This module provides robust error handling, recovery mechanisms,
and retry logic for research pipeline operations.

Key Features:
- Automatic retry with exponential backoff
- Error logging and reporting
- Recovery from checkpoints
- Data validation and sanitization
- Exception classification

Usage:
    from error_handler import ErrorHandler, retry_with_backoff
    
    # Decorator for automatic retry
    @retry_with_backoff(max_retries=3)
    def collect_data():
        # Data collection code
        pass
    
    # Manual error handling
    handler = ErrorHandler(log_file='errors.log')
    try:
        result = risky_operation()
    except Exception as e:
        handler.handle_error(e, context={'operation': 'data_collection'})

Version: 4.0
Last Updated: 2025-11-02
"""

import logging
import time
import traceback
from functools import wraps
from typing import Callable, Any, Optional, Dict, List
from pathlib import Path
from datetime import datetime
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResearchPipelineError(Exception):
    """Base exception for research pipeline"""
    pass


class DataCollectionError(ResearchPipelineError):
    """Error during data collection"""
    pass


class DataQualityError(ResearchPipelineError):
    """Error related to data quality"""
    pass


class AnalysisError(ResearchPipelineError):
    """Error during statistical analysis"""
    pass


class ConfigurationError(ResearchPipelineError):
    """Error in configuration"""
    pass


# =============================================================================
# Retry Decorators
# =============================================================================

def retry_with_backoff(max_retries: int = 3, 
                      initial_delay: float = 1.0,
                      backoff_factor: float = 2.0,
                      exceptions: tuple = (Exception,)):
    """
    Retry decorator with exponential backoff
    
    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        backoff_factor: Multiplier for delay on each retry
        exceptions: Tuple of exceptions to catch
    
    Returns:
        Decorated function with retry logic
    
    Example:
        @retry_with_backoff(max_retries=3, initial_delay=2)
        def fetch_data():
            return requests.get(url)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            delay = initial_delay
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries - 1:
                        logger.error(f"{func.__name__} failed after {max_retries} attempts")
                        raise
                    
                    logger.warning(f"{func.__name__} attempt {attempt + 1} failed: {e}")
                    logger.info(f"Retrying in {delay:.1f}s...")
                    time.sleep(delay)
                    delay *= backoff_factor
            
            return None  # Should never reach here
        
        return wrapper
    return decorator


def handle_errors(error_handler: Optional['ErrorHandler'] = None,
                 default_return: Any = None,
                 reraise: bool = False):
    """
    Decorator for automatic error handling
    
    Args:
        error_handler: ErrorHandler instance
        default_return: Value to return on error
        reraise: Whether to re-raise exception after handling
    
    Example:
        @handle_errors(default_return=None)
        def process_data():
            # Processing code
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {e}")
                
                if error_handler:
                    error_handler.handle_error(e, context={
                        'function': func.__name__,
                        'args': str(args)[:100],
                        'kwargs': str(kwargs)[:100]
                    })
                
                if reraise:
                    raise
                
                return default_return
        
        return wrapper
    return decorator


# =============================================================================
# Error Handler Class
# =============================================================================

class ErrorHandler:
    """
    Comprehensive error handler with logging and recovery
    
    Attributes:
        log_file: Path to error log file
        errors: List of recorded errors
        recovery_strategies: Dictionary of recovery functions
    """
    
    def __init__(self, log_file: str = 'pipeline_errors.log'):
        """
        Initialize error handler
        
        Args:
            log_file: Path to error log file
        """
        self.log_file = Path(log_file)
        self.errors = []
        self.recovery_strategies = {}
        
        # Set up file logging
        self.setup_logging()
        
        logger.info(f"ErrorHandler initialized: {self.log_file}")
    
    def setup_logging(self):
        """Configure error logging to file"""
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.ERROR)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    def handle_error(self, 
                    exception: Exception,
                    context: Optional[Dict] = None,
                    fatal: bool = False) -> bool:
        """
        Handle an exception with logging and optional recovery
        
        Args:
            exception: Exception to handle
            context: Additional context information
            fatal: Whether error is fatal (stops execution)
        
        Returns:
            True if error was recovered, False otherwise
        """
        error_record = {
            'timestamp': datetime.now().isoformat(),
            'type': type(exception).__name__,
            'message': str(exception),
            'traceback': traceback.format_exc(),
            'context': context or {},
            'fatal': fatal
        }
        
        self.errors.append(error_record)
        
        # Log error
        logger.error(f"\n{'=' * 80}")
        logger.error(f"ERROR: {error_record['type']}")
        logger.error(f"{'=' * 80}")
        logger.error(f"Message: {error_record['message']}")
        
        if context:
            logger.error(f"Context: {context}")
        
        logger.error(f"\nTraceback:\n{error_record['traceback']}")
        
        # Try recovery if strategy exists
        exception_type = type(exception).__name__
        if exception_type in self.recovery_strategies and not fatal:
            logger.info(f"Attempting recovery strategy for {exception_type}...")
            try:
                recovery_func = self.recovery_strategies[exception_type]
                recovery_func(exception, context)
                logger.info("✓ Recovery successful")
                return True
            except Exception as recovery_error:
                logger.error(f"✗ Recovery failed: {recovery_error}")
        
        if fatal:
            logger.critical("FATAL ERROR - Execution stopped")
        
        return False
    
    def register_recovery_strategy(self, 
                                  exception_type: str,
                                  recovery_func: Callable):
        """
        Register recovery strategy for exception type
        
        Args:
            exception_type: Name of exception class
            recovery_func: Function to call for recovery
        
        Example:
            def recover_from_timeout(exc, context):
                time.sleep(10)
                # Retry operation
            
            handler.register_recovery_strategy('TimeoutError', recover_from_timeout)
        """
        self.recovery_strategies[exception_type] = recovery_func
        logger.info(f"Registered recovery strategy for {exception_type}")
    
    def get_error_summary(self) -> Dict[str, Any]:
        """
        Get summary of errors
        
        Returns:
            Dictionary with error statistics
        """
        if not self.errors:
            return {'total_errors': 0}
        
        error_types = {}
        for error in self.errors:
            error_type = error['type']
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        fatal_count = sum(1 for e in self.errors if e.get('fatal', False))
        
        return {
            'total_errors': len(self.errors),
            'fatal_errors': fatal_count,
            'error_types': error_types,
            'most_recent': self.errors[-1]['timestamp'] if self.errors else None
        }
    
    def export_errors(self, filepath: str):
        """
        Export error log to JSON file
        
        Args:
            filepath: Output file path
        """
        with open(filepath, 'w') as f:
            json.dump(self.errors, f, indent=2)
        
        logger.info(f"Errors exported: {filepath}")
    
    def clear_errors(self):
        """Clear error log"""
        self.errors = []
        logger.info("Error log cleared")


# =============================================================================
# Data Validation
# =============================================================================

class DataValidator:
    """
    Validate data quality and integrity
    
    Provides validation checks for common data issues
    """
    
    @staticmethod
    def validate_panel_structure(df, 
                                firm_id_col: str = 'firm_id',
                                time_col: str = 'year') -> List[str]:
        """
        Validate panel data structure
        
        Args:
            df: DataFrame to validate
            firm_id_col: Firm identifier column
            time_col: Time identifier column
        
        Returns:
            List of validation issues
        """
        issues = []
        
        # Check required columns
        if firm_id_col not in df.columns:
            issues.append(f"Missing column: {firm_id_col}")
        if time_col not in df.columns:
            issues.append(f"Missing column: {time_col}")
        
        if issues:
            return issues
        
        # Check for duplicates
        duplicates = df.duplicated(subset=[firm_id_col, time_col]).sum()
        if duplicates > 0:
            issues.append(f"Found {duplicates} duplicate firm-year observations")
        
        # Check balance
        panel_counts = df.groupby(firm_id_col).size()
        if panel_counts.std() > 0:
            issues.append(f"Unbalanced panel: observations per firm range from {panel_counts.min()} to {panel_counts.max()}")
        
        # Check missing values
        missing = df.isnull().sum()
        if missing.sum() > 0:
            issues.append(f"Missing values found in {(missing > 0).sum()} columns")
        
        return issues
    
    @staticmethod
    def validate_numeric_range(df,
                              column: str,
                              min_val: Optional[float] = None,
                              max_val: Optional[float] = None) -> List[str]:
        """
        Validate numeric column range
        
        Args:
            df: DataFrame
            column: Column to validate
            min_val: Minimum acceptable value
            max_val: Maximum acceptable value
        
        Returns:
            List of validation issues
        """
        issues = []
        
        if column not in df.columns:
            issues.append(f"Column not found: {column}")
            return issues
        
        if min_val is not None:
            below_min = (df[column] < min_val).sum()
            if below_min > 0:
                issues.append(f"{below_min} values in {column} below minimum {min_val}")
        
        if max_val is not None:
            above_max = (df[column] > max_val).sum()
            if above_max > 0:
                issues.append(f"{above_max} values in {column} above maximum {max_val}")
        
        return issues
    
    @staticmethod
    def validate_required_columns(df, required_columns: List[str]) -> List[str]:
        """
        Check for required columns
        
        Args:
            df: DataFrame
            required_columns: List of required column names
        
        Returns:
            List of missing columns
        """
        missing = [col for col in required_columns if col not in df.columns]
        return missing


# =============================================================================
# Safe Operations
# =============================================================================

def safe_divide(numerator: float, 
               denominator: float,
               default: float = 0.0) -> float:
    """
    Safe division with zero handling
    
    Args:
        numerator: Numerator value
        denominator: Denominator value
        default: Value to return if division by zero
    
    Returns:
        Result of division or default value
    """
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except Exception:
        return default


def safe_log(value: float, default: float = 0.0) -> float:
    """
    Safe logarithm with non-positive handling
    
    Args:
        value: Value to take log of
        default: Value to return for non-positive input
    
    Returns:
        Log of value or default
    """
    import numpy as np
    
    try:
        if value <= 0:
            return default
        return np.log(value)
    except Exception:
        return default


# =============================================================================
# Example Usage
# =============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("ERROR HANDLER DEMO")
    print("=" * 80)
    
    # Initialize handler
    handler = ErrorHandler(log_file='demo_errors.log')
    
    # Example 1: Retry decorator
    print("\n[Example 1: Retry with backoff]")
    
    @retry_with_backoff(max_retries=3, initial_delay=0.5)
    def flaky_function(success_probability=0.3):
        """Function that sometimes fails"""
        import random
        if random.random() > success_probability:
            raise ConnectionError("Simulated connection failure")
        return "Success!"
    
    try:
        result = flaky_function(success_probability=0.7)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Failed: {e}")
    
    # Example 2: Error handling
    print("\n[Example 2: Error handling]")
    
    try:
        # Simulate an error
        raise DataCollectionError("Failed to collect data from API")
    except Exception as e:
        handler.handle_error(e, context={'api': 'example.com', 'retry_count': 3})
    
    # Example 3: Data validation
    print("\n[Example 3: Data validation]")
    
    import pandas as pd
    import numpy as np
    
    df = pd.DataFrame({
        'firm_id': ['A', 'A', 'B', 'B'],
        'year': [2020, 2021, 2020, 2021],
        'revenue': [100, 110, 200, -10]  # Negative value is issue
    })
    
    validator = DataValidator()
    
    issues = validator.validate_panel_structure(df)
    print(f"Panel structure issues: {issues if issues else 'None'}")
    
    issues = validator.validate_numeric_range(df, 'revenue', min_val=0)
    print(f"Revenue validation issues: {issues if issues else 'None'}")
    
    # Example 4: Error summary
    print("\n[Example 4: Error summary]")
    summary = handler.get_error_summary()
    print(f"Total errors: {summary['total_errors']}")
    print(f"Error types: {summary['error_types']}")
    
    print("\n" + "=" * 80)
    print("DEMO COMPLETED")
    print("=" * 80)
