if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/service-worker.js')
        .then(() => console.log('service worker registered'))
        .catch((err) => console.log('service worker registration failed' ,err))
}