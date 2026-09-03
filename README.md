# dontknowif.github.io — sito pubblico

Sito di **dontknowif** e dell'app **Recurr**, ospitato su GitHub Pages e online
su <https://dontknowif.github.io/>.

Contiene anche Privacy Policy e Termini e condizioni: sono documenti **pubblici e
gia in vigore**, non bozze. Vanno trattati con la stessa cura del codice di
produzione, e ogni modifica sostanziale richiede di aggiornare la data in cima
alla pagina.

## Regola di manutenzione

Questo file va aggiornato quando cambiano struttura del sito, strumenti collegati
(analytics, motori di ricerca) o le informazioni sull'app riportate nelle pagine.

**Il sito afferma dei numeri sull'app.** Se cambiano nel codice e non qui, il sito
diventa silenziosamente falso e nessuno se ne accorge. Da ricontrollare a ogni
modifica rilevante dell'app:

| Cosa dice il sito | Dove sta la verita nell'app |
|---|---|
| 8 spese gratis | `SpeseStore.freeLimit` |
| 57 voci nel catalogo di partenza | conteggio di `SpesaSuggerita(` in `Views/OnboardingView.swift` |
| 12 categorie di sistema | `Category.systemCatalog` |
| 5 lingue (IT, EN, ES, FR, DE) | `Localizable.xcstrings` |
| 9 tipi di segnalazione nel report | i rilevatori in `Engine/SavingsReportEngine.swift` (contali con `grep -c 'static func detect'`) |
| una sola valuta per l'app, scelta fra ~155 | `Valuta.tutte` e `SettingsView.applicaValuta` in `Model/UserSettings.swift` |
| iOS 17 o successivo | `IPHONEOS_DEPLOYMENT_TARGET` |
| Elenco eventi analytics nella Privacy Policy §3.1 | tutte le chiamate `Analytics.signal(` nell'app |

L'ultima riga e la piu delicata: aggiungere un evento analytics nell'app senza
elencarlo nella Privacy Policy rende la policy incompleta, e questo ha rilevanza
legale, non solo di forma.

## Struttura

```text
/                                  home: elenco delle app, volutamente generica
/robots.txt                        ammette esplicitamente i crawler AI
/sitemap.xml                       5 URL, con alternate hreflang
/llms.txt                          scheda fattuale dell'app per gli assistenti AI
/googlea082b78555501c8d.html       verifica Google Search Console
/BingSiteAuth.xml                  verifica Bing (copia anche in /spese-ricorrenti/)

/spese-ricorrenti/                 landing italiana — URL canonico dell'app
/spese-ricorrenti/en/              landing inglese
/spese-ricorrenti/privacy.html     Privacy Policy, bilingue IT/EN
/spese-ricorrenti/terms.html       Termini e condizioni, bilingue IT/EN
/spese-ricorrenti/style.css        stile base, condiviso con le pagine legali
/spese-ricorrenti/site.css         stile della sola landing
/spese-ricorrenti/og-image.png     anteprima social 1200x630
```

Il percorso contiene ancora `spese-ricorrenti` perche precede il rinominamento
dell'app in Recurr. E stato lasciato di proposito: cambiarlo obbligherebbe a
rifare la verifica su Bing e a reindicizzare tutto, e la parola chiave nell'URL ha
comunque valore. Se un giorno si passa a un dominio proprio, quello e il momento
giusto per sistemarlo.

### Due lingue, due URL

Le **landing** usano un URL per lingua, collegati da `hreflang` + `x-default`: e
la struttura che i motori di ricerca interpretano correttamente.

Le **pagine legali** usano invece un solo URL con entrambe le lingue nello stesso
HTML e un selettore JavaScript. E una struttura peggiore per l'indicizzazione, ma
sono documenti di riferimento, non pagine da posizionare. Se si tocca privacy o
termini, va aggiornato **il testo in entrambe le lingue** nello stesso file.

### Il mockup dell'iPhone

Nella landing la schermata dell'app e ricostruita in HTML/CSS, non e uno
screenshot. Gli importi mostrati sono coerenti fra loro: 650 + 12,99 + 39 + 84,20
= 786,19 € questo mese; il mese dopo la bolletta bimestrale non ricade, quindi
701,99 €. Se si cambiano i numeri vanno rifatti i conti, in entrambe le lingue.

## SEO e visibilita sulle AI

