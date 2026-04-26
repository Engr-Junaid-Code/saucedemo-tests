# ============================================================
# Tests: Produkte
# ============================================================

import logging
import pytest
from seiten.produkt_seite  import ProduktSeite
from seiten.navigation_seite import NavigationSeite
from testdaten.benutzer    import PRODUKTE
from seiten.warenkorb_seite import WarenkorbSeite

# ── Logger konfigurieren ──────────────────────────────────
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class TestProduktAnzeige:
    """Tests für die Produktanzeige"""
    def test_sechs_produkte_sichtbar(self, eingeloggte_seite):
        """Dieser Test läuft mit JEDEM User!"""      
        produkte = ProduktSeite(eingeloggte_seite)
        #user = eingeloggte_seite.user_type      
        #logger.info(f"👤 Testing with: {user}")
        assert produkte.hole_produktanzahl() == 6

    def test_alle_produktnamen_vorhanden(self, eingeloggte_seite):
        """Alle erwarteten Produktnamen sind vorhanden"""
        produkte = ProduktSeite(eingeloggte_seite)
        angezeigte = produkte.hole_alle_produktnamen()
        for name in PRODUKTE:
            assert name in angezeigte, f"Produkt '{name}' fehlt!"

    def test_alle_preise_positiv(self, eingeloggte_seite):
        """Alle Produktpreise sind positiv"""
        produkte = ProduktSeite(eingeloggte_seite)
        preise   = produkte.hole_alle_preise()
        for preis in preise:
            assert preis > 0, f"Ungültiger Preis: {preis}"

    def test_seiten_titel_korrekt(self, eingeloggte_seite):
        """Seitentitel ist 'Products'"""
        produkte = ProduktSeite(eingeloggte_seite)
        assert "Products" in produkte.hole_seiten_titel()


class TestProduktSortierung:
    """Tests für die Produktsortierung"""

    def test_sortierung_a_bis_z(self, eingeloggte_seite):
        """Produkte können von A bis Z sortiert werden"""
        produkte = ProduktSeite(eingeloggte_seite)
        produkte.sortiere_nach("az")
        namen = produkte.hole_alle_produktnamen()
        assert namen == sorted(namen)

    def test_sortierung_z_bis_a(self, eingeloggte_seite):
        """Produkte können von Z bis A sortiert werden"""
        produkte = ProduktSeite(eingeloggte_seite)
        produkte.sortiere_nach("za")
        namen = produkte.hole_alle_produktnamen()
        assert namen == sorted(namen, reverse=True)

    def test_sortierung_preis_aufsteigend(self, eingeloggte_seite):
        """Produkte können nach Preis aufsteigend sortiert werden"""
        produkte = ProduktSeite(eingeloggte_seite)
        produkte.sortiere_nach("preis_asc")
        preise   = produkte.hole_alle_preise()
        assert preise == sorted(preise)

    def test_sortierung_preis_absteigend(self, eingeloggte_seite):
        """Produkte können nach Preis absteigend sortiert werden"""
        produkte = ProduktSeite(eingeloggte_seite)
        produkte.sortiere_nach("preis_desc")
        preise   = produkte.hole_alle_preise()
        assert preise == sorted(preise, reverse=True)


class TestWarenkorbAktionen:
    """Tests für Warenkorb-Aktionen auf der Produktseite"""

    def test_produkt_zum_warenkorb_hinzufuegen(self, eingeloggte_seite):
        """Ein Produkt kann zum Warenkorb hinzugefügt werden"""
        produkte = ProduktSeite(eingeloggte_seite)
        produkte.fuege_produkt_zum_warenkorb_hinzu("Sauce Labs Backpack")
        assert produkte.hole_warenkorb_anzahl() == 1

    def test_mehrere_produkte_hinzufuegen(self, eingeloggte_seite):
        """Mehrere Produkte können hinzugefügt werden"""
        produkte = ProduktSeite(eingeloggte_seite)
        produkte.fuege_produkt_zum_warenkorb_hinzu("Sauce Labs Backpack")
        produkte.fuege_produkt_zum_warenkorb_hinzu("Sauce Labs Bike Light")
        produkte.fuege_produkt_zum_warenkorb_hinzu("Sauce Labs Bolt T-Shirt")
        assert produkte.hole_warenkorb_anzahl() == 3

    def test_produkt_aus_warenkorb_entfernen(self, eingeloggte_seite):
        """Ein Produkt kann aus dem Warenkorb entfernt werden"""
        produkte = ProduktSeite(eingeloggte_seite)
        produkte.fuege_produkt_zum_warenkorb_hinzu("Sauce Labs Backpack")
        assert produkte.hole_warenkorb_anzahl() == 1
        produkte.entferne_produkt_aus_warenkorb("Sauce Labs Backpack")
        assert produkte.hole_warenkorb_anzahl() == 0

    def test_remove_button_nach_hinzufuegen(self, eingeloggte_seite):
        """Remove-Button erscheint nach Hinzufügen"""
        produkte = ProduktSeite(eingeloggte_seite)
        produkte.fuege_produkt_zum_warenkorb_hinzu("Sauce Labs Backpack")
        assert produkte.ist_remove_button_sichtbar("Sauce Labs Backpack")

    def test_alle_produkte_hinzufuegen(self, eingeloggte_seite):
        """Alle 6 Produkte können zum Warenkorb hinzugefügt werden"""
        produkte = ProduktSeite(eingeloggte_seite)
        for name in PRODUKTE:
            produkte.fuege_produkt_zum_warenkorb_hinzu(name)
        assert produkte.hole_warenkorb_anzahl() == 6
