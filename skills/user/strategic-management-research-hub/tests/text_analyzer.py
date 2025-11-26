"""
Strategic Management Research Hub - Text Analyzer Module
=========================================================

Advanced text analysis for strategic management research:
- MD&A (Management Discussion & Analysis) Analysis
- Patent Abstract & Claims Analysis
- Press Release Sentiment & Topic Analysis
- 10-K/Annual Report Textual Features
- Strategic Language & Framing Analysis

Methods: NLP, Topic Modeling (LDA/BERTopic), Sentiment Analysis, Readability

Author: Strategic Management Research Hub
Version: 3.0
License: MIT

References:
- Li (2010): Textual Analysis of Corporate Disclosures. JAR
- Loughran & McDonald (2011): Finance-Specific Dictionary. JF
- Kaplan & Vakili (2015): Patent Textual Attributes. SMJ
- Short & Palmer (2008): Strategic Rhetoric. SMJ
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple, Union, Set
import logging
from pathlib import Path
import re
import string
from collections import Counter, defaultdict
import warnings

# NLP libraries
try:
    import nltk
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer, WordNetLemmatizer
    NLTK_AVAILABLE = True
    
    # Download required NLTK data
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
except ImportError:
    NLTK_AVAILABLE = False
    warnings.warn("NLTK not installed. Some text analysis features will be limited.")

# Advanced NLP
try:
    from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
    from sklearn.decomposition import LatentDirichletAllocation
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    warnings.warn("scikit-learn not installed. Topic modeling unavailable.")

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False
    warnings.warn("TextBlob not installed. Sentiment analysis will use basic method.")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LoughranMcDonaldDictionary:
    """
    Loughran & McDonald (2011) Finance-Specific Sentiment Dictionary.
    
    Standard sentiment dictionaries (e.g., Harvard GI) perform poorly in
    financial contexts. LM dictionary is specifically designed for 10-Ks.
    
    Categories:
    - Negative: litigious, uncertain, constraining, negative emotion
    - Positive: positive emotion
    - Uncertainty: modal words suggesting uncertainty
    - Litigious: legal/regulatory language
    - Constraining: limiting conditions
    
    Reference:
    Loughran, T., & McDonald, B. (2011). When is a liability not a liability?
    Textual analysis, dictionaries, and 10-Ks. The Journal of Finance, 66(1), 35-65.
    """
    
    def __init__(self):
        """Initialize LM dictionary (simplified version for demonstration)."""
        
        # Negative words
        self.negative = {
            'adverse', 'adversely', 'allegations', 'antitrust', 'bankruptcy', 'breach',
            'cancel', 'cancelled', 'catastrophe', 'closure', 'complaint', 'complaints',
            'conflict', 'critical', 'damage', 'damages', 'decline', 'declined', 'declining',
            'default', 'deficiency', 'deficit', 'delinquent', 'deteriorate', 'deteriorated',
            'deteriorating', 'difficult', 'difficulty', 'discontinue', 'discontinued',
            'discrimination', 'dismissal', 'dispute', 'disputed', 'downturn', 'elimination',
            'embargo', 'encumbered', 'fail', 'failed', 'failing', 'fails', 'failure',
            'felony', 'force', 'forced', 'fraud', 'fraudulent', 'impair', 'impaired',
            'impairment', 'inadequate', 'inability', 'incur', 'incurred', 'infringement',
            'insolvent', 'investigation', 'lawsuit', 'lawsuits', 'liability', 'liabilities',
            'litigation', 'loss', 'losses', 'negative', 'negatively', 'noncompliance',
            'obligation', 'obsolete', 'penalty', 'penalties', 'problem', 'problems',
            'recession', 'regulatory', 'rejection', 'remediation', 'restructuring',
            'risk', 'risks', 'slowdown', 'substantial', 'significantly', 'terminate',
            'terminated', 'termination', 'unfavorable', 'unfavorably', 'unpaid',
            'violation', 'violations', 'volatility', 'vulnerable', 'weakness', 'write-down'
        }
        
        # Positive words
        self.positive = {
            'able', 'abundance', 'abundant', 'accomplish', 'accomplished', 'accomplishment',
            'achieve', 'achieved', 'achievement', 'achievements', 'achieving', 'adequate',
            'advancement', 'advances', 'advantage', 'advantageous', 'advantages', 'advanced',
            'attractive', 'benefit', 'benefits', 'beneficial', 'benefited', 'bolster',
            'bolstered', 'boosting', 'collaboration', 'competitive', 'competitively',
            'confidence', 'confident', 'constructive', 'creative', 'dedication', 'delight',
            'delighted', 'efficient', 'efficiently', 'enhance', 'enhanced', 'enhancement',
            'enhancements', 'enhancing', 'enjoy', 'enjoyed', 'excellent', 'exceptional',
            'exceptionally', 'excel', 'excelled', 'exciting', 'gain', 'gained', 'gains',
            'great', 'greater', 'greatest', 'greatly', 'grew', 'grow', 'growing', 'grown',
            'growth', 'high', 'higher', 'highest', 'improve', 'improved', 'improvement',
            'improvements', 'improving', 'innovation', 'innovative', 'innovate', 'leadership',
            'leading', 'opportunity', 'opportunities', 'optimal', 'optimistic', 'positive',
            'positively', 'proficiency', 'proficient', 'profit', 'profitability', 'profitable',
            'profits', 'progress', 'progressed', 'progressing', 'prosperity', 'prosperous',
            'rebound', 'rebounded', 'recovery', 'robust', 'strength', 'strengthen',
            'strengthened', 'strengthening', 'strong', 'stronger', 'strongest', 'succeed',
            'succeeded', 'succeeding', 'success', 'successes', 'successful', 'successfully',
            'superior', 'talent', 'talented', 'unique', 'valuable', 'value', 'values'
        }
        
        # Uncertainty words
        self.uncertainty = {
            'approximate', 'approximately', 'believe', 'believes', 'believing', 'cautious',
            'could', 'depend', 'depending', 'estimate', 'estimated', 'estimates', 'estimating',
            'expect', 'expected', 'expecting', 'forecast', 'forecasted', 'forecasting',
            'guidance', 'indicate', 'indicated', 'indicates', 'indicating', 'intend',
            'intended', 'intending', 'intends', 'likely', 'may', 'might', 'pending',
            'possible', 'possibly', 'potential', 'potentially', 'predict', 'predicted',
            'predicting', 'projected', 'projecting', 'projection', 'projections', 'risk',
            'risks', 'risky', 'should', 'uncertain', 'uncertainties', 'uncertainty',
            'unclear', 'unpredictable', 'variable', 'variability', 'vary', 'varies'
        }
        
        # Litigious words
        self.litigious = {
            'action', 'allegation', 'allegations', 'allege', 'alleged', 'alleging',
            'claim', 'claims', 'claimant', 'claimants', 'complaint', 'complaints',
            'contract', 'contractual', 'court', 'courts', 'defendant', 'defendants',
            'dispute', 'disputed', 'disputes', 'disputing', 'enforce', 'enforcement',
            'infringement', 'injunction', 'judge', 'judgment', 'judicial', 'jurisdiction',
            'law', 'laws', 'lawsuit', 'lawsuits', 'legal', 'legally', 'legislation',
            'legislative', 'liability', 'liabilities', 'liable', 'litigation', 'litigations',
            'patent', 'patents', 'plaintiff', 'plaintiffs', 'proceeding', 'proceedings',
            'prosecute', 'prosecuting', 'prosecution', 'regulatory', 'regulations',
            'settlement', 'settlements', 'statute', 'statutes', 'sue', 'sued', 'suing',
            'suit', 'suits', 'tort', 'torts', 'trial', 'trials', 'violate', 'violated',
            'violation', 'violations'
        }
        
        # Constraining words
        self.constraining = {
            'bound', 'bounded', 'commitment', 'commitments', 'comply', 'complying',
            'compulsory', 'constraint', 'constraints', 'contingent', 'covenant', 'covenants',
            'dependent', 'enforce', 'enforcement', 'mandated', 'mandatory', 'must',
            'obligate', 'obligated', 'obligation', 'obligations', 'prohibit', 'prohibited',
            'prohibition', 'provisions', 'regulate', 'regulated', 'regulation', 'regulations',
            'regulatory', 'require', 'required', 'requirement', 'requirements', 'requiring',
            'requires', 'restriction', 'restrictions', 'restrictive', 'shall', 'should',
            'statutory', 'subject', 'subjected', 'unable'
        }
        
        logger.info("Loughran-McDonald dictionary initialized")
        
    def score_text(self, text: str) -> Dict[str, Union[int, float]]:
        """
        Score text using LM dictionary.
        
        Parameters:
        -----------
        text : str
            Text to analyze
            
        Returns:
        --------
        scores : dict
            Dictionary of sentiment scores
        """
        # Tokenize and clean
        words = text.lower().split()
        total_words = len(words)
        
        if total_words == 0:
            return {
                'negative_count': 0,
                'positive_count': 0,
                'uncertainty_count': 0,
                'litigious_count': 0,
                'constraining_count': 0,
                'negative_ratio': 0,
                'positive_ratio': 0,
                'uncertainty_ratio': 0,
                'litigious_ratio': 0,
                'constraining_ratio': 0,
                'net_sentiment': 0
            }
            
        # Count words in each category
        negative_count = sum(1 for w in words if w in self.negative)
        positive_count = sum(1 for w in words if w in self.positive)
        uncertainty_count = sum(1 for w in words if w in self.uncertainty)
        litigious_count = sum(1 for w in words if w in self.litigious)
        constraining_count = sum(1 for w in words if w in self.constraining)
        
        # Compute ratios
        scores = {
            'negative_count': negative_count,
            'positive_count': positive_count,
            'uncertainty_count': uncertainty_count,
            'litigious_count': litigious_count,
            'constraining_count': constraining_count,
            'total_words': total_words,
            'negative_ratio': negative_count / total_words,
            'positive_ratio': positive_count / total_words,
            'uncertainty_ratio': uncertainty_count / total_words,
            'litigious_ratio': litigious_count / total_words,
            'constraining_ratio': constraining_count / total_words,
            'net_sentiment': (positive_count - negative_count) / total_words
        }
        
        return scores


class MDAAnalyzer:
    """
    Analyze Management Discussion & Analysis (MD&A) sections from 10-K filings.
    
    MD&A provides qualitative disclosure about firm operations, performance,
    and future outlook. Textual features predict future performance and risk.
    
    Usage:
    ```python
    analyzer = MDAAnalyzer()
    
    # Analyze MD&A text
    results = analyzer.analyze_mda(mda_text)
    
    # Batch process multiple MD&As
    df = pd.read_csv('mda_texts.csv')
    df_analyzed = analyzer.batch_analyze(df, text_column='mda_text')
    ```
    
    Metrics Computed:
    - **Sentiment**: LM positive/negative tone
    - **Uncertainty**: Modal words, risk mentions
    - **Readability**: Fog Index, Flesch-Kincaid
    - **Specificity**: Numeric vs. vague language
    - **Forward-looking**: Future-oriented language
    - **Length & Complexity**: Word count, avg sentence length
    """
    
    def __init__(self):
        self.lm_dict = LoughranMcDonaldDictionary()
        self.stemmer = PorterStemmer() if NLTK_AVAILABLE else None
        
    def analyze_mda(self, text: str) -> Dict[str, Union[int, float]]:
        """
        Comprehensive analysis of MD&A text.
        
        Parameters:
        -----------
        text : str
            MD&A text
            
        Returns:
        --------
        metrics : dict
            Dictionary of textual metrics
        """
        if not text or len(text.strip()) == 0:
            return self._empty_metrics()
            
        metrics = {}
        
        # 1. Basic text statistics
        metrics.update(self._compute_basic_stats(text))
        
        # 2. LM sentiment
        lm_scores = self.lm_dict.score_text(text)
        metrics.update(lm_scores)
        
        # 3. Readability
        metrics.update(self._compute_readability(text))
        
        # 4. Forward-looking language
        metrics['forward_looking_ratio'] = self._compute_forward_looking(text)
        
        # 5. Specificity (numeric mentions)
        metrics['numeric_ratio'] = self._compute_specificity(text)
        
        # 6. Risk mentions
        metrics['risk_mentions'] = self._count_risk_mentions(text)
        
        return metrics
        
    def _compute_basic_stats(self, text: str) -> Dict[str, Union[int, float]]:
        """Compute basic text statistics."""
        # Word count
        words = text.split()
        word_count = len(words)
        
        # Sentence count
        if NLTK_AVAILABLE:
            sentences = sent_tokenize(text)
        else:
            sentences = text.split('.')
        sentence_count = len(sentences)
        
        # Average sentence length
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        
        # Character count
        char_count = len(text)
        
        # Unique words
        unique_words = len(set(w.lower() for w in words))
        lexical_diversity = unique_words / word_count if word_count > 0 else 0
        
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_sentence_length': avg_sentence_length,
            'char_count': char_count,
            'unique_words': unique_words,
            'lexical_diversity': lexical_diversity
        }
        
    def _compute_readability(self, text: str) -> Dict[str, float]:
        """
        Compute readability metrics.
        
        - **Fog Index**: Grade level needed to understand text
        - **Flesch Reading Ease**: 0-100 scale (higher = easier)
        """
        words = text.split()
        
        if NLTK_AVAILABLE:
            sentences = sent_tokenize(text)
        else:
            sentences = text.split('.')
            
        word_count = len(words)
        sentence_count = len(sentences)
        
        if word_count == 0 or sentence_count == 0:
            return {'fog_index': 0, 'flesch_reading_ease': 0}
            
        # Fog Index = 0.4 * (avg_sentence_length + percent_complex_words)
        avg_sentence_length = word_count / sentence_count
        
        # Complex words: 3+ syllables
        complex_words = sum(1 for w in words if self._count_syllables(w) >= 3)
        percent_complex = (complex_words / word_count) * 100
        
        fog_index = 0.4 * (avg_sentence_length + percent_complex)
        
        # Flesch Reading Ease = 206.835 - 1.015(total_words/total_sentences) 
        #                       - 84.6(total_syllables/total_words)
        total_syllables = sum(self._count_syllables(w) for w in words)
        flesch_reading_ease = 206.835 - 1.015 * (word_count / sentence_count) \
                             - 84.6 * (total_syllables / word_count)
                             
        return {
            'fog_index': fog_index,
            'flesch_reading_ease': max(0, min(100, flesch_reading_ease))  # Cap at 0-100
        }
        
    def _count_syllables(self, word: str) -> int:
        """Estimate syllable count (simplified)."""
        word = word.lower()
        vowels = 'aeiouy'
        syllable_count = 0
        previous_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel
            
        # Adjust for silent 'e'
        if word.endswith('e'):
            syllable_count -= 1
            
        # Every word has at least 1 syllable
        return max(1, syllable_count)
        
    def _compute_forward_looking(self, text: str) -> float:
        """Compute proportion of forward-looking language."""
        forward_words = {
            'will', 'would', 'expect', 'anticipate', 'intend', 'plan', 'project',
            'forecast', 'outlook', 'future', 'upcoming', 'next', 'going forward',
            'believe', 'should', 'may', 'could', 'might', 'aim', 'goal', 'target'
        }
        
        words = text.lower().split()
        forward_count = sum(1 for w in words if w in forward_words)
        
        return forward_count / len(words) if len(words) > 0 else 0
        
    def _compute_specificity(self, text: str) -> float:
        """Compute proportion of numeric/specific language."""
        # Count numeric tokens
        words = text.split()
        numeric_pattern = r'\d+'
        numeric_count = sum(1 for w in words if re.search(numeric_pattern, w))
        
        return numeric_count / len(words) if len(words) > 0 else 0
        
    def _count_risk_mentions(self, text: str) -> int:
        """Count mentions of 'risk' and related terms."""
        risk_words = ['risk', 'risks', 'risky', 'uncertainty', 'uncertainties', 'uncertain']
        text_lower = text.lower()
        
        return sum(text_lower.count(word) for word in risk_words)
        
    def _empty_metrics(self) -> Dict:
        """Return empty metrics for null text."""
        return {
            'word_count': 0,
            'sentence_count': 0,
            'avg_sentence_length': 0,
            'char_count': 0,
            'unique_words': 0,
            'lexical_diversity': 0,
            'negative_count': 0,
            'positive_count': 0,
            'uncertainty_count': 0,
            'litigious_count': 0,
            'constraining_count': 0,
            'total_words': 0,
            'negative_ratio': 0,
            'positive_ratio': 0,
            'uncertainty_ratio': 0,
            'litigious_ratio': 0,
            'constraining_ratio': 0,
            'net_sentiment': 0,
            'fog_index': 0,
            'flesch_reading_ease': 0,
            'forward_looking_ratio': 0,
            'numeric_ratio': 0,
            'risk_mentions': 0
        }
        
    def batch_analyze(
        self,
        df: pd.DataFrame,
        text_column: str,
        id_columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Batch process multiple MD&A texts.
        
        Parameters:
        -----------
        df : DataFrame
            Input data with text column
        text_column : str
            Name of column containing MD&A text
        id_columns : list, optional
            Columns to keep as identifiers (e.g., ['company_id', 'year'])
            
        Returns:
        --------
        results_df : DataFrame
            Original data with textual metrics added
        """
        logger.info(f"Batch analyzing {len(df)} MD&A texts...")
        
        # Analyze each text
        metrics_list = []
        for idx, row in df.iterrows():
            text = row[text_column]
            metrics = self.analyze_mda(text)
            
            # Add identifiers
            if id_columns:
                for col in id_columns:
                    metrics[col] = row[col]
                    
            metrics_list.append(metrics)
            
            if (idx + 1) % 100 == 0:
                logger.info(f"Processed {idx + 1}/{len(df)} texts")
                
        results_df = pd.DataFrame(metrics_list)
        
        # Reorder columns to put IDs first
        if id_columns:
            other_cols = [c for c in results_df.columns if c not in id_columns]
            results_df = results_df[id_columns + other_cols]
            
        logger.info("Batch analysis complete")
        return results_df


