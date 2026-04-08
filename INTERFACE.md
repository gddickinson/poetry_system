# Poetry System -- Interface Map

## Project Overview
NLP-based poetry analysis and generation system. Generates haiku, tanka,
sonnets, and free verse with mood-based vocabulary selection. Uses spaCy,
TextBlob, and the pronouncing library.

## Core Modules: `core/`

- **`analyzer.py`** -- Poetry analysis
  - `PoetryAnalyzer` -- meter, rhyme scheme, imagery, and sentiment analysis
    - `count_syllables(word)` -- syllable counting with CMU dict + fallback
    - `analyze_rhyme_scheme(poem)` -- detect rhyme scheme (ABAB etc.)
    - `analyze_imagery(poem)` -- categorize imagery (nature, emotion, etc.)
    - `analyze_sentiment(poem)` -- polarity/subjectivity via TextBlob

- **`generator.py`** -- Poetry generation
  - `PoetryGenerator(analyzer)` -- generates poems in various forms
    - `generate_haiku(mood)` -- 5-7-5 syllable haiku
    - `generate_free_verse(num_lines, mood)` -- variable-length free verse
    - `generate_sonnet(mood)` -- Shakespearean sonnet (ABABCDCDEFEFGG)
    - `generate_line(syllables, mood, end_word, line_type)` -- single line

## Vocabulary Modules: `vocabulary/`

- **`nature_words.py`** -- nature-themed vocabulary
  - `get_all_nature_words()` -- returns flat list of nature words
- **`emotion_words.py`** -- emotion-themed vocabulary
  - `get_all_emotion_words()`
- **`abstract_words.py`** -- abstract/philosophical vocabulary
  - `get_all_abstract_words()`
- **`sensory_words.py`** -- sensory vocabulary (sight, sound, touch, etc.)
  - `get_all_sensory_words()`

## Entry Points
- **`main.py`** -- Demo script: generates sample poems and analyzes text

## Tests: `tests/`
- **`test_analyzer.py`** -- tests for syllable counting, rhyme scheme, etc.
- **`test_generator.py`** -- tests for haiku generation and syllable structure

## Standalone
- **`simple-version/poetry-system.py`** -- self-contained single-file version

## Archived: `_archive/`
- `analyzer_old.py` -- previous version of analyzer module
