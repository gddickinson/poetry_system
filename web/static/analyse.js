// Analyse: paste a poem and see syllables per line, rhyme scheme (CMU rhyming parts) and stress patterns
// (analyze_meter). Imagery and sentiment need spaCy and TextBlob, so they appear only on the local app.
import { route, api, app, esc, $, isStatic, needsServer } from './core.js';
import { poemHtml, rhymeTag, takeHandoff } from './ui.js';

const imageryHtml = imagery => {
  const keys = Object.keys(imagery || {});
  if (!keys.length) return '<p class="mute">No words from the vocabulary lists found.</p>';
  return `<table><tr><th>Category</th><th>Words</th></tr>${keys.map(k =>
    `<tr><td>${esc(k)}</td><td>${esc(imagery[k].join(', '))}</td></tr>`).join('')}</table>`;
};

route('analyse', async () => {
  const samples = await api('/samples');
  const examples = [...samples.quoted, ...samples.readme];
  const initial = takeHandoff() || examples[1].text;
  app().innerHTML = `
  <h1 class="glow">Analyse</h1>
  <p class="lead">Syllables, rhyme scheme and metre from the CMU pronouncing dictionary, as computed by
    <code>core/prosody.py</code>${isStatic() ? ' (here: its JavaScript port, same results)' : ''}.</p>
  <div class="two">
    <div>
      <label for="poem">Poem (one line per line)</label>
      <textarea id="poem" rows="9">${esc(initial)}</textarea>
      <button type="button" id="go">Analyse</button>
      <label for="ex">Or load an example from the repo</label>
      <select id="ex"><option value="">choose...</option>${examples.map((e, i) =>
        `<option value="${i}">${esc(e.title)}</option>`).join('')}</select>
    </div>
    <div class="panel"><h3>Rhyme scheme</h3><div class="scheme" id="scheme">-</div>
      <p class="small mute">Lines whose last words share the CMU "rhyming part" (stressed vowel to the end) get the same
        letter; words not in the dictionary only match themselves.</p>
      <div id="nlp"></div></div>
  </div>
  <div class="panel" id="lines" aria-live="polite"></div>
  <p class="legend">Stress: <b>/</b> primary, <b>\\</b> secondary, <b>x</b> unstressed (first CMU pronunciation of each
    word; words not in the dictionary get an alternating guess). Syllables use the same dictionary with a vowel-group
    fallback.</p>`;

  const run = async () => {
    const poem = $('#poem').value;
    const r = await api('/analyze', { body: { poem } });
    $('#scheme').innerHTML = r.scheme ? [...r.scheme].map(rhymeTag).join(' ') : '-';
    $('#lines').innerHTML = r.lines.length ? `<h3>Lines</h3>${poemHtml(r.lines)}` : '<p class="mute">Paste a poem above.</p>';
    const nlp = r.nlp;
    $('#nlp').innerHTML = nlp.available
      ? `<h3>Imagery (vocabulary words found)</h3>${imageryHtml(nlp.imagery)}<h3>Sentiment (TextBlob)</h3>
         <p class="mono">polarity ${nlp.sentiment.polarity.toFixed(3)} · subjectivity ${nlp.sentiment.subjectivity.toFixed(3)}</p>`
      : `<h3>Imagery and sentiment</h3>${nlp.static ? needsServer('Imagery and sentiment analysis (spaCy, TextBlob)')
        : `<p class="small mute">Unavailable on this server: ${esc(nlp.reason)}. Install spacy, textblob and en_core_web_sm.</p>`}`;
  };
  $('#go').addEventListener('click', run);
  $('#ex').addEventListener('change', e => {
    if (e.target.value !== '') { $('#poem').value = examples[+e.target.value].text; run(); }
  });
  await run();
});
