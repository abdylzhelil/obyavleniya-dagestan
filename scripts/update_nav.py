"""Update the shared site navigation. Run from any directory."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parent.parent
NAV=(ROOT/'scripts/templates/site-nav.html').read_text().strip()
for p in ROOT.glob('*.html'):
    text=p.read_text()
    if 'id="site-nav"' not in text: continue
    nav=NAV.replace('index.html#','#') if p.name=='index.html' else NAV
    text,count=re.subn(r'<nav\b(?=[^>]*\bid="site-nav")[^>]*>.*?</nav>',lambda _:nav,text,count=1,flags=re.S)
    if count!=1: raise ValueError('Navigation missing: '+p.name)
    p.write_text(text)
    print('Navigation:',p.name)
