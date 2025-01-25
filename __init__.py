"""Poetry Generation System initialization"""

from poetry_system.core.analyzer import PoetryAnalyzer
from poetry_system.core.generator import PoetryGenerator

__version__ = '1.0.0'
__author__ = 'Claude AI & Human Collaborator'

def create_poetry_system():
    """Create and return initialized analyzer and generator instances."""
    analyzer = PoetryAnalyzer()
    generator = PoetryGenerator(analyzer)
    return analyzer, generator

__all__ = ['PoetryAnalyzer', 'PoetryGenerator', 'create_poetry_system']
