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

    def analyze_meter(self, poem):
        """Analyze the metrical pattern of a poem"""
        lines = [line.strip() for line in poem.split('\n') if line.strip()]
        meter_patterns = []

        for line in lines:
            words = line.split()
            pattern = []

            for word in words:
                phones = pronouncing.phones_for_word(word)
                if phones:
                    stresses = pronouncing.stresses(phones[0])
                    pattern.extend([int(s) for s in stresses])
                else:
                    # Fallback to alternating stress pattern
                    syllables = self.count_syllables(word)
                    pattern.extend([1, 0] * (syllables // 2) + ([1] if syllables % 2 else []))

            meter_patterns.append(pattern)

        return meter_patterns

    def analyze_alliteration(self, poem):
        """Detect alliteration in the poem"""
        doc = self.nlp(poem)
        alliterations = []
        current_sound = None
        current_group = []

        for token in doc:
            if token.is_alpha and len(token.text) > 2:
                sound = token.text[0].lower()
                if sound == current_sound:
                    current_group.append(token.text)
                else:
                    if len(current_group) > 2:
                        alliterations.append(current_group[:])
                    current_sound = sound
                    current_group = [token.text]

        if len(current_group) > 2:
            alliterations.append(current_group)

        return alliterations

    def analyze_imagery(self, poem):
        """Analyze types of imagery used in the poem"""
        from vocabulary import (
            nature_words, emotion_words,
            abstract_words, sensory_words
        )

        imagery = defaultdict(list)
        doc = self.nlp(poem.lower())

        # Check against our vocabulary categories
        for token in doc:
            word = token.text.lower()

            if word in nature_words.get_all_nature_words():
                imagery['nature'].append(word)
            if word in emotion_words.get_all_emotion_words():
                imagery['emotional'].append(word)
            if word in abstract_words.get_all_abstract_words():
                imagery['abstract'].append(word)
            if word in sensory_words.get_all_sensory_words():
                imagery['sensory'].append(word)

        return dict(imagery)

    def analyze_sentiment(self, poem):
        """Analyze the emotional tone of the poem"""
        blob = TextBlob(poem)

        # Overall sentiment
        sentiment = {
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity
        }

        # Emotion detection
        from vocabulary.emotion_words import EMOTIONS
        emotion_counts = defaultdict(int)

        for sentence in blob.sentences:
            words = sentence.words.lower()
            for emotion, word_list in EMOTIONS.items():
                emotion_counts[emotion] += sum(1 for word in words if word in word_list)

        sentiment['dominant_emotions'] = sorted(
            emotion_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]

        return sentiment

    def analyze_sound_devices(self, poem):
        """Analyze various sound devices in the poem"""
        devices = {
            'rhyme_scheme': self.analyze_rhyme_scheme(poem),
            'alliteration': self.analyze_alliteration(poem),
            'meter_patterns': self.analyze_meter(poem),
            'assonance': self._find_assonance(poem),
            'consonance': self._find_consonance(poem)
        }
        return devices

    def _find_assonance(self, poem):
        """Find instances of assonance (repeated vowel sounds)"""
        vowels = 'aeiou'
        words = poem.lower().split()
        assonance_patterns = defaultdict(list)

        for word in words:
            vowel_pattern = ''.join(char for char in word if char in vowels)
            if len(vowel_pattern) >= 2:
                assonance_patterns[vowel_pattern].append(word)

        return {k: v for k, v in assonance_patterns.items() if len(v) >= 2}

    def _find_consonance(self, poem):
        """Find instances of consonance (repeated consonant sounds)"""
        consonants = ''.join(c for c in string.ascii_lowercase if c not in 'aeiou')
        words = poem.lower().split()
        consonance_patterns = defaultdict(list)

        for word in words:
            consonant_pattern = ''.join(char for char in word if char in consonants)
            if len(consonant_pattern) >= 2:
                consonance_patterns[consonant_pattern].append(word)

        return {k: v for k, v in consonance_patterns.items() if len(v) >= 2}

    def get_complete_analysis(self, poem):
        """Perform a complete analysis of the poem"""
        analysis = {
            'sound_devices': self.analyze_sound_devices(poem),
            'imagery': self.analyze_imagery(poem),
            'sentiment': self.analyze_sentiment(poem),
            'meter': self.analyze_meter(poem),
            'structure': {
                'lines': len(poem.split('\n')),
                'words': len(poem.split()),
                'syllables_per_line': [
                    sum(self.count_syllables(word) for word in line.split())
                    for line in poem.split('\n') if line.strip()
                ]
            }
        }
        return analysis
