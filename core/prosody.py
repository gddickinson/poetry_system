"""Pure prosody helpers (CMU dictionary via `pronouncing`): syllables and rhyme scheme.

No spaCy or TextBlob here, so the generator and the web interface can use these without the heavy NLP models.
`PoetryAnalyzer` (core/analyzer.py) inherits from `ProsodyAnalyzer` and adds imagery and sentiment analysis.
"""
import string

import pronouncing


def count_syllables(word):
    """Count syllables in a word using the CMU dictionary, with a vowel-group fallback.

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
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if word.endswith('e'):
            count -= 1
        return max(1, count)
    except (IndexError, KeyError, ValueError):
        return 1


def clean_word(word):
    """Lower-case a word and strip surrounding punctuation."""
    return word.lower().strip(string.punctuation)


def analyze_rhyme_scheme(poem):
    """Detect the rhyme scheme of a poem.

    Args:
        poem: Multi-line poem string.

    Returns:
        str: Rhyme scheme letters (e.g. 'ABAB'), empty string if poem is empty.
    """
    if not poem or not isinstance(poem, str) or not poem.strip():
        return ''

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


class ProsodyAnalyzer:
    """Syllable and rhyme analysis without NLP models; enough for PoetryGenerator."""

    def count_syllables(self, word):
        return count_syllables(word)

    def analyze_rhyme_scheme(self, poem):
        return analyze_rhyme_scheme(poem)
