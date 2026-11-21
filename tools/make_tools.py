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


AUTO_STYLE = """
.calc { display:grid; grid-template-columns:minmax(0,1.35fr) minmax(0,1fr); gap:28px; align-items:start; }
.fields { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:16px 14px; }
.fields > div[hidden] { display:none; }
.fields .wide { grid-column:1 / -1; }
.fields label { white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.tool select, .tool input { height:48px; padding:0 14px; font-size:15px; line-height:normal; }
.tool select { appearance:none; -webkit-appearance:none; padding-right:38px; cursor:pointer;
  background:#fff url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%230f766e' stroke-width='2' fill='none'/%3E%3C/svg%3E") no-repeat right 14px center; }
.money { display:flex; }
.money input { border-radius:12px 0 0 12px; flex:1; min-width:0; }
.money select { width:132px; flex:none; border-radius:0 12px 12px 0; border-left:0; background-color:var(--bg-2); }
.rate { display:flex; flex-wrap:wrap; align-items:center; gap:6px 10px; margin:14px 0 0; font-size:13px; color:var(--muted); }
.rate button { font:inherit; font-size:13px; color:var(--teal); background:none; border:0; padding:0; cursor:pointer; text-decoration:underline; }
.rate input { width:110px; height:34px; padding:0 10px; font-size:14px; }
.result { background:linear-gradient(135deg,#071a26,#0b3a4a 60%,#0f766e); color:#fff; border-radius:16px; padding:22px; position:sticky; top:80px; }
.result h3 { margin:0 0 4px; font-size:14px; font-weight:600; color:#5eead4; text-transform:uppercase; letter-spacing:.05em; }
.result .total { font-size:34px; font-weight:700; line-height:1.15; margin:0 0 12px; }
.result .small, .result li { color:rgba(255,255,255,.72); }
.res { width:100%; border-collapse:collapse; }
.res td { padding:9px 0; border-top:1px solid rgba(255,255,255,.14); vertical-align:top; font-size:14.5px; }
.res td:last-child { text-align:right; font-weight:600; white-space:nowrap; padding-left:12px; }
.res .small { font-size:12.5px; }
.result ul { padding-left:18px; margin:10px 0 0; font-size:13px; }
.result .empty { color:rgba(255,255,255,.72); font-size:14.5px; margin:0; }
.disclaimer { margin:16px 0 0; }
@media (max-width:860px) { .calc { grid-template-columns:1fr; } .result { position:static; } }
@media (max-width:480px) { .money select { width:112px; } }
"""

AUTO_TOOL = """<div class="tool"><div class="calc">
<div>
<div class="fields">
<div><label for="a-who">Кто ввозит</label><select id="a-who"><option value="personal">Физлицо для себя</option><option value="company">Юрлицо / для продажи</option></select></div>
<div><label for="a-age">Возраст авто</label><select id="a-age"><option value="new">до 3 лет</option><option value="3">от 3 до 5 лет</option><option value="5">от 5 до 7 лет</option><option value="7">старше 7 лет</option></select></div>
<div class="wide"><label for="a-engine">Двигатель</label><select id="a-engine"><option value="petrol">Бензин</option><option value="diesel">Дизель</option><option value="hyb">Гибрид</option><option value="seq">Последовательный гибрид</option><option value="ev">Электромобиль</option></select></div>
<div id="a-cc-box"><label for="a-cc">Объём, см³</label><input id="a-cc" inputmode="numeric" placeholder="1998"></div>
<div id="a-hp-box"><label for="a-hp">Мощность ДВС, л.с.</label><input id="a-hp" inputmode="decimal" placeholder="150"></div>
<div id="a-em-box" hidden><label for="a-em" id="a-em-label" title="Максимальная 30-минутная мощность электромотора">Электромотор, л.с.</label><input id="a-em" inputmode="decimal" placeholder="100"></div>
<div class="wide"><label for="a-price">Стоимость авто</label><div class="money"><input id="a-price" inputmode="decimal" placeholder="2 000 000"><select id="a-cur" aria-label="Валюта"><option value="RUB">₽ рубли</option><option value="EUR">€ евро</option><option value="USD">$ доллары</option><option value="CNY">¥ юани</option><option value="AED">AED дирхамы</option><option value="TRY">₺ лиры</option></select></div></div>
</div>
<div class="rate"><span id="a-ratedate">Загружаем курс ЦБ…</span><button type="button" id="a-rate-edit">изменить курс</button><span id="a-eur-box" hidden><input id="a-eur" inputmode="decimal" aria-label="Курс евро, ₽"> ₽ за €</span></div>
</div>
<div class="result allow-copy" aria-live="polite"><h3>Платежи на таможне</h3><div id="a-out"></div></div>
</div>
<p class="small disclaimer">Расчёт предварительный, по ставкам 2026 года. Точную сумму считает таможня на дату декларации; утильсбор — на дату оплаты.</p>
</div>"""

