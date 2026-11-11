"""Gallery content taken from the repo itself: README example output, poems quoted in the code, seeded samples.

Nothing here is written by hand: texts are read from core/README.md, main.py and simple-version/poetry-system.py
(via `ast`, without importing them), and the generated samples come from the repo's generator with fixed seeds.
"""
import ast
import re
from pathlib import Path

from web.poems import MOODS, generate

ROOT = Path(__file__).resolve().parent.parent

SEEDED = ([("haiku", m, s) for m in MOODS for s in (1, 2)] + [("haiku", None, 7)]
          + [("free_verse", m, 3) for m in ("nature", "emotion")] + [("sonnet", None, 5), ("sonnet", "nature", 11)])


def _dedent_lines(text):
    return "\n".join(ln.strip() for ln in text.strip().split("\n"))


def readme_example():
    """The 'Example Output' block from core/README.md, split into its generated poems."""
    text = (ROOT / "core" / "README.md").read_text()
    block = re.search(r"### Example Output\s*```\n(.*?)```", text, re.S).group(1)
    out = []
    for title, body in re.findall(r"Generated ([^:\n]+):\n(.*?)(?:\n\n|$)", block, re.S):
        out.append({"title": f"README example: {title.lower()}", "text": body.strip(),
                    "source": "core/README.md, 'Example Output' (output of an earlier run, recorded in the README)"})
    return out


def _string_assignments(path, names):
    tree = ast.parse(path.read_text())
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) in names for t in node.targets):
            if isinstance(node.value, ast.Constant):
                found.append(node.value.value)
            elif isinstance(node.value, ast.List):
                found.extend(e.value for e in node.value.elts if isinstance(e, ast.Constant))
    return found


def quoted_poems():
    """Poems the repo's demo code analyses: main.py and the simple version's sample poems."""
    out = []
    for text in _string_assignments(ROOT / "main.py", {"poem_to_analyze"}):
        out.append({"title": "main.py demo poem", "text": _dedent_lines(text),
                    "source": "main.py (poem_to_analyze)"})
    for i, text in enumerate(_string_assignments(ROOT / "simple-version" / "poetry-system.py", {"sample_poems"})):
        out.append({"title": f"simple-version sample poem {i + 1}", "text": _dedent_lines(text),
                    "source": "simple-version/poetry-system.py (sample_poems; public-domain verse)"})
    return out


def seeded_samples():
    out = []
    for form, mood, seed in SEEDED:
        call = f"random.seed({seed}); generate_{form}({'mood=' + repr(mood) if mood else ''})"
        out.append({"form": form, "mood": mood, "seed": seed, "text": generate(form, mood, seed), "call": call})
    return out


def all_samples():
    return {"readme": readme_example(), "quoted": quoted_poems(), "seeded": seeded_samples()}
