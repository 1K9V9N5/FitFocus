# ⚡ FitFocus Dashboard

Ein kompaktes, mobiles Fitness- & Ernährungs-Dashboard, optimiert auf eine einzige Smartphone-Bildschirmseite ohne Scrollaufwand. Dieses Projekt demonstriert die saubere Integration einer relationalen Datenbank mit einem modernen Web-Framework unter Anwendung des CRUD-Prinzips.

## 🚀 Features & Core-Logik
- **One-Screen-Layout:** Volle Übersicht über Tagesziele und Vorräte ohne langes Scrollen.
- **Dauerhafte Speicherung:** Vollständige Integration von **SQLite** zur persistenten Datenspeicherung.
- **Professionelles CRUD-Prinzip:** Live-Updates der Datenbank bei Benutzerinteraktion (Haken setzen, Vorrat reduzieren).
- **Modernes UI-Design:** Individuell angepasstes Light/Dark-Theme im sportlichen Petrol-Mint-Look.

## 🛠️ Tech-Stack
- **Backend/Logik:** Python 3
- **Datenbank:** SQLite (relational)
- **Frontend:** Streamlit Framework

## 📈 Portfolio-Kontext
Dieses Projekt ist Teil meines praktischen Portfolios (`1K9V9N5`), mit dem ich meine Fähigkeiten im Bereich der Python-Entwicklung und relationalen Datenbanken demonstriere. Es dokumentiert meinen Lernfortschritt beim Aufbau von persistenten Web-Anwendungen, dem State Management (Zustandsverwaltung) in Frameworks und dem strukturierten Refactoring von Quellcode für berufliche Anforderungen.

## ⏰ Smart-Wecker & WhatsApp API Integration
Das Dashboard verfügt über eine integrierte Schnittstelle zur automatisierten Benachrichtigung via WhatsApp (unter Nutzung der CallMeBot-API). 

**Entwickler-Hinweis:** Aufgrund der restriktiven API-Regulierungen von Meta (WhatsApp) kann es bei externen Gateway-Servern temporär zu Verzögerungen bei der Schlüssel-Generierung kommen. Der Quellcode nutzt die standardbasierte HTTP-GET-Methode (`requests`), um eine nahtlose Übertragung zu gewährleisten, sobald der Drittanbieter-Dienst aktiv ist.
