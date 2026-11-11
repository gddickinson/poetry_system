// Compose: generate a haiku, sonnet or free verse with the repo's generator (Python on the local app, the exact JS
// port on the static site). Form, mood and seed live in the URL, so a poem can be shared and recreated.
import { route, api, app, esc, $, $$, isStatic } from './core.js';
import { poemHtml, FORM_NAMES, TARGETS, pyCall, sendToAnalyse } from './ui.js';

const randomSeed = () => Math.floor(Math.random() * 100000);

route('compose', async (args, query) => {
  const info = await api('/info');
  const state = {
    form: info.forms[query.form] ? query.form : 'haiku',
    mood: info.moods.includes(query.mood) ? query.mood : '',
    seed: query.seed !== undefined && query.seed !== '' && Number.isInteger(+query.seed) && +query.seed >= 0
      ? +query.seed : randomSeed(),
    num_lines: +query.lines || '',
  };
  app().innerHTML = `
  <h1 class="glow">Compose</h1>
  <p class="lead">${isStatic()
    ? 'The generator runs in your browser: a JavaScript port of <code>core/generator.py</code> that makes the same poem as the Python for the same seed.'
    : 'Poems come from <code>core/generator.py</code> running on the local Python server.'}</p>
  <div class="compose">
    <form class="controls" id="ctl">
      <label id="form-l">Form</label>
      <div class="seg" role="group" aria-labelledby="form-l">${Object.keys(info.forms).map(f =>
        `<button type="button" data-form="${f}">${FORM_NAMES[f]}</button>`).join('')}</div>
      <p class="small mute" id="form-desc"></p>
      <label for="mood">Mood (vocabulary category)</label>
      <select id="mood"><option value="">default for the form</option>${info.moods.map(m =>
        `<option value="${m}">${m}</option>`).join('')}</select>
      <div id="lines-box"><label for="lines">Lines (free verse; blank = 4 to 8 at random)</label>
        <input id="lines" type="number" min="1" max="40" placeholder="random"></div>
      <div class="seedrow"><div style="flex:1"><label for="seed">Seed</label>
        <input id="seed" type="number" min="0" max="2147483647"></div>
        <button type="button" class="alt" id="reseed" title="new random seed">New seed</button></div>
      <button type="submit">Generate</button>
    </form>
    <div>
      <div class="panel" id="out" aria-live="polite"><p class="mute">Generating...</p></div>
      <p class="legend">Each line: syllable count (CMU dictionary) against the form's target, and its stress pattern:
        <b>/</b> primary stress, <b>\\</b> secondary, <b>x</b> unstressed. Sonnets also show the rhyme letter each line
        actually got (the generator ends a line on a rhyme only when one fits the syllable count).</p>
    </div>
  </div>`;

  const show = () => {
    $$('[data-form]').forEach(b => b.classList.toggle('on', b.dataset.form === state.form));
    $('#form-desc').textContent = info.forms[state.form];
    $('#mood').value = state.mood;
    $('#seed').value = state.seed;
    $('#lines').value = state.num_lines;
    $('#lines-box').hidden = state.form !== 'free_verse';
  };
  const run = async () => {
    const q = new URLSearchParams({ form: state.form, mood: state.mood, seed: state.seed });
    if (state.form === 'free_verse' && state.num_lines) q.set('lines', state.num_lines);
    history.replaceState(null, '', '#/compose?' + q);
    const body = { form: state.form, mood: state.mood || null, seed: state.seed,
      num_lines: state.form === 'free_verse' && state.num_lines ? state.num_lines : null };
    const out = $('#out');
    try {
      const r = await api('/generate', { body });
      out.innerHTML = `<h3>${FORM_NAMES[r.form]} · mood ${esc(r.mood || 'default')} · seed ${r.seed}</h3>
        ${poemHtml(r.lines, { target: TARGETS[r.form] || null, rhyme: r.form === 'sonnet' })}
        <p class="pycall">Python: ${esc(pyCall(body))}</p>
        <button type="button" class="alt" id="to-analyse">Analyse this poem</button>
        <button type="button" class="alt" id="copy">Copy text</button>`;
      $('#to-analyse').onclick = () => sendToAnalyse(r.text);
      $('#copy').onclick = () => navigator.clipboard?.writeText(r.text);
    } catch (e) {
      out.innerHTML = `<p class="err">${esc(e.message)}</p>`;
    }
  };

  $$('[data-form]').forEach(b => b.addEventListener('click', () => { state.form = b.dataset.form; show(); run(); }));
  $('#mood').addEventListener('change', e => { state.mood = e.target.value; run(); });
  $('#reseed').addEventListener('click', () => { state.seed = randomSeed(); show(); run(); });
  $('#ctl').addEventListener('submit', e => {
    e.preventDefault();
    state.seed = Math.max(0, Math.min(2147483647, Math.floor(+$('#seed').value || 0)));
    const n = Math.floor(+$('#lines').value);
    state.num_lines = n >= 1 && n <= 40 ? n : '';
    show(); run();
  });
  show();
  await run();
});
