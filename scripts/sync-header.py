"""Keep crawlable, no-JavaScript navigation identical on every marketing page."""
from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
header=(root/'partials/header.html').read_text().strip()
for relative in [str(p.relative_to(root)) for p in root.rglob('index.html') if 'node_modules' not in p.parts]:
    path=root/relative
    text=path.read_text()
    if 'http-equiv="refresh"' in text: continue
    text,count=re.subn(r'<header class="header">[\s\S]*?</header>',lambda _:header,text,count=1)
    assert count==1,relative
    path.write_text(text)
