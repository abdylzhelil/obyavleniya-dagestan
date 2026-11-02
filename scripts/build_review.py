from pathlib import Path
import shutil,re
root=Path(__file__).resolve().parent.parent;dist=root/'dist'
for p in list(root.iterdir()):
 if p.name.startswith('.') or p.name in ['dist','CNAME','README.md','scripts']:continue
 q=dist/p.name
 if p.is_dir():shutil.copytree(p,q,dirs_exist_ok=True)
 else:shutil.copy2(p,q)
for p in dist.glob('*.html'):
 s=p.read_text();s=re.sub(r'<meta name="robots"[^>]*>','',s)
 if 'data-preview="true"' not in s:s=s.replace('<html lang="ru"','<html lang="ru" data-preview="true"',1)
 s=s.replace('</head>','<meta name="robots" content="noindex, nofollow">\n</head>');p.write_text(s)
(dist/'robots.txt').write_text('User-agent: *\nDisallow: /\n')
print('Built private review copy')
