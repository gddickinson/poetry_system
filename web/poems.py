"""Server-side poem generation and analysis for the web API, using the repo's own code.

generate() seeds Python's `random` and calls PoetryGenerator with the model-free ProsodyAnalyzer, which is exactly
what the browser engine (static/generator_engine.js) reproduces. analyze() returns per-line syllables, stress
patterns (analyze_meter) and rhyme letters (analyze_rhyme_scheme); imagery and sentiment need spaCy + TextBlob and
are added only when PoetryAnalyzer can load them.
"""
import random
import threading
from functools import lru_cache

from core.generator import PoetryGenerator
from core.prosody import (ProsodyAnalyzer, analyze_meter, analyze_rhyme_scheme, clean_word,
                          count_syllables)
import vocabulary

FORMS = {
    "haiku": "Haiku: three lines of 5, 7 and 5 syllables (generate_haiku)",
    "tanka": "Tanka: five lines of 5, 7, 5, 7 and 7 syllables (generate_tanka)",
    "sonnet": "Sonnet: 14 lines of up to 10 syllables, rhyme plan ABABCDCDEFEFGG (generate_sonnet)",
    "free_verse": "Free verse: 4 to 8 lines of 5 to 12 syllables (generate_free_verse)",
}
MOODS = ["nature", "emotion", "abstract", "sensory"]

_lock = threading.Lock()  # PoetryGenerator uses the global `random` state


@lru_cache(maxsize=1)
def _generator():
    return PoetryGenerator(ProsodyAnalyzer())


def generate(form, mood=None, seed=0, num_lines=None):
    """Poem text for `form` after random.seed(seed); mood None means the generator's default per form."""
    if form not in FORMS:
        raise ValueError(f"unknown form {form!r}; choose from {', '.join(FORMS)}")
    if mood is not None and mood not in MOODS:
        raise ValueError(f"unknown mood {mood!r}; choose from {', '.join(MOODS)}")
    gen = _generator()
    with _lock:
        random.seed(seed)
        if form == "haiku":
            return gen.generate_haiku(mood=mood)
        if form == "tanka":
            return gen.generate_tanka(mood=mood)
        if form == "sonnet":
            return gen.generate_sonnet(mood=mood)
        return gen.generate_free_verse(num_lines=num_lines, mood=mood)


def analyze_lines(poem):
    """Per-line words, syllables, stress pattern and rhyme letter (mirrors analyzeLines in prosody_engine.js)."""
    scheme, meter = analyze_rhyme_scheme(poem), analyze_meter(poem)
    lines = [ln.strip() for ln in (poem or "").split("\n") if ln.strip()]
    out = []
    for i, line in enumerate(lines):
        words = line.split()
        out.append({"text": line, "syllables": sum(count_syllables(w) for w in words), "stress": meter[i],
                    "rhyme": scheme[i] if i < len(scheme) else "", "end": clean_word(words[-1]) if words else ""})
    return out


@lru_cache(maxsize=1)
def _full_analyzer():
    """PoetryAnalyzer (spaCy) or the reason it is unavailable."""
    try:
        from core.analyzer import PoetryAnalyzer
        return PoetryAnalyzer(), None
    except (ImportError, OSError) as e:
        return None, str(e)


def analyze(poem):
    """Analysis dict: lines, scheme, and imagery/sentiment when spaCy and TextBlob are installed."""
    result = {"lines": analyze_lines(poem), "scheme": analyze_rhyme_scheme(poem)}
    full, why = _full_analyzer()
    if full is None:
        result["nlp"] = {"available": False, "reason": why}
    else:
        try:
            result["nlp"] = {"available": True, "imagery": full.analyze_imagery(poem),
                             "sentiment": full.analyze_sentiment(poem)}
        except ImportError as e:  # TextBlob missing
            result["nlp"] = {"available": False, "reason": str(e)}
    return result


def vocabulary_info():
    """Word lists exactly as the generator reads them (vocabulary.get_all_words(); repeats kept)."""
    return vocabulary.get_all_words()
