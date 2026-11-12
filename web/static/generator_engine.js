// JavaScript port of core/generator.py (PoetryGenerator). With the same vocabulary, CMU dictionary and seed it makes
// the same poem as `random.seed(seed); PoetryGenerator(ProsodyAnalyzer()).generate_<form>(...)` in Python: every
// random call is made in the same order through PyRandom (CPython's Mersenne Twister). Node-tested on the fixture.
import { PyRandom, IndexError } from './pyrandom.js';
import { countSyllables, getRhymingWords, pySplit } from './prosody_engine.js';

const TEMPLATES = {
  haiku: { structure: [5, 7, 5], focus: ['nature', 'sensory', 'emotion'] },
  tanka: { structure: [5, 7, 5, 7, 7], focus: ['emotion', 'nature', 'abstract'] },
  sonnet: { structure: Array(14).fill(10), rhyme_scheme: 'ABABCDCDEFEFGG' },
  free_verse: { min_lines: 4, max_lines: 8, min_syllables: 5, max_syllables: 12 },
};
const METAPHORS = ['like {} in {}', '{} of {}', '{} beneath {}', '{} among {}', 'through {} like {}', '{} within {}'];
const SIMPLE = ['{} {}', '{} in {}', '{} like {}', '{} through {}'];
const COMPLEX = ['{} {} in the {}', '{} like {} {}', '{} through the {}', 'where {} meets {}', '{} of {} {}'];

const fill = (template, words) => { let i = 0; return template.replace(/\{\}/g, () => words[i++]); };
const phraseSyllables = phrase => pySplit(phrase).reduce((s, w) => s + countSyllables(w), 0);

export class PoetryGenerator {
  // vocab: {nature: [...], emotion: [...], abstract: [...], sensory: [...]} as vocabulary.get_all_words()
  constructor(vocab, seed = 0) {
    this.rng = new PyRandom(seed);
    this.cache = new Map();  // category -> Map(syllables -> words); mirrors the nested defaultdict
    for (const [cat, words] of Object.entries(vocab)) {
      const bySyll = new Map();
      for (const w of words) {
        const n = countSyllables(w);
        if (!bySyll.has(n)) bySyll.set(n, []);
        bySyll.get(n).push(w);
      }
      this.cache.set(cat, bySyll);
    }
  }
  seed(n) { this.rng.seed(n); }
  hasMood(mood) { return !!mood && this.cache.has(mood); }
  // word_cache[cat][syll]: inner defaultdict access that creates an empty list (affects later `in` checks)
  slot(cat, syll) {
    const m = this.cache.get(cat);
    if (!m.has(syll)) m.set(syll, []);
    return m.get(syll);
  }
  wordsUpTo(cat, maxSyll) {
    const m = this.cache.get(cat), out = [];
    for (let s = 1; s <= maxSyll; s++) if (m.has(s)) out.push(...m.get(s));
    return out;
  }

  createMetaphor(mood) {
    const r = this.rng, categories = ['nature', 'emotion', 'abstract', 'sensory'];
    let primary, secondary;
    if (categories.includes(mood)) { primary = mood; secondary = r.choice(categories.filter(c => c !== mood)); }
    else [primary, secondary] = r.sample(categories, 2);
    const w1 = r.choice(this.slot(primary, r.randint(1, 2)));
    const w2 = r.choice(this.slot(secondary, r.randint(1, 2)));
    return fill(r.choice(METAPHORS), [w1, w2]);
  }

  createImagePhrase(syllables, mood) {
    const r = this.rng;
    const template = r.choice(syllables < 6 ? SIMPLE : COMPLEX);
    const needed = template.split('{}').length - 1;
    let categories = ['nature', 'sensory', 'abstract'];
    if (this.hasMood(mood)) categories = [mood, ...categories.filter(c => c !== mood)];
    const words = [];
    let remaining = syllables;
    for (let k = 0; k < needed; k++) {
      if (remaining <= 0) break;
      let attempts = 0, found = false;
      while (attempts < 10 && !found) {
        const possible = this.wordsUpTo(r.choice(categories), remaining);
        if (possible.length) {
          const word = r.choice(possible), n = countSyllables(word);
          if (n <= remaining) { words.push(word); remaining -= n; found = true; }
        }
        attempts++;
      }
    }
    if (words.length < needed) return this.createSimplePhrase(syllables, mood);
    return fill(template, words);
  }

  createSimplePhrase(syllables, mood) {
    const category = this.hasMood(mood) ? mood : this.rng.choice(['nature', 'sensory', 'abstract']);
    const m = this.cache.get(category);
    for (let s = 1; s <= syllables; s++) if (m.has(s) && m.get(s).length) return this.rng.choice(m.get(s));
    return 'gentle';
  }

