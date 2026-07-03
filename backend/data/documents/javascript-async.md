# JavaScript 异步编程

## Promise

```javascript
fetch("/api/data")
    .then(res => res.json())
    .then(data => console.log(data))
    .catch(err => console.error(err));
```

## Async/Await

```javascript
async function loadData() {
    try {
        const res = await fetch("/api/data");
        const data = await res.json();
        return data;
    } catch (err) {
        console.error(err);
    }
}
```

## ReadableStream

```javascript
const reader = response.body.getReader();
const decoder = new TextDecoder();
while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    console.log(decoder.decode(value));
}
```
