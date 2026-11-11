"""Web interface for Poetry System (FastAPI + plain ES-module front end; static GitHub Pages export).

Contents:
    app.py       FastAPI app: /api/info, /vocabulary, /cmu, /samples (GET, exported) and /generate, /analyze (POST)
    poems.py     generate() and analyze() over core/ (seeded PoetryGenerator, prosody, optional spaCy/TextBlob)
    samples.py   gallery texts read from the repo (README example, quoted poems) and seeded generated samples
    cmu_data.py  compact CMU dictionary export used by the browser prosody engine
    static/      front end; prosody_engine.js, generator_engine.js and pyrandom.js are the JS ports
"""
