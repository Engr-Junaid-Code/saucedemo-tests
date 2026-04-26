# ============================================================
# Basis-Seite — Gemeinsame Methoden für alle Seiten
# ============================================================

class BasisSeite:
    BASIS_URL = "https://www.saucedemo.com"

    def __init__(self, page):
        self.page = page

    def navigiere_zu(self, pfad=""):
        """Navigiere zu einer URL"""
        self.page.goto(f"{self.BASIS_URL}/{pfad}")

    def hole_aktuelle_url(self):
        """Gibt die aktuelle URL zurück"""
        return self.page.url

    def warte_auf_element(self, selektor, timeout=10000):
        """Warte bis ein Element sichtbar ist"""
        self.page.wait_for_selector(selektor, state="visible", timeout=timeout)

    def ist_element_sichtbar(self, selektor):
        """Prüfe ob ein Element sichtbar ist"""
        return self.page.locator(selektor).is_visible()

    def hole_text(self, selektor):
        """Hole den Textinhalt eines Elements"""
        return self.page.locator(selektor).inner_text()

    def klicke(self, selektor, timeout=10000):
        """Warte bis Element sichtbar ist, dann klicken"""
        locator = self.page.locator(selektor)
        locator.wait_for(state="visible", timeout=timeout)
        locator.scroll_into_view_if_needed()
        locator.click()

    def fuelle_feld(self, selektor, wert):
        """Fülle ein Eingabefeld"""
        locator = self.page.locator(selektor)
        locator.wait_for(state="visible", timeout=10000)
        locator.fill(wert)

    def warte_auf_url(self, url_teil, timeout=10000):
        """Warte bis URL einen bestimmten Teil enthält"""
        self.page.wait_for_url(f"**{url_teil}**", timeout=timeout)

    def warte_auf_laden(self):
        """Warte bis Seite vollständig geladen ist"""
        self.page.wait_for_load_state("domcontentloaded")
