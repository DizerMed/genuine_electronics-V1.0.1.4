import re

with open("public/sw.js", "r") as f:
    content = f.read()

# Replace both occurrences of the opaque check
content = content.replace(
    "if (networkResponse && (networkResponse.status === 200 || networkResponse.type === 'opaque')) {",
    "if (networkResponse && networkResponse.status === 200 && networkResponse.type !== 'opaque') {"
)

with open("public/sw.js", "w") as f:
    f.write(content)
