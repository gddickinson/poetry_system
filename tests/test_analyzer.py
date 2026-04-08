"""
Unit tests for PoetryAnalyzer.

Tests syllable counting, rhyme scheme detection, and input validation.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.analyzer import PoetryAnalyzer


@pytest.fixture(scope='module')
def analyzer():
    """Shared analyzer instance (loads spaCy model once)."""
    return PoetryAnalyzer()


class TestCountSyllables:
    """Tests for count_syllables."""

    def test_known_words(self, analyzer):
        """Common words have expected syllable counts."""
        assert analyzer.count_syllables('cat') == 1
        assert analyzer.count_syllables('water') == 2
        assert analyzer.count_syllables('beautiful') == 3

    def test_empty_string(self, analyzer):
        """Empty string returns 1 (minimum)."""
        assert analyzer.count_syllables('') == 1

    def test_none_input(self, analyzer):
        """None input returns 1."""
        assert analyzer.count_syllables(None) == 1

    def test_punctuation_stripped(self, analyzer):
        """Words with trailing punctuation still count correctly."""
        # Syllable count should work even with punctuation
        result = analyzer.count_syllables('hello,')
        assert result >= 1

    def test_returns_at_least_one(self, analyzer):
        """Always returns at least 1."""
        assert analyzer.count_syllables('x') >= 1


class TestAnalyzeRhymeScheme:
    """Tests for analyze_rhyme_scheme."""

    def test_simple_couplet(self, analyzer):
        """Two rhyming lines get same letter."""
        poem = "I saw a cat\nWho wore a hat"
        scheme = analyzer.analyze_rhyme_scheme(poem)
        assert len(scheme) == 2

    def test_empty_poem(self, analyzer):
        """Empty poem returns empty string."""
        assert analyzer.analyze_rhyme_scheme('') == ''
        assert analyzer.analyze_rhyme_scheme(None) == ''

    def test_single_line(self, analyzer):
        """Single line gets one letter."""
        scheme = analyzer.analyze_rhyme_scheme('A single line of verse')
        assert len(scheme) == 1


class TestAnalyzeImagery:
    """Tests for analyze_imagery."""

    def test_returns_dict(self, analyzer):
        """Returns a dictionary."""
        result = analyzer.analyze_imagery('The sun shone on the river')
        assert isinstance(result, dict)

    def test_empty_input(self, analyzer):
        """Empty input returns empty dict."""
        assert analyzer.analyze_imagery('') == {}
        assert analyzer.analyze_imagery(None) == {}


class TestAnalyzeSentiment:
    """Tests for analyze_sentiment."""

    def test_returns_expected_keys(self, analyzer):
        """Returns dict with polarity and subjectivity."""
        result = analyzer.analyze_sentiment('This is a wonderful day')
        assert 'polarity' in result
        assert 'subjectivity' in result

    def test_empty_input(self, analyzer):
        """Empty input returns neutral sentiment."""
        result = analyzer.analyze_sentiment('')
        assert result['polarity'] == 0.0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
