/* ==========================================================================
   ОБЪЯВЛЕНИЯ ДАГЕСТАНА — script.js
   Один файл для index.html, group.html и privacy.html.
   Разделы:
     1. Настройки сайта (SITE)
     2. Данные: группы (GROUPS) и правила (RULES)
     3. Вспомогательные функции
     4. Отрисовка: главная страница
     5. Отрисовка: страница группы и SEO (мета-теги, canonical, JSON-LD)
     6. Интерфейс: меню и анимация появления
     7. Ссылки и аналитика
     8. Уведомление о cookie
     9. Запуск
   ========================================================================== */
"use strict";

/* ---------- 1. Настройки сайта ---------- */
const SITE = {
  siteName: "ОБЪЯВЛЕНИЯ ДАГЕСТАНА",

  /* Адрес сайта без слэша в конце. Из него собираются canonical, og:url, og:image и адреса в JSON-LD. */
  baseUrl: "https://obyavleniya-dagestan.ru",

  homeUrl: "index.html",
  privacyUrl: "privacy.html", /* страница политики конфиденциальности */
  groupPageUrl: "group.html", /* совместимость со старыми ссылками ?id; новые адреса создаёт getGroupPageHref */

  /* Картинки для SEO (пути от корня сайта; абсолютные адреса собираются из baseUrl) */
  ogImage: "assets/brand/og-community.jpg",
  logo: "assets/brand/whatsapp.webp",

  adContacts: {
    telegram: "@Abdylzhelil05",
    whatsapp: "+79637968587"
  },

  /* Номер счётчика Яндекс Метрики. Тот же номер указан в коде счётчика в index.html и group.html.
     Если поставить null, цели перестанут отправляться. */
  metrikaId: 113403438
};

/* ---------- 2. Данные ---------- */

/* Единственный источник данных о группах.
   status: "open" — идёт набор, "full" — группа заполнена (вступление закрыто).
   number: номер группы WhatsApp; только у пронумерованных групп показывается бейдж статуса.
   shortText: короткий текст для карточки в блоке «Две группы в WhatsApp».
   admin.name — необязательно: если пусто, выводится только контакт.
   Чтобы добавить группу, добавьте сюда новый объект. */
const GROUPS = [
  {
    id: "telegram-main",
    order: 1,
    platform: "telegram",
    status: "open",
    name: "ОБЪЯВЛЕНИЯ ДАГЕСТАНА",
    description: "Объявления и реклама по Республике Дагестан. Пересылки, харам и сообщения не по теме запрещены. Из ссылок разрешены только конкретные товары или объявления на Авито. Реклама платная.",
    membersLabel: "менее 3 000 участников",
    categories: ["Автомобили", "Недвижимость", "Техника", "Одежда", "Услуги", "Работа"],
    whatIsPosted: "Объявления и реклама по Республике Дагестан: покупка, продажа, услуги и другие предложения участников.",
    admin: { contact: "@Abdylzhelil05" },
    link: "https://t.me/AvitoDag05_reklama_group",
    logo: "assets/brand/telegram.webp"
  },
  {
    id: "whatsapp-main",
    order: 2,
    platform: "whatsapp",
    number: 1,
    status: "full",
    name: "ОБЪЯВЛЕНИЯ ДАГЕСТАНА",
    description: "Покупка, продажа, услуги и работа для жителей Дагестана. Группа работает с 08:00 до 22:00, обычные объявления участников — бесплатно.",
    membersLabel: "Группа заполнена",
    shortText: "Группа заполнена. Новые участники сюда больше не добавляются.",
    categories: ["Автомобили", "Недвижимость", "Техника", "Одежда", "Услуги", "Работа"],
    whatIsPosted: "Обычные объявления участников (бесплатно в часы работы группы) и платная реклама — каналы, соцсети, сайты и сторонние площадки.",
    admin: { name: "Главный администратор", contact: "+79637968587" },
    link: "https://chat.whatsapp.com/KA9KJ5Gt9W4Lb0HZkn7VvT?s=cl&p=a&mlu=4&ilr=4",
    logo: "assets/brand/whatsapp.webp"
  },
  {
    id: "whatsapp-2",
    order: 3,
    platform: "whatsapp",
    number: 2,
    status: "open",
    name: "ОБЪЯВЛЕНИЯ ДАГЕСТАНА — группа №2",
    description: "Новая группа в WhatsApp: идёт активный набор участников. Покупка, продажа, услуги и работа для жителей Дагестана.",
    membersLabel: "Новая группа · идёт набор",
    shortText: "Новая группа. Идёт активный набор участников — вступайте и публикуйте объявления.",
    categories: ["Автомобили", "Недвижимость", "Техника", "Одежда", "Услуги", "Работа"],
    whatIsPosted: "Обычные объявления участников и платная реклама — по правилам группы.",
    admin: { name: "Главный администратор", contact: "+79637968587" },
    link: "https://chat.whatsapp.com/EisxSK0qarkJzyrlt9v1fx",
    logo: "assets/brand/whatsapp.webp"
  }
];

