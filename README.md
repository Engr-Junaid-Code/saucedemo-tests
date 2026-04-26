Überblick
Dieses Repository enthält eine Playwright + pytest Test-Suite für den Demo‑Shop https://www.saucedemo.com/.
Ziel ist es, eine saubere Regression‑Suite aufzubauen – inklusive HTML‑Report mit Logs und Screenshots bei Fehlern.

---

# 🧪 Saucedemo Playwright Test-Suite

Eine umfassende **Automatisierungstestsuite** für die [Saucedemo-Webshop](https://www.saucedemo.com/) mit **Playwright**, **Python** und **pytest**.

---

## 📋 Inhaltsverzeichnis

- [Überblick](#überblick)
- [Features](#features)
- [Voraussetzungen](#voraussetzungen)
- [Installation](#installation)
- [Projektstruktur](#projektstruktur)
- [Tests ausführen](#tests-ausführen)
- [Page Object Model](#page-object-model)
- [HTML-Reports](#html-reports)
- [Troubleshooting](#troubleshooting)
- [Kontakt](#kontakt)

---

## 🎯 Überblick

Diese Test-Suite automatisiert **End-to-End-Tests** für einen E-Commerce-Webshop mit verschiedenen Benutzertypen:

- **Standard User** — Normaler Benutzer
- **Problem User** — Benutzer mit bekannten Bugs
- **Fehler User** — Fehlerbenutzer
- **Visual User** — Visueller Benutzer
- **Leistung User** — Performance-fokussierter Benutzer

Alle Tests laufen **parametrisiert** — jeder Test wird automatisch mit **ALLEN 5 Benutzern** ausgeführt! 🚀

---

## ✨ Features

✅ **Page Object Model (POM)** — Strukturierte, wartbare Tests  
✅ **Parametrisierte Fixtures** — Ein Test, alle User-Typen  
✅ **Deutsche Test-Klassen & Methoden** — Lesbare Test-Namen  
✅ **Headless & Headed Mode** — Flexibles Browser-Rendering  
✅ **HTML-Reports mit Screenshots** — Detaillierte Test-Berichte  
✅ **Dynamische Report-Naming** — Reports nach Test-Kategorie benannt  
✅ **Logging & Debugging** — Umfangreiches Logging für jeden Test  
✅ **CI/CD Ready** — Einfache Integration in Pipeline  

---

## 📦 Voraussetzungen

- **Python 3.8+** oder höher
- **pip** (Python Package Manager)
- **Git** (optional)

---

## 🔧 Installation

1. Repository klonen (oder ZIP herunterladen)
git clone <repository-url>
2.Virtuelle Umgebung erstellen 
# Windows
python -m venv venv
venv\Scripts\activate
# macOS/Linux
python3 -m venv venv
source venv/bin/activate
3. Abhängigkeiten installieren
pip install -r requirements.txt
4. Playwright Browser installieren
playwright install chromium

---

## 📁 Projektstruktur
tests/ – Testfälle
seiten/ – Page Objects
testdaten/ – Testdaten (Benutzer etc.)
bildschirm/ – Screenshots bei Fehlern

saucedemo-tests/
├── tests/                          # 🧪 Tests
│   ├──conftest.py                  # ⚙️ Pytest Konfiguration & Fixtures
│   ├── test_anmeldung.py           # Tests für Login
│   ├── test_kasse.py               # Tests für Kasse
│   ├── test_navigation.py          # Tests für Navigation
│   ├── test_produkte.py            # Tests für Produktseite
│   ├── test_sitzung.py             # Tests für Sitzung
│   ├── test_visuell.py             # Tests für Visuell UI
│   ├── test_warenkorb.py           # Tests für Warenkorb
│
├── seiten/                         # 📄 Page Object Models
│   ├── anmelde_seite.py            # Login-Seite POM
│   ├── basis_seite.py              # Basis-Klasse für alle Seiten
│   ├── kasse_seite.py              # Kasse-Klasse für alle Seiten
│   ├── basis_navigation.py         # Basis-Navigation für alle Seiten
│   ├── produkt_seite.py            # Produktseite POM
│   ├── warenkorb_seite.py          # Warenkorb-Seite POM
│
├── testdaten/                      # 📊 Test-Daten
│   ├── benutzer.py                 # Benutzer-Credentials
│
├── pytest.ini                      # 📋 Pytest Einstellungen
├── README.md                       # 📖 Diese Datei
├── requirements.txt                # 📦 Python-Abhängigkeiten
├── testlauf.py                     # 📋 Main Test Datei

---

## 🚀 Tests ausführen
Führen Sie „testlauf.py“ aus, woraufhin sich der interaktive Chatbot im CMD öffnet. Dort können Sie wählen, ob Sie den Test im Headless- oder im Headed-Modus ausführen möchten.
Anschließend können Sie den Browser auswählen: Chromium, Firefox oder WebKit (Safari). Wählen Sie dann die Testgruppe aus, um entweder die gesamte Regressionstestsuite 
oder nur funktionsspezifische Tests auszuführen. Bestätigen Sie abschließend die Auswahl und starten Sie den Test.
Es ist auch möglich, Tests für eine bestimmte Seite, einen bestimmten Benutzer oder ein bestimmtes Stichwort direkt über die Eingabeaufforderung auszuführen. 

---

## 📄 Page Object Model
Das Page Object Model (POM) strukturiert Tests übersichtlich. Jede Seite hat ihre eigene Klasse mit Methoden:
Beispiel: ProduktSeite
from seiten.basis_seite import BasisSeite
class ProduktSeite(BasisSeite):
    """Seite mit Produkten"""
    
    def __init__(self, page):
        super().__init__(page)
    
    def hole_produktanzahl(self):
        """Anzahl der Produkte zurückgeben"""
        return len(self.page.locator("[data-test='inventory-item']").all())
    
    def fuege_produkt_zum_warenkorb_hinzu(self, produktname):
        """Produkt zum Warenkorb hinzufügen"""
        self.page.locator(f"button:has-text('{produktname}')").click()
    
    def sortiere_nach(self, sortierkriterium):
        """Nach Kriterium sortieren"""
        self.page.select_option("[data-test='product-sort-container']", sortierkriterium)
In Tests verwenden:
def test_artikel_hinzufuegen(self, eingeloggte_seite):
    """Artikel zum Warenkorb hinzufügen"""
    produkte = ProduktSeite(eingeloggte_seite)
    produkte.fuege_produkt_zum_warenkorb_hinzu("Sauce Labs Backpack")
    assert produkte.hole_warenkorb_anzahl() > 0

---

## 📊 HTML-Reports
✅ Detaillierte Test-Ergebnisse — PASSED/FAILED/SKIPPED
✅ Screenshots — Für fehlgeschlagene Tests
✅ Logs — Vollständige Logger-Ausgabe
✅ Timing — Wie lange dauerte jeder Test?
✅ Metadata — Test-Umgebung, Framework-Info

---

## 🐛 Troubleshooting
Problem 1: ModuleNotFoundError: No module named 'seiten'
Lösung: #Stelle sicher, dass du im Project-Root-Verzeichnis bist -> cd saucedemo-tests
		# Installiere Dependencies neu -> pip install -r requirements.txt		
Problem 2: IndentationError: unindent does not match
Lösung: Nutze Spaces statt Tabs -> VS Code: Ctrl+Shift+P → Convert Indentation to Spaces
Problem 3: Playwright Browser nicht installiert
Lösung: playwright install chromium

---
## Kontakt
Muhammad Junaid Raza
Engr_Junaid@yahoo.com








