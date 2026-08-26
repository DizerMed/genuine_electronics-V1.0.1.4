import re

with open("public/sw.js", "r") as f:
    content = f.read()

# Replace all occurrences
content = content.replace(
    "if (networkResponse && networkResponse.status === 200) {",
    "if (networkResponse && networkResponse.status === 200 && networkResponse.type !== 'opaque') {"
)

with open("public/sw.js", "w") as f:
    f.write(content)
