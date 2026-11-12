# Poetry System -- Interface Map

## Project Overview
NLP-based poetry analysis and generation system. Generates haiku, tanka, sonnets and free verse with mood-based
vocabulary selection. Uses the pronouncing library (CMU dictionary) for
syllables, rhyme and metre, and spaCy + TextBlob for imagery and sentiment. A FastAPI web app and a static GitHub Pages
site (JS port of the generator and prosody code) live in `web/`.

## Core Modules: `core/`

- **`prosody.py`** -- model-free prosody (pronouncing only; no spaCy)
  - `count_syllables(word)` -- CMU dict (also without surrounding punctuation) + vowel-group fallback
  - `clean_word(word)`, `rhyme_keys_for(word)` -- CMU rhyming parts of all pronunciations, else the word
  - `analyze_rhyme_scheme(poem)` -- rhyme letters (ABAB etc.)
  - `analyze_meter(poem)` -- per-line CMU stress digits (restored from simple-version)
  - `ProsodyAnalyzer` -- the above as methods + `get_rhyming_words(word)`; enough for PoetryGenerator

- **`analyzer.py`** -- `PoetryAnalyzer(ProsodyAnalyzer)`: adds (spaCy/TextBlob imported lazily)
  - `analyze_imagery(poem)` -- vocabulary categories found in the poem (spaCy tokens)
  - `analyze_sentiment(poem)` -- polarity/subjectivity via TextBlob

- **`generator.py`** -- `PoetryGenerator(analyzer)` (any object with count_syllables/get_rhyming_words)
  - `generate_haiku(mood)` -- 5-7-5 syllable haiku
  - `generate_tanka(mood)` -- 5-7-5-7-7 tanka (built like generate_haiku)
  - `generate_free_verse(num_lines, mood)` -- variable-length free verse
  - `generate_sonnet(mood)` -- 14 lines, ABABCDCDEFEFGG end-word rhymes where they fit; rhymes from
    `_sonnet_rhymes(word, mood)`: mood list, then whole vocabulary, then the CMU dictionary
  - `generate_line(syllables, mood, end_word, line_type)` -- single line
  - moods: the vocabulary categories nature, emotion, abstract, sensory (others act as no mood)

## Vocabulary Modules: `vocabulary/`
- `__init__.py` -- `get_all_words()`, `get_words_by_category()`, `get_vocabulary_size()`
- **`nature_words.py`**, **`emotion_words.py`**, **`abstract_words.py`**, **`sensory_words.py`** --
  `get_all_<x>_words()` flat lists (repeats kept; they weight random choice)

## Web: `web/` (see `web/__init__.py`)
- **`app.py`** -- FastAPI: GET `/api/info`, `/api/vocabulary`, `/api/cmu`, `/api/samples` (exported to the static
  site via `STATIC_ENDPOINTS`); POST `/api/generate`, `/api/analyze`
- **`poems.py`** -- `generate(form, mood, seed, num_lines)`, `analyze_lines(poem)`, `analyze(poem)` (adds imagery and
  sentiment when spaCy is available), `FORMS`, `MOODS`
- **`samples.py`** -- gallery texts read from the repo (`readme_example`, `quoted_poems`) + `seeded_samples`
- **`cmu_data.py`** -- `cmu_compact()`: CMU dict as word/stress/rhyming-part rows for the browser
- **`static/`** -- front end (no build step): `index.html`, `core.js` + `style.css` (shared kit), `style_app.css`,
  `main.js` (router), `static_api.js` (static-site api()), `ui.js` (poem rendering), pages `home.js`, `compose.js`,
  `analyse.js`, `gallery.js`, `about.js`; JS ports `pyrandom.js` (CPython random), `prosody_engine.js`
  (core/prosody.py), `generator_engine.js` (core/generator.py); node test `engine.test.mjs`

## Entry Points
- **`main.py`** -- Demo script: generates sample poems and analyzes text
- **`run_web.py`** -- web app on http://127.0.0.1:8139

## Scripts: `scripts/`
- `build_static.py` -- export `site/` for GitHub Pages
- `screenshots.py` -- Playwright smoke test and README images (`docs/img/`)
- `make_poem_fixture.py` -- writes `tests/fixtures/poem_fixture.json` (Python results the JS must match)

## Tests: `tests/`
- **`test_analyzer.py`**, **`test_generator.py`** -- original tests (need spaCy + en_core_web_sm)
- **`test_prosody.py`** -- prosody and generator without spaCy, incl. regression tests for the Nov 2026 fixes
- **`test_web.py`** -- API, static build, fixture currency, node JS-engine test

## Standalone
- **`simple-version/poetry-system.py`** -- self-contained single-file version

## Archived: `_archive/`
- `analyzer_old.py` -- previous version of analyzer module
