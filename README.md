# Emotional Enhancement of Cloned Voices via Speaker-Embedding Editing — Demo Page

Demo page for the paper "Emotional Enhancement of Cloned Voices via
Speaker-Embedding Editing".

## Contents

- `index.html` — static demo page (no build step, no external dependencies)
- `figures/` — method overview figures (rendered from the paper)
- `audio/` — 10 curated evaluation cases (5 zero-shot cloning + 5 native
  emotional instruction), selected from the 18-speaker text-driven evaluation
  for best identity preservation and highest emotion-cosine gains.
  Per case: reference (ground-truth neutral), unedited, pooled-affect
  baseline (alpha = 1), ours (alpha = 1), ours norm-matched, target
  (ground-truth emotional, anchor only).
- `cases_manifest.json` — per-case metadata and objective metrics
  (emotion-cosine gain, emotion cosine, identity cosine)
- `tools/build_curated_set.py` — rebuilds `audio/` + manifest from the
  evaluation run
- `tools/build_page.py` — regenerates `index.html` (fill in the author /
  arXiv / GitHub placeholders at the top of the script first)

## Serve locally

```bash
python3 -m http.server 8080
# open http://localhost:8080
```

## Deploy

This repository is designed for GitHub Pages: push to a repository and enable
"GitHub Pages -> deploy from branch -> main / (root)". The page uses only
relative paths, so it works both at a repository subpath
(`https://<user>.github.io/<repo>/`) and at a custom domain.