const ADMIN_CATEGORY_BENEFITS = [
  "Админство своей категории.",
  "Закрепление категории за вами на месяц.",
  "Публикация своих объявлений в своей категории в течение месяца.",
  "Удаление неактуальных и неподходящих объявлений.",
  "Контроль порядка публикаций в своей категории.",
  "Один статус группы в день — бесплатно для админа категории.",
  "Дополнительное доверие участников группы."
];

const RULES = [
  "Группа открывается в 08:00 и закрывается в 22:00.",
  "Обычные объявления участников — бесплатно в часы работы группы.",
  "Пересылки, харам и сообщения не по теме запрещены.",
  "Сторонние ссылки запрещены. Исключение — ссылки на конкретные товары или объявления на Авито.",
  "Реклама каналов, групп, соцсетей, сайтов, онлайн-сервисов и сторонних площадок размещается только платно, по согласованию с администратором.",
  "Участникам запрещено самостоятельно публиковать статусы WhatsApp-группы. Для размещения обратитесь к администратору."
];

/* Подписи платформ и статусов */
const PLATFORM_NAMES = { telegram: "Telegram", whatsapp: "WhatsApp" };
const STATUS_LABELS = { open: "Идёт набор", full: "Группа заполнена" };

/* ---------- 3. Вспомогательные функции ---------- */

function getGroupById(id) {
  return GROUPS.find(function (g) { return g.id === id; }) || null;
}

function getGroupsByPlatform(platform) {
  return GROUPS
    .filter(function (g) { return g.platform === platform; })
    .sort(function (a, b) { return (a.status === "full") - (b.status === "full") || a.order - b.order; });
}

/* Первая группа платформы, в которую сейчас идёт набор */
function getOpenGroup(platform) {
  return getGroupsByPlatform(platform).find(function (g) { return g.status === "open"; }) || null;
}

/* Ссылка на страницу группы — единственное место, где собирается этот адрес */
function getGroupPageHref(id) {
  const group = getGroupById(id);
  return group ? "group-" + group.id + ".html" : SITE.groupPageUrl + "?id=" + encodeURIComponent(id);
}

/* Создание элемента. Текст вставляется через textContent — безопасно для любых данных.
   opts: { cls, text, attrs: {имя: значение}, children: [узлы] } */
function el(tag, opts) {
  const node = document.createElement(tag);
  if (!opts) return node;
  if (opts.cls) node.className = opts.cls;
  if (opts.text != null) node.textContent = opts.text;
  if (opts.attrs) {
    Object.keys(opts.attrs).forEach(function (name) { node.setAttribute(name, opts.attrs[name]); });
  }
  if (opts.children) opts.children.forEach(function (child) { if (child) node.appendChild(child); });
  return node;
}

/* Внешняя ссылка: открывается в новой вкладке */
function setExternal(anchor, url) {
  anchor.setAttribute("href", url);
  anchor.setAttribute("target", "_blank");
  anchor.setAttribute("rel", "noopener noreferrer");
}

function getContactUrl(type) {
  if (type === "telegram") return "https://t.me/" + SITE.adContacts.telegram.replace(/^@/, "");
  if (type === "whatsapp") return "https://wa.me/" + SITE.adContacts.whatsapp.replace(/\D/g, "");
  return null;
}

/* true, только когда в SITE.baseUrl указан настоящий адрес (не заглушка SITE_URL) */
function hasSiteDomain() {
  return /^https?:\/\/[^\s\/]+/.test(SITE.baseUrl) && SITE.baseUrl.indexOf("SITE_URL") === -1;
}

/* Адрес сайта без слэша в конце или null, если домен ещё не задан */
function getBaseUrl() {
  return hasSiteDomain() ? SITE.baseUrl.replace(/\/+$/, "") : null;
}

/* Абсолютный адрес страницы или файла сайта; null, пока домен не задан */
function getAbsoluteUrl(path) {
  const base = getBaseUrl();
  return base ? base + "/" + String(path).replace(/^\/+/, "") : null;
}

/* Порядковые числительные для текстов про статус групп WhatsApp */
const ORDINALS = {
  1: { nom: "Первая", acc: "в первую" },
  2: { nom: "Вторая", acc: "во вторую" },
  3: { nom: "Третья", acc: "в третью" },
  4: { nom: "Четвёртая", acc: "в четвёртую" },
  5: { nom: "Пятая", acc: "в пятую" }
};

