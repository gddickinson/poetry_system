# Poetry System

An NLP-based poetry analysis and generation system using spaCy, TextBlob, and the pronouncing library. Generates haiku, sonnets and free verse with mood-based vocabulary selection (a tanka template is defined in the generator but has no `generate_tanka` method yet).

## Features

- **Poetry generation** -- haiku, sonnet, free verse
- **Poetry analysis** -- meter (per-line CMU stress patterns), rhyme scheme, sentiment, imagery detection
- **Mood-based generation** -- nature, emotion, abstract, sensory (the four vocabulary categories)
- **Syllable counting** using the pronouncing library (CMU dictionary)
- **Vocabulary system** with mood-categorized word lists

## Requirements

- Python 3.7+
- spacy, textblob, pronouncing

```bash
pip install spacy textblob pronouncing
python -m spacy download en_core_web_sm
```

## Usage

```python
from core.analyzer import PoetryAnalyzer
from core.generator import PoetryGenerator

analyzer = PoetryAnalyzer()
generator = PoetryGenerator(analyzer)

# Generate poems
print(generator.generate_haiku(mood='nature'))
print(generator.generate_free_verse(mood='emotion'))
```

```bash
python main.py
```

## Project Structure

```
poetry_system/
├── __init__.py
├── main.py                # Example usage and demo
├── setup.py               # Package setup
├── core/
│   ├── prosody.py         # syllables, rhyme scheme, meter (no spaCy needed)
│   ├── analyzer.py        # PoetryAnalyzer (adds imagery and sentiment)
│   └── generator.py       # PoetryGenerator (haiku, sonnet, free verse)
├── vocabulary/            # Mood-categorized word lists
└── simple-version/        # Simplified standalone version
```


---
*Built with AI assistance from [Claude (Anthropic)](https://claude.com/).*
