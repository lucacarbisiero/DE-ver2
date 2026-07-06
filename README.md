# Diagnosi Energetica — fbc group

Applicazione web per la **raccolta dati di rilievo in campo** durante una diagnosi/sopralluogo energetico
(11 sezioni tecniche, gestione record, export Excel/JSON). Ottimizzata per **smartphone**.
Documento tecnico per il reparto IT (deploy, dipendenze, manutenzione).

> Progetto **indipendente** dall'app "Audit Energetico" (cartella `AUDIT-main`): non condividono codice, file o dati.

---

## 1. Tipo di applicazione
- **PWA statica**: solo `HTML + CSS + JavaScript`. **Nessun backend, nessun database server.**
- Tutto in un unico file `index.html`. I dati restano **sul dispositivo** (`localStorage`).
- Ottimizzata per uso **mobile** (testata su Samsung A56), con tema chiaro/scuro.

## 2. Come si esegue / Deploy
- **Uso locale**: aprire `index.html` con un browser.
- **Deploy**: copiare la cartella su un qualsiasi **hosting statico** (IIS, Apache/Nginx, GitHub Pages, ecc.). Nessun runtime server-side.
- Per **installazione PWA + offline** dev'essere servita via **HTTP/HTTPS** (registra `sw.js`); poi è installabile come app dal browser.

## 3. Dipendenze esterne (CDN) e comportamento offline
- **SheetJS (xlsx) 0.18.5** (export Excel) — `cdnjs.cloudflare.com`.
- Icone interfaccia: **SVG inline** + emoji; **font di sistema** → nessuna dipendenza da font/icon CDN.
- Offline: dopo la prima apertura online funziona **offline** (service worker `sw.js`). Se l'export Excel non è disponibile (offline al primo avvio), l'app ripiega su **CSV**.

## 4. Dati e privacy
- Salvataggio progetti: `localStorage`, chiave **`diagenergetica_projects_v1`**.
- Import/Export: **JSON** (progetto completo) ed **Excel** (multi-foglio per sezione).
- **Nessun dato viene inviato a server** fbc/terzi (l'unica chiamata esterna è il CDN della libreria Excel).

## 5. Inventario file
**Da pubblicare (necessari):**
| File | Ruolo |
|------|-------|
| `index.html` | Applicazione completa |
| `icon-192.png`, `icon-512.png` | Icone PWA |
| `manifest.webmanifest` | Manifesto PWA |
| `sw.js` | Service worker (cache offline) |

**Da NON pubblicare (sviluppo/scarti — escludere dal deploy):**
- `index_backup_20260610.html`, `index_old.html` — versioni precedenti/backup.
- `ChatGPT Image ... .png` — immagine sorgente usata per generare le icone.
- `make_icons.py` — script di build icone (vedi §7).
- `README.md` — questo documento.

## 6. Funzionalità (sintesi)
Gestione **progetti** (anagrafica sito) e **11 sezioni** di rilievo: Impianti termici, Illuminazione, Termografia, Air Leak, Gruppi frigo, Compressori, Caricabatterie muletti, HVAC, Chiusure trasparenti, Chiusure opache, Motori. Per ogni sezione: inserimento/modifica/duplica/elimina record, ricerca, **export Excel** (per sezione o completo) e **JSON**, con **import JSON**.

## 7. Manutenzione
- **Icone** (`icon-*.png`): rigenerabili con `python make_icons.py` (Python + Pillow).
- Dopo modifiche a file cacheabili, **incrementare** la costante `CACHE` in `sw.js`.

## 8. Compatibilità
Browser mobile e desktop moderni (Chrome/Edge/Safari/Firefox). Layout **mobile-first** (navigazione in basso, schede a tutta larghezza, dark mode AMOLED).
