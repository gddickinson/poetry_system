"""Tests for core/prosody.py and the generator using the model-free ProsodyAnalyzer (no spaCy needed).

Includes regression tests for bugs fixed in November 2026 (see SESSION_LOG.md).
"""
import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.prosody import ProsodyAnalyzer, analyze_rhyme_scheme, count_syllables  # noqa: E402
from core.generator import PoetryGenerator  # noqa: E402


@pytest.fixture()
def generator():
    return PoetryGenerator(ProsodyAnalyzer())


def test_punctuation_does_not_change_syllable_count():
    """'fire,' was counted by the vowel fallback (1) instead of the CMU dictionary (2)."""
    assert count_syllables('fire') == 2
    assert count_syllables('fire,') == 2
    assert count_syllables('Hour.') == count_syllables('hour') == 2
    assert count_syllables('...') == 1


def test_rhyme_scheme_matches_words_that_rhyme():
    """'bat' and 'at' rhyme but got different letters: the key was the first three rhymes of each word,
    and each word is missing from its own rhyme list."""
    assert analyze_rhyme_scheme("I saw a bat\nI looked at") == 'AA'
    assert analyze_rhyme_scheme("the cat\nthe hat\nthe day\nthe way") == 'AABB'
    assert analyze_rhyme_scheme("Soft winds whisper dreams\nThrough autumn's golden branches\nTime flows like water") == 'ABC'
    assert analyze_rhyme_scheme("one xqzzy\ntwo xqzzy\nthree plorf") == 'AAB'


def test_sonnet_generates_fourteen_lines(generator):
    """generate_sonnet called analyzer.get_rhyming_words, which did not exist (AttributeError)."""
    random.seed(3)
    lines = generator.generate_sonnet(mood='nature').split('\n')
    assert len(lines) == 14 and all(line.strip() for line in lines)


def test_get_rhyming_words():
    words = ProsodyAnalyzer().get_rhyming_words('Day,')
    assert 'way' in words and 'day' not in words
    assert ProsodyAnalyzer().get_rhyming_words('xqzzy') == []


def test_haiku_lines_never_exceed_their_syllables(generator):
    """Metaphor and image phrases were checked with count_syllables on the whole phrase (one 'word'), which
    missed the dictionary and used the vowel guess, so lines like 'raven hawk in the violet' (8) passed as 7."""
    for seed in range(200):
        random.seed(seed)
        lines = generator.generate_haiku().split('\n')
        for line, target in zip(lines, [5, 7, 5]):
            assert sum(count_syllables(w) for w in line.split()) <= target, (seed, line)