class PatentTextAnalyzer:
    """
    Analyze patent abstracts and claims for technological characteristics.
    
    Patent text contains rich information about innovation:
    - **Breadth**: Scope of technology covered
    - **Radicalness**: Novelty vs. incremental
    - **Generality**: Applicability across domains
    
    Usage:
    ```python
    analyzer = PatentTextAnalyzer()
    
    # Analyze single patent
    metrics = analyzer.analyze_patent(abstract, claims)
    
    # Batch process
    df = pd.read_csv('patents.csv')
    df_analyzed = analyzer.batch_analyze(df, abstract_col='abstract', claims_col='claims')
    ```
    
    References:
    - Kaplan & Vakili (2015): Patent Scope. SMJ
    - Lanjouw & Schankerman (2004): Patent Quality. AER
    """
    
    def __init__(self):
        self.stemmer = PorterStemmer() if NLTK_AVAILABLE else None
        
    def analyze_patent(
        self,
        abstract: str,
        claims: Optional[str] = None
    ) -> Dict[str, Union[int, float]]:
        """
        Analyze patent text for technological characteristics.
        
        Parameters:
        -----------
        abstract : str
            Patent abstract
        claims : str, optional
            Patent claims text
            
        Returns:
        --------
        metrics : dict
            Patent textual metrics
        """
        metrics = {}
        
        # 1. Basic statistics
        abstract_words = abstract.split() if abstract else []
        metrics['abstract_word_count'] = len(abstract_words)
        
        if claims:
            claims_words = claims.split()
            metrics['claims_word_count'] = len(claims_words)
            metrics['total_word_count'] = len(abstract_words) + len(claims_words)
        else:
            metrics['claims_word_count'] = 0
            metrics['total_word_count'] = len(abstract_words)
            
        # 2. Claim count (number of claims)
        if claims:
            # Claims typically separated by numbered claims (1., 2., etc.)
            claim_count = len(re.findall(r'\d+\.', claims))
            metrics['claim_count'] = claim_count
        else:
            metrics['claim_count'] = 0
            
        # 3. Independent claims (broader scope)
        # Independent claims don't reference other claims
        if claims:
            independent_pattern = r'\d+\.\s+(?!.*claim \d+)'
            independent_claims = len(re.findall(independent_pattern, claims, re.IGNORECASE))
            metrics['independent_claims'] = independent_claims
        else:
            metrics['independent_claims'] = 0
            
        # 4. Breadth proxy: unique technical terms
        tech_terms = self._extract_technical_terms(abstract)
        metrics['unique_tech_terms'] = len(tech_terms)
        
        # 5. Complexity: average word length
        if abstract_words:
            avg_word_length = np.mean([len(w) for w in abstract_words])
            metrics['avg_word_length'] = avg_word_length
        else:
            metrics['avg_word_length'] = 0
            
        return metrics
        
    def _extract_technical_terms(self, text: str) -> Set[str]:
        """Extract technical terms (heuristic: long words, compound words)."""
        words = text.lower().split()
        
        # Technical terms tend to be longer
        tech_terms = set()
        for word in words:
            # Remove punctuation
            word = word.strip(string.punctuation)
            
            # Technical terms: length >= 8 or contains hyphens/numbers
            if len(word) >= 8 or '-' in word or any(c.isdigit() for c in word):
                tech_terms.add(word)
                
        return tech_terms
        
    def compute_patent_breadth(
        self,
        abstract: str,
        ipc_codes: Optional[List[str]] = None
    ) -> float:
        """
        Compute patent breadth score.
        
        Breadth = f(unique_tech_terms, ipc_diversity, claim_count)
        
        Parameters:
        -----------
        abstract : str
            Patent abstract
        ipc_codes : list, optional
            IPC classification codes (e.g., ['A01B', 'B02C'])
            
        Returns:
        --------
        breadth_score : float
            Higher = broader patent scope
        """
        # Component 1: Textual diversity
        tech_terms = self._extract_technical_terms(abstract)
        textual_breadth = len(tech_terms)
        
        # Component 2: IPC diversity (if available)
        if ipc_codes:
            # Count unique 4-digit IPC codes
            unique_ipc = len(set(code[:4] for code in ipc_codes))
            ipc_breadth = unique_ipc
        else:
            ipc_breadth = 0
            
        # Combined breadth score (normalized)
        breadth_score = np.log1p(textual_breadth) + np.log1p(ipc_breadth)
        
        return breadth_score
        
    def batch_analyze(
        self,
        df: pd.DataFrame,
        abstract_col: str,
        claims_col: Optional[str] = None,
        id_columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Batch process multiple patents.
        
        Parameters:
        -----------
        df : DataFrame
            Patent data
        abstract_col : str
            Column name for abstracts
        claims_col : str, optional
            Column name for claims
        id_columns : list, optional
            ID columns to keep
            
        Returns:
        --------
        results_df : DataFrame
            Patent data with textual metrics
        """
        logger.info(f"Batch analyzing {len(df)} patents...")
        
        metrics_list = []
        for idx, row in df.iterrows():
            abstract = row[abstract_col] if pd.notna(row[abstract_col]) else ""
            claims = row[claims_col] if claims_col and pd.notna(row[claims_col]) else None
            
            metrics = self.analyze_patent(abstract, claims)
            
            # Add identifiers
            if id_columns:
                for col in id_columns:
                    metrics[col] = row[col]
                    
            metrics_list.append(metrics)
            
            if (idx + 1) % 1000 == 0:
                logger.info(f"Processed {idx + 1}/{len(df)} patents")
                
        results_df = pd.DataFrame(metrics_list)
        
        # Reorder columns
        if id_columns:
            other_cols = [c for c in results_df.columns if c not in id_columns]
            results_df = results_df[id_columns + other_cols]
            
        logger.info("Batch analysis complete")
        return results_df


class TopicModeler:
    """
    Topic modeling using Latent Dirichlet Allocation (LDA).
    
    Discover latent topics in corporate disclosures, press releases, etc.
    
    Usage:
    ```python
    modeler = TopicModeler(n_topics=5)
    
    # Fit model
    modeler.fit(documents)
    
    # Get topic distributions
    topic_dist = modeler.transform(documents)
    
    # Display topics
    modeler.display_topics(n_words=10)
    ```
    
    References:
    - Blei et al. (2003): Latent Dirichlet Allocation. JMLR
    - Kaplan & Vakili (2015): Topic Modeling in Strategy. SMJ
    """
    
    def __init__(self, n_topics: int = 10, max_features: int = 1000):
        """
        Initialize topic modeler.
        
        Parameters:
        -----------
        n_topics : int
            Number of topics to extract
        max_features : int
            Maximum vocabulary size
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("scikit-learn required for topic modeling")
            
        self.n_topics = n_topics
        self.max_features = max_features
        
        # TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            stop_words='english',
            max_df=0.8,  # Remove very common words
            min_df=2     # Remove very rare words
        )
        
        # LDA model
        self.lda_model = LatentDirichletAllocation(
            n_components=n_topics,
            random_state=42,
            max_iter=50
        )
        
        self.fitted = False
        
    def fit(self, documents: List[str]):
        """
        Fit topic model on documents.
        
        Parameters:
        -----------
        documents : list of str
            Text documents
        """
        logger.info(f"Fitting LDA model with {self.n_topics} topics...")
        
        # Vectorize
        X = self.vectorizer.fit_transform(documents)
        
        # Fit LDA
        self.lda_model.fit(X)
        
        self.fitted = True
        logger.info("Model fitting complete")
        
    def transform(self, documents: List[str]) -> np.ndarray:
        """
        Get topic distributions for documents.
        
        Parameters:
        -----------
        documents : list of str
            Text documents
            
        Returns:
        --------
        topic_dist : ndarray
            (n_documents, n_topics) array of topic probabilities
        """
        if not self.fitted:
            raise ValueError("Model not fitted. Call fit() first.")
            
        X = self.vectorizer.transform(documents)
        topic_dist = self.lda_model.transform(X)
        
        return topic_dist
        
    def display_topics(self, n_words: int = 10):
        """
        Display top words for each topic.
        
        Parameters:
        -----------
        n_words : int
            Number of words to display per topic
        """
        if not self.fitted:
            raise ValueError("Model not fitted. Call fit() first.")
            
        feature_names = self.vectorizer.get_feature_names_out()
        
        print("\n" + "=" * 80)
        print("TOPIC MODEL RESULTS")
        print("=" * 80)
        
        for topic_idx, topic in enumerate(self.lda_model.components_):
            top_indices = topic.argsort()[-n_words:][::-1]
            top_words = [feature_names[i] for i in top_indices]
            
            print(f"\nTopic {topic_idx + 1}:")
            print("  " + ", ".join(top_words))
            
        print("\n" + "=" * 80)


