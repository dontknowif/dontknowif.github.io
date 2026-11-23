#!/usr/bin/env python3
"""Genera le landing di Piano di Cura (IT in piano-di-cura/index.html, EN in piano-di-cura/en/index.html).

Tutti i testi stanno qui, in un solo posto. Lo script verifica da solo che le FAQ del JSON-LD
siano identiche parola per parola a quelle visibili in pagina (regola di Google sui dati strutturati).

Uso, dalla radice del repo:  python3 piano-di-cura/_sorgenti/genera-landing.py

La cartella _sorgenti inizia con "_" apposta: GitHub Pages (Jekyll) non la pubblica.

Quando l'app esce su App Store: mettere APP_STORE_ID qui sotto e rigenerare. Il badge
"Presto su App Store" diventa un link, i testi "in arrivo" diventano "disponibile".
"""
import html
import json
import os

APP_STORE_ID = ""  # es. "6830000000" quando l'app è pubblicata

BASE = "https://dontknowif.github.io/piano-di-cura/"
QUI = os.path.dirname(os.path.abspath(__file__))
CARTELLA = os.path.dirname(QUI)

APPLE_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16.365 1.43c0 1.14-.493 2.27-1.177 3.08-.744.9-1.99 '
             '1.57-2.987 1.57-.12 0-.23-.02-.3-.03-.01-.06-.04-.22-.04-.39 0-1.15.6-2.28 1.22-3 .78-.93 2.07-1.6 3.14-1.64.02.06.04.24.04.4zm4.565 '
             '15.71c-.03.07-.463 1.58-1.518 3.12-.945 1.34-1.94 2.71-3.43 2.71-1.517 0-1.9-.88-3.63-.88-1.698 0-2.302.91-3.67.91-1.377 '
             '0-2.332-1.26-3.428-2.8-1.287-1.82-2.323-4.63-2.323-7.28 0-4.28 2.797-6.55 5.552-6.55 1.448 0 2.675.95 3.6.95.865 0 2.222-1.01 '
             '3.902-1.01.613 0 2.886.06 4.374 2.19-.13.09-2.383 1.37-2.383 4.19 0 3.26 2.854 4.42 2.955 4.45z"/></svg>')

ICONE = {
    "piani": '<path d="M4 7h16M4 12h16M4 17h10"/><circle cx="19" cy="17" r="2"/>',
    "ripeti": '<path d="M4 12a8 8 0 0 1 14-5.3L20 9"/><path d="M20 4v5h-5"/><path d="M20 12a8 8 0 0 1-14 5.3L4 15"/><path d="M4 20v-5h5"/>',
    "prima": '<path d="M9 6h11M9 12h11M9 18h11"/><path d="M4 6l1 1 2-2M4 12l1 1 2-2"/><circle cx="5" cy="18" r="1.2"/>',
    "campana": '<path d="M12 2a7 7 0 0 0-7 7c0 3.5-1.5 5-2 5.5h18c-.5-.5-2-2-2-5.5a7 7 0 0 0-7-7Z"/><path d="M10 18.5a2 2 0 0 0 4 0"/>',
    "modelli": '<rect x="3" y="3" width="8" height="8" rx="2"/><rect x="13" y="3" width="8" height="8" rx="2"/><rect x="3" y="13" width="8" height="8" rx="2"/><path d="M17 14v6M14 17h6"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "medico": '<path d="M5 4v5a5 5 0 0 0 10 0V4"/><path d="M10 14v2a4 4 0 0 0 8 0v-2"/><circle cx="18" cy="12" r="2"/>',
    "documenti": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
    "widget": '<rect x="3" y="3" width="8" height="8" rx="2"/><rect x="13" y="3" width="8" height="8" rx="2"/><rect x="3" y="13" width="18" height="8" rx="2"/>',
    "scudo": '<path d="M12 3 4.5 6v6c0 4.5 3.2 7.9 7.5 9 4.3-1.1 7.5-4.5 7.5-9V6L12 3Z"/><path d="M9 12.2l2 2 4-4.2"/>',
    "no": '<circle cx="12" cy="12" r="9"/><path d="M5.6 5.6l12.8 12.8"/>',
    "lucchetto": '<rect x="4" y="10" width="16" height="11" rx="3"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    "invio": '<path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4z"/>',
}

