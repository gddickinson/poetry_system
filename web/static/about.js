// About: what the project is, how generation and analysis work, what runs where, how to run it, credits.
import { route, api, app, esc, isStatic } from './core.js';
import { FORM_NAMES } from './ui.js';

route('about', async () => {
  const info = await api('/info');
  app().innerHTML = `
  <h1 class="glow">About</h1>
  <p class="lead">Poetry System is a Python system for generating and analysing poetry with natural language processing
    and computational creativity techniques: structured poetic forms filled from mood-categorised vocabularies, and
    analysis of rhyme, metre, imagery and sentiment.</p>

  <h2>Generation</h2>
  <p><code>core/generator.py</code> (<code>PoetryGenerator</code>) builds lines word by word to a syllable budget, from
    four vocabulary lists in <code>vocabulary/</code>: ${Object.entries(info.vocabulary).map(([k, n]) =>
      `${esc(k)} (${n} words)`).join(', ')}. Lines are plain word runs, metaphors ("{} of {}", "like {} in {}", ...) or
    image phrases ("where {} meets {}", ...).</p>
  <table><tr><th>Form</th><th>What the generator does</th></tr>
    ${Object.entries(info.forms).map(([f, d]) => `<tr><td>${FORM_NAMES[f]}</td><td>${esc(d)}</td></tr>`).join('')}</table>
  <p class="small mute">A tanka template (5-7-5-7-7) is defined in the generator but has no generate method yet, so it is
    not offered here.</p>

  <h2>Analysis</h2>
  <ul>
    <li><b>Syllables</b>: CMU Pronouncing Dictionary via <code>pronouncing</code>, with a vowel-group guess for unknown words.</li>
    <li><b>Rhyme scheme</b>: line endings that share the CMU rhyming part get the same letter.</li>
    <li><b>Metre</b>: per-line stress patterns (<code>analyze_meter</code>, restored from the simple version).</li>
    <li><b>Imagery</b>: which words belong to the vocabulary categories (spaCy tokeniser), and <b>sentiment</b>
      (TextBlob polarity and subjectivity). These need the NLP models, so they run only in the local app.</li>
  </ul>

  <h2>What runs where</h2>
  <p>${isStatic() ? 'You are on the static site.' : 'You are on the local app.'} On the static site the generator, the
    Mersenne Twister behind Python's <code>random</code>, and the syllable, rhyme and metre code run as a JavaScript port
    that a node test checks against the Python on fixed seeds and texts: same seed, same poem. The CMU data
    (${info.cmu_entries.toLocaleString('en')} pronunciations) is loaded once, about 0.9 MB compressed. Imagery and
    sentiment show a "needs the local app" note.</p>

  <h2>Run it</h2>
  <pre>pip install spacy textblob pronouncing
python -m spacy download en_core_web_sm
python main.py                      # desktop demo: a haiku, free verse and an analysis

pip install -r requirements-web.txt
python run_web.py                   # web app on http://127.0.0.1:8139</pre>
  <p class="small mute">The web app works without spaCy and TextBlob; install them to see imagery and sentiment.</p>

  <h2>Fixed while adding this site (November 2026)</h2>
  <ul class="small">
    <li>Sonnets crashed (the generator called a missing <code>get_rhyming_words</code>).</li>
    <li>Generated lines could run over their syllable count (phrases were counted as one unknown word).</li>
    <li>Words with punctuation attached ("fire,") missed the dictionary; some rhyming pairs ("at" / "bat") got different letters.</li>
    <li>Moods other than the four categories added an empty word category.</li>
  </ul>

  <h2>Credits</h2>
  <p>By George Dickinson, built with AI assistance from Claude (Anthropic); MIT licence. Uses
    <a href="https://github.com/aparrish/pronouncingpy">pronouncing</a> (Allison Parrish) and the
    CMU Pronouncing Dictionary, <a href="https://spacy.io/">spaCy</a> and
    <a href="https://textblob.readthedocs.io/">TextBlob</a>.
    <a href="https://github.com/gddickinson/poetry_system">Source on GitHub</a>.</p>`;
});
