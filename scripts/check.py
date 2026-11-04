#!/usr/bin/env python3
"""Offline validation of the committed static folder. No third-party dependencies."""
import argparse
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

WEBSITE = Path(__file__).resolve().parents[1]
PUBLIC = WEBSITE / 'public'
PAGES = {'index.html', 'privacy.html', 'support.html', 'terms.html', 'press.html', '404.html'}
COPYRIGHT = '© 2026 LAZSOL AI PTE. LTD.'
DISCLAIMER = ('Quotabell is not affiliated with, endorsed by or sponsored by Anthropic, OpenAI, xAI or Google. '
              'Claude, ChatGPT, Codex, Grok, SuperGrok, Google, Gemini and Antigravity are trademarks of their respective owners.')

class Document(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.ids, self.refs, self.errors = path, [], [], []
        self.h1s, self.main, self.lang, self.viewport = 0, 0, False, False
        self.comments = []

    def handle_comment(self, data):
        self.comments.append(data)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if attrs.get('id'):
            self.ids.append(attrs['id'])
        self.h1s += tag == 'h1'
        self.main += tag == 'main'
        self.lang |= tag == 'html' and attrs.get('lang') == 'en'
        self.viewport |= tag == 'meta' and attrs.get('name') == 'viewport'
        if tag in {'script', 'iframe', 'object', 'embed', 'form', 'style'}:
            self.errors.append(f'unexpected {tag}')
        if 'style' in attrs or any(k.startswith('on') for k in attrs):
            self.errors.append('inline style or event handler')
        if tag == 'img' and not all(k in attrs for k in ('alt', 'width', 'height')):
            self.errors.append('image needs alt, width and height')
        for key in ('href', 'src'):
            if key in attrs:
                self.refs.append((tag, attrs[key]))
        if 'srcset' in attrs:
            for item in attrs['srcset'].split(','):
                self.refs.append((tag, item.strip().split()[0]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--publish-ready', action='store_true', help='also fail on unresolved publication placeholders')
    args = parser.parse_args()
    errors, docs, placeholders = [], {}, []
    actual = {p.name for p in PUBLIC.glob('*.html')}
    if actual != PAGES:
        errors.append(f'page inventory differs: {actual ^ PAGES}')
    for path in sorted(PUBLIC.glob('*.html')):
        content = path.read_text()
        doc = Document(path)
        doc.feed(content)
        docs[path.resolve()] = doc
        errors += [f'{path.name}: {e}' for e in doc.errors]
        if doc.h1s != 1 or doc.main != 1 or not doc.lang or not doc.viewport:
            errors.append(f'{path.name}: missing semantic structure')
        if COPYRIGHT not in content or DISCLAIMER not in content:
            errors.append(f'{path.name}: missing required footer text')
        if any(count != 1 for count in Counter(doc.ids).values()):
            errors.append(f'{path.name}: duplicate id')
        if 'TODO' in content:
            placeholders.append(path.name)
            if not any('TODO' in c for c in doc.comments):
                errors.append(f'{path.name}: placeholder lacks an HTML TODO comment')
    refs, external_links = 0, 0
    for path, doc in docs.items():
        for tag, ref in doc.refs:
            refs += 1
            url = urlsplit(ref)
            if url.scheme or url.netloc:
                if tag == 'a' and url.scheme in {'https', 'mailto'}:
                    external_links += 1  # Destinations are not fetched; external assets remain forbidden.
                else:
                    errors.append(f'{path.name}: unexpected external asset or unsafe link: {ref}')
                continue
            target = (PUBLIC / unquote(url.path).lstrip('/') if url.path.startswith('/') else path.parent / unquote(url.path)) if url.path else path
            target = target.resolve()
            if not target.is_relative_to(PUBLIC.resolve()) or not target.is_file():
                errors.append(f'{path.name}: missing/escaping target {ref}')
            elif url.fragment and (target not in docs or unquote(url.fragment) not in docs[target].ids):
                errors.append(f'{path.name}: missing fragment {ref}')
    css = (PUBLIC / 'assets/site.css').read_text()
    if re.search(r'@import|https?://|url\(', css):
        errors.append('CSS contains an external import or unvalidated URL')
    # All text/background combinations, including AA normal-text buttons in both themes.
    def luminance(color):
        values = [int(color[i:i+2], 16) / 255 for i in (0, 2, 4)]
        values = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in values]
        return sum(a*b for a,b in zip(values, (.2126, .7152, .0722)))
    min_contrast = 100
    # Light theme, then dark theme, then the fixed dark privacy band and Lock Screen tile.
    for text, background in [('0f2238','f6f8fb'),('3d5064','f6f8fb'),('5a6b7c','f6f8fb'),('5a6b7c','ffffff'),
                             ('5a6b7c','f1f5f8'),('1f666d','f6f8fb'),('1f666d','e8f0f2'),('ffffff','0f2238'),
                             ('eef3f7','0a0f14'),('c3cfd9','121a22'),('9aabba','121a22'),('9aabba','17212b'),
                             ('7fcbd1','0a0f14'),('7fcbd1','17262d'),('0a0f14','eef3f7'),
                             ('eef6f7','14323b'),('c9dde2','14323b'),('9ad6db','14323b'),('a9b8c6','18242f')]:
        low, high = sorted((luminance(text), luminance(background)))
        contrast = (high+.05)/(low+.05)
        min_contrast = min(min_contrast, contrast)
        if contrast < 4.5:
            errors.append(f'AA contrast failure: {text} on {background}: {contrast:.2f}')
    config = json.loads((WEBSITE / 'wrangler.jsonc').read_text())
    if config.get('name') != 'quotabell-website' or config.get('compatibility_date') != '2026-11-01':
        errors.append('unexpected Workers name/date')
    assets = config.get('assets', {})
    if (WEBSITE / assets.get('directory','')).resolve() != PUBLIC.resolve() or assets.get('not_found_handling') != '404-page' or assets.get('html_handling') != 'none':
        errors.append('Workers assets configuration differs from expected')
    headers = (PUBLIC / '_headers').read_text()
    for expected in ('Content-Security-Policy:', "default-src 'self'", "script-src 'none'", "frame-ancestors 'none'", 'X-Content-Type-Options: nosniff', 'Referrer-Policy: no-referrer', 'Permissions-Policy:'):
        if expected not in headers:
            errors.append(f'missing security header: {expected}')
    if (WEBSITE / '_source-shots').exists():
        errors.append('remove Website/_source-shots before committing')
    if args.publish_ready and placeholders:
        errors.append('publication placeholders remain in: ' + ', '.join(placeholders))
    size = sum(p.stat().st_size for p in PUBLIC.rglob('*') if p.is_file())
    if size > 2_000_000:
        errors.append(f'site exceeds 2 MB budget: {size} bytes')
    print(f'{len(docs)} pages; {refs} local links/assets/fragments; {size:,} static bytes; minimum tested text contrast {min_contrast:.2f}:1')
    print(f'External destinations skipped without network access: {external_links}')
    print('Publication TODOs: ' + ', '.join(placeholders))
    if errors:
        print('\n'.join('FAIL: ' + e for e in errors))
        return 1
    print('PASS: offline structural, path, fragment, asset, contrast and config checks')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
