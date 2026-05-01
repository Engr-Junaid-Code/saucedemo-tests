# ============================================================
# conftest.py — Fixtures & Hooks für alle Tests
# ============================================================

import sys, os
# seiten/ and testdaten/ live one level up from tests/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import pytest
import logging
from datetime import datetime
from pytest_html import extras
from playwright.sync_api import sync_playwright
from seiten.anmelde_seite import AnmeldeSeite
from testdaten.benutzer import BENUTZER

# ── Logger einrichten ──────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── Globaler Test-Zähler ───────────────────────────────────
_test_zaehler = {"nummer": 0}


# ══════════════════════════════════════════════════════════════
# PAGE FIXTURE (MUSS ZUERST KOMMEN!)
# ══════════════════════════════════════════════════════════════

@pytest.fixture(scope="function")
def page(request):
    """Fresh Page für jeden Test"""
    logger.info("🔧 Fixture: page wird vorbereitet")
    
    # ── Hole --headless Flag aus Kommandozeile ──────────────
    headless = True  # Default: headless mode
    
    if hasattr(request.config, "option"):
        # Wenn --headed Flag gesetzt wurde
        if hasattr(request.config.option, "headed") and request.config.option.headed:
            headless = False
        # Wenn --headless Flag gesetzt wurde
        elif hasattr(request.config.option, "headless") and request.config.option.headless:
            headless = True
    
    logger.info(f"🌐 Browser Mode: {'HEADED (sichtbar)' if not headless else 'HEADLESS (unsichtbar)'}")
    
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=headless)
    page = browser.new_page()
    yield page
    page.close()
    browser.close()
    playwright.stop()

# ══════════════════════════════════════════════════════════════
# HOOKS
# ══════════════════════════════════════════════════════════════

def pytest_runtest_setup(item):
    """Vor jedem Test: Nummer und Zeitstempel loggen"""
    _test_zaehler["nummer"] += 1
    nummer = _test_zaehler["nummer"]
    zeitstempel = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item._tc_nummer = f"TC-{nummer:03d}"
    item._tc_zeitstempel = zeitstempel
    logger.info(f"╔══ {item._tc_nummer} ══════════════════════════════")
    logger.info(f"║  📋 Test      : {item.name}")
    logger.info(f"║  🕐 Gestartet : {zeitstempel}")
    logger.info(f"╚{'═' * 44}")


