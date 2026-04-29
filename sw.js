const CACHE = 'catpat-v2';
const FILES = [
  'index.html',
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
];

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
  // Chỉ cache GET, không can thiệp navigation
  if (e.request.method !== 'GET') return;
  e.respondWith(
    caches.match(e.request).then(r => r || fetch(e.request))
  );
});
