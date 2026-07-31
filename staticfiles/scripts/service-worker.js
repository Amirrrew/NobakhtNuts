const CACHE_NAME = 'nobakhtnuts-v1';

const urlsToCache = [
    '/',
    '/static/styles/main.css',
    '/static/scripts/main.js',
    '/static/scripts/home.js',
    '/static/scripts/verify.js',
    '/static/scripts/account.js',
    '/static/media/logo/pwa-icons/icon-192.png',
    '/offline/',
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(async cache => {
            for (const url of urlsToCache) {
                const response = await fetch(url);

                console.log(
                    url,
                    'status:', response.status,
                    'type:', response.type,
                    'ok:', response.ok
                );

                await cache.put(url, response);
            }
        })
    );

    self.skipWaiting();
});