AUTO_BODY = """<section><h2>Что входит в растаможку авто</h2><ul class="list">
<li><b>Физлицо для себя</b> платит единую ставку — она заменяет пошлину, акциз и НДС. До 3 лет — процент от стоимости, но не менее определённой суммы за см³; старше — евро за см³ объёма.</li>
<li><b>Юрлицо или физлицо для продажи</b> платит пошлину по Единому таможенному тарифу ЕАЭС, акциз по мощности и НДС 22 %.</li>
<li><b>Таможенный сбор</b> — от 1 231 до 73 860 ₽, зависит от стоимости авто.</li>
<li><b>Утилизационный сбор</b> — для личного авто до 160 л.с. и 3 000 см³: 3 400 ₽ (до 3 лет) или 5 200 ₽ (старше). Мощнее или для продажи — по коммерческой шкале, от сотен тысяч рублей.</li>
<li><b>Электромобили</b> с 2026 года платят пошлину 15 %, акциз и НДС — льготный ввоз для России закончился 31.12.2025.</li>
</ul></section>
<section><h2>Как считается возраст</h2><ul class="list">
<li>Возраст — от даты выпуска авто. Если известен только год — от 1 июля этого года, если год и месяц — от 15-го числа.</li>
<li>Для единой ставки возраст смотрят на день регистрации декларации, для утильсбора «старше 3 лет» — тоже от даты выпуска.</li>
</ul></section>"""

AUTO_FAQ = [
    ("Сколько стоит растаможка авто в 2026 году?",
     "Зависит от возраста, объёма и мощности. Например, бензиновое авто 2,0 л, 150 л.с., 4 года, для себя: единая ставка 2,7 € за см³ (около 5 400 €), сбор 13 541 ₽ при стоимости 1,2–2,7 млн ₽, утильсбор 5 200 ₽."),
    ("Какой утильсбор для личного авто?",
     "3 400 ₽ для авто до 3 лет и 5 200 ₽ для авто старше 3 лет — при мощности до 160 л.с. и объёме до 3 000 см³, одна машина в 12 месяцев. Для электромобилей льгота — до 80 л.с."),
    ("Платят ли электромобили пошлину?",
     "Да. С 2026 года при ввозе в Россию — пошлина 15 %, акциз по мощности и НДС 22 %, утильсбор по мощности электромотора."),
    ("Можете растаможить авто за меня?",
     "Да. Проверим документы, посчитаем платежи, подадим декларацию и проведём через таможню. Растаможка — от 10 000 ₽."),
]  # fmt: skip

UTIL_JSON = (Path(__file__).with_name("util2026.json")).read_text()
AUTO_SCRIPT = Path(__file__).with_name("auto_calc.js").read_text().replace("UTIL_JSON", UTIL_JSON)

PAGES = {
    "kod-tn-ved.html": dict(
        title="Код ТН ВЭД онлайн: поиск по названию товара, пошлина и НДС | CargoClear",
        description="Бесплатный поиск кода ТН ВЭД ЕАЭС по описанию товара или цифрам кода: ставка ввозной пошлины и НДС при ввозе в Россию. Без регистрации.",
        h1="Поиск кода ТН ВЭД",
        lead="Опишите товар своими словами или введите код — покажем подходящие коды ТН ВЭД ЕАЭС с пошлиной и НДС. Бесплатно и без регистрации.",
        tool=HS_TOOL, body=HS_BODY, faq=HS_FAQ, script=HS_SCRIPT,
    ),
    "rastamozhka-avto.html": dict(
        title="Калькулятор растаможки авто 2026 онлайн: пошлина, утильсбор, НДС | CargoClear",
        description="Рассчитайте растаможку автомобиля в 2026 году: единая ставка для физлиц, пошлина, акциз и НДС для юрлиц, таможенный и утилизационный сбор. Бензин, дизель, гибрид, электро.",
        h1="Калькулятор растаможки авто",
        lead="Посчитайте платежи за ввоз легкового автомобиля в Россию по ставкам 2026 года: единая ставка или пошлина с акцизом и НДС, таможенный и утилизационный сбор.",
        tool=AUTO_TOOL, body=AUTO_BODY, faq=AUTO_FAQ, script=AUTO_SCRIPT, extra_style=AUTO_STYLE,
    ),
}  # fmt: skip


def main() -> None:
    for slug, spec in PAGES.items():
        (ROOT / slug).write_text(page(slug, **spec), encoding="utf-8")
        print("written", slug)


if __name__ == "__main__":
    main()
