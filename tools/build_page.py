#!/usr/bin/env python3
"""Generate index.html for the anonymous SPK demo page from cases_manifest.json."""
import json, html, os

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
manifest = json.load(open(os.path.join(SITE, 'cases_manifest.json'), encoding='utf-8'))

EMO = {'angry': ('Angry', '#c0392b', '&#128544;'),
       'happy': ('Happy', '#d68910', '&#128522;'),
       'sad': ('Sad', '#2471a3', '&#128546;'),
       'surprised': ('Surprised', '#7d3c98', '&#128562;')}
EMO_ORDER = ['angry', 'happy', 'sad', 'surprised']


def ckey(m):
    spk = 0 if m['case'].startswith('spkA') else 1
    emo = EMO_ORDER.index(m['emotion'])
    idx = int(m['case'].rsplit('_', 1)[1])
    return (spk, emo, idx)


manifest = sorted(manifest, key=ckey)


def chip(emo):
    name, color, icon = EMO[emo]
    return (f'<span class="chip" style="background:{color}1a;color:{color};'
            f'border:1px solid {color}55">{icon}&nbsp;{name}</span>')


def audio(path):
    return (f'<audio controls preload="none" style="width:100%;height:36px">'
            f'<source src="audio/{path}" type="audio/wav">Your browser does not support audio.</audio>')


# ---------- main comparison rows ----------
main_rows = []
for i, m in enumerate(manifest, 1):
    c = m['case']
    txt = html.escape(m['text'])
    lang = 'zh' if c.startswith('spkA') else 'en'
    main_rows.append(f'''      <tr>
        <td class="cinfo"><div class="cid">Case {i:02d} &middot; {chip(m['emotion'])}</div>
          <div class="ctext" lang="{lang}">{txt}</div>
          <div class="cspk">{m['speaker_label']}</div></td>
        <td>{audio(c + '/reference.wav')}</td>
        <td>{audio(c + '/unedited.wav')}</td>
        <td>{audio(c + '/pooled_a1.5.wav')}</td>
        <td class="ours">{audio(c + '/film_a1.5.wav')}</td>
        <td class="ours">{audio(c + '/film_a2.5.wav')}</td>
        <td>{audio(c + '/target.wav')}</td>
      </tr>''')
main_rows = '\n'.join(main_rows)

# ---------- dose cards ----------
cards = []
for i, m in enumerate(manifest, 1):
    c = m['case']
    txt = html.escape(m['text'])
    lang = 'zh' if c.startswith('spkA') else 'en'
    arm_rows = [
        ('Reference', 'Ground-truth neutral recording', 'reference.wav', 'anchor'),
        ('Unedited', 'Frozen CV3, original speaker embedding (&alpha; = 0)', 'unedited.wav', 'base'),
        ('Ours &alpha; = 1.0', 'FiLM residual, strength 1.0', 'film_a1.wav', 'ours'),
        ('Ours &alpha; = 1.25', 'FiLM residual, strength 1.25', 'film_a1.25.wav', 'ours'),
        ('Ours &alpha; = 1.5', 'FiLM residual, strength 1.5', 'film_a1.5.wav', 'ours'),
        ('Ours &alpha; = 2.0', 'FiLM residual, strength 2.0', 'film_a2.wav', 'ours'),
        ('Ours &alpha; = 2.5', 'FiLM residual, strength 2.5', 'film_a2.5.wav', 'ours'),
        ('Pooled-affect &alpha; = 1.0', 'Shared-shift baseline, strength 1.0', 'pooled_a1.wav', 'base'),
        ('Pooled-affect &alpha; = 1.25', 'Shared-shift baseline, strength 1.25', 'pooled_a1.25.wav', 'base'),
        ('Pooled-affect &alpha; = 1.5', 'Shared-shift baseline, strength 1.5', 'pooled_a1.5.wav', 'base'),
        ('Target', 'Ground-truth emotional recording (reference anchor only)', 'target.wav', 'anchor'),
    ]
    rows = '\n'.join(
        f'          <tr class="r-{cls}"><td class="alabel">{lbl}</td>'
        f'<td class="adesc">{desc}</td><td>{audio(c + "/" + fn)}</td></tr>'
        for lbl, desc, fn, cls in arm_rows)
    cards.append(f'''    <div class="card">
      <div class="card-head">
        <div class="card-title">Case {i:02d} &nbsp;{chip(m['emotion'])}</div>
        <div class="ctext" lang="{lang}">&ldquo;{txt}&rdquo;</div>
        <div class="cspk">{m['speaker_label']}</div>
      </div>
      <table class="dose">
{rows}
      </table>
    </div>''')
cards = '\n'.join(cards)

