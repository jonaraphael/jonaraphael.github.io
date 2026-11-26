# jonaraphael.com

Source for the homepage at [jonaraphael.com](https://jonaraphael.com). GitHub Pages serves this repo from the root of `main`; a push to `main` redeploys the site.

The page is static: `index.html` with embedded CSS, images under `assets/`, no JavaScript and no build step. `.nojekyll` turns off Jekyll processing.

## Project sites under this domain

This repo is the account's user site and carries the custom domain (`CNAME`). GitHub Pages therefore serves every other Pages-enabled repo in the account that has no custom domain of its own at `jonaraphael.com/<repo-name>/`, and redirects `jonaraphael.github.io/<repo-name>/` there. A push to a project repo redeploys that project's path.

The path segment is the repo name, case-sensitive. A top-level file or folder in this repo with the same name as a project repo would collide with that project's path.

## Connecting a project: `connect-site`

`tools/connect-site/` holds the command and agent skill that put a repo's site at `jonaraphael.com/<slug>/`. From inside a project repo:

```bash
connect-site <slug>      # slug optional; defaults to the repo name
connect-site --list      # every Pages repo, its URL, current HTTP status
```

It turns Pages on if needed, renames the repo when the slug differs from its name, waits for the deploy, and checks that the page and the files it references resolve. `SKILL.md` tells an agent how to handle the cases the script hands back (adding a build workflow, fixing base paths).

Install on a machine (the GitHub repo is `jonaraphael.github.io`; the local folder name is free):

```bash
git clone https://github.com/jonaraphael/jonaraphael.github.io ~/git/jonaraphael.com
ln -s ~/git/jonaraphael.com/tools/connect-site/connect-site ~/.local/bin/connect-site
ln -s ~/git/jonaraphael.com/tools/connect-site ~/.claude/skills/connect-site
ln -s ~/git/jonaraphael.com/tools/connect-site ~/.codex/skills/connect-site
```

Requires `gh` (authenticated), `git`, and `curl`.

## Files

- `index.html` — the homepage
- `assets/` — images
- `CNAME` — custom domain for GitHub Pages
- `tools/connect-site/` — the `connect-site` command, its agent skill, and a Pages workflow template
- `.local/` — untracked; DNS backups taken before the move to GitHub Pages
- `robots.txt` — allows crawling
- `ASSET_SOURCES.md`, `assets-manifest.json`, `VERIFICATION.md` — image provenance, checksums, and the original bundle's verification notes
