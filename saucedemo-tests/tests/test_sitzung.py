# ============================================================
# Tests: Sitzung & Session-Verhalten
# ============================================================

import pytest
from seiten.anmelde_seite    import AnmeldeSeite
from seiten.produkt_seite    import ProduktSeite
from seiten.navigation_seite import NavigationSeite
from testdaten.benutzer      import BENUTZER


class TestSitzungPersistenz:
    """Tests für Session-Persistenz"""

    def test_warenkorb_bleibt_nach_navigation(self, eingeloggte_seite):
        """Warenkorb-Inhalt bleibt nach Navigation erhalten"""
        produkte = ProduktSeite(eingeloggte_seite)
        produkte.fuege_produkt_zum_warenkorb_hinzu("Sauce Labs Backpack")
        nav = NavigationSeite(eingeloggte_seite)
        nav.gehe_zu_warenkorb()
        nav.gehe_zu_alle_artikel()
        assert produkte.hole_warenkorb_anzahl() == 1

    def test_warenkorb_persistent_nach_logout_login(self, page):
        """
        [BEKANNTER BUG] Saucedemo speichert Warenkorb im localStorage.
        Nach Logout + Login bleibt der Warenkorb erhalten.
        """
        anmeldung = AnmeldeSeite(page)
        anmeldung.navigiere_zu_anmeldung()
        anmeldung.anmelden_und_warten(
            BENUTZER["standard"]["benutzername"],
            BENUTZER["standard"]["passwort"],
        )

        produkte = ProduktSeite(page)
        produkte.fuege_produkt_zum_warenkorb_hinzu("Sauce Labs Backpack")
        assert produkte.hole_warenkorb_anzahl() == 1

        nav = NavigationSeite(page)
        nav.abmelden()

        # Neu einloggen
        anmeldung.anmelden_und_warten(
            BENUTZER["standard"]["benutzername"],
            BENUTZER["standard"]["passwort"],
        )

        # Bekannter Bug: Warenkorb bleibt nach Logout erhalten
        anzahl = produkte.hole_warenkorb_anzahl()
        assert anzahl == 1, (
            f"[BEKANNTER BUG] Warenkorb nach Logout nicht geleert. "
            f"Erwartet: 1, Tatsächlich: {anzahl}"
        )

    def test_warenkorb_leer_nach_localStorage_reset(self, page):
        """Warenkorb ist nach localStorage-Reset leer"""
        anmeldung = AnmeldeSeite(page)
        anmeldung.navigiere_zu_anmeldung()
        anmeldung.anmelden_und_warten(
            BENUTZER["standard"]["benutzername"],
            BENUTZER["standard"]["passwort"],
        )

        produkte = ProduktSeite(page)
        produkte.fuege_produkt_zum_warenkorb_hinzu("Sauce Labs Backpack")
        assert produkte.hole_warenkorb_anzahl() == 1

        nav = NavigationSeite(page)
        nav.abmelden()

        # localStorage leeren — simuliert echten Browser-Reset
        page.evaluate("window.localStorage.clear()")

        anmeldung.anmelden_und_warten(
            BENUTZER["standard"]["benutzername"],
            BENUTZER["standard"]["passwort"],
        )
        assert produkte.hole_warenkorb_anzahl() == 0

    def test_direkt_url_ohne_login_blockiert(self, page):
        """Direkter URL-Zugriff ohne Login wird blockiert"""
        seiten    = [
            "inventory.html",
            "cart.html",
            "checkout-step-one.html",
            "checkout-step-two.html",
        ]
        anmeldung = AnmeldeSeite(page)
        for seite in seiten:
            anmeldung.navigiere_zu(seite)
            page.wait_for_load_state("domcontentloaded")
            assert anmeldung.ist_auf_anmeldeseite(), \
                f"Seite '{seite}' sollte ohne Login blockiert sein!"


class TestLeistungsBenutzer:
    """Tests für den Leistungs-Benutzer"""

    def test_leistungs_benutzer_login(self, page):
        """Leistungs-Benutzer kann sich einloggen (auch wenn langsamer)"""
        anmeldung = AnmeldeSeite(page)
        anmeldung.navigiere_zu_anmeldung()
        anmeldung.anmelden_und_warten(
            BENUTZER["leistung"]["benutzername"],
            BENUTZER["leistung"]["passwort"],
            timeout=15000,
        )
        assert "inventory.html" in page.url