CSS = ''':root{--ink:#1f2430;--muted:#5b6472;--accent:#2f5fe0;--accent2:#1d3fa8;--line:#e3e7ee;--bg:#f4f6fa;--card:#ffffff;--ours:#eef3ff;}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;color:var(--ink);background:var(--bg);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",Roboto,Helvetica,Arial,sans-serif;line-height:1.65}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px}
nav{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.92);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
nav .wrap{display:flex;align-items:center;gap:22px;height:56px}
nav .brand{font-weight:700;letter-spacing:.02em;color:var(--ink)}
nav .links{display:flex;gap:18px;margin-left:auto;flex-wrap:wrap}
nav a{color:var(--muted);font-size:14.5px}
nav a:hover{color:var(--accent);text-decoration:none}
header{padding:64px 0 40px;text-align:center}
.badges{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-bottom:18px}
.badge{font-size:13px;padding:5px 14px;border-radius:999px;border:1px solid var(--line);background:#fff;color:var(--muted)}
.badge.blue{border-color:#c7d6ff;background:#eef3ff;color:var(--accent2)}
h1{font-size:34px;line-height:1.25;margin:0 0 14px;letter-spacing:-.01em}
.authors{color:var(--muted);font-size:16px;margin-bottom:8px}
.note-line{color:var(--muted);font-size:13.5px}
section{padding:36px 0 8px}
h2{font-size:23px;margin:0 0 16px;padding-left:12px;border-left:4px solid var(--accent)}
.card-plain{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:26px 28px;box-shadow:0 1px 3px rgba(20,30,60,.05)}
.abstract{font-size:16px;text-align:justify}
figure{margin:20px 0 6px;text-align:center}
figure img{max-width:100%;border:1px solid var(--line);border-radius:10px;background:#fff}
figcaption{font-size:13.5px;color:var(--muted);margin-top:10px;text-align:left}
.method-grid{display:grid;grid-template-columns:1fr;gap:14px}
.chip{display:inline-block;font-size:12.5px;font-weight:600;padding:2px 10px;border-radius:999px;white-space:nowrap}
.tablewrap{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:12px;box-shadow:0 1px 3px rgba(20,30,60,.05)}
table.main{border-collapse:collapse;width:100%;min-width:1080px}
table.main th{background:#f8fafd;font-size:13px;color:var(--muted);font-weight:600;padding:10px;border-bottom:1px solid var(--line)}
table.main td{padding:10px;border-bottom:1px solid var(--line);vertical-align:middle;min-width:150px}
table.main tr:last-child td{border-bottom:none}
th.ours,td.ours{background:var(--ours)}
.cinfo{min-width:230px}
.cid{font-size:13px;font-weight:600;margin-bottom:4px}
.ctext{font-size:14px;margin:2px 0}
.cspk{font-size:12px;color:var(--muted);margin-top:2px}
.grid2{display:grid;grid-template-columns:repeat(auto-fill,minmax(430px,1fr));gap:18px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px 20px;box-shadow:0 1px 3px rgba(20,30,60,.05)}
.card-head{margin-bottom:10px}
.card-title{font-size:15px;font-weight:700}
table.dose{border-collapse:collapse;width:100%}
table.dose td{padding:5px 6px;border-bottom:1px dashed var(--line);vertical-align:middle}
table.dose tr:last-child td{border-bottom:none}
.alabel{font-size:13.5px;font-weight:600;white-space:nowrap;width:180px}
.adesc{font-size:12px;color:var(--muted);width:44%}
tr.r-ours td.alabel{color:var(--accent2)}
tr.r-anchor td{opacity:.92}
tr.r-anchor .alabel{color:var(--muted);font-weight:500}
.explain{font-size:14px;color:var(--muted);margin:0 0 18px}
footer{margin-top:48px;padding:26px 0 34px;border-top:1px solid var(--line);color:var(--muted);font-size:13px;text-align:center}
@media (max-width:760px){h1{font-size:26px} .grid2{grid-template-columns:1fr}}'''

ABSTRACT = '''Native emotion instructions guide speech planning, but do not directly specify how the acoustic
condition derived from a reference voice should change. We introduce a lightweight,
reference-conditioned speaker-embedding editor for enhancing emotional expression in frozen
text-to-speech synthesis. Trained on paired synthetic embeddings, the editor predicts a residual
from the reference embedding and requested emotion, allowing both direction and magnitude to
adapt to the reference rather than applying a shared shift. A scalar controls editing strength,
and the edited condition enters CosyVoice&nbsp;3 through its native acoustic interface without
updating the synthesizer or requiring target-emotion recordings at inference. By holding speech
tokens, acoustic prompts and decoding noise fixed, the method enables acoustic realization to be
adjusted independently of changes to the speech plan. Experiments across Chinese and English, in
both zero-shot and native emotional-instruction settings, show approximately 6.3&ndash;18.2% relative
gains in mean target-emotion cosine. Bilingual listening evaluation further supports improved
emotion appropriateness and conditional naturalness non-inferiority, alongside reduced speaker
similarity at higher editing strength.'''

page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Emotional Enhancement of Cloned Voices via Speaker-Embedding Editing</title>
<meta name="description" content="Anonymous demo page: reference-conditioned speaker-embedding editing for emotional enhancement of frozen TTS.">
<style>{CSS}</style>
</head>
<body>
<nav><div class="wrap">
  <span class="brand">Speaker-Embedding Editing</span>
  <div class="links">
    <a href="#abstract">Abstract</a><a href="#method">Method</a>
    <a href="#main">Main Comparison</a><a href="#dose">Dose Response</a>
  </div>
