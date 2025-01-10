# Computational Poetry System

A Python-based system for generating and analyzing poetry using natural language processing and computational creativity techniques. This system combines structured poetic forms with creative word combinations to generate unique poems while maintaining the ability to analyze existing poetry.

## Features

### Poetry Generation
- Multiple poetic forms:
  - Haiku (5-7-5 syllables)
  - Free Verse
  - Custom forms
- Diverse vocabulary categories:
  - Nature words
  - Emotional expressions
  - Abstract concepts
  - Sensory details
- Creative combinations through:
  - Metaphor generation
  - Image phrase creation
  - Thematic development
  - Mood-based word selection

### Poetry Analysis
- Rhyme scheme detection
- Imagery analysis
- Sentiment analysis
- Syllable counting
- Literary device identification

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Required Libraries
```bash
pip install spacy textblob pronouncing numpy
python -m spacy download en_core_web_sm
```

### Setup
```bash
git clone https://github.com/yourusername/poetry-system.git
cd poetry-system
```

## Usage

### Basic Usage
```python
from core.analyzer import PoetryAnalyzer
from core.generator import PoetryGenerator

# Initialize the system
analyzer = PoetryAnalyzer()
generator = PoetryGenerator(analyzer)

# Generate a haiku
haiku = generator.generate_haiku(mood='nature')
print(haiku)

# Generate free verse
poem = generator.generate_free_verse(num_lines=4, mood='emotion')
print(poem)

# Analyze a poem
analysis = analyzer.analyze_imagery(poem)
print(analysis)
```

### Example Output

```
Generated Haiku:
lake self regret pool
courage subtle sigh jade calm
bloom fluid spicy

Generated Free Verse:
where happiness meets infinity
suffering of might rhythm
icy embrace crow faith grief marvel awe branch touch
will of delta

Analysis:
Imagery: {'sensory': ['soft', 'whisper'], 'abstract': ['whisper'], 'nature': ['autumn']}
Sentiment: {'polarity': 0.2, 'subjectivity': 0.425}
```

## Project Structure

```
poetry_system/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── analyzer.py
│   └── generator.py
├── vocabulary/
│   ├── __init__.py
│   ├── abstract_words.py
│   ├── emotion_words.py
│   ├── nature_words.py
│   └── sensory_words.py
└── main.py
```

## Vocabulary System

The system uses categorized vocabulary sets:
- Nature words: Environmental and natural phenomena
- Emotion words: Feelings and emotional states
- Abstract words: Philosophical and conceptual terms
- Sensory words: Descriptive and sensory details

## Technical Details

### Generation Process
1. Word selection based on syllable requirements
2. Thematic combination of different word categories
3. Metaphor and image phrase creation
4. Line construction with rhythm considerations
5. Poem assembly with form constraints

### Analysis Capabilities
1. Rhyme scheme detection using pronunciation patterns
2. Imagery categorization across multiple domains
3. Sentiment analysis using TextBlob
4. Syllable counting with fallback mechanisms
5. Literary device identification

## Contributing

Contributions are welcome! Here are some ways you can contribute:
- Add new poetic forms
- Expand vocabulary sets
- Improve generation algorithms
- Enhance analysis capabilities
- Fix bugs and improve documentation

Please feel free to submit issues and pull requests.

## Future Enhancements

Planned features:
- More poetic forms (sonnet, tanka, etc.)
- Enhanced metaphor generation
- Improved semantic coherence
- Interactive poem evolution
- Extended analysis capabilities
- User interface for poem generation

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Created with assistance from Anthropic's Claude AI
- Built on principles of computational creativity
- Inspired by both traditional poetry and modern NLP techniques

## Contact

Please file any issues through the GitHub issue tracker.

---

*Note: This project demonstrates the potential of computational systems to engage in creative expression while respecting traditional poetic forms.*