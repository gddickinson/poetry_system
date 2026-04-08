# Poetry System

An NLP-based poetry analysis and generation system using spaCy, TextBlob, and the pronouncing library. Generates haiku, tanka, sonnets, and free verse with mood-based vocabulary selection.

## Features

- **Poetry generation** -- haiku, tanka, sonnet, free verse
- **Poetry analysis** -- meter, rhyme scheme, sentiment, imagery detection
- **Mood-based generation** -- nature, love, melancholy, joy themes
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
print(generator.generate_free_verse(mood='melancholy'))
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
│   ├── analyzer.py        # PoetryAnalyzer (meter, rhyme, sentiment)
│   └── generator.py       # PoetryGenerator (haiku, sonnet, free verse)
├── vocabulary/            # Mood-categorized word lists
└── simple-version/        # Simplified standalone version
```
