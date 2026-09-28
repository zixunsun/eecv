#!/usr/bin/env python3
"""Assemble the human-rated demo set: copy re-rendered dose audio of the 8
selected cases into demo_site/audio, with per-case 16-listener MOS ratings."""
import json, os, shutil

RUN = '/apdcephfs/share_2967269/zixunsun/SPK/exp/dynamic_voiceprint/runs/demo_selected_dose_20260927'
PLAN = '/apdcephfs/share_2967269/zixunsun/SPK/exp/dynamic_voiceprint/evaluation/cv3_mos_speaker_intensity_20260922_v2/DEMO_SELECTED_PLAN.json'
MOS = '/apdcephfs/share_2967269/zixunsun/SPK/paper/review/mos_final_20260925_n16x2_v5/out/MOS_RESULT_v5.json'
SITE = '/apdcephfs/share_2967269/zixunsun/SPK/demo_site'
ARMS = ['unedited', 'film_a1.5', 'film_a3', 'film_a5']

plan = json.load(open(PLAN, encoding='utf-8'))
mos = json.load(open(MOS, encoding='utf-8'))
ratings = {(r['case_id'], r['arm']): r for r in mos['case_means']}

aud = os.path.join(RUN, 'audio')
assert os.path.isdir(aud), 'render output missing: ' + aud
files = os.listdir(aud)

root = os.path.join(SITE, 'audio')
if os.path.exists(root):
    shutil.rmtree(root)
os.makedirs(root)

LANG = {'zh': 'Chinese', 'en': 'English'}
manifest = []
for c in plan['cases']:
    cid = c['case_id']
    spk_num = c['speaker'].split('_')[1]
    dirname = f"{c['language']}_{c['emotion']}_spk{spk_num}"
    cdir = os.path.join(root, dirname)
    os.makedirs(cdir)
    shutil.copy2(c['reference_wav'], os.path.join(cdir, 'reference.wav'))
    for arm in ARMS:
        name = f"{cid}__{arm}.wav"
        assert name in files, 'missing ' + name
        shutil.copy2(os.path.join(aud, name), os.path.join(cdir, arm + '.wav'))
    r5 = ratings[(cid, 'film_a5')]
    r0 = ratings[(cid, 'unedited')]
    manifest.append({
        'case': dirname, 'language': LANG[c['language']],
        'speaker_label': f"Speaker {int(spk_num)} ({LANG[c['language']]})",
        'emotion': c['emotion'], 'text': c['text'],
        # human ratings at alpha=5 (16-listener MOS, 1-5 scale)
        'E': round(r5['emotion'], 2), 'N': round(r5['naturalness'], 2),
        'I': round(r5['intensity'], 2), 'S': round(r5['similarity'], 2),
        'n': r5['n_listener_ratings'],
        'dE': round(r5['emotion'] - r0['emotion'], 2),
    })

json.dump(manifest, open(os.path.join(SITE, 'cases_manifest.json'), 'w',
                         encoding='utf-8'), ensure_ascii=False, indent=1)
print('cases:', len(manifest), 'files:', sum(len(f) for _, _, f in os.walk(root)))
for m in manifest:
    print(m['case'], '| E=%s N=%s I=%s S=%s (dE=%+.2f, n=%d)' % (m['E'], m['N'], m['I'], m['S'], m['dE'], m['n']), '|', m['text'][:24])
