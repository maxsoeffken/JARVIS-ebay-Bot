
import csv
from pathlib import Path

MAX_PREIS = 40.00
MIN_GEWINN = 10.00
MAX_PRODUKTE = 100
ZIEL_BESTAND = 4

# Vorläufige Gebührenannahme
GEBUEHREN_PROZENT = 0.13
GEBUEHREN_FIX = 0.35


def pruefen(produkt):
    einkauf = float(produkt["einkauf"])
    verkauf = float(produkt["verkauf"])
    versand = float(produkt["versand"])

    gebuehren = (
        verkauf * GEBUEHREN_PROZENT
        + GEBUEHREN_FIX
    )

    gewinn = round(
        verkauf - einkauf - versand - gebuehren,
        2
    )

    geeignet = (
        verkauf <= MAX_PREIS
        and gewinn >= MIN_GEWINN
    )

    return geeignet, gewinn


def main():
    print("JARVIS gestartet")

    datei = Path("produkte.csv")

    if not datei.exists():
        print("FEHLER: produkte.csv fehlt.")
        return

    with datei.open(
        encoding="utf-8-sig",
        newline=""
    ) as f:
        zeilen = [
            zeile for zeile in f
            if zeile.strip()
        ]

    if not zeilen:
        print("FEHLER: Produktliste ist leer.")
        return

    reader = csv.DictReader(
        zeilen,
        skipinitialspace=True
    )

    spalten = [
        name.strip()
        for name in (reader.fieldnames or [])
    ]

    print("Erkannte Spalten:", spalten)

    benoetigt = {
        "name", "einkauf", "verkauf", "versand"
    }

    if not benoetigt.issubset(set(spalten)):
        print("FEHLER: Spalten fehlen.")
        print("Erwartet:", sorted(benoetigt))
        return

    gefunden = 0

    for nummer, produkt in enumerate(reader, 2):
        produkt = {
            str(k).strip(): v.strip()
            for k, v in produkt.items()
            if k is not None and v is not None
        }

        try:
            geeignet, gewinn = pruefen(produkt)
        except (ValueError, KeyError) as fehler:
            print(
                f"Zeile {nummer} übersprungen:",
                fehler
            )
            continue

        if geeignet:
            gefunden += 1

            print(
                f"{gefunden}. {produkt['name']}"
            )
            print(
                f"Verkauf: {produkt['verkauf']} EUR"
            )
            print(
                f"Gewinn: {gewinn:.2f} EUR"
            )
            print(
                f"Zielmenge: {ZIEL_BESTAND}"
            )

        if gefunden >= MAX_PRODUKTE:
            break

    print("Geeignete Produkte:", gefunden)
    print("Keine eBay-Angebote veröffentlicht.")


if __name__ == "__main__":
    main()
