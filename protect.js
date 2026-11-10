/* Защита от копирования: мешает выделять, сохранять и перетаскивать содержимое.
   Поля формы, почта и телефон остаются доступными, чтобы клиенту было удобно. */
(function () {
  var css = document.createElement("style");
  css.textContent =
    "body{-webkit-user-select:none;user-select:none;-webkit-touch-callout:none}" +
    "input,textarea,select,[contenteditable],a[href^='mailto:'],a[href^='tel:'],.allow-copy" +
    "{-webkit-user-select:text;user-select:text}" +
    "img,video,svg{-webkit-user-drag:none;user-drag:none}" +
    "@media print{body{display:none!important}}";
  document.head.appendChild(css);

  function editable(el) {
    return el && el.closest && el.closest("input,textarea,select,[contenteditable],.allow-copy,a[href^='mailto:'],a[href^='tel:']");
  }
  document.addEventListener("contextmenu", function (e) { if (!editable(e.target)) e.preventDefault(); });
  document.addEventListener("dragstart", function (e) { if (!editable(e.target)) e.preventDefault(); });
  document.addEventListener("copy", function (e) { if (!editable(e.target) && !editable(document.activeElement)) e.preventDefault(); });
  document.addEventListener("cut", function (e) { if (!editable(e.target)) e.preventDefault(); });
  document.addEventListener("keydown", function (e) {
    var k = (e.key || "").toLowerCase(), mod = e.ctrlKey || e.metaKey;
    if (e.key === "F12" ||
        (mod && ["s", "u", "p"].indexOf(k) >= 0) ||
        (mod && e.shiftKey && ["i", "j", "c"].indexOf(k) >= 0) ||
        (e.metaKey && e.altKey && ["i", "j", "c", "u"].indexOf(k) >= 0) ||
        (mod && ["a", "c"].indexOf(k) >= 0 && !editable(document.activeElement))) {
      e.preventDefault();
    }
  });
  document.querySelectorAll("video").forEach(function (v) {
    v.setAttribute("controlsList", "nodownload noplaybackrate");
    v.setAttribute("disablePictureInPicture", "");
  });
})();
