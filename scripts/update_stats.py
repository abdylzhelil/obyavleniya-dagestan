#!/usr/bin/env python3
"""Обновляет data/stats.json: число участников публичной Telegram-группы.
Берётся с открытой страницы t.me/<группа> (без токенов). При ошибке файл не меняется."""
import json, re, sys, urllib.request, datetime, pathlib

GROUP = "AvitoDag05_reklama_group"
OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "stats.json"

req = urllib.request.Request("https://t.me/" + GROUP, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
m = re.search(r'tgme_page_extra">\s*([\d\s\xa0]+?)\s*(?:members|участник)', html)
if not m:
    sys.exit("не нашёл число участников на странице группы")
members = int(re.sub(r"\D", "", m.group(1)))
if not 100 <= members <= 1_000_000:
    sys.exit("подозрительное число участников: %d" % members)

old = {}
try:
    old = json.loads(OUT.read_text(encoding="utf-8"))
except Exception:
    pass
if old.get("telegram_members") == members:
    print("без изменений:", members)
    sys.exit(0)
OUT.write_text(json.dumps({
    "telegram_members": members,
    "updated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("обновлено:", members)