/* Тексты о статусе групп WhatsApp собираются из данных GROUPS,
   поэтому не устаревают при смене status. Возвращает { lead, faq }. */
function describeWhatsAppStatus() {
  const groups = getGroupsByPlatform("whatsapp");
  const full = groups.filter(function (g) { return g.status === "full"; });
  const open = getOpenGroup("whatsapp");

  if (!open) {
    const closed = "Сейчас набор в группы WhatsApp закрыт: все группы заполнены.";
    return { lead: closed, faq: closed };
  }
  if (!full.length) {
    const only = "Идёт набор в группу №" + open.number + ".";
    return { lead: only, faq: "Вступайте в группу WhatsApp — в ней идёт набор." };
  }

  const firstFull = full[0];
  const canUseWords = full.length === 1 && ORDINALS[firstFull.number] && ORDINALS[open.number];
  if (canUseWords) {
    return {
      lead: ORDINALS[firstFull.number].nom + " группа заполнена — новые участники в неё больше не принимаются. " +
            "Вступайте " + ORDINALS[open.number].acc + ": там идёт активный набор.",
      faq: ORDINALS[firstFull.number].nom + " группа в WhatsApp заполнена, новые участники в неё не принимаются. " +
           "Вступайте " + ORDINALS[open.number].acc + " группу — в ней идёт набор."
    };
  }
  const numbers = full.map(function (g) { return "№" + g.number; }).join(", ");
  const text = (full.length === 1 ? "Группа " : "Группы ") + numbers +
    (full.length === 1 ? " заполнена — новые участники в неё больше не принимаются. " : " заполнены — новые участники в них больше не принимаются. ") +
    "Вступайте в группу №" + open.number + ": там идёт активный набор.";
  return { lead: text, faq: text };
}

/* ---------- 4. Отрисовка: главная страница ---------- */

function createStatusBadge(status, extraClass) {
  return el("span", {
    cls: "wa-status " + (status === "open" ? "open" : "full") + (extraClass ? " " + extraClass : ""),
    text: STATUS_LABELS[status]
  });
}

/* Карточка в блоке «Две группы в WhatsApp» */
function createWhatsAppCard(group) {
  const isOpen = group.status === "open";
  const card = el("div", { cls: "wa-card reveal " + (isOpen ? "is-open" : "is-full") });

  card.appendChild(el("div", { cls: "wa-num", text: "WhatsApp · " + group.number }));
  card.appendChild(createStatusBadge(group.status));
  card.appendChild(el("h3", { text: "Группа №" + group.number }));
  card.appendChild(el("p", { text: group.shortText || group.description }));

  if (isOpen) {
    const join = el("a", { cls: "btn btn-wa btn-block", text: "Вступить в группу №" + group.number, attrs: { "data-goal": "join_whatsapp" } });
    setExternal(join, group.link);
    card.appendChild(join);
  } else {
    card.appendChild(el("span", { cls: "btn btn-disabled btn-block", text: "Набор закрыт", attrs: { "aria-disabled": "true" } }));
  }
  return card;
}

/* Карточка в разделе «Наши группы» */
function createGroupCard(group) {
  const tg = group.platform === "telegram", open = group.status === "open";
  const card = el("article", { cls: "group-card rd-community " + (tg ? "is-tg" : "is-wa") + (open ? "" : " is-full") });
  const cover = el("div", { cls: "rd-card-cover", attrs: { "aria-hidden": "true" } });
  cover.appendChild(el("img", { attrs: { src: tg ? "assets/brand/hero.webp" : (open ? "assets/brand/whatsapp-cover.webp" : "assets/brand/hero.webp"), alt: "", width: "1536", height: "1024", loading: "lazy" } }));
  cover.appendChild(createStatusBadge(group.status));
  card.appendChild(cover);
  const body = el("div", { cls: "rd-card-body" });
  const identity = el("a", { cls: "rd-card-identity", attrs: { href: getGroupPageHref(group.id), "data-goal": "open_group_page" } });
  identity.appendChild(el("img", { attrs: { src: group.logo, alt: "", width: "76", height: "76", loading: "lazy" } }));
  identity.appendChild(el("span", { text: tg ? "Telegram" : "WhatsApp · группа №" + group.number }));
  body.appendChild(identity);
  const title = el("h3");title.appendChild(el("a", { text: "Объявления Дагестана", attrs: { href: getGroupPageHref(group.id), "data-goal": "open_group_page" } }));body.appendChild(title);
  body.appendChild(el("p", { text: open ? (tg ? "Покупка, продажа, услуги и работа в Telegram." : "Новая группа: вступайте и размещайте объявления.") : "Набор закрыт. Выберите группу, в которой есть места." }));
  if(open){const join=el("a", {cls:"btn btn-block "+(tg?"btn-tg":"btn-wa"),text:"Вступить в группу",attrs:{"data-goal":tg?"join_telegram":"join_whatsapp"}});setExternal(join,group.link);body.appendChild(join);}
  else{const alternative=getOpenGroup(group.platform);body.appendChild(el("a",{cls:"btn btn-ghost btn-block",text:"Выбрать другую группу",attrs:{href:alternative?getGroupPageHref(alternative.id):SITE.homeUrl+"#groups"}}));}
  card.appendChild(body);return card;
}

