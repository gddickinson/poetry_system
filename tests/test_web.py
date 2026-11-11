"""Web interface tests: every exported endpoint answers, the static build is complete, and the JS engine tests pass.

Run: python -m pytest -q tests/test_web.py
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from web.app import STATIC, STATIC_ENDPOINTS, app  # noqa: E402

client = TestClient(app)


def test_index_served():
    r = client.get("/")
    assert r.status_code == 200 and "static/main.js" in r.text


@pytest.mark.parametrize("path", STATIC_ENDPOINTS)
def test_endpoint(path):
    r = client.get("/api" + path)
    assert r.status_code == 200, r.text
    assert r.json() is not None


def test_static_build(tmp_path):
    sys.path.insert(0, str(ROOT / "scripts"))
    import build_static
    build_static.build(tmp_path / "site")
    assert (tmp_path / "site" / "index.html").read_text().count("APP_STATIC") == 1
    for path in STATIC_ENDPOINTS:
        assert (tmp_path / "site" / "api" / (path.strip("/") + ".json")).exists()


def test_static_assets_referenced_exist():
    html = (STATIC / "index.html").read_text()
    for name in ("style.css", "main.js"):
        assert f"static/{name}" in html and (STATIC / name).exists()


@pytest.mark.skipif(not shutil.which("node"), reason="node not installed")
def test_js_engine():
    tests = sorted(STATIC.glob("*.test.mjs"))
    for t in tests:
        env = {**os.environ, "PYTHON": sys.executable}  # the node test reads the CMU export via this Python
        r = subprocess.run(["node", str(t)], capture_output=True, text=True, env=env)
        assert r.returncode == 0, r.stdout + r.stderr


# --- Poetry System API --------------------------------------------------------------------------------------------
def test_generate_matches_python_generator():
    import random
    from core.generator import PoetryGenerator
    from core.prosody import ProsodyAnalyzer
    r = client.post("/api/generate", json={"form": "haiku", "mood": "nature", "seed": 4})
    assert r.status_code == 200
    random.seed(4)
    assert r.json()["text"] == PoetryGenerator(ProsodyAnalyzer()).generate_haiku(mood="nature")
    assert all(ln["syllables"] <= t for ln, t in zip(r.json()["lines"], [5, 7, 5]))
    sonnet = client.post("/api/generate", json={"form": "sonnet", "seed": 1}).json()
    assert len(sonnet["lines"]) == 14


@pytest.mark.parametrize("body", [{"form": "tanka"}, {"form": "haiku", "mood": "melancholy"}, {"seed": -1}])
def test_generate_rejects_bad_input(body):
    assert client.post("/api/generate", json=body).status_code in (400, 422)


def test_analyze():
    r = client.post("/api/analyze", json={"poem": "I saw a bat,\nI looked at\n\nthe fire."}).json()
    assert r["scheme"] == "AAB"
    assert [ln["syllables"] for ln in r["lines"]] == [4, 3, 3]
    assert r["lines"][2]["stress"] == [0, 1, 0]
    assert "available" in r["nlp"]


def test_samples_come_from_repo():
    s = client.get("/api/samples").json()
    assert s["readme"][0]["text"].startswith("lake self regret pool")
    assert any("Shall I compare thee" in p["text"] for p in s["quoted"])
    assert all(p["text"] for p in s["seeded"])


def test_fixture_is_current():
    """tests/fixtures/poem_fixture.json matches the Python code (regenerate: python scripts/make_poem_fixture.py)."""
    import json
    sys.path.insert(0, str(ROOT / "scripts"))
    import make_poem_fixture
    saved = json.loads(make_poem_fixture.FIXTURE.read_text())
    fresh = json.loads(json.dumps(make_poem_fixture.build()))
    for c_saved, c_fresh in zip(saved.pop("rng"), fresh.pop("rng")):
        assert c_saved["random"] == pytest.approx(c_fresh["random"], rel=1e-9)
        c_saved.pop("random"), c_fresh.pop("random")
        assert c_saved == c_fresh
    assert saved == fresh
