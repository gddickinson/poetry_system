"""Natural world vocabulary for poetry generation"""

NATURE_ELEMENTS = {
    'celestial': [
        'sun', 'moon', 'stars', 'comet', 'aurora', 'galaxy', 
        'nebula', 'planet', 'meteor', 'constellation',
        'zodiac', 'eclipse', 'nova', 'cosmos', 'astral'
    ],
    
    'weather': [
        'rain', 'snow', 'mist', 'fog', 'storm', 'thunder', 
        'lightning', 'rainbow', 'cloud', 'frost', 'hail', 
        'breeze', 'gale', 'hurricane', 'tempest', 'wind',
        'cyclone', 'blizzard', 'drought', 'monsoon'
    ],
    
    'landscape': [
        'mountain', 'valley', 'cliff', 'cave', 'beach', 'desert', 
        'forest', 'meadow', 'plain', 'canyon', 'glacier', 'volcano', 
        'island', 'peninsula', 'prairie', 'tundra', 'marsh', 'swamp',
        'plateau', 'hill', 'dune', 'oasis', 'gorge', 'ravine'
    ],
    
    'water': [
        'ocean', 'river', 'stream', 'lake', 'waterfall', 'wave', 
        'tide', 'ripple', 'cascade', 'pool', 'spring', 'sea', 
        'brook', 'rapid', 'current', 'whirlpool', 'lagoon', 
        'reservoir', 'delta', 'bay', 'inlet', 'fjord'
    ],
    
    'plants': [
        'tree', 'flower', 'grass', 'leaf', 'vine', 'root', 
        'branch', 'blossom', 'petal', 'seed', 'moss', 'fern', 
        'bloom', 'forest', 'garden', 'grove', 'thicket', 'bush',
        'shrub', 'willow', 'oak', 'pine', 'rose', 'lily'
    ],
    
    'seasons': [
        'spring', 'summer', 'autumn', 'winter', 'solstice', 
        'equinox', 'dawn', 'dusk', 'twilight', 'midnight', 
        'noon', 'morning', 'evening', 'night', 'day', 'season',
        'cycle', 'phase', 'period', 'era'
    ],
    
    'creatures': [
        'bird', 'butterfly', 'deer', 'wolf', 'eagle', 'swan',
        'dolphin', 'whale', 'fish', 'dragon', 'phoenix', 'unicorn',
        'serpent', 'lion', 'tiger', 'bear', 'owl', 'hawk', 'dove',
        'nightingale', 'raven', 'crow', 'fox', 'rabbit'
    ]
}

def get_all_nature_words():
    """Return a flat list of all nature words"""
    return [word for category in NATURE_ELEMENTS.values() for word in category]

def get_category_words(category):
    """Return all words for a specific category"""
    return NATURE_ELEMENTS.get(category, [])