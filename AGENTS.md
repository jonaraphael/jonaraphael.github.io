# Agent notes for jonaraphael.com

## What this repo is

- GitHub repo `jonaraphael/jonaraphael.github.io`, the account's GitHub Pages user site. The repo name is fixed by GitHub; the local folder is `~/git/jonaraphael.com`.
- It serves the homepage at `https://jonaraphael.com/` and, through the `CNAME` file, puts every other Pages repo in the account at `https://jonaraphael.com/<repo-name>/`.
- The repo is public and its root is the web root. Every tracked file is readable at `jonaraphael.com/<path>`. Private or machine-specific material goes in `.local/`, which is gitignored.

## Rules

- Leave `CNAME` alone. Removing or changing it detaches the domain from the homepage and from every project path.
- Reserve project repo names for their native Pages paths. Check the homepage root and the account's repo names before assigning a custom slug.
- Do not set a custom domain on a project repo unless the owner asks. A project with its own domain leaves `jonaraphael.com/<repo>/`.
- Do not commit secrets or API tokens. None are stored anywhere in this folder.
- `git pull --rebase` before pushing. GitHub writes commits to `main` itself when the custom domain is changed through the API or settings page.

## Homepage

- `index.html` is the whole page: embedded CSS, no JavaScript, no build step. Images are under `assets/` and referenced by relative path. `.nojekyll` disables Jekyll.
- A push to `main` deploys. Measured on 2026-11-25: 25 seconds from push to live.
- `assets-manifest.json`, `ASSET_SOURCES.md` and `VERIFICATION.md` describe the image set as of the original bundle. Adding or replacing an image makes them stale unless they are updated too.

## Project sites

- The native Pages path is the case-sensitive repo name. For a different slug, serve a directory in this homepage deployment. Never rename or duplicate an existing repo to get a slug. Use a redirect only when the owner asks for a short link.
- `/owl/` serves the Offline Wandering Library landing page and builder. Edit the originals in `offline-wandering-library`. The homepage's `Sync OWL pages` workflow checks the published HTML every 15 minutes and supports manual dispatch. Downloads and scripts come from the project's existing deployment.
- `/backby` serves `backby.html`, which redirects browsers to `https://backby.date/`.
- `/cerulean` serves `cerulean.html`, which redirects browsers to `https://cerulean.org/`.
- Run `tools/connect-site/connect-site <slug>` inside the project repo for the native path or custom-slug instructions. `connect-site --list` reports native Pages sites. This section records homepage-served aliases.
- `fmrl.ink` and `snapandshop` have their own domains and are not under `jonaraphael.com`. `connect-site --drop-domain` moves one over; that is the owner's decision.

## Hosting layout

- Registrar: Namecheap. Nameservers and DNS: Cloudflare, zone `jonaraphael.com`.
- DNS records that serve the site: `CNAME jonaraphael.com -> jonaraphael.github.io` and `CNAME www -> jonaraphael.github.io`, both DNS-only (grey cloud). Cloudflare flattens the apex CNAME into GitHub's A records.
- The two records stay DNS-only. GitHub issues and renews the certificate only while it sees its own IPs for the domain. The current certificate covers `jonaraphael.com` and `www.jonaraphael.com` and expires 2027-02-23; GitHub renews it automatically.
- Mail: the apex MX records and the SPF TXT record point at Namecheap email forwarding. DNS work on the site does not touch them.
- HTTPS is enforced on the homepage repo and on each project repo (a per-repo Pages setting).

## Runbook

**Check the domain's health.**

```bash
gh api repos/jonaraphael/jonaraphael.github.io/pages --jq '{cname, https_enforced, cert: .https_certificate}'
gh api repos/jonaraphael/jonaraphael.github.io/pages/health --jq '.domain | {is_pointed_to_github_pages_ip, is_cloudflare_ip, is_https_eligible, reason}'
```

**Certificate missing or stuck (`https_certificate` is null).** GitHub resolves the domain through its own cache, which held the old answer for about 9 minutes after the DNS change on 2026-11-25. Wait until the health call reports `is_pointed_to_github_pages_ip: true`, then remove and re-add the domain. Re-saving the same value did not trigger issuance; remove and re-add did, within 20 seconds.

```bash
printf '{"cname":null}' | gh api -X PUT repos/jonaraphael/jonaraphael.github.io/pages --input -
gh api -X PUT repos/jonaraphael/jonaraphael.github.io/pages -f cname=jonaraphael.com
# once .https_certificate.state is "approved":
gh api -X PUT repos/jonaraphael/jonaraphael.github.io/pages -F https_enforced=true
```

This makes GitHub commit "Delete CNAME" and "Create CNAME" to `main`. The domain is detached for the seconds between the two calls.

**Plain `http://` on a project path returns 200 instead of a redirect.** Any change to the user site's domain resets `https_enforced` to `false` on every project repo. Set it back per repo; it took about 3 minutes to take effect.

```bash
gh api -X PUT repos/jonaraphael/<repo>/pages -F https_enforced=true
```

`connect-site` does this for the repo it runs in.

**A project path 404s.** Check, in order: Pages is on for the repo; the repo has no custom domain of its own; the path uses the repo name's exact case; the last Pages deploy succeeded (`gh run list` in the repo); nothing at the top level of this repo has the same name.

**A project page loads but its assets 404.** The site was built for a different base path. It is served from `/<repo-name>/`. See the base-path list in `tools/connect-site/SKILL.md`.

**DNS or Cloudflare changes.** No Cloudflare credential is stored. Ask the owner for a scoped API token: "Edit zone DNS" on `jonaraphael.com` for record changes. Records that Cloudflare marks as managed by a Worker custom domain are read-only to that token (error 1043) and need "Workers Scripts: Edit" to detach. On 2026-11-25 the agent harness blocked use of the machine's saved `wrangler` login for this; ask for a token instead.

## History

- 2026-11-25: the domain moved from a Cloudflare Worker serving a static bundle to GitHub Pages. HTTPS on the domain failed for about 11 minutes during the switch while GitHub issued the certificate. The Worker was detached, not deleted. Identifiers, the pre-switch DNS backup and rollback steps are in `.local/INFRA.md`, which exists only on the machine that did the move.

## Open items (as of 2026-11-25)

- `linkedmd`: 5 of the 7 files its page references return 404. The page points at `../store-assets/screenshots/*.png`, which is outside that repo's published `docs/` folder.
- `connect-site` has run its checks, listing and verification against real repos. Enabling Pages on a repo without it, `--drop-domain`, and the no-deployable-site exit have not run against a real repo.