function createCategoryChips(categories) {
  const wrapper = el("div", { cls: "group-cats" });
  categories.forEach(function (name) { wrapper.appendChild(el("span", { text: name })); });
  return wrapper;
}

function createRuleItem(text) {
  return el("li", { text: text });
}

function renderWhatsAppGroups() {
  const grid = document.getElementById("wa-groups-grid");
  if (!grid) return;
  grid.textContent = "";
  getGroupsByPlatform("whatsapp").forEach(function (group) { grid.appendChild(createWhatsAppCard(group)); });

  const lead = document.getElementById("wa-groups-lead");
  if (lead) lead.textContent = describeWhatsAppStatus().lead;
}

/* В «Наших группах» показываются группы, в которые идёт набор */
function renderGroups() {
  const grid = document.getElementById("groups-grid");
  if (!grid) return;
  grid.textContent = "";
  GROUPS
    .filter(function (g) { return true; })
    .sort(function (a, b) { return (a.status === "full") - (b.status === "full") || a.order - b.order; })
    .forEach(function (group) { grid.appendChild(createGroupCard(group)); });
}

function renderRules() {
  const list = document.getElementById("rules-list");
  if (!list) return;
  list.textContent = "";
  RULES.forEach(function (rule) { list.appendChild(createRuleItem(rule)); });
}

/* Ответ в FAQ про выбор группы WhatsApp */
function renderFaqAnswers() {
  const target = document.querySelector('[data-faq="wa-group"]');
  if (target) target.textContent = describeWhatsAppStatus().faq;
}

/* ---------- 5. Отрисовка: страница группы ---------- */

function createPromoRow(title, content, extraClass) {
  const row = el("div", { cls: "promo-row" + (extraClass ? " " + extraClass : "") });
  row.appendChild(el("h2", { text: title }));
  row.appendChild(content);
  return row;
}

function createCategoryAdminOffer(group) {
  const offer=el("section",{cls:"community-admin",attrs:{id:"category-admin"}});
  const heading=el("div",{cls:"community-admin-heading"});
  heading.appendChild(el("h2",{text:"Стать админом категории"}));
  const price=el("p",{cls:"community-admin-price",text:"850 ₽"});price.appendChild(el("span",{text:"/ месяц"}));heading.appendChild(price);offer.appendChild(heading);
  offer.appendChild(el("p",{text:"Получите свою категорию в группе и занимайтесь её развитием."}));
  const list=el("ul");
  ADMIN_CATEGORY_BENEFITS.forEach(function(text){list.appendChild(el("li",{text:text}));});offer.appendChild(list);
  offer.appendChild(el("p",{cls:"community-admin-note",text:"Группу, доступность категории и условия согласуйте с главным администратором перед оплатой."}));
  const actions=el("div",{cls:"community-admin-actions"});
  const contact=el("a",{cls:"btn btn-wa",text:"Обсудить категорию",attrs:{"data-goal":"ad_contact_whatsapp"}});
  setExternal(contact,getContactUrl("whatsapp")+"?text="+encodeURIComponent("Здравствуйте! Хочу стать админом категории в группе «"+group.name+"» за 850 ₽ в месяц. Подскажите доступные категории и условия."));actions.appendChild(contact);
  actions.appendChild(el("a",{cls:"community-admin-details",text:"Полные условия админства",attrs:{href:"reklama.html#category-admin"}}));offer.appendChild(actions);return offer;
}

