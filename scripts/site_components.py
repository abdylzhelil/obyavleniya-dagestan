"""Shared accessible bot navigation and screenshot region."""
CATS=[('avto','Автомобили'),('nedvizhimost','Недвижимость'),('tehnika','Техника'),('odezhda','Одежда'),('uslugi','Услуги'),('rabota','Работа'),('tovary','Товары'),('raznoe','Разное')]
def enhance_bot(s):
    s=s.replace('<div class="shots">','<div class="shots" tabindex="0" role="region" aria-label="Скриншоты бота. Прокрутка клавишами влево и вправо">')
    if 'class="bh-site-sections"' not in s:
        sections='<div class="bh-site-sections"><a href="index.html#groups">Наши группы</a><details><summary>Категории</summary>'+''.join('<a href="%s-dagestan.html">%s</a>'%(slug,name) for slug,name in CATS)+'</details><a href="reklama.html">Реклама и цены</a><a href="index.html#rules">Правила групп</a><a href="index.html#contact">Контакты администратора</a></div>'
        s=s.replace('</div></div>\n</header>',sections+'</div></div>\n</header>',1)
    s=s.replace("m.hidden=!o;b.setAttribute", "m.hidden=!o;document.documentElement.style.setProperty('--bot-menu-top',Math.ceil(b.closest('header').getBoundingClientRect().bottom)+'px');b.setAttribute")
    if "b.setAttribute('aria-label',o?" not in s: s=s.replace("b.setAttribute('aria-expanded',o?'true':'false');","b.setAttribute('aria-expanded',o?'true':'false');b.setAttribute('aria-label',o?'Закрыть меню':'Меню');if(o)m.scrollTop=0;")
    return s
