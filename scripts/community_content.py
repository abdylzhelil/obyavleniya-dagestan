"""Shared static content for category pages and offer placement."""
from html import escape
from urllib.parse import quote
ADMIN_BENEFITS = [
 "Админство своей категории.",
 "Закрепление категории за вами на месяц.",
 "Публикация своих объявлений в своей категории в течение месяца.",
 "Удаление неактуальных и неподходящих объявлений.",
 "Контроль порядка публикаций в своей категории.",
 "Один статус группы в день — бесплатно для админа категории.",
 "Дополнительное доверие участников группы."
]
def admin_offer(category=None, detailed=False, anchor=None):
 title = "Стать админом категории" if not category else "Стать админом категории «" + category + "»"
 message = "Здравствуйте! Хочу стать админом " + ("категории «" + category + "»" if category else "категории в группе") + " за 850 ₽ в месяц. Подскажите доступность категории и условия."
 href = "https://wa.me/79637968587?text=" + quote(message)
 benefits = ADMIN_BENEFITS if detailed else [ADMIN_BENEFITS[1], ADMIN_BENEFITS[2], ADMIN_BENEFITS[5]]
 ident = ' id="' + escape(anchor, quote=True) + '"' if anchor else ''
 return ('<section class="community-admin"' + ident + '><div class="community-admin-heading"><div><p class="community-eyebrow">Админство внутри группы</p><h2>' + escape(title) + '</h2></div><p class="community-admin-price">850 ₽<span>/ месяц</span></p></div><p>Получите свою категорию в группе и занимайтесь её развитием.</p><ul>' + ''.join('<li>' + escape(item) + '</li>' for item in benefits) + '</ul><p class="community-admin-note">Группу, доступность категории и условия согласуйте с главным администратором перед оплатой.</p><div class="community-admin-actions"><a class="btn btn-wa" href="' + escape(href, quote=True) + '" target="_blank" rel="noopener" data-goal="ad_contact_whatsapp">' + ('Обсудить эту категорию' if category else 'Написать о категории') + '</a><a class="community-admin-details" href="reklama.html#category-admin">Полные условия админства</a></div></section>')
