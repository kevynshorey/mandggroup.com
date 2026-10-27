# mandggroup.com

Website for **M&G Group**: <https://www.mandggroup.com>

A static, dependency-free site: hand-written HTML and CSS with self-hosted fonts and one line of
JavaScript (the footer year). It is published by GitHub Pages from the `main` branch.

## Structure

| Path | Purpose |
| --- | --- |
| `index.html` | The whole site: hero, About, Portfolio, Contact |
| `404.html` | Branded "page not found" page |
| `assets/css/site.css` | All styles. Design tokens (colours, type, spacing) are CSS variables at the top |
| `assets/fonts/` | Cormorant Garamond and Hanken Grotesk (latin subsets, WOFF2) with their licences |
| `assets/img/` | Favicon, Apple touch icon, logo and social-share image |
| `favicon.ico`, `robots.txt`, `sitemap.xml` | Standard root files |
| `tools/` | Generators for the monogram icons and the social image (not used at runtime) |

## Editing content

- All copy lives in `index.html`.
- Each portfolio business is one `<li class="ledger-row">` in the Portfolio section. To add or remove
  one, copy or delete a row and renumber the `ledger-num` values. Then update the business count
  ("six") in the meta description, the hero paragraph and the About facts list.
- Keep `sitemap.xml`'s `lastmod` current when content changes.

## Preview locally

```sh
python3 -m http.server 8000
# open http://localhost:8000
```

## Deploying

Push to `main`. GitHub Pages republishes within a minute or two.

## Domain and DNS

- **Registrar:** LCN. Registration runs to 31 Aug 2027; keep auto-renew on.
- **DNS host:** Microsoft 365 (nameservers `ns1`–`ns4.bdm.microsoftonline.com`). Edit records in
  Microsoft 365 admin centre → Settings → Domains → `mandggroup.com` → DNS records.
  **Leave the MX, SPF (TXT), `MS=` verification and `autodiscover` records alone: they run M&G email.**
- **Website records** (GitHub Pages):

  | Type | Name | Value |
  | --- | --- | --- |
  | A | `@` | `185.199.108.153` |
  | A | `@` | `185.199.109.153` |
  | A | `@` | `185.199.110.153` |
  | A | `@` | `185.199.111.153` |
  | CNAME | `www` | `kevynshorey.github.io` |

- **Canonical address:** `https://www.mandggroup.com/`. GitHub Pages redirects `mandggroup.com` to it,
  and HTTPS is enforced.

## Regenerating assets

- Icons and logo: `python3 tools/build_assets.py`. Needs `fonttools` and `brotli` (pip),
  `rsvg-convert` and ImageMagick.
- Social image: serve the repo locally and screenshot `tools/og.html` at exactly 1200×630 to
  `assets/img/og-image.png`.

## Licences

- Fonts: Cormorant Garamond and Hanken Grotesk, SIL Open Font License 1.1 (`assets/fonts/OFL-*.txt`).
- Arrow icons: paths from [Lucide](https://lucide.dev), ISC licence.
- Site content © M&G Group.