T = {
    "it": {
        "lang": "it", "og_locale": "it_IT", "og_alt": "en_GB", "url": BASE, "prefix": "",
        "title": "Piano di Cura — Visite, esami e farmaci su iPhone",
        "description": "App iPhone per chi segue una cura: visite, esami, ritiro dei farmaci e terapie che si ripetono, con le cose da fare prima (impegnativa, prenotazione, viaggio) e promemoria che tornano finché non le hai fatte. Dati solo su iPhone e iCloud. In arrivo entro fine 2026.",
        "og_description": "Visite, esami e farmaci in un unico posto, con le cose da fare prima e promemoria che non ti lasciano dimenticare nulla. In arrivo su App Store entro fine 2026.",
        "nav": ["Funzioni", "Privacy", "FAQ"],
        "eyebrow": "In arrivo su App Store entro fine 2026",
        "h1": 'Visite, esami e farmaci,<br><span class="grad">senza dimenticare nulla.</span>',
        "sub": "Chi segue una cura lo sa: prima della visita c'è l'impegnativa da chiedere, il prelievo da prenotare, il farmaco da ritirare. <strong>Piano di Cura mette in fila ogni appuntamento con le cose da fare prima</strong> e ti ricorda ciascuna al momento giusto, finché non l'hai fatta.",
        "soon_small": "Presto su", "soon_big": "App Store",
        "out_small": "Scarica su", "out_big": "App Store",
        "notify": "Avvisami quando esce",
        "notify_subject": "Avvisami quando esce Piano di Cura",
        "note": "Per iPhone, iOS 17 o successivo · Nessun account · Italiano, inglese, spagnolo, tedesco, francese",
        "facts": [("8", "modelli pronti per le cure più comuni"), ("1", "posto per appuntamenti, medici e documenti"),
                  ("5", "lingue: IT, EN, ES, DE, FR"), ("0", "server, account e pubblicità")],
        "feat_h": "Tutto il tuo piano di cura, in ordine",
        "feat_p": "Pensata per chi ha visite, esami e terapie che si ripetono e vuole smettere di tenere tutto a mente.",
        "features": [
            ("piani", "Un piano per ogni patologia", "Più piani di cura, ognuno con i suoi appuntamenti, specialisti e documenti. Il medico di base è uno solo e vale per tutti."),
            ("ripeti", "Appuntamenti che si ripetono", "Visite, esami, ritiro dei farmaci, terapie: ogni quanti giorni, settimane, mesi o anni vuoi, con l'orario se serve. Segni fatto e l'app fissa la volta successiva."),
            ("prima", "Le cose da fare prima", "Per ogni appuntamento, quello che va fatto in anticipo: chiedere l'impegnativa, prenotare, ritirare, organizzare il viaggio. Ognuna con il suo anticipo."),
            ("campana", "Promemoria che insistono", "Una notifica all'orario che scegli. Se non segni una cosa come fatta, il promemoria torna ogni qualche giorno fino all'appuntamento."),
            ("modelli", "Modelli pronti", "Farmaco ospedaliero, esami del sangue, visita di controllo, esame annuale, rinnovo del piano terapeutico, vaccino, esenzione, terapia periodica: scegli e adatti."),
            ("mail", "Mail al medico già scritte", "La richiesta dell'impegnativa con l'elenco degli esami, a uno o più destinatari, firmata con il tuo nome. La rileggi e la invii dalla tua posta."),
            ("medico", "Medici a portata di mano", "Medico di base e specialisti con telefono, email e orari dello studio. Li chiami o gli scrivi con un tocco."),
            ("documenti", "Documenti sempre con te", "Referti, ricette e piani terapeutici in PDF o foto, anche da Condividi in qualsiasi app. Li alleghi alla mail quando servono."),
            ("widget", "Agenda, widget e Calendario", "«Prossime» mostra cosa è in ritardo, cosa c'è questa settimana, entro un mese e più avanti. Widget per la Home e il Blocco schermo, e Aggiungi al Calendario."),
        ],
        "priv_h": "I tuoi dati di salute restano tuoi",
        "priv_p": "Visite, esami e terapie sono tra le informazioni più personali che esistano. Per questo Piano di Cura è costruita così.",
        "privacy": [
            ("scudo", "Nessun nostro server", "Tutto sta sul tuo iPhone e, se vuoi, nel <strong>tuo</strong> iCloud personale, direttamente fra te e Apple. Noi non vediamo niente."),
            ("no", "Nessuna pubblicità, nessun tracking", "L'app non contiene reti pubblicitarie e non ti traccia. Raccoglie solo statistiche d'uso anonime, mai dati sanitari."),
            ("lucchetto", "Nessun account", "Non serve registrarsi. Il tuo nome, se lo scrivi, serve solo a firmare le mail ai medici."),
            ("invio", "Le mail partono da te", "L'app prepara il testo, tu lo rileggi e lo invii dalla tua casella. Nessuna copia passa da noi."),
        ],
        "priv_more": 'Tutti i dettagli sono nella <a href="{p}privacy.html">Privacy Policy</a>.',
        "faq_h": "Domande frequenti",
        "faq": [
            ("Che cos'è Piano di Cura?", "È un'app per iPhone per chi segue una cura nel tempo: visite di controllo, esami del sangue, ritiro di farmaci ospedalieri, terapie periodiche, rinnovi di piani terapeutici ed esenzioni. Per ogni appuntamento elenchi le cose da fare prima, come chiedere l'impegnativa o prenotare, e l'app ti ricorda ciascuna al momento giusto."),
            ("Quando esce?", "Piano di Cura è in arrivo su App Store entro la fine del 2026, per iPhone con iOS 17 o versione successiva. Se vuoi un avviso il giorno dell'uscita, scrivici a feedbacksr@icloud.com."),
            ("Posso seguire più patologie?", "Sì. Puoi creare più piani di cura, per esempio uno per ogni patologia, ognuno con i suoi appuntamenti, specialisti e documenti. L'agenda «Prossime» li mostra tutti insieme oppure uno alla volta."),
            ("Come funzionano i promemoria?", "Ogni cosa da fare ha il suo anticipo, per esempio prenotare il prelievo un mese prima degli esami. Ricevi una notifica all'orario che scegli e, se non la segni come fatta, il promemoria torna ogni qualche giorno fino all'appuntamento. Puoi scegliere ogni quanto, oppure disattivarlo."),
            ("Posso scrivere al medico dall'app?", "Sì. L'app prepara la mail per chiedere l'impegnativa o la ricetta, con l'elenco degli esami e il tuo nome, a uno o più destinatari. La mail si apre nella tua app di posta: la rileggi, la modifichi se vuoi e la invii tu."),
            ("Dove finiscono i miei dati?", "Restano nella memoria del tuo iPhone e, se lo vuoi, vengono sincronizzati nel tuo account iCloud personale, così li ritrovi sugli altri dispositivi con lo stesso Apple Account. Non esiste alcun server dello sviluppatore e l'app non contiene pubblicità. Raccoglie solo statistiche d'uso anonime, che non contengono mai dati sanitari."),
            ("Piano di Cura sostituisce il medico?", "No. Piano di Cura è un'agenda personale: ti aiuta a ricordare appuntamenti e cose da fare, ma non dà indicazioni mediche, non è un dispositivo medico e non sostituisce il parere del medico o del farmacista."),
            ("In quali lingue è disponibile?", "L'app è disponibile in italiano, inglese, spagnolo, tedesco e francese, e segue la lingua impostata sull'iPhone. Le date e gli orari sono nel formato del tuo Paese."),
        ],
        "closing_h": "In arrivo entro fine 2026",
        "closing_p": "Piano di Cura sta per arrivare su App Store. Vuoi un avviso il giorno dell'uscita, o hai un'idea da suggerirci? Scrivici.",
        "closing_h_out": "Disponibile su App Store",
        "closing_p_out": "Piano di Cura è disponibile su App Store. Per domande o per segnalarci qualcosa puoi scriverci quando vuoi.",
        "footer": ["Privacy Policy", "Supporto"],
        "shot_alt": "Schermata «Prossime» di Piano di Cura: le cose da fare questa settimana, gli appuntamenti entro un mese e più avanti.",
        "phone": {
            "title": "Prossime",
            "sections": [
                ("Questa settimana", [
                    ("#e84a57", "pill", "Prenota il ritiro del farmaco", "Farmaco ospedaliero", "Oggi", "late"),
                    ("#2a8cdb", "mail", "Chiedi l'impegnativa", "Esami del sangue", "Ven", "due"),
                ]),
                ("Entro un mese", [
                    ("#34a853", "steth", "Visita di controllo", "Cardiologia · 10:30", "12 dic", ""),
                    ("#2a8cdb", "drop", "Esami del sangue", "Ogni 3 mesi", "18 dic", ""),
                ]),
                ("Più avanti", [
                    ("#8e5bd9", "scan", "Risonanza annuale", "Neurologia", "14 mar", ""),
                ]),
            ],
            "tabs": ["Prossime", "Appuntamenti", "Documenti", "Impostazioni"],
            "tag_late": "Da fare", "tag_due": "Tra 3 giorni",
        },
        "ld": {
            "subcategory": "Piano di cura, appuntamenti medici e promemoria",
            "os": "iOS 17.0 o successivo",
            "desc": "App per iPhone che raccoglie il piano di cura del paziente: appuntamenti ricorrenti (visite, esami, ritiro di farmaci, terapie) con le azioni da svolgere prima, promemoria ripetuti, mail precompilate ai medici, rubrica di medico di base e specialisti, documenti sanitari. I dati restano sul dispositivo e nell'account iCloud personale dell'utente: non esistono server dello sviluppatore.",
            "features": ["Più piani di cura, uno per patologia", "Appuntamenti ricorrenti ogni N giorni, settimane, mesi o anni, con orario facoltativo",
                         "Cose da fare prima di ogni appuntamento, con anticipo", "Promemoria ripetuti finché un'azione non è fatta",
                         "8 modelli pronti per le cure più comuni", "Mail precompilate al medico con elenco degli esami e più destinatari",
                         "Medico di base e specialisti con telefono, email e orari", "Documenti PDF e foto, anche dal foglio Condividi",
                         "Widget per Home e Blocco schermo", "Aggiungi al Calendario", "Sincronizzazione con l'account iCloud personale"],
        },
    },
    "en": {
        "lang": "en", "og_locale": "en_GB", "og_alt": "it_IT", "url": BASE + "en/", "prefix": "../",
        "title": "Piano di Cura — Visits, tests and medicines on iPhone",
        "description": "iPhone app for people following a course of care: recurring visits, tests, medicine pick-ups and therapies, with the things to do beforehand (referral, booking, trip) and reminders that keep coming back until they are done. Data only on iPhone and iCloud. Coming by the end of 2026.",
        "og_description": "Visits, tests and medicines in one place, with the things to do beforehand and reminders that make sure nothing is forgotten. Coming to the App Store by the end of 2026.",
        "nav": ["Features", "Privacy", "FAQ"],
        "eyebrow": "Coming to the App Store by the end of 2026",
        "h1": 'Visits, tests and medicines,<br><span class="grad">nothing forgotten.</span>',
        "sub": "Anyone following a course of care knows it: before the visit there is a referral to ask for, a blood test to book, a medicine to pick up. <strong>Piano di Cura lines up every appointment with the things to do beforehand</strong> and reminds you of each one at the right time, until it is done.",
        "soon_small": "Coming soon on", "soon_big": "App Store",
        "out_small": "Download on the", "out_big": "App Store",
        "notify": "Tell me when it's out",
        "notify_subject": "Tell me when Piano di Cura is out",
        "note": "For iPhone, iOS 17 or later · No account · English, Italian, Spanish, German, French",
        "facts": [("8", "ready-made templates for the most common care"), ("1", "place for appointments, doctors and documents"),
                  ("5", "languages: EN, IT, ES, DE, FR"), ("0", "servers, accounts and ads")],
        "feat_h": "Your whole care plan, in order",
        "feat_p": "Made for people with recurring visits, tests and therapies who want to stop keeping it all in their head.",
        "features": [
            ("piani", "One plan for each condition", "Several care plans, each with its own appointments, specialists and documents. There is one family doctor, shared by all of them."),
            ("ripeti", "Appointments that repeat", "Visits, tests, medicine pick-ups, therapies: every so many days, weeks, months or years, with a time if needed. Mark it done and the app sets the next one."),
            ("prima", "Things to do beforehand", "For each appointment, what needs doing in advance: asking for a referral, booking, picking up, planning the trip. Each with its own lead time."),
            ("campana", "Reminders that insist", "A notification at the time you choose. If you don't mark something as done, the reminder comes back every few days until the appointment."),
            ("modelli", "Ready-made templates", "Hospital medicine, blood tests, check-up visit, yearly scan, therapy plan renewal, vaccine, exemption, periodic therapy: pick and adapt."),
            ("mail", "Emails to your doctor, already written", "The referral request with the list of tests, to one or more recipients, signed with your name. You read it over and send it from your own mailbox."),
            ("medico", "Doctors at hand", "Family doctor and specialists with phone, email and office hours. Call or write with one tap."),
            ("documenti", "Documents always with you", "Reports, prescriptions and therapy plans as PDFs or photos, also from Share in any app. Attach them to an email when needed."),
            ("widget", "Agenda, widgets and Calendar", "“Upcoming” shows what is overdue, what is on this week, within a month and later on. Widgets for the Home and Lock Screen, and Add to Calendar."),
        ],
        "priv_h": "Your health data stays yours",
        "priv_p": "Visits, tests and therapies are among the most personal information there is. That is why Piano di Cura is built this way.",
        "privacy": [
            ("scudo", "None of our servers", "Everything stays on your iPhone and, if you want, in <strong>your</strong> personal iCloud, directly between you and Apple. We see nothing."),
            ("no", "No ads, no tracking", "The app contains no ad networks and does not track you. It only collects anonymous usage statistics, never health data."),
            ("lucchetto", "No account", "No sign-up needed. Your name, if you enter it, is only used to sign emails to your doctors."),
            ("invio", "Emails are sent by you", "The app prepares the text, you read it over and send it from your own mailbox. No copy goes through us."),
        ],
        "priv_more": 'All the details are in the <a href="{p}privacy.html?lang=en">Privacy Policy</a>.',
        "faq_h": "Frequently asked questions",
        "faq": [
            ("What is Piano di Cura?", "It is an iPhone app for people following a course of care over time: check-up visits, blood tests, hospital medicine pick-ups, periodic therapies, renewals of therapy plans and exemptions. For each appointment you list the things to do beforehand, such as asking for a referral or booking, and the app reminds you of each one at the right time."),
            ("When does it come out?", "Piano di Cura is coming to the App Store by the end of 2026, for iPhone with iOS 17 or later. If you would like a heads-up on launch day, write to us at feedbacksr@icloud.com."),
            ("Can I follow more than one condition?", "Yes. You can create several care plans, for example one for each condition, each with its own appointments, specialists and documents. The “Upcoming” agenda shows them all together or one at a time."),
            ("How do reminders work?", "Each thing to do has its own lead time, for example booking a blood draw a month before the tests. You get a notification at the time you choose and, if you don't mark it as done, the reminder comes back every few days until the appointment. You can choose how often, or turn it off."),
            ("Can I write to my doctor from the app?", "Yes. The app prepares the email asking for a referral or prescription, with the list of tests and your name, to one or more recipients. The email opens in your email app: you read it over, edit it if you like and send it yourself."),
            ("Where does my data go?", "It stays in your iPhone's storage and, if you want, it is synced to your personal iCloud account, so you find it on your other devices signed in with the same Apple Account. There is no developer server and the app contains no ads. It only collects anonymous usage statistics, which never contain health data."),
            ("Does Piano di Cura replace my doctor?", "No. Piano di Cura is a personal agenda: it helps you remember appointments and things to do, but it gives no medical advice, is not a medical device and does not replace the advice of your doctor or pharmacist."),
            ("Which languages is it available in?", "The app is available in English, Italian, Spanish, German and French, and follows the language set on your iPhone. Dates and times use your country's format."),
        ],
        "closing_h": "Coming by the end of 2026",
        "closing_p": "Piano di Cura is about to arrive on the App Store. Want a heads-up on launch day, or have an idea for us? Write to us.",
        "closing_h_out": "Available on the App Store",
        "closing_p_out": "Piano di Cura is available on the App Store. For questions or to report something, write to us any time.",
        "footer": ["Privacy Policy", "Support"],
        "shot_alt": "The “Upcoming” screen of Piano di Cura: things to do this week, appointments within a month and later on.",
        "phone": {
            "title": "Upcoming",
            "sections": [
                ("This week", [
                    ("#e84a57", "pill", "Book the medicine pick-up", "Hospital medicine", "Today", "late"),
                    ("#2a8cdb", "mail", "Ask for the referral", "Blood tests", "Fri", "due"),
                ]),
                ("Within a month", [
                    ("#34a853", "steth", "Check-up visit", "Cardiology · 10:30", "Dec 12", ""),
                    ("#2a8cdb", "drop", "Blood tests", "Every 3 months", "Dec 18", ""),
                ]),
                ("Later on", [
                    ("#8e5bd9", "scan", "Yearly MRI", "Neurology", "Mar 14", ""),
                ]),
            ],
            "tabs": ["Upcoming", "Appointments", "Documents", "Settings"],
            "tag_late": "To do", "tag_due": "In 3 days",
        },
        "ld": {
            "subcategory": "Care plan, medical appointments and reminders",
            "os": "iOS 17.0 or later",
            "desc": "iPhone app that holds a patient's care plan: recurring appointments (visits, tests, medicine pick-ups, therapies) with the actions to take beforehand, repeating reminders, pre-filled emails to doctors, a directory of family doctor and specialists, and health documents. Data stays on the device and in the user's personal iCloud account: the developer runs no servers.",
            "features": ["Several care plans, one per condition", "Appointments repeating every N days, weeks, months or years, with optional time",
                         "Things to do before each appointment, with lead time", "Reminders that repeat until an action is done",
                         "8 ready-made templates for the most common care", "Pre-filled emails to the doctor with the list of tests and multiple recipients",
                         "Family doctor and specialists with phone, email and office hours", "PDF and photo documents, also from the Share sheet",
                         "Home and Lock Screen widgets", "Add to Calendar", "Sync with the personal iCloud account"],
        },
    },
}

