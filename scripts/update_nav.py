"""Единое меню и подвал на всех страницах сайта (запуск из корня репозитория)."""
import re,glob
CATS=[('avto-dagestan','Автомобили'),('nedvizhimost-dagestan','Недвижимость'),('tehnika-dagestan','Техника'),('odezhda-dagestan','Одежда'),('uslugi-dagestan','Услуги'),('rabota-dagestan','Работа'),('tovary-dagestan','Товары'),('raznoe-dagestan','Разное')]
def nav_inner(home):
    p='' if home else 'index.html'
    cats=''.join('<a href="%s.html">%s</a>'%(s,n) for s,n in CATS)
    return f'''
      <a href="index.html">Главная</a>
      <a href="{p}#groups">Наши группы</a>
      <div class="nav-dd dd-cats"><a href="{p}#categories">Категории</a><div class="dd-menu">{cats}</div></div>
      <a href="{p}#rules">Правила</a>
      <a href="{p}#advertising">Реклама</a>
      <div class="nav-dd dd-bots"><a href="{p}#bots">Боты</a><div class="dd-menu"><a href="bot-moderation.html">Modexa</a><a href="bot-crm.html">КлиентРадар</a></div></div>
      <a href="#contact">Контакты</a>
    '''
def foot_cats():
    cats=''.join('<a href="%s.html">%s</a>'%(s,n) for s,n in CATS)
    return '    <nav class="footer-cats" aria-label="Категории объявлений"><span>Категории:</span>'+cats+'</nav>\n    '
pages=['index.html','group.html','privacy.html','reklama.html']+[s+'.html' for s,_ in CATS]
for f in pages:
    t=open(f,encoding='utf-8').read()
    t,n=re.subn(r'(<nav class="nav-links" id="site-nav"[^>]*>).*?(</nav>)',lambda m:m.group(1)+nav_inner(f=='index.html')+'    '+m.group(2),t,count=1,flags=re.S); assert n==1,f
    # footer links: ensure bots present
    if 'bot-moderation.html">Modexa</a>\n        <a href="bot-crm' not in t.split('footer-links')[1].split('</nav>')[0]:
        t=t.replace('<a href="#contact" data-contact="telegram" data-goal="ad_contact_telegram">Контакты</a>\n      </nav>','<a href="bot-moderation.html">Modexa</a>\n        <a href="bot-crm.html">КлиентРадар</a>\n        <a href="#contact" data-contact="telegram" data-goal="ad_contact_telegram">Контакты</a>\n      </nav>',1)
    if 'footer-cats' not in t:
        t=t.replace('<div class="footer-bottom">',foot_cats()+'<div class="footer-bottom">',1)
    else:
        t=re.sub(r'<nav class="footer-cats".*?</nav>\n    ',lambda m: foot_cats(),t,count=1,flags=re.S)
    open(f,'w',encoding='utf-8').write(t); print('ok',f)
# 404
t=open('404.html',encoding='utf-8').read()
links='<p class="nf-links">'+''.join('<a href="/%s.html">%s</a>'%(s,n) for s,n in CATS)+'<a href="/bot-moderation.html">Modexa</a><a href="/bot-crm.html">КлиентРадар</a></p>'
if 'nf-links' not in t:
    t=t.replace('<p><a class="promo-link" href="/">Перейти на главную страницу</a></p>','<p><a class="promo-link" href="/">Перейти на главную страницу</a></p>\n          <p>Или выберите раздел:</p>\n          '+links)
    open('404.html','w',encoding='utf-8').write(t)
