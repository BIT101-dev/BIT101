declare let self: ServiceWorkerGlobalScope;

type PushMessage = {
	data: string
	badge: string
	icon: string
	timestamp: number
}

type PushNotificationData = {
  id: number
  created_time: string
  update_time: string
  delete_time: string
  uid: number
  type: "comment" | "like" | "follow" | "system"
  unread_num: number
  last_time: string
  content: string
}



self.addEventListener('push', (event) => {
  console.debug("[Service Worker] Push event received", event);
  const data: PushMessage = event.data?.json();
  console.debug("[Service Worker] Push event data", data);

  const msg : PushNotificationData = JSON.parse(atob(data.data));

  const title = "BIT101";
  let body = "";

  if (msg.type === "comment") {
    body = `你收到了 ${msg.unread_num} 条评论`;
  } else if (msg.type === "like") {
    body = `你收到了 ${msg.unread_num} 个赞`;
  } else if (msg.type === "follow") {
    body = `你有 ${msg.unread_num} 个新粉丝`;
  } else if (msg.type === "system") {
    body = `你有 ${msg.unread_num} 条系统消息`;
  } else return ;

  event.waitUntil(
    self.registration.showNotification(title, {
      body: body,
      badge: data.badge,
      icon: data.icon,
      // 好像是Workers Typing问题
      //@ts-expect-error
      timestamp: data.timestamp,
      tag: msg.type,
    })
  );
})

self.addEventListener('notificationclick', function (event) {
  console.log('[Service Worker] Notification click Received.');

  let clients = new Clients();

  event.notification.close();
  event.waitUntil(
    clients
      .matchAll({
        type: "window",
      })
      .then((clientList) => {
        for (const client of clientList) {
          if (client.url === "/" && "focus" in client) return client.focus();
        }
        if (clients.openWindow) return clients.openWindow("/");
      }),
  );
});

import { precacheAndRoute, cleanupOutdatedCaches } from 'workbox-precaching';

cleanupOutdatedCaches();

precacheAndRoute(self.__WB_MANIFEST);

import { clientsClaim } from 'workbox-core';

self.skipWaiting();
clientsClaim();