"""Сборка страниц ботов: bot-moderation.html (Modexa) и bot-crm.html (КлиентРадар).

Запуск из любой папки:
    python3 scripts/build_bot_pages.py            # только Modexa
    python3 scripts/build_bot_pages.py crm        # только КлиентРадар
    python3 scripts/build_bot_pages.py modexa crm # обе

Шапка (<head>) берётся из уже существующего файла страницы, остальное собирается
из словарей mod и crm ниже. Нужен пакет Pillow (размеры картинок).
Править тексты — в словарях mod/crm, а не в готовом HTML: при следующей сборке
правки в HTML затираются. Видео лежат в assets/video, превью — assets/images.
"""
import os,sys
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import re,html
from PIL import Image
def a(t): return html.escape(t,quote=False)
ICONS={
'shield':'<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
'msg':'<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
'clock':'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
'mega':'<path d="M3 11l18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
'key':'<circle cx="7.5" cy="15.5" r="4.5"/><path d="M21 2l-9.6 9.6M15.5 7.5l3 3L22 7l-3-3"/>',
'chart':'<path d="M18 20V10M12 20V4M6 20v-6"/>',
'users':'<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
'gift':'<rect x="3" y="8" width="18" height="4"/><path d="M12 8v13M19 12v9H5v-9M7.5 8a2.5 2.5 0 0 1 0-5C11 3 12 8 12 8s1-5 4.5-5a2.5 2.5 0 0 1 0 5"/>',
'search':'<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
'filter':'<path d="M22 3H2l8 9.5V19l4 2v-8.5L22 3z"/>',
'list':'<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
'bolt':'<path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>',
'send':'<path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/>',
'bell':'<path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9M13.7 21a2 2 0 0 1-3.4 0"/>',
'star':'<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
'pen':'<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/>',
'globe':'<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20M12 2a15 15 0 0 0 0 20"/>',
'wand':'<path d="M15 4V2M15 16v-2M8 9h2M20 9h2M17.8 11.8 19 13M15 9h.01M17.8 6.2 19 5M3 21l9-9M12.2 6.2 11 5"/>',
'ai':'<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 1v3M15 1v3M9 20v3M15 20v3M20 9h3M20 14h3M1 9h3M1 14h3"/>',
'lock':'<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
'brain':'<path d="M9.5 2A3.5 3.5 0 0 0 6 5.5v.3A3.5 3.5 0 0 0 4 9a3.5 3.5 0 0 0 1 2.4A3.5 3.5 0 0 0 6 17.5 3.5 3.5 0 0 0 9.5 22H12V2ZM14.5 2A3.5 3.5 0 0 1 18 5.5v.3A3.5 3.5 0 0 1 20 9a3.5 3.5 0 0 1-1 2.4A3.5 3.5 0 0 1 18 17.5a3.5 3.5 0 0 1-3.5 4.5H12"/>',
'return':'<path d="M9 14 4 9l5-5"/><path d="M4 9h10.5a5.5 5.5 0 0 1 0 11H11"/>',
}
def ic(n): return '<span class="ic"><svg viewBox="0 0 24 24" aria-hidden="true">%s</svg></span>'%ICONS[n]
TG='<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.9 4.1 2.8 11.5c-1 .4-1 1.3-.2 1.6l4.8 1.5 1.9 5.6c.2.6.4.8.9.8.4 0 .6-.2.9-.5l2.3-2.2 4.7 3.5c.9.5 1.5.2 1.7-.8L23.5 5.4c.3-1.3-.5-1.8-1.6-1.3zM8.7 13.6l9.4-5.9c.4-.3.8-.1.5.2l-7.9 7.1-.3 3.4-1.7-4.8z"/></svg>'

def vid(v):
    fn,po,lab=v
    return '<div class="vidbox"><div class="vid"><video src="assets/video/%s" poster="assets/images/%s" muted loop playsinline preload="none" aria-label="%s"></video></div><button class="snd" type="button">🔊 Включить звук</button></div>'%(fn,po,a(lab).replace('"','&quot;'))
