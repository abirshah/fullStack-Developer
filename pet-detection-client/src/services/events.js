export function getEvents() {
    return fetch('http://localhost:5000/events')
        .then(data => data.json())
}