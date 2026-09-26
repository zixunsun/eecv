#!/usr/bin/env python3
"""Build the curated demo set: copy best cases (identity-preserved + highest
emotion gain) from the Table 1 evaluation run into demo_site/audio."""
import json, os, shutil, glob

RUN = '/apdcephfs/share_2967269/zixunsun/SPK/exp/dynamic_voiceprint/runs/table1_magnitude_h20_20260925_v1'
SITE = '/apdcephfs/share_2967269/zixunsun/SPK/demo_site'

# curated selection: (regime, case_id prefix) — chosen from PER_CASE.json by
# high e2v gain + high identity cosine + zero text error, balanced across
# language and emotion; see cases_manifest.json for the recorded metrics.
SELECTED = [
    ('default',        '4e5c427d8ed8012f8b1b0f36'),
    ('default',        '227fc09270edd6d8e008ebdf'),
    ('default',        '416f0155afd1'),
    ('default',        '18fbb560096a5e3468b65c31'),
    ('default',        '15c7d7020a79'),
    ('emotion_vector', '651a2f4d0d7e2b08e30b2ef0'),
    ('emotion_vector', '6918b5a9aac23c205247234e'),
    ('emotion_vector', '9121f3c1edf06fcfad9c18f0'),
    ('emotion_vector', '9008fad958d1'),
    ('emotion_vector', '43e25e53ff13'),
]
ARMS = ['unedited', 'pooled_a1', 'film_a1', 'film_matched_a1']

plan = json.load(open(RUN + '/PLAN.json'))
per_case = json.load(open(RUN + '/results/PER_CASE.json'))
metrics = {}
for x in per_case:
    metrics[(x['regime'], x['case_id'], x['arm'])] = x

# map full case_id -> plan entry
plan_by_id = {}
for entry in plan:
    plan_by_id[entry['case']['case_id']] = entry

aud_root = os.path.join(SITE, 'audio')
if os.path.exists(aud_root):
    shutil.rmtree(aud_root)
os.makedirs(aud_root)

LANG = {'zh': 'Chinese', 'en': 'English'}
manifest = []
for reg, pref in SELECTED:
    matches = [e for cid, e in plan_by_id.items() if cid.startswith(pref)]
    assert len(matches) == 1, (reg, pref, len(matches))
    e = matches[0]
    c = e['case']
    fid = c['case_id']
    spk_num = c['speaker'].split('_')[1]
    lang = c['language']
    # case dir: zh_happy_spk08
    dirname = f"{lang}_{c['target_emotion']}_spk{spk_num}"
    cdir = os.path.join(aud_root, dirname)
    os.makedirs(cdir)
    # reference: enrollment neutral (single-clip policy)
    ref_wav = c['enrollment_neutral'][0]['wav']
    shutil.copy2(ref_wav, os.path.join(cdir, 'reference.wav'))
    # target GT (evaluator-only anchor)
    shutil.copy2(c['target_wav'], os.path.join(cdir, 'target.wav'))
    for arm in ARMS:
        src = os.path.join(RUN, 'audio', f"{fid}__{reg}__{arm}.wav")
        assert os.path.exists(src), src
        shutil.copy2(src, os.path.join(cdir, arm + '.wav'))
    f = metrics[(reg, fid, 'film_a1')]
    u = metrics[(reg, fid, 'unedited')]
    manifest.append({
        'case': dirname,
        'regime': reg,
        'regime_label': ('Zero-shot cloning' if reg == 'default'
                         else 'Native emotional instruction'),
        'language': LANG[lang],
        'speaker_label': f"Speaker {int(spk_num)} ({LANG[lang]})",
        'emotion': c['target_emotion'],
        'text': c['text'],
        'ref_text': c['enrollment_neutral'][0]['text'],
        'gain': round(f['e2v_cosine'] - u['e2v_cosine'], 4),
        'e2v_film': round(f['e2v_cosine'], 4),
        'cam_film': round(f['cam_cosine'], 4),
    })

# fill text from plan 'case' entries (query text lives in a different field)
for entry in plan:
    pass  # text extracted below if missing

json.dump(manifest, open(os.path.join(SITE, 'cases_manifest.json'), 'w',
                         encoding='utf-8'), ensure_ascii=False, indent=1)
n = sum(len(fs) for _, _, fs in os.walk(aud_root))
print('cases:', len(manifest), 'files:', n)
for m in manifest:
    print(m['case'], '|', m['regime'], '|', m['emotion'],
          '| gain %+.3f' % m['gain'], '| e2v %.3f' % m['e2v_film'],
          '| cam %.3f' % m['cam_film'], '|', m['text'][:30])
