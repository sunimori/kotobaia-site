(() => {
 'use strict';
 // Wordbook / friend-invite landing pages (/d/, /f/). The app puts the deck data or invite code after "#":
 // browsers never send that part to the server, so it is read here, on the visitor's device, and nowhere else.
 // With Kotobaia installed, iOS and macOS open these links in the app directly (universal links).
 const root = document.querySelector('[data-share-page]');
 if (!root) return;
 const MAX_OUTPUT = 4 * 1024 * 1024;
 const reveal = selector => root.querySelectorAll(selector).forEach(el => { el.hidden = false; });
 const openLinks = [...root.querySelectorAll('[data-open-app]')];
 const fail = () => {
  root.querySelectorAll('.share-ready, .share-nopreview').forEach(el => { el.hidden = true; });
  openLinks.forEach(a => { a.hidden = true; });
  reveal('.share-error');
 };
 let fragment = '';
 try { fragment = decodeURIComponent(location.hash.slice(1)); } catch { fragment = ''; }
 fragment = fragment.replace(/[?&].*$/, '');   // some apps append tracking parameters after the fragment

 if (root.dataset.sharePage === 'friend') {
  const code = fragment.trim();
  if (!/^[A-Za-z0-9]{4,32}$/.test(code)) { fail(); return; }
  root.querySelector('.invite-code').textContent = code;
  openLinks.forEach(a => { a.href = 'kotobaia://friend?code=' + encodeURIComponent(code); });
  reveal('.share-ready');
  return;
 }

 if (!/^1\.[A-Za-z0-9_-]+$/.test(fragment)) { fail(); return; }
 // Universal links do not fire for a link on the same site, so the button uses the app's own scheme.
 openLinks.forEach(a => { a.href = 'kotobaia://d#' + fragment; });
 if (typeof DecompressionStream !== 'function') { reveal('.share-nopreview'); return; }
 decode(fragment.slice(2)).then(render).catch(fail);

 async function decode(payload) {
  const base64 = payload.replace(/-/g, '+').replace(/_/g, '/');
  const binary = atob(base64 + '==='.slice((base64.length + 3) % 4));
  const bytes = Uint8Array.from(binary, c => c.charCodeAt(0));
  // The app compresses with Apple's zlib, which is raw DEFLATE (no zlib header).
  const reader = new Blob([bytes]).stream().pipeThrough(new DecompressionStream('deflate-raw')).getReader();
  const chunks = [];
  let size = 0;
  for (;;) {
   const { done, value } = await reader.read();
   if (done) break;
   size += value.length;
   if (size > MAX_OUTPUT) { reader.cancel(); throw new Error('too large'); }
   chunks.push(value);
  }
  const deck = JSON.parse(new TextDecoder().decode(await new Blob(chunks).arrayBuffer()));
  if (!deck || typeof deck.name !== 'string' || !Array.isArray(deck.tracks) || !deck.tracks.length) throw new Error('not a deck');
  return deck;
 }

 // Meanings: Chinese pages show the Chinese meaning; other pages show a meaning in their language only when the
 // sender's link carries one (built-in meanings are not included in links), otherwise just the word and reading.
 function meaningFor(deck, track) {
  const page = document.documentElement.lang || 'en';
  if (page.startsWith('zh')) return track.zh || '';
  const lang = ['ja', 'ko'].includes(page) ? page : 'en';
  return deck.sharedMeanings?.[track.id]?.[lang] || '';
 }

 function span(cls, text, lang) {
  const el = document.createElement('span');
  el.className = cls;
  el.textContent = text;
  if (lang) el.lang = lang;
  return el;
 }

 function render(deck) {
  root.querySelector('.deck-name').textContent = deck.name.slice(0, 200);
  root.querySelector('.deck-count').textContent = String(deck.tracks.length);
  const list = root.querySelector('.deck-words');
  for (const track of deck.tracks.slice(0, 8)) {
   const item = document.createElement('li');
   const lang = typeof track.lang === 'string' ? track.lang : 'ja';
   item.append(span('deck-word', String(track.jp || '').slice(0, 80), lang));
   if (track.reading && track.reading !== track.jp) item.append(span('deck-reading', String(track.reading).slice(0, 120), lang));
   const meaning = String(meaningFor(deck, track)).slice(0, 160);
   if (meaning) item.append(span('deck-meaning', meaning));
   list.append(item);
  }
  if (deck.tracks.length > 8) {
   const more = document.createElement('li');
   more.className = 'deck-more';
   more.textContent = '+' + (deck.tracks.length - 8);
   list.append(more);
  }
  reveal('.share-ready');
 }
})();
