"""Sensory vocabulary for poetry generation"""

SENSORY_DETAILS = {
    'colors': [
        'gold', 'silver', 'crimson', 'azure', 'emerald',
        'obsidian', 'violet', 'amber', 'ivory', 'ebony',
        'scarlet', 'indigo', 'sapphire', 'ruby', 'pearl',
        'opal', 'jade', 'turquoise', 'bronze', 'copper'
    ],
    
    'light': [
        'shine', 'glow', 'gleam', 'sparkle', 'flash',
        'glitter', 'shimmer', 'radiate', 'illuminate', 'beam',
        'glare', 'glimmer', 'flicker', 'blaze', 'bright',
        'brilliant', 'luminous', 'iridescent', 'phosphorescent', 'incandescent'
    ],
    
    'sound': [
        'whisper', 'echo', 'murmur', 'song', 'rhythm',
        'melody', 'silence', 'harmony', 'resonance', 'vibration',
        'chime', 'ring', 'hum', 'buzz', 'roar',
        'thunder', 'rustle', 'chirp', 'howl', 'sigh'
    ],
    
    'texture': [
        'soft', 'rough', 'smooth', 'sharp', 'gentle',
        'cold', 'warm', 'fluid', 'crystalline', 'velvet',
        'silken', 'metallic', 'wooden', 'stone', 'liquid',
        'icy', 'burning', 'frozen', 'melting', 'flowing'
    ],
    
    'movement': [
        'flow', 'drift', 'dance', 'swirl', 'spin',
        'float', 'glide', 'soar', 'dive', 'leap',
        'flutter', 'hover', 'ripple', 'wave', 'pulse',
        'vibrate', 'tremble', 'shake', 'quiver', 'oscillate'
    ],
    
    'taste_smell': [
        'sweet', 'bitter', 'salt', 'fragrant', 'pungent',
        'fresh', 'stale', 'aromatic', 'musty', 'perfumed',
        'spicy', 'rich', 'delicate', 'subtle', 'intense',
        'ethereal', 'earthy', 'floral', 'wild', 'pure'
    ]
}

def get_all_sensory_words():
    """Return a flat list of all sensory words"""
    return [word for category in SENSORY_DETAILS.values() for word in category]

def get_sensory_words(category):
    """Return all words for a specific sensory category"""
    return SENSORY_DETAILS.get(category, [])