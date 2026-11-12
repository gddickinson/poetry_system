"""Shared fixtures. Tests that need the full PoetryAnalyzer (spaCy + en_core_web_sm, TextBlob) skip cleanly when those
are not installed, so `pytest tests` runs without them (the web and prosody tests do not need them)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture(scope='session')
def full_analyzer():
    """A PoetryAnalyzer, or skip if spaCy, its English model or TextBlob is missing."""
    pytest.importorskip('spacy', reason='spaCy not installed (pip install spacy)')
    pytest.importorskip('textblob', reason='TextBlob not installed (pip install textblob)')
    from core.analyzer import PoetryAnalyzer
    try:
        return PoetryAnalyzer()
    except OSError as e:  # en_core_web_sm missing
        pytest.skip(str(e))
