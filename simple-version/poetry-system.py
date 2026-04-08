import numpy as np
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import cmudict
import string
import random
import re
from collections import defaultdict, Counter
import spacy
import pronouncing
from textblob import TextBlob

class PoetryAnalyzer:
    def __init__(self):
        self.d = cmudict.dict()
        self.nlp = spacy.load('en_core_web_sm')
        self.pos_to_words = defaultdict(list)
        self.rhyme_dict = defaultdict(list)
        self.markov_chain = defaultdict(list)
        self.syllable_patterns = []
        self.mood_words = self._load_mood_words()
        
    def _load_mood_words(self):
        # Expanded dictionary of words associated with different moods
        return {
            'joy': [
                'smile', 'laugh', 'bright', 'sun', 'happy', 'light', 'dance',
                'glow', 'shine', 'golden', 'warmth', 'embrace', 'delight', 'sparkle',
                'radiant', 'gleam', 'flutter', 'sing', 'bloom', 'cherish'
            ],
            'melancholy': [
                'rain', 'grey', 'sigh', 'dark', 'shadow', 'tear', 'silence',
                'mist', 'twilight', 'fade', 'whisper', 'autumn', 'lone', 'drift',
                'empty', 'distant', 'echo', 'somber', 'still', 'soft'
            ],
            'wonder': [
                'star', 'dream', 'magic', 'mystery', 'infinite', 'wonder', 'sparkle',
                'galaxy', 'cosmic', 'ethereal', 'celestial', 'enchant', 'mythic', 'timeless',
                'eternal', 'mystic', 'sacred', 'divine', 'astral', 'sublime'
            ],
            'nature': [
                'tree', 'flower', 'river', 'mountain', 'wind', 'sky', 'earth',
                'ocean', 'forest', 'meadow', 'sunrise', 'storm', 'leaf', 'cloud',
                'rain', 'valley', 'stream', 'garden', 'moon', 'sunlight'
            ],
            'abstract': [
                'time', 'love', 'soul', 'mind', 'dream', 'thought', 'memory',
                'spirit', 'hope', 'fate', 'destiny', 'truth', 'freedom', 'peace',
                'eternity', 'wisdom', 'harmony', 'serenity', 'infinity', 'grace'
            ]
        }
    
    def count_syllables(self, word):
        word = word.lower()
        try:
            return max([len(list(y for y in x if y[-1].isdigit())) for x in self.d[word]])
        except:
            # Fallback syllable counting
            count = 0
            vowels = 'aeiouy'
            word = word.lower()
            if word[0] in vowels:
                count += 1
            for index in range(1, len(word)):
                if word[index] in vowels and word[index-1] not in vowels:
                    count += 1
            if word.endswith('e'):
                count -= 1
            if count == 0:
                count += 1
            return count
    
    def analyze_rhyme_scheme(self, poem):
        def simple_tokenize(text):
            # Remove punctuation and split into words
            cleaned = text.translate(str.maketrans('', '', string.punctuation))
            return cleaned.lower().split()

        lines = [line.strip() for line in poem.split('\n') if line.strip()]
        rhyme_scheme = []
        rhyme_mapping = {}
        current_rhyme = 0
        
        for line in lines:
            words = simple_tokenize(line)
            if not words:  # Skip empty lines
                continue
            last_word = words[-1].lower()
            
            # Get pronunciation for rhyming
            try:
                pronunciation = pronouncing.rhymes(last_word)
                rhyme_key = tuple(pronunciation[:3]) if pronunciation else last_word
            except:
                rhyme_key = last_word
            
            if rhyme_key not in rhyme_mapping:
                rhyme_mapping[rhyme_key] = chr(65 + current_rhyme)
                current_rhyme += 1
            
            rhyme_scheme.append(rhyme_mapping[rhyme_key])
        
        return ''.join(rhyme_scheme)
    
    def analyze_meter(self, poem):
        lines = [line.strip() for line in poem.split('\n') if line.strip()]
        meter_patterns = []
        
        for line in lines:
            words = word_tokenize(line)
            pattern = []
            
            for word in words:
                try:
                    stresses = [int(c) for c in pronouncing.stresses(pronouncing.phones_for_word(word)[0])]
                    pattern.extend(stresses)
                except:
                    # Fallback to alternating stress pattern
                    syllables = self.count_syllables(word)
                    pattern.extend([1, 0] * (syllables // 2) + ([1] if syllables % 2 else []))
            
            meter_patterns.append(pattern)
        
        return meter_patterns
    
    def analyze_imagery(self, poem):
        doc = self.nlp(poem)
        imagery = {
            'visual': [],
            'auditory': [],
            'tactile': [],
            'nature': [],
            'abstract': []
        }
        
        # Words associated with different types of imagery
        imagery_words = {
            'visual': ['bright', 'dark', 'red', 'blue', 'shine', 'shadow', 'gleam'],
            'auditory': ['whisper', 'roar', 'sing', 'cry', 'echo', 'silence', 'ring'],
            'tactile': ['soft', 'rough', 'smooth', 'cold', 'warm', 'touch', 'sharp'],
            'nature': ['tree', 'flower', 'wind', 'sky', 'sun', 'moon', 'star'],
            'abstract': ['love', 'hope', 'dream', 'soul', 'spirit', 'time', 'fate']
        }
        
        for token in doc:
            word = token.text.lower()
            for category, words in imagery_words.items():
                if word in words:
                    imagery[category].append(word)
        
        return imagery
    
    def analyze_sentiment(self, poem):
        blob = TextBlob(poem)
        return {
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity
        }
    
    def train(self, poems):
        """Train the generator on a collection of poems"""
        for poem in poems:
            # Simple tokenization by splitting on whitespace and punctuation
            def simple_tokenize(text):
                # Remove punctuation and split into words
                cleaned = text.translate(str.maketrans('', '', string.punctuation))
                return cleaned.lower().split()

            # Build Markov chain
            words = simple_tokenize(poem)
            for i in range(len(words) - 2):
                key = (words[i], words[i + 1])
                self.markov_chain[key].append(words[i + 2])
            
            # Build POS patterns
            doc = self.nlp(poem)
            for token in doc:
                self.pos_to_words[token.pos_].append(token.text)
            
            # Collect syllable patterns
            lines = [line.strip() for line in poem.split('\n') if line.strip()]
            for line in lines:
                pattern = [self.count_syllables(word) for word in simple_tokenize(line)]
                if pattern:
                    self.syllable_patterns.append(pattern)
            
            # Build rhyme dictionary
            for word in words:
                rhymes = pronouncing.rhymes(word)
                if rhymes:
                    self.rhyme_dict[word].extend(rhymes)

class PoetryGenerator:
    def __init__(self, analyzer):
        self.analyzer = analyzer
        
    def generate_line(self, syllable_target=None, end_word=None, mood=None):
        """Generate a single line of poetry with improved variety and flow"""
        if not syllable_target:
            if self.analyzer.syllable_patterns:
                syllable_target = sum(random.choice(self.analyzer.syllable_patterns))
            else:
                syllable_target = random.randint(5, 10)
        
        # Get mood words and their alternatives
        available_words = set()
        if mood and mood in self.analyzer.mood_words:
            primary_words = set(self.analyzer.mood_words[mood])
            # Add words from complementary moods
            if mood == 'joy':
                available_words.update(self.analyzer.mood_words['wonder'])
            elif mood == 'melancholy':
                available_words.update(self.analyzer.mood_words['nature'])
            elif mood == 'wonder':
                available_words.update(self.analyzer.mood_words['abstract'])
            available_words.update(primary_words)
        else:
            for words in self.analyzer.mood_words.values():
                available_words.update(words)
        
        # Start with a thematically appropriate word
        used_words = set()
        if available_words:
            start_word = random.choice(list(available_words))
            used_words.add(start_word)
        else:
            start_words = list(self.analyzer.markov_chain.keys())
            if start_words:
                start_word = random.choice(start_words)[0]
            else:
                return "Whispers echo through time"  # Poetic fallback
        
        line = [start_word]
        current_syllables = self.analyzer.count_syllables(start_word)
        
        # Build line with attention to flow and variety
        attempts = 0
        while current_syllables < syllable_target and attempts < 20:
            attempts += 1
            
            # Try Markov chain first
            next_word = None
            if len(line) >= 2 and (line[-2], line[-1]) in self.analyzer.markov_chain:
                candidates = self.analyzer.markov_chain[(line[-2], line[-1])]
                # Filter out recently used words
                candidates = [w for w in candidates if w not in used_words]
                if candidates:
                    next_word = random.choice(candidates)
            
            # If no suitable word found, try mood-appropriate words
            if not next_word and available_words:
                candidates = [w for w in available_words if w not in used_words]
                if candidates:
                    next_word = random.choice(candidates)
            
            # Last resort: use any appropriate POS
            if not next_word:
                pos = random.choice(['NOUN', 'VERB', 'ADJ'])
                if pos in self.analyzer.pos_to_words:
                    candidates = [w for w in self.analyzer.pos_to_words[pos] if w not in used_words]
                    if candidates:
                        next_word = random.choice(candidates)
            
            if next_word:
                next_syllables = self.analyzer.count_syllables(next_word)
                if current_syllables + next_syllables <= syllable_target:
                    line.append(next_word)
                    used_words.add(next_word)
                    current_syllables += next_syllables
            
            # If we're stuck, break and try to finish the line
            if attempts >= 20:
                break
        
        # If we need a specific end word for rhyming
        if end_word and line[-1] != end_word and len(line) > 1:
            line[-1] = end_word
        
        # Clean up the line
        return ' '.join(line)
    
    def generate_poem(self, form='free', num_lines=4, mood=None):
        """Generate a complete poem"""
        if form == 'haiku':
            return self.generate_haiku(mood)
        elif form == 'sonnet':
            return self.generate_sonnet(mood)
        elif form == 'limerick':
            return self.generate_limerick(mood)
        else:
            return self.generate_free_verse(num_lines, mood)
    
    def generate_haiku(self, mood=None):
        """Generate a haiku (5-7-5 syllables)"""
        line1 = self.generate_line(syllable_target=5, mood=mood)
        line2 = self.generate_line(syllable_target=7, mood=mood)
        line3 = self.generate_line(syllable_target=5, mood=mood)
        return f"{line1}\n{line2}\n{line3}"
    
    def generate_sonnet(self, mood=None):
        """Generate a Shakespearean sonnet (14 lines, ABABCDCDEFEFGG)"""
        lines = []
        rhyme_scheme = 'ABABCDCDEFEFGG'
        rhyme_words = defaultdict(list)
        
        for i in range(14):
            if rhyme_scheme[i] in rhyme_words:
                # Use existing rhyme
                end_word = random.choice(rhyme_words[rhyme_scheme[i]])
                lines.append(self.generate_line(syllable_target=10, end_word=end_word, mood=mood))
            else:
                # Generate new line and find rhyming words for future
                line = self.generate_line(syllable_target=10, mood=mood)
                lines.append(line)
                last_word = line.split()[-1]
                rhymes = self.analyzer.rhyme_dict.get(last_word, [])
                if rhymes:
                    rhyme_words[rhyme_scheme[i]].extend(rhymes)
                
        return '\n'.join(lines)
    
    def generate_limerick(self, mood=None):
        """Generate a limerick (AABBA rhyme scheme)"""
        lines = []
        # First line establishes rhyme A
        line1 = self.generate_line(syllable_target=9, mood=mood)
        lines.append(line1)
        last_word = line1.split()[-1]
        rhymes_a = self.analyzer.rhyme_dict.get(last_word, [])
        
        # Second line rhymes with first
        if rhymes_a:
            end_word = random.choice(rhymes_a)
            lines.append(self.generate_line(syllable_target=9, end_word=end_word, mood=mood))
        else:
            lines.append(self.generate_line(syllable_target=9, mood=mood))
        
        # Third and fourth lines establish and complete rhyme B
        line3 = self.generate_line(syllable_target=6, mood=mood)
        lines.append(line3)
        last_word = line3.split()[-1]
        rhymes_b = self.analyzer.rhyme_dict.get(last_word, [])
        
        if rhymes_b:
            end_word = random.choice(rhymes_b)
            lines.append(self.generate_line(syllable_target=6, end_word=end_word, mood=mood))
        else:
            lines.append(self.generate_line(syllable_target=6, mood=mood))
        
        # Last line rhymes with first two
        if rhymes_a:
            end_word = random.choice(rhymes_a)
            lines.append(self.generate_line(syllable_target=9, end_word=end_word, mood=mood))
        else:
            lines.append(self.generate_line(syllable_target=9, mood=mood))
        
        return '\n'.join(lines)
    
    def generate_free_verse(self, num_lines=4, mood=None):
        """Generate free verse poetry"""
        lines = []
        for _ in range(num_lines):
            syllables = random.randint(5, 10)
            lines.append(self.generate_line(syllable_target=syllables, mood=mood))
        return '\n'.join(lines)

if __name__ == "__main__":
    # Example usage
    sample_poems = [
        """Shall I compare thee to a summer's day?
        Thou art more lovely and more temperate.
        Rough winds do shake the darling buds of May,
        And summer's lease hath all too short a date.""",
        
        """Because I could not stop for Death,
        He kindly stopped for me;
        The carriage held but just ourselves
        And Immortality."""
    ]
    
    # Initialize and train the system
    analyzer = PoetryAnalyzer()
    generator = PoetryGenerator(analyzer)
    
    # Train on sample poems
    analyzer.train(sample_poems)
    
    # Generate different types of poems
    print("Generated Haiku:")
    print(generator.generate_poem(form='haiku', mood='nature'))
    print("\nGenerated Free Verse:")
    print(generator.generate_poem(form='free', num_lines=4, mood='melancholy'))
    
    # Analyze a poem
    poem_to_analyze = """
    Soft winds whisper dreams
    Through autumn's golden branches
    Time flows like water
    """
    print("\nAnalyzing poem:")
    print("Rhyme scheme:", analyzer.analyze_rhyme_scheme(poem_to_analyze))
    print("Imagery:", analyzer.analyze_imagery(poem_to_analyze))
    print("Sentiment:", analyzer.analyze_sentiment(poem_to_analyze))