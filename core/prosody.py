"""Pure prosody helpers (CMU dictionary via `pronouncing`): syllables, rhyme scheme and metre (stress patterns).

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
        # Look the word up as written, then without surrounding punctuation ("fire," -> "fire")
        phones = pronouncing.phones_for_word(word) or pronouncing.phones_for_word(clean_word(word))
        if phones:
            return len(pronouncing.stresses(phones[0]))

        # Fallback syllable counting
        count = 0
        vowels = 'aeiouy'
        word = clean_word(word)
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


def rhyme_keys_for(word):
    """Keys under which a line ending rhymes: the CMU rhyming part of every pronunciation of the word
    (so 'fog', listed as F AA1 G and F AO1 G, rhymes with 'dog' and 'bog'), else the word itself."""
    word = clean_word(word)
    phones = pronouncing.phones_for_word(word)
    if phones:
        return {('sound', pronouncing.rhyming_part(p)) for p in phones}
    return {('word', word)}


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
    seen = []  # (keys, letter) of earlier lines, in order
    current_rhyme = 0

    for line in lines:
        words = line.split()
        if not words:
            continue

        keys = rhyme_keys_for(words[-1])
        # Same letter as the first earlier line sharing any pronunciation's rhyming part
        letter = next((lt for ks, lt in seen if ks & keys), None)
        if letter is None:
            letter = chr(65 + current_rhyme)
            current_rhyme += 1
        seen.append((keys, letter))
        rhyme_scheme.append(letter)

    return ''.join(rhyme_scheme)


def analyze_meter(poem):
    """Stress pattern of each line from the CMU dictionary (restored from simple-version/poetry-system.py).

    Each word contributes its CMU stress digits (0 unstressed, 1 primary, 2 secondary stress); a word that
    is not in the dictionary gets an alternating 1, 0, ... pattern over its estimated syllables.

    Returns:
        list[list[int]]: one stress list per non-empty line; [] for empty input.
    """
    if not poem or not isinstance(poem, str) or not poem.strip():
        return []
    patterns = []
    for line in (ln.strip() for ln in poem.split('\n')):
        if not line:
            continue
        pattern = []
        for word in (clean_word(w) for w in line.split()):
            if not any(c.isalpha() for c in word):
                continue
            phones = pronouncing.phones_for_word(word)
            if phones:
                pattern.extend(int(c) for c in pronouncing.stresses(phones[0]))
            else:
                syllables = count_syllables(word)
                pattern.extend([1, 0] * (syllables // 2) + ([1] if syllables % 2 else []))
        patterns.append(pattern)
    return patterns


class ProsodyAnalyzer:
    """Syllable and rhyme analysis without NLP models; enough for PoetryGenerator."""

    def count_syllables(self, word):
        return count_syllables(word)

    def analyze_rhyme_scheme(self, poem):
        return analyze_rhyme_scheme(poem)

    def analyze_meter(self, poem):
        return analyze_meter(poem)

    def get_rhyming_words(self, word):
        """Words in the CMU dictionary that rhyme with `word` (used by generate_sonnet)."""
        return pronouncing.rhymes(clean_word(word))