TABJS='''<script>(function(){var tabs=[].slice.call(document.querySelectorAll('.tab'));if(!tabs.length)return;var panels=tabs.map(function(t){return document.getElementById(t.getAttribute('aria-controls'));});
function show(i,f){tabs.forEach(function(t,k){t.setAttribute('aria-selected',k===i?'true':'false');t.tabIndex=k===i?0:-1;panels[k].hidden=k!==i;});if(f)tabs[i].focus();var t=tabs[i];if(t.scrollIntoView&&t.parentNode.scrollWidth>t.parentNode.clientWidth){t.parentNode.scrollTo({left:t.offsetLeft-16,behavior:'smooth'});}}
tabs.forEach(function(t,i){t.addEventListener('click',function(){show(i);});t.addEventListener('keydown',function(e){var n=e.key==='ArrowRight'?1:e.key==='ArrowLeft'?-1:0;if(n){e.preventDefault();show((i+n+tabs.length)%tabs.length,true);}});});show(0);})();</script>'''
VIDJS='''<script>(function(){var vs=[].slice.call(document.querySelectorAll('.vid video'));if(!vs.length)return;var rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
function snd(v){return v.closest('.vidbox').querySelector('.snd');}
vs.forEach(function(v){var b=snd(v);function tg(){var on=v.muted;vs.forEach(function(o){if(o!==v){o.muted=true;snd(o).textContent='🔊 Включить звук';}});v.muted=!on;if(on){v.volume=1;v.controls=true;var p=v.play();if(p&&p.catch)p.catch(function(){v.controls=true;});}else{v.controls=false;}b.textContent=on?'🔇 Выключить звук':'🔊 Включить звук';}b.addEventListener('click',tg);v.addEventListener('click',tg);});
if(rm||!('IntersectionObserver' in window))return;
var io=new IntersectionObserver(function(es){es.forEach(function(e){var v=e.target;if(e.isIntersecting){var p=v.play();if(p&&p.catch)p.catch(function(){});}else{v.pause();}});},{threshold:.35});vs.forEach(function(v){io.observe(v);});})();</script>'''
def page(cfg):
    old=open(cfg['file'],encoding='utf-8').read()
    head=re.sub(r'<script type="application/ld\+json">.*?</script>\n?','',old[:old.index('</head>')+7],flags=re.S).replace('<link rel="stylesheet" href="style.css">','<link rel="stylesheet" href="bot.css">')
    f=cfg
    import json
    ld={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":t}} for q,t in f['faq']]}
    head=head.replace('</head>','<script type="application/ld+json">\n'+json.dumps(ld,ensure_ascii=False,indent=1)+'\n</script>\n</head>',1)
    cards=''.join('<div class="card">%s<h3>%s</h3><p>%s</p></div>'%(ic(i),a(t),a(p)) for i,t,p in f.get('features',[]))
    shots=''
    if f.get('shots'):
        shots='''<section id="screens"><div class="wrap">
<div class="sec-head"><div class="eyebrow">Скриншоты</div><h2>Как выглядит бот</h2></div>
<div class="shots">%s</div></div></section>'''%''.join('<figure class="shot"><div class="phone phone-ph"><div class="ph-in"><span>Скриншот скоро</span></div></div><figcaption><strong>%s</strong>%s</figcaption></figure>'%(a(t),a(c)) if fn is None else '<figure class="shot"><div class="phone"><img src="assets/images/%s" alt="Скриншот бота %s: %s" width="%d" height="%d" loading="lazy"></div><figcaption><strong>%s</strong>%s</figcaption></figure>'%(fn,f['name'],a(t).lower(),*Image.open('assets/images/'+fn).size,a(t),a(c)) for fn,t,c,w,h in f['shots'])
    if f.get('vshots'):
        _vf=['<figure class="shot">%s<figcaption><strong>%s</strong>%s</figcaption></figure>'%(vid(v),a(t),a(c)) for v,t,c in f['vshots']]
        _n=f.get('vmore',len(_vf))
        vrow='<div class="sub-h">Видео</div><div class="shots shots-v">'+''.join(_vf[:_n])+'</div>'
        if len(_vf)>_n: vrow+='<details class="more more-v"><summary class="btn btn-line">Ещё видео</summary><div class="shots shots-v">'+''.join(_vf[_n:])+'</div></details>'
        vrow+='<div class="sub-h">Скриншоты</div>'
        shots=shots.replace('<div class="shots">',vrow+'<div class="shots">',1).replace('<div class="eyebrow">Скриншоты</div>','<div class="eyebrow">Видео и скриншоты</div>',1)
    aud=''.join('<div class="card"><h3>%s</h3><p>%s</p></div>'%(a(t),a(p)) for t,p in f['aud'])
    steps=''.join('<li class="step"><p>%s</p></li>'%s for s in f['steps'])
    tar=''.join('<div class="tariff%s">%s<h3>%s</h3><div class="price">%s<small>%s</small></div><p>%s</p></div>'%(' pop' if pop else '','<span class="badge">'+f.get('badge','Популярный')+'</span>' if pop else '',a(n),a(pr),a(sm),a(tx)) for n,pr,sm,tx,pop in f['tariffs'])
    if f.get('tmore'):
        _t=tar.split('<div class="tariff')[1:]
        _t=['<div class="tariff'+x for x in _t]
        tar=''.join(_t[:f['tmore']])+'</div><details class="more more-t"><summary class="btn btn-line">Показать все тарифы</summary><div class="tariffs t3">'+''.join(_t[f['tmore']:])+'</div></details><div hidden>'
    faq=''.join('<details><summary>%s</summary><p>%s</p></details>'%(a(q),a(t)) for q,t in f['faq'])
    if f.get('faqmore'):
        _q=['<details><summary>%s</summary><p>%s</p></details>'%(a(q),a(t)) for q,t in f['faq']]
        faq=''.join(_q[:f['faqmore']])+'</div><details class="more more-q"><summary class="btn btn-line">Ещё вопросы</summary><div class="faq">'+''.join(_q[f['faqmore']:])+'</div></details><div hidden>'
    cta=lambda cls,txt,goal:'<a class="btn %s" href="%s" rel="noopener" target="_blank" data-goal="%s">%s%s</a>'%(cls,f['tg'],goal,TG,txt)
    other=f['other']
    why=''
    adm=''
    cab=''
    if f.get('cabinet'):
        cab='<section id="cabinet"><div class="wrap"><div class="sec-head rv"><div class="eyebrow">Мини-приложение</div><h2>%s</h2></div><div class="card rv" style="max-width:820px"><p style="font-size:16px">%s</p></div></div></section>'%(a(f['cabinet'][0]),f['cabinet'][1])
    if f.get('admins'):
        adm='<section id="admins"><div class="wrap"><div class="sec-head"><div class="eyebrow">Группы</div><h2>%s</h2></div><div class="card" style="max-width:820px"><p style="font-size:16px">%s</p></div></div></section>'%(a(f['admins'][0]),f['admins'][1])
    if f.get('why'):
        why='<section><div class="wrap"><div class="sec-head"><div class="eyebrow">Преимущества</div><h2>Почему Modexa</h2></div><div class="grid '+f.get('whycls','g4')+'">'+''.join('<div class="card">%s<h3>%s</h3><p>%s</p></div>'%(ic(i),a(t),a(x)) for i,t,x in f['why'])+'</div></div></section>'
    visual=f['visual']
    if f.get('tabs'):
        tb=''.join('<button class="tab" role="tab" type="button" id="t-%d" aria-controls="p-%d" aria-selected="%s">%s</button>'%(k,k,'true' if k==0 else 'false',a(t['label'])) for k,t in enumerate(f['tabs']))
        pn=''
        for k,t in enumerate(f['tabs']):
            rows='<ul class="chips">'+''.join('<li>%s</li>'%a(c) for c in t['chips'])+'</ul>' if t.get('chips') else ''.join('<details class="acc"><summary><span class="ic"><svg viewBox="0 0 24 24" aria-hidden="true">%s</svg></span><span class="acc-t">%s</span></summary><p>%s</p></details>'%(ICONS[i],a(ti),a(tx)) for i,ti,tx in t['items'])
            intro='<p class="tp-intro">%s</p>'%a(t['intro']) if t.get('intro') else ''
            pn+='<div class="tabpanel" role="tabpanel" id="p-%d" aria-labelledby="t-%d"><div class="tp-grid">%s<div class="tp-body">%s<div class="acc-list">%s</div></div></div></div>'%(k,k,vid(t['vid']) if t.get('vid') else '',intro,rows)
        featsec='<section id="features"><div class="wrap"><div class="sec-head"><div class="eyebrow">Возможности</div><h2>%s</h2></div><div class="tabs" role="tablist" aria-label="Разделы возможностей">%s</div>%s</div></section>'%(a(f['fh']),tb,pn)
    elif f.get('secs'):
        featsec=''
        for k,sc in enumerate(f['secs']):
            cs=''.join('<div class="card">%s<h3>%s</h3><p>%s</p></div>'%(ic(i),a(t),p if sc.get('raw') else a(p)) for i,t,p in sc.get('cards',[]))
            hd='<div class="sec-head"><div class="eyebrow">%s</div><h2>%s</h2>%s</div>'%(a(sc['eyebrow']),a(sc['title']),'<p class="sec-lead">%s</p>'%sc['lead'] if sc.get('lead') else '')
            if sc.get('vid'): hd='<div class="head-vid">%s%s</div>'%(hd,vid(sc['vid']))
            featsec+='<section%s><div class="wrap">%s%s%s</div></section>\n'%(' id="features"' if k==0 else '',hd,'<div class="grid %s">%s</div>'%(sc.get('cols','g3'),cs) if cs else '',sc.get('html',''))
    else:
        featsec='<section id="features"><div class="wrap"><div class="sec-head"><div class="eyebrow">Возможности</div><h2>%s</h2></div><div class="grid g4">%s</div></div></section>'%(a(f['fh']),cards)
    points='<ul class="hero-points">'+''.join('<li>%s</li>'%a(x) for x in f['points'])+'</ul>' if f.get('points') else ''
    tnotehtml=f['tlist'] if f.get('tlist') else '<p class="note">%s</p>'%a(f['tnote'])
    facts='<div class="facts"><div class="wrap">'+''.join('<div class="fact"><b>%s</b><span>%s</span></div>'%(a(x),a(y)) for x,y in f['facts'])+'</div></div>' if f.get('facts') else ''
    vidjs=(TABJS if f.get('tabs') else '')+(VIDJS if ('<video' in featsec or '<video' in shots or '<video' in visual or f.get('startvid')) else '')
    startvid=vid(f['startvid']) if f.get('startvid') else ''
    audsec='' if f.get('noaud') else '<section><div class="wrap"><div class="sec-head"><div class="eyebrow">Для кого</div><h2>Кому подойдёт</h2></div><div class="grid g3">%s</div></div></section>'%aud
    _ss='<section id="start"><div class="wrap">\n  <div class="%s"><div class="sec-head"><div class="eyebrow">%s</div><h2>%s</h2></div>%s</div>\n  <ol class="steps">%s</ol>\n  %s\n</div></section>'
    startsec_before=startsec_after=''
    startnote='<p class="note">%s</p>'%f['startnote'] if f.get('startnote') else ''
    _startsec=_ss%('head-vid' if startvid else 'sh-plain',a(f.get('seyebrow','Как начать')),a(f.get('sh','Четыре шага до результата')),startvid,steps,startnote)
    if f.get('startfirst'): startsec_before=_startsec
    else: startsec_after=_startsec
    if f.get('meta'):
        mt=a(f['meta']).replace('"','&quot;')
        for nm in ('<meta name="description" content="','<meta property="og:description" content="','<meta name="twitter:description" content="'):
            head=re.sub('('+re.escape(nm)+')[^"]*',lambda m:m.group(1)+mt,head)
    if f.get('ogtitle'):
        _t=a(f['ogtitle']).replace('"','&quot;')
        head=re.sub(r'<title>.*?</title>','<title>%s</title>'%_t,head,count=1)
        for nm in ('<meta property="og:title" content="','<meta name="twitter:title" content="'):
            head=re.sub('('+re.escape(nm)+')[^"]*',lambda m:m.group(1)+_t,head)
    if f.get('ogimg'):
        _u='https://obyavleniya-dagestan.ru/assets/images/'+f['ogimg']
        for nm in ('<meta property="og:image" content="','<meta name="twitter:image" content="'):
            head=re.sub('('+re.escape(nm)+')[^"]*',lambda m:m.group(1)+_u,head)
    if f.get('ogalt'):
        _a=a(f['ogalt']).replace('"','&quot;')
        for nm in ('<meta property="og:image:alt" content="','<meta name="twitter:image:alt" content="'):
            head=re.sub('('+re.escape(nm)+')[^"]*',lambda m:m.group(1)+_a,head)
    body='''<body class="theme-%(theme)s">
<a class="skip-link" href="#main">К содержимому</a>
<header class="bh"><div class="wrap">
  <a class="bh-brand" href="%(file)s">%(hlogo)s<span>%(name)s</span></a>
  <nav class="bh-nav" aria-label="Разделы страницы"><a href="#features">Возможности</a>%(shotsnav)s<a href="#start">%(startlabel)s</a><a href="#tariffs">Тарифы</a><a href="#faq">Вопросы</a><span class="bh-sep" aria-hidden="true"></span><a href="index.html">← На сайт</a><a href="%(ofile)s">%(oshort)s</a></nav>
  %(cta_head)s
  <button class="bh-burger" type="button" aria-label="Меню" aria-expanded="false" aria-controls="bh-menu"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
</div>
<div class="bh-menu" id="bh-menu" hidden><div class="wrap">
  <a href="index.html">← На сайт «Объявления Дагестана»</a>
  <a href="%(ofile)s">%(oshort)s — другой бот</a>
  <a href="#features">Возможности</a>%(shotsmenu)s<a href="#start">%(startlabel)s</a><a href="#tariffs">Тарифы</a><a href="#faq">Вопросы</a>
</div></div>
</header>
<main id="main">
<section class="hero"><div class="wrap">
  <div>
    <div class="pill"><i></i>%(pill)s</div>
    <h1>%(h1)s</h1>
    <p class="lead">%(lead)s</p>
    <div class="hero-ctas">%(cta_hero)s<a class="btn btn-line" href="#features">Что умеет бот</a></div>
    <p class="hero-note">%(note)s</p>
    %(points)s
  </div>
  <div class="hero-visual">%(visual)s</div>
</div></section>
%(facts)s%(startsec_before)s%(featsec)s
%(shots)s
%(cab)s
%(why)s
%(startsec_after)s
%(audsec)s
%(adm)s
<section id="tariffs"><div class="wrap">
  <div class="sec-head"><div class="eyebrow">Тарифы</div><h2>Сколько это стоит</h2></div>
  <div class="tariffs %(tcls)s">%(tar)s</div>
  %(tnotehtml)s
  %(tsoon)s
</div></section>
<section id="faq"><div class="wrap">
  <div class="sec-head"><div class="eyebrow">Вопросы</div><h2>Частые вопросы</h2></div>
  <div class="faq">%(faq)s</div>
</div></section>
<div class="wrap"><div class="final">
  <h2>%(ft)s</h2><p>%(fp)s</p>
  <div class="hero-ctas">%(cta_final)s<a class="btn btn-line" href="%(ofile)s">%(oname)s</a></div>
</div></div>
</main>
<footer class="bf"><div class="wrap">
  <a class="bh-brand" href="%(file)s">%(hlogo)s<span>%(name)s</span></a>
  <a href="index.html">← ОБЪЯВЛЕНИЯ ДАГЕСТАНА</a>
  <a href="%(ofile)s">%(oname)s</a>
  %(contacts)s<a class="sp" href="privacy.html">Политика конфиденциальности</a>
</div></footer>
<script>(function(){var b=document.querySelector('.bh-burger'),m=document.getElementById('bh-menu');if(!b||!m)return;function s(o){m.hidden=!o;b.setAttribute('aria-expanded',o?'true':'false');}b.addEventListener('click',function(){s(m.hidden);});m.addEventListener('click',function(e){if(e.target.closest('a'))s(false);});document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!m.hidden){s(false);b.focus();}});})();</script>
<script src="script.js" defer></script>
</body>
</html>
'''%dict(theme=f['theme'],file=f['file'],logo=f['logo'],hlogo=f.get('hlogo',f['logo']),name=f['name'],shotsnav='<a href="#screens">Скриншоты</a>' if f.get('shots') else '',shotsmenu='<a href="#screens">Скриншоты</a>' if f.get('shots') else '',oshort=f['oshort'],
      cta_head=cta('btn-primary btn-sm','Открыть в Telegram',f['goal']),cta_hero=cta('btn-primary',f.get('cta','Открыть '+f['handle']),f['goal']),cta_final=cta('btn-primary',f.get('cta','Открыть '+f['handle']),f['goal']),
      sh=a(f.get('sh','Четыре шага до результата')),why=why,adm=adm,cab=cab,pill=a(f['pill']),h1=f['h1'],lead=a(f['lead']),note=f['note'],visual=visual,fh=a(f['fh']),cards=cards,shots=shots,steps=steps,aud=aud,
      tcls=f.get('tcls',''),startlabel=a(f.get('startlabel','Как начать')),startsec_before=startsec_before,startsec_after=startsec_after,featsec=featsec,audsec=audsec,facts=facts,startvid=startvid,headcls='head-vid' if startvid else 'sh-plain',vidjs=vidjs,points=points,tnotehtml=tnotehtml,startnote=startnote,tsoon=f.get('tsoon',''),tar=tar,tnote=a(f['tnote']),faq=faq,ft=a(f['ft']),fp=a(f['fp']),ofile=other[0],oname=a(other[1]),contacts=f.get('contacts',''))
    # RVPASS: блоки появляются при прокрутке
    for a_,b_ in [('<div class="card">','<div class="card rv">'),('<li class="step">','<li class="step rv">'),('<div class="tariff pop">','<div class="tariff pop rv">'),('<div class="tariff">','<div class="tariff rv">'),('<figure class="shot">','<figure class="shot rv">'),('<div class="sec-head">','<div class="sec-head rv">'),('<details>','<details class="rv">'),('<div class="final">','<div class="final rv">')]:
        body=body.replace(a_,b_)
    body=body.replace('<script src="script.js" defer></script>','<script src="script.js" defer></script>\n<script src="page.js" defer></script>'+('\n'+vidjs if vidjs else ''))
    out=head+'\n'+body
    for fn in ('bot.css','page.js','script.js'):
        out=out.replace('"'+fn+'"','"'+fn+'?v=20261024"')
    open(cfg['file'],'w',encoding='utf-8').write(out)

TGL='https://t.me/ModexaGuardBot?start=src_site'
def cg(items,cols='g4',extra=''):
    return '<div class="grid %s"%s>%s</div>'%(cols,extra,''.join('<div class="card">%s<h3>%s</h3><p>%s</p></div>'%(ic(i),a(t),a(p)) for i,t,p in items))
OFER='https://telegra.ph/Publichnaya-oferta-na-ispolzovanie-Telegram-bota-Modexa-10-15'
POLIT='https://telegra.ph/Politika-konfidencialnosti-Modexa-10-15'
mod=dict(file='bot-moderation.html',theme='modexa',name='Modexa',handle='@ModexaGuardBot',tg=TGL,goal='bot_moderation_open',
 cta='Подключить бесплатно',sh='Три шага до защиты группы',
 ogtitle='Modexa — бот для Telegram-групп | ОБЪЯВЛЕНИЯ ДАГЕСТАНА',ogimg='og-bot-moderation-v3.jpg',ogalt='Modexa: чистит группу от спама и мошенников. 1 группа — бесплатно навсегда',
 meta='Telegram-бот Modexa для админов групп и каналов: антиспам с ИИ, объявления через бота, рейтинг продавцов, реклама без комиссии. 1 группа — бесплатно навсегда.',
 logo='<img src="assets/images/modexa-logo.jpg" alt="" width="34" height="34">',
 pill='Telegram-бот для админов групп и каналов',
 h1='Бот, который сам чистит группу <span class="grad">от спама и мошенников</span> и помогает зарабатывать на рекламе',
 lead='Антиспам с ИИ, объявления через бота по шаблону, рейтинг продавцов, приветствие, автопостинг и реклама без комиссии. 1 группа — бесплатно навсегда. Гарантия 7 дней на первую оплату.',
 note='<b>1 группа — бесплатно навсегда.</b>',
 points=['🤖 ИИ ловит спам, который пропускают обычные фильтры','📝 Объявления только через бота — спамерам негде писать','🛡 Не понравится за 7 дней — вернём деньги'],
 visual='''<div class="mfeed" role="img" aria-label="Пример: в группе объявлений бот удаляет спам, а обычные объявления остаются">
<div class="mf-head"><span class="mf-shield"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M8.5 12l2.5 2.5 4.5-5"/></svg></span><div><b>Барахолка · пример группы</b><small>защищает Modexa</small></div></div>
<div class="mf-body">
<div class="mf-msg m1"><b>Хадижат</b>Платье вечернее, размер 44 — <i>3 500 ₽</i><em>👍 12 сделок, жалоб 0</em></div>
<div class="mf-msg mf-spam m2"><b>Анна Работа</b><span>Подработка, пиши в личку</span><u>🛡 удалено ботом</u></div>
<div class="mf-msg m3"><b>Арсен</b>Велосипед горный, 26 дюймов — <i>8 000 ₽</i></div>
<div class="mf-msg mf-spam m4"><b>Курьер Про</b><span>Курьеры до 6000 ₽ в день, жми ссылку</span><u>🛡 удалено ботом</u></div>
<div class="mf-msg m5"><b>Магомед</b>Продам диван, почти новый — <i>12 000 ₽</i></div>
</div></div>''',
 facts=[('0 ₽','1 группа, навсегда'),('0%','комиссии с рекламы'),('7 дней','гарантия возврата'),('1 кнопка','«Быстрая настройка»')],
 fh='Что умеет бот',
 tabs=[
  dict(label='🛡 Защита',items=[
   ('shield','Капча для новичков','Кнопка «Я не бот» или пример «7 + 9 = ?».'),
   ('wand','Спам о заработке','«Подработка, пиши в личку», «курьеры до 6000 ₽», казино ловятся сами, без списков слов — по признакам. Бот читает и текст на картинках у новичков.'),
   ('globe','Ссылки на чужие сайты и каналы','Удаляются в том числе ссылки, спрятанные в QR-код на картинке. Свои сайты можно разрешить.'),
   ('ai','ИИ-модерация на русском','Работает на российских сервисах GigaChat и Yandex. Вы выбираете, что удалять: работа «в личку», казино, крипта, реклама каналов, 18+, мошенничество, наркотики, оскорбления. Можно своими словами дописать, что ещё запрещено и что разрешено. Обычные объявления «продам, пишите в лс» и настоящие вакансии ИИ не трогает.'),
   ('brain','Память спама','Бот учится на подтверждённом спаме всех групп Modexa и сразу удаляет похожие сообщения, даже если слова поменяли.'),
   ('search','Общая база мошенников','Отмеченный в одной группе мошенник получает предупреждение или бан в других.'),
   ('filter','Остальные фильтры','Общая база спамеров, защита от ботов, мат, антифлуд, дубли и лимит объявлений в сутки, ограничения для новичков, защита от наплыва ботов, ночной режим, жалобы /report, стоп-слова.'),
   ('return','«Это не спам»','Если бот ошибся, одна кнопка возвращает сообщение, а бот запоминает исключение.'),
   ('bell','Наказания и журнал','Удалить, предупреждение, мут, кик, бан или «лестница» (предупреждения → мут → бан). Журнал наказаний с кнопкой «Снять».'),
   ('bolt','Быстрая настройка в одну кнопку','«Барахолка», «Обычный чат», «Строгий режим», «Обсуждение канала».'),
   ('wand','Настроить словами','Напишите боту как помощнику: «удаляй ссылки и мат, ночью закрывай группу с 0 до 7». Бот покажет, что поменяет, и поменяет после кнопки «Применить».')]),
  dict(label='📝 Предложка',intro='Главная фишка для групп с объявлениями: объявления только через бота. Группу можно закрыть — писать в ней может только бот, и спамерам негде писать.',items=[
   ('pen','1. Подать объявление','Участник нажимает «📝 Подать объявление», бот спрашивает по шагам: описание и фото, цена, город.'),
   ('ai','2. Улучшить текст','По желанию ИИ улучшит текст объявления («✨ Улучшить текст»), продавец может вернуть свой вариант.'),
   ('filter','3. Проверка','Бот проверяет объявление фильтрами и базами мошенников и спамеров.'),
   ('send','4. Публикация','Сразу или после проверки админом — красиво, с кнопкой «💬 Написать продавцу».'),
   ('lock','Группу можно закрыть','Писать в ней может только бот.'),
   ('search','Поиск по объявлениям','Поиск по объявлениям за 2 недели.'),
   ('list','Лимит в сутки','Лимит бесплатных объявлений в сутки; сверх лимита — платное размещение.'),
   ('chart','Платное автоподнятие','Продавец платит админу (например, 100 ₽), бот каждый день поднимает объявление наверх. Цену и срок задаёт админ, деньги идут админу.')]),
  dict(label='💰 Реклама',intro='Рекламодатель открывает вашу ссылку, видит цену, присылает пост и чек. Вы жмёте одну кнопку «Оплата получена» — бот публикует, закрепляет, сам открепляет и удаляет по сроку.',items=[
   ('mega','Как проходит реклама','Рекламодатель по ссылке видит цену и условия, присылает пост, выбирает время, платит по реквизитам админа и присылает чек. Админ жмёт «✅ Оплата получена — опубликовать». Бот публикует в нужное время, закрепляет, сам открепляет и удаляет по сроку, рекламодателю присылает ссылку и через сутки отчёт.'),
   ('gift','Деньги — вам, комиссии нет','Деньги идут напрямую админу, бот комиссию не берёт (на биржах вроде Telega.in она около 20%).'),
   ('list','Каталог для рекламодателей','Одна ссылка на все группы админа — рекламодатель выбирает несколько и платит одним чеком.'),
   ('star','Рейтинг продавцов','После сделки покупатель отвечает продавцу /rep + или /rep -; под сообщениями и объявлениями видно «👍 12 сделок, жалоб 0». Рейтинг общий для всех групп Modexa, защищён от накрутки.'),
   ('users','Продвижение групп и каналов — бесплатно','Каталог Modexa — группу или канал находят по теме и городу.'),
   ('send','Взаимопиар','Раз в неделю группы и каналы одной темы и города показывают друг друга.')]),
  dict(label='📢 Каналы',intro='Для каналов и закрытых групп.',items=[
   ('lock','🚪 Заявки на вступление','Бот одобряет заявки сразу или после кнопки «Я не бот» в личке (боты её не нажимают), отказывает людям из баз спамеров и мошенников и пишет новичку приветствие в личку.'),
   ('pen','✍️ Автоподпись','К каждому посту канала бот сам дописывает подпись и кнопки («Подписаться», «Реклама»).'),
   ('clock','Автопостинг и реклама в каналах','Автопостинг и реклама без комиссии работают и в каналах.')]),
  dict(label='⚙️ Ещё',chips=['Приветствие и /rules','Автоответы','Автопостинг','Доступ за приглашение','Статистика и отчёт по понедельникам','Веб-панель в Telegram','Помощники «Менеджер» и «Модератор»','Перенос настроек между группами','«Настроим за вас»','Копии базы каждый день'])],
 vmore=4,
 vshots=[(('modexa-spam.mp4','modexa-vid-1.jpg','Видео: бот удаляет спам в группе объявлений'),'Бот удаляет спам','Спам в группе удаляется сам, обычные объявления остаются.'),
 (('modexa-predlozhka.mp4','modexa-vid-2.jpg','Видео: подача объявления через бота'),'Предложка','Как участник подаёт объявление через бота.'),
 (('modexa-reklama.mp4','modexa-vid-3.jpg','Видео: приём платной рекламы без комиссии'),'Реклама без комиссии','Заявка, чек и публикация одной кнопкой.'),
 (('modexa-podklyuchenie.mp4','modexa-vid-4.jpg','Видео: подключение бота за три шага'),'Подключение','Три шага: «Старт», «Группа», «Барахолка».'),
 (('modexa-nastroyka.mp4','modexa-vid-5.jpg','Видео: быстрая настройка в одну кнопку'),'Быстрая настройка','Одна кнопка — и защита включена.'),
 (('modexa-ii.mp4','modexa-vid-6.jpg','Видео: ИИ-модерация'),'ИИ-модерация','Вы выбираете, что удалять, ИИ читает сообщения на русском.'),
 (('modexa-reyting.mp4','modexa-vid-7.jpg','Видео: рейтинг продавцов'),'Рейтинг продавцов','После сделки покупатель отвечает /rep +.'),
 (('modexa-kanaly.mp4','modexa-vid-8.jpg','Видео: каналы и закрытые группы'),'Каналы и закрытые группы','Заявки на вступление и автоподпись под постами.'),
 (('modexa-slovami.mp4','modexa-vid-9.jpg','Видео: настроить словами'),'Настроить словами','Напишите боту, что нужно, и нажмите «Применить».')],
 shots=[('modexa-groups.jpg','Мои группы и каналы','Все подключённые группы в одном списке: ✅ — лицензия активна.',0,0),
 ('modexa-filters.jpg','Фильтры и наказания','Каждый фильтр включается отдельно: ✅ — работает, ⏸ — выключен. У каждого своё наказание.',0,0),
 ('modexa-panel-stats.jpg','Статистика в веб-панели','Участники, рост, вступившие и вышедшие, сообщения по дням.',0,0)],
 why=[('ai','ИИ-модерация на русском','Работает на российских сервисах GigaChat и Yandex.'),
 ('pen','Предложка','Объявления только через бота — по шаблону и с проверкой.'),
 ('star','Рейтинг продавцов','Общий для групп Modexa, защищён от накрутки.'),
 ('mega','Реклама без комиссии','Деньги идут напрямую админу, бот процент не берёт.'),
 ('return','Гарантия 7 дней','Первую оплату вернём без объяснений.'),
 ('key','3 группы за 250 ₽','Тариф «Подписка»: до 3 групп за 250 ₽ в месяц.')],
 whycls='g3',
 steps=['Откройте <a href="%s" rel="noopener" target="_blank">@ModexaGuardBot</a> и нажмите «Старт».'%TGL,'Нажмите «➕ Группа», выберите свою группу и оставьте боту права администратора (удаление сообщений и блокировка участников).','Выберите тип группы («Барахолка», «Обычный чат»…) — защита включится одной кнопкой. Первая группа сразу получает бесплатный тариф.'],
 startnote='Подключить группу может только её создатель. Если бота добавил другой админ, создатель пишет в группе <code>/connect</code>.',
 aud=[('Барахолки и доски объявлений','Главная аудитория бота — в первую очередь Дагестан.'),('Городские и районные чаты','Защита от спама и мошенников без круглосуточного дежурства.'),('Каналы с обсуждениями и сообщества','Автопостинг и реклама работают в каналах, модерация — в группах и обсуждениях.')],
 tcls='t3',
 tariffs=[('🆓 Бесплатный','0 ₽',' навсегда','1 группа или канал. Капча, защита от ботов, ссылки, антифлуд, мат, спам о заработке, память спама, ИИ-модерация (до 100 проверок в сутки), рейтинг продавцов, приветствие (с подписью бота), каталог и взаимопиар.',False),
 ('🔁 Подписка','250 ₽',' в месяц','До 3 групп и каналов. Всё.',False),
 ('🗓 На год','2490 ₽',' в год','До 7 групп и каналов. Всё — выгоднее помесячной (вместо 3000 ₽, экономия 510 ₽).',True),
 ('🎁 Пробный','0 ₽',' 7 дней, один раз','1 группа. Вся модерация, приветствие, статистика, предложка.',False),
 ('🌐 Сеть','4990 ₽',' в год','До 20 групп и каналов. Всё — для админов сетей групп по районам и городам.',False),
 ('💎 Навсегда','6990 ₽',' один раз','До 10 групп и каналов. Всё, без ежемесячной оплаты — дешевле трёх лет на годовом (7470 ₽), дальше бесплатно.',False)],
 tmore=3,faqmore=6,noaud=True,
 badge='Выгоднее',
 tnote='',
 tlist='''<div class="acc-list tl">
<details class="acc"><summary><span class="acc-t">Что есть только на платных тарифах</span></summary><p>Предложка, автопостинг, реклама, автоответы, доступ за приглашения, база мошенников и спамеров, все фильтры, более умный ИИ с двойной проверкой, приветствие без подписи бота.</p></details>
<details class="acc"><summary><span class="acc-t">Оплата и гарантия 7 дней</span></summary><p>Оплата картой или через СБП прямо в боте (ЮKassa), тариф включается сразу. Можно переводом по реквизитам со скриншотом чека. Гарантия: первую оплату вернём без объяснений — кнопкой в боте или командой /refund. Один раз на человека и группу. Следующие оплаты можно вернуть в течение 3 дней.</p></details>
<details class="acc"><summary><span class="acc-t">Промокоды, партнёрка и бонусы</span></summary><p>Есть промокоды. После пробного периода — личный промокод со скидкой 20%. Партнёрка: 20% с оплат приглашённых админов деньгами (вывод от 500 ₽) и +7 дней подписки. Отзыв через неделю — +7 дней подписки.</p></details>
</div>
<p class="note">Оплата проходит только в боте. Документы: <a href="@O@" rel="noopener" target="_blank">публичная оферта</a> · <a href="@P@" rel="noopener" target="_blank">политика конфиденциальности</a>.</p>
<p style="margin-top:16px"><a class="btn btn-primary" href="@T@" rel="noopener" target="_blank" data-goal="bot_moderation_open">@G@Подключить бесплатно</a></p>'''.replace('@O@',OFER).replace('@P@',POLIT).replace('@T@',TGL).replace('@G@',TG),
 faq=[('Это правда бесплатно?','Да, одна группа бесплатно навсегда, с ИИ. В приветствии будет маленькая подпись бота.'),
 ('Бот будет удалять обычные сообщения?','Нет. Каждый фильтр включается отдельно, админов бот не трогает. Обычные объявления «продам, пишите в лс» и настоящие вакансии ИИ не трогает. Ошибся — кнопка «Это не спам» вернёт сообщение, а надёжных участников можно добавить в белый список командой /trust.'),
 ('Что такое предложка?','Объявления через бота по шаблону: описание, фото, цена, город, кнопка «Написать продавцу». Группу можно закрыть от спамеров.'),
 ('Как ИИ понимает, что удалять?','Вы выбираете категории и можете своими словами написать, что запрещено и что разрешено. Тексты проверяют российские сервисы GigaChat и Yandex.'),
 ('Сложно настроить?','Одна кнопка «Быстрая настройка». Или напишите боту словами, что нужно, или нажмите «Настроим за вас».'),
 ('Как оплатить?','Картой или СБП в боте, тариф включится сразу. Или переводом с чеком.'),
 ('Можно вернуть деньги?','Первую оплату — 7 дней без объяснений. Следующие — 3 дня.'),
 ('Нужно что-то устанавливать?','Нет, всё работает в Telegram: меню бота и веб-панель внутри Telegram.'),
 ('Можно дать доступ помощнику?','Да, с ролью «Менеджер» (все настройки) или «Модератор» (только модерация).'),
 ('Подходит для каналов?','Да: автопостинг, реклама без комиссии, автоподпись под постами, заявки на вступление, каталог и взаимопиар. Модерация — в группах и в чате комментариев.'),
 ('Бот берёт процент с рекламы?','Нет. Деньги за рекламу и автоподнятие идут вам.'),
 ('Сколько групп можно подключить?','Бесплатно 1, подписка 3, год 7, «Сеть» 20, навсегда 10.')],
 ft='Подключите группу бесплатно',fp='Первая группа — бесплатно навсегда. Гарантия 7 дней на первую оплату.',oshort='КлиентРадар',other=('bot-crm.html','КлиентРадар — заявки от клиентов'),
 contacts='<span>Поддержка: <a href="https://t.me/Abdylzhelil05" rel="noopener" target="_blank">@Abdylzhelil05</a> · вопросы по оплате — команда /paysupport в боте</span><span>Самозанятый Раджабов Абдулжелил Маликович, ИНН 053004641154</span><span>Документы Modexa: <a href="%s" rel="noopener" target="_blank">оферта</a> · <a href="%s" rel="noopener" target="_blank">политика</a></span>'%(OFER,POLIT))

SVG_RADAR='''<div class="radar"><svg viewBox="0 0 200 200" role="img" aria-label="Радар заявок"><defs><radialGradient id="rg" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#4CC3FF" stop-opacity=".22"/><stop offset="1" stop-color="#4CC3FF" stop-opacity="0"/></radialGradient><linearGradient id="sw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4CC3FF" stop-opacity="0"/><stop offset="1" stop-color="#4CC3FF" stop-opacity=".55"/></linearGradient></defs>
<circle cx="100" cy="100" r="95" fill="url(#rg)"/>
<circle class="ring" cx="100" cy="100" r="96"/><circle class="ring" cx="100" cy="100" r="66"/><circle class="ring" cx="100" cy="100" r="36"/>
<path class="ring" d="M100 4v192M4 100h192"/>
<path class="ring tick" d="M186.9 123.3L190.8 124.3M177.9 145.0L181.4 147.0M163.6 163.6L166.5 166.5M145.0 177.9L147.0 181.4M123.3 186.9L124.3 190.8M76.7 186.9L75.7 190.8M55.0 177.9L53.0 181.4M36.4 163.6L33.5 166.5M22.1 145.0L18.6 147.0M13.1 123.3L9.2 124.3M13.1 76.7L9.2 75.7M22.1 55.0L18.6 53.0M36.4 36.4L33.5 33.5M55.0 22.1L53.0 18.6M76.7 13.1L75.7 9.2M123.3 13.1L124.3 9.2M145.0 22.1L147.0 18.6M163.6 36.4L166.5 33.5M177.9 55.0L181.4 53.0M186.9 76.7L190.8 75.7"/>
<g class="sweep"><path d="M100 100L100 4A96 96 0 0 1 167.9 32.1Z" fill="url(#sw)"/><path d="M100 100L167.9 32.1" stroke="#7BD8FF" stroke-width="1.2" stroke-linecap="round" fill="none"/></g>
<circle class="rd-ping" cx="123.9" cy="55.0" r="5.2" style="animation-delay:-0.24s"/><circle class="rd-blip" cx="123.9" cy="55.0" r="4.2" style="animation-delay:-0.24s"/><circle class="rd-ping" cx="171.5" cy="62.0" r="4.4" style="animation-delay:-4.76s"/><circle class="rd-blip" cx="171.5" cy="62.0" r="3.4" style="animation-delay:-4.76s"/><circle class="rd-ping" cx="119.9" cy="109.3" r="4.2" style="animation-delay:-4.03s"/><circle class="rd-blip" cx="119.9" cy="109.3" r="3.2" style="animation-delay:-4.03s"/><circle class="rd-ping" cx="134.1" cy="137.9" r="5.2" style="animation-delay:-3.71s"/><circle class="rd-blip" cx="134.1" cy="137.9" r="4.2" style="animation-delay:-3.71s"/><circle class="rd-ping" cx="127.7" cy="176.1" r="4.4" style="animation-delay:-3.40s"/><circle class="rd-blip" cx="127.7" cy="176.1" r="3.4" style="animation-delay:-3.40s"/><circle class="rd-ping" cx="68.6" cy="140.2" r="4.8" style="animation-delay:-2.60s"/><circle class="rd-blip" cx="68.6" cy="140.2" r="3.8" style="animation-delay:-2.60s"/><circle class="rd-ping" cx="23.9" cy="127.7" r="5.0" style="animation-delay:-2.15s"/><circle class="rd-blip" cx="23.9" cy="127.7" r="4.0" style="animation-delay:-2.15s"/><circle class="rd-ping" cx="84.4" cy="84.4" r="4.2" style="animation-delay:-1.25s"/><circle class="rd-blip" cx="84.4" cy="84.4" r="3.2" style="animation-delay:-1.25s"/><circle class="rd-ping" cx="53.5" cy="33.6" r="4.6" style="animation-delay:-1.11s"/><circle class="rd-blip" cx="53.5" cy="33.6" r="3.6" style="animation-delay:-1.11s"/><circle class="rd-ping" cx="53.8" cy="78.4" r="4.4" style="animation-delay:-1.53s"/><circle class="rd-blip" cx="53.8" cy="78.4" r="3.4" style="animation-delay:-1.53s"/>
<circle cx="100" cy="100" r="5" fill="#4CC3FF"/><circle cx="100" cy="100" r="9" fill="none" stroke="#4CC3FF" stroke-opacity=".35"/></svg></div>'''
crm=dict(file='bot-crm.html',theme='radar',name='КлиентРадар',handle='@klientradarbot',tg='https://t.me/klientradarbot?start=src_site',goal='bot_crm_open',
 logo='<span class="ic" style="width:34px;height:34px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(135deg,#4CC3FF,#3B82F6);color:#031321"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><path d="M12 12l6-6"/></svg></span>',
 hlogo='<img class="brand-logo" src="assets/images/logo-klientradar.svg?v=2" alt="" width="40" height="40">',
 meta='КлиентРадар — Telegram-бот находит заявки от клиентов в группах: 75 ниш, ИИ-проверка, ответ в один клик, CRM. Бесплатно: до 5 заявок в день.',
 pill='Telegram-бот для продаж',h1='Находит <span class="grad">заявки от клиентов</span> в Telegram',
 lead='КлиентРадар ищет людей, которым нужна ваша услуга, в Telegram-группах и каналах, присылает заявки и помогает вести клиентов — от первого сообщения до оплаты.',
 note='<b>Бесплатно:</b> до 5 заявок в день с задержкой 30 минут. Новым — 3 дня 💎 бесплатно. Выберите ниши и город — и сразу получите заявки за сутки.',
 visual=SVG_RADAR,fh='Что внутри',
 startfirst=True,seyebrow='Как это работает',startlabel='Как это работает',sh='Три шага до первых заявок',
 features=[('search','75 готовых ниш','И поиск ниши по слову. Выберите свою нишу и город — остальное бот сделает сам.'),
 ('filter','Без лишнего мусора','Бот сам отсеивает рекламу мастеров, вакансии и спам.'),
 ('shield','Подсказка о возможной схеме','Если в заявке просят предоплату, перевод, оплату в крипте, код из СМС или зовут на сторонний сайт, бот пишет «⚠️ Осторожно, возможна схема» и называет причину. Это помогает заметить признаки обмана, но не гарантирует защиту.'),
 ('list','Заявки по одной','Выберите нишу и место (Дагестан, Махачкала, Москва…) и листайте «Предыдущая / Следующая».'),
 ('send','Ответ в один клик','Скопируйте готовый текст с вашими ценами и ответьте в группе. Бот сам клиентам не пишет — пишете вы.'),
 ('chart','Мини-CRM','Этапы сделки, заметки и напоминания — чтобы не терять клиентов.'),
 ('bell','«Не беспокоить» и «Тишина»','Паузу на час, день или неделю можно включить в любой момент, а ночью бот молчит. Заявки не пропадают.'),
 ('users','Приглашения','Друг заходит по вашей ссылке — вам обоим +7 дней полного тарифа.'),
 ('msg','«Сообщить о проблеме»','Кнопка прямо в боте: если что-то не так, напишите, и вам ответят.')],
 shots=[(None,'Карточка заявки','Заявка с кнопками «Скопировать ответ», «В работу», «Отложить».',0,0),
 (None,'Тариф','Цены и оплата в боте.',0,0),
 (None,'Рейтинг в закрепе группы','Рейтинг заявок по нишам и кнопки ниш.',0,0),
 (None,'Кабинет','Заявки, клиенты и тариф в одном окне.',0,0),
 ('radar-start.jpg','Знакомство с ботом','Что умеет бот и кнопка «Запустить»: настройка занимает около 30 секунд.',0,0),
 ('radar-cabinet.jpg','Кабинет в Telegram','Заявки, клиенты, профиль и тариф в одном окне. Вход без пароля — по аккаунту Telegram.',0,0),
 ('radar-profile.jpg','Автонастройка профиля','Бот сам подставит режим тишины и минус-слова, ниши выбираются касанием.',0,0),
 ('radar-catalog.jpg','Каталог групп','Добавьте свою группу: бонусные дни за заявки из неё, уровни и рейтинг.',0,0),
 ('radar-stages.jpg','CRM: этапы сделки','Новый, в переговорах, думает, оплата, выполнено, отказ — клиенты по этапам, поиск и добавление.',0,0),
 ('radar-clients.jpg','CRM в кабинете','Поиск по имени или @нику и этапы сделки в мини-приложении.',0,0),
 ('radar-commands.jpg','Меню команд','Кабинет, заявки, CRM, каталог, условия оплаты, политика и удаление данных — всё под рукой.',0,0)],
 cabinet=('📱 Кабинет в Telegram','Заявки, клиенты, профиль, тариф, статистика и кредиты — в одном окне прямо в Telegram. Вход без пароля.'),
 steps=['Откройте <a href="https://t.me/klientradarbot?start=src_site" rel="noopener" target="_blank">@klientradarbot</a>, нажмите «Старт» и выберите свою нишу и город.','Бот сам находит в Telegram-группах людей, которые ищут исполнителя, и присылает вам их заявки.','Пишите им первым: скопируйте готовый ответ и отправьте его в группе или в личку.'],
 startnote='Заявки из групп Дагестана и соседних регионов приходят в первую очередь, потом из остальной России.',
 aud=[('Мастера и специалисты','Электрики, мастера по ремонту, репетиторы, фотографы — те, кому нужны новые клиенты.'),('Агентства и студии','Недвижимость, сайты, реклама, юристы: ловите запросы в момент, когда человек ищет исполнителя.'),('Магазины и небольшой бизнес','Находите покупателей в городских группах и ведите их до оплаты в одной CRM.')],
 tariffs=[('Бесплатный','0 ₽','','До 5 заявок в день с задержкой 30 минут. Своя CRM, ниши и город. Новым — 3 дня 💎 бесплатно (один раз), за день до конца бот напомнит.',False),
 ('💎 Полный · 30 дней','490 ₽','','Все заявки сразу и без лимита.',False),
 ('💎 Полный · 90 дней','1290 ₽','','Все заявки сразу и без лимита.',False),
 ('💎 Полный · 365 дней','3990 ₽','','Все заявки сразу и без лимита.',False)],
 admins=('Для администраторов групп','<div class="acc-list"><details class="acc" open><summary><span class="acc-t">Рейтинг заявок в закрепе</span></summary><p style="padding-left:0">Добавьте @klientradarbot в свою группу админом (с правом закреплять сообщения) — в закрепе появится рейтинг заявок вашего города и кнопки ниш. Ничего другого бот в группе не публикует; выключить рейтинг можно командой /rating off.</p></details><details class="acc"><summary><span class="acc-t">20% кредитами с оплат участников</span></summary><p style="padding-left:0">С оплат участников, пришедших из вашей группы, вам 20% в кредитах (1 кредит = 1 ₽ внутри бота). Их можно обменять на дни полного тарифа или на бота модерации для вашей группы. Деньгами кредиты не выводятся. Первые 3 дня после оплаты участника (срок возврата) кредиты заморожены, потом доступны.</p></details><details class="acc"><summary><span class="acc-t">Каталог групп</span></summary><p style="padding-left:0">Добавьте группу в каталог: +1 день 💎 за каждые 5 заявок из неё, а заявки из своей группы приходят вам всегда, даже сверх лимита. Для защиты группы есть отдельный бот <a class="promo-link" style="color:var(--accent);font-weight:700" href="bot-moderation.html">Modexa</a>.</p></details></div><p style="margin-top:18px"><a class="btn btn-primary" href="https://t.me/klientradarbot?startgroup=rating&amp;admin=pin_messages" rel="noopener" target="_blank" data-goal="bot_crm_group">'+TG+'Поставить бота в группу</a></p>'),
 contacts='<span>Контакты: <a href="https://t.me/Abdylzhelil05" rel="noopener" target="_blank">@Abdylzhelil05</a> · <a href="mailto:abdulzelilradzabov879@gmail.com">abdulzelilradzabov879@gmail.com</a></span>',
 tnote='Оплата в боте: картой или по СБП, возврат в течение 3 дней. Автопродление по желанию, карту можно отвязать одной кнопкой. Гарантия: если за неделю пришло меньше 10 заявок, бот сам добавит 7 дней.',
 tsoon='<p style="margin-top:16px"><a class="btn btn-primary" href="https://t.me/klientradarbot?start=src_site" rel="noopener" target="_blank" data-goal="bot_crm_pay">'+TG+'Оплатить в боте</a></p><p class="note">Откройте бота и выберите «Профиль» → «💎 Тариф»: оплата проходит прямо в Telegram.</p>',
 faq=[('Откуда берутся заявки?','Бот читает открытые Telegram-группы и группы, куда его добавили, и присылает сообщения людей, которые ищут исполнителя, — по вашей нише и городу. В группах бот пишет только рейтинг заявок в закрепе — и только если админ дал ему это право.'),
 ('Бот пишет клиентам?','Нет. Бот сам клиентам не пишет: вы копируете готовый ответ и отвечаете сами — в группе или в личку.'),
 ('Бот собирает данные людей?','Бот не собирает номера телефонов и закрытые переписки. Из открытых сообщений сохраняется текст заявки, имя и публичный ник автора — не дольше 90 дней. Удалить свои данные можно командой /deleteme; автор сообщения в группе может написать @Abdylzhelil05, и его данные удалят. Текст сообщения (без имени, ника и ID автора) может проверяться ИИ GigaChat (Сбер), чтобы отсеять рекламу и спам.'),
 ('Сколько стоит полный тариф?','Полный тариф 💎: все заявки сразу и без лимита — 490 ₽ на 30 дней, 1290 ₽ на 90 дней и 3990 ₽ на год. Бесплатно: до 5 заявок в день с задержкой 30 минут. Новым — 3 дня 💎 бесплатно. Оплата картой или по СБП, возврат в течение 3 дней.'),
 ('Что если заявок будет мало?','Если за неделю пришло меньше 10 заявок, бот сам добавит 7 дней. Деньгами это не компенсируется. Конкретное число заявок мы не обещаем: оно зависит от ниши и города.'),
 ('Можно отключить автопродление?','Автопродление включается по желанию. Привязанную карту можно отвязать одной кнопкой: «💎 Тариф» → «🗑 Отвязать карту».'),
 ('Что получает админ группы?','В закрепе группы появится рейтинг заявок вашего города и кнопки ниш. С оплат участников, пришедших из вашей группы, вам 20% в кредитах (1 кредит = 1 ₽ внутри бота): их можно обменять на дни полного тарифа или на бота модерации. Деньгами кредиты не выводятся.'),
 ('Как выбрать, какие заявки получать?','При старте вы выбираете нишу и город. Слова, минус-слова, режим «Тишина» и «Не беспокоить» настраиваются в боте.'),
 ('Можно ли передать заявку коллеге?','Да, кнопка «📨 Коллеге» на карточке заявки отправляет её другому пользователю бота.')],
 oshort='Modexa',ft='Начните получать заявки',fp='Выберите ниши и город — первые заявки придут сразу.',other=('bot-moderation.html','Modexa — модерация для вашей группы'))
_args=sys.argv[1:] or ['modexa']
if 'modexa' in _args: page(mod)
if 'crm' in _args: page(crm)
