
import csv
from pathlib import Path

MAX_PREIS = 40.00
MIN_GEWINN = 10.00
MAX_PRODUKTE = 100
ZIEL_BESTAND = 4

def pruefen(produkt):
    einkauf = float(produkt["einkauf"])
    verkauf = float(produkt["verkauf"])
    versand = float(produkt["versand"])

    # Vorläufige Gebührenannahme, keine verbindliche eBay-Gebühr
    gebuehren = verkauf * 0.13 + 0.35
    gewinn = round(
        verkauf - einkauf - versand - gebuehren, 2
    )

    return gewinn >= MIN_GEWINN and verkauf <= MAX_PREIS, gewinn

datei = Path("produkte.csv")

if not datei.exists():
    print("Bitte zuerst produkte.csv anlegen.")
else:
    with datei.open(encoding="utf-8-sig", newline="") as f:
        produkte = list(csv.DictReader(f))

    gefunden = 0

    for produkt in produkte:
        geeignet, gewinn = pruefen(produkt)

        if geeignet and gefunden < MAX_PRODUKTE:
            gefunden += 1
            print(
                f"{produkt['name']} | "
                f"Gewinn: {gewinn:.2f} EUR | "
                f"Zielbestand: {ZIEL_BESTAND}"
            )

    print(f"Geeignete Produkte: {gefunden}")
    print("Keine Angebote automatisch veröffentlicht.")