PH_ICONE = {
    "pill": '<rect x="3" y="9" width="18" height="6" rx="3" transform="rotate(-35 12 12)"/><path d="M9.5 8.5l5 7"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "steth": '<path d="M5 4v5a5 5 0 0 0 10 0V4"/><path d="M10 14v2a4 4 0 0 0 8 0v-2"/><circle cx="18" cy="12" r="2"/>',
    "drop": '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>',
    "scan": '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3"/>',
}
TAB_ICONE = [
    '<path d="M9 6h11M9 12h11M9 18h11"/><path d="M4 6l1 1 2-2M4 12l1 1 2-2M4 18l1 1 2-2"/>',
    '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    '<path d="M8 3h8l4 4v12a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z"/><path d="M4 7v12a2 2 0 0 0 2 2"/>',
    '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.6 1.6 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.6 1.6 0 0 0-2.7 1.1V21a2 2 0 1 1-4 0v-.1a1.6 1.6 0 0 0-2.7-1.1l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1A1.6 1.6 0 0 0 3.6 15H3a2 2 0 1 1 0-4h.1a1.6 1.6 0 0 0 1.1-2.7l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1A1.6 1.6 0 0 0 9.7 4.6V4a2 2 0 1 1 4 0v.1a1.6 1.6 0 0 0 2.7 1.1l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.6 1.6 0 0 0 1.1 2.7H21a2 2 0 1 1 0 4h-.1a1.6 1.6 0 0 0-1.5 1z"/>',
]