  generateLine(syllables, mood = null, endWord = null, lineType = 'standard') {
    const r = this.rng;
    if (syllables < 3) {
      if (this.hasMood(mood)) {
        const m = this.cache.get(mood);
        for (let s = 1; s <= syllables; s++) if (m.has(s)) return r.choice(m.get(s));
      }
      return 'oh';
    }
    if (lineType === 'metaphor' && r.random() < 0.7) {
      try {
        const metaphor = this.createMetaphor(mood);
        if (phraseSyllables(metaphor) <= syllables) return metaphor;
      } catch (e) { if (!(e instanceof IndexError)) throw e; }
    }
    if (lineType === 'image' || r.random() < 0.3) {
      const image = this.createImagePhrase(syllables, mood);
      if (phraseSyllables(image) <= syllables) return image;
    }
    let primary, secondary;
    const keys = [...this.cache.keys()];
    if (this.hasMood(mood)) { primary = mood; secondary = keys.filter(c => c !== mood); }
    else { primary = r.choice(keys); secondary = keys.filter(c => c !== primary); }

    const words = [];
    let current = 0;
    while (current < syllables) {
      const remaining = syllables - current;
      const possible = this.wordsUpTo(r.choice([primary, ...secondary]), remaining);
      if (!possible.length) { if (!words.length) return 'gentle wind'; break; }
      const word = r.choice(possible);
      words.push(word);
      current += countSyllables(word);
    }
    if (endWord && words.length) {
      const before = words.slice(0, -1).reduce((s, w) => s + countSyllables(w), 0);
      if (before + countSyllables(endWord) <= syllables) words[words.length - 1] = endWord;
    }
    return words.join(' ');
  }

  generateHaiku(mood = null) {
    const { structure, focus } = TEMPLATES.haiku;
    return structure.map((n, i) => this.generateLine(n, mood || focus[i % focus.length], null,
      i === 1 ? 'image' : 'standard')).join('\n');
  }

  generateTanka(mood = null) {
    const { structure, focus } = TEMPLATES.tanka;
    return structure.map((n, i) => this.generateLine(n, mood || focus[i % focus.length], null,
      i === 1 ? 'image' : 'standard')).join('\n');
  }

  generateFreeVerse(numLines = null, mood = null) {
    const t = TEMPLATES.free_verse, r = this.rng;
    if (!numLines) numLines = r.randint(t.min_lines, t.max_lines);
    const lines = [];
    let prev = null;
    for (let i = 0; i < numLines; i++) {
      let n;
      if (prev) n = Math.max(t.min_syllables, Math.min(t.max_syllables, prev + r.randint(-2, 2)));
      else n = r.randint(t.min_syllables, t.max_syllables);
      const lineType = i % 3 === 0 ? 'metaphor' : i % 3 === 1 ? 'image' : 'standard';
      lines.push(this.generateLine(n, mood, null, lineType));
      prev = n;
    }
    return lines.join('\n');
  }

  generateSonnet(mood = null) {
    const scheme = TEMPLATES.sonnet.rhyme_scheme, syllables = TEMPLATES.sonnet.structure[0];
    const rhymeWords = new Map(), lines = [];
    for (let i = 0; i < scheme.length; i++) {
      const rhyme = scheme[i];
      const lineType = i % 4 === 0 ? 'metaphor' : i % 4 === 2 ? 'image' : 'standard';
      if (rhymeWords.has(rhyme)) {
        const endWord = this.rng.choice(rhymeWords.get(rhyme));
        lines.push(this.generateLine(syllables, mood, endWord, lineType));
      } else {
        const line = this.generateLine(syllables, mood, null, lineType);
        lines.push(line);
        const parts = pySplit(line), found = getRhymingWords(parts[parts.length - 1]);
        if (found.length) rhymeWords.set(rhyme, found);
      }
    }
    return lines.join('\n');
  }

  // form: 'haiku' | 'tanka' | 'sonnet' | 'free_verse' (the forms PoetryGenerator has methods for)
  generate(form, { mood = null, numLines = null } = {}) {
    if (form === 'haiku') return this.generateHaiku(mood);
    if (form === 'tanka') return this.generateTanka(mood);
    if (form === 'sonnet') return this.generateSonnet(mood);
    if (form === 'free_verse') return this.generateFreeVerse(numLines, mood);
    throw new Error('Unknown form: ' + form);
  }
}

export const FORMS = ['haiku', 'tanka', 'sonnet', 'free_verse'];
export const MOODS = ['nature', 'emotion', 'abstract', 'sensory'];
