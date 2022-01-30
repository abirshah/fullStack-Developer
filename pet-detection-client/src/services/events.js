export function getEvents() {
    return fetch('http://127.0.0.1:8000/events')
        .then(data => data.json())
}