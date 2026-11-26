# Bundle verification

The rebuilt package was checked against the supplied `jona-portfolio-static-hosting.zip` and the downloaded original assets.

| Check | Result |
| --- | --- |
| Original remote image URLs recovered | 7 of 7 |
| Original downloads successful | 7 of 7, HTTP 200 |
| Original downloaded bytes preserved in bundle | 7 of 7, verified with SHA-256 |
| Additional sourced photographs | Osmobot, Lumeter hardware, and restored original headshot |
| Total raster assets | 10: five PNG, four JPEG, one AVIF |
| Full image decoding | All 10 passed, including AVIF |
| HTML and CSS image references | All 10 resolve to local `assets/` files |
| Remote image, stylesheet, font, or script dependencies | 0 |
| SVG files, inline SVG, or SVG data URIs | 0 |
| Osmo and Lumeter drawn placeholders | Removed and replaced with photographs |
| Image manifest | Sizes, formats, dimensions, and SHA-256 verified |
| Local HTTP entrypoint | HTTP 200 |
| ZIP integrity and extracted file equality | Passed |

The page uses relative asset paths, embedded CSS, and system fonts. No JavaScript or external stylesheet imports are present. External project, contact, press, and documentation links are intentional navigation links, not assets loaded to render the page.

These results cover static dependency analysis, full image decoding, file checksums, a local HTTP check, and archive extraction verification. They do not claim a browser layout or cross-browser visual test. The original copy and project order were retained; this rebuild did not refresh the portfolio's adoption metrics or press claims.
