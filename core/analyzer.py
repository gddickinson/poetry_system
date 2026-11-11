"""Poetry analysis module for detecting rhythm, rhyme, and other poetic elements."""

from collections import defaultdict
import sys
import os

# Ensure parent directory is importable for vocabulary package
_parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

from vocabulary import (
    nature_words,
    emotion_words,
    abstract_words,
    sensory_words
)
from core.prosody import ProsodyAnalyzer


class PoetryAnalyzer(ProsodyAnalyzer):
    """Full analyzer: syllables and rhyme (from ProsodyAnalyzer) plus imagery and sentiment.

    spaCy and TextBlob are imported when needed, so the pure prosody helpers (and the
    generator and web interface) work without the NLP models installed.
    """

    def __init__(self):
        """Initialize the poetry analyzer with required NLP tools.

        Raises:
            OSError: If spaCy model 'en_core_web_sm' is not installed.
                     Install it with: python -m spacy download en_core_web_sm
        """
        import spacy
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except OSError:
            raise OSError(
                "spaCy model 'en_core_web_sm' not found. "
                "Install it with: python -m spacy download en_core_web_sm"
            )
        self.pos_to_words = defaultdict(list)
        self.rhyme_dict = defaultdict(list)
        self.syllable_patterns = []
        
    def analyze_imagery(self, poem):
        """Analyze types of imagery used in the poem.

        Returns empty dict for empty/invalid input.
        """
        if not poem or not isinstance(poem, str) or not poem.strip():
            return {}
        imagery = defaultdict(list)
        doc = self.nlp(poem.lower())
        
        # Get all words from our vocabulary modules
        nature_vocab = set(nature_words.get_all_nature_words())
        emotion_vocab = set(emotion_words.get_all_emotion_words())
        abstract_vocab = set(abstract_words.get_all_abstract_words())
        sensory_vocab = set(sensory_words.get_all_sensory_words())
        
        for token in doc:
            word = token.text.lower()
            
            if word in nature_vocab:
                imagery['nature'].append(word)
            if word in emotion_vocab:
                imagery['emotional'].append(word)
            if word in abstract_vocab:
                imagery['abstract'].append(word)
            if word in sensory_vocab:
                imagery['sensory'].append(word)
        
        return dict(imagery)
    
    def analyze_sentiment(self, poem):
        """Analyze the emotional tone of the poem.

        Returns neutral sentiment for empty/invalid input.
        """
        if not poem or not isinstance(poem, str) or not poem.strip():
            return {'polarity': 0.0, 'subjectivity': 0.0, 'emotion_count': {}}
        from textblob import TextBlob
        blob = TextBlob(poem)
        sentiment = {
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity
        }
        
        # Count emotion words
        emotion_counts = defaultdict(int)
        doc = self.nlp(poem.lower())
        
        for token in doc:
            word = token.text.lower()
            # Check against emotion vocabulary
            for emotion_word in emotion_words.get_all_emotion_words():
                if word == emotion_word:
                    emotion_counts['emotional'] += 1
        
        sentiment['emotion_count'] = dict(emotion_counts)
        return sentiment