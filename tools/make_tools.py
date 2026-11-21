"""Страницы-инструменты сайта: поиск кода ТН ВЭД и калькулятор растаможки авто.

python3 tools/make_tools.py — пишет HTML в корень сайта. Оформление — как у страниц товаров
(tools/make_guides.py). Список страниц должен совпадать с GUIDE_PAGES в
customs-agent/customs/site_news.py (оттуда строится sitemap.xml).
"""

from __future__ import annotations

import json
from pathlib import Path

from make_guides import SITE, STYLE, WA, _e

ROOT = Path(__file__).resolve().parent.parent
PANEL = "https://panel.cargoclear.ru"

TOOL_STYLE = """
.tool { background:#fff; border:1px solid var(--line); border-radius:20px; padding:24px; box-shadow:0 18px 40px rgba(11,29,42,.07); margin-top:-28px; position:relative; }
.tool label { display:block; font-weight:600; font-size:13px; color:var(--muted); margin:0 0 6px; }
.tool input, .tool select { width:100%; padding:12px 14px; border:1px solid var(--line); border-radius:12px; font:inherit; color:var(--ink); background:#fff; }
.tool input:focus, .tool select:focus { outline:none; border-color:var(--teal); box-shadow:0 0 0 3px var(--teal-soft); }
.tool .go { border:0; cursor:pointer; background:var(--teal); color:#fff; border-radius:12px; padding:12px 22px; font:inherit; font-weight:600; }
.tool .go:disabled { opacity:.6; cursor:default; }
.row2 { display:flex; gap:10px; }
.row2 input { flex:1; min-width:0; }
.chips { display:flex; flex-wrap:wrap; gap:8px; margin:12px 0 0; }
.chips button { font:inherit; font-size:13px; padding:6px 12px; border-radius:999px; border:1px solid var(--line); background:var(--teal-soft); color:var(--teal); cursor:pointer; }
.note { margin:14px 0 0; font-size:14px; color:var(--muted); }
.note:empty { display:none; }
.items { display:grid; gap:12px; margin-top:14px; }
.items:empty { display:none; }
.item { border:1px solid var(--line); border-radius:14px; padding:14px 16px; display:grid; gap:6px; }
.item .top { display:flex; flex-wrap:wrap; align-items:baseline; gap:4px 12px; }
.item .code { font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:19px; font-weight:700; color:var(--teal); white-space:nowrap; }
.item .title { font-weight:600; }
.item .path { font-size:13px; color:var(--muted); }
.item .why { font-size:14px; }
.tags { display:flex; flex-wrap:wrap; gap:8px; align-items:center; }
.tag { font-size:13px; font-weight:600; border-radius:999px; padding:3px 10px; background:var(--bg-2); }
.tag.vat { background:#ecfdf5; color:#065f46; }
.calc-link { margin-left:auto; font-size:13px; font-weight:600; color:var(--teal); border:1px solid var(--teal); border-radius:999px; padding:4px 12px; text-decoration:none; }
.small { font-size:13px; color:var(--muted); }
.allow-copy, .allow-copy * { -webkit-user-select:text; user-select:text; }
@media (max-width:640px) { .row2 { flex-direction:column; } .calc-link { margin-left:0; } .tool { padding:18px; } }
"""


