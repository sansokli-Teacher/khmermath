// Minimal service worker: makes the site installable and shows a friendly page when
// the phone is offline. It never caches the API or exam pages, so data is always live.
const OFFLINE = '/offline';
self.addEventListener('install', (e) => { e.waitUntil(caches.open('exam-offline-v2').then((c) => c.add(OFFLINE)).then(() => self.skipWaiting())); });
self.addEventListener('activate', (e) => { e.waitUntil(self.clients.claim()); });
self.addEventListener('fetch', (e) => {
  if (e.request.mode !== 'navigate') return;
  e.respondWith(fetch(e.request).catch(() => caches.match(OFFLINE)));
});
