from setuptools import setup, find_packages

setup(
    name="poetry_system",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'spacy',
        'textblob',
        'pronouncing',
        'numpy'
    ],
    author="Claude AI & Human Collaborator",
    description="A system for analyzing and generating poetry",
    python_requires='>=3.7',
)
