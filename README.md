# dontknowif.github.io — sito pubblico

Sito di **dontknowif** e dell'app **Skurda**, ospitato su GitHub Pages e online
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
| 5 secondi per annullare l'eliminazione di una spesa (card "Annulla eliminazione" in `funzionalita.html`) | `DashboardView.pendingDeleteWindow` |

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
/spese-ricorrenti/funzionalita.html  pagina funzionalità, IT/EN/ES/FR/DE — non indicizzata
/spese-ricorrenti/automazione-wallet.html  guida all'automazione Wallet→Skurda, IT/EN/ES/FR/DE — non indicizzata
/spese-ricorrenti/assets/wallet-guide/     screenshot e video della guida qui sopra
```

### La pagina "Funzionalità" non è pubblica

`/spese-ricorrenti/funzionalita.html` presenta le funzionalità dell'app (widget,
Siri, spese manuali, addebito automatico, pausa personalizzata, spese quotidiane)
in 5 lingue, ma
è **deliberatamente non indicizzata**: `<meta name="robots" content="noindex,
nofollow">`, nessuna voce in `sitemap.xml`, nessun link da `index.html` o dalle
altre pagine. Ci si arriva solo da un link nelle Impostazioni dell'app, che
apre l'URL con `?lang=<codice>` per aprirla già nella lingua corrente
dell'utente. Se un giorno diventa una pagina pubblica, va tolto il meta
`noindex`, aggiunta a `sitemap.xml` e — probabilmente — spezzata in un URL per
lingua come le landing, invece dell'unico file con tutte e 5 dentro.

Segue lo stesso pattern di selettore lingua di `privacy.html`
(`data-lang`/`data-set-lang`, salvataggio in `localStorage`), esteso da 2 a 5
lingue e con l'aggiunta della lettura di `?lang=` dall'URL come priorità
massima — le pagine legali non ne hanno bisogno perché non si aprono da un
link generato dall'app.

Il percorso contiene ancora `spese-ricorrenti` perche precede i rinominamenti
dell'app (prima in Recurr, poi in Skurda). E stato lasciato di proposito: cambiarlo
obbligherebbe a rifare la verifica su Bing e a reindicizzare tutto, e la parola
chiave nell'URL ha comunque valore. Se un giorno si passa a un dominio proprio,
quello e il momento giusto per sistemarlo.

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
- Il marchio e "Skurda", ma le frasi descrittive dicono ancora "spese ricorrenti"
  in minuscolo: e la parola che la gente cerca davvero, mentre "Skurda" non lo
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

## Stato al 5 settembre 2026

Secondo rinominamento dell'app, da Recurr a **Skurda** (il primo, da "Spese
Ricorrenti" a Recurr, risale ad agosto), pubblicato insieme al rilascio della
build con il nuovo nome. Il lavoro era stato preparato il 4 settembre e tenuto
fermo di proposito fino all'approvazione di Apple, per non avere un periodo in
cui il sito diceva Skurda e lo store ancora Recurr.

Sostituito il brand in tutte le pagine HTML (landing IT/EN, `funzionalita.html`,
`privacy.html`, `terms.html`, home del dominio) e nella documentazione
(`llms.txt`, questo file), lasciando invariati i termini generici
("ricorrenti"/"recurring") e gli URL App Store correnti, che contengono ancora
`recurr` nello slug e cambieranno se Apple li aggiorna in autonomia — non e
garantito che lo faccia, quindi vanno ricontrollati fra qualche giorno.

Nella stessa passata, la card "Pausa personalizzata" di `funzionalita.html` e
stata riscritta nelle cinque lingue con un esempio concreto (lo sport del figlio
che si ferma d'estate) e un mockup nuovo, `.pause-mock`: la riga di una spesa in
pausa con badge arancione e data di ripresa, nello stesso linguaggio visivo
degli altri mockup ricostruiti in HTML/CSS.

## Stato al 10 settembre 2026

Aggiunte due card a `funzionalita.html`, in tutte e 5 le lingue, per due
funzionalità nuove dell'app: **Annulla eliminazione** (swipe-to-delete con 5
secondi per tornare indietro prima che la spesa sparisca davvero) e **Storico
prezzi** (una card in fondo alla scheda spesa con i prezzi precedenti e quando
sono cambiati). Due nuovi mockup HTML/CSS, `.undo-mock` e `.history-mock`,
stesso principio degli altri: nessuno screenshot, solo ricostruzioni fedeli
allo stile reale dell'app.