function createPromoPage(group) {
  const isTelegram = group.platform === "telegram";
  const fragment = document.createDocumentFragment();

  const hero = el("div", { cls: "promo-hero rd-group-hero" });
  hero.appendChild(el("img", { cls: "rd-group-cover", attrs: { src: isTelegram ? "assets/brand/hero.webp" : "assets/brand/whatsapp-cover.webp", alt: "", width: "1536", height: "1024" } }));
  const avatar = el("div", { cls: "promo-avatar " + (isTelegram ? "tg" : "wa") });
  avatar.appendChild(el("img", { attrs: { src: group.logo, alt: "Логотип группы «" + group.name + "»", width: "84", height: "84" } }));
  hero.appendChild(avatar);
  hero.appendChild(el("div", { cls: "promo-platform", text: PLATFORM_NAMES[group.platform] }));
  hero.appendChild(el("h1", { text: group.name }));
  hero.appendChild(el("p", { cls: "rd-group-intro", text: group.description }));
  hero.appendChild(createJoinRow(group));
  fragment.appendChild(hero);

  const card = el("div", { cls: "promo-card" });
  card.appendChild(createPromoRow("Участники", el("p", { text: group.membersLabel })));
  card.appendChild(createPromoRow("Описание", el("p", { text: group.description })));
  card.appendChild(createPromoRow("Категории объявлений", createCategoryChips(group.categories)));
  card.appendChild(createPromoRow("Что публикуется", el("p", { text: group.whatIsPosted })));

  const rules = el("ul", { cls: "rules-list" });
  RULES.forEach(function (rule) { rules.appendChild(createRuleItem(rule)); });
  card.appendChild(createPromoRow("Правила", rules));

  /* Имя администратора необязательно: без него выводится только контакт */
  const admin = el("p");
  if (group.admin.name) {
    admin.appendChild(document.createTextNode(group.admin.name));
    admin.appendChild(el("br"));
  }
  admin.appendChild(document.createTextNode(group.admin.contact));
  card.appendChild(createPromoRow("Администрация", admin));

  card.appendChild(createJoinRow(group));
  fragment.appendChild(card);
  fragment.appendChild(createCategoryAdminOffer(group));
  return fragment;
}

/* Нижний блок: кнопка вступления или, для заполненной группы, переход в открытую */
function createJoinRow(group) {
  const isTelegram = group.platform === "telegram";
  const row = el("div", { cls: "promo-row is-last" });

  if (group.status === "open") {
    const join = el("a", {
      cls: "btn btn-block " + (isTelegram ? "btn-tg" : "btn-wa"),
      text: "Вступить в группу",
      attrs: { "data-goal": isTelegram ? "join_telegram" : "join_whatsapp" }
    });
    setExternal(join, group.link);
    row.appendChild(join);
    return row;
  }

  row.appendChild(el("span", { cls: "btn btn-disabled btn-block", text: "Группа заполнена — набор закрыт", attrs: { "aria-disabled": "true" } }));
  const alternative = getOpenGroup(group.platform);
  if (alternative) {
    const label = alternative.number != null ? "Вступить в новую группу №" + alternative.number : "Вступить в новую группу";
    const join = el("a", {
      cls: "btn btn-block " + (isTelegram ? "btn-tg" : "btn-wa"),
      text: label,
      attrs: { "data-goal": isTelegram ? "join_telegram" : "join_whatsapp" }
    });
    setExternal(join, alternative.link);
    row.appendChild(join);
  }
  return row;
}

function createNotFound() {
  const card = el("div", { cls: "promo-card promo-message" });
  card.appendChild(el("h1", { text: "Группа не найдена" }));

  const first = el("p", { text: "Проверьте ссылку или вернитесь на " });
  first.appendChild(el("a", { cls: "promo-link", text: "главную страницу", attrs: { href: SITE.homeUrl } }));
  first.appendChild(document.createTextNode("."));
  card.appendChild(first);

  const second = el("p");
  second.appendChild(el("a", { cls: "promo-link", text: "Посмотреть все группы", attrs: { href: SITE.homeUrl + "#groups" } }));
  card.appendChild(second);
  return card;
}

/* ---------- SEO: мета-теги, canonical, Open Graph, JSON-LD ---------- */

/* Тег <meta name|property="..."> обновляется, а если его нет — создаётся (дублей не бывает) */
function setMetaTag(attrName, attrValue, content) {
  let node = document.querySelector("meta[" + attrName + '="' + attrValue + '"]');
  if (!node) {
    const attrs = {};
    attrs[attrName] = attrValue;
    node = el("meta", { attrs: attrs });
    document.head.appendChild(node);
  }
  node.setAttribute("content", content);
}

function setRobots(value) {
  if (document.documentElement.dataset.preview === "true") value = "noindex, nofollow";
  setMetaTag("name", "robots", value);
}

function setCanonical(url) {
  let node = document.querySelector('link[rel="canonical"]');
  if (!node) {
    node = el("link", { attrs: { rel: "canonical" } });
    document.head.appendChild(node);
  }
  node.setAttribute("href", url);
}

