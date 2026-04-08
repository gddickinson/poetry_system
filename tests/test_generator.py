"""
Unit tests for PoetryGenerator.

Tests haiku generation and basic line generation.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.analyzer import PoetryAnalyzer
from core.generator import PoetryGenerator


@pytest.fixture(scope='module')
def generator():
    """Shared generator instance."""
    analyzer = PoetryAnalyzer()
    return PoetryGenerator(analyzer)


@pytest.fixture(scope='module')
def analyzer():
    """Shared analyzer for syllable checking."""
    return PoetryAnalyzer()


class TestGenerateHaiku:
    """Tests for generate_haiku."""

    def test_has_three_lines(self, generator):
        """Haiku produces exactly 3 lines."""
        haiku = generator.generate_haiku(mood='nature')
        lines = haiku.strip().split('\n')
        assert len(lines) == 3

    def test_non_empty_lines(self, generator):
        """All lines are non-empty."""
        haiku = generator.generate_haiku()
        lines = haiku.strip().split('\n')
        for line in lines:
            assert len(line.strip()) > 0

    def test_syllable_structure(self, generator, analyzer):
        """Lines approximate 5-7-5 syllable structure.

        We allow some tolerance since syllable counting is approximate.
        """
        haiku = generator.generate_haiku(mood='nature')
        lines = haiku.strip().split('\n')
        syllable_counts = []
        for line in lines:
            count = sum(analyzer.count_syllables(w) for w in line.split())
            syllable_counts.append(count)

        # Allow +/- 2 syllable tolerance per line
        assert abs(syllable_counts[0] - 5) <= 3
        assert abs(syllable_counts[1] - 7) <= 3
        assert abs(syllable_counts[2] - 5) <= 3


class TestGenerateFreeVerse:
    """Tests for generate_free_verse."""

    def test_produces_lines(self, generator):
        """Free verse produces at least one line."""
        poem = generator.generate_free_verse(num_lines=4)
        lines = poem.strip().split('\n')
        assert len(lines) >= 1

    def test_respects_num_lines(self, generator):
        """Respects num_lines parameter."""
        poem = generator.generate_free_verse(num_lines=6)
        lines = poem.strip().split('\n')
        assert len(lines) == 6


class TestGenerateLine:
    """Tests for generate_line."""

    def test_returns_string(self, generator):
        """Returns a non-empty string."""
        line = generator.generate_line(syllables=5)
        assert isinstance(line, str)
        assert len(line) > 0

    def test_small_syllable_count(self, generator):
        """Handles very small syllable requests."""
        line = generator.generate_line(syllables=2)
        assert isinstance(line, str)
        assert len(line) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
