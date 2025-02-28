import os
import pickle
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Produkt-Klasse
class Produkt:
    def __init__(self, name, preis):
        self.name = name
        self.preis = preis

# Rechnung-Klasse
class Rechnung:
    def __init__(self):
        self.produkte = []
        self.gesamtpreis = 0.0

    def hinzufuegen(self, produkt):
        self.produkte.append(produkt)
        self.gesamtpreis += produkt.preis

    def anzeigen(self):
        print("Rechnung:")
        for produkt in self.produkte:
            print(f"{produkt.name}: {produkt.preis} €")
        print(f"Gesamtpreis: {self.gesamtpreis} €")

    def als_pdf_speichern(self, dateiname="rechnung.pdf"):
        c = canvas.Canvas(dateiname, pagesize=letter)
        c.setFont("Helvetica", 12)
        c.drawString(100, 750, "Rechnung:")

        y_position = 730
        for produkt in self.produkte:
            c.drawString(100, y_position, f"{produkt.name}: {produkt.preis} €")
            y_position -= 20

        c.drawString(100, y_position - 20, f"Gesamtpreis: {self.gesamtpreis} €")
        c.save()
        print(f"Die Rechnung wurde als PDF unter '{dateiname}' gespeichert.")

# Benutzer-Klasse für Registrierung und Login
class Benutzer:
    def __init__(self, benutzername, passwort):
        self.benutzername = benutzername
        self.passwort = passwort
        self.rechnungen = []

    def add_rechnung(self, rechnung):
        self.rechnungen.append(rechnung)

# Benutzer-Daten speichern
def speichere_benutzer(benutzer):
    if not os.path.exists('benutzer_data'):
        os.makedirs('benutzer_data')
    
    with open(f'benutzer_data/{benutzer.benutzername}.pkl', 'wb') as file:
        pickle.dump(benutzer, file)

# Benutzer aus Datei laden
def lade_benutzer(benutzername):
    try:
        with open(f'benutzer_data/{benutzername}.pkl', 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return None

# Benutzer registrieren
def registrieren():
    benutzername = input("Benutzername: ")
    passwort = input("Passwort: ")
    benutzer = Benutzer(benutzername, passwort)
    speichere_benutzer(benutzer)
    print(f"Benutzer {benutzername} erfolgreich registriert!")

# Benutzer anmelden
def anmelden():
    benutzername = input("Benutzername: ")
    passwort = input("Passwort: ")
    benutzer = lade_benutzer(benutzername)

    if benutzer and benutzer.passwort == passwort:
        print(f"Willkommen {benutzername}!")
        return benutzer
    else:
        print("Ungültiger Benutzername oder Passwort.")
        return None

# Produkt hinzufügen
def produkt_hinzufuegen():
    name = input("Gib den Produktnamen ein: ")
    preis = float(input("Gib den Preis des Produkts ein: "))
    return Produkt(name, preis)

# Hauptfunktion des Rechnungsystems
def rechnungssystem():
    print("Willkommen im Rechnungsystem!")
    print("1. Registrieren")
    print("2. Anmelden")
    
    auswahl = input("Wähle eine Option (1 oder 2): ")

    if auswahl == '1':
        registrieren()
        return anmelden()  # nach der Registrierung automatisch anmelden
    elif auswahl == '2':
        return anmelden()

    print("Ungültige Auswahl.")
    return None

def benutzer_rechnungen_verwalten(benutzer):
    while True:
        print("\nWähle eine Option:")
        print("1. Produkt zur Rechnung hinzufügen")
        print("2. Rechnung anzeigen")
        print("3. Rechnung als PDF speichern")
        print("4. Neue Rechnung starten")
        print("5. Abmelden")

        wahl = input("Gib die Zahl der gewählten Option ein: ")

        if wahl == '1':
            produkt = produkt_hinzufuegen()
            if not benutzer.rechnungen:
                benutzer.rechnungen.append(Rechnung())  # Falls keine Rechnung existiert, wird eine neue erstellt
            benutzer.rechnungen[-1].hinzufuegen(produkt)  # Produkt zur letzten Rechnung hinzufügen
        elif wahl == '2':
            if benutzer.rechnungen:
                benutzer.rechnungen[-1].anzeigen()
            else:
                print("Keine Rechnungen vorhanden.")
        elif wahl == '3':
            if benutzer.rechnungen:
                dateiname = input("Gib den Dateinamen für das PDF ein (z.B. 'rechnung.pdf'): ")
                benutzer.rechnungen[-1].als_pdf_speichern(dateiname)
            else:
                print("Keine Rechnungen vorhanden.")
        elif wahl == '4':
            benutzer.rechnungen.append(Rechnung())  # Neue Rechnung starten
            print("Neue Rechnung wurde gestartet.")
        elif wahl == '5':
            print("Abmelden...")
            break
        else:
            print("Ungültige Auswahl.")

if __name__ == "__main__":
    benutzer = rechnungssystem()

    if benutzer:
        benutzer_rechnungen_verwalten(benutzer)
