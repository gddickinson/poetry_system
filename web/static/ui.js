// Shared rendering for poems: per-line syllables, stress patterns (CMU digits) and rhyme letters.
import { esc } from './core.js';

const RHYME_COLOURS = ['#c39bff', '#ff7eb6', '#7fd6ff', '#ffd27f', '#8dffb0', '#ff9d7f', '#b4c2ff', '#f0a6ff'];
export const rhymeColour = letter => RHYME_COLOURS[(letter.charCodeAt(0) - 65) % RHYME_COLOURS.length];
export const rhymeTag = letter => letter ? `<span class="rh" style="background:${rhymeColour(letter)}">${esc(letter)}</span>` : '';

// Stress digits as scansion marks: 1 primary (/), 2 secondary (\), 0 unstressed (x).
const MARK = { 0: 'x', 1: '/', 2: '\\' };
export function stressMarks(stress) {
  return `<span class="stress" aria-label="stress pattern ${esc(stress.join(''))}">${
    stress.map(d => `<span class="s${d}">${MARK[d]}</span>`).join(' ')}</span>`;
}

// lines: [{text, syllables, stress, rhyme}] from /generate or /analyze. target: syllables per line, if any.
export function poemHtml(lines, { target = null, stress = true, rhyme = true } = {}) {
  return `<div class="poem">${lines.map((l, i) => {
    const t = Array.isArray(target) ? target[i] : target;
    const syl = t ? `<b>${l.syllables}</b>/${t}` : `<b>${l.syllables}</b>`;
    return `<div class="ln"><span class="no">${i + 1}</span><span>${esc(l.text)}${stress ? stressMarks(l.stress) : ''}</span>
      <span class="meta">${syl} syl ${rhyme ? rhymeTag(l.rhyme) : ''}</span></div>`;
  }).join('')}</div>`;
}

export const FORM_NAMES = { haiku: 'Haiku', sonnet: 'Sonnet', free_verse: 'Free verse' };
export const TARGETS = { haiku: [5, 7, 5], sonnet: 10 };

// Python call that reproduces a seeded poem.
export function pyCall({ form, mood, seed, num_lines }) {
  const args = [];
  if (form === 'free_verse' && num_lines) args.push(`num_lines=${num_lines}`);
  if (mood) args.push(`mood='${mood}'`);
  return `random.seed(${seed}); generator.generate_${form}(${args.join(', ')})`;
}

// Hand a poem to the Analyse page (sessionStorage when available, else in memory).
let handoff = null;
export function sendToAnalyse(text) {
  handoff = text;
  try { sessionStorage.setItem('poem', text); } catch (e) { /* private mode: memory only */ }
  location.hash = '#/analyse';
}
export function takeHandoff() {
  let t = handoff;
  try { t = t ?? sessionStorage.getItem('poem'); sessionStorage.removeItem('poem'); } catch (e) { /* ignore */ }
  handoff = null;
  return t;
}