def e(s):
    return html.escape(s, quote=True)


def telefono(t):
    p = t["phone"]
    righe = []
    for titolo, voci in p["sections"]:
        righe.append(f'<p class="ph-list-title">{e(titolo)}</p>\n          <ul class="ph-list">')
        for colore, ico, nome, sotto, quando, tag in voci:
            tag_html = ""
            if tag == "late":
                tag_html = f'<span class="ph-tag late">{e(p["tag_late"])}</span>'
            elif tag == "due":
                tag_html = f'<span class="ph-tag due">{e(p["tag_due"])}</span>'
            righe.append(
                f'''            <li class="ph-row"><span class="ph-ico" style="background:{colore}1f;color:{colore}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{PH_ICONE[ico]}</svg></span>
              <span class="ph-name"><b>{e(nome)}</b><span>{e(sotto)}</span>{tag_html}</span>
              <span class="ph-amt"><span>{e(quando)}</span></span></li>''')
        righe.append('          </ul>')
    tabs = "".join(
        f'<span class="ph-tab{" on" if i == 0 else ""}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{TAB_ICONE[i]}</svg>{e(n)}</span>'
        for i, n in enumerate(p["tabs"]))
    return f'''<div class="phone" role="img" aria-label="{e(t["shot_alt"])}">
        <div class="phone-screen" aria-hidden="true">
          <div class="ph-status"><span>9:41</span><span style="display:flex;gap:5px;align-items:center"><span class="ph-signal"><i></i><i></i><i></i></span><span class="ph-battery"></span></span></div>
          <div class="ph-greet">{e(p["title"])}</div>
          {chr(10).join(righe)}
          <div class="ph-tabs">{tabs}</div>
        </div>
      </div>'''


