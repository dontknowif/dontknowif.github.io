#!/usr/bin/env python3
"""Aggiunge a privacy.html e support.html i meta per i social, i robots e i dati
strutturati (JSON-LD). Il blocco sta tra <!-- SEO:inizio --> e <!-- SEO:fine -->
e viene riscritto a ogni esecuzione.

La FAQPage di support.html è ricavata dal testo italiano visibile della pagina
(h3 + paragrafo seguente): dopo aver cambiato le domande frequenti, rilanciare
questo script dalla cartella piano-di-cura/:  python3 _sorgenti/seo-pagine-legali.py
"""
import html
import json
import re
from datetime import date

BASE = "https://dontknowif.github.io/piano-di-cura/"
APP = BASE + "#app"
PUB = "https://dontknowif.github.io/#publisher"


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
    mesi = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio",
            "agosto", "settembre", "ottobre", "novembre", "dicembre"]
    m = re.search(r"Ultimo aggiornamento: (\d+) (\w+) (\d{4})", s)
    return date(int(m.group(3)), mesi.index(m.group(2)) + 1, int(m.group(1))).isoformat()


def blocco(titolo, descrizione, url, grafo):
    e = lambda x: html.escape(x, quote=True)
    ld = json.dumps({"@context": "https://schema.org", "@graph": grafo}, ensure_ascii=False, indent=2)
    return f"""<!-- SEO:inizio (generato da _sorgenti/seo-pagine-legali.py) -->
<meta name="robots" content="index, follow, max-snippet:-1">
<meta name="author" content="Rocco Barletta">
<meta name="theme-color" content="#1f73c4">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Piano di Cura">
<meta property="og:locale" content="it_IT">
<meta property="og:locale:alternate" content="en_GB">
<meta property="og:title" content="{e(titolo)}">
<meta property="og:description" content="{e(descrizione)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(titolo)}">
<meta name="twitter:description" content="{e(descrizione)}">
<meta name="twitter:image" content="{BASE}og-image.png">
<script type="application/ld+json">
{ld}
</script>
<!-- SEO:fine -->"""


def aggiorna(nome, costruisci):
    s = open(nome, encoding="utf-8").read()
    s = re.sub(r"\n<!-- SEO:inizio.*?<!-- SEO:fine -->", "", s, flags=re.S)
    titolo = testo(re.search(r"<title>(.*?)</title>", s, re.S).group(1))
    descr = html.unescape(re.search(r'<meta name="description" content="(.*?)">', s).group(1))
    url = re.search(r'<link rel="canonical" href="(.*?)">', s).group(1)
    nuovo = blocco(titolo, descr, url, costruisci(s, titolo, descr, url))
    s = s.replace(f'<link rel="canonical" href="{url}">',
                  f'<link rel="canonical" href="{url}">\n{nuovo}', 1)
    open(nome, "w", encoding="utf-8").write(s)
    print("scritto", nome)


def pagina_web(tipo, s, titolo, descr, url, extra=None):
    p = {"@type": tipo, "@id": url + "#page", "url": url, "name": titolo, "description": descr,
         "inLanguage": ["it", "en"], "isPartOf": {"@id": BASE + "#website"},
         "about": {"@id": APP}, "publisher": {"@id": PUB}}
    p.update(extra or {})
    return p


def privacy(s, titolo, descr, url):
    return [
        pagina_web("WebPage", s, titolo, descr, url, {"dateModified": ultimo_aggiornamento(s)}),
        {"@type": "MobileApplication", "@id": APP, "name": "Piano di Cura", "url": BASE,
         "operatingSystem": "iOS 17.0+", "applicationCategory": "HealthApplication",
         "privacyPolicy": url},
    ]


def supporto(s, titolo, descr, url):
    faq = faq_italiane(s)
    return [
        pagina_web("ContactPage", s, titolo, descr, url),
        {"@type": "Organization", "@id": PUB, "name": "dontknowif", "url": "https://dontknowif.github.io/",
         "email": "feedbacksr@icloud.com",
         "contactPoint": {"@type": "ContactPoint", "contactType": "customer support",
                          "email": "feedbacksr@icloud.com", "availableLanguage": ["Italian", "English"]}},
        {"@type": "FAQPage", "@id": url + "#faq", "inLanguage": "it",
         "mainEntity": [{"@type": "Question", "name": q,
                         "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ]


if __name__ == "__main__":
    aggiorna("privacy.html", privacy)
    aggiorna("support.html", supporto)
