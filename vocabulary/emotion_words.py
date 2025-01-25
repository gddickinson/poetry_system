"""Emotional vocabulary for poetry generation"""

EMOTIONS = {
    'joy': [
        'delight', 'bliss', 'rapture', 'ecstasy', 'elation',
        'jubilation', 'mirth', 'gladness', 'euphoria', 'radiance',
        'happiness', 'pleasure', 'cheer', 'joy', 'delight',
        'triumph', 'celebration', 'laughter', 'smile', 'warmth'
    ],
    
    'sorrow': [
        'melancholy', 'grief', 'sadness', 'despair', 'anguish',
        'longing', 'yearning', 'regret', 'lament', 'sigh',
        'tears', 'sorrow', 'pain', 'heartache', 'suffering',
        'mourning', 'weeping', 'darkness', 'shadow', 'void'
    ],
    
    'wonder': [
        'awe', 'marvel', 'enchantment', 'fascination', 'revelation',
        'mystery', 'magic', 'miracle', 'dream', 'vision',
        'wonder', 'amazement', 'astonishment', 'curiosity', 'discovery',
        'imagination', 'fantasy', 'spectacle', 'magnificence', 'splendor'
    ],
    
    'peace': [
        'serenity', 'tranquility', 'calm', 'stillness', 'harmony',
        'silence', 'peace', 'repose', 'quietude', 'rest',
        'contentment', 'ease', 'comfort', 'solace', 'sanctuary',
        'haven', 'refuge', 'shelter', 'embrace', 'grace'
    ],
    
    'passion': [
        'desire', 'ardor', 'fervor', 'intensity', 'flame',
        'fire', 'heat', 'spark', 'burning', 'glow',
        'passion', 'love', 'yearning', 'longing', 'hunger',
        'thirst', 'craving', 'need', 'want', 'wish'
    ],
    
    'fear': [
        'terror', 'dread', 'horror', 'fright', 'panic',
        'anxiety', 'worry', 'unease', 'apprehension', 'trembling',
        'shiver', 'chill', 'darkness', 'shadow', 'nightmare',
        'monster', 'ghost', 'specter', 'phantom', 'demon'
    ],
    
    'courage': [
        'valor', 'bravery', 'strength', 'might', 'power',
        'resolve', 'determination', 'will', 'spirit', 'force',
        'courage', 'boldness', 'daring', 'fearlessness', 'heroism',
        'gallantry', 'fortitude', 'resilience', 'endurance', 'persistence'
    ]
}

def get_all_emotion_words():
    """Return a flat list of all emotion words"""
    return [word for category in EMOTIONS.values() for word in category]

def get_emotion_words(emotion):
    """Return all words for a specific emotion"""
    return EMOTIONS.get(emotion, [])