function removeHeadNodes(selector) {
  document.querySelectorAll(selector).forEach(function (node) { node.remove(); });
}

/* Заглушка домена (SITE_URL) в адресах: пока домен не выбран, такие значения не должны попадать к поисковикам */
function isStubUrl(value) {
  return typeof value === "string" && value.indexOf("SITE_URL") !== -1;
}

/* Удаляет адресные теги, в которых стоит заглушка домена. Теги с настоящим адресом остаются. */
function removeStubUrlTags() {
  document.querySelectorAll('link[rel="canonical"], meta[property="og:url"], meta[property="og:image"], meta[name="twitter:image"]')
    .forEach(function (node) {
      if (isStubUrl(node.getAttribute("href")) || isStubUrl(node.getAttribute("content"))) node.remove();
    });
}

/* Заголовок и описание страницы: <title>, description, Open Graph и Twitter Card */
function setPageText(title, description) {
  document.title = title;
  setMetaTag("name", "description", description);
  setMetaTag("property", "og:title", title);
  setMetaTag("property", "og:description", description);
  setMetaTag("name", "twitter:title", title);
  setMetaTag("name", "twitter:description", description);
}

/* Адресные теги (canonical, og:url, og:image, twitter:image).
   В HTML они записаны статически с заглушкой SITE_URL; здесь они обновляются по SITE.baseUrl.
   Пока домен не задан, теги с заглушкой удаляются: ложных адресов в готовой странице нет. */
function setPageUrls(path) {
  const pageUrl = getAbsoluteUrl(path);
  const imageUrl = getAbsoluteUrl(SITE.ogImage);
  if (!pageUrl || !imageUrl) {
    removeStubUrlTags();
    return;
  }
  setCanonical(pageUrl);
  setMetaTag("property", "og:url", pageUrl);
  setMetaTag("property", "og:image", imageUrl);
  setMetaTag("name", "twitter:image", imageUrl);
}

/* Мета-теги страницы группы: зависят от группы и её статуса в GROUPS */
function updateGroupPageMeta(group) {
  if (!group) {
    setPageText("Группа не найдена — " + SITE.siteName, "Такой группы нет. Посмотрите все группы проекта «Объявления Дагестана» на главной странице.");
    /* У несуществующей группы нет своего адреса: canonical и og:url не нужны */
    removeHeadNodes('link[rel="canonical"], meta[property="og:url"]');
    removeStubUrlTags();
    setRobots("noindex, follow");
    return;
  }
  setPageText(group.name + " — " + PLATFORM_NAMES[group.platform] + " | " + SITE.siteName, group.description);
  setPageUrls(getGroupPageHref(group.id));
  /* Заполненные группы не индексируются, открытые — индексируются */
  setRobots(group.status === "open" ? "index, follow" : "noindex, follow");
}

/* Вопросы и ответы читаются из FAQ на странице, поэтому JSON-LD всегда совпадает с тем, что видит посетитель */
function readFaqFromPage() {
  const items = [];
  document.querySelectorAll(".faq details").forEach(function (details) {
    const question = details.querySelector("summary");
    const answer = details.querySelector("p");
    const questionText = question ? question.textContent.trim() : "";
    const answerText = answer ? answer.textContent.trim() : "";
    if (questionText && answerText) {
      items.push({
        "@type": "Question",
        name: questionText,
        acceptedAnswer: { "@type": "Answer", text: answerText }
      });
    }
  });
  return items;
}

/* Дополняет JSON-LD из index.html: адреса (когда задан домен), ссылки на Telegram-группу из GROUPS
   и актуальный FAQ. Статическая часть разметки остаётся рабочей и без JavaScript. */
function updateStructuredData() {
  const node = document.getElementById("structured-data");
  if (!node) return;
  let data;
  try {
    data = JSON.parse(node.textContent);
  } catch (error) {
    return;
  }
  const base = getBaseUrl();

  (data["@graph"] || []).forEach(function (item) {
    if (item["@type"] === "WebSite") {
      if (base) item.url = base + "/";
      else if (isStubUrl(item.url)) delete item.url;
    }
    if (item["@type"] === "Organization") {
      if (base) {
        item.url = base + "/";
        item.logo = getAbsoluteUrl(SITE.logo);
      } else {
        if (isStubUrl(item.url)) delete item.url;
        if (isStubUrl(item.logo)) delete item.logo;
      }
      const profiles = getGroupsByPlatform("telegram")
        .filter(function (g) { return g.status === "open"; })
        .map(function (g) { return g.link; });
      if (profiles.length) item.sameAs = profiles;
    }
    if (item["@type"] === "FAQPage") {
      const faq = readFaqFromPage();
      if (faq.length) item.mainEntity = faq;
    }
  });
  node.textContent = JSON.stringify(data);
}

