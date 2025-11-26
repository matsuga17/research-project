"""
topic_modeler.py

Topic Modeling for Strategic Management Research

This module implements Latent Dirichlet Allocation (LDA) and other topic
modeling techniques for discovering thematic structures in corporate documents.

Common applications:
- Strategy identification in 10-K filings
- Theme discovery in earnings call transcripts
- Strategic change detection over time
- Industry trend analysis

Usage:
    from topic_modeler import TopicModeler
    
    modeler = TopicModeler(documents, n_topics=5)
    topics, document_topics = modeler.fit_lda()
    modeler.visualize_topics()
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
import logging
from collections import Counter
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TopicModeler:
    """
    Topic modeling for text analysis
    
    Implements LDA (Latent Dirichlet Allocation) and related methods
    for discovering latent topics in document collections.
    
    Attributes:
        documents: List of text documents
        n_topics: Number of topics to extract
        model: Fitted topic model
        vectorizer: Fitted vectorizer
        feature_names: Terms in vocabulary
    """
    
    def __init__(self, documents: List[str], n_topics: int = 5):
        """
        Initialize topic modeler
        
        Args:
            documents: List of text documents
            n_topics: Number of topics to extract
        """
        self.documents = documents
        self.n_topics = n_topics
        self.model = None
        self.vectorizer = None
        self.feature_names = None
        self.document_term_matrix = None
        
        logger.info(f"TopicModeler initialized:")
        logger.info(f"  Documents: {len(documents)}")
        logger.info(f"  Topics: {n_topics}")
    
    def preprocess(self, documents: List[str] = None,
                  remove_stopwords: bool = True,
                  min_df: int = 2,
                  max_df: float = 0.95,
                  max_features: int = 1000) -> np.ndarray:
        """
        Preprocess documents and create document-term matrix
        
        Args:
            documents: List of documents (default: use self.documents)
            remove_stopwords: Whether to remove stopwords
            min_df: Minimum document frequency
            max_df: Maximum document frequency (proportion)
            max_features: Maximum number of features
        
        Returns:
            Document-term matrix
        """
        if documents is None:
            documents = self.documents
        
        logger.info("Preprocessing documents...")
        
        try:
            from sklearn.feature_extraction.text import CountVectorizer
        except ImportError:
            logger.error("scikit-learn not installed")
            return None
        
        # Create vectorizer
        self.vectorizer = CountVectorizer(
            max_df=max_df,
            min_df=min_df,
            max_features=max_features,
            stop_words='english' if remove_stopwords else None,
            token_pattern=r'\b[a-zA-Z]{3,}\b'  # At least 3 letters
        )
        
        # Fit and transform
        self.document_term_matrix = self.vectorizer.fit_transform(documents)
        self.feature_names = self.vectorizer.get_feature_names_out()
        
        logger.info(f"  ✓ Created document-term matrix:")
        logger.info(f"    Shape: {self.document_term_matrix.shape}")
        logger.info(f"    Vocabulary size: {len(self.feature_names)}")
        
        return self.document_term_matrix
    
    def fit_lda(self, n_iter: int = 1000, 
               random_state: int = 42) -> Tuple[np.ndarray, np.ndarray]:
        """
        Fit LDA topic model
        
        Args:
            n_iter: Number of iterations
            random_state: Random seed
        
        Returns:
            Tuple of (topic-term matrix, document-topic matrix)
        """
        if self.document_term_matrix is None:
            self.preprocess()
        
        logger.info(f"\nFitting LDA model with {self.n_topics} topics...")
        
        try:
            from sklearn.decomposition import LatentDirichletAllocation
        except ImportError:
            logger.error("scikit-learn not installed")
            return None, None
        
        # Fit LDA
        self.model = LatentDirichletAllocation(
            n_components=self.n_topics,
            max_iter=n_iter,
            learning_method='online',
            random_state=random_state,
            n_jobs=-1
        )
        
        document_topics = self.model.fit_transform(self.document_term_matrix)
        
        logger.info("  ✓ LDA model fitted")
        logger.info(f"    Perplexity: {self.model.perplexity(self.document_term_matrix):.2f}")
        
        return self.model.components_, document_topics
    
    def get_top_words(self, n_words: int = 10) -> Dict[int, List[Tuple[str, float]]]:
        """
        Get top words for each topic
        
        Args:
            n_words: Number of top words to return
        
        Returns:
            Dictionary mapping topic ID to list of (word, weight) tuples
        """
        if self.model is None:
            logger.error("Model not fitted. Run fit_lda() first.")
            return None
        
        topics = {}
        
        for topic_idx, topic in enumerate(self.model.components_):
            top_indices = topic.argsort()[-n_words:][::-1]
            top_words = [(self.feature_names[i], topic[i]) for i in top_indices]
            topics[topic_idx] = top_words
        
        return topics
    
    def print_topics(self, n_words: int = 10):
        """
        Print top words for each topic
        
        Args:
            n_words: Number of words to display per topic
        """
        topics = self.get_top_words(n_words)
        
        if topics is None:
            return
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Top {n_words} words per topic:")
        logger.info(f"{'='*60}")
        
        for topic_id, words in topics.items():
            words_str = ", ".join([word for word, weight in words])
            logger.info(f"\nTopic {topic_id}:")
            logger.info(f"  {words_str}")
    
    def get_document_topics(self, threshold: float = 0.1) -> pd.DataFrame:
        """
        Get dominant topics for each document
        
        Args:
            threshold: Minimum topic weight to include
        
        Returns:
            DataFrame with document topic assignments
        """
        if self.model is None:
            logger.error("Model not fitted. Run fit_lda() first.")
            return None
        
        document_topics = self.model.transform(self.document_term_matrix)
        
        results = []
        for doc_idx, topic_dist in enumerate(document_topics):
            # Get dominant topic
            dominant_topic = topic_dist.argmax()
            dominant_weight = topic_dist[dominant_topic]
            
            # Get all topics above threshold
            above_threshold = [(i, weight) for i, weight in enumerate(topic_dist) 
                             if weight >= threshold]
            
            results.append({
                'document_id': doc_idx,
                'dominant_topic': dominant_topic,
                'dominant_weight': dominant_weight,
                'topic_distribution': topic_dist.tolist(),
                'n_topics_above_threshold': len(above_threshold)
            })
        
        return pd.DataFrame(results)
    
    def visualize_topics(self, save_path: str = None):
        """
        Create visualization of topics
        
        Args:
            save_path: Path to save figure (optional)
        """
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns
        except ImportError:
            logger.error("matplotlib/seaborn not installed")
            return
        
        if self.model is None:
            logger.error("Model not fitted. Run fit_lda() first.")
            return
        
        # Get top words
        topics = self.get_top_words(n_words=10)
        
        # Create figure
        n_topics = len(topics)
        fig, axes = plt.subplots(n_topics, 1, figsize=(12, 3*n_topics))
        
        if n_topics == 1:
            axes = [axes]
        
        for topic_id, words in topics.items():
            ax = axes[topic_id]
            
            words_list = [word for word, weight in words]
            weights = [weight for word, weight in words]
            
            ax.barh(words_list, weights, color='steelblue')
            ax.set_xlabel('Weight')
            ax.set_title(f'Topic {topic_id}', fontweight='bold')
            ax.invert_yaxis()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"  ✓ Visualization saved: {save_path}")
        
        return fig
    
    def coherence_score(self) -> float:
        """
        Calculate topic coherence (simplified version)
        
        Returns:
            Coherence score
        """
        if self.model is None:
            logger.error("Model not fitted. Run fit_lda() first.")
            return None
        
        # This is a simplified coherence measure
        # For full implementation, use gensim's CoherenceModel
        
        topics = self.get_top_words(n_words=10)
        
        # Calculate average pairwise similarity within topics
        coherences = []
        
        for topic_id, words in topics.items():
            word_indices = [self.vectorizer.vocabulary_[word] 
                          for word, _ in words 
                          if word in self.vectorizer.vocabulary_]
            
            # Co-occurrence matrix for these words
            dtm_subset = self.document_term_matrix[:, word_indices].toarray()
            
            # Calculate pairwise co-occurrence
            n_words = len(word_indices)
            if n_words < 2:
                continue
            
            pairs = []
            for i in range(n_words):
                for j in range(i+1, n_words):
                    co_occur = np.sum((dtm_subset[:, i] > 0) & (dtm_subset[:, j] > 0))
                    pairs.append(co_occur)
            
            if pairs:
                coherences.append(np.mean(pairs))
        
        return np.mean(coherences) if coherences else 0.0
    
    def track_topics_over_time(self, dates: List[str]) -> pd.DataFrame:
        """
        Track topic prevalence over time
        
        Args:
            dates: List of dates corresponding to documents
        
        Returns:
            DataFrame with topic proportions over time
        """
        if self.model is None:
            logger.error("Model not fitted. Run fit_lda() first.")
            return None
        
        if len(dates) != len(self.documents):
            logger.error("Number of dates must match number of documents")
            return None
        
        # Get document-topic matrix
        document_topics = self.model.transform(self.document_term_matrix)
        
        # Create DataFrame
        df = pd.DataFrame(document_topics)
        df.columns = [f'topic_{i}' for i in range(self.n_topics)]
        df['date'] = dates
        
        # Convert dates to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Group by time period and calculate mean topic weights
        df_time = df.groupby('date').mean().reset_index()
        
        return df_time


# Example usage
if __name__ == "__main__":
    # Sample documents (simplified 10-K MD&A excerpts)
    documents = [
        "Our company focuses on innovation and research development to drive growth. We invest heavily in new product development and technology advancement.",
        "Risk management is critical to our operations. We maintain strong internal controls and compliance programs to mitigate operational risks.",
        "Digital transformation initiatives continue to reshape our business model. Cloud computing and data analytics are key strategic priorities.",
        "Customer satisfaction drives our success. We emphasize quality service delivery and building long-term customer relationships.",
        "Supply chain efficiency is essential. We optimize logistics operations and maintain strong relationships with suppliers and distributors.",
        "Our growth strategy emphasizes market expansion through strategic acquisitions and organic growth in emerging markets.",
        "Environmental sustainability is a core value. We invest in renewable energy and implement green manufacturing practices.",
        "Talent development and employee engagement are priorities. We offer competitive compensation and comprehensive training programs.",
    ] * 10  # Repeat to create larger corpus
    
    # Create and fit model
    modeler = TopicModeler(documents, n_topics=5)
    topics, doc_topics = modeler.fit_lda()
    
    # Display results
    modeler.print_topics(n_words=8)
    
    # Get document topic assignments
    doc_topic_df = modeler.get_document_topics()
    logger.info(f"\nDocument topic distribution:")
    logger.info(doc_topic_df.head(10))
    
    # Visualize
    fig = modeler.visualize_topics()
    if fig:
        import matplotlib.pyplot as plt
        plt.show()
    
    # Coherence score
    coherence = modeler.coherence_score()
    logger.info(f"\nTopic coherence: {coherence:.4f}")