def card(ico, h, p):
    return f'''      <article class="feature">
        <div class="ficon"><svg viewBox="0 0 24 24" aria-hidden="true">{ICONE[ico]}</svg></div>
        <h3>{e(h)}</h3>
        <p>{p if "<strong>" in p else e(p)}</p>
      </article>'''


def badge(t):
    if APP_STORE_ID:
        link = f"https://apps.apple.com/{'it/' if t['lang'] == 'it' else ''}app/id{APP_STORE_ID}"
        return f'''<a class="store-badge" href="{link}">
          {APPLE_SVG}
          <span><span class="small">{e(t["out_small"])}</span><span class="big">{e(t["out_big"])}</span></span>
        </a>'''
    return f'''<span class="store-badge soon" aria-label="{e(t["soon_small"] + " " + t["soon_big"])}">
          {APPLE_SVG}
          <span><span class="small">{e(t["soon_small"])}</span><span class="big">{e(t["soon_big"])}</span></span>
        </span>'''


def json_ld(t):
    ld = t["ld"]
    app = {
        "@type": "MobileApplication",
        "@id": BASE + "#app",
        "name": "Piano di Cura",
        "applicationCategory": "HealthApplication",
        "applicationSubCategory": ld["subcategory"],
        "operatingSystem": ld["os"],
        "url": t["url"],
        "image": BASE + "icon-512.png",
        "screenshot": BASE + ("og-image.png" if t["lang"] == "it" else "og-image-en.png"),
        "inLanguage": ["it", "en", "es", "de", "fr"],
        "description": ld["desc"],
        "featureList": ld["features"],
        "author": {"@id": "https://dontknowif.github.io/#publisher"},
        "publisher": {"@id": "https://dontknowif.github.io/#publisher"},
        "privacyPolicy": BASE + "privacy.html",
    }
    if APP_STORE_ID:
        link = f"https://apps.apple.com/{'it/' if t['lang'] == 'it' else ''}app/id{APP_STORE_ID}"
        app.update({"downloadUrl": link, "installUrl": link, "sameAs": [link]})
    grafo = [
        app,
        {"@type": "Organization", "@id": "https://dontknowif.github.io/#publisher", "name": "dontknowif",
         "url": "https://dontknowif.github.io/", "founder": {"@type": "Person", "name": "Rocco Barletta"}},
        {"@type": "WebSite", "@id": t["url"] + "#website", "url": t["url"], "name": "Piano di Cura",
         "inLanguage": t["lang"], "publisher": {"@id": "https://dontknowif.github.io/#publisher"}},
        {"@type": "FAQPage", "@id": t["url"] + "#faq", "inLanguage": t["lang"],
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]},
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": grafo}, ensure_ascii=False, indent=2)


