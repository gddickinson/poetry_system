"""Compact export of the CMU pronouncing dictionary (as loaded by `pronouncing`) for the browser engine.

Only what the prosody code uses is kept, in dictionary order: for each entry the word, its stress digits and the index
of its rhyming part. That is enough to reproduce `phones_for_word` (stress patterns, syllable counts),
`rhyming_part` and `rhymes()` exactly in JavaScript (static/prosody_engine.js).
"""
from functools import lru_cache

import pronouncing


@lru_cache(maxsize=1)
def cmu_compact():
    """Return {'rp': [rhyming parts], 'entries': 'word stresses rpIndex' entries joined by '|', 'count': n}."""
    pronouncing.init_cmu()
    rp_index = {}
    rows = []
    for word, phones in pronouncing.pronunciations:
        rp = pronouncing.rhyming_part(phones)
        idx = rp_index.setdefault(rp, len(rp_index))
        rows.append(f"{word} {pronouncing.stresses(phones)} {idx:x}")
    return {"rp": list(rp_index), "entries": "|".join(rows), "count": len(rows)}
