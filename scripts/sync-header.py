"""Keep crawlable, no-JavaScript navigation identical on every marketing page."""
from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
header=(root/'partials/header.html').read_text().strip()
for relative in ['index.html','prijzen/index.html','alles-in-1/index.html','contact/index.html']:
    path=root/relative
    text=path.read_text()
    text,count=re.subn(r'<header class="header">[\s\S]*?</header>',lambda _:header,text,count=1)
    assert count==1,relative
    path.write_text(text)
