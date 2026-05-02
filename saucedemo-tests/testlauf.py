# ============================================================
# testlauf.py — Interaktiver CLI Test-Runner mit HTML-Bericht
# ============================================================

import pytest
import sys
import os
from datetime import datetime

# ── Konfiguration ──────────────────────────────────────────
BERICHT_ORDNER  = "berichte"
BILDSCHIRMFOTOS = "bildschirmfotos"

# ── Farben (ANSI) ──────────────────────────────────────────
ROT   = "\033[91m"
GRUEN = "\033[92m"
GELB  = "\033[93m"
BLAU  = "\033[94m"
LILA  = "\033[95m"
CYAN  = "\033[96m"
WEISS = "\033[97m"
GRAU  = "\033[90m"
FETT  = "\033[1m"
RESET = "\033[0m"


# ══════════════════════════════════════════════════════════════
# HILFSFUNKTIONEN
# ══════════════════════════════════════════════════════════════

def loesche_konsole():
    os.system("cls" if os.name == "nt" else "clear")


def trennlinie(farbe=BLAU, zeichen="═", breite=54):
    print(f"{farbe}{zeichen * breite}{RESET}")


def titel_block(text):
    trennlinie()
    print(f"{LILA}{FETT}  {text}{RESET}")
    trennlinie()


def eingabe_holen(prompt, gueltige_optionen):
    """Wiederhole Eingabe bis eine gültige Option gewählt wird"""
    while True:
        auswahl = input(f"\n{CYAN}{prompt}{RESET} ").strip().lower()
        if auswahl in gueltige_optionen:
            return auswahl
        print(f"{ROT}  ❌ Ungültige Eingabe. Bitte erneut versuchen.{RESET}")


def ordner_vorbereiten():
    for ordner in [BERICHT_ORDNER]:
        os.makedirs(ordner, exist_ok=True)


# ══════════════════════════════════════════════════════════════
# MENÜS
# ══════════════════════════════════════════════════════════════

def zeige_willkommen():
    loesche_konsole()
    trennlinie(BLAU, "═", 54)
    print(f"{LILA}{FETT}   🧪 SAUCEDEMO TEST-RUNNER{RESET}")
    print(f"{GRAU}   Playwright · Python · pytest{RESET}")
    trennlinie(BLAU, "═", 54)
    print()


def modus_menu():
    """Schritt 1: Headed oder Headless"""
    print(f"{FETT}{WEISS}  👁️  MODUS AUSWÄHLEN{RESET}")
    print()
    print(f"  {GELB}1{RESET}  →  🫣 Headless  (kein Browser-Fenster)")
    print(f"  {GELB}2{RESET}  →  👁️  Headed    (Browser sichtbar)")
    print()
    auswahl = eingabe_holen("Deine Wahl [1/2]:", ["1", "2"])
    headed  = auswahl == "2"
    modus   = "Headed (Browser sichtbar)" if headed else "Headless"
    print(f"\n  {GRUEN}✅ Modus: {modus}{RESET}")
    return headed


def browser_menu():
    """Schritt 2: Browser wählen"""
    print()
    trennlinie(BLAU, "─", 54)
    print(f"{FETT}{WEISS}  🌐 BROWSER AUSWÄHLEN{RESET}")
    print()
    print(f"  {GELB}a{RESET}  →  Chromium  (Standard)")
    print(f"  {GELB}b{RESET}  →  Firefox")
    print(f"  {GELB}c{RESET}  →  WebKit    (Safari)")
    print()
    browser_map = {"a": "chromium", "b": "firefox", "c": "webkit"}
    auswahl     = eingabe_holen("Deine Wahl [a/b/c]:", list(browser_map.keys()))
    browser     = browser_map[auswahl]
    print(f"\n  {GRUEN}✅ Browser: {browser.capitalize()}{RESET}")
    return browser


def testgruppe_menu():
    """Schritt 3: Testgruppe wählen"""
    print()
    trennlinie(BLAU, "─", 54)
    print(f"{FETT}{WEISS}  🎯 TESTGRUPPE AUSWÄHLEN{RESET}")
    print()
    print(f"  {GELB}r{RESET}  →  🧪 Regression Test suite (Alle Tests)")
    print(f"  {GELB}a{RESET}  →  🔐 Anmeldung")
    print(f"  {GELB}p{RESET}  →  📦 Produkte")
    print(f"  {GELB}w{RESET}  →  🛒 Warenkorb")
    print(f"  {GELB}k{RESET}  →  💳 Kasse")
    print(f"  {GELB}n{RESET}  →  🧭 Navigation")
    print(f"  {GELB}s{RESET}  →  🔄 Sitzung")
    print(f"  {GELB}v{RESET}  →  🎨 Visuell-UI")
    print()
    gruppe_map = {
        "r": None,
        "a": "Anmeldung",
        "p": "Produkt",
        "w": "Warenkorb",
        "k": "Kasse",
        "n": "Navigation",
        "s": "Sitzung",
        "v": "Visuell",
    }
    auswahl = eingabe_holen(
        "Deine Wahl [r/a/p/w/k/n/s/v]:",
        list(gruppe_map.keys())
    )
    gruppe = gruppe_map[auswahl]
    name   = "Alle Tests" if gruppe is None else gruppe
    print(f"\n  {GRUEN}✅ Testgruppe: {name}{RESET}")
    return gruppe