I testi dei mockup riprendono le stringhe vere dell'app invece di inventarne
di nuove: il bottone "Annulla"/"Cancel"/"Cancelar"/"Annuler"/"Abbrechen" e la
frase `"%@" eliminata` sono le stesse di `Localizable.xcstrings`, comprese le
virgolette tipografiche per francese (`« … »`) e tedesco (`„…"`).

## Stato al 17-20 settembre 2026

Aggiornamento del sito per la **versione 3.0** dell'app, che introduce le spese
quotidiane (automatiche via automazione Wallet, da foto scontrino, o a mano)
accanto alle spese ricorrenti. Preparato il 17 settembre e tenuto **di
proposito non pubblicato** fino al via libera dell'utente (stesso schema già
usato per il rename Recurr→Skurda, vedi sopra) — l'app non era ancora andata
live con la 3.0. **Pubblicato il 20 settembre 2026**, commit `a622976`, dopo
che l'utente ha confermato che l'app è live sullo Store.

Tocchi fatti:

- **`funzionalita.html`**: nuova card "Spese quotidiane" (5 lingue), con un
  nuovo mockup `.daily-modes` — tre badge (automatica, scontrino, a mano) sullo
  stesso principio visivo di `.tp-badge`. Testo adattato da quello già scritto
  e approvato per `fastlane/metadata/*/description.txt` nell'app.
- **`automazione-wallet.html`**: aggiunta una riga che spiega cosa succede a un
  pagamento che non corrisponde a nessuna spesa ricorrente — diventa una spesa
  quotidiana invece di andare perso. Prima non lo diceva.
- **Landing IT/EN**: title/meta/OG/Twitter aggiornati, `featureList` e
  `applicationSubCategory` nel JSON-LD estesi, una nuova card in `#funzioni`,
  una nuova FAQ sulle spese quotidiane e la FAQ "si collega alla banca?"
  precisata per menzionare l'automazione Wallet — in entrambi i casi il testo
  è identico parola per parola fra JSON-LD e HTML visibile (verificato con
  uno script, non solo a occhio).
- **`privacy.html`** (bilingue IT/EN): la sezione "Cosa non facciamo" diceva
  che l'app non accede alle foto — non più vero con lo scontrino fotografato,
  corretto. Aggiunto un paragrafo nella sezione 2 che spiega l'OCR on-device
  (Vision) per lo scontrino — l'immagine non viene mai salvata né trasmessa —
  e uno sul fatto che l'automazione Wallet parla con l'app tramite URL scheme
  locale, senza server.
- **`llms.txt`**: nuova sezione "Daily expenses" con le tre modalità, intro e
  "What the app does NOT do" aggiornati di conseguenza.
- **Home del dominio** (`index.html` root): riga descrittiva di Skurda
  aggiornata per menzionare anche le spese quotidiane.
- **Nome dell'app**: secondo quanto indicato dall'utente, il nome pubblico è
  ora, per lingua: IT "Skurda - Gestione Spese Budget", FR "Skurda - Suivi des
  Dépenses", DE "Skurda - Haushaltsbuch Budget", ES "Skurda - Control de
  Gastos" (EN invariato, "Skurda - All your expenses" da fastlane). **Nota di
  disallineamento scoperta durante il lavoro**: `fastlane/metadata/it/name.txt`
  nel repo dell'app ha invece "Skurda - Spese in tasca" (deciso e caricato su
  App Store Connect il 16 settembre 2026, vedi `ROADMAP.md` dell'app,
  sezione «Versione 3.0») — il sito non mostra comunque la stringa completa
  "Skurda - X" in nessun punto letterale, quindi qui non c'è stato bisogno di
  scegliere fra le due; ma se `fastlane/metadata/it/name.txt` non viene
  allineato al nuovo nome, resta un disallineamento fra quello che l'utente
  intende e cosa dice davvero l'App Store.

