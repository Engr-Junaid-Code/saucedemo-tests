# ============================================================
# Navigation-Seite — Menü & Navigation Funktionen
# ============================================================

from seiten.basis_seite import BasisSeite


class NavigationSeite(BasisSeite):

    # Selektoren
    BURGER_MENU      = "#react-burger-menu-btn"
    MENU_SCHLIESSEN  = "#react-burger-cross-btn"
    ALLE_ARTIKEL     = "#inventory_sidebar_link"
    UEBER            = "#about_sidebar_link"
    ABMELDEN_LINK    = "#logout_sidebar_link"
    ZURUECKSETZEN    = "#reset_sidebar_link"
    WARENKORB_LINK   = ".shopping_cart_link"
    WARENKORB_BADGE  = ".shopping_cart_badge"

    def oeffne_menu(self):
        """Öffne das Burger-Menü"""
        self.klicke(self.BURGER_MENU)
        self.warte_auf_element(self.ABMELDEN_LINK)

    def schliesse_menu(self):
        """Schließe das Burger-Menü"""
        self.klicke(self.MENU_SCHLIESSEN)

    def abmelden(self):
        """Abmelden über das Menü"""
        self.oeffne_menu()
        self.klicke(self.ABMELDEN_LINK)
        # Saucedemo leitet nach Logout zu "/" weiter, nicht zu "index.html"
        self.page.wait_for_load_state("domcontentloaded", timeout=10000)
        assert "inventory" not in self.page.url

    def gehe_zu_alle_artikel(self):
        """Gehe zur Produktliste"""
        self.oeffne_menu()
        self.klicke(self.ALLE_ARTIKEL)
        self.warte_auf_url("inventory.html")

    def setze_app_zurueck(self):
        """Setze App-Status zurück (Reset)"""
        self.oeffne_menu()
        self.klicke(self.ZURUECKSETZEN)
        self.schliesse_menu()

    def gehe_zu_warenkorb(self):
        """Navigiere zum Warenkorb"""
        self.klicke(self.WARENKORB_LINK)
        self.warte_auf_url("cart.html")

    def hole_warenkorb_anzahl(self):
        """Hole Warenkorb-Anzahl aus der Navigationsleiste"""
        if not self.ist_element_sichtbar(self.WARENKORB_BADGE):
            return 0
        return int(self.hole_text(self.WARENKORB_BADGE))

    def ist_menu_offen(self):
        """Prüfe ob das Menü geöffnet ist"""
        return self.ist_element_sichtbar(self.ABMELDEN_LINK)
