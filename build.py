"""Build the standalone Kotobaia public website from checked-in assets and copy."""
from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'dist'
DIST.mkdir(exist_ok=True)

def t(text, tag='span', cls=''):
    return f'<{tag} class="{cls}" data-en="{escape(text, quote=True)}">{escape(text)}</{tag}>'

arrow = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 19 19 5M5 5h14v14" stroke="currentColor" stroke-width="1.5"/></svg>'
globe = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/></svg>'
languages = [('en','English','English'),('ja','日本語','Japanese'),('ko','한국어','Korean'),('zh-Hans','简体中文','Simplified Chinese'),('zh-Hant','繁體中文','Traditional Chinese'),('es','Español','Spanish'),('fr','Français','French'),('de','Deutsch','German'),('pt-BR','Português','Portuguese'),('it','Italiano','Italian'),('ru','Русский','Russian'),('ar','العربية','Arabic')]

header = f'''<a class="skip" href="#main">{t('Skip to content')}</a>
<header class="site-header"><div class="nav wrap"><a class="brand" href="/" aria-label="Kotobaia"><img src="/assets/kotobaia-icon-small.png" width="42" height="42" alt="">Kotobaia</a>
<nav id="site-nav" aria-label="Kotobaia"><a href="/#experience">{t('Discover the app')}</a><a href="/support/">{t('Support')}</a><a href="https://sunimori.com/">Sunimori {arrow}</a></nav>
<div class="nav-actions"><button class="language-open" aria-haspopup="dialog" aria-controls="language-dialog" aria-label="Choose a display language" data-i18n-aria="Choose a display language">{globe}<span class="language-current">EN</span></button><a class="nav-contact" href="mailto:dev@sunimori.com">{t('Get in touch')} {arrow}</a><button class="menu-toggle" aria-controls="site-nav" aria-expanded="false" aria-label="Open navigation" data-i18n-aria="Open navigation"><span></span><span></span></button></div></div></header>
<dialog id="language-dialog" aria-labelledby="language-title"><div class="dialog-top"><h2 id="language-title">{t('Choose a display language')}</h2><button class="dialog-close" aria-label="Close" data-i18n-aria="Close">×</button></div><div class="language-grid">{''.join(f'<button data-language="{code}" aria-pressed="false"><span lang="{code}" dir="auto">{name}</span><small>{eng}</small><span class="language-check" aria-hidden="true">✓</span></button>' for code,name,eng in languages)}</div></dialog>'''

footer = f'''<footer class="site-footer"><div class="wrap"><div class="footer-top"><div><a class="brand" href="/"><img src="/assets/kotobaia-icon-small.png" alt="" width="38" height="38">Kotobaia</a>{t('A Sunimori app.','p')}</div><div class="footer-links"><a href="/support/">{t('Support')}</a><a href="/privacy/">{t('Privacy policy')}</a><a href="/terms/">{t('Terms of use')}</a><button class="language-open" aria-haspopup="dialog" aria-controls="language-dialog">{globe}{t('Language')}</button></div></div><div class="footer-bottom"><span>© 2026 Sunimori</span><a href="/website-privacy/">{t('Website privacy')}</a><a href="mailto:dev@sunimori.com">dev@sunimori.com {arrow}</a></div></div></footer>'''

