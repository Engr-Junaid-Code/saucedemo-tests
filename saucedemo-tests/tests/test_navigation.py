# ============================================================
# Tests: Navigation
# ============================================================

import pytest
from seiten.navigation_seite import NavigationSeite
from seiten.produkt_seite    import ProduktSeite


class TestNavigation:
    """Tests für die Navigation"""

    def test_burger_menu_oeffnet(self, eingeloggte_seite):
        """Burger-Menü öffnet sich"""
        nav = NavigationSeite(eingeloggte_seite)
        nav.oeffne_menu()
        assert nav.ist_menu_offen()

    def test_burger_menu_schliesst(self, eingeloggte_seite):
        """Burger-Menü schließt sich"""
        nav = NavigationSeite(eingeloggte_seite)
        nav.oeffne_menu()
        nav.schliesse_menu()
        eingeloggte_seite.wait_for_timeout(500)
        assert not nav.ist_menu_offen()

    def test_abmelden_funktioniert(self, eingeloggte_seite):
        """Abmelden leitet zur Login-Seite weiter"""
        nav = NavigationSeite(eingeloggte_seite)
        nav.abmelden()
        assert "inventory" not in nav.hole_aktuelle_url()

    def test_gehe_zu_warenkorb(self, eingeloggte_seite):
        """Warenkorb-Link navigiert zum Warenkorb"""
        nav = NavigationSeite(eingeloggte_seite)
        nav.gehe_zu_warenkorb()
        assert "cart.html" in nav.hole_aktuelle_url()

    def test_gehe_zu_alle_artikel(self, eingeloggte_seite):
        """'Alle Artikel' navigiert zur Produktliste"""
        nav = NavigationSeite(eingeloggte_seite)
        nav.gehe_zu_warenkorb()
        nav.gehe_zu_alle_artikel()
        assert "inventory.html" in nav.hole_aktuelle_url()

    def test_warenkorb_badge_leer(self, eingeloggte_seite):
        """Warenkorb-Badge ist leer nach Login"""
        nav = NavigationSeite(eingeloggte_seite)
        assert nav.hole_warenkorb_anzahl() == 0

    def test_warenkorb_badge_aktualisiert(self, eingeloggte_seite):
        """Warenkorb-Badge aktualisiert sich nach Hinzufügen"""
        produkte = ProduktSeite(eingeloggte_seite)
        produkte.fuege_produkt_zum_warenkorb_hinzu("Sauce Labs Backpack")
        nav = NavigationSeite(eingeloggte_seite)
        assert nav.hole_warenkorb_anzahl() == 1

    def test_app_zuruecksetzen(self, eingeloggte_seite):
        """App-Reset leert den Warenkorb"""
        produkte = ProduktSeite(eingeloggte_seite)
        produkte.fuege_produkt_zum_warenkorb_hinzu("Sauce Labs Backpack")
        nav = NavigationSeite(eingeloggte_seite)
        assert nav.hole_warenkorb_anzahl() == 1
        nav.setze_app_zurueck()
        assert nav.hole_warenkorb_anzahl() == 0
