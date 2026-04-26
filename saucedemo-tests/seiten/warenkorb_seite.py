# ============================================================
# Warenkorb-Seite — Warenkorb Funktionen
# ============================================================

from seiten.basis_seite import BasisSeite


class WarenkorbSeite(BasisSeite):

    # Selektoren
    WARENKORB_ITEMS      = ".cart_item"
    WARENKORB_ITEM_NAME  = ".inventory_item_name"
    WARENKORB_ITEM_PREIS = ".inventory_item_price"
    WARENKORB_ITEM_MENGE = ".cart_quantity"
    WEITER_EINKAUFEN     = "[data-test='continue-shopping']"
    ZUR_KASSE            = "[data-test='checkout']"
    ENTFERNEN_PREFIX     = "[data-test='remove-"

    def navigiere_zu_warenkorb(self):
        """Navigiere direkt zum Warenkorb"""
        self.navigiere_zu("cart.html")
        self.warte_auf_laden()

    def hole_warenkorb_artikel(self):
        """Hole alle Artikelnamen im Warenkorb"""
        return self.page.locator(self.WARENKORB_ITEM_NAME).all_inner_texts()

    def hole_warenkorb_anzahl(self):
        """Hole die Anzahl der Artikel im Warenkorb"""
        return self.page.locator(self.WARENKORB_ITEMS).count()

    def hole_warenkorb_preise(self):
        """Hole alle Preise im Warenkorb als Float-Liste"""
        preise_text = self.page.locator(
            self.WARENKORB_ITEM_PREIS
        ).all_inner_texts()
        return [float(p.replace("$", "")) for p in preise_text]

    def entferne_artikel(self, produktname):
        """Entferne einen Artikel aus dem Warenkorb"""
        produkt_id = produktname.lower().replace(" ", "-").replace("(", "").replace(")", "")
        selektor   = f"[data-test='remove-{produkt_id}']"
        self.warte_auf_element(selektor)
        self.klicke(selektor)

    def klicke_weiter_einkaufen(self):
        """Klicke auf 'Weiter einkaufen'"""
        self.klicke(self.WEITER_EINKAUFEN)
        self.warte_auf_url("inventory.html")

    def klicke_zur_kasse(self):
        """Klicke auf 'Zur Kasse'"""
        self.klicke(self.ZUR_KASSE)
        self.warte_auf_url("checkout-step-one.html")

    def ist_artikel_im_warenkorb(self, produktname):
        """Prüfe ob ein Artikel im Warenkorb ist"""
        artikel = self.hole_warenkorb_artikel()
        return produktname in artikel

    def ist_warenkorb_leer(self):
        """Prüfe ob der Warenkorb leer ist"""
        return self.hole_warenkorb_anzahl() == 0
