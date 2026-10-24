const IMAGE_CACHE='phone-images-v1';
self.addEventListener('install',()=>self.skipWaiting());
self.addEventListener('activate',event=>event.waitUntil(self.clients.claim()));
self.addEventListener('fetch',event=>{
 const url=new URL(event.request.url);
 if(event.request.method!=='GET'||url.origin!==self.location.origin||!/(?:\/media\/|\/ig\/|\/stories\/|\/kakao\/|\/music\/.*(?:cover|\.jpg))/.test(url.pathname)||! /\.(?:jpg|jpeg|png|webp)$/i.test(url.pathname))return;
 event.respondWith(caches.open(IMAGE_CACHE).then(async cache=>{
  const cached=await cache.match(event.request);if(cached)return cached;
  const response=await fetch(event.request);if(response.ok)event.waitUntil(cache.put(event.request,response.clone()).catch(()=>{}));return response;
 }));
});
