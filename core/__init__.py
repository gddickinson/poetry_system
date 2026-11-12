"""Core functionality for poetry analysis and generation.

Contents:
    prosody.py    syllables, rhyme scheme, metre (pronouncing only; ProsodyAnalyzer)
    analyzer.py   PoetryAnalyzer: prosody + imagery and sentiment (spaCy, TextBlob)
    generator.py  PoetryGenerator: haiku, tanka, sonnet, free verse

The classes are imported on first use, so `import core.prosody` needs neither spaCy nor the analyzer.
"""

__all__ = ['PoetryAnalyzer', 'PoetryGenerator']


def __getattr__(name):
    if name == 'PoetryAnalyzer':
        from .analyzer import PoetryAnalyzer
        return PoetryAnalyzer
    if name == 'PoetryGenerator':
        from .generator import PoetryGenerator
        return PoetryGenerator
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
