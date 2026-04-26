# ============================================================
# Tests: Warenkorb
# ============================================================

import pytest
from seiten.produkt_seite    import ProduktSeite
from seiten.warenkorb_seite  import WarenkorbSeite
from seiten.navigation_seite import NavigationSeite


class TestWarenkorbAnzeige:
    """Tests für die Warenkorb-Anzeige"""

    def test_warenkorb_artikel_korrekt(self, warenkorb_mit_artikel):
        """Hinzugefügter Artikel erscheint im Warenkorb"""
        warenkorb = WarenkorbSeite(warenkorb_mit_artikel)
        warenkorb.navigiere_zu_warenkorb()
        assert "Sauce Labs Backpack" in warenkorb.hole_warenkorb_artikel()

    def test_warenkorb_leer_nach_start(self, eingeloggte_seite):
        """Warenkorb ist nach dem Login leer"""
        warenkorb = WarenkorbSeite(eingeloggte_seite)
        warenkorb.navigiere_zu_warenkorb()
        assert warenkorb.ist_warenkorb_leer()

    def test_warenkorb_anzahl_korrekt(self, warenkorb_mit_mehreren_artikeln):
        """Warenkorb zeigt korrekte Artikelanzahl"""
        warenkorb = WarenkorbSeite(warenkorb_mit_mehreren_artikeln)
        warenkorb.navigiere_zu_warenkorb()
        assert warenkorb.hole_warenkorb_anzahl() == 3

    def test_warenkorb_preise_korrekt(self, warenkorb_mit_artikel):
        """Warenkorb zeigt korrekte Preise"""
        warenkorb = WarenkorbSeite(warenkorb_mit_artikel)
        warenkorb.navigiere_zu_warenkorb()
        preise    = warenkorb.hole_warenkorb_preise()
        assert len(preise) == 1
        assert preise[0] > 0


class TestWarenkorbAktionen:
    """Tests für Warenkorb-Aktionen"""

    def test_artikel_aus_warenkorb_entfernen(self, warenkorb_mit_artikel):
        """Artikel kann aus dem Warenkorb entfernt werden"""
        warenkorb = WarenkorbSeite(warenkorb_mit_artikel)
        warenkorb.navigiere_zu_warenkorb()
        warenkorb.entferne_artikel("Sauce Labs Backpack")
        assert warenkorb.ist_warenkorb_leer()

    def test_weiter_einkaufen_button(self, warenkorb_mit_artikel):
        """'Weiter einkaufen' navigiert zurück zur Produktseite"""
        warenkorb = WarenkorbSeite(warenkorb_mit_artikel)
        warenkorb.navigiere_zu_warenkorb()
        warenkorb.klicke_weiter_einkaufen()
        assert "inventory.html" in warenkorb.hole_aktuelle_url()

    def test_zur_kasse_button(self, warenkorb_mit_artikel):
        """'Zur Kasse' navigiert zur Checkout-Seite"""
        warenkorb = WarenkorbSeite(warenkorb_mit_artikel)
        warenkorb.navigiere_zu_warenkorb()
        warenkorb.klicke_zur_kasse()
        assert "checkout-step-one.html" in warenkorb.hole_aktuelle_url()

    def test_mehrere_artikel_entfernen(self, warenkorb_mit_mehreren_artikeln):
        """Mehrere Artikel können einzeln entfernt werden"""
        warenkorb = WarenkorbSeite(warenkorb_mit_mehreren_artikeln)
        warenkorb.navigiere_zu_warenkorb()
        warenkorb.entferne_artikel("Sauce Labs Backpack")
        warenkorb.entferne_artikel("Sauce Labs Bike Light")
        assert warenkorb.hole_warenkorb_anzahl() == 1
