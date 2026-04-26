# ============================================================
# Kasse-Seite — Checkout Funktionen
# ============================================================

from seiten.basis_seite import BasisSeite


class KasseSeite(BasisSeite):

    # Selektoren Schritt 1
    VORNAME_FELD    = "[data-test='firstName']"
    NACHNAME_FELD   = "[data-test='lastName']"
    PLZ_FELD        = "[data-test='postalCode']"
    WEITER_BUTTON   = "[data-test='continue']"
    ABBRECHEN_BTN   = "[data-test='cancel']"
    FEHLER_MSG      = "[data-test='error']"

    # Selektoren Schritt 2
    ARTIKEL_LISTE   = ".cart_item"
    ARTIKEL_NAME    = ".inventory_item_name"
    ARTIKEL_PREIS   = ".inventory_item_price"
    ZWISCHENSUMME   = ".summary_subtotal_label"
    STEUER          = ".summary_tax_label"
    GESAMT          = ".summary_total_label"
    BEENDEN_BTN     = "[data-test='finish']"
    ZURUECK_BTN     = "[data-test='back']"

    # Selektoren Bestätigung
    BESTAETIGUNG    = ".complete-header"
    BESTAETIGUNG_TX = ".complete-text"
    ZURUECK_HOME    = "[data-test='back-to-products']"

    def fuelle_lieferadresse(self, vorname, nachname, plz):
        """Fülle das Lieferadressformular aus"""
        self.fuelle_feld(self.VORNAME_FELD, vorname)
        self.fuelle_feld(self.NACHNAME_FELD, nachname)
        self.fuelle_feld(self.PLZ_FELD, plz)

    def klicke_weiter(self):
        """Klicke auf Weiter in Schritt 1"""
        self.klicke(self.WEITER_BUTTON)

    def klicke_beenden(self):
        """Klicke auf Bestellung abschließen"""
        self.klicke(self.BEENDEN_BTN)
        self.warte_auf_url("checkout-complete.html")

    def klicke_abbrechen(self):
        """Klicke auf Abbrechen"""
        self.klicke(self.ABBRECHEN_BTN)

    def klicke_zurueck_zur_startseite(self):
        """Klicke auf Zurück zur Startseite"""
        self.klicke(self.ZURUECK_HOME)
        self.warte_auf_url("inventory.html")

    def hole_fehlermeldung(self):
        """Hole Fehlermeldung in Schritt 1"""
        self.warte_auf_element(self.FEHLER_MSG)
        return self.hole_text(self.FEHLER_MSG)

    def hole_zwischensumme(self):
        """Hole Zwischensumme als Float"""
        text = self.hole_text(self.ZWISCHENSUMME)
        return float(text.split("$")[1])

    def hole_steuer(self):
        """Hole Steuer als Float"""
        text = self.hole_text(self.STEUER)
        return float(text.split("$")[1])

    def hole_gesamtbetrag(self):
        """Hole Gesamtbetrag als Float"""
        text = self.hole_text(self.GESAMT)
        return float(text.split("$")[1])

    def hole_bestaetigungstext(self):
        """Hole den Bestätigungstext"""
        self.warte_auf_element(self.BESTAETIGUNG)
        return self.hole_text(self.BESTAETIGUNG)

    def ist_bestellung_abgeschlossen(self):
        """Prüfe ob die Bestellung erfolgreich abgeschlossen wurde"""
        return self.ist_element_sichtbar(self.BESTAETIGUNG)

    def hole_artikel_im_checkout(self):
        """Hole alle Artikelnamen in der Bestellübersicht"""
        return self.page.locator(self.ARTIKEL_NAME).all_inner_texts()