- Dati strutturati JSON-LD su ogni landing: `MobileApplication`, `Organization`,
  `WebSite`, `FAQPage`. Le domande nel JSON-LD devono **corrispondere parola per
  parola** a quelle visibili in pagina, altrimenti Google considera il markup
  ingannevole.
- `alternateName: "Spese Ricorrenti"` e volutamente rimasto nei dati strutturati:
  serve a farsi trovare da chi cerca il vecchio nome.
- Il marchio e "Recurr", ma le frasi descrittive dicono ancora "spese ricorrenti"
  in minuscolo: e la parola che la gente cerca davvero, mentre "Recurr" non lo
  cerca nessuno finche non conosce l'app. **Non sostituirla** in una futura
  ripulitura del nome.
- `llms.txt` riporta il link allo store e continua a dichiarare che **il prezzo
  non e stato annunciato**, cosi gli assistenti AI non inventano una cifra o un
  numero di recensioni. Se un giorno il prezzo viene comunicato pubblicamente, va
  aggiornato anche li.

## Link allo store

L'app e pubblicata dal 3 settembre 2026. I link usati nel sito non sono tutti
uguali, e la differenza e voluta:

| Dove | Link | Perche |
|---|---|---|
| Landing italiana | `apps.apple.com/it/app/recurr-spese-ricorrenti/id6806970079` | pubblico italiano: va diritto allo store italiano, senza redirect |
| Landing inglese e `llms.txt` | `apps.apple.com/app/id6806970079` | senza codice paese Apple reindirizza allo store del visitatore: l'app e in vendita in 175 store, e un lettore inglese non e detto sia negli Stati Uniti |

Il badge "App Store" nelle landing e un `<a class="store-badge">`, non piu uno
`<span>`: se si tocca quel blocco va tenuto il `text-decoration: none` in
`site.css`, altrimenti eredita la sottolineatura dei link.

## Analytics

**Cloudflare Web Analytics**, senza cookie: niente banner di consenso e nessuna
profilazione dei singoli visitatori. Il beacon e solo sulle due landing, non sulle
pagine legali. Il token nell'HTML e pubblico per definizione, non e un segreto.

Dati su <https://dash.cloudflare.com> → Analytics & Logs → Web Analytics.

Il tag e la sezione 13 della Privacy Policy ("Questo sito web") vanno tenuti
allineati: **se si toglie l'uno va tolta anche l'altra**, e viceversa. Non deve
mai esistere un momento in cui il sito misura senza dichiararlo.

Google Analytics e stato escluso di proposito: richiederebbe un banner cookie,
una sezione aggiuntiva nella policy, e contraddirebbe la dicitura "0 pubblicita e
tracker" scritta nella landing.

## Motori di ricerca

| | Proprieta | Stato |
|---|---|---|
| Google Search Console | `https://dontknowif.github.io/` (root) | Verificata via file HTML |
| Bing Webmaster Tools | `https://dontknowif.github.io/spese-ricorrenti/` | Verificata |

La sitemap sta nella root del dominio. Su Search Console va inviata dalla
proprieta root: una proprieta su un sottopercorso la rifiuta, perche i motori
accettano solo sitemap che stiano dentro il perimetro verificato. Per lo stesso
motivo, per inviarla anche a Bing serve aggiungere li una seconda proprieta sulla
root — il file di verifica e gia online, quindi si verifica al primo colpo.

**Passi ancora da fare a mano** (nessuno richiede modifiche al codice):

1. Search Console → Sitemap → inviare `sitemap.xml`.
2. Search Console → Controllo URL → richiedere l'indicizzazione di
   `/spese-ricorrenti/` e `/spese-ricorrenti/en/`. Senza questo, Google puo
   metterci settimane.
3. Bing → aggiungere la proprieta root e inviare la sitemap.

Il verificatore CNAME offerto da Bing **non e utilizzabile**: richiede di
modificare il DNS di `github.io`, che appartiene a GitHub.

## Anteprima locale

I CSS sono collegati con percorsi relativi, quindi aprire i file con `file://`
non basta: serve un server.

```bash
cd ~/Documents/spese-ricorrenti-legal && python3 -m http.server 8765
```

Poi <http://localhost:8765/spese-ricorrenti/>. Dopo il push, GitHub Pages impiega
uno o due minuti a pubblicare.

## Stato al 27 agosto 2026

Sito online e allineato con `origin/main`. Ultimo intervento: rinominamento in
Recurr e pulizia della home del dominio, che ora e un semplice elenco di app senza
riferimenti a una in particolare, pronta per le prossime.
