self.addEventListener("install", event => {
    self.skipWaiting();
    event.waitUntil(caches.open("vvs-SW_HASH")
        .then(cache => cache.addAll(["/static/screen.css?CSS_HASH", "/static/manifest.json",
            "/static/icons/favicon.ico", "/static/icons/icon-192x192.png", "/static/icons/icon-256x256.png",
            "/header", "/offline"])))
});

self.addEventListener("activate", event => event.waitUntil(
    caches.keys().then(cacheNames => Promise.all(cacheNames
        .filter(name => name != "vvs-SW_HASH")
        .map(cacheName => caches.delete(cacheName))))));


self.addEventListener("fetch", event => {
    const url = new URL(event.request.url);
    if (url.pathname.startsWith('/dest/')) {
        const { readable, writable } = new TransformStream();
        event.respondWith(new Response(readable, {
            headers: { 'Content-Type': 'text/html; charset=utf-8' }
        }));

        event.waitUntil(async function () {
            const content = fetch(`/content${url.pathname.substring(5)}${url.search}`);
            const header = caches.match('/header');

            try {
                await (await header).body.pipeTo(writable, { preventClose: true });
                await (await content).body.pipeTo(writable);
            } catch (e) {
                const offline = caches.match('/offline');
                await (await offline).body.pipeTo(writable);
            }
        }());
    } else {
        event.respondWith(caches.match(event.request)
            .then(response => response || fetch(event.request)));
    }
});
