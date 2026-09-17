# gal-orlanczyk.github.io

Public support/privacy pages for apps by Gal Orlanczyk, served by GitHub
Pages at https://gal-orlanczyk.github.io. Separate from each app's own
(usually private) source repo, since Pages requires a public repo on the
free plan and these pages (privacy policy, support) are meant to be public
anyway.

## Structure

```
index.html          Root "Apps" list, links to each app's /<slug>/
style.css            Shared styling for every page (light/dark aware)
assets/<slug>-icon.png   Each app's icon
<slug>/index.html    Per-app landing page (hero + links to privacy/support)
<slug>/privacy.html  Per-app privacy policy
<slug>/support.html  Per-app support page (links to this repo's Issues)
templates/*.tmpl     Templates used by scripts/new_app.py
scripts/new_app.py   Scaffolds a new app's pages
```

## Adding a new app's pages

```bash
scripts/new_app.py \
  --slug myapp \
  --name "My App" \
  --tagline "Short marketing headline." \
  --subhead "One sentence describing what it does." \
  --index-blurb "One line for the root apps list." \
  --icon /path/to/icon.png
```

This generates `<slug>/index.html`, `privacy.html`, `support.html`, copies
the icon to `assets/<slug>-icon.png`, and adds an entry to the root
`index.html`'s app list (skipped if already present — safe to re-run).

**Review the generated `privacy.html` and `support.html` before publishing**
— they're placeholders (marked `TODO`) that assume the app collects no data
and has no real FAQ yet. Edit anything that isn't actually true.

Then: `git add -A && git commit && git push` — GitHub Pages serves the new
pages automatically within a minute or two of the push.

## Support issues

Each app's support page links here to this repo's own Issues tab, so bug
reports/questions land in one place without needing a mailing address or a
public issue tracker on each app's (often private) source repo.
