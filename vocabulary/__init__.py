"""
Vocabulary module containing word collections for poetry generation.
"""

from . import nature_words
from . import emotion_words
from . import abstract_words
from . import sensory_words

__all__ = [
    'nature_words',
    'emotion_words',
    'abstract_words',
    'sensory_words'
]

# Expose main functions from each module
get_all_nature_words = nature_words.get_all_nature_words
get_all_emotion_words = emotion_words.get_all_emotion_words
get_all_abstract_words = abstract_words.get_all_abstract_words
get_all_sensory_words = sensory_words.get_all_sensory_words

# Convenience function to get all words
def get_all_words():
    """Return a dictionary containing all words from all categories."""
    return {
        'nature': get_all_nature_words(),
        'emotion': get_all_emotion_words(),
        'abstract': get_all_abstract_words(),
        'sensory': get_all_sensory_words()
    }

# Convenience function to get words by category
def get_words_by_category(category):
    """Get all words for a specific category."""
    categories = {
        'nature': get_all_nature_words,
        'emotion': get_all_emotion_words,
        'abstract': get_all_abstract_words,
        'sensory': get_all_sensory_words
    }
    return categories.get(category, lambda: [])()

# Function to get total vocabulary size
def get_vocabulary_size():
    """Return the total number of unique words in the vocabulary."""
    all_words = set()
    for getter in [get_all_nature_words, get_all_emotion_words, 
                  get_all_abstract_words, get_all_sensory_words]:
        all_words.update(getter())
    return len(all_words)