def page(slug: str, title: str, description: str, h1: str, lead: str, tool: str, body: str,
         faq: list[tuple[str, str]], script: str, extra_style: str = "") -> str:  # fmt: skip
    url = f"{SITE}/{slug}"
    AUTO_LINK = ('<a class="hide-m" href="/rastamozhka-avto.html">Растаможка авто</a>'
                 if "rastamozhka-avto.html" in PAGES else "")
    faq_ld = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq],
    }  # fmt: skip
    faq_html = "".join(f"<details><summary>{_e(q)}</summary><p>{_e(a)}</p></details>"
                       for q, a in faq)  # fmt: skip
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_e(title)}</title>
<meta name="description" content="{_e(description)}">
<link rel="canonical" href="{url}">
<link rel="apple-touch-icon" href="/icon-180.png">
<meta property="og:type" content="website">
<meta property="og:title" content="{_e(h1)}">
<meta property="og:description" content="{_e(description)}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:url" content="{url}">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
<style>{STYLE}{TOOL_STYLE}{extra_style}</style>
<script src="/protect.js" defer></script>
</head>
<body>
<header><div class="wrap"><a class="logo" href="/">CargoClear</a>
<nav><a class="hide-m" href="/kod-tn-ved.html">Код ТН ВЭД</a>{AUTO_LINK}<a href="/#quote">Расчёт</a></nav></div></header>
<div class="hero"><div class="wrap">
<h1>{_e(h1)}</h1>
<p>{_e(lead)}</p>
</div></div>
<main class="wrap">
{tool}
{body}
<section><h2>Частые вопросы</h2>{faq_html}</section>
<div class="cta"><h2>Растаможим за вас</h2>
<p>Растаможка — от 10 000 ₽ за машину или отправку. Импорт на нашу компанию — от 20 000 ₽ + расходы по факту, без наценки. Расчёт до отгрузки бесплатно.</p>
<a class="btn primary" href="/#quote">Получить расчёт</a><a class="btn ghost" href="{WA}" target="_blank" rel="noopener">WhatsApp +7 963 949-38-85</a></div>
</main>
<footer><div class="wrap">© 2026 CargoClear · <a href="/privacy.html">Политика конфиденциальности</a><br>
ООО «КАРГО КЛИР» · ИНН 9723281737 · КПП 772301001 · ОГРН 1267700368275 · г. Москва, ул. Маршала Кожедуба, д. 8, помещ. 2/1<br>
Расчёт на сайте предварительный. Точные ставки — по коду ТН ВЭД на дату ввоза.</div></footer>
<script>{script}</script>
</body>
</html>
"""


HS_TOOL = """<div class="tool">
<form id="hs-form" role="search">
<label for="hs-q">Товар своими словами или код</label>
<div class="row2"><input id="hs-q" type="search" maxlength="200" autocomplete="off" placeholder="например: розы свежие, светодиодные лампы, 8471 30"><button class="go" id="hs-go" type="submit">Найти код</button></div>
</form>
<div class="chips" id="hs-ex"></div>
<div class="note" id="hs-note" role="status" aria-live="polite"></div>
<div class="items allow-copy" id="hs-list"></div>
<p class="small">Результат предварительный. Окончательный код подтверждает наш брокер по документам и составу товара.</p>
</div>"""

HS_BODY = """<section><h2>Как работает поиск</h2><ul class="list">
<li><b>По коду.</b> Введите 4–10 цифр — покажем все коды этой группы с пошлиной и НДС.</li>
<li><b>По описанию.</b> Напишите товар своими словами: из чего сделан, для чего, в каком виде. Искусственный интеллект выберет до трёх подходящих кодов — только из официального справочника, выдуманный код не пройдёт.</li>
<li><b>Ставки</b> — из Единого таможенного тарифа ЕАЭС, справочник обновляется ежедневно. НДС 10 % — для товаров из перечня Постановления Правительства № 908, остальные — 22 %.</li>
</ul></section>
<section><h2>Почему код так важен</h2><ul class="list">
<li>От кода зависят пошлина, НДС, нужные сертификаты, фитоконтроль и маркировка.</li>
<li>Неверный код — доначисление платежей, штраф и задержка груза на складе.</li>
<li>Для одного товара часто подходят несколько кодов: свежие и сушёные фрукты, детали и готовые изделия. Брокер выбирает по документам и составу.</li>
</ul></section>"""

HS_FAQ = [
    ("Что такое код ТН ВЭД?",
     "Десятизначный код товара по Товарной номенклатуре внешнеэкономической деятельности ЕАЭС. По нему определяют пошлину, НДС и требования к ввозу."),
    ("Можно ли доверять подбору кода на сайте?",
     "Это предварительный подбор. Коды берутся из официального справочника, но окончательный код определяет брокер по документам, составу и назначению товара."),
    ("Какая ставка НДС при ввозе?",
     "22 % для большинства товаров. 10 % — для продовольственных и детских товаров из перечня Постановления Правительства № 908, например свежих фруктов."),
    ("Сколько стоит растаможка у вас?",
     "Растаможка — от 10 000 ₽ за машину или отправку (авто, авиа, ЖД), вес не важен. Импорт на нашу компанию — от 20 000 ₽ плюс расходы по факту."),
]  # fmt: skip

HS_SCRIPT = """
(function () {
  var form = document.getElementById("hs-form"), q = document.getElementById("hs-q");
  var note = document.getElementById("hs-note"), list = document.getElementById("hs-list");
  var go = document.getElementById("hs-go"), ex = document.getElementById("hs-ex");
  var MODE = {ai: "Наиболее подходящие коды по описанию:", words: "Коды, в названии которых есть ваши слова:", code: "Коды в этой группе:"};
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text) e.textContent = text; return e; }
  ["розы свежие", "курага", "томатная паста", "запчасти для грузовиков", "8708"].forEach(function (w) {
    var b = el("button", "", w); b.type = "button";
    b.addEventListener("click", function () { q.value = w; search(); }); ex.appendChild(b);
  });
  function render(j) {
    list.innerHTML = "";
    if (!j.items.length) { note.textContent = "Ничего не нашли. Опишите товар подробнее (материал, назначение) или отправьте заявку — подберём код сами."; return; }
    note.textContent = MODE[j.mode];
    j.items.forEach(function (it) {
      var card = el("div", "item"), top = el("div", "top");
      top.appendChild(el("span", "code", it.code_fmt)); top.appendChild(el("span", "title", it.title));
      card.appendChild(top);
      if (it.path) card.appendChild(el("div", "path", it.path));
      if (it.reason) card.appendChild(el("div", "why", it.reason));
      var tags = el("div", "tags");
      tags.appendChild(el("span", "tag", "Пошлина: " + (it.duty || "ставку уточним")));
      tags.appendChild(el("span", "tag vat", "НДС " + it.vat + " %" + (it.vat_conditional ? " (при условии)" : "")));
      var a = el("a", "calc-link", "Рассчитать платежи");
      a.href = "/#quote"; tags.appendChild(a);
      card.appendChild(tags); list.appendChild(card);
    });
  }
  function search() {
    var text = q.value.trim();
    if (text.length < 3) { q.focus(); return; }
    note.textContent = /^[\\d\\s.\\-]+$/.test(text) ? "Ищем…" : "Ищем… по описанию это 10–30 секунд.";
    list.innerHTML = ""; go.disabled = true;
    fetch("PANEL/public/hs-search", {method: "POST", body: JSON.stringify({q: text, lang: "ru"})})
      .then(function (r) { return r.json().then(function (j) { j.status = r.status; return j; }); })
      .then(function (j) {
        if (j.status === 429) { note.textContent = "Слишком много запросов с вашей сети — попробуйте через час."; return; }
        if (!j.ok) { note.textContent = "Введите хотя бы 3 символа."; return; }
        render(j);
      })
      .catch(function () { note.textContent = "Поиск сейчас недоступен — напишите нам, подберём код."; })
      .then(function () { go.disabled = false; });
  }
  form.addEventListener("submit", function (e) { e.preventDefault(); search(); });
  var start = new URLSearchParams(location.search).get("q");
  if (start) { q.value = start; search(); }
})();
""".replace("PANEL", PANEL)

PAGES = {
    "kod-tn-ved.html": dict(
        title="Код ТН ВЭД онлайн: поиск по названию товара, пошлина и НДС | CargoClear",
        description="Бесплатный поиск кода ТН ВЭД ЕАЭС по описанию товара или цифрам кода: ставка ввозной пошлины и НДС при ввозе в Россию. Без регистрации.",
        h1="Поиск кода ТН ВЭД",
        lead="Опишите товар своими словами или введите код — покажем подходящие коды ТН ВЭД ЕАЭС с пошлиной и НДС. Бесплатно и без регистрации.",
        tool=HS_TOOL, body=HS_BODY, faq=HS_FAQ, script=HS_SCRIPT,
    ),
}  # fmt: skip


def main() -> None:
    for slug, spec in PAGES.items():
        (ROOT / slug).write_text(page(slug, **spec), encoding="utf-8")
        print("written", slug)


if __name__ == "__main__":
    main()
