// Калькулятор растаможки легкового авто (ТН ВЭД 8703) в РФ. Ставки на 2026 год:
// ЕТС — Решение Совета ЕЭК № 107 (прил. 2, табл. 2); пошлина юрлиц — ЕТТ ЕАЭС (Решение № 80);
// акциз — НК РФ ст. 193 (ред. 425-ФЗ); НДС 22 % — НК РФ ст. 164; сбор — Постановление № 1637
// (ред. № 1638); утильсбор — Постановление № 1291 (ред. № 1713), коэффициенты 2026 года.
(function () {
  var UTIL = UTIL_JSON, BASE = 20000, KW = 0.7355;
  var $ = function (id) { return document.getElementById(id); };
  var RATES = {RUB: 1};
  fetch("/rates.json").then(function (r) { return r.json(); }).then(function (j) {
    Object.keys(j.rates).forEach(function (k) { RATES[k] = j.rates[k].value; });
    RATE_DAY = j.date.split("-").reverse().join(".");
    if (!$("a-eur").value) $("a-eur").value = RATES.EUR;
    calc();
  }).catch(function () { $("a-ratedate").textContent = "Курс не загрузился — укажите курс евро:"; $("a-eur-box").hidden = false; $("a-rate-edit").hidden = true; });
  var RATE_DAY = "";
  $("a-rate-edit").addEventListener("click", function () { $("a-eur-box").hidden = false; $("a-rate-edit").hidden = true; $("a-eur").focus(); });

  function band(rows, kw) { for (var i = 0; i < rows.length; i++) if (kw <= rows[i][0]) return rows[i]; return rows[rows.length - 1]; }
  function etsNew(eur, cc) {
    var t = [[8500, .54, 2.5], [16700, .48, 3.5], [42300, .48, 5.5], [84500, .48, 7.5], [169000, .48, 15], [1e12, .48, 20]];
    for (var i = 0; i < t.length; i++) if (eur <= t[i][0]) return Math.max(eur * t[i][1], cc * t[i][2]);
  }
  function etsUsed(cc, over5) {
    var t = [[1000, 1.5, 3], [1500, 1.7, 3.2], [1800, 2.5, 3.5], [2300, 2.7, 4.8], [3000, 3, 5], [1e9, 3.6, 5.7]];
    for (var i = 0; i < t.length; i++) if (cc <= t[i][0]) return cc * (over5 ? t[i][2] : t[i][1]);
  }
  // Пошлина ЕТТ: доля от стоимости, минимум евро/см3 или евро/см3 — в евро.
  function ettDuty(fuel, age, cc, eur) {
    if (age === "new") return eur * (fuel === "petrol" && cc > 2800 ? .125 : .15);
    var t = fuel === "diesel"
      ? [[1500, .32, 1.5], [2500, .4, 2.2], [1e9, .8, 3.2]]
      : [[1000, .36, 1.4], [1500, .4, 1.5], [1800, .36, 1.6], [3000, .44, 2.2], [1e9, .8, 3.2]];
    for (var i = 0; i < t.length; i++) if (cc <= t[i][0]) return age === "7" ? cc * t[i][2] : Math.max(eur * .2, cc * t[i][1]);
  }
  function excise(hp) {
    var t = [[90, 0], [150, 64], [200, 613], [300, 1004], [400, 1711], [500, 1771], [1e9, 1829]];
    for (var i = 0; i < t.length; i++) if (hp <= t[i][0]) return hp * t[i][1];
  }
  function fee(rub) {
    var t = [[200000, 1231], [450000, 2462], [1200000, 4924], [2700000, 13541], [4200000, 18465], [5500000, 21344], [10000000, 49240], [1e15, 73860]];
    for (var i = 0; i < t.length; i++) if (rub <= t[i][0]) return t[i][1];
  }
  function util(kind, cc, kw, used, personal) {
    var col = used ? 2 : 1;
    if (kind === "ev") {
      if (personal && kw <= 58.84) return BASE * (used ? .26 : .17);
      return BASE * band(UTIL.ev, kw)[col];
    }
    if (personal && cc <= 3000 && kw <= 117.68) return BASE * (used ? .26 : .17);
    var key = cc <= 1000 ? "ice1000" : cc <= 2000 ? "ice2000" : cc <= 3000 ? "ice3000" : cc <= 3500 ? "ice3500" : "iceMax";
    return BASE * band(UTIL[key], kw)[col];
  }
  function rub(v) { return Math.round(v).toLocaleString("ru-RU") + " ₽"; }
  function num(id) { return parseFloat(String($(id).value).replace(/\s/g, "").replace(",", ".")) || 0; }

  function show() {
    var eng = $("a-engine").value;
    $("a-cc-box").hidden = eng === "ev";
    $("a-hp-box").hidden = eng === "ev" || eng === "seq";
    $("a-em-box").hidden = !(eng === "ev" || eng === "seq" || eng === "hyb");
    var e = num("a-eur");
    if (e) $("a-ratedate").textContent = "Курс ЦБ" + (RATE_DAY ? " на " + RATE_DAY : "") + ": 1 € = " + e.toLocaleString("ru-RU", {maximumFractionDigits: 2}) + " ₽";
  }
  function calc() {
    show();
    var who = $("a-who").value, age = $("a-age").value, eng = $("a-engine").value;
    var cur = $("a-cur").value, price = num("a-price"), eurRate = num("a-eur");
    var cc = eng === "ev" ? 0 : num("a-cc"), hp = num("a-hp"), em = num("a-em");
    var out = $("a-out");
    if (!price || !eurRate || (eng !== "ev" && !cc) || (eng === "ev" || eng === "seq" ? !em : !hp)) {
      out.innerHTML = '<div class="total">—</div><p class="empty">Заполните объём, мощность и стоимость — расчёт появится сразу.</p>'; return;
    }
    if (!RATES[cur]) { out.innerHTML = '<p class="small">Нет курса для этой валюты — выберите рубли или евро.</p>'; return; }
    var valueRub = cur === "EUR" ? price * eurRate : price * RATES[cur], valueEur = valueRub / eurRate;
    var used = age !== "new", personal = who === "personal";
    // Мощность: для акциза и утильсбора гибрида — ДВС + электромотор; последовательный гибрид и электро — только электромотор.
    var powerHp = eng === "ev" || eng === "seq" ? em : eng === "hyb" ? hp + em : hp;
    var utilKind = eng === "ev" || eng === "seq" ? "ev" : "ice";
    var lines = [], total = 0;
    function add(name, v, hint) { lines.push([name, v, hint || ""]); total += v; }
    var notes = [];
    if (personal && eng !== "ev") {
      var ets = age === "new" ? etsNew(valueEur, cc) : etsUsed(cc, age === "5" || age === "7");
      add("Единая ставка (пошлина и налоги)", ets * eurRate, age === "new" ? "до 3 лет: % от стоимости, но не менее евро за см³" : "евро за см³ объёма");
    } else {
      var fuel = eng === "diesel" ? "diesel" : "petrol";
      var dutyEur = eng === "ev" || eng === "seq" ? valueEur * .15 : ettDuty(fuel, age, cc, valueEur);
      var duty = dutyEur * eurRate, exc = excise(powerHp), vat = (valueRub + duty + exc) * .22;
      add("Ввозная пошлина", duty, eng === "ev" || eng === "seq" ? "15 % от стоимости" : "по ЕТТ ЕАЭС");
      add("Акциз", exc, Math.round(powerHp) + " л.с. по ставке 2026 года");
      add("НДС 22 %", vat, "от стоимости, пошлины и акциза");
      if (personal && eng === "ev") notes.push("Электромобили не платят единую ставку: физлицо платит пошлину 15 %, акциз и НДС.");
    }
    add("Таможенный сбор", fee(valueRub), "по таможенной стоимости");
    var u = util(utilKind, cc, powerHp * KW, used, personal);
    add("Утилизационный сбор", u, (u <= 5200 ? "льготный — для личного пользования" : "коммерческая ставка 2026 года"));
    if (personal && u > 5200) notes.push(utilKind === "ev"
      ? "Льготный утильсбор (3 400 / 5 200 ₽) для электромобиля — только до 80 л.с. (58,84 кВт)."
      : "Льготный утильсбор (3 400 / 5 200 ₽) — только до 160 л.с. и 3 000 см³. Выше — коммерческая ставка.");
    if (personal) notes.push("Льготы для личного пользования — одна машина в 12 месяцев; при продаже раньше года утильсбор доплачивается до коммерческого.");
    var html = '<div class="total">' + rub(total) + '</div><table class="res"><tbody>' + lines.map(function (l) {
      return "<tr><td>" + l[0] + (l[2] ? '<br><span class="small">' + l[2] + "</span>" : "") + "</td><td>" + rub(l[1]) + "</td></tr>";
    }).join("") + "</tbody></table>";
    html += '<p class="small">Стоимость авто: ' + rub(valueRub) + " (" + Math.round(valueEur).toLocaleString("ru-RU") + " €). Без учёта доставки, СВХ, СБКТС и ЭРА-ГЛОНАСС.</p>";
    if (notes.length) html += '<ul class="small">' + notes.map(function (n) { return "<li>" + n + "</li>"; }).join("") + "</ul>";
    out.innerHTML = html;
  }
  ["a-who", "a-age", "a-engine", "a-cur", "a-price", "a-eur", "a-cc", "a-hp", "a-em"].forEach(function (id) {
    $(id).addEventListener("input", calc); $(id).addEventListener("change", calc);
  });
  $("a-cur").addEventListener("change", function () { if ($("a-cur").value === "EUR" && RATES.EUR && !$("a-eur").value) $("a-eur").value = RATES.EUR; });
  calc();
  window.__autoCalc = {etsNew: etsNew, etsUsed: etsUsed, ettDuty: ettDuty, excise: excise, fee: fee, util: util};
})();
