"""Poetry analysis module for detecting rhythm, rhyme, and other poetic elements."""

import spacy
import pronouncing
from textblob import TextBlob
from collections import defaultdict
import string
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

class PoetryAnalyzer:
    def __init__(self):
        """Initialize the poetry analyzer with required NLP tools.

        Raises:
            OSError: If spaCy model 'en_core_web_sm' is not installed.
                     Install it with: python -m spacy download en_core_web_sm
        """
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
        
    def count_syllables(self, word):
        """Count syllables in a word using pronouncing dictionary.

        Args:
            word: A single word string.

        Returns:
            int: Syllable count (minimum 1).
        """
        if not word or not isinstance(word, str):
            return 1
        word = word.strip()
        if not word:
            return 1
        try:
            phones = pronouncing.phones_for_word(word)
            if phones:
                return len(pronouncing.stresses(phones[0]))
            
            # Fallback syllable counting
            count = 0
            vowels = 'aeiouy'
            word = word.lower().strip('.,!?')
            if word[0] in vowels:
                count += 1
            for index in range(1, len(word)):
                if word[index] in vowels and word[index-1] not in vowels:
                    count += 1
            if word.endswith('e'):
                count -= 1
            return max(1, count)
        except (IndexError, KeyError, ValueError):
            return 1
    
    def analyze_rhyme_scheme(self, poem):
        """Detect the rhyme scheme of a poem.

        Args:
            poem: Multi-line poem string.

        Returns:
            str: Rhyme scheme letters (e.g. 'ABAB'), empty string if poem is empty.
        """
        if not poem or not isinstance(poem, str) or not poem.strip():
            return ''
        def clean_word(word):
            return word.lower().strip(string.punctuation)
        
        lines = [line.strip() for line in poem.split('\n') if line.strip()]
        rhyme_scheme = []
        rhyme_mapping = {}
        current_rhyme = 0
        
        for line in lines:
            words = line.split()
            if not words:
                continue
            
            last_word = clean_word(words[-1])
            rhymes = pronouncing.rhymes(last_word)
            rhyme_key = tuple(rhymes[:3]) if rhymes else last_word
            
            if rhyme_key not in rhyme_mapping:
                rhyme_mapping[rhyme_key] = chr(65 + current_rhyme)
                current_rhyme += 1
            
            rhyme_scheme.append(rhyme_mapping[rhyme_key])
        
        return ''.join(rhyme_scheme)
    
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