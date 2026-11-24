#!/usr/bin/env python3
"""Genera le landing di Piano di Cura: IT in piano-di-cura/index.html, EN/ES/DE/FR in piano-di-cura/<lingua>/index.html.

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
        "title": "App promemoria per visite, esami e farmaci | Piano di Cura",
        "og_alt_text": "Icona di Piano di Cura e la frase: visite, esami e farmaci, senza dimenticare nulla. In arrivo entro fine 2026.",
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
        "title": "Medical appointment and medication reminder app | Piano di Cura",
        "og_alt_text": "Piano di Cura icon and the line: visits, tests and medicines, nothing forgotten. Coming by the end of 2026.",
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

# ---------------------------------------------------------------------------
# Spagnolo, tedesco, francese: stessa struttura di T["en"]. Privacy e Supporto
# esistono solo in IT/EN (come per Skurda): i link puntano alla versione inglese.
# ---------------------------------------------------------------------------

def _lingua(base, **diff):
    d = dict(base)
    d.update(diff)
    return d

T["es"] = _lingua(T["en"],
    lang="es", og_locale="es_ES", url=BASE + "es/", prefix="../",
    title="App de recordatorios para citas médicas, análisis y medicamentos | Piano di Cura",
    og_alt_text="Icono de Piano di Cura y la frase: visitas, análisis y medicamentos, sin olvidar nada. Disponible antes de finales de 2026.",
    description="App para iPhone para quien sigue un tratamiento: visitas, análisis, recogida de medicamentos y terapias que se repiten, con lo que hay que hacer antes (volante, cita, viaje) y recordatorios que vuelven hasta que lo hayas hecho. Datos solo en el iPhone y en iCloud. Llega antes de finales de 2026.",
    og_description="Visitas, análisis y medicamentos en un solo lugar, con lo que hay que hacer antes y recordatorios para no olvidar nada. Llega al App Store antes de finales de 2026.",
    nav=["Funciones", "Privacidad", "Preguntas"],
    eyebrow="Llega al App Store antes de finales de 2026",
    h1='Visitas, análisis y medicamentos,<br><span class="grad">sin olvidar nada.</span>',
    sub="Quien sigue un tratamiento lo sabe: antes de la visita hay que pedir el volante, reservar la extracción, recoger el medicamento. <strong>Piano di Cura ordena cada cita con lo que hay que hacer antes</strong> y te recuerda cada cosa en el momento justo, hasta que la hayas hecho.",
    soon_small="Muy pronto en", out_small="Descárgalo en el",
    notify="Avísame cuando salga", notify_subject="Avísame cuando salga Piano di Cura",
    note="Para iPhone, iOS 17 o posterior · Sin cuenta · Español, inglés, italiano, alemán, francés",
    facts=[("8", "plantillas listas para los cuidados más comunes"), ("1", "lugar para citas, médicos y documentos"),
           ("5", "idiomas: ES, EN, IT, DE, FR"), ("0", "servidores, cuentas y anuncios")],
    feat_h="Todo tu plan de cuidados, en orden",
    feat_p="Pensada para quien tiene visitas, análisis y terapias que se repiten y quiere dejar de tenerlo todo en la cabeza.",
    features=[
        ("piani", "Un plan para cada enfermedad", "Varios planes de cuidados, cada uno con sus citas, especialistas y documentos. El médico de cabecera es uno solo y vale para todos."),
        ("ripeti", "Citas que se repiten", "Visitas, análisis, recogida de medicamentos, terapias: cada tantos días, semanas, meses o años, con hora si hace falta. La marcas como hecha y la app fija la siguiente."),
        ("prima", "Lo que hay que hacer antes", "Para cada cita, lo que hay que hacer con antelación: pedir el volante, reservar, recoger, organizar el viaje. Cada cosa con su antelación."),
        ("campana", "Recordatorios que insisten", "Una notificación a la hora que elijas. Si no marcas algo como hecho, el recordatorio vuelve cada pocos días hasta la cita."),
        ("modelli", "Plantillas listas", "Medicamento hospitalario, análisis de sangre, revisión, prueba anual, renovación del plan terapéutico, vacuna, exención, terapia periódica: eliges y adaptas."),
        ("mail", "Correos al médico ya escritos", "La petición del volante con la lista de análisis, a uno o varios destinatarios, firmada con tu nombre. La revisas y la envías desde tu correo."),
        ("medico", "Médicos a mano", "Médico de cabecera y especialistas con teléfono, correo y horario de consulta. Los llamas o les escribes con un toque."),
        ("documenti", "Documentos siempre contigo", "Informes, recetas y planes terapéuticos en PDF o foto, también desde Compartir en cualquier app. Los adjuntas al correo cuando hace falta."),
        ("widget", "Agenda, widgets y Calendario", "«Próximas» muestra lo que va con retraso, lo de esta semana, lo de este mes y lo de más adelante. Widgets para la pantalla de inicio y de bloqueo, y Añadir al Calendario."),
    ],
    priv_h="Tus datos de salud son tuyos",
    priv_p="Visitas, análisis y terapias son de la información más personal que existe. Por eso Piano di Cura está hecha así.",
    privacy=[
        ("scudo", "Ningún servidor nuestro", "Todo está en tu iPhone y, si quieres, en <strong>tu</strong> iCloud personal, directamente entre tú y Apple. Nosotros no vemos nada."),
        ("no", "Sin anuncios ni rastreo", "La app no contiene redes publicitarias y no te rastrea. Solo recoge estadísticas de uso anónimas, nunca datos de salud."),
        ("lucchetto", "Sin cuenta", "No hace falta registrarse. Tu nombre, si lo escribes, solo sirve para firmar los correos a los médicos."),
        ("invio", "Los correos los envías tú", "La app prepara el texto, tú lo revisas y lo envías desde tu buzón. Ninguna copia pasa por nosotros."),
    ],
    priv_more='Todos los detalles están en la <a href="{p}privacy.html?lang=en">Privacy Policy</a> (en inglés e italiano).',
    faq_h="Preguntas frecuentes",
    faq=[
        ("¿Qué es Piano di Cura?", "Es una app para iPhone para quien sigue un tratamiento en el tiempo: revisiones, análisis de sangre, recogida de medicamentos hospitalarios, terapias periódicas, renovaciones de planes terapéuticos y exenciones. Para cada cita apuntas lo que hay que hacer antes, como pedir el volante o reservar, y la app te recuerda cada cosa en el momento justo."),
        ("¿Cuándo sale?", "Piano di Cura llega al App Store antes de finales de 2026, para iPhone con iOS 17 o posterior. Si quieres un aviso el día del lanzamiento, escríbenos a feedbacksr@icloud.com."),
        ("¿Puedo seguir varias enfermedades?", "Sí. Puedes crear varios planes de cuidados, por ejemplo uno para cada enfermedad, cada uno con sus citas, especialistas y documentos. La agenda «Próximas» los muestra todos juntos o de uno en uno."),
        ("¿Cómo funcionan los recordatorios?", "Cada cosa por hacer tiene su antelación, por ejemplo reservar la extracción un mes antes de los análisis. Recibes una notificación a la hora que elijas y, si no la marcas como hecha, el recordatorio vuelve cada pocos días hasta la cita. Puedes elegir cada cuánto, o desactivarlo."),
        ("¿Puedo escribir al médico desde la app?", "Sí. La app prepara el correo para pedir el volante o la receta, con la lista de análisis y tu nombre, a uno o varios destinatarios. El correo se abre en tu app de correo: lo revisas, lo cambias si quieres y lo envías tú."),
        ("¿Dónde acaban mis datos?", "Se quedan en la memoria de tu iPhone y, si quieres, se sincronizan con tu cuenta personal de iCloud, para encontrarlos en tus otros dispositivos con el mismo Apple Account. No existe ningún servidor del desarrollador y la app no contiene anuncios. Solo recoge estadísticas de uso anónimas, que nunca contienen datos de salud."),
        ("¿Piano di Cura sustituye al médico?", "No. Piano di Cura es una agenda personal: te ayuda a recordar citas y cosas por hacer, pero no da indicaciones médicas, no es un producto sanitario y no sustituye la opinión del médico o del farmacéutico."),
        ("¿En qué idiomas está disponible?", "La app está disponible en español, inglés, italiano, alemán y francés, y sigue el idioma configurado en el iPhone. Las fechas y horas usan el formato de tu país."),
    ],
    closing_h="Llega antes de finales de 2026",
    closing_p="Piano di Cura está a punto de llegar al App Store. ¿Quieres un aviso el día del lanzamiento o tienes una idea para nosotros? Escríbenos.",
    closing_h_out="Disponible en el App Store",
    closing_p_out="Piano di Cura está disponible en el App Store. Para preguntas o para avisarnos de algo, escríbenos cuando quieras.",
    footer=["Privacy Policy", "Soporte"],
    shot_alt="La pantalla «Próximas» de Piano di Cura: lo que hay que hacer esta semana, las citas de este mes y las de más adelante.",
    phone={
        "title": "Próximas",
        "sections": [
            ("Esta semana", [
                ("#e84a57", "pill", "Reserva la recogida del medicamento", "Medicamento hospitalario", "Hoy", "late"),
                ("#2a8cdb", "mail", "Pide el volante", "Análisis de sangre", "Vie", "due"),
            ]),
            ("En un mes", [
                ("#34a853", "steth", "Revisión", "Cardiología · 10:30", "12 dic", ""),
                ("#2a8cdb", "drop", "Análisis de sangre", "Cada 3 meses", "18 dic", ""),
            ]),
            ("Más adelante", [
                ("#8e5bd9", "scan", "Resonancia anual", "Neurología", "14 mar", ""),
            ]),
        ],
        "tabs": ["Próximas", "Citas", "Documentos", "Ajustes"],
        "tag_late": "Por hacer", "tag_due": "En 3 días",
    },
    ld={
        "subcategory": "Plan de cuidados, citas médicas y recordatorios",
        "os": "iOS 17.0 o posterior",
        "desc": "App para iPhone que reúne el plan de cuidados del paciente: citas que se repiten (visitas, análisis, recogida de medicamentos, terapias) con las tareas previas, recordatorios repetidos, correos a los médicos ya redactados, médico de cabecera y especialistas, y documentos sanitarios. Los datos se quedan en el dispositivo y en la cuenta personal de iCloud del usuario: el desarrollador no tiene servidores.",
        "features": T["en"]["ld"]["features"],
    },
)

T["de"] = _lingua(T["en"],
    lang="de", og_locale="de_DE", url=BASE + "de/", prefix="../",
    title="Erinnerungs-App für Arzttermine, Untersuchungen und Medikamente | Piano di Cura",
    og_alt_text="Icon von Piano di Cura und der Satz: Arzttermine, Untersuchungen und Medikamente, nichts vergessen. Erscheint bis Ende 2026.",
    description="iPhone-App für alle, die eine Behandlung begleiten: wiederkehrende Arzttermine, Laboruntersuchungen, Medikamentenabholung und Therapien, mit allem, was vorher zu erledigen ist (Überweisung, Termin, Anreise), und Erinnerungen, die wiederkommen, bis es erledigt ist. Daten nur auf dem iPhone und in iCloud. Erscheint bis Ende 2026.",
    og_description="Arzttermine, Untersuchungen und Medikamente an einem Ort, mit allem, was vorher zu tun ist, und Erinnerungen, damit nichts vergessen wird. Bis Ende 2026 im App Store.",
    nav=["Funktionen", "Datenschutz", "FAQ"],
    eyebrow="Bis Ende 2026 im App Store",
    h1='Arzttermine, Untersuchungen, Medikamente –<br><span class="grad">nichts mehr vergessen.</span>',
    sub="Wer eine Behandlung begleitet, kennt das: Vor dem Termin braucht es eine Überweisung, die Blutabnahme muss gebucht, das Medikament abgeholt werden. <strong>Piano di Cura ordnet jeden Termin mit allem, was vorher zu tun ist,</strong> und erinnert dich rechtzeitig an jeden Schritt, bis er erledigt ist.",
    soon_small="Demnächst im", out_small="Laden im",
    notify="Benachrichtige mich zum Start", notify_subject="Benachrichtige mich zum Start von Piano di Cura",
    note="Für iPhone, iOS 17 oder neuer · Kein Konto · Deutsch, Englisch, Italienisch, Spanisch, Französisch",
    facts=[("8", "fertige Vorlagen für die häufigsten Behandlungen"), ("1", "Ort für Termine, Ärzte und Dokumente"),
           ("5", "Sprachen: DE, EN, IT, ES, FR"), ("0", "Server, Konten und Werbung")],
    feat_h="Dein ganzer Behandlungsplan, geordnet",
    feat_p="Für alle mit wiederkehrenden Terminen, Untersuchungen und Therapien, die nicht mehr alles im Kopf behalten wollen.",
    features=[
        ("piani", "Ein Plan pro Erkrankung", "Mehrere Behandlungspläne, jeder mit eigenen Terminen, Fachärzten und Dokumenten. Der Hausarzt gilt für alle."),
        ("ripeti", "Wiederkehrende Termine", "Arzttermine, Laboruntersuchungen, Medikamentenabholung, Therapien: alle so viele Tage, Wochen, Monate oder Jahre, mit Uhrzeit, wenn nötig. Als erledigt markieren, und die App plant den nächsten."),
        ("prima", "Was vorher zu tun ist", "Für jeden Termin, was vorab erledigt werden muss: Überweisung holen, buchen, abholen, Anreise planen. Jeweils mit eigenem Vorlauf."),
        ("campana", "Erinnerungen, die dranbleiben", "Eine Mitteilung zur gewünschten Uhrzeit. Ist etwas nicht erledigt, kommt die Erinnerung alle paar Tage wieder, bis zum Termin."),
        ("modelli", "Fertige Vorlagen", "Krankenhausmedikament, Blutuntersuchung, Kontrolltermin, jährliche Untersuchung, Verlängerung des Therapieplans, Impfung, Befreiung, regelmäßige Therapie: auswählen und anpassen."),
        ("mail", "Fertige E-Mails an den Arzt", "Die Bitte um Überweisung mit der Liste der Untersuchungen, an einen oder mehrere Empfänger, mit deinem Namen. Du liest sie durch und sendest sie aus deinem Postfach."),
        ("medico", "Ärzte griffbereit", "Hausarzt und Fachärzte mit Telefon, E-Mail und Sprechzeiten. Anrufen oder schreiben mit einem Tippen."),
        ("documenti", "Dokumente immer dabei", "Befunde, Rezepte und Therapiepläne als PDF oder Foto, auch über Teilen aus jeder App. Bei Bedarf an die E-Mail anhängen."),
        ("widget", "Agenda, Widgets und Kalender", "„Anstehend“ zeigt, was überfällig ist, was diese Woche, in einem Monat und später ansteht. Widgets für Home- und Sperrbildschirm und Zum Kalender hinzufügen."),
    ],
    priv_h="Deine Gesundheitsdaten bleiben deine",
    priv_p="Termine, Untersuchungen und Therapien gehören zu den persönlichsten Informationen überhaupt. Deshalb ist Piano di Cura so gebaut.",
    privacy=[
        ("scudo", "Keine eigenen Server", "Alles bleibt auf deinem iPhone und, wenn du willst, in <strong>deiner</strong> persönlichen iCloud, direkt zwischen dir und Apple. Wir sehen nichts."),
        ("no", "Keine Werbung, kein Tracking", "Die App enthält keine Werbenetzwerke und verfolgt dich nicht. Sie sammelt nur anonyme Nutzungsstatistiken, nie Gesundheitsdaten."),
        ("lucchetto", "Kein Konto", "Keine Registrierung nötig. Dein Name, falls du ihn einträgst, dient nur zum Unterschreiben der E-Mails an deine Ärzte."),
        ("invio", "E-Mails sendest du", "Die App bereitet den Text vor, du liest ihn durch und sendest ihn aus deinem Postfach. Keine Kopie geht über uns."),
    ],
    priv_more='Alle Details stehen in der <a href="{p}privacy.html?lang=en">Privacy Policy</a> (auf Englisch und Italienisch).',
    faq_h="Häufige Fragen",
    faq=[
        ("Was ist Piano di Cura?", "Eine iPhone-App für alle, die eine Behandlung über längere Zeit begleiten: Kontrolltermine, Blutuntersuchungen, Abholung von Krankenhausmedikamenten, regelmäßige Therapien, Verlängerungen von Therapieplänen und Befreiungen. Zu jedem Termin notierst du, was vorher zu tun ist, etwa eine Überweisung holen oder buchen, und die App erinnert dich rechtzeitig daran."),
        ("Wann erscheint die App?", "Piano di Cura erscheint bis Ende 2026 im App Store, für iPhone mit iOS 17 oder neuer. Wenn du am Starttag benachrichtigt werden möchtest, schreib uns an feedbacksr@icloud.com."),
        ("Kann ich mehrere Erkrankungen verwalten?", "Ja. Du kannst mehrere Behandlungspläne anlegen, zum Beispiel einen pro Erkrankung, jeder mit eigenen Terminen, Fachärzten und Dokumenten. Die Agenda „Anstehend“ zeigt alle zusammen oder einzeln."),
        ("Wie funktionieren die Erinnerungen?", "Jede Aufgabe hat ihren eigenen Vorlauf, zum Beispiel die Blutabnahme einen Monat vor der Untersuchung buchen. Du bekommst eine Mitteilung zur gewünschten Uhrzeit, und wenn du sie nicht als erledigt markierst, kommt die Erinnerung alle paar Tage wieder, bis zum Termin. Du kannst wählen, wie oft, oder sie ausschalten."),
        ("Kann ich dem Arzt aus der App schreiben?", "Ja. Die App bereitet die E-Mail für die Überweisung oder das Rezept vor, mit der Liste der Untersuchungen und deinem Namen, an einen oder mehrere Empfänger. Die E-Mail öffnet sich in deiner Mail-App: Du liest sie durch, änderst sie bei Bedarf und sendest sie selbst."),
        ("Wo landen meine Daten?", "Sie bleiben im Speicher deines iPhone und werden, wenn du willst, mit deinem persönlichen iCloud-Konto synchronisiert, damit du sie auf deinen anderen Geräten mit demselben Apple Account findest. Es gibt keinen Server des Entwicklers und keine Werbung. Die App sammelt nur anonyme Nutzungsstatistiken, die nie Gesundheitsdaten enthalten."),
        ("Ersetzt Piano di Cura den Arzt?", "Nein. Piano di Cura ist ein persönlicher Terminplaner: Er hilft dir, Termine und Aufgaben nicht zu vergessen, gibt aber keine medizinischen Ratschläge, ist kein Medizinprodukt und ersetzt nicht den Rat von Arzt oder Apotheker."),
        ("In welchen Sprachen gibt es die App?", "Die App gibt es auf Deutsch, Englisch, Italienisch, Spanisch und Französisch; sie folgt der Sprache deines iPhone. Datum und Uhrzeit erscheinen im Format deines Landes."),
    ],
    closing_h="Erscheint bis Ende 2026",
    closing_p="Piano di Cura kommt bald in den App Store. Möchtest du am Starttag benachrichtigt werden oder hast du eine Idee für uns? Schreib uns.",
    closing_h_out="Jetzt im App Store",
    closing_p_out="Piano di Cura ist im App Store erhältlich. Für Fragen oder Hinweise kannst du uns jederzeit schreiben.",
    footer=["Privacy Policy", "Support"],
    shot_alt="Der Bildschirm „Anstehend“ von Piano di Cura: Aufgaben dieser Woche, Termine im nächsten Monat und später.",
    phone={
        "title": "Anstehend",
        "sections": [
            ("Diese Woche", [
                ("#e84a57", "pill", "Medikamentenabholung buchen", "Krankenhausmedikament", "Heute", "late"),
                ("#2a8cdb", "mail", "Überweisung anfragen", "Blutuntersuchung", "Fr", "due"),
            ]),
            ("Innerhalb eines Monats", [
                ("#34a853", "steth", "Kontrolltermin", "Kardiologie · 10:30", "12. Dez", ""),
                ("#2a8cdb", "drop", "Blutuntersuchung", "Alle 3 Monate", "18. Dez", ""),
            ]),
            ("Später", [
                ("#8e5bd9", "scan", "Jährliches MRT", "Neurologie", "14. März", ""),
            ]),
        ],
        "tabs": ["Anstehend", "Termine", "Dokumente", "Einstellungen"],
        "tag_late": "Zu erledigen", "tag_due": "In 3 Tagen",
    },
    ld={
        "subcategory": "Behandlungsplan, Arzttermine und Erinnerungen",
        "os": "iOS 17.0 oder neuer",
        "desc": "iPhone-App, die den Behandlungsplan eines Patienten bündelt: wiederkehrende Termine (Arztbesuche, Untersuchungen, Medikamentenabholung, Therapien) mit den vorher zu erledigenden Aufgaben, wiederholte Erinnerungen, vorbereitete E-Mails an Ärzte, Hausarzt und Fachärzte sowie Gesundheitsdokumente. Die Daten bleiben auf dem Gerät und im persönlichen iCloud-Konto: Der Entwickler betreibt keine Server.",
        "features": T["en"]["ld"]["features"],
    },
)

T["fr"] = _lingua(T["en"],
    lang="fr", og_locale="fr_FR", url=BASE + "fr/", prefix="../",
    title="App de rappels pour rendez-vous médicaux, examens et médicaments | Piano di Cura",
    og_alt_text="Icône de Piano di Cura et la phrase : rendez-vous, examens et médicaments, sans rien oublier. Disponible d'ici fin 2026.",
    description="App iPhone pour celles et ceux qui suivent un traitement : rendez-vous, examens, retrait de médicaments et thérapies qui se répètent, avec ce qu'il faut faire avant (ordonnance, réservation, trajet) et des rappels qui reviennent tant que ce n'est pas fait. Données uniquement sur l'iPhone et dans iCloud. Disponible d'ici fin 2026.",
    og_description="Rendez-vous, examens et médicaments au même endroit, avec ce qu'il faut faire avant et des rappels pour ne rien oublier. Sur l'App Store d'ici fin 2026.",
    nav=["Fonctions", "Confidentialité", "FAQ"],
    eyebrow="Sur l'App Store d'ici fin 2026",
    h1='Rendez-vous, examens et médicaments,<br><span class="grad">sans rien oublier.</span>',
    sub="Quand on suit un traitement, on le sait : avant la consultation, il faut demander l'ordonnance, réserver la prise de sang, retirer le médicament. <strong>Piano di Cura organise chaque rendez-vous avec ce qu'il faut faire avant</strong> et vous rappelle chaque étape au bon moment, jusqu'à ce qu'elle soit faite.",
    soon_small="Bientôt sur", out_small="Télécharger dans",
    notify="Prévenez-moi à la sortie", notify_subject="Prévenez-moi à la sortie de Piano di Cura",
    note="Pour iPhone, iOS 17 ou ultérieur · Sans compte · Français, anglais, italien, espagnol, allemand",
    facts=[("8", "modèles prêts pour les soins les plus courants"), ("1", "endroit pour rendez-vous, médecins et documents"),
           ("5", "langues : FR, EN, IT, ES, DE"), ("0", "serveur, compte et publicité")],
    feat_h="Tout votre plan de soins, en ordre",
    feat_p="Conçue pour celles et ceux qui ont des rendez-vous, des examens et des thérapies récurrents et ne veulent plus tout garder en tête.",
    features=[
        ("piani", "Un plan par pathologie", "Plusieurs plans de soins, chacun avec ses rendez-vous, ses spécialistes et ses documents. Le médecin traitant est unique et vaut pour tous."),
        ("ripeti", "Des rendez-vous qui se répètent", "Consultations, examens, retrait de médicaments, thérapies : tous les combien de jours, semaines, mois ou années, avec l'heure si besoin. Marquez-le comme fait et l'app fixe le suivant."),
        ("prima", "Ce qu'il faut faire avant", "Pour chaque rendez-vous, ce qui doit être fait à l'avance : demander l'ordonnance, réserver, retirer, organiser le trajet. Chaque étape avec son délai."),
        ("campana", "Des rappels qui insistent", "Une notification à l'heure choisie. Si une étape n'est pas marquée comme faite, le rappel revient tous les quelques jours jusqu'au rendez-vous."),
        ("modelli", "Modèles prêts", "Médicament hospitalier, prise de sang, consultation de contrôle, examen annuel, renouvellement du plan thérapeutique, vaccin, exonération, thérapie périodique : choisissez et adaptez."),
        ("mail", "E-mails au médecin déjà rédigés", "La demande d'ordonnance avec la liste des examens, à un ou plusieurs destinataires, signée de votre nom. Vous la relisez et l'envoyez depuis votre messagerie."),
        ("medico", "Vos médecins à portée de main", "Médecin traitant et spécialistes avec téléphone, e-mail et horaires du cabinet. Appelez ou écrivez d'un geste."),
        ("documenti", "Vos documents toujours avec vous", "Comptes rendus, ordonnances et plans thérapeutiques en PDF ou en photo, aussi depuis Partager dans n'importe quelle app. Joignez-les à l'e-mail quand il faut."),
        ("widget", "Agenda, widgets et Calendrier", "« À venir » montre ce qui est en retard, ce qui arrive cette semaine, dans le mois et plus tard. Widgets pour l'écran d'accueil et l'écran verrouillé, et Ajouter au Calendrier."),
    ],
    priv_h="Vos données de santé restent les vôtres",
    priv_p="Rendez-vous, examens et thérapies font partie des informations les plus personnelles qui soient. C'est pourquoi Piano di Cura est conçue ainsi.",
    privacy=[
        ("scudo", "Aucun serveur à nous", "Tout reste sur votre iPhone et, si vous le souhaitez, dans <strong>votre</strong> iCloud personnel, directement entre vous et Apple. Nous ne voyons rien."),
        ("no", "Ni publicité ni pistage", "L'app ne contient aucune régie publicitaire et ne vous piste pas. Elle ne collecte que des statistiques d'usage anonymes, jamais de données de santé."),
        ("lucchetto", "Sans compte", "Aucune inscription. Votre nom, si vous le saisissez, sert uniquement à signer les e-mails à vos médecins."),
        ("invio", "C'est vous qui envoyez", "L'app prépare le texte, vous le relisez et l'envoyez depuis votre boîte. Aucune copie ne passe par nous."),
    ],
    priv_more='Tous les détails sont dans la <a href="{p}privacy.html?lang=en">Privacy Policy</a> (en anglais et en italien).',
    faq_h="Questions fréquentes",
    faq=[
        ("Qu'est-ce que Piano di Cura ?", "C'est une app iPhone pour celles et ceux qui suivent un traitement dans la durée : consultations de contrôle, prises de sang, retrait de médicaments hospitaliers, thérapies périodiques, renouvellements de plans thérapeutiques et d'exonérations. Pour chaque rendez-vous, vous notez ce qu'il faut faire avant, comme demander l'ordonnance ou réserver, et l'app vous rappelle chaque étape au bon moment."),
        ("Quand sort-elle ?", "Piano di Cura arrive sur l'App Store d'ici fin 2026, pour iPhone sous iOS 17 ou ultérieur. Pour être prévenu le jour de la sortie, écrivez-nous à feedbacksr@icloud.com."),
        ("Puis-je suivre plusieurs pathologies ?", "Oui. Vous pouvez créer plusieurs plans de soins, par exemple un par pathologie, chacun avec ses rendez-vous, ses spécialistes et ses documents. L'agenda « À venir » les montre tous ensemble ou un par un."),
        ("Comment fonctionnent les rappels ?", "Chaque étape a son propre délai, par exemple réserver la prise de sang un mois avant les examens. Vous recevez une notification à l'heure choisie et, si vous ne la marquez pas comme faite, le rappel revient tous les quelques jours jusqu'au rendez-vous. Vous pouvez choisir la fréquence, ou le désactiver."),
        ("Puis-je écrire à mon médecin depuis l'app ?", "Oui. L'app prépare l'e-mail pour demander l'ordonnance ou la prescription, avec la liste des examens et votre nom, à un ou plusieurs destinataires. L'e-mail s'ouvre dans votre app de messagerie : vous le relisez, le modifiez si besoin et l'envoyez vous-même."),
        ("Où vont mes données ?", "Elles restent dans la mémoire de votre iPhone et, si vous le souhaitez, sont synchronisées avec votre compte iCloud personnel, pour les retrouver sur vos autres appareils avec le même Apple Account. Il n'existe aucun serveur du développeur et l'app ne contient pas de publicité. Elle ne collecte que des statistiques d'usage anonymes, qui ne contiennent jamais de données de santé."),
        ("Piano di Cura remplace-t-elle le médecin ?", "Non. Piano di Cura est un agenda personnel : elle vous aide à ne pas oublier rendez-vous et démarches, mais elle ne donne aucun avis médical, n'est pas un dispositif médical et ne remplace pas l'avis du médecin ou du pharmacien."),
        ("Dans quelles langues est-elle disponible ?", "L'app est disponible en français, anglais, italien, espagnol et allemand, et suit la langue réglée sur l'iPhone. Les dates et les heures suivent le format de votre pays."),
    ],
    closing_h="Disponible d'ici fin 2026",
    closing_p="Piano di Cura arrive bientôt sur l'App Store. Envie d'être prévenu le jour de la sortie, ou une idée à nous suggérer ? Écrivez-nous.",
    closing_h_out="Disponible sur l'App Store",
    closing_p_out="Piano di Cura est disponible sur l'App Store. Pour toute question ou remarque, écrivez-nous quand vous voulez.",
    footer=["Privacy Policy", "Assistance"],
    shot_alt="L'écran « À venir » de Piano di Cura : les étapes de la semaine, les rendez-vous du mois et ceux plus tard.",
    phone={
        "title": "À venir",
        "sections": [
            ("Cette semaine", [
                ("#e84a57", "pill", "Réserver le retrait du médicament", "Médicament hospitalier", "Auj.", "late"),
                ("#2a8cdb", "mail", "Demander l'ordonnance", "Prise de sang", "Ven", "due"),
            ]),
            ("Dans le mois", [
                ("#34a853", "steth", "Consultation de contrôle", "Cardiologie · 10:30", "12 déc", ""),
                ("#2a8cdb", "drop", "Prise de sang", "Tous les 3 mois", "18 déc", ""),
            ]),
            ("Plus tard", [
                ("#8e5bd9", "scan", "IRM annuelle", "Neurologie", "14 mars", ""),
            ]),
        ],
        "tabs": ["À venir", "Rendez-vous", "Documents", "Réglages"],
        "tag_late": "À faire", "tag_due": "Dans 3 jours",
    },
    ld={
        "subcategory": "Plan de soins, rendez-vous médicaux et rappels",
        "os": "iOS 17.0 ou ultérieur",
        "desc": "App iPhone qui réunit le plan de soins du patient : rendez-vous récurrents (consultations, examens, retrait de médicaments, thérapies) avec les démarches à faire avant, rappels répétés, e-mails pré-remplis aux médecins, médecin traitant et spécialistes, documents de santé. Les données restent sur l'appareil et dans le compte iCloud personnel de l'utilisateur : le développeur n'exploite aucun serveur.",
        "features": T["en"]["ld"]["features"],
    },
)

LINGUE = ["it", "en", "es", "de", "fr"]


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
        "inLanguage": LINGUE,
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
         "url": "https://dontknowif.github.io/", "email": "feedbacksr@icloud.com", "founder": {"@type": "Person", "name": "Rocco Barletta"}},
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
    q_legal = "" if t["lang"] == "it" else "?lang=en"  # privacy e supporto esistono solo in IT/EN
    privacy_href = f'{pre}privacy.html{q_legal}'
    support_href = f'{pre}support.html{q_legal}'
    def url_lingua(c):
        return BASE if c == "it" else f"{BASE}{c}/"
    def href_lingua(c):
        if c == t["lang"]:
            return "./"
        return (pre or "./") if c == "it" else f"{pre}{c}/"
    hreflang = "\n".join(f'<link rel="alternate" hreflang="{c}" href="{url_lingua(c)}">' for c in LINGUE)
    og_alt = "\n".join(f'<meta property="og:locale:alternate" content="{T[c]["og_locale"]}">' for c in LINGUE if c != t["lang"])
    nav_lingue = "\n      ".join(
        f'<a href="{href_lingua(c)}" {"aria-current=" + chr(34) + "true" + chr(34) + " " if c == t["lang"] else ""}hreflang="{c}">{c.upper()}</a>'
        for c in LINGUE)
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

{hreflang}
<link rel="alternate" hreflang="x-default" href="{BASE}">

<meta name="theme-color" content="#1f73c4">
<meta name="author" content="Rocco Barletta">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">

<meta property="og:type" content="website">
<meta property="og:site_name" content="Piano di Cura">
<meta property="og:locale" content="{t["og_locale"]}">
{og_alt}
<meta property="og:title" content="{e(t["title"])}">
<meta property="og:description" content="{e(t["og_description"])}">
<meta property="og:url" content="{t["url"]}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(t["og_alt_text"])}">

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
      {nav_lingue}
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
    out = os.path.join(CARTELLA, "index.html" if codice == "it" else f"{codice}/index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    testo = pagina(t)
    verifica_faq(testo, t)
    with open(out, "w", encoding="utf-8") as f:
        f.write(testo)
    print("scritto", os.path.relpath(out, os.path.dirname(CARTELLA)))
