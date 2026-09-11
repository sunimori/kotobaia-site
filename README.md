# Kotobaia

The official Kotobaia website by Sunimori. Static, accessible and available in 12 languages, including Arabic with right-to-left layout. The app is presented as preparing for launch.

## Content

- Product homepage with real development screenshots and keyboard-accessible feature tabs.
- Support, app privacy, terms and website privacy pages.
- Browser-language detection, explicit language selection and local preference storage.
- Responsive layouts, native language dialog and reduced-motion support.

## Build and preview

Python 3.9+ is sufficient. No dependency installation is required.

```sh
python3 build.py
python3 check.py
python3 -m http.server 18791 --bind 127.0.0.1 --directory dist
```

`build.py` generates pages and translation dictionaries. Edit the shared layout there, translation content in `content/`, and styling/interactions in `dist/style.css` and `dist/app.js`. Generated files in `dist/` are checked in for transparent review. `check.py` validates local routes, anchors, required translations, accessible image labels and public-file boundaries.

## Hosting

Pushes to `main` build and publish `dist/` through GitHub Actions to GitHub Pages. The production custom domain is `kotobaia.com`; `www` redirects to it through Pages. DNS remains at Squarespace, including email forwarding and DNSSEC. Domain association and HTTPS are configured in repository Pages settings. The `.openai/hosting.json` manifest supports a separate owner-only design preview; it contains no credentials.

Only website source and public marketing assets belong in this repository. There is no app source, account database, sandbox receipt, backend configuration or API credential here. Visitors can download delivered frontend assets. Contact links use the visitor's email application; there is no tracking or form backend.

## Assets

Kotobaia icon, character and development screenshots are Sunimori product assets. The courtyard hero is an original AI-generated marketing illustration. Screenshots show a development version and do not imply final availability. Website translations do not imply the app itself supports all website languages.

Copyright © 2026 Sunimori. All rights reserved. Public repository visibility does not grant a license to reuse the brand, artwork or application assets.