# Example usage
if __name__ == "__main__":
    print("=" * 80)
    print("Text Analysis Module - Example Usage")
    print("=" * 80)
    
    # Example 1: MD&A Analysis
    print("\nExample 1: MD&A Analysis")
    print("-" * 80)
    
    sample_mda = """
    Our business continues to face significant challenges due to ongoing 
    supply chain disruptions and increased competition. We expect revenue 
    growth to slow in the coming quarters. However, we remain confident in 
    our strategic initiatives and believe our innovative products will 
    strengthen our market position. We may need to raise additional capital
    to fund our expansion plans. Risks include regulatory changes and 
    potential litigation from patent infringement claims.
    """
    
    analyzer = MDAAnalyzer()
    results = analyzer.analyze_mda(sample_mda)
    
    print("\nMD&A Metrics:")
    for key, value in results.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.4f}")
        else:
            print(f"  {key}: {value}")
            
    # Example 2: Patent Analysis
    print("\n\nExample 2: Patent Text Analysis")
    print("-" * 80)
    
    sample_abstract = """
    A novel machine learning algorithm for real-time anomaly detection in 
    high-dimensional time-series data. The method combines convolutional 
    neural networks with attention mechanisms to achieve state-of-the-art 
    performance. Applications include cybersecurity, financial fraud detection,
    and industrial quality control.
    """
    
    patent_analyzer = PatentTextAnalyzer()
    patent_metrics = patent_analyzer.analyze_patent(sample_abstract)
    
    print("\nPatent Metrics:")
    for key, value in patent_metrics.items():
        print(f"  {key}: {value}")
        
    print("\n" + "=" * 80)
    print("Text analysis module ready for use!")
    print("=" * 80)
