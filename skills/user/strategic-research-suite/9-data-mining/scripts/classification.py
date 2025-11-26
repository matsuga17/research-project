"""
classification.py

Classification Models for Strategic Management Research

This module implements classification algorithms for predicting categorical
outcomes in strategic management research.

Common applications:
- Bankruptcy/financial distress prediction
- M&A target prediction
- Strategic group classification
- Innovation success prediction

Usage:
    from classification import FirmClassifier
    
    classifier = FirmClassifier(df, target='bankrupt', features=features)
    classifier.train_random_forest()
    predictions = classifier.predict(test_data)
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FirmClassifier:
    """
    Classification models for firm-level predictions
    
    Attributes:
        df: Input DataFrame
        target: Target variable (binary or multiclass)
        features: Feature variables
        model: Trained model
        X_train, X_test, y_train, y_test: Train/test splits
    """
    
    def __init__(self, df: pd.DataFrame,
                 target: str,
                 features: List[str] = None):
        """
        Initialize classifier
        
        Args:
            df: DataFrame with target and features
            target: Target variable name
            features: List of feature names (if None, use all numeric except target)
        """
        self.df = df.copy()
        self.target = target
        
        if features is None:
            self.features = [col for col in df.select_dtypes(include=[np.number]).columns
                           if col != target]
        else:
            self.features = features
        
        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
        logger.info(f"FirmClassifier initialized:")
        logger.info(f"  Target: {target}")
        logger.info(f"  Features: {len(self.features)}")
        logger.info(f"  Observations: {len(df)}")
    
    def prepare_data(self, test_size: float = 0.2,
                    stratify: bool = True,
                    random_state: int = 42) -> Tuple:
        """
        Prepare train/test split
        
        Args:
            test_size: Proportion for test set
            stratify: Whether to stratify split by target
            random_state: Random seed
        
        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
        """
        from sklearn.model_selection import train_test_split
        
        # Remove missing values
        analysis_vars = [self.target] + self.features
        df_clean = self.df[analysis_vars].dropna()
        
        logger.info(f"\nPreparing data...")
        logger.info(f"  Complete cases: {len(df_clean)} / {len(self.df)}")
        
        # Split features and target
        X = df_clean[self.features]
        y = df_clean[self.target]
        
        # Check class distribution
        logger.info(f"\nTarget distribution:")
        value_counts = y.value_counts()
        for value, count in value_counts.items():
            logger.info(f"  {value}: {count} ({count/len(y)*100:.1f}%)")
        
        # Train/test split
        stratify_param = y if stratify else None
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y,
            test_size=test_size,
            stratify=stratify_param,
            random_state=random_state
        )
        
        logger.info(f"\n  Train set: {len(self.X_train)}")
        logger.info(f"  Test set: {len(self.X_test)}")
        
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def train_random_forest(self, n_estimators: int = 100,
                          max_depth: int = None,
                          **kwargs) -> 'RandomForestClassifier':
        """
        Train Random Forest classifier
        
        Args:
            n_estimators: Number of trees
            max_depth: Maximum tree depth
            **kwargs: Additional parameters for RandomForestClassifier
        
        Returns:
            Trained model
        """
        from sklearn.ensemble import RandomForestClassifier
        
        if self.X_train is None:
            self.prepare_data()
        
        logger.info(f"\nTraining Random Forest...")
        logger.info(f"  Trees: {n_estimators}")
        logger.info(f"  Max depth: {max_depth if max_depth else 'unlimited'}")
        
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=42,
            **kwargs
        )
        
        self.model.fit(self.X_train, self.y_train)
        logger.info("  ✓ Model trained")
        
        return self.model
    
    def train_gradient_boosting(self, n_estimators: int = 100,
                               learning_rate: float = 0.1,
                               **kwargs) -> 'GradientBoostingClassifier':
        """
        Train Gradient Boosting classifier
        
        Args:
            n_estimators: Number of boosting stages
            learning_rate: Learning rate
            **kwargs: Additional parameters
        
        Returns:
            Trained model
        """
        from sklearn.ensemble import GradientBoostingClassifier
        
        if self.X_train is None:
            self.prepare_data()
        
        logger.info(f"\nTraining Gradient Boosting...")
        logger.info(f"  Estimators: {n_estimators}")
        logger.info(f"  Learning rate: {learning_rate}")
        
        self.model = GradientBoostingClassifier(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            random_state=42,
            **kwargs
        )
        
        self.model.fit(self.X_train, self.y_train)
        logger.info("  ✓ Model trained")
        
        return self.model
    
    def train_logistic_regression(self, penalty: str = 'l2',
                                 C: float = 1.0) -> 'LogisticRegression':
        """
        Train Logistic Regression
        
        Args:
            penalty: Regularization type ('l1', 'l2', 'elasticnet', 'none')
            C: Inverse of regularization strength
        
        Returns:
            Trained model
        """
        from sklearn.linear_model import LogisticRegression
        
        if self.X_train is None:
            self.prepare_data()
        
        logger.info(f"\nTraining Logistic Regression...")
        logger.info(f"  Penalty: {penalty}")
        logger.info(f"  C: {C}")
        
        self.model = LogisticRegression(
            penalty=penalty,
            C=C,
            max_iter=1000,
            random_state=42
        )
        
        self.model.fit(self.X_train, self.y_train)
        logger.info("  ✓ Model trained")
        
        return self.model
    
    def evaluate(self) -> Dict:
        """
        Evaluate model performance
        
        Returns:
            Dictionary with performance metrics
        """
        if self.model is None:
            logger.error("Model not trained. Train a model first.")
            return None
        
        from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                                     f1_score, roc_auc_score, classification_report,
                                     confusion_matrix)
        
        logger.info("\nEvaluating model...")
        
        # Predictions
        y_pred_train = self.model.predict(self.X_train)
        y_pred_test = self.model.predict(self.X_test)
        
        # Probabilities (if available)
        try:
            y_prob_train = self.model.predict_proba(self.X_train)[:, 1]
            y_prob_test = self.model.predict_proba(self.X_test)[:, 1]
        except:
            y_prob_train = None
            y_prob_test = None
        
        # Calculate metrics
        results = {
            'train': {
                'accuracy': accuracy_score(self.y_train, y_pred_train),
                'precision': precision_score(self.y_train, y_pred_train, average='weighted', zero_division=0),
                'recall': recall_score(self.y_train, y_pred_train, average='weighted', zero_division=0),
                'f1': f1_score(self.y_train, y_pred_train, average='weighted', zero_division=0)
            },
            'test': {
                'accuracy': accuracy_score(self.y_test, y_pred_test),
                'precision': precision_score(self.y_test, y_pred_test, average='weighted', zero_division=0),
                'recall': recall_score(self.y_test, y_pred_test, average='weighted', zero_division=0),
                'f1': f1_score(self.y_test, y_pred_test, average='weighted', zero_division=0)
            }
        }
        
        # AUC for binary classification
        if len(self.y_test.unique()) == 2 and y_prob_test is not None:
            results['train']['auc'] = roc_auc_score(self.y_train, y_prob_train)
            results['test']['auc'] = roc_auc_score(self.y_test, y_prob_test)
        
        # Confusion matrix
        results['confusion_matrix'] = confusion_matrix(self.y_test, y_pred_test)
        
        # Print results
        logger.info("\n" + "="*60)
        logger.info("Model Performance")
        logger.info("="*60)
        logger.info("\nTrain Set:")
        for metric, value in results['train'].items():
            logger.info(f"  {metric.capitalize()}: {value:.4f}")
        
        logger.info("\nTest Set:")
        for metric, value in results['test'].items():
            logger.info(f"  {metric.capitalize()}: {value:.4f}")
        
        logger.info("\nConfusion Matrix:")
        logger.info(results['confusion_matrix'])
        
        logger.info("\nClassification Report:")
        logger.info(classification_report(self.y_test, y_pred_test))
        
        return results
    
    def feature_importance(self, top_n: int = 10) -> pd.DataFrame:
        """
        Get feature importance (for tree-based models)
        
        Args:
            top_n: Number of top features to return
        
        Returns:
            DataFrame with feature importances
        """
        if self.model is None:
            logger.error("Model not trained")
            return None
        
        if not hasattr(self.model, 'feature_importances_'):
            logger.warning("Model does not have feature_importances_ attribute")
            return None
        
        importance_df = pd.DataFrame({
            'feature': self.features,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        logger.info(f"\nTop {top_n} Features:")
        for idx, row in importance_df.head(top_n).iterrows():
            logger.info(f"  {row['feature']}: {row['importance']:.4f}")
        
        return importance_df
    
    def predict(self, X_new: pd.DataFrame) -> np.ndarray:
        """
        Make predictions on new data
        
        Args:
            X_new: DataFrame with features
        
        Returns:
            Array of predictions
        """
        if self.model is None:
            logger.error("Model not trained")
            return None
        
        predictions = self.model.predict(X_new[self.features])
        return predictions


# Example usage
if __name__ == "__main__":
    # Generate sample data for bankruptcy prediction
    np.random.seed(42)
    n = 1000
    
    # Features: financial ratios
    leverage = np.random.normal(0.5, 0.2, n)
    roa = np.random.normal(0.05, 0.05, n)
    current_ratio = np.random.normal(1.5, 0.5, n)
    zscore = np.random.normal(2.5, 1.5, n)
    
    # Target: bankruptcy (influenced by poor financial health)
    bankruptcy_prob = 1 / (1 + np.exp(-(
        -3 + 5*leverage - 20*roa - 1*current_ratio - 0.5*zscore
    )))
    bankrupt = (np.random.random(n) < bankruptcy_prob).astype(int)
    
    df = pd.DataFrame({
        'firm_id': range(n),
        'bankrupt': bankrupt,
        'leverage': leverage,
        'roa': roa,
        'current_ratio': current_ratio,
        'zscore': zscore
    })
    
    logger.info("="*60)
    logger.info("Bankruptcy Prediction Example")
    logger.info("="*60)
    
    # Create classifier
    classifier = FirmClassifier(df, target='bankrupt')
    
    # Train Random Forest
    classifier.train_random_forest(n_estimators=100)
    
    # Evaluate
    results = classifier.evaluate()
    
    # Feature importance
    importance = classifier.feature_importance()
    
    logger.info("\n" + "="*60)
    logger.info("Classification completed!")
    logger.info("="*60)
