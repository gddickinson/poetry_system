"""Poetry analysis module for detecting rhythm, rhyme, and other poetic elements."""

import spacy
import pronouncing
from textblob import TextBlob
from collections import defaultdict
import string
import numpy as np
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vocabulary import (
    nature_words,
    emotion_words,
    abstract_words,
    sensory_words
)

class PoetryAnalyzer:
    def __init__(self):
        """Initialize the poetry analyzer with required NLP tools"""
        self.nlp = spacy.load('en_core_web_sm')
        self.pos_to_words = defaultdict(list)
        self.rhyme_dict = defaultdict(list)
        self.syllable_patterns = []
        
    def count_syllables(self, word):
        """Count syllables in a word using pronouncing dictionary"""
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
        except:
            return 1
    
    def analyze_rhyme_scheme(self, poem):
        """Detect the rhyme scheme of a poem"""
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
        """Analyze types of imagery used in the poem"""
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
        """Analyze the emotional tone of the poem"""
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