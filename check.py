"""Check publishable files, local links, labels and all website translations."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
from collections import Counter
import json
import re

ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'dist'
keys, errors, pages = set(), [], {}

class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.references = [], [], []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for name in ('data-en', 'data-i18n-aria', 'data-i18n-alt'):
            if name in attrs:
                keys.add(attrs[name])
        for name in ('aria-controls', 'aria-labelledby'):
            self.references.extend(attrs.get(name, '').split())
        if tag in ('a', 'link', 'script', 'img'):
            ref = attrs.get('href') or attrs.get('src')
            if ref:
                self.links.append(ref)
        if tag == 'img' and 'alt' not in attrs:
            errors.append('An image is missing its alt attribute')

for path in DIST.rglob('*.html'):
    scan = Scan()
    scan.feed(path.read_text())
    pages[path] = scan
    errors.extend(f'{path.name}: duplicate id {key}' for key, count in Counter(scan.ids).items() if count > 1)
    errors.extend(f'{path.name}: missing ARIA target {key}' for key in scan.references if key not in scan.ids)

for path, scan in pages.items():
    for reference in scan.links:
        url = urlsplit(reference)
        if url.scheme or url.netloc:
            continue
        target = DIST / url.path.lstrip('/') if url.path.startswith('/') else path.parent / url.path if url.path else path
        if target.is_dir():
            target /= 'index.html'
        if not target.exists():
            errors.append(f'{path.name}: missing {reference}')
        elif url.fragment and target in pages and url.fragment not in pages[target].ids:
            errors.append(f'{path.name}: missing anchor {reference}')

source = (DIST / 'locales.js').read_text().removeprefix('window.KOTOBAIA_TRANSLATIONS = ').strip().removesuffix(';')
dictionaries = json.loads(source)
assert set(dictionaries) == {'en','ja','ko','zh-Hans','zh-Hant','es','fr','de','pt-BR','it','ru','ar'}
for locale, dictionary in dictionaries.items():
    for key in sorted(keys):
        if not dictionary.get(key):
            errors.append(f'{locale}: missing translation for {key}')

for path in DIST.rglob('*'):
    if path.is_symlink():
        errors.append(f'Publishable directory contains a symlink: {path.name}')
    if path.is_file() and path.suffix not in {'.html','.css','.js','.png','.jpg','.xml','.txt',''}:
        errors.append(f'Unexpected public file type: {path.name}')
    if path.is_file() and path.suffix in {'.html','.css','.js'}:
        text = path.read_text()
        if re.search(r'(?:ghp_|github_pat_)[A-Za-z0-9_]{20,}|-----BEGIN .*PRIVATE KEY|sourceMappingURL|/Users/|eyJ[A-Za-z0-9_-]{40,}\.', text):
            errors.append(f'Potential private data or source map in {path.name}')

if errors:
    raise SystemExit('\n'.join(errors))
print(f'Validated {len(pages)} pages, {len(keys)} translated labels × {len(dictionaries)} languages, local links and public-file boundaries.')
