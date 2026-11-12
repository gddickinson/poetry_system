// JavaScript port of core/prosody.py on the compact CMU dictionary exported by web/cmu_data.py:
// count_syllables, clean_word, rhyme_keys_for, analyze_rhyme_scheme, analyze_meter and get_rhyming_words
// (pronouncing.rhymes). Node-tested against the Python on tests/fixtures/poem_fixture.json.

const PUNCT = new Set('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~');  // Python string.punctuation

let lookup = null;       // word -> [[stresses, rpIndex], ...] in dictionary order
let rhymeLookup = null;  // rpIndex -> [words...] in dictionary order (as pronouncing.rhyme_lookup)
let rhymeParts = null;

// Load the {rp, entries} object from api('/cmu') (or the Python export in tests).
export function loadCmu(data) {
  rhymeParts = data.rp;
  lookup = new Map();
  rhymeLookup = new Map();
  for (const row of data.entries.split('|')) {
    const [word, stresses, hex] = row.split(' ');
    const rp = parseInt(hex, 16);
    if (!lookup.has(word)) lookup.set(word, []);
    lookup.get(word).push([stresses, rp]);
    if (!rhymeLookup.has(rp)) rhymeLookup.set(rp, []);
    rhymeLookup.get(rp).push(word);
  }
}
export const cmuLoaded = () => lookup !== null;

function phonesForWord(word) {
  if (!lookup) throw new Error('CMU dictionary not loaded');
  return lookup.get(word.toLowerCase()) || [];
}

// Python str.strip(chars) / str.split() / str.strip() equivalents.
function stripChars(s, set) {
  let a = 0, b = s.length;
  while (a < b && set.has(s[a])) a++;
  while (b > a && set.has(s[b - 1])) b--;
  return s.slice(a, b);
}
export const pySplit = s => s.split(/\s+/).filter(Boolean);
const pyStrip = s => s.trim();

export const cleanWord = w => stripChars(w.toLowerCase(), PUNCT);

export function countSyllables(word) {
  if (!word || typeof word !== 'string') return 1;
  word = pyStrip(word);
  if (!word) return 1;
  let phones = phonesForWord(word);
  if (!phones.length) phones = phonesForWord(cleanWord(word));
  if (phones.length) return phones[0][0].length;
  const vowels = 'aeiouy';
  word = cleanWord(word);
  if (!word.length) return 1;  // Python: word[0] raises IndexError, caught -> 1
  let count = vowels.includes(word[0]) ? 1 : 0;
  for (let i = 1; i < word.length; i++) if (vowels.includes(word[i]) && !vowels.includes(word[i - 1])) count++;
  if (word.endsWith('e')) count--;
  return Math.max(1, count);
}

// pronouncing.rhymes(word): words sharing the rhyming part of the word's first pronunciation, minus the word.
export function rhymes(word) {
  const phones = phonesForWord(word);
  if (!phones.length) return [];
  return (rhymeLookup.get(phones[0][1]) || []).filter(w => w !== word);
}
export const getRhymingWords = word => rhymes(cleanWord(word));

// Keys of every pronunciation's rhyming part (core/prosody.py rhyme_keys_for), else the word itself.
export function rhymeKeysFor(word) {
  word = cleanWord(word);
  const phones = phonesForWord(word);
  return new Set(phones.length ? phones.map(p => 'sound:' + rhymeParts[p[1]]) : ['word:' + word]);
}

const poemLines = poem => poem.split('\n').map(pyStrip).filter(Boolean);
const isBlank = poem => !poem || typeof poem !== 'string' || !pyStrip(poem);

export function analyzeRhymeScheme(poem) {
  if (isBlank(poem)) return '';
  const seen = [];  // [keys, letter] of earlier lines, in order
  let out = '', next = 0;
  for (const line of poemLines(poem)) {
    const words = pySplit(line);
    if (!words.length) continue;
    const keys = rhymeKeysFor(words[words.length - 1]);
    const hit = seen.find(([ks]) => [...keys].some(k => ks.has(k)));
    const letter = hit ? hit[1] : String.fromCharCode(65 + next++);
    seen.push([keys, letter]);
    out += letter;
  }
  return out;
}

export function analyzeMeter(poem) {
  if (isBlank(poem)) return [];
  return poemLines(poem).map(line => {
    const pattern = [];
    for (const word of pySplit(line).map(cleanWord)) {
      if (!/\p{L}/u.test(word)) continue;
      const phones = phonesForWord(word);
      if (phones.length) { for (const c of phones[0][0]) pattern.push(+c); continue; }
      const n = countSyllables(word);
      for (let i = 0; i < Math.floor(n / 2); i++) pattern.push(1, 0);
      if (n % 2) pattern.push(1);
    }
    return pattern;
  });
}

// Per-line view used by the Analyse page and /api/analyze: words, syllables, stress, rhyme letter.
export function analyzeLines(poem) {
  const scheme = analyzeRhymeScheme(poem), meter = analyzeMeter(poem);
  return poemLines(poem).map((line, i) => {
    const words = pySplit(line);
    return { text: line, syllables: words.reduce((s, w) => s + countSyllables(w), 0),
      stress: meter[i], rhyme: scheme[i] || '', end: words.length ? cleanWord(words[words.length - 1]) : '' };
  });
}