def page(route, title, description, content, body_class=''):
    canonical = 'https://kotobaia.com' + route
    filename = DIST / (route.lstrip('/') + 'index.html')
    if route == '/404.html': filename = DIST / '404.html'
    filename.parent.mkdir(parents=True, exist_ok=True)
    filename.write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)}</title><meta name="description" content="{escape(description,quote=True)}"><meta name="theme-color" content="#f6f8fc"><link rel="canonical" href="{canonical}"><meta property="og:type" content="website"><meta property="og:site_name" content="Kotobaia"><meta property="og:title" content="{escape(title,quote=True)}"><meta property="og:description" content="{escape(description,quote=True)}"><meta property="og:url" content="{canonical}"><link rel="icon" href="/assets/kotobaia-icon-small.png" type="image/png"><link rel="stylesheet" href="/style.css?v=1"><script defer src="/locales.js?v=1"></script><script defer src="/app.js?v=1"></script></head><body class="{body_class}">{header}<main id="main">{content}</main>{footer}</body></html>''')

panels = [
    ('words','Your words','Start with something useful.','Build a collection of words you want to use. Hear them, follow the pronunciation, and find meaning in the example.','app-words.png','The Kotobaia vocabulary screen, showing pronunciation, meaning and an example sentence.','ありがとう','arigatō'),
    ('today','Daily rhythm','Make room for a little, every day.','Return to what you have learned with daily practice and reviews that fit your routine.','app-today.png','The Kotobaia daily learning screen.','少しずつ','sukoshi zutsu'),
    ('library','Your library','Follow your curiosity.','Explore word lists, Japanese levels and the language you want to learn next.','app-library.png','The Kotobaia word library.','好奇心','kōkishin'),
]
tabs = ''.join(f'<button id="tab-{key}" role="tab" aria-controls="panel-{key}" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}" data-experience="{key}"><span class="tab-number">0{i+1}</span>{t(label)}</button>' for i,(key,label,*_) in enumerate(panels))
panel_html = ''.join(f'''<section role="tabpanel" id="panel-{key}" aria-labelledby="tab-{key}" tabindex="0" {'hidden' if i else ''}><div class="experience-copy"><p class="eyebrow">KOTOBAIA / 0{i+1}</p>{t(title,'h3')}{t(body,'p')}<div class="specimen" aria-hidden="true"><span lang="ja">{word}</span><span>{reading}</span></div><div class="device-list"><span>iPhone</span><span>iPad</span><span>Mac</span></div></div><figure class="app-shot"><div class="shot-surface"><img src="/assets/{asset}" width="1206" height="2622" loading="lazy" alt="{alt}" data-i18n-alt="{alt}"></div><figcaption>{t('App preview · Development version')}</figcaption></figure></section>''' for i,(key,label,title,body,asset,alt,word,reading) in enumerate(panels))

home = f'''<section class="hero wrap"><div class="hero-copy"><p class="eyebrow">{t('A language, closer to you.')}</p><h1>{t('A little language.')}<em>{t('A larger world.')}</em></h1>{t('A word you hear. A sentence you understand. A conversation you make your own. Let Japanese become part of your everyday.','p','intro')}<a class="button" href="#experience">{t('Explore the experience')}<span aria-hidden="true">↓</span></a><p class="release">{t('Coming to iPhone, iPad & Mac')}</p></div><figure class="hero-art"><div class="hero-photo"><img src="/assets/komorebi-hero.jpg" width="1536" height="1024" fetchpriority="high" alt="Sunlight falls through maple leaves into a quiet courtyard." data-i18n-alt="Sunlight falls through maple leaves into a quiet courtyard."><div class="hero-device" aria-hidden="true"><img src="/assets/app-words.png" width="1206" height="2622" alt=""></div><span class="photo-label">{t('A moment in Japanese')}</span></div><figcaption class="word-caption"><div><span class="word" lang="ja">木漏れ日</span><span class="reading">komorebi</span></div>{t('Sunlight filtering through the leaves.','p')}</figcaption></figure></section>
<div class="brand-strip wrap"><span class="launch-label">{t('Preparing for launch')}</span><span class="strip-line" aria-hidden="true"></span><span>日本語 · 中文 · English · 한국어</span></div>
<section id="experience" class="experience-section wrap"><div class="section-heading"><div><p class="eyebrow">01 / {t('Discover the app')}</p><h2>{t('From a word to a world.')}</h2></div>{t('Your listening, vocabulary and practice, together.','p')}</div><div class="experience-tabs" role="tablist" aria-label="Kotobaia">{tabs}</div><div class="experience-panels">{panel_html}</div></section>
<section class="learning-section"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">02 / KOTOBAIA</p><h2>{t('Made for the way you learn.')}</h2></div>{t('Listen. Understand. Make it yours.','p')}</div><div class="learning-grid">
<article><span class="feature-glyph" aria-hidden="true">聴</span><p class="index">01</p>{t('Listen with context.','h3')}{t('Explore listening and reading material, follow spoken language, and revisit the parts you want to understand better.','p')}</article>
<article><span class="feature-glyph" aria-hidden="true">語</span><p class="index">02</p>{t('Keep useful words close.','h3')}{t('Collect vocabulary, study word lists, review what you have learned and check your understanding with quizzes.','p')}</article>
<article><span class="feature-glyph" aria-hidden="true">話</span><p class="index">03</p>{t('Find your voice.','h3')}{t('Use optional AI explanations, conversation and pronunciation practice when you want extra help. Cloud features and membership allowances are explained in the app.','p')}</article></div></div></section>
<section class="ai-section wrap"><div class="ai-panel"><div><p class="eyebrow">03 / {t('Put language into practice')}</p><h2>{t('With a little help from AI.')}</h2>{t('Bring listening, vocabulary, review and optional AI practice together. Build your own language routine, one useful moment at a time.','p')}<p class="ai-note">{t('Optional AI and speech features. Availability and allowances are shown in the app.')}</p></div><div class="companion"><img src="/assets/neko-wave.png" width="500" height="500" loading="lazy" alt="こにゃん"><p lang="ja">こにゃん</p>{t('Meet your everyday companion.','span')}</div></div></section>
<section class="account-section wrap"><div><p class="eyebrow">04 / {t('Clear choices.')}</p><h2>{t('Your account.')}<br><em>{t('Clear choices.')}</em></h2></div><div>{t('Sign in to sync your learning and keep purchases linked to your Kotobaia account. Google sign-in is used to identify your account using basic profile information; Kotobaia does not receive your Google password.','p')}{t('The privacy policy explains account data, optional cloud processing, storage and account deletion.','p')}<a class="text-link" href="/privacy/">{t('Read the privacy policy')} {arrow}</a></div></section>
<section class="closing-section"><div class="wrap"><p class="eyebrow">{t('Small steps. New possibilities.')}</p><h2>{t('A little language can take you somewhere new.')}</h2><div class="closing-actions"><a class="button white" href="/support/">{t('Visit support')} {arrow}</a><a class="text-link" href="mailto:dev@sunimori.com">{t('Get in touch')} {arrow}</a></div><p class="closing-note">{t('Preparing for launch')} · iPhone · iPad · Mac</p></div></section>'''
page('/', 'Kotobaia — A little language. A larger world.', 'A language, closer to you. Discover Japanese listening, vocabulary, daily review and optional AI practice with Kotobaia, a Sunimori app for iPhone, iPad and Mac.', home, 'home-page')

routes = [('/', 'Home')]
for route,title,description in [
    ('privacy','Kotobaia Privacy Policy','How Kotobaia handles account information, Google sign-in, learning data, purchases, optional AI and speech processing.'),
    ('support','Kotobaia Support','Help with Kotobaia accounts, purchases, restoration and learning features.'),
    ('terms','Kotobaia Terms of Use','Kotobaia app license, subscriptions, service access and AI content.'),
    ('website-privacy','Kotobaia Website Privacy','Privacy information for this website and your language preferences.'),
]:
    article=(ROOT/'content'/f'{route}.html').read_text()
    page('/'+route+'/',title,description,'<div class="wrap document-wrap">'+article+'</div>','document-page')
    routes.append(('/'+route+'/',title))
not_found=f'<div class="wrap not-found"><p class="eyebrow">404 / KOTOBAIA</p><h1>{t("Page not found")}</h1><a class="button" href="/">Kotobaia {arrow}</a></div>'
page('/404.html','Page Not Found — Kotobaia','Return to the Kotobaia website.',not_found,'document-page')
(DIST/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://kotobaia.com/sitemap.xml\n')
(DIST/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>https://kotobaia.com{route}</loc></url>' for route,_ in routes)+'</urlset>\n')
(DIST/'.nojekyll').touch()
base=(ROOT/'content/base-locales.js').read_text().strip().removeprefix('window.SUNIMORI_TRANSLATIONS = ').removesuffix(';')
dictionaries=json.loads(base)
extra=ROOT/'content/translations.json'
if extra.exists():
    additions=json.loads(extra.read_text())
    for locale in dictionaries: dictionaries[locale].update(additions[locale])
(DIST/'locales.js').write_text('window.KOTOBAIA_TRANSLATIONS = '+json.dumps(dictionaries,ensure_ascii=False,separators=(',',':'))+';\n')
print('Built Kotobaia homepage, four supporting pages, 404, sitemap and translations.')
