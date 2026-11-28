Skurda – Video Kit per YouTube Shorts (agente settimanale)
App
Skurda: app iOS di Rocco (sviluppatore indipendente italiano) per tracciare spese ricorrenti e spese quotidiane.
Punto forte: un'automazione dei Comandi (Shortcuts) registra in automatico i pagamenti Apple Pay / Wallet.
Nessun collegamento alla banca; dati sul dispositivo / iCloud. Gratis fino a 10 spese ricorrenti; Premium opzionale.
Link app: https://apps.apple.com/app/id6806970079
Codice offerta: SKURDAFREE2M = 2 mesi di Premium gratis Link riscatto: https://apps.apple.com/redeem?ctx=offercodes&id=6806970079&code=SKURDAFREE2M
Regole per i video
Formato: 1080×1920, 30 fps, 15–20 s, MP4 H.264. Nessuna musica protetta da copyright.
Stile: sfondo blu notte con gradiente, testo bianco font Inter, accento gradiente 
#8f9bff → 
#5ee1b5, telefono mockup arrotondato.
Struttura: hook (0–3 s) → problema/demo → beneficio Skurda → CTA finale (logo, "Gratis su App Store", codice SKURDAFREE2M, "Cerca «Skurda» su App Store").
Nei Shorts i link NON sono cliccabili: la CTA nel video dice di cercare "Skurda" su App Store.
L'interfaccia nel telefono è un mockup illustrativo: non inventare funzioni che l'app non ha (es. non promettere promemoria di rinnovo, sync bancario, grafici avanzati se non confermati da Rocco).
Prezzi/voci negli esempi sono generici, senza marchi di terzi.
Dal 28/11/2026 tutti gli Shorts parlano dell'automazione di iOS 27 (vedi AUTOMAZIONE_PRIMO_MESSAGGIO in LOG.md): si varia l'angolo, non il tema. Temi usati prima, ora solo come contorno: Apple Pay automatico, abbonamenti dimenticati, caffè al giorno × anno, budget mensile, privacy senza banca, spese fisse vs variabili, "regola delle 24 ore", fine mese in rosso.
Lingue a rotazione: IT → DE → FR → EN. Formati numeri: IT "€ 1.248,30", DE "1.248,30 €", FR "1 248,30 €" (spazio non separabile normale, non U+202F), EN "€1,248.30".
Strumenti
render.py <html> <out.mp4> <durata> renderizza un HTML con funzione globale render(t) (t in secondi) in MP4 via Playwright + ffmpeg (aggiunge traccia audio muta). Modalità anteprima: render.py <html> <prefisso> 0 preview 1,5,9 → PNG ai tempi indicati (controllare SEMPRE le anteprime prima del render finale).
template_v1_applepay_IT.html, template_v2_abbonamenti_IT.html: esempi completi da cui partire.
localize_example.py: esempio di localizzazione per sostituzione testi + formattazione valuta.
Pubblicazione
Pubblicazione tramite connettore Metricool (canale YouTube collegato da Rocco). Pubblicare/programmare è un'azione pubblica: serve l'ok esplicito di Rocco per ogni batch prima di creare i post programmati.
Titolo ≤100 caratteri con #shorts; descrizione con link app, codice e hashtag nella lingua del video.
Notifiche di iOS 27 (dalla 3.9.4, provate su iPhone vero; aggiunto il 09/11/2026)
Da iOS 27 un'automazione dei Comandi («Quando ricevo una notifica da [app]») passa a Skurda le notifiche di pagamento delle app che l'utente sceglie (banca, carta, Wallet): Skurda le legge sul telefono e crea la spesa. Si può dire: «su iOS 27 anche le notifiche di banche e carte», «solo le app che scegli tu», «letta sul tuo iPhone», «nessun accesso alla banca», «dopo una configurazione una tantum». Frase privacy approvata: «Skurda legge sul tuo iPhone solo le notifiche di pagamento delle app che scegli, per creare la spesa. Non le inviamo a nessuno.»
NON dire: «legge tutte le notifiche», «funziona con tutte le banche» (provate solo alcune), «non raccogliamo dati», «senza configurare niente», nomi di banche vere. Serve iOS 27.
