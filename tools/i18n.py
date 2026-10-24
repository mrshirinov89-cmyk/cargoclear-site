import json, re, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, "/Users/kamransirinov/Таможенный агент/customs-agent")
from adapters.openrouter.client import OpenRouterClient

PATH = "/Users/kamransirinov/Таможенный агент/cargoclear-site/index.html"
s = open(PATH, encoding="utf-8").read()
GROUP = re.compile(r'<span class="en">((?:(?!</span>).)*?)</span>((?:<span class="(?:ru|zh|tr|fa|ar)">(?:(?!</span>).)*?</span>)*)', re.S)
LANGS = {"zh": "Simplified Chinese", "tr": "Turkish", "fa": "Persian (Farsi)", "ar": "Arabic"}
need = {l: [] for l in LANGS}
for m in GROUP.finditer(s):
    have = set(re.findall(r'<span class="(\w+)">', m.group(2)))
    for l in LANGS:
        if l not in have and m.group(1) not in need[l]:
            need[l].append(m.group(1))
client = OpenRouterClient.from_environment(timeout_s=180.0)
def _batch(lang, items):
    prompt = (f"Translate each English UI string of a customs-broker website (CargoClear: customs clearance and importer of record in Russia, food exporters) into {LANGS[lang]}. "
              "Keep HTML tags (<br>, <em>, </em>) and entities (&amp;) exactly, keep brand names. Natural business tone, concise. "
              "Input is a JSON object {\"id\": \"text\"}. Return a JSON object with the same ids mapped to translations, nothing else.")
    payload = json.dumps({str(i): t for i, t in enumerate(items)}, ensure_ascii=False)
    for attempt in range(3):
        r = client.chat_completion(model="deepseek/deepseek-v3.2", messages=[{"role": "system", "content": prompt}, {"role": "user", "content": payload}],
                                   response_format={"type": "json_object"}, extra_body={"max_tokens": 6000})
        try:
            out = json.loads(r.message_content or "")
            return [out[str(i)] for i in range(len(items))]
        except (ValueError, KeyError):
            continue
    raise RuntimeError(f"{lang}: no valid answer")
def translate(lang):
    items = need[lang]
    chunks = [items[i:i + 20] for i in range(0, len(items), 20)]
    with ThreadPoolExecutor(5) as ex2:
        parts = list(ex2.map(lambda c: _batch(lang, c), chunks))
    return lang, dict(zip(items, [t for part in parts for t in part]))
with ThreadPoolExecutor(4) as ex:
    tr = dict(ex.map(translate, LANGS))
def fill(m):
    have = set(re.findall(r'<span class="(\w+)">', m.group(2)))
    extra = "".join(f'<span class="{l}">{tr[l][m.group(1)]}</span>' for l in LANGS if l not in have)
    return m.group(0) + extra
s = GROUP.sub(fill, s)
open(PATH, "w", encoding="utf-8").write(s)
print({l: len(v) for l, v in need.items()}, f"${client.usage_snapshot().cost:.4f}")
