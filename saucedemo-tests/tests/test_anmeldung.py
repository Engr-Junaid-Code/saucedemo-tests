# ============================================================
# Tests: Anmeldung
# ============================================================

import pytest
from seiten.anmelde_seite import AnmeldeSeite
from testdaten.benutzer   import BENUTZER, UNGUELTIGE_BENUTZER


class TestErfolgreicheAnmeldung:
    """Tests für erfolgreiche Anmeldungen"""

    def test_standard_benutzer_login(self, anmelde_seite):
        """Standard-Benutzer kann sich einloggen"""
        anmelde_seite.anmelden_und_warten(
            BENUTZER["standard"]["benutzername"],
            BENUTZER["standard"]["passwort"],
        )
        assert "inventory.html" in anmelde_seite.hole_aktuelle_url()

    def test_leistung_benutzer_login(self, anmelde_seite):
        """Leistungs-Benutzer kann sich einloggen (mit erhöhtem Timeout)"""
        anmelde_seite.anmelden_und_warten(
            BENUTZER["leistung"]["benutzername"],
            BENUTZER["leistung"]["passwort"],
            timeout=15000,
        )
        assert "inventory.html" in anmelde_seite.hole_aktuelle_url()

    def test_problem_benutzer_login(self, anmelde_seite):
        """Problem-Benutzer kann sich einloggen"""
        anmelde_seite.anmelden_und_warten(
            BENUTZER["problem"]["benutzername"],
            BENUTZER["problem"]["passwort"],
        )
        assert "inventory.html" in anmelde_seite.hole_aktuelle_url()

    def test_visual_benutzer_login(self, anmelde_seite):
        """Visual-Benutzer kann sich einloggen"""
        anmelde_seite.anmelden_und_warten(
            BENUTZER["visual"]["benutzername"],
            BENUTZER["visual"]["passwort"],
        )
        assert "inventory.html" in anmelde_seite.hole_aktuelle_url()

    def test_login_seite_titel(self, anmelde_seite):
        """Login-Seite zeigt korrekten Titel"""
        assert anmelde_seite.ist_auf_anmeldeseite()

    def test_login_button_sichtbar(self, anmelde_seite):
        """Login-Button ist sichtbar"""
        assert anmelde_seite.ist_element_sichtbar(
            AnmeldeSeite.LOGIN_BUTTON
        )

    def test_benutzername_feld_sichtbar(self, anmelde_seite):
        """Benutzername-Feld ist sichtbar"""
        assert anmelde_seite.ist_element_sichtbar(
            AnmeldeSeite.BENUTZERNAME_FELD
        )

    def test_passwort_feld_sichtbar(self, anmelde_seite):
        """Passwort-Feld ist sichtbar"""
        assert anmelde_seite.ist_element_sichtbar(
            AnmeldeSeite.PASSWORT_FELD
        )


class TestFehlgeschlageneAnmeldung:
    """Tests für fehlgeschlagene Anmeldungen"""

    def test_gesperrter_benutzer_login(self, anmelde_seite):
        """Gesperrter Benutzer kann sich NICHT einloggen"""
        anmelde_seite.anmelden(
            BENUTZER["gesperrt"]["benutzername"],
            BENUTZER["gesperrt"]["passwort"],
        )
        assert anmelde_seite.ist_fehlermeldung_sichtbar()
        assert "locked out" in anmelde_seite.hole_fehlermeldung().lower()

    def test_falsches_passwort(self, anmelde_seite):
        """Falsches Passwort zeigt Fehlermeldung"""
        anmelde_seite.anmelden(
            UNGUELTIGE_BENUTZER["falsches_passwort"]["benutzername"],
            UNGUELTIGE_BENUTZER["falsches_passwort"]["passwort"],
        )
        assert anmelde_seite.ist_fehlermeldung_sichtbar()

    def test_falscher_benutzer(self, anmelde_seite):
        """Unbekannter Benutzername zeigt Fehlermeldung"""
        anmelde_seite.anmelden(
            UNGUELTIGE_BENUTZER["falscher_benutzer"]["benutzername"],
            UNGUELTIGE_BENUTZER["falscher_benutzer"]["passwort"],
        )
        assert anmelde_seite.ist_fehlermeldung_sichtbar()

    def test_leere_felder(self, anmelde_seite):
        """Leere Felder zeigen Fehlermeldung"""
        anmelde_seite.anmelden(
            UNGUELTIGE_BENUTZER["leer"]["benutzername"],
            UNGUELTIGE_BENUTZER["leer"]["passwort"],
        )
        assert anmelde_seite.ist_fehlermeldung_sichtbar()

    def test_nur_benutzername(self, anmelde_seite):
        """Nur Benutzername ohne Passwort zeigt Fehlermeldung"""
        anmelde_seite.anmelden(
            UNGUELTIGE_BENUTZER["nur_benutzer"]["benutzername"],
            UNGUELTIGE_BENUTZER["nur_benutzer"]["passwort"],
        )
        assert anmelde_seite.ist_fehlermeldung_sichtbar()

    def test_nur_passwort(self, anmelde_seite):
        """Nur Passwort ohne Benutzername zeigt Fehlermeldung"""
        anmelde_seite.anmelden(
            UNGUELTIGE_BENUTZER["nur_passwort"]["benutzername"],
            UNGUELTIGE_BENUTZER["nur_passwort"]["passwort"],
        )
        assert anmelde_seite.ist_fehlermeldung_sichtbar()

    def test_fehlermeldung_schliessen(self, anmelde_seite):
        """Fehlermeldung kann geschlossen werden"""
        anmelde_seite.anmelden(
            UNGUELTIGE_BENUTZER["leer"]["benutzername"],
            UNGUELTIGE_BENUTZER["leer"]["passwort"],
        )
        assert anmelde_seite.ist_fehlermeldung_sichtbar()
        anmelde_seite.schliesse_fehlermeldung()
        assert not anmelde_seite.ist_fehlermeldung_sichtbar()
