#!/usr/bin/env python3
"""Meta social, robots e dati strutturati (JSON-LD) per le pagine scritte a mano
delle app (privacy, termini, supporto). Il blocco sta tra <!-- SEO:inizio --> e
<!-- SEO:fine --> e viene riscritto a ogni esecuzione: il resto della pagina non
si tocca.

- La data (dateModified) viene da «Ultimo aggiornamento: …» nella pagina.
- Per le pagine di supporto la FAQPage è ricavata dal testo italiano visibile
  (h3 + paragrafo seguente sotto «Domande frequenti»).

Dopo aver modificato una di queste pagine, rilanciare dalla radice del repo:
    python3 _sorgenti/seo-pagine-legali.py
(Jekyll non pubblica le cartelle che iniziano con «_».)
"""
import html
import json
import os
import re
from datetime import date

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITO = "https://dontknowif.github.io/"
PUB = SITO + "#publisher"

APP = {
    "piano-di-cura": {"nome": "Piano di Cura", "colore": "#1f73c4", "os": "iOS 17.0+",
                      "categoria": "HealthApplication"},
    "spese-ricorrenti": {"nome": "Skurda", "colore": "#5ba8f1", "os": "iOS 17.0+",
                         "categoria": "FinanceApplication"},
    "homeoffice": {"nome": "HomeOffice", "colore": "#5856d6", "os": "iOS 18.0+",
                   "categoria": "BusinessApplication"},
}

# (cartella, file, tipo): tipo = "privacy", "termini" o "supporto"
PAGINE = [
    ("piano-di-cura", "privacy.html", "privacy"),
    ("piano-di-cura", "support.html", "supporto"),
    ("spese-ricorrenti", "privacy.html", "privacy"),
    ("spese-ricorrenti", "terms.html", "termini"),
    ("homeoffice", "privacy.html", "privacy"),
]

MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio",
        "agosto", "settembre", "ottobre", "novembre", "dicembre"]


def testo(frammento):
    """HTML -> testo semplice su una riga, come lo legge un utente."""
    t = re.sub(r"<[^>]+>", "", frammento)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def faq_italiane(s):
    it = s.split('<div data-lang="it">', 1)[1].split('<div data-lang="en"', 1)[0]
    faq = it.split("<h2>Domande frequenti</h2>", 1)[1].split("<h2>", 1)[0]
    coppie = re.findall(r"<h3>(.*?)</h3>\s*<p>(.*?)</p>", faq, re.S)
    assert coppie, "nessuna FAQ trovata"
    return [(testo(q), testo(a)) for q, a in coppie]


def ultimo_aggiornamento(s):
    m = re.search(r"Ultimo aggiornamento: (\d+) (\w+) (\d{4})", s)
    if not m:
        return None
    return date(int(m.group(3)), MESI.index(m.group(2)) + 1, int(m.group(1))).isoformat()


def blocco(app, base, titolo, descrizione, url, grafo):
    e = lambda x: html.escape(x, quote=True)
    ld = json.dumps({"@context": "https://schema.org", "@graph": grafo}, ensure_ascii=False, indent=2)
    return f"""<!-- SEO:inizio (generato da _sorgenti/seo-pagine-legali.py) -->
<meta name="robots" content="index, follow, max-snippet:-1">
<meta name="author" content="Rocco Barletta">
<meta name="theme-color" content="{app['colore']}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(app['nome'])}">
<meta property="og:locale" content="it_IT">
<meta property="og:locale:alternate" content="en_GB">
<meta property="og:title" content="{e(titolo)}">
<meta property="og:description" content="{e(descrizione)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{base}og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(titolo)}">
<meta name="twitter:description" content="{e(descrizione)}">
<meta name="twitter:image" content="{base}og-image.png">
<script type="application/ld+json">
{ld}
</script>
<!-- SEO:fine -->"""


def grafo(tipo, app, base, s, titolo, descr, url):
    app_id = base + "#app"
    pagina = {"@type": "ContactPage" if tipo == "supporto" else "WebPage", "@id": url + "#page",
              "url": url, "name": titolo, "description": descr, "inLanguage": ["it", "en"],
              "about": {"@id": app_id}, "publisher": {"@id": PUB}}
    data = ultimo_aggiornamento(s)
    if data:
        pagina["dateModified"] = data
    applicazione = {"@type": "MobileApplication", "@id": app_id, "name": app["nome"], "url": base,
                    "operatingSystem": app["os"], "applicationCategory": app["categoria"]}
    if tipo == "privacy":
        applicazione["privacyPolicy"] = url
    if tipo == "termini":
        applicazione["termsOfService"] = url
    nodi = [pagina, applicazione]
    if tipo == "supporto":
        nodi.append({"@type": "Organization", "@id": PUB, "name": "dontknowif", "url": SITO,
                     "email": "feedbacksr@icloud.com",
                     "contactPoint": {"@type": "ContactPoint", "contactType": "customer support",
                                      "email": "feedbacksr@icloud.com",
                                      "availableLanguage": ["Italian", "English"]}})
        nodi.append({"@type": "FAQPage", "@id": url + "#faq", "inLanguage": "it",
                     "mainEntity": [{"@type": "Question", "name": q,
                                     "acceptedAnswer": {"@type": "Answer", "text": a}}
                                    for q, a in faq_italiane(s)]})
    return nodi


def aggiorna(cartella, nome, tipo):
    app, base = APP[cartella], f"{SITO}{cartella}/"
    percorso = os.path.join(RADICE, cartella, nome)
    s = open(percorso, encoding="utf-8").read()
    s = re.sub(r"\n<!-- SEO:inizio.*?<!-- SEO:fine -->", "", s, flags=re.S)
    titolo = testo(re.search(r"<title>(.*?)</title>", s, re.S).group(1))
    descr = re.sub(r"\s+", " ", html.unescape(re.search(r'<meta name="description" content="(.*?)">', s, re.S).group(1)))
    url = re.search(r'<link rel="canonical" href="(.*?)">', s).group(1)
    nuovo = blocco(app, base, titolo, descr, url, grafo(tipo, app, base, s, titolo, descr, url))
    s = s.replace(f'<link rel="canonical" href="{url}">', f'<link rel="canonical" href="{url}">\n{nuovo}', 1)
    open(percorso, "w", encoding="utf-8").write(s)
    print("scritto", f"{cartella}/{nome}")


if __name__ == "__main__":
    for c, n, t in PAGINE:
        aggiorna(c, n, t)
