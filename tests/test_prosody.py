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
