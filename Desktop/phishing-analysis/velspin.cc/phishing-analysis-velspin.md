# 🔍 Analisi Phishing — velspin.cc

| Campo | Dettaglio |
|-------|-----------|
| **Data** | 01 Maggio 2026 |
| **Analista** | 0xCosmix |
| **Target** | velspin.cc |
| **Metodo** | Network Forensics · Behavioral Analysis · OSINT |
| **Verdetto** | 🔴 TRUFFA PHISHING AGGRESSIVA |

---

## 📋 Executive Summary

L'analisi del sito `velspin.cc` rivela uno schema di truffa volto alla sottrazione di dati personali e finanziari. Il sito utilizza tecniche di **Social Engineering** per indurre l'utente a inserire informazioni sensibili sotto la falsa promessa di prelievi di denaro, proteggendo l'infrastruttura con Cloudflare per evitare il tracciamento.

L'interazione segue un pattern classico di phishing:
1. **Esca finanziaria** — simulazione di prelievi di denaro
2. **Raccolta dati personali** — richiesta di informazioni identificative complete
3. **Login forzato** — inserimento credenziali email/password per completare il furto

> ⚠️ *Il sito è progettato per creare un senso di urgenza nel prelievo, riducendo la soglia di attenzione dell'utente e aumentando l'efficacia dell'attacco.*

---

## 🎯 Indicatori di Compromissione (IOC)

| Tipo | Valore |
|------|--------|
| **Dominio** | velspin.cc |
| **IP** | 104.21.1.240 |
| **Provider** | Cloudflare Inc. |
| **ASN** | AS13335 |
| **Paese server** | USA (Cloudflare edge) |
| **Protocollo** | HTTPS / TLS |

---

## 🌐 Analisi WHOIS & Infrastruttura

| Campo | Valore |
|-------|--------|
| **Registrar** | *da compilare* |
| **Data registrazione** | *da compilare* |
| **Data scadenza** | *da compilare* |
| **Name Servers** | *da compilare* |
| **Paese registrante** | *da compilare* |

> 💡 Il dominio `.cc` (Isole Cocos) è frequentemente abusato da attori malevoli per la scarsa regolamentazione e l'anonimato offerto dai registrar.

---

## 🔬 Analisi Tecnica

### Network Forensics (Wireshark)

Le evidenze tecniche raccolte mostrano:

| Evidenza | Dettaglio |
|----------|-----------|
| **Offuscamento infrastruttura** | IP 104.21.1.240 dietro Cloudflare WAF |
| **Anomalie TLS** | Handshake Failure — pacchetti 1478/1497 |
| **WAF attivo** | HTTP 403 Forbidden — pacchetto 1516 |
| **Persistenza TCP** | Keep-Alive attivo anche in presenza di errori |

#### Pacchetti significativi

```
Pacchetto 1478 — TLS Handshake Failure
Pacchetto 1497 — TLS Alert (fatal)
Pacchetto 1516 — HTTP/1.1 403 Forbidden
```

### Behavioral Analysis

Il sito segue questo flow di attacco:

```
Utente arriva sul sito
        ↓
Simulazione saldo/prelievo disponibile
        ↓
Richiesta dati personali (nome, cognome, telefono)
        ↓
Richiesta email + password
        ↓
Dati esfiltrati verso server C2
        ↓
Utente reindirizzato o pagina di errore
```

### Tecnologie rilevate

| Tecnologia | Scopo |
|------------|-------|
| Cloudflare | Protezione IP reale del server |
| WAF | Blocco scanner automatici |
| HTTPS/TLS | Apparenza di legittimità |

---

## 🛠️ Tool Utilizzati

| Tool | Utilizzo |
|------|----------|
| **Wireshark** | Cattura e analisi pacchetti |
| **Burp Suite** | Analisi richieste HTTP |
| **0xRecon** | OSINT dominio e IP |
| **VirusTotal** | Reputazione dominio |

---

## 📊 Threat Assessment

| Parametro | Livello |
|-----------|---------|
| **Pericolosità** | 🔴 Alta |
| **Sofisticazione** | 🟡 Media |
| **Target** | Utenti generici italiani |
| **Obiettivo** | Furto credenziali e dati finanziari |
| **Campagna attiva** | ✅ Sì (al momento dell'analisi) |

---

## 🚨 Segnalazioni Effettuate

- [ ] CERT-AgID — cert-agid.gov.it
- [ ] Cloudflare Abuse — abuse.cloudflare.com

---

## 💡 Raccomandazioni

**Per gli utenti:**
- Non inserire mai dati personali su siti sconosciuti
- Verificare sempre il dominio prima di inserire credenziali
- Siti legittimi non promettono prelievi di denaro facile

**Per i difensori:**
- Bloccare IP `104.21.1.240` sui firewall aziendali
- Aggiungere `velspin.cc` alle blacklist DNS
- Sensibilizzare utenti su questo pattern di attacco

---

## 📝 Note dell'Analista

> L'infrastruttura Cloudflare rende difficile risalire al server reale dell'attaccante. Le anomalie TLS osservate (Handshake Failure sui pacchetti 1478/1497) suggeriscono che il WAF blocca attivamente le connessioni provenienti da tool di analisi automatici, indicando un livello di consapevolezza tecnica medio-alta da parte degli operatori della truffa.
> 
> Il pattern comportamentale osservato è coerente con campagne di phishing strutturate e professionali, probabilmente parte di una campagna più ampia.

---

*Report redatto da [0xCosmix](https://github.com/0xCosmix) — Tutti i dati sono stati raccolti con metodi passivi e legali a scopo di ricerca e protezione degli utenti.*
