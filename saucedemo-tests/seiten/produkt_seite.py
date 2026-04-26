# ============================================================
# Produkt-Seite — Produkt & Warenkorb Funktionen
# ============================================================

from seiten.basis_seite import BasisSeite


class ProduktSeite(BasisSeite):

    # Selektoren
    PRODUKT_LISTE        = ".inventory_list"
    PRODUKT_ITEMS        = ".inventory_item"
    PRODUKT_NAME         = ".inventory_item_name"
    PRODUKT_PREIS        = ".inventory_item_price"
    PRODUKT_BESCHREIBUNG = ".inventory_item_desc"
    WARENKORB_BADGE      = ".shopping_cart_badge"
    WARENKORB_LINK       = ".shopping_cart_link"
    SORTIERUNG           = "[data-test='product-sort-container']"
    SEITEN_TITEL         = ".title"

    # Produkt-ID Mapping
    PRODUKT_IDS = {
        "Sauce Labs Backpack":              "sauce-labs-backpack",
        "Sauce Labs Bike Light":            "sauce-labs-bike-light",
        "Sauce Labs Bolt T-Shirt":          "sauce-labs-bolt-t-shirt",
        "Sauce Labs Fleece Jacket":         "sauce-labs-fleece-jacket",
        "Sauce Labs Onesie":                "sauce-labs-onesie",
        "Test.allTheThings() T-Shirt (Red)":"test.allthethings()-t-shirt-(red)",
    }

    def _produktname_zu_id(self, name):
        """Konvertiere Produktname zu Button-ID"""
        return self.PRODUKT_IDS.get(name, name.lower().replace(" ", "-"))

    def fuege_produkt_zum_warenkorb_hinzu(self, produktname):
        """Füge ein Produkt zum Warenkorb hinzu"""
        produkt_id = self._produktname_zu_id(produktname)
        selektor   = f"[data-test='add-to-cart-{produkt_id}']"
        self.warte_auf_element(selektor)
        self.klicke(selektor)

    def entferne_produkt_aus_warenkorb(self, produktname):
        """Entferne ein Produkt aus dem Warenkorb"""
        produkt_id = self._produktname_zu_id(produktname)
        selektor   = f"[data-test='remove-{produkt_id}']"
        self.warte_auf_element(selektor)
        self.klicke(selektor)

    def hole_warenkorb_anzahl(self):
        """Hole die Anzahl der Artikel im Warenkorb"""
        if not self.ist_element_sichtbar(self.WARENKORB_BADGE):
            return 0
        return int(self.hole_text(self.WARENKORB_BADGE))

    def hole_alle_produktnamen(self):
        """Hole alle Produktnamen von der Seite"""
        self.warte_auf_element(self.PRODUKT_LISTE)
        return self.page.locator(self.PRODUKT_NAME).all_inner_texts()

    def hole_alle_preise(self):
        """Hole alle Produktpreise als Float-Liste"""
        self.warte_auf_element(self.PRODUKT_LISTE)
        preise_text = self.page.locator(self.PRODUKT_PREIS).all_inner_texts()
        return [float(p.replace("$", "")) for p in preise_text]

    def hole_produktanzahl(self):
        """Hole die Anzahl der angezeigten Produkte"""
        self.warte_auf_element(self.PRODUKT_LISTE)
        return self.page.locator(self.PRODUKT_ITEMS).count()

    def sortiere_nach(self, option):
        """
        Sortiere Produkte:
        az, za, preis_asc, preis_desc
        """
        optionen = {
            "az":         "az",
            "za":         "za",
            "preis_asc":  "lohi",
            "preis_desc": "hilo",
        }
        self.page.locator(self.SORTIERUNG).select_option(optionen[option])

    def oeffne_produkt_detail(self, produktname):
        """Öffne die Detailseite eines Produkts"""
        self.page.locator(self.PRODUKT_NAME).filter(
            has_text=produktname
        ).click()
        self.warte_auf_laden()

    def ist_remove_button_sichtbar(self, produktname):
        """Prüfe ob Remove-Button für ein Produkt sichtbar ist"""
        produkt_id = self._produktname_zu_id(produktname)
        selektor   = f"[data-test='remove-{produkt_id}']"
        return self.ist_element_sichtbar(selektor)

    def hole_seiten_titel(self):
        """Hole den Titel der aktuellen Seite"""
        return self.hole_text(self.SEITEN_TITEL)
