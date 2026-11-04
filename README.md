# Quotabell website

Plain HTML and CSS for marketing, App Store privacy/support URLs and press materials. No build step, JavaScript, cookies, tracking, analytics, remote fonts, CDN assets or runtime dependencies. All public files are in `public/`; this folder works on any static host.

## Structure

- `public/index.html` — marketing, features, sample screenshots, two data modes, Wake, download placeholders, FAQ.
- `public/privacy.html` — Privacy Policy, effective 2026-11-03.
- `public/support.html` — contact placeholder, FAQ and troubleshooting.
- `public/terms.html` — Terms of Use, effective 2026-11-03.
- `public/press.html` — short/long copy, icon and screenshot downloads, logo usage and company facts.
- `public/404.html` — missing-page response, with root-relative navigation so nested missing URLs work.
- `public/assets/` — shared CSS, current teal app icon and optimized screenshots.
- `public/_headers` — CSP and other security headers for Workers assets and compatible hosts.
- `wrangler.jsonc` — Workers static-assets configuration, no Worker script or build output needed.
- `scripts/check.py` — dependency-free, offline link/fragment/asset and content/config checks.
- `ACCURACY.md` — source map, screenshot provenance, limitations and review notes.
- `QA.md` — verification results and design review.

HTML is the source of truth. Edit the committed files directly. Shared navigation/footer markup is repeated intentionally; keep it consistent across all six pages. Normal pages use relative links and open directly as files. The 404 uses root-relative links for host fallback routing. Explicit `.html` URLs are preserved by Workers `html_handling: "none"`.

## Preview

From the repository root:

```sh
python3 -m http.server -d public 8000
```

Open `http://localhost:8000/`. Python serves files only; it does not apply `_headers` or the custom 404 fallback. Direct file opening also works for ordinary pages.

For the actual Workers asset router and headers, with Wrangler available:

```sh
npx wrangler dev
```

`npx` may download Wrangler if it is not installed/cached. No package installation, login or deployment was performed in this implementation. No global install is required. The configured compatibility date is `2026-11-01` and Worker name is `quotabell-website`.

## Checks

From the repository root:

```sh
python3 scripts/check.py
python3 scripts/check.py --publish-ready
```

The first command validates all internal links, fragment IDs, image paths (including dark-mode `srcset`), structure, no external resources, selected AA text contrast pairs, the Workers config and security header declarations. It does not make network requests. The second command also rejects unresolved publication TODOs and is **expected to fail until Eric fills them**. The script is not a legal review or a substitute for browser/assistive-technology testing.

## Every publication placeholder

All placeholders are deliberate. No fake download links, email links or invented App Store listing are active.

| Marker | Current value/location | Eric must supply |
| --- | --- | --- |
| `SITE_ORIGIN` | “domain coming soon” pill in `public/press.html` (HTML `TODO SITE_ORIGIN` comment) and URL templates below | The chosen public HTTPS origin. This is not an existing domain. Search for all `TODO-domain` occurrences when replacing it. |
| `CONTACT_EMAIL` | “support address coming soon” pill in privacy, support, terms and press; an adjacent HTML `TODO CONTACT_EMAIL` comment identifies it | A working, monitored support/privacy email address. Replace the pill and optionally add real `mailto:` links. A working contact is required before App Store review. |
| `APP_STORE_URL` | “Coming soon” pill in `public/index.html#download`, with an HTML TODO comment | The approved iPhone App Store listing URL; replace the placeholder paragraph with a real link. |
| `MAC_DOWNLOAD_URL` | “coming soon” pill in `public/index.html#download`, with an HTML TODO comment | The hosted, released Developer ID signed and notarized ZIP URL. Add a real download link only when the artifact exists. Signing/notarization are the distribution plan, not a claim that a downloadable release already exists. |
| `HOMEBREW_TAP` | HTML TODO comment in `public/index.html#download` (shown as “Homebrew coming soon”) | The published tap owner/name and verified install command. Replace the template-only wording when it is usable. |

Related release configuration in the separate Quotabell app repository: `Packaging/homebrew/quotabell.rb` contained release placeholders and a template version `0.1.0` when reviewed. Check its current state and set the actual release version, notarized ZIP URL, SHA-256 and homepage consistently with the website. The asset folder contains no release ZIP.

Before publishing, review the legal copy: **not legal advice; review before publishing**. Confirm hosting log settings and the website-host description in the Privacy Policy match the chosen host. Check the release gates in `Docs/HANDOFF.md` in the separate app repository. Review provider-policy disclosures and trademark permissions before release.

## App Store Connect URLs

After choosing the origin and publishing this folder, use these exact paths (replace the placeholder origin):

| App Store Connect field | URL template |
| --- | --- |
| Privacy Policy URL | `https://TODO-domain/privacy.html` |
| Support URL | `https://TODO-domain/support.html` |
| Marketing URL | `https://TODO-domain/` |

Additional pages: `/terms.html`, `/press.html`. No canonical or social-origin URLs are embedded before the domain is chosen. Do not enter placeholder URLs into App Store Connect. Confirm the final URLs load publicly, the support channel works, and the privacy and support contents are accurate before submitting.

## Deploy later

Eric will deploy to Cloudflare Workers from this MacBook when ready:

1. **Prerequisites:** Node.js LTS (if missing, install it, for example with `brew install node`) and a Cloudflare account. `npx` may download Wrangler if it is not installed/cached; no global install is required.

2. Open a terminal at this repository's root, which contains `wrangler.jsonc`.

3. Log in to Cloudflare:

   ```sh
   npx wrangler login
   ```

   This opens the Mac browser to authorise Wrangler with Cloudflare. Eric completes this himself. Verify the authenticated account:

   ```sh
   npx wrangler whoami
   ```

4. Optionally preview locally with the Workers asset router and headers:

   ```sh
   npx wrangler dev
   ```

   Open `http://localhost:8787`. Stop the preview with Ctrl-C before continuing.

5. Fill all TODO placeholders listed above and review the publication requirements. Run the strict check **before deploying**, from the repository root:

   ```sh
   python3 scripts/check.py --publish-ready
   ```

   Resolve any failures before continuing.

6. Deploy to Cloudflare Workers:

   ```sh
   npx wrangler deploy
   ```

   Note the printed `*.workers.dev` URL. Workers serves `./public`, applies `_headers` and returns the top-level `404.html` with `not_found_handling: "404-page"`. No Worker script, secrets, bindings or server APIs are needed.

7. Optionally add a custom domain: Cloudflare dashboard → **Workers & Pages → quotabell-website → Settings → Domains & Routes → Add custom domain**. Alternatively, add a `routes` entry with `custom_domain: true` in `wrangler.jsonc` and redeploy. Replace all `TODO-domain` occurrences with the chosen public domain (use the `workers.dev` hostname if skipping a custom domain). If the chosen origin changes, update the previously filled origin values too. Rerun the strict check and deploy any updated files. Verify HTTPS, the home/privacy/support URLs, a deliberately missing nested URL (HTTP 404 with the branded page), image/CSS content types and security headers.

8. In App Store Connect, paste the live **Privacy Policy URL**, **Support URL** and **Marketing URL** using the paths in the table above and the deployed origin. Confirm they load publicly and the support channel works. Do not paste TODO placeholders.

9. Optionally log out when finished:

   ```sh
   npx wrangler logout
   ```
