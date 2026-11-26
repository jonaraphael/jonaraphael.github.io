---
name: connect-site
description: Publish a project's site at jonaraphael.com using its existing Pages path or a custom slug in the homepage deployment. Use for project hosting, slug requests and listing connected sites.
---

# Connect a repo's site to jonaraphael.com/<slug>/

## How it works

`jonaraphael/jonaraphael.github.io` is the GitHub Pages user site and carries the
custom domain `jonaraphael.com`. GitHub Pages serves every other Pages repo in
the account that has no custom domain of its own at
`jonaraphael.com/<repo-name>/`. The homepage can also serve its own directories.
Always preserve the existing project repository. Never rename or duplicate it
to obtain a slug.

## Custom slug

When the requested slug differs from the repository name, publish that path in
the existing homepage deployment. Check the homepage root and the owner's repo
names for collisions. Reuse a directory already assigned to the same project.

For example, `offline-wandering-library` publishes the library assets and the
homepage serves its landing page and builder under `/owl/`. See
`tools/sync-owl.py` and `.github/workflows/sync-owl.yml` in the homepage
repo. Adapt the entry pages, links, routing and asset URLs to the project.
Keep the pages updated from the project's deployment and verify direct entry,
navigation, and a representative asset or download at the live URL. A request
to serve the site at a slug means the address stays there. Use a redirect
when the owner specifically wants a short link.

## Default project path

Run from inside the repo:

```bash
connect-site <slug>      # slug optional; defaults to the repo name
```

The script (`~/git/jonaraphael.com/tools/connect-site/connect-site`, on PATH
via `~/.local/bin`) checks preconditions, turns Pages on, waits for the deploy, then fetches
`https://jonaraphael.com/<slug>/` and every same-origin file the page
references. Follow its exit code:

| Exit | Meaning | What to do |
|---|---|---|
| 0 | Live and verified | Report the URL. |
| 2 | Precondition failed | Relay the message; a different slug or a user decision is needed. |
| 3 | Follow-up edits | For a custom slug, follow the custom slug procedure above. For the default path, make the listed changes, push, and rerun the command. |
| 4 | Deploy failed or URL never came up | Read the failing run with `gh run list` / `gh run view --log-failed`, fix, push, re-run. |

### Exit 3 cases

**No deployable site.** The repo needs a build. Copy `pages-workflow.yml`
(next to this file) to `.github/workflows/pages.yml`, set the branch, build command and output folder
for this project, and make the build emit the base path `/<slug>/`. Verify the
build locally before pushing.

**References that do not resolve.** The default project site is served from `/<repo-name>/`. Set the base path where
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
(`${{ github.event.repository.name }}`).

**CNAME file after `--drop-domain`.** Delete the listed file, commit, push,
re-run.

## Decisions that belong to the user

- **Repos with their own domain** (`fmrl.ink`, `snapandshop`): the script stops
  with exit 2. Pass `--drop-domain` only when the user has said that domain
  should stop serving the site.
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

Homepage-served aliases are recorded under Project sites in the homepage's `AGENTS.md`.

## Problems with the domain itself

`~/git/jonaraphael.com/AGENTS.md` holds the hosting layout (registrar, DNS,
certificate, mail records) and a runbook for a missing certificate, HTTP not
redirecting to HTTPS, project paths that 404, and DNS changes. Read it before
touching the homepage repo, DNS, or any Pages domain setting.
