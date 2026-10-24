# Инструменты сайта

- `og_image.py` — рисует `og-image.png` (превью ссылки): `python3 tools/og_image.py tools/land_dots.b64 og-image.png`
- `land_dots.b64` — точки суши для планеты (те же, что встроены в `index.html`).
- `i18n.py` — дописывает недостающие переводы (zh, tr, fa, ar) к строкам `<span class="en">…</span>` через OpenRouter; запускать из venv проекта customs-agent.