/* SEO главной страницы */
function applyHomeSeo() {
  if (!document.body.classList.contains("rd-home") && !document.getElementById("wa-groups")) return;
  setPageUrls("");
  updateStructuredData();
}

function renderPromoPage() {
  if (document.getElementById("group-root")?.dataset.staticGroup) return;
  const root = document.getElementById("group-root");
  if (!root) return;

  const id = new URLSearchParams(window.location.search).get("id");
  const group = id ? getGroupById(id) : null;

  root.textContent = "";
  root.appendChild(group ? createPromoPage(group) : createNotFound());
  updateGroupPageMeta(group);
}

/* ---------- 6. Интерфейс: меню и анимация появления ---------- */

function initMenu() {
  const toggle = document.querySelector(".menu-toggle"), nav = document.getElementById("site-nav");
  if (!toggle || !nav) return;
  const modern = document.body.matches(".rd-home, .rd-group, .rd-page");
  const backdrop = modern ? el("button", { cls: "site-menu-backdrop", attrs: { type: "button", "aria-label": "Закрыть меню", tabindex: "-1", hidden: "" } }) : null;
  if (backdrop) document.body.appendChild(backdrop);
  function setOpen(open) {
    if (modern) {
      document.documentElement.style.setProperty("--menu-top", Math.ceil(toggle.closest("header").getBoundingClientRect().bottom + 8) + "px");
      document.body.classList.toggle("nav-open", open);
      backdrop.hidden = !open;
    }
    nav.classList.toggle("open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Закрыть меню" : "Меню");
    if (open && modern) { nav.scrollTop=0; nav.querySelector("a, summary").focus({preventScroll:true}); }
    if (!open) nav.querySelectorAll("details[open]").forEach(function(d){d.open=false;});
  }
  toggle.addEventListener("click", function(){setOpen(!nav.classList.contains("open"));});
  nav.addEventListener("click", function(e){if(e.target.closest("a"))setOpen(false);});
  if (backdrop) backdrop.addEventListener("click", function(){setOpen(false);toggle.focus();});
  document.addEventListener("keydown", function(e){
    if(!nav.classList.contains("open"))return;
    if(e.key==="Escape"){setOpen(false);toggle.focus();return;}
    if(modern && e.key==="Tab"){
      const items=[toggle,...nav.querySelectorAll("a[href], summary")].filter(function(n){return n.getClientRects().length;});
      const first=items[0],last=items[items.length-1];
      if(e.shiftKey && document.activeElement===first){e.preventDefault();last.focus();}
      else if(!e.shiftKey && document.activeElement===last){e.preventDefault();first.focus();}
    }
  });
  window.addEventListener("resize",function(){if(window.innerWidth>860 && nav.classList.contains("open"))setOpen(false);});
}

function initReveal() {
  const items = document.querySelectorAll(".reveal:not(.reveal-in)");
  const reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (reduced || !("IntersectionObserver" in window)) {
    items.forEach(function (item) { item.classList.add("reveal-in"); });
    return;
  }
  const observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add("reveal-in");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  items.forEach(function (item) { observer.observe(item); });
}

/* ---------- 7. Ссылки и аналитика ---------- */

/* Кнопки с data-join="telegram|whatsapp" ведут в группу, где идёт набор;
   ссылки с data-contact="telegram|whatsapp" — к администратору. Адреса берутся из SITE и GROUPS. */
function applyLinks() {
  document.querySelectorAll("[data-join]").forEach(function (anchor) {
    const group = getOpenGroup(anchor.getAttribute("data-join"));
    if (group) setExternal(anchor, group.link);
  });
  document.querySelectorAll("[data-contact]").forEach(function (anchor) {
    const url = getContactUrl(anchor.getAttribute("data-contact"));
    if (url) setExternal(anchor, url);
  });
}

/* Цель Яндекс Метрики: отправляется, только если указан SITE.metrikaId и счётчик подключён */
function trackGoal(goal) {
  if (window.cookieAccepted && SITE.metrikaId && typeof window.ym === "function") {
    window.ym(SITE.metrikaId, "reachGoal", goal);
  }
}

function initAnalytics() {
  document.addEventListener("click", function (event) {
    const target = event.target.closest("[data-goal]");
    if (target) trackGoal(target.getAttribute("data-goal"));
  });
}

/* ---------- 8. Уведомление о cookie ---------- */

/* Выбор посетителя хранится в localStorage: "yes" — принято, "no" — отказ от Яндекс Метрики.
   Скрипт в <head> запускает Метрику только при сохранённом "yes".
   До выбора и при отказе запросов к Метрике нет. */
