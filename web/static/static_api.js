// Static-site data layer: GETs come from the JSON files exported by scripts/build_static.py; POST /generate and
// /analyze run the JS ports of the Python generator and prosody code (same results for the same seed and text).
// Imagery and sentiment need spaCy and TextBlob, so they are reported as unavailable here.
import { loadCmu, cmuLoaded, analyzeLines, analyzeRhymeScheme } from './prosody_engine.js';
import { PoetryGenerator, FORMS, MOODS } from './generator_engine.js';

const files = new Map();
function file(rel) {
  if (!files.has(rel)) files.set(rel, fetch('api/' + rel + '.json').then(r => { if (!r.ok) throw new Error(`${r.status} ${rel}`); return r.json(); }));
  return files.get(rel);
}

let generator = null;
async function engines() {
  if (!cmuLoaded()) loadCmu(await file('cmu'));
  if (!generator) generator = new PoetryGenerator(await file('vocabulary'));
  return generator;
}

const NLP_NOTE = 'Imagery and sentiment use spaCy and TextBlob, which run only in the local app.';

export async function staticApi(path, body) {
  const clean = path.split('?')[0].replace(/^\/+/, '');
  if (clean === 'generate') {
    const gen = await engines();
    const form = body?.form || 'haiku', mood = body?.mood || null, seed = Number(body?.seed ?? 0);
    if (!FORMS.includes(form)) throw new Error('unknown form ' + form);
    if (mood && !MOODS.includes(mood)) throw new Error('unknown mood ' + mood);
    gen.seed(seed);
    const text = gen.generate(form, { mood, numLines: body?.num_lines || null });
    return { text, form, mood, seed, lines: analyzeLines(text) };
  }
  if (clean === 'analyze') {
    await engines();
    const poem = String(body?.poem ?? '');
    return { lines: analyzeLines(poem), scheme: analyzeRhymeScheme(poem), nlp: { available: false, reason: NLP_NOTE, static: true } };
  }
  return file(clean);
}
