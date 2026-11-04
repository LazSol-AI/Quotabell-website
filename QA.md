# Website verification

Verified locally on 2026-11-03. No deployment, login, provider request, remote modification or push was performed.

## Results

- `python3 Website/scripts/check.py`: **PASS**, 6 pages and 121 local links/image references/fragments. Static folder: **865,270 bytes** (about 0.87 MB, including both screenshot themes and the downloadable 1024 icon).
- Minimum tested normal-text contrast: **5.21:1**. The darker teal button has white text; the original sampled ring teal is retained as the brand accent. Focus indicators are visible in both themes.
- `python3 Website/scripts/check.py --publish-ready`: **expected failure** for the deliberately unresolved publication TODOs on index, privacy, support, terms and press. See the complete replacement table in `README.md`.
- Design skill source lint: **0 failures, 0 warnings**.
- Final design skill browser inspection at **1440, 768 and 390 px**: **0 failures, 2 warnings**. All listed fold and full-page contact-sheet screenshots were opened and reviewed after the final changes.
- Additional temporary headless Chrome harness: **48 cases passed** (6 pages × 4 widths: 320, 390, 768, 1440 × light/dark). Both closed and fully expanded disclosure states were measured. No horizontal overflow, broken images or headings exceeding two lines. Dark screenshots followed the dark colour-scheme preference.
- Native phone-only disclosure: full Enter-key event opens the disclosure; focused summary has a visible solid outline. The accessibility tree exposes main, navigation, headings, lists, images, figures and disclosure roles. This is structural browser evidence, not a VoiceOver session.
- All observed page requests were local. No remote assets, fonts or scripts were requested. Opening `index.html` directly as a file loaded its stylesheet and images.
- `Website/_source-shots/` removed; no raw staging screenshots are included. `git diff --check` passed. No application code was changed.

The two inspector warnings are intentional/understood:

1. **No video:** the brief calls for a small, static, minimally scripted site and supplied still screenshots. No honest video was supplied; no stock footage or invented demo is appropriate. Motion is omitted, with a reduced-motion override retained for future changes. The inspector's `still-page` rule was explicitly allowed for this requirement.
2. **Off-centre content sample (160 px versus 176 px):** the inspector infers edges from occupied text/image regions. The shared `.wrap` is centered at an equal 160 px outer margin on a 1440 px viewport; individual text lengths and a centered screenshot leave different occupied-text extents. The actual site frame is symmetric. Mobile uses equal 20 px margins.

## Design review

Direction: **The quiet instrument**, seed **867747738**. One hero redraw was made because the initial photograph-filled midline hero required subject photography that did not exist. The brand palette and system typography were kept. The design was adapted to the user's explicit static, calm product brief; no stock atmospheric photography, animation, app mockup or additional third-party marks were introduced.

Idea: On this page, **Quotabell’s own remaining-quota display becomes the demonstration**, with real sample screenshots paired with the exact storage and sign-in choices behind the numbers.

Live element: native, keyboard-operable disclosures let the reader expand each data mode and FAQ without JavaScript. Both the main-page Mac mode and the first troubleshooting answer start open.

ROUND 1
Seen in one second: the quota dashboard beside the product promise.
Idea (one sentence): real remaining-quota numbers lead into the reader's choice of data source.
Live thing: native mode/FAQ disclosures.
Layout words by section: hero=split / features=definition-list / showcase=staggered-images / how=disclosures / wake=two-columns / download=field / faq=reading-list.
Scores: design 7.0 · usability 8.0 · creativity 6.5 · content 5.0 → overall 7.0.
Caps applied: static-motion design cap 7; content capped at 5 because requested publication placeholders remain. This is a publication limitation, not fabricated product evidence.
Top three problems (most visible first), each with the screenshot it shows in and the fix:
1. Desktop reading measure was too wide in long details/captions. Fix: cap paragraphs at 68ch.
2. Lock Screen crop included unused pale gallery space at the bottom. Fix: tighten crop to 830 px before resizing.
3. Button text on sampled teal fell just short of normal-text AA. Fix: darker teal button background; retain sampled brand accent.

ROUND 2
Seen in one second: a real dashboard and a concise explanation of what it shows.
Idea (one sentence): quota readings stay connected to the data mode and privacy explanation that make them possible.
Live thing: native disclosures with keyboard focus and Enter activation verified.
Layout words by section: hero=split / features=definition-list / showcase=staggered-images / how=disclosures / wake=two-columns / download=field / faq=reading-list.
Scores: design 7.0 · usability 8.0 · creativity 6.5 · content 5.0 → overall 7.0.
Caps applied: same requested static-motion and unresolved-placeholder caps.
Top three remaining limitations:
1. Download section visibly contains TODOs. Replace with verified links only after releases/tap exist.
2. Support/privacy contact is visibly inactive. Replace with a monitored real address before publishing.
3. Screenshots are simulator sample data and in-app widget previews. They show the actual interface but do not establish real-device widget, notification or background-sync acceptance.

## What was not tested

Wrangler was not installed or cached in this environment. No network install was made, so `wrangler dev` was not run. Workers configuration and header declarations were checked offline, but live Cloudflare routing, response security headers, custom-domain HTTPS and the branded nested-URL HTTP 404 must be checked with Wrangler or on the selected host later. The local Python file server does not emulate those hosting features.

No Safari/Firefox, physical iPhone, native VoiceOver session, App Store review, production iCloud, real provider sign-in or notarized Mac release was tested by this website task. Legal text and provider-policy disclosures still need the owner's pre-publication review, as documented in the README.

Temporary inspection artifacts are in ignored `Website/.taste-skill/final/` and `Website/.taste-skill/browser/` while this worktree exists. They are not published or committed, and the site has no dependency on them. The committed offline check script can be run without Node, Chrome, Wrangler or third-party packages.
