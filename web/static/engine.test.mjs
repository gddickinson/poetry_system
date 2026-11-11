// Node test: the JS ports (pyrandom.js, prosody_engine.js, generator_engine.js) reproduce the Python exactly on
// tests/fixtures/poem_fixture.json (written by scripts/make_poem_fixture.py). The CMU data comes from the same Python
// export the site uses (`python scripts/make_poem_fixture.py --cmu-stdout`; set PYTHON to choose the interpreter).
// Run: node web/static/engine.test.mjs
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { PyRandom } from './pyrandom.js';
import { loadCmu, countSyllables, analyzeRhymeScheme, analyzeMeter, analyzeLines, getRhymingWords } from './prosody_engine.js';
import { PoetryGenerator } from './generator_engine.js';

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, '..', '..');
const fx = JSON.parse(readFileSync(join(root, 'tests', 'fixtures', 'poem_fixture.json'), 'utf8'));
const cmu = JSON.parse(execFileSync(process.env.PYTHON || 'python3', ['-W', 'ignore', join(root, 'scripts', 'make_poem_fixture.py'), '--cmu-stdout'],
  { cwd: root, maxBuffer: 64 << 20, encoding: 'utf8' }));
loadCmu(cmu);

let n = 0;
const check = (got, want, msg) => { assert.deepEqual(got, want, msg); n++; };

// CPython random
for (const c of fx.rng) {
  const r = new PyRandom(c.seed);
  for (const v of c.random) { const g = r.random(); assert.ok(Math.abs(g - v) <= 1e-12 * Math.max(1, Math.abs(v)), `random seed ${c.seed}`); n++; }
  check(c.randint.map(() => r.randint(-2, 2)), c.randint, `randint seed ${c.seed}`);
  check(c.choice.map(() => r.choice([...'abcdefg'])), c.choice, `choice seed ${c.seed}`);
  check(c.sample.map(() => r.sample(['nature', 'emotion', 'abstract', 'sensory'], 2)), c.sample, `sample seed ${c.seed}`);
  check(c.big.map(() => r.randint(1, 1000)), c.big, `randint big seed ${c.seed}`);
}

// prosody
for (const [w, s] of Object.entries(fx.syllables)) check(countSyllables(w), s, `syllables ${JSON.stringify(w)}`);
for (const a of fx.analysis) {
  check(analyzeRhymeScheme(a.poem), a.scheme, `scheme ${JSON.stringify(a.poem)}`);
  check(analyzeMeter(a.poem), a.meter, `meter ${JSON.stringify(a.poem)}`);
  check(analyzeLines(a.poem), a.lines, `lines ${JSON.stringify(a.poem)}`);
}
check(getRhymingWords('Day,').includes('way'), true, 'rhymes day/way');

// seeded poems: same text as the Python generator
const gen = new PoetryGenerator(fx.vocabulary);
for (const p of fx.poems) {
  gen.seed(p.seed);
  check(gen.generate(p.form, { mood: p.mood, numLines: p.num_lines }), p.text, `${p.form} mood=${p.mood} seed=${p.seed}`);
}
console.log(`engine.test.mjs: ${n} checks ok (${fx.poems.length} poems, ${Object.keys(fx.syllables).length} words)`);
