# ============================================================
# Anmelde-Seite — Login Funktionen
# ============================================================

from seiten.basis_seite import BasisSeite


class AnmeldeSeite(BasisSeite):

    # Selektoren
    BENUTZERNAME_FELD  = "[data-test='username']"
    PASSWORT_FELD      = "[data-test='password']"
    LOGIN_BUTTON       = "[data-test='login-button']"
    FEHLER_NACHRICHT   = "[data-test='error']"
    FEHLER_SCHLIESSEN  = ".error-button"

    def navigiere_zu_anmeldung(self):
        """Öffne die Login-Seite"""
        self.navigiere_zu()
        self.warte_auf_laden()

    def anmelden(self, benutzername, passwort):
        """Logge einen Benutzer ein"""
        self.fuelle_feld(self.BENUTZERNAME_FELD, benutzername)
        self.fuelle_feld(self.PASSWORT_FELD, passwort)
        self.klicke(self.LOGIN_BUTTON)

    def anmelden_und_warten(self, benutzername, passwort, timeout=10000):
        """Anmelden und auf Weiterleitung warten"""
        self.anmelden(benutzername, passwort)
        self.page.wait_for_url("**/inventory.html", timeout=timeout)

    def hole_fehlermeldung(self):
        """Hole den Text der Fehlermeldung"""
        self.warte_auf_element(self.FEHLER_NACHRICHT)
        return self.hole_text(self.FEHLER_NACHRICHT)

    def ist_fehlermeldung_sichtbar(self):
        """Prüfe ob eine Fehlermeldung angezeigt wird"""
        return self.ist_element_sichtbar(self.FEHLER_NACHRICHT)

    def schliesse_fehlermeldung(self):
        """Schließe die Fehlermeldung"""
        self.klicke(self.FEHLER_SCHLIESSEN)

    def ist_auf_anmeldeseite(self):
        """Prüfe ob der Benutzer auf der Login-Seite ist"""
        return (
            "saucedemo.com" in self.hole_aktuelle_url()
            and "inventory" not in self.hole_aktuelle_url()
        )

    def hole_benutzername_wert(self):
        """Hole den aktuellen Wert im Benutzernamefeld"""
        return self.page.locator(self.BENUTZERNAME_FELD).input_value()

    def hole_passwort_wert(self):
        """Hole den aktuellen Wert im Passwortfeld"""
        return self.page.locator(self.PASSWORT_FELD).input_value()
