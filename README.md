# jonaraphael.com

Source for the homepage at [jonaraphael.com](https://jonaraphael.com). GitHub Pages serves this repo from the root of `main`; a push to `main` redeploys the site.

The page is static: `index.html` with embedded CSS, images under `assets/`, no JavaScript and no build step. `.nojekyll` turns off Jekyll processing.

## Project sites under this domain

This repo is the account's user site and carries the custom domain (`CNAME`). GitHub Pages therefore serves every other Pages-enabled repo in the account that has no custom domain of its own at `jonaraphael.com/<repo-name>/`, and redirects `jonaraphael.github.io/<repo-name>/` there. A push to a project repo redeploys that project's path.

The path segment is the repo name, case-sensitive. A top-level file or folder in this repo with the same name as a project repo would collide with that project's path.

## Files

- `index.html` — the homepage
- `assets/` — images
- `CNAME` — custom domain for GitHub Pages
- `robots.txt` — allows crawling
- `ASSET_SOURCES.md`, `assets-manifest.json`, `VERIFICATION.md` — image provenance, checksums, and the original bundle's verification notes