</div></nav>

<header><div class="wrap">
  <div class="badges">
    <span class="badge blue">Under Review at ICLR 2027</span>
    <span class="badge">Anonymous Authors</span>
    <span class="badge">Demo Page</span>
  </div>
  <h1>Emotional Enhancement of Cloned Voices via<br>Speaker-Embedding Editing</h1>
  <div class="authors">Anonymous authors &mdash; paper under double-blind review</div>
  <div class="note-line">Code and paper links will be provided upon publication.</div>
</div></header>

<section id="abstract"><div class="wrap">
  <h2>Abstract</h2>
  <div class="card-plain abstract">{ABSTRACT}</div>
</div></section>

<section id="method"><div class="wrap">
  <h2>Method</h2>
  <div class="card-plain method-grid">
    <p style="margin:0 0 6px">The editor takes a <b>reference speaker embedding</b> (192-d) and the
    <b>requested emotion</b> as input, and predicts a <b>residual edit</b> through lightweight FiLM
    blocks. A scalar <b>&alpha;</b> scales the predicted residual before it is added to the reference
    embedding and re-normalized. The edited condition then drives the <b>frozen CosyVoice&nbsp;3</b>
    synthesizer through its native acoustic interface &mdash; the planner and the Flow decoder remain
    unchanged, and no gradient passes through the synthesizer. At inference, no target-emotion
    recording of the speaker is required.</p>
    <figure>
      <img src="figures/figure2_architecture.png" alt="Method architecture" loading="lazy">
      <figcaption><b>Method overview.</b> The reference embedding, requested emotion and predicted
      residual, with a bypass path, strength &alpha; and normalization produce the edited condition
      <i>U<sub>&alpha;</sub></i> for frozen CV3. Paired synthetic neutral/target embeddings supervise only
      the editor; two width-256 FiLM residual blocks predict the edit. Speech tokens, the acoustic
      prompt and decoding noise are held fixed across the comparisons below.</figcaption>
    </figure>
    <figure>
      <img src="figures/figure1_story.png" alt="Why edit the speaker condition and how the edit is learned" loading="lazy">
      <figcaption><b>Why edit the speaker condition, and how is the edit learned?</b>
      (a) Emotion requests guide planning; reference-conditioned editing adds control of acoustic
      realization. (b) Real within-speaker variation motivates editing, while separate synthetic
      neutral/target pairs supervise the residual predictor. (c) The learned edit enters frozen CV3
      under matched text, tokens and decoding. (d) Historical direction studies provide complementary
      evidence, not replications of the main editor.</figcaption>
    </figure>
  </div>
</div></section>

<section id="main"><div class="wrap">
  <h2>Audio Demos &mdash; Main Comparison</h2>
  <p class="explain">For each case, a frozen CosyVoice&nbsp;3 voice clone is synthesized from the
  same reference recording and the same text. <b>Unedited</b> uses the original speaker embedding;
  <b>Ours</b> adds the predicted residual at two strengths; the <b>pooled-affect</b> baseline applies
  a shared emotion shift instead of a reference-conditioned prediction. The
  <b>Reference</b> (ground-truth neutral) and <b>Target</b> (ground-truth emotional) recordings are
  real recordings of the same speaker, shown as anchors only &mdash; the target recording is never used
  at inference.</p>
  <div class="tablewrap">
    <table class="main">
      <thead><tr>
        <th style="text-align:left">Case</th>
        <th>Reference<br><span style="font-weight:400">GT neutral</span></th>
        <th>Unedited<br><span style="font-weight:400">&alpha; = 0</span></th>
        <th>Pooled-affect<br><span style="font-weight:400">&alpha; = 1.5</span></th>
        <th class="ours">Ours<br><span style="font-weight:400">&alpha; = 1.5</span></th>
        <th class="ours">Ours<br><span style="font-weight:400">&alpha; = 2.5</span></th>
        <th>Target<br><span style="font-weight:400">GT emotional</span></th>
      </tr></thead>
      <tbody>
{main_rows}
      </tbody>
    </table>
  </div>
</div></section>

<section id="dose"><div class="wrap">
  <h2>Audio Demos &mdash; Full Dose Response</h2>
  <p class="explain">All arms of the evaluation set: the FiLM editor at five strengths
  (&alpha; = 1.0 &hellip; 2.5) and the pooled-affect shared-shift baseline at three strengths, together with the
  unedited output and the two ground-truth anchors. Higher &alpha; increases emotional intensity while
  speech content, tokens and decoding remain fixed.</p>
  <div class="grid2">
{cards}
  </div>
</div></section>

<footer><div class="wrap">
  Anonymous demo page accompanying a paper under double-blind review at ICLR 2027.<br>
  All audio is generated by a frozen CosyVoice 3 synthesizer; no target-emotion recording is used
  at inference. Audio files are in WAV format.
</div></footer>
</body>
</html>
'''
open(os.path.join(SITE, 'index.html'), 'w', encoding='utf-8').write(page)
print('index.html written:', len(page), 'chars,', len(manifest), 'cases')
