# ============================================================
# Tests: Visuell / UI
# ============================================================

import pytest
from seiten.produkt_seite    import ProduktSeite
from seiten.navigation_seite import NavigationSeite
from seiten.anmelde_seite    import AnmeldeSeite


class TestUI:
    """Tests für UI-Elemente"""

    def test_produktseite_hat_titel(self, eingeloggte_seite):
        """Produktseite hat sichtbaren Titel"""
        produkte = ProduktSeite(eingeloggte_seite)
        assert produkte.hole_seiten_titel() != ""

    def test_warenkorb_icon_sichtbar(self, eingeloggte_seite):
        """Warenkorb-Icon ist sichtbar"""
        nav = NavigationSeite(eingeloggte_seite)
        assert nav.ist_element_sichtbar(NavigationSeite.WARENKORB_LINK)

    def test_burger_menu_sichtbar(self, eingeloggte_seite):
        """Burger-Menü ist sichtbar"""
        nav = NavigationSeite(eingeloggte_seite)
        assert nav.ist_element_sichtbar(NavigationSeite.BURGER_MENU)

    def test_login_logo_sichtbar(self, page):
        """Login-Seite zeigt das Logo"""
        anmeldung = AnmeldeSeite(page)
        anmeldung.navigiere_zu_anmeldung()
        assert anmeldung.ist_element_sichtbar(".login_logo")

    def test_produkte_haben_bilder(self, eingeloggte_seite):
        """Alle Produkte haben Bilder"""
        bilder = eingeloggte_seite.locator(".inventory_item_img img").all()
        assert len(bilder) == 6
        for bild in bilder:
            src = bild.get_attribute("src")
            assert src and len(src) > 0

    def test_produkte_haben_beschreibung(self, eingeloggte_seite):
        """Alle Produkte haben Beschreibungen"""
        beschreibungen = eingeloggte_seite.locator(
            ".inventory_item_desc"
        ).all_inner_texts()
        for beschreibung in beschreibungen:
            assert len(beschreibung.strip()) > 0

    def test_sortierungsdropdown_sichtbar(self, eingeloggte_seite):
        """Sortierungs-Dropdown ist sichtbar"""
        produkte = ProduktSeite(eingeloggte_seite)
        assert produkte.ist_element_sichtbar(ProduktSeite.SORTIERUNG)
