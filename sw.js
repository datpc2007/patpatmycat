const CACHE = 'catpat-v1';
const BASE = self.registration.scope; // tự detect: local hay GitHub Pages

const FILES = [
  '',
  'index.html',
  'manifest.json',
  'icon.png',
  'image/cat_sleep.png',
  'image/cat_stare.png',
  'image/cat_head.png',
  'image/hand0.png',
  'image/hand1.png',
  'image/hand2.png',
  'image/hand3.png',
  'image/hand4.png',
  'sound/pat0.ogg',
  'sound/pat1.ogg',
  'sound/pat2.ogg',
  'sound/bruh.ogg',
  'sound/crazy.ogg',
].map(f => BASE + f);

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(FILES))
  );
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(r => r || fetch(e.request))
  );
});