def pytest_runtest_logreport(report):
    """Nach jedem Test: Status loggen"""
    if report.when == "call":
        if report.passed:
            logger.info("✅ BESTANDEN")
        elif report.failed:
            logger.error("❌ FEHLGESCHLAGEN")
        elif report.skipped:
            logger.warning("⏭️  ÜBERSPRUNGEN")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Screenshot bei Fehler aufnehmen — speichern + in HTML einbetten"""
    outcome = yield
    report = outcome.get_result()

    # ── TC-Nummer & Zeitstempel anhängen ───────────────────
    report.tc_nummer = getattr(item, "_tc_nummer", "TC-???")
    report.tc_zeitstempel = getattr(
        item,
        "_tc_zeitstempel",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    # ── Screenshot nur bei Fehler in der "call"-Phase ──────
    if report.when == "call" and report.failed:

        # Playwright page-Objekt aus den Fixtures holen
        page = None
        for fixture_name in ("page", "eingeloggte_seite",
                             "warenkorb_mit_artikel",
                             "warenkorb_mit_mehreren_artikeln",
                             "eingeloggte_seite_problem",
                             "eingeloggte_seite_error",
                             "eingeloggte_seite_visual",
                             "eingeloggte_seite_performance",
                             "anmelde_seite"):
            page = item.funcargs.get(fixture_name)
            if page is not None:
                break

        if page is not None:
            try:
                import base64
                import os
                from pathlib import Path

                # ── Ordner sicherstellen ───────────────────
                screenshot_ordner = Path("bildschirm")
                screenshot_ordner.mkdir(parents=True, exist_ok=True)

                # ── Dateiname: TC-Nummer + Testname + Zeitstempel ──
                zeitstempel_datei = datetime.now().strftime("%Y%m%d_%H%M%S")
                tc_nr = getattr(item, "_tc_nummer", "TC-000")
                sicherer_name = item.name.replace(
                    "/", "_"
                ).replace("::", "_").replace(" ", "_")
                dateiname = (
                    f"{tc_nr}_{sicherer_name}_{zeitstempel_datei}.png"
                )
                dateipfad = screenshot_ordner / dateiname

                # ── Screenshot aufnehmen & auf Disk speichern ──
                page.screenshot(path=str(dateipfad), full_page=True)
                logger.error(
                    f"📸 Screenshot gespeichert: bildschirm/{dateiname}"
                )

                # ── Auch als Base64 in HTML einbetten ─────
                with open(dateipfad, "rb") as f:
                    screenshot_b64 = base64.b64encode(
                        f.read()
                    ).decode("utf-8")

                screenshot_html = (
                    f'<div style="margin-top:10px;">'
                    f'<strong>📸 Screenshot bei Fehler:</strong>'
                    f'<br/>'
                    f'<small style="color:gray;">💾 Gespeichert: '
                    f'bildschirm/{dateiname}</small><br/>'
                    f'<img src="data:image/png;base64,{screenshot_b64}" '
                    f'style="max-width:100%;border:2px solid red;'
                    f'border-radius:6px;margin-top:6px;" />'
                    f'</div>'
                )

                if not hasattr(report, "extra"):
                    report.extra = []
                report.extra.append(extras.html(screenshot_html))

            except Exception as e:
                logger.warning(f"⚠️  Screenshot fehlgeschlagen: {e}")


def pytest_html_report_title(report):
    """Titel des HTML-Berichts"""
    report.title = "🧪 Saucedemo Test-Bericht"


def pytest_configure(config):
    """Metadaten im HTML-Bericht"""
    config._metadata = {
        "Projekt": "Saucedemo Playwright Tests",
        "Erstellt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Framework": "Playwright + pytest",
        "Sprache": "Python",
        "Umgebung": "https://www.saucedemo.com",
    }


# ══════════════════════════════════════════════════════════════
# HTML BERICHT — EXTRA SPALTEN
# ══════════════════════════════════════════════════════════════

def pytest_html_results_table_header(cells):
    """Füge TC-Nummer und Zeitstempel als Spalten hinzu"""
    cells.insert(1, "<th>TC-Nr.</th>")
    cells.insert(2, "<th>🕐 Zeitstempel</th>")


def pytest_html_results_table_row(report, cells):
    """Befülle die neuen Spalten pro Zeile"""
    tc_nr = getattr(report, "tc_nummer", "TC-???")
    tc_zeit = getattr(report, "tc_zeitstempel", "—")
    cells.insert(1, f"<td>{tc_nr}</td>")
    cells.insert(2, f"<td>{tc_zeit}</td>")


# ══════════════════════════════════════════════════════════════
# FIXTURES — LOGIN SEITE
# ══════════════════════════════════════════════════════════════

@pytest.fixture
def anmelde_seite(page):
    """Fixture: Gibt eine frische Login-Seite zurück"""
    logger.info("🔧 Fixture: anmelde_seite wird vorbereitet")
    seite = AnmeldeSeite(page)
    seite.navigiere_zu_anmeldung()
    return seite


# ══════════════════════════════════════════════════════════════
# PARAMETRIERTE FIXTURE: eingeloggte_seite (mit ALLEN Usern)
# ══════════════════════════════════════════════════════════════

@pytest.fixture(params=["standard", "problem", "fehler", "visual", "leistung"])
def eingeloggte_seite(request, page):
    """
    Fixture: Eingeloggter Benutzer (PARAMETRIERT mit ALLEN Usern)
    
    Test läuft automatisch mit JEDEM dieser Benutzer:
    - standard_user
    - problem_user
    - error_user
    - visual_user
    - performance_user
    
    VERWENDUNG:
    def test_something(self, eingeloggte_seite):
        # Läuft 5 Mal (einmal pro User)
        pass
    """
    user_type = request.param
    logger.info(f"🔧 Fixture: eingeloggte_seite wird mit {user_type} vorbereitet")
    
    # Hole Benutzer-Daten
    if user_type == "standard":
        benutzername = BENUTZER["standard"]["benutzername"]
        passwort = BENUTZER["standard"]["passwort"]
    elif user_type == "problem":
        benutzername = BENUTZER["problem"]["benutzername"]
        passwort = BENUTZER["problem"]["passwort"]
    elif user_type == "fehler":
        benutzername = BENUTZER["fehler"]["benutzername"]
        passwort = BENUTZER["fehler"]["passwort"]
    elif user_type == "visual":
        benutzername = BENUTZER["visual"]["benutzername"]
        passwort = BENUTZER["visual"]["passwort"]
    elif user_type == "leistung":
        benutzername = BENUTZER["leistung"]["benutzername"]
        passwort = BENUTZER["leistung"]["passwort"]
    
    # Login
    seite = AnmeldeSeite(page)
    seite.navigiere_zu_anmeldung()
    seite.anmelden_und_warten(benutzername, passwort)
    
    # Speichere User-Typ für Test-Zugriff
    page.user_type = user_type
    
    logger.info(f"✅ {user_type}-Benutzer erfolgreich eingeloggt")
    return page


# ══════════════════════════════════════════════════════════════
# EINZELNE USER FIXTURES (für spezifische Tests)
# ══════════════════════════════════════════════════════════════

@pytest.fixture
def eingeloggte_seite_standard(page):
    """Fixture: Nur Standard-Benutzer"""
    logger.info("🔧 Fixture: eingeloggte_seite_standard wird vorbereitet")
    seite = AnmeldeSeite(page)
    seite.navigiere_zu_anmeldung()
    seite.anmelden_und_warten(
        BENUTZER["standard"]["benutzername"],
        BENUTZER["standard"]["passwort"]
    )
    page.user_type = "standard"
    logger.info("✅ Standard-Benutzer erfolgreich eingeloggt")
    return page


@pytest.fixture
def eingeloggte_seite_problem(page):
    """Fixture: Nur Problem-Benutzer"""
    logger.info("🔧 Fixture: eingeloggte_seite_problem wird vorbereitet")
    seite = AnmeldeSeite(page)
    seite.navigiere_zu_anmeldung()
    seite.anmelden_und_warten(
        BENUTZER["problem"]["benutzername"],
        BENUTZER["problem"]["passwort"]
    )
    page.user_type = "problem"
    logger.info("✅ Problem-Benutzer erfolgreich eingeloggt")
    return page


@pytest.fixture
def eingeloggte_seite_error(page):
    """Fixture: Nur Error-Benutzer"""
    logger.info("🔧 Fixture: eingeloggte_seite_error wird vorbereitet")
    seite = AnmeldeSeite(page)
    seite.navigiere_zu_anmeldung()
    seite.anmelden_und_warten(
        BENUTZER["error"]["benutzername"],
        BENUTZER["error"]["passwort"]
    )
    page.user_type = "error"
    logger.info("✅ Error-Benutzer erfolgreich eingeloggt")
    return page


@pytest.fixture
def eingeloggte_seite_visual(page):
    """Fixture: Nur Visual-Benutzer"""
    logger.info("🔧 Fixture: eingeloggte_seite_visual wird vorbereitet")
    seite = AnmeldeSeite(page)
    seite.navigiere_zu_anmeldung()
    seite.anmelden_und_warten(
        BENUTZER["visual"]["benutzername"],
        BENUTZER["visual"]["passwort"]
    )
    page.user_type = "visual"
    logger.info("✅ Visual-Benutzer erfolgreich eingeloggt")
    return page


@pytest.fixture
def eingeloggte_seite_performance(page):
    """Fixture: Nur Performance-Benutzer"""
    logger.info("🔧 Fixture: eingeloggte_seite_performance wird vorbereitet")
    seite = AnmeldeSeite(page)
    seite.navigiere_zu_anmeldung()
    seite.anmelden_und_warten(
        BENUTZER["performance"]["benutzername"],
        BENUTZER["performance"]["passwort"]
    )
    page.user_type = "performance"
    logger.info("✅ Performance-Benutzer erfolgreich eingeloggt")
    return page


# ══════════════════════════════════════════════════════════════
# FIXTURES — WARENKORB
# ══════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════
# PARAMETRIERTE FIXTURES — WARENKORB mit ALLEN USERN
# ══════════════════════════════════════════════════════════════

@pytest.fixture(params=["standard", "problem", "fehler", "visual", "leistung"])
def warenkorb_mit_artikel(request, page):
    """
    Fixture: Artikel im Warenkorb (PARAMETRIERT mit ALLEN Usern)
    
    Test läuft automatisch mit JEDEM dieser Benutzer:
    - standard_user
    - problem_user
    - error_user
    - visual_user
    - performance_user
    """
    from seiten.produkt_seite import ProduktSeite
    
    user_type = request.param
    logger.info(f"🔧 Fixture: warenkorb_mit_artikel wird mit {user_type} vorbereitet")
    
    # ── Hole Benutzer-Daten ────────────────────────────────────
    if user_type == "standard":
        benutzername = BENUTZER["standard"]["benutzername"]
        passwort = BENUTZER["standard"]["passwort"]
    elif user_type == "problem":
        benutzername = BENUTZER["problem"]["benutzername"]
        passwort = BENUTZER["problem"]["passwort"]
    elif user_type == "fehler":
        benutzername = BENUTZER["fehler"]["benutzername"]
        passwort = BENUTZER["fehler"]["passwort"]
    elif user_type == "visual":
        benutzername = BENUTZER["visual"]["benutzername"]
        passwort = BENUTZER["visual"]["passwort"]
    elif user_type == "leistung":
        benutzername = BENUTZER["leistung"]["benutzername"]
        passwort = BENUTZER["leistung"]["passwort"]
    
    # ── Login ───────────────────────────────────────────────────
    seite = AnmeldeSeite(page)
    seite.navigiere_zu_anmeldung()
    seite.anmelden_und_warten(benutzername, passwort)
    
    # ── Füge Artikel zum Warenkorb hinzu ────────────────────────
    produkte = ProduktSeite(page)
    produkte.fuege_produkt_zum_warenkorb_hinzu("Sauce Labs Backpack")
    
    # ── Speichere User-Typ ──────────────────────────────────────
    page.user_type = user_type
    
    logger.info(f"✅ {user_type}-Benutzer mit Artikel im Warenkorb vorbereitet")
    return page


@pytest.fixture(params=["standard", "problem", "fehler", "visual", "leistung"])
def warenkorb_mit_mehreren_artikeln(request, page):
    """
    Fixture: Mehrere Artikel im Warenkorb (PARAMETRIERT mit ALLEN Usern)
    
    Test läuft automatisch mit JEDEM dieser Benutzer
    """
    from seiten.produkt_seite import ProduktSeite
    
    user_type = request.param
    logger.info(f"🔧 Fixture: warenkorb_mit_mehreren_artikeln wird mit {user_type} vorbereitet")
    
    # ── Hole Benutzer-Daten ────────────────────────────────────
    if user_type == "standard":
        benutzername = BENUTZER["standard"]["benutzername"]
        passwort = BENUTZER["standard"]["passwort"]
    elif user_type == "problem":
        benutzername = BENUTZER["problem"]["benutzername"]
        passwort = BENUTZER["problem"]["passwort"]
    elif user_type == "fehler":
        benutzername = BENUTZER["fehler"]["benutzername"]
        passwort = BENUTZER["fehler"]["passwort"]
    elif user_type == "visual":
        benutzername = BENUTZER["visual"]["benutzername"]
        passwort = BENUTZER["visual"]["passwort"]
    elif user_type == "leistung":
        benutzername = BENUTZER["leistung"]["benutzername"]
        passwort = BENUTZER["leistung"]["passwort"]
    
    # ── Login ───────────────────────────────────────────────────
    seite = AnmeldeSeite(page)
    seite.navigiere_zu_anmeldung()
    seite.anmelden_und_warten(benutzername, passwort)
    
    # ── Füge Artikel zum Warenkorb hinzu ────────────────────────
    produkte = ProduktSeite(page)
    produkte.fuege_produkt_zum_warenkorb_hinzu("Sauce Labs Backpack")
    produkte.fuege_produkt_zum_warenkorb_hinzu("Sauce Labs Bike Light")
    produkte.fuege_produkt_zum_warenkorb_hinzu("Sauce Labs Bolt T-Shirt")
    
    # ── Speichere User-Typ ──────────────────────────────────────
    page.user_type = user_type
    
    logger.info(f"✅ {user_type}-Benutzer mit 3 Artikeln im Warenkorb vorbereitet")
    return page