function readConsent() { return window.SiteConsent ? SiteConsent.read() : null; }

function writeConsent(value) { if(window.SiteConsent) SiteConsent.write(value); }

function clearConsent() { if(window.SiteConsent) SiteConsent.clear(); }

function initCookieNotice() {
  if (["yes", "no"].includes(readConsent())) return;

  const notice = el("div", { cls: "cookie-notice", attrs: { role: "region", "aria-label": "Уведомление о cookie" } });
  const text = el("p");
  text.appendChild(document.createTextNode("Мы используем cookie и «Яндекс Метрику» для статистики посещаемости. Метрика включится только после нажатия «Принять». Можно отказаться и продолжить пользоваться сайтом. Подробнее — в "));
  text.appendChild(el("a", { text: "Политике конфиденциальности", attrs: { href: SITE.privacyUrl } }));
  text.appendChild(document.createTextNode("."));

  const accept = el("button", { cls: "btn btn-wa btn-sm", text: "Принять", attrs: { type: "button" } });
  const decline = el("button", { cls: "btn btn-ghost btn-sm", text: "Отказаться", attrs: { type: "button" } });
  accept.addEventListener("click", function () {
    writeConsent("yes");
    window.location.reload(); /* загрузить Метрику после явного согласия */
  });
  decline.addEventListener("click", function () {
    writeConsent("no");
    window.location.reload(); /* после перезагрузки счётчик не запускается */
  });

  notice.appendChild(text);
  notice.appendChild(el("div", { cls: "cookie-actions", children: [accept, decline] }));
  document.body.appendChild(notice);
  /* запас снизу, чтобы уведомление не закрывало подвал, пока его не закрыли */
  document.body.classList.add("with-cookie-notice");
}

/* Кнопка «Изменить выбор по cookie» на странице политики */
function initCookieReset() {
  const button = document.getElementById("cookie-reset");
  if (!button) return;
  button.addEventListener("click", function () {
    clearConsent();
    window.location.reload();
  });
}

/* ---------- 8а. Плавающая панель «Вступить» (только телефоны, только главная) ----------
   Видна, когда кнопки первого экрана прокручены вверх и подвал ещё не показался. */
function initDock() {
  const dock = document.getElementById("cta-dock");
  const heroCtas = document.querySelector(".rd-hero .hero-ctas, .hero .hero-ctas");
  const footer = document.querySelector("footer");
  if (!dock || !heroCtas || !footer || !("IntersectionObserver" in window)) return;

  document.body.classList.add("has-dock");
  let heroVisible = true;
  let footerVisible = false;

  function update() {
    const show = !heroVisible && !footerVisible;
    dock.classList.toggle("is-visible", show);
  }
  /* кнопки первого экрана считаются видимыми, если на экране больше половины их блока;
     на низких экранах, где они не помещаются, панель видна сразу */
  new IntersectionObserver(function (entries) {
    heroVisible = entries[0].intersectionRatio > 0.5;
    update();
  }, { threshold: [0, 0.25, 0.5, 0.75, 1] }).observe(heroCtas);
  new IntersectionObserver(function (entries) {
    footerVisible = entries[0].isIntersecting;
    update();
  }).observe(footer);
}

/* Open disclosure content when a visitor follows its direct link. */
function initDisclosureAnchors() {
  function reveal(hash, scroll) {
    let node; try { node=document.getElementById(decodeURIComponent(hash.slice(1))); } catch(e) { return; }
    if(!node)return;
    let expanded=false;
    for(let p=node;p;p=p.parentElement){if(p.tagName==='DETAILS'&&!p.open){p.open=true;expanded=true;}}
    if(expanded&&scroll)node.scrollIntoView({block:'start'});
  }
  reveal(window.location.hash,true);
  window.addEventListener('hashchange',function(){reveal(window.location.hash,true);});
  document.addEventListener('click',function(e){
    const a=e.target.closest('a[href]');if(!a||a.target==='_blank')return;
    let url;try{url=new URL(a.href);}catch(error){return;}
    if(url.origin===location.origin&&url.pathname===location.pathname&&url.search===location.search&&url.hash)reveal(url.hash,false);
  });
}

/* ---------- 9. Запуск ---------- */

function initApp() {
  renderWhatsAppGroups();
  renderGroups();
  renderRules();
  renderFaqAnswers();
  renderPromoPage();
  applyHomeSeo();
  applyLinks();
  initMenu();
  initReveal();
  initAnalytics();
  initCookieNotice();
  initCookieReset();
  initDock();
  initDisclosureAnchors();
}

document.addEventListener("DOMContentLoaded", initApp);