# ══════════════════════════════════════════════════════════════
# ZUSAMMENFASSUNG
# ══════════════════════════════════════════════════════════════

def zeige_zusammenfassung(browser, headed, gruppe):
    print()
    trennlinie(BLAU, "─", 54)
    print(f"{FETT}{WEISS}  📋 ZUSAMMENFASSUNG{RESET}")
    print()
    print(f"  🌐 Browser   : {CYAN}{browser.capitalize()}{RESET}")
    modus = "Headed" if headed else "Headless"
    print(f"  👁️  Modus     : {CYAN}{modus}{RESET}")
    name  = "Alle Tests" if gruppe is None else gruppe
    print(f"  🎯 Gruppe    : {CYAN}{name}{RESET}")
    print()
    trennlinie(BLAU, "─", 54)
    auswahl = eingabe_holen(
        "Tests jetzt starten? [j = Ja / n = Neu starten]:",
        ["j", "n"]
    )
    return auswahl == "j"


# ══════════════════════════════════════════════════════════════
# TESTS AUSFÜHREN
# ══════════════════════════════════════════════════════════════

def fuehre_tests_aus(browser, headed, gruppe):
    """Führe pytest mit den gewählten Optionen aus"""
    ordner_vorbereiten()
    zeitstempel = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    bericht     = os.path.join(BERICHT_ORDNER, f"bericht_{zeitstempel}.html")

    print()
    trennlinie(BLAU, "═", 54)
    print(f"{LILA}{FETT}  🚀 TESTS WERDEN GESTARTET...{RESET}")
    trennlinie(BLAU, "═", 54)
    print(f"\n  📄 Bericht wird gespeichert in:\n  {GRAU}{bericht}{RESET}\n")
    trennlinie(BLAU, "─", 54)
    print()

    # ── pytest Argumente ───────────────────────────────────
    args = [
    "tests/",
    f"--browser={browser}",
    f"--html={bericht}",
    "--self-contained-html",
    "--tb=short",
    "-v",
    "--no-header",
    "-p", "no:warnings",
    "--log-level=INFO",           # ✅ Logs für alle Tests
    "--capture=no",               # ✅ Stdout nicht unterdrücken
    ]


    if headed:
        args.append("--headed")

    if gruppe:
        args.extend(["-k", gruppe])

    ergebnis = pytest.main(args)

    # ── Ergebnis anzeigen ──────────────────────────────────
    print()
    trennlinie(BLAU, "═", 54)
    if ergebnis == 0:
        print(f"{GRUEN}{FETT}  ✅  ALLE TESTS BESTANDEN!{RESET}")
    elif ergebnis == 1:
        print(f"{ROT}{FETT}  ❌  EINIGE TESTS FEHLGESCHLAGEN!{RESET}")
    elif ergebnis == 2:
        print(f"{GELB}{FETT}  ⚠️   TESTS UNTERBROCHEN!{RESET}")
    elif ergebnis == 5:
        print(f"{GELB}{FETT}  ⚠️   KEINE TESTS GEFUNDEN!{RESET}")
    else:
        print(f"{GELB}{FETT}  ⚠️   FEHLER (Code {ergebnis}){RESET}")

    print()
    print(f"  📄 Bericht: {CYAN}{bericht}{RESET}")
    trennlinie(BLAU, "═", 54)
    return bericht


# ══════════════════════════════════════════════════════════════
# NACH DEM TESTLAUF
# ══════════════════════════════════════════════════════════════

def nach_testlauf(bericht):
    print()
    print(f"  {GELB}1{RESET}  →  📄 Bericht im Browser öffnen")
    print(f"  {GELB}2{RESET}  →  🔄 Neuen Testlauf starten")
    print(f"  {GELB}3{RESET}  →  🚪 Beenden")
    print()
    auswahl = eingabe_holen("Deine Wahl [1/2/3]:", ["1", "2", "3"])
    if auswahl == "1":
        import webbrowser
        webbrowser.open(f"file://{os.path.abspath(bericht)}")
        print(f"\n  {GRUEN}✅ Bericht wird geöffnet...{RESET}\n")
        return "neu"
    elif auswahl == "2":
        return "neu"
    else:
        print(f"\n  {GRAU}👋 Auf Wiedersehen!{RESET}\n")
        return "beenden"


# ══════════════════════════════════════════════════════════════
# HAUPTPROGRAMM
# ══════════════════════════════════════════════════════════════

def main():
    while True:
        zeige_willkommen()
        headed  = modus_menu()
        browser = browser_menu()
        gruppe  = testgruppe_menu()
        if not zeige_zusammenfassung(browser, headed, gruppe):
            continue
        bericht = fuehre_tests_aus(browser, headed, gruppe)
        aktion  = nach_testlauf(bericht)
        if aktion == "beenden":
            break


if __name__ == "__main__":
    main()
