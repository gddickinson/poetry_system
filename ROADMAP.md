# Poetry System -- Roadmap

## Current State
An NLP-based poetry analysis and generation system using spaCy, TextBlob, and the pronouncing library. Generates haiku, tanka, sonnets, and free verse with mood-based vocabulary selection. Structure: `core/analyzer.py` (meter, rhyme, sentiment analysis), `core/generator.py` (poem generation), four vocabulary modules (`nature_words.py`, `emotion_words.py`, `abstract_words.py`, `sensory_words.py`), `main.py` for demo, and a `simple-version/` standalone. Has a stale `core/analyzer_old.py` that should be removed. Uses `sys.path` manipulation in `generator.py` instead of proper package imports.

## Short-term Improvements
- [x] Remove `core/analyzer_old.py` -- stale file from earlier iteration
- [x] Fix `sys.path.append` hack in `core/generator.py` (line 10) -- use guarded sys.path.insert
- [x] Add unit tests for `analyzer.count_syllables()`, `analyze_meter()`, and `detect_rhyme_scheme()`
- [x] Add unit tests for `generator.generate_haiku()` verifying 5-7-5 syllable structure
- [x] Add input validation in `analyzer.py` for empty strings and non-English text
- [x] Add `requirements.txt` with pinned spacy, textblob, pronouncing versions
- [x] Create `INTERFACE.md` for project navigation

## Feature Enhancements
- [ ] Add limerick generation (AABBA rhyme scheme, anapestic meter)
- [ ] Add villanelle and sestina forms for advanced poetry generation
- [ ] Implement rhyme-aware line generation in `generator.py` (currently mood-based only, weak rhyming)
- [ ] Add poem-to-poem style transfer using spaCy embeddings
- [ ] Implement a CLI with argparse: `poetry_system generate --form haiku --mood nature`
- [ ] Add alliteration and assonance scoring in `analyzer.py`
- [ ] Expand vocabulary modules with part-of-speech tags for grammatically correct line construction

## Long-term Vision
- [ ] Integrate a language model (GPT-2/LLaMA) for more natural poem generation
- [ ] Build a web interface with Flask for interactive poem creation
- [ ] Add multi-language support (at least Spanish, French, Japanese for haiku)
- [ ] Implement a poetry corpus analysis tool for studying poetic patterns
- [ ] Add text-to-speech output for poem recitation
- [ ] Publish as a pip package for use as a library

## Technical Debt
- [ ] `simple-version/poetry-system.py` duplicates logic from `core/` -- consider removing or clearly marking as standalone demo
- [ ] Vocabulary modules have no tests and may contain words with incorrect syllable assumptions
- [ ] `main.py` mixes demo code with execution -- separate demo examples from entry point
- [x] No `pyproject.toml` or modern packaging configuration
- [x] Missing error handling when spaCy model `en_core_web_sm` is not installed
- [ ] `setup.py` exists but likely outdated -- verify it installs correctly
- [x] Fix bare except clauses in `analyzer.py` and `generator.py`