Volutamente non toccati in questa sessione: `terms.html` (nessuna clausola
dipende dalle spese quotidiane), gli screenshot marketing su App Store Connect
(fuori da questo repo, già preparati dall'utente in
`Screenshot Marketing Quotidiane/`), e i benefici del paywall su RevenueCat
(dashboard, non file di questo repo).

## Stato al 21 settembre 2026

L'utente ha segnalato che il sito era rimasto indietro rispetto alla **versione
3.1** dell'app (share extension "Condividi scontrino", pubblicata lo stesso
giorno): mancava ovunque il quarto modo di registrare una spesa quotidiana,
oltre ad automatico/foto/a mano.

- **Landing IT/EN**: hero, card "Le spese di ogni giorno"/"Everyday expenses",
  FAQ "Come funzionano le spese quotidiane?" e relativo JSON-LD (`featureList`
  e testo della FAQ, verificati identici parola per parola con uno script)
  aggiornati per menzionare la condivisione dello screenshot dal foglio
  "Condividi" di iOS.
- **`funzionalita.html`**, tutte e 5 le lingue: nuovo badge "Condividi" (icona
  share, colore verde `#e4f6ea`/`#2ba14f`, nuova classe `.tp-badge.share`)
  inserito fra "Automatica" e "Scontrino" nella card "Spese quotidiane"; testo
  aggiornato da "tre modi" a "più modi" in tutte le lingue.
- **`automazione-wallet.html`**, tutte e 5 le lingue: nuovo paragrafo dopo la
  spiegazione di cosa succede a un pagamento senza corrispondenza, che
  segnala la condivisione dello screenshot come alternativa per chi preferisce
  non configurare l'automazione.
- **`llms.txt`**: sezione "Daily expenses" aggiornata da "Three ways" a
  quattro, con la nuova voce introdotta in versione 3.1; aggiornata anche la
  riga di sintesi in cima al file.
- **Correzione non collegata, trovata mentre si verificava il file**:
  `llms.txt` dichiarava bundle id (`it.dontknowif.SpeseRicorrenti`), container
  iCloud e entitlement RevenueCat (`Spese Ricorrenti Pro`) come se fossero
  rimasti fermi al nome originale — nel codice sono invece fermi al **primo**
  rename, `Recurr` (`it.dontknowif.Recurr`, `iCloud.it.dontknowif.Recurr`,
  `Recurr Pro`). Corretto.

Verificato in anteprima locale (`python3 -m http.server`) che i 4 badge non
rompono il layout della card, in italiano e in inglese.

**Correzione successiva, stessa giornata**: la card privacy "Statistiche
disattivabili"/"Statistics you can switch off" e la FAQ "Ci sono pubblicità o
tracciamento?" (landing IT/EN, testo visibile e JSON-LD) dicevano ancora che
un interruttore in Opzioni spegne le statistiche — falso dal **04/09/2026**,
quando quel toggle è stato rimosso dall'app e `privacy.html` aggiornata di
conseguenza (commit `983e69b`, vedi `ROADMAP.md` dell'app, sezione
«Rimozione del toggle statistiche d'uso»): l'opposizione si esercita solo
scrivendo a `feedbacksr@icloud.com`, senza garanzia tecnica di poter fermare
la raccolta per un singolo dispositivo. Le landing e `llms.txt` non erano
mai stati allineati a quel cambiamento. Corretto ora in entrambe le lingue e
in `llms.txt`, con lo stesso testo di `privacy.html` §7.

**Quarta correzione, stessa giornata**: la sezione Prezzi (piano Premium e
FAQ "L'app è gratuita?", testo visibile + JSON-LD, IT+EN) non menzionava le
spese quotidiane da nessuna parte, pur essendo una funzione Premium dal
lancio della 3.0 — segnalato dall'utente con uno screenshot della card
Premium. Aggiunta una riga alla lista Premium e un inciso alla FAQ, in
entrambe le lingue.

**Quinta correzione, stessa giornata**: la primissima FAQ, "Che cos'è
Skurda?" — quella aperta di default, la prima cosa che chi arriva sul sito
legge — descriveva l'app come se facesse solo spese ricorrenti, senza una
parola sulle quotidiane. Segnalato dall'utente con uno screenshot.
Riscritta per presentare entrambi i tipi di spesa fin dall'inizio, IT+EN,
testo visibile e JSON-LD verificati identici.
