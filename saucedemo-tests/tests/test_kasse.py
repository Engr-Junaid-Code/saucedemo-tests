# ============================================================
# Tests: Kasse / Checkout
# ============================================================

import pytest
from seiten.kasse_seite      import KasseSeite
from seiten.warenkorb_seite  import WarenkorbSeite


class TestKasseSchritt1:
    """Tests für Checkout Schritt 1 — Lieferadresse"""

    def test_checkout_schritt1_oeffnet(self, warenkorb_mit_artikel):
        """Checkout Schritt 1 öffnet sich korrekt"""
        warenkorb = WarenkorbSeite(warenkorb_mit_artikel)
        warenkorb.navigiere_zu_warenkorb()
        warenkorb.klicke_zur_kasse()
        assert "checkout-step-one.html" in warenkorb.hole_aktuelle_url()

    def test_lieferadresse_ausfullen(self, warenkorb_mit_artikel):
        """Lieferadresse kann ausgefüllt werden"""
        warenkorb = WarenkorbSeite(warenkorb_mit_artikel)
        warenkorb.navigiere_zu_warenkorb()
        warenkorb.klicke_zur_kasse()
        kasse = KasseSeite(warenkorb_mit_artikel)
        kasse.fuelle_lieferadresse("Max", "Mustermann", "12345")
        kasse.klicke_weiter()
        assert "checkout-step-two.html" in kasse.hole_aktuelle_url()

    def test_leere_felder_fehlermeldung(self, warenkorb_mit_artikel):
        """Leere Felder zeigen Fehlermeldung"""
        warenkorb = WarenkorbSeite(warenkorb_mit_artikel)
        warenkorb.navigiere_zu_warenkorb()
        warenkorb.klicke_zur_kasse()
        kasse = KasseSeite(warenkorb_mit_artikel)
        kasse.klicke_weiter()
        assert kasse.ist_element_sichtbar(KasseSeite.FEHLER_MSG)

    def test_nur_vorname_fehlermeldung(self, warenkorb_mit_artikel):
        """Nur Vorname zeigt Fehlermeldung"""
        warenkorb = WarenkorbSeite(warenkorb_mit_artikel)
        warenkorb.navigiere_zu_warenkorb()
        warenkorb.klicke_zur_kasse()
        kasse = KasseSeite(warenkorb_mit_artikel)
        kasse.fuelle_lieferadresse("Max", "", "")
        kasse.klicke_weiter()
        assert kasse.ist_element_sichtbar(KasseSeite.FEHLER_MSG)

    def test_abbrechen_kehrt_zurueck(self, warenkorb_mit_artikel):
        """Abbrechen kehrt zum Warenkorb zurück"""
        warenkorb = WarenkorbSeite(warenkorb_mit_artikel)
        warenkorb.navigiere_zu_warenkorb()
        warenkorb.klicke_zur_kasse()
        kasse = KasseSeite(warenkorb_mit_artikel)
        kasse.klicke_abbrechen()
        assert "cart.html" in kasse.hole_aktuelle_url()


class TestKasseSchritt2:
    """Tests für Checkout Schritt 2 — Bestellübersicht"""

    def _gehe_zu_schritt2(self, page):
        """Hilfsmethode: Navigiere zu Checkout Schritt 2"""
        warenkorb = WarenkorbSeite(page)
        warenkorb.navigiere_zu_warenkorb()
        warenkorb.klicke_zur_kasse()
        kasse = KasseSeite(page)
        kasse.fuelle_lieferadresse("Max", "Mustermann", "12345")
        kasse.klicke_weiter()
        return kasse

    def test_bestelluebersicht_zeigt_artikel(self, warenkorb_mit_artikel):
        """Bestellübersicht zeigt den Artikel"""
        kasse = self._gehe_zu_schritt2(warenkorb_mit_artikel)
        artikel = kasse.hole_artikel_im_checkout()
        assert "Sauce Labs Backpack" in artikel

    def test_zwischensumme_positiv(self, warenkorb_mit_artikel):
        """Zwischensumme ist positiv"""
        kasse = self._gehe_zu_schritt2(warenkorb_mit_artikel)
        assert kasse.hole_zwischensumme() > 0

    def test_steuer_positiv(self, warenkorb_mit_artikel):
        """Steuer ist positiv"""
        kasse = self._gehe_zu_schritt2(warenkorb_mit_artikel)
        assert kasse.hole_steuer() > 0

    def test_gesamt_korrekt_berechnet(self, warenkorb_mit_artikel):
        """Gesamtbetrag = Zwischensumme + Steuer"""
        kasse        = self._gehe_zu_schritt2(warenkorb_mit_artikel)
        zwischensumme = kasse.hole_zwischensumme()
        steuer        = kasse.hole_steuer()
        gesamt        = kasse.hole_gesamtbetrag()
        assert abs(gesamt - (zwischensumme + steuer)) < 0.01


class TestKasseAbschluss:
    """Tests für den Bestellabschluss"""

    def _schliesse_bestellung_ab(self, page):
        """Hilfsmethode: Kompletter Checkout-Prozess"""
        warenkorb = WarenkorbSeite(page)
        warenkorb.navigiere_zu_warenkorb()
        warenkorb.klicke_zur_kasse()
        kasse = KasseSeite(page)
        kasse.fuelle_lieferadresse("Max", "Mustermann", "12345")
        kasse.klicke_weiter()
        kasse.klicke_beenden()
        return kasse

    def test_bestellung_erfolgreich(self, warenkorb_mit_artikel):
        """Bestellung kann erfolgreich abgeschlossen werden"""
        kasse = self._schliesse_bestellung_ab(warenkorb_mit_artikel)
        assert kasse.ist_bestellung_abgeschlossen()

    def test_bestaetigungstext_korrekt(self, warenkorb_mit_artikel):
        """Bestätigungsseite zeigt korrekten Text"""
        kasse = self._schliesse_bestellung_ab(warenkorb_mit_artikel)
        assert "Thank you" in kasse.hole_bestaetigungstext()

    def test_zurueck_zur_startseite(self, warenkorb_mit_artikel):
        """Nach Bestellung kann zur Startseite navigiert werden"""
        kasse = self._schliesse_bestellung_ab(warenkorb_mit_artikel)
        kasse.klicke_zurueck_zur_startseite()
        assert "inventory.html" in kasse.hole_aktuelle_url()
