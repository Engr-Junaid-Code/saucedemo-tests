# ============================================================
# Testdaten — Benutzer
# ============================================================

BENUTZER = {
    "standard" : {"benutzername": "standard_user",     "passwort": "secret_sauce"},
    "leistung" : {"benutzername": "performance_glitch_user", "passwort": "secret_sauce"},
    "problem"  : {"benutzername": "problem_user",       "passwort": "secret_sauce"},
    "gesperrt" : {"benutzername": "locked_out_user",    "passwort": "secret_sauce"},
    "fehler"   : {"benutzername": "error_user",         "passwort": "secret_sauce"},  # ✅ ADD THIS
    "visual"   : {"benutzername": "visual_user",        "passwort": "secret_sauce"},
}


UNGUELTIGE_BENUTZER = {
    "falsches_passwort": {
        "benutzername": "standard_user",
        "passwort":     "falsches_passwort",
    },
    "falscher_benutzer": {
        "benutzername": "kein_benutzer",
        "passwort":     "secret_sauce",
    },
    "leer": {
        "benutzername": "",
        "passwort":     "",
    },
    "nur_benutzer": {
        "benutzername": "standard_user",
        "passwort":     "",
    },
    "nur_passwort": {
        "benutzername": "",
        "passwort":     "secret_sauce",
    },
}

PRODUKTE = [
    "Sauce Labs Backpack",
    "Sauce Labs Bike Light",
    "Sauce Labs Bolt T-Shirt",
    "Sauce Labs Fleece Jacket",
    "Sauce Labs Onesie",
    "Test.allTheThings() T-Shirt (Red)",
]
