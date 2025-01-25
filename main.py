"""Example usage of the Poetry System"""

import sys
import os

# Add the current directory to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from core.analyzer import PoetryAnalyzer
from core.generator import PoetryGenerator

def main():
    # Initialize the system
    analyzer = PoetryAnalyzer()
    generator = PoetryGenerator(analyzer)

    # Generate different types of poems
    print("Generated Haiku:")
    print(generator.generate_haiku(mood='nature'))
    print("\nGenerated Free Verse:")
    print(generator.generate_free_verse(num_lines=4, mood='emotion'))

    # Analyze a poem
    poem_to_analyze = """
    Soft winds whisper dreams
    Through autumn's golden branches
    Time flows like water
    """
    print("\nAnalyzing poem:")
    print("Rhyme scheme:", analyzer.analyze_rhyme_scheme(poem_to_analyze))
    print("Imagery:", analyzer.analyze_imagery(poem_to_analyze))
    print("Sentiment:", analyzer.analyze_sentiment(poem_to_analyze))

if __name__ == "__main__":
    main()
