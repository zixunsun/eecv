# Emotional Enhancement of Cloned Voices via Speaker-Embedding Editing — Demo Page

Anonymous demo page for a paper under double-blind review at ICLR 2027.

## Contents

- `index.html` — static demo page (no build step, no external dependencies)
- `figures/` — method overview figures (rendered from the paper)
- `audio/` — 16 evaluation cases x 11 arms per case (reference, unedited,
  FiLM editor at alpha = 1.0 / 1.25 / 1.5 / 2.0 / 2.5, pooled-affect baseline at
  alpha = 1.0 / 1.25 / 1.5, target)
- `cases_manifest.json` — per-case metadata (speaker, requested emotion, text)
- `tools/build_page.py` — regenerates `index.html` from `cases_manifest.json`

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
