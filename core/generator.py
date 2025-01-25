"""Poetry generation module for creating various forms of poetry."""

import random
from collections import defaultdict
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

class PoetryGenerator:
    def __init__(self, analyzer):
        """Initialize the poetry generator with an analyzer instance"""
        self.analyzer = analyzer
        self.word_cache = self._build_word_cache()
        self.templates = self._load_templates()

    def _build_word_cache(self):
        """Build a cache of words categorized by type and syllable count"""
        cache = defaultdict(lambda: defaultdict(list))

        all_words = {
            'nature': nature_words.get_all_nature_words(),
            'emotion': emotion_words.get_all_emotion_words(),
            'abstract': abstract_words.get_all_abstract_words(),
            'sensory': sensory_words.get_all_sensory_words()
        }

        for category, words in all_words.items():
            for word in words:
                syllables = self.analyzer.count_syllables(word)
                cache[category][syllables].append(word)

        return cache

    def _load_templates(self):
        """Load poetic templates and patterns"""
        return {
            'haiku': {
                'structure': [5, 7, 5],
                'focus': ['nature', 'sensory', 'emotion']
            },
            'tanka': {
                'structure': [5, 7, 5, 7, 7],
                'focus': ['emotion', 'nature', 'abstract']
            },
            'sonnet': {
                'structure': [10] * 14,  # 14 lines of 10 syllables each
                'rhyme_scheme': 'ABABCDCDEFEFGG'
            },
            'free_verse': {
                'min_lines': 4,
                'max_lines': 8,
                'min_syllables': 5,
                'max_syllables': 12
            }
        }

    def _create_metaphor(self, mood=None):
        """Create a metaphorical phrase combining different domains"""
        templates = [
            "like {} in {}",
            "{} of {}",
            "{} beneath {}",
            "{} among {}",
            "through {} like {}",
            "{} within {}"
        ]

        categories = ['nature', 'emotion', 'abstract', 'sensory']
        if mood:
            primary = mood
            secondary = random.choice([c for c in categories if c != mood])
        else:
            primary, secondary = random.sample(categories, 2)

        word1 = random.choice(self.word_cache[primary][random.randint(1, 2)])
        word2 = random.choice(self.word_cache[secondary][random.randint(1, 2)])

        return random.choice(templates).format(word1, word2)

    def _create_image_phrase(self, syllables, mood=None):
        """Create a vivid image phrase with specific syllable count"""
        # Simpler templates that require fewer words
        simple_templates = [
            "{} {}",
            "{} in {}",
            "{} like {}",
            "{} through {}",
        ]

        # More complex templates for when we have more syllables
        complex_templates = [
            "{} {} in the {}",
            "{} like {} {}",
            "{} through the {}",
            "where {} meets {}",
            "{} of {} {}"
        ]

        # Choose appropriate templates based on syllable count
        templates = simple_templates if syllables < 6 else complex_templates
        template = random.choice(templates)
        needed_words = template.count("{}")

        # Select categories
        categories = ['nature', 'sensory', 'abstract']
        if mood and mood in self.word_cache:
            categories = [mood] + [c for c in categories if c != mood]

        # Collect words
        words = []
        remaining_syllables = syllables

        for _ in range(needed_words):
            if remaining_syllables <= 0:
                break

            # Try to find a word that fits
            attempts = 0
            word_found = False

            while attempts < 10 and not word_found:
                category = random.choice(categories)
                possible_words = []

                # Look for words with appropriate syllable count
                for syll in range(1, remaining_syllables + 1):
                    if syll in self.word_cache[category]:
                        possible_words.extend(self.word_cache[category][syll])

                if possible_words:
                    word = random.choice(possible_words)
                    word_syllables = self.analyzer.count_syllables(word)
                    if word_syllables <= remaining_syllables:
                        words.append(word)
                        remaining_syllables -= word_syllables
                        word_found = True

                attempts += 1

        # If we couldn't get enough words, fall back to simpler phrase
        if len(words) < needed_words:
            return self._create_simple_phrase(syllables, mood)

        try:
            return template.format(*words)
        except:
            return self._create_simple_phrase(syllables, mood)

    def _create_simple_phrase(self, syllables, mood=None):
        """Create a very simple phrase when more complex ones fail"""
        if mood and mood in self.word_cache:
            category = mood
        else:
            category = random.choice(['nature', 'sensory', 'abstract'])

        # Get a single word
        for syll in range(1, syllables + 1):
            if syll in self.word_cache[category]:
                words = self.word_cache[category][syll]
                if words:
                    return random.choice(words)

        # Ultimate fallback
        return "gentle"

    def generate_line(self, syllables, mood=None, end_word=None, line_type='standard'):
        """Generate a single line of poetry with specified constraints"""
        # Handle very small syllable counts
        if syllables < 3:
            if mood and mood in self.word_cache:
                for s in range(1, syllables + 1):
                    if s in self.word_cache[mood]:
                        return random.choice(self.word_cache[mood][s])
            return "oh"  # Ultimate fallback

        # Try metaphor
        if line_type == 'metaphor' and random.random() < 0.7:
            try:
                metaphor = self._create_metaphor(mood)
                if self.analyzer.count_syllables(metaphor) <= syllables:
                    return metaphor
            except:
                pass

        # Try image phrase
        if line_type == 'image' or random.random() < 0.3:
            try:
                image = self._create_image_phrase(syllables, mood)
                if self.analyzer.count_syllables(image) <= syllables:
                    return image
            except:
                pass

        # Standard line generation
        if mood and mood in self.word_cache:
            primary_category = mood
            secondary_categories = [c for c in self.word_cache.keys() if c != mood]
        else:
            categories = list(self.word_cache.keys())
            if categories:
                primary_category = random.choice(categories)
                secondary_categories = [c for c in categories if c != primary_category]
            else:
                return "gentle breeze"  # Ultimate fallback

        # Build line word by word
        words = []
        current_syllables = 0

        while current_syllables < syllables:
            remaining = syllables - current_syllables
            if remaining < 1:
                break

            # Try to find appropriate word
            category = random.choice([primary_category] + secondary_categories)
            possible_words = []

            for syll in range(1, remaining + 1):
                if syll in self.word_cache[category]:
                    possible_words.extend(self.word_cache[category][syll])

            if not possible_words:
                if not words:  # If we haven't added any words yet, use fallback
                    return "gentle wind"
                break

            word = random.choice(possible_words)
            words.append(word)
            current_syllables += self.analyzer.count_syllables(word)

        # Handle end word requirement
        if end_word and words:
            try:
                current_syllables = sum(self.analyzer.count_syllables(w) for w in words[:-1])
                if current_syllables + self.analyzer.count_syllables(end_word) <= syllables:
                    words[-1] = end_word
            except:
                pass

        return ' '.join(words)

    def generate_haiku(self, mood=None):
        """Generate a haiku"""
        structure = self.templates['haiku']['structure']
        focus = self.templates['haiku']['focus']

        lines = []
        for i, syllables in enumerate(structure):
            line_type = 'image' if i == 1 else 'standard'
            mood_for_line = mood or focus[i % len(focus)]
            lines.append(self.generate_line(syllables, mood_for_line, line_type=line_type))

        return '\n'.join(lines)

    def generate_free_verse(self, num_lines=None, mood=None):
        """Generate free verse poetry"""
        if not num_lines:
            num_lines = random.randint(
                self.templates['free_verse']['min_lines'],
                self.templates['free_verse']['max_lines']
            )

        lines = []
        prev_syllables = None

        for i in range(num_lines):
            # Vary line length but maintain some rhythm
            if prev_syllables:
                syllables = prev_syllables + random.randint(-2, 2)
                syllables = max(self.templates['free_verse']['min_syllables'],
                              min(self.templates['free_verse']['max_syllables'], syllables))
            else:
                syllables = random.randint(
                    self.templates['free_verse']['min_syllables'],
                    self.templates['free_verse']['max_syllables']
                )

            # Alternate between different line types
            line_type = 'metaphor' if i % 3 == 0 else 'image' if i % 3 == 1 else 'standard'

            lines.append(self.generate_line(syllables, mood, line_type=line_type))
            prev_syllables = syllables

        return '\n'.join(lines)

    def generate_sonnet(self, mood=None):
        """Generate a Shakespearean sonnet"""
        lines = []
        rhyme_scheme = self.templates['sonnet']['rhyme_scheme']
        syllables = self.templates['sonnet']['structure'][0]
        rhyme_words = defaultdict(list)

        for i, rhyme in enumerate(rhyme_scheme):
            if i % 4 == 0:  # Start of new quatrain
                line_type = 'metaphor'
            elif i % 4 == 2:  # Middle of quatrain
                line_type = 'image'
            else:
                line_type = 'standard'

            if rhyme in rhyme_words:
                # Use existing rhyme
                end_word = random.choice(rhyme_words[rhyme])
                lines.append(self.generate_line(syllables, mood, end_word, line_type))
            else:
                # Generate new line
                line = self.generate_line(syllables, mood, line_type=line_type)
                lines.append(line)

                # Find rhyming words for future
                last_word = line.split()[-1]
                rhymes = self.analyzer.get_rhyming_words(last_word)
                if rhymes:
                    rhyme_words[rhyme].extend(rhymes)

        return '\n'.join(lines)
