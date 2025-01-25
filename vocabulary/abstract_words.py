"""Abstract concepts vocabulary for poetry generation"""

ABSTRACT_CONCEPTS = {
    'time': [
        'eternity', 'moment', 'infinity', 'age', 'epoch',
        'era', 'instant', 'forever', 'temporal', 'timeless',
        'past', 'present', 'future', 'memory', 'history',
        'destiny', 'fate', 'cycle', 'rhythm', 'flow'
    ],
    
    'existence': [
        'being', 'essence', 'spirit', 'soul', 'life',
        'death', 'void', 'presence', 'absence', 'reality',
        'existence', 'consciousness', 'awareness', 'self', 'identity',
        'nature', 'substance', 'form', 'matter', 'energy'
    ],
    
    'thought': [
        'memory', 'dream', 'idea', 'wisdom', 'knowledge',
        'truth', 'consciousness', 'mind', 'thought', 'reflection',
        'contemplation', 'meditation', 'understanding', 'insight', 'reason',
        'logic', 'intuition', 'imagination', 'fantasy', 'vision'
    ],
    
    'human': [
        'heart', 'breath', 'pulse', 'blood', 'bone',
        'flesh', 'body', 'hand', 'eye', 'voice',
        'whisper', 'touch', 'smile', 'tear', 'laugh',
        'sigh', 'dance', 'song', 'dream', 'memory'
    ],
    
    'virtues': [
        'truth', 'beauty', 'justice', 'wisdom', 'courage',
        'honor', 'faith', 'hope', 'love', 'peace',
        'harmony', 'balance', 'grace', 'dignity', 'nobility',
        'kindness', 'mercy', 'compassion', 'empathy', 'understanding'
    ],
    
    'concepts': [
        'freedom', 'destiny', 'fate', 'chance', 'necessity',
        'possibility', 'potential', 'purpose', 'meaning', 'value',
        'unity', 'diversity', 'complexity', 'simplicity', 'infinity',
        'eternity', 'mortality', 'immortality', 'divinity', 'humanity'
    ]
}

def get_all_abstract_words():
    """Return a flat list of all abstract words"""
    return [word for category in ABSTRACT_CONCEPTS.values() for word in category]

def get_abstract_words(category):
    """Return all words for a specific category"""
    return ABSTRACT_CONCEPTS.get(category, [])