def pagina(t):
    pre = t["prefix"]
    og = BASE + ("og-image.png" if t["lang"] == "it" else "og-image-en.png")
    uscita = bool(APP_STORE_ID)
    eyebrow = "" if uscita else f'<p class="eyebrow">{e(t["eyebrow"])}</p>'
    notify = "" if uscita else (f'<a class="notify-link" href="mailto:feedbacksr@icloud.com?subject='
                                f'{e(t["notify_subject"]).replace(" ", "%20")}">{e(t["notify"])}</a>')
    feats = "\n".join(card(*f) for f in t["features"])
    privs = "\n".join(card(*f) for f in t["privacy"])
    facts = "\n".join(f'    <div class="fact"><b>{e(n)}</b><span>{e(s)}</span></div>' for n, s in t["facts"])
    faq = "\n\n".join(f'''      <details{" open" if i == 0 else ""}>
        <summary>{e(q)}</summary>
        <p>{e(a)}</p>
      </details>''' for i, (q, a) in enumerate(t["faq"]))
    lang_it = 'aria-current="true" ' if t["lang"] == "it" else ""
    lang_en = 'aria-current="true" ' if t["lang"] == "en" else ""
    privacy_href = f'{pre}privacy.html' + ("?lang=en" if t["lang"] == "en" else "")
    support_href = f'{pre}support.html' + ("?lang=en" if t["lang"] == "en" else "")
    closing_h = t["closing_h_out"] if uscita else t["closing_h"]
    closing_p = t["closing_p_out"] if uscita else t["closing_p"]
    closing_cta = badge(t) if uscita else (f'<a class="store-badge" href="mailto:feedbacksr@icloud.com?subject='
                                           f'{e(t["notify_subject"]).replace(" ", "%20")}"><span><span class="big">'
                                           f'{e(t["notify"])}</span></span></a>')
    return f'''<!DOCTYPE html>
<html lang="{t["lang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<!-- Pagina generata da piano-di-cura/_sorgenti/genera-landing.py: modificare lo script, non questo file. -->

<title>{e(t["title"])}</title>
<meta name="description" content="{e(t["description"])}">
<link rel="canonical" href="{t["url"]}">

<link rel="alternate" hreflang="it" href="{BASE}">
<link rel="alternate" hreflang="en" href="{BASE}en/">
<link rel="alternate" hreflang="x-default" href="{BASE}">

<meta name="theme-color" content="#1f73c4">
<meta name="author" content="Rocco Barletta">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">

<meta property="og:type" content="website">
<meta property="og:site_name" content="Piano di Cura">
<meta property="og:locale" content="{t["og_locale"]}">
<meta property="og:locale:alternate" content="{t["og_alt"]}">
<meta property="og:title" content="{e(t["title"])}">
<meta property="og:description" content="{e(t["og_description"])}">
<meta property="og:url" content="{t["url"]}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(t["title"])}">
<meta name="twitter:description" content="{e(t["og_description"])}">
<meta name="twitter:image" content="{og}">

<link rel="icon" href="{pre}favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="{pre}icon-180.png">

<link rel="stylesheet" href="{pre}style.css">
<link rel="stylesheet" href="{pre}site.css">

<script type="application/ld+json">
{json_ld(t)}
</script>
</head>

<body class="landing">

<nav class="nav">
  <div class="nav-inner">
    <a class="brand" href="./"><img class="dot" src="{pre}icon-96.png" width="28" height="28" alt=""> Piano di Cura</a>
    <div class="nav-links">
      <a href="#funzioni">{e(t["nav"][0])}</a>
      <a href="#privacy">{e(t["nav"][1])}</a>
      <a href="#faq">{e(t["nav"][2])}</a>
    </div>
    <div class="langs">
      <a href="{pre or "./"}" {lang_it}hreflang="it">IT</a>
      <a href="{"./" if t["lang"] == "en" else "en/"}" {lang_en}hreflang="en">EN</a>
    </div>
  </div>
</nav>

<main>

<!-- ===================== HERO ===================== -->
<header class="hero">
  <div class="container hero-grid">
    <div>
      {eyebrow}
      <h1>{t["h1"]}</h1>
      <p class="hero-sub">{t["sub"]}</p>
      <div class="hero-actions">
        {badge(t)}
        {notify}
      </div>
      <p class="hero-note">{e(t["note"])}</p>
    </div>

    <div class="hero-phone">
      {telefono(t)}
    </div>
  </div>
</header>

<!-- ===================== DATI CHIAVE ===================== -->
<section class="container" aria-label="{e(t["feat_h"])}">
  <div class="facts">
{facts}
  </div>
</section>

<!-- ===================== FUNZIONI ===================== -->
<section class="section" id="funzioni">
  <div class="container">
    <div class="section-head">
      <h2>{e(t["feat_h"])}</h2>
      <p>{e(t["feat_p"])}</p>
    </div>

    <div class="grid">
{feats}
    </div>
  </div>
</section>

<!-- ===================== PRIVACY ===================== -->
<section class="section section-alt" id="privacy">
  <div class="container">
    <div class="section-head">
      <h2>{e(t["priv_h"])}</h2>
      <p>{e(t["priv_p"])}</p>
    </div>

    <div class="grid">
{privs}
    </div>

    <p style="margin-top:26px">{t["priv_more"].format(p=pre)}</p>
  </div>
</section>

<!-- ===================== FAQ ===================== -->
<section class="section" id="faq">
  <div class="container">
    <div class="section-head"><h2>{e(t["faq_h"])}</h2></div>

    <div class="faq">
{faq}
    </div>
  </div>
</section>

<!-- ===================== CHIUSURA ===================== -->
<section class="container" style="padding:76px 22px">
  <div class="closing">
    <h2>{e(closing_h)}</h2>
    <p>{e(closing_p)}</p>
    {closing_cta}
  </div>
</section>

</main>

<!--
  Cloudflare Web Analytics: senza cookie, non profila i singoli visitatori e
  non richiede un banner di consenso. Stesso token del resto del dominio.
  Questo tag e la sezione «Questo sito web» della Privacy Policy vanno tenuti allineati.
-->
<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js"
        data-cf-beacon='{{"token": "c71e538f281a4296b8b84c74ad2b43ad"}}'></script>

<footer>
  <div class="container">
    <a href="{privacy_href}">{e(t["footer"][0])}</a>
    <a href="{support_href}">{e(t["footer"][1])}</a>
    <a href="mailto:feedbacksr@icloud.com">feedbacksr@icloud.com</a>
    <span class="spacer">© 2026 dontknowif</span>
  </div>
</footer>

</body>
</html>
'''


def verifica_faq(testo, t):
    """Le FAQ del JSON-LD devono comparire identiche (dopo l'escape HTML) nel testo visibile."""
    for q, a in t["faq"]:
        assert f"<summary>{e(q)}</summary>" in testo, f"domanda mancante: {q}"
        assert f"<p>{e(a)}</p>" in testo, f"risposta mancante: {q}"
    ld = json.loads(testo.split('<script type="application/ld+json">')[1].split("</script>")[0])
    faq_ld = [n for n in ld["@graph"] if n["@type"] == "FAQPage"][0]["mainEntity"]
    assert [(x["name"], x["acceptedAnswer"]["text"]) for x in faq_ld] == list(t["faq"])


for codice, t in T.items():
    out = os.path.join(CARTELLA, "index.html" if codice == "it" else "en/index.html")
    testo = pagina(t)
    verifica_faq(testo, t)
    with open(out, "w", encoding="utf-8") as f:
        f.write(testo)
    print("scritto", os.path.relpath(out, os.path.dirname(CARTELLA)))
