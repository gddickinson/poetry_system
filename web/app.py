"""FastAPI web app for Poetry System: serves the front end in static/ and the JSON API under /api.

Run with `python run_web.py` (http://127.0.0.1:8139, local only). `scripts/build_static.py` exports every path in
STATIC_ENDPOINTS to JSON for the GitHub Pages site, so keep that list in step with the GET routes below. The POST
routes (/generate, /analyze) are answered in the browser on the static site by the JS engines (static_api.js), except
imagery and sentiment, which need spaCy and TextBlob on the local server.
"""
import sys
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi import FastAPI, HTTPException  # noqa: E402
from fastapi.responses import FileResponse  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402
from pydantic import BaseModel, Field  # noqa: E402

from web import poems, samples  # noqa: E402
from web.cmu_data import cmu_compact  # noqa: E402

STATIC = Path(__file__).resolve().parent / "static"

app = FastAPI(title="Poetry System")
app.mount("/static", StaticFiles(directory=STATIC), name="static")


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(STATIC / "index.html")


@app.get("/api/info")
def info():
    """Project summary and real counts for the home page."""
    import vocabulary
    words = poems.vocabulary_info()
    return {"title": "Poetry System", "forms": poems.FORMS, "moods": poems.MOODS,
            "vocabulary": {k: len(set(v)) for k, v in words.items()},
            "vocabulary_unique": vocabulary.get_vocabulary_size(), "cmu_entries": cmu_compact()["count"]}


@app.get("/api/vocabulary")
def vocabulary_lists():
    """Word lists per category, exactly as the generator reads them (repeats kept: they weight the choice)."""
    return poems.vocabulary_info()


@app.get("/api/cmu")
def cmu():
    """Compact CMU pronouncing dictionary for the browser engine (stress digits and rhyming parts only)."""
    return cmu_compact()


@app.get("/api/samples")
def gallery_samples():
    return samples.all_samples()


class GenerateIn(BaseModel):
    form: str = "haiku"
    mood: Optional[str] = None
    seed: int = Field(0, ge=0, le=2**31 - 1)
    num_lines: Optional[int] = Field(None, ge=1, le=40)


@app.post("/api/generate")
def generate(req: GenerateIn):
    try:
        text = poems.generate(req.form, req.mood or None, req.seed, req.num_lines)
    except ValueError as e:
        raise HTTPException(400, str(e))
    return {"text": text, "form": req.form, "mood": req.mood, "seed": req.seed, "lines": poems.analyze_lines(text)}


class AnalyzeIn(BaseModel):
    poem: str = Field(..., max_length=20000)


@app.post("/api/analyze")
def analyze(req: AnalyzeIn):
    return poems.analyze(req.poem)


# GET paths (without the /api prefix) written to the static site as api/<path>.json.
STATIC_ENDPOINTS = ["/info", "/vocabulary", "/cmu", "/samples"]
