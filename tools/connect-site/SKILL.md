---
name: connect-site
description: Publish the current repo's website at jonaraphael.com/<slug>/ and keep it updating on every push. Use when the user asks to connect, publish, mount, host, or move a repo's page or site to jonaraphael.com, names a slug for a project site, or asks which projects are live under jonaraphael.com.
---

# Connect a repo's site to jonaraphael.com/<slug>/

## How it works

`jonaraphael/jonaraphael.github.io` is the GitHub Pages user site and carries the
custom domain `jonaraphael.com`. GitHub Pages serves every other Pages repo in
the account that has no custom domain of its own at
`jonaraphael.com/<repo-name>/`. So:

- The slug is the repo name, case-sensitive.
- Connecting a repo = Pages on + repo name equals the slug + no per-repo custom domain.
- Each push that redeploys the repo's Pages site updates the URL. No extra wiring.

## Procedure

Run from inside the repo:

```bash
connect-site <slug>      # slug optional; defaults to the repo name
```

The script (`~/git/jonaraphael.com/tools/connect-site/connect-site`, on PATH
via `~/.local/bin`) checks preconditions, renames the repo when the slug differs
from its name, turns Pages on, waits for the deploy, then fetches
`https://jonaraphael.com/<slug>/` and every same-origin file the page
references. Follow its exit code:

| Exit | Meaning | What to do |
|---|---|---|
| 0 | Live and verified | Report the URL. |
| 2 | Precondition failed | Relay the message; a different slug or a user decision is needed. |
| 3 | Repo edits needed, listed under `ACTION NEEDED` | Make the edits, commit, push, run `connect-site` again (no slug needed after a rename). Repeat until 0. |
| 4 | Deploy failed or URL never came up | Read the failing run with `gh run list` / `gh run view --log-failed`, fix, push, re-run. |

If the folder has no GitHub repo yet, create one named after the slug
(`gh repo create jonaraphael/<slug> --source . --push`, public unless the user
says otherwise), then run the script.

### Exit 3 cases

**No deployable site.** The repo needs a build. Copy `pages-workflow.yml`
(next to this file) to `.github/workflows/pages.yml`, set the branch, build command and output folder
for this project, and make the build emit the base path `/<slug>/`. Verify the
build locally before pushing.

**References to the old name after a rename, or references that do not
resolve.** The site is served from `/<slug>/`, not `/`. Set the base path where
the project defines it, then fix remaining hard-coded links:

- Vite: `base` in `vite.config.*` (or the env var the config reads)
- Create React App: `homepage` in `package.json`
- Next.js static export: `basePath` and `assetPrefix`
- Astro: `base` (and `site`); SvelteKit: `kit.paths.base`
- Jekyll: `baseurl` in `_config.yml`
- Plain HTML: root-absolute `href="/..."` / `src="/..."` become relative
- Also check: router basename, service-worker scope, `manifest.json`
  `start_url`, `404.html` redirects, sitemap, canonical and Open Graph URLs,
  README links

Prefer deriving the base path from the repo name in the workflow
(`${{ github.event.repository.name }}`) over hard-coding it, so a later rename
needs no source edits.

**CNAME file after `--drop-domain`.** Delete the listed file, commit, push,
re-run.

## Decisions that belong to the user

- **Repos with their own domain** (`fmrl.ink`, `snapandshop`): the script stops
  with exit 2. Pass `--drop-domain` only when the user has said that domain
  should stop serving the site.
- **Renames**: asking for a slug that differs from the repo name is the
  authorization to rename. Say in the report that the GitHub URL changed, old
  git URLs redirect, and the old Pages path no longer resolves.
- **Homepage card**: add or edit a project entry in
  `~/git/jonaraphael.com/index.html` (the local clone of
  `jonaraphael/jonaraphael.github.io`) only when the user asks.

## Limits

- Static sites only. A project that needs a server (for example an app on
  Vercel) cannot be mounted this way.
- GitHub Pages on a private repo requires a paid GitHub plan.
- A slug equal to a top-level file or folder in the homepage repo (`assets`,
  `tools`, `robots.txt`, ...) is rejected.

## Listing

```bash
connect-site --list      # every Pages repo, its URL, current HTTP status
```

## Problems with the domain itself

`~/git/jonaraphael.com/AGENTS.md` holds the hosting layout (registrar, DNS,
certificate, mail records) and a runbook for a missing certificate, HTTP not
redirecting to HTTPS, project paths that 404, and DNS changes. Read it before
touching the homepage repo, DNS, or any Pages domain setting.
