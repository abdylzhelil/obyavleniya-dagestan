"""Refresh both radar instances from the canonical template, without rebuilding page copy."""
from pathlib import Path
import re

root = Path(__file__).resolve().parent.parent
template = (root / "scripts/templates/client-radar.html").read_text().strip()
for name, demo_id in (("index.html", "home-radar"), ("bot-crm.html", "client-radar")):
    page = root / name
    text = page.read_text()
    # Balanced div parser: the component contains nested cards and controls.
    marker = '<div class="kr-demo" id="' + demo_id + '"'
    start = text.index(marker)
    depth = 0
    end = None
    for tag in re.finditer(r"</?div\b[^>]*>", text[start:]):
        depth += -1 if tag.group().startswith("</") else 1
        if depth == 0:
            end = start + tag.end()
            break
    if end is None:
        raise ValueError("Unclosed radar component: " + name)
    text = text[:start] + template.replace("client-radar", demo_id) + text[end:]
    page.write_text(text)
print("Updated home and CRM radar from the same template")
