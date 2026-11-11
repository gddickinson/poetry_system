"""Write tests/fixtures/poem_fixture.json: Python results the JS engines must reproduce exactly.

Covers CPython `random` (seed, random, randint, choice, sample), syllable counts, rhyme schemes, stress patterns and
seeded poems from PoetryGenerator for every form and mood. tests/test_web.py checks the file is current and runs the
node test (web/static/engine.test.mjs) against it.

Run: python scripts/make_poem_fixture.py [--cmu-stdout]
"""
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.prosody import analyze_meter, analyze_rhyme_scheme, count_syllables  # noqa: E402
from web import poems, samples  # noqa: E402
from web.cmu_data import cmu_compact  # noqa: E402

FIXTURE = ROOT / "tests" / "fixtures" / "poem_fixture.json"
RNG_SEEDS = [0, 1, 42, 2**31 - 1, 2**40 + 5]
POEM_SEEDS = range(6)
EXTRA_WORDS = ["fire,", "Hour.", "...", "summer's", "xqzzyab", "  Moon  ", "", "rhythm", "CAT!", "--dawn--", "ée"]
EXTRA_POEMS = ["I saw a bat\nI looked at", "the cat\nthe hat\nthe day\nthe way", "one xqzzy\ntwo xqzzy\n\nthree",
               "  \n", "word -- \n  — dash line —", "Tyger Tyger, burning bright,\nIn the forests of the night;"]


def rng_cases():
    out = []
    cats = ["nature", "emotion", "abstract", "sensory"]
    for s in RNG_SEEDS:
        random.seed(s)
        vals = {"random": [random.random() for _ in range(3)], "randint": [random.randint(-2, 2) for _ in range(8)],
                "choice": [random.choice(list("abcdefg")) for _ in range(8)],
                "sample": [random.sample(cats, 2) for _ in range(4)], "big": [random.randint(1, 1000) for _ in range(4)]}
        out.append({"seed": s, **vals})
    return out


def poem_cases():
    out = []
    for form in poems.FORMS:
        for mood in [None] + poems.MOODS:
            for seed in POEM_SEEDS:
                out.append({"form": form, "mood": mood, "seed": seed, "num_lines": None,
                            "text": poems.generate(form, mood, seed)})
    for seed in POEM_SEEDS:
        out.append({"form": "free_verse", "mood": "emotion", "seed": seed, "num_lines": 6,
                    "text": poems.generate("free_verse", "emotion", seed, 6)})
    return out


def build():
    vocab = poems.vocabulary_info()
    words = sorted({w for ws in vocab.values() for w in ws}) + EXTRA_WORDS
    generated = poem_cases()
    texts = EXTRA_POEMS + [p["text"] for p in samples.quoted_poems() + samples.readme_example()] \
        + [p["text"] for p in generated[::5]]
    return {
        "vocabulary": vocab,
        "rng": rng_cases(),
        "syllables": {w: count_syllables(w) for w in words},
        "analysis": [{"poem": t, "scheme": analyze_rhyme_scheme(t), "meter": analyze_meter(t),
                      "lines": poems.analyze_lines(t)} for t in texts],
        "poems": generated,
    }


def main():
    if "--cmu-stdout" in sys.argv:
        sys.stdout.write(json.dumps(cmu_compact(), separators=(",", ":")))
        return
    FIXTURE.parent.mkdir(parents=True, exist_ok=True)
    data = build()
    FIXTURE.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"wrote {FIXTURE.relative_to(ROOT)}: {len(data['poems'])} poems, {len(data['syllables'])} words")


if __name__ == "__main__":
    main()
