
import csv
from pathlib import Path
from decimal import Decimal, InvalidOperation

MAX_PREIS = Decimal("40.00")
MIN_GEWINN = Decimal("10.00")
MAX_PRODUKTE = 100
ZIELMENGE = 4

# Geschätzte Gebühren, später durch echte Werte ersetzen
GEBUEHREN_SATZ = Decimal("0.13")
GEBUEHREN_FIX = Decimal("0.35")

QUELLE = Path("produkte.csv")
AUSGABE = Path("kandidaten.csv")


def geld(wert):
    return Decimal(str(wert).strip().replace(",", "."))


def main():
    print("JARVIS gestartet")

    if not QUELLE.exists():
        print("Fehler: produkte.csv fehlt.")
        return

    with QUELLE.open(
        encoding="utf-8-sig",
        newline=""
    ) as datei:
        zeilen = [
            zeile for zeile in datei
            if zeile.strip()
        ]

    if not zeilen:
        print("Keine Produkte vorhanden.")
        return

    reader = csv.DictReader(
        zeilen,
        skipinitialspace=True
    )

    benoetigt = {
        "name", "einkauf", "verkauf",
        "versand", "amazon_link"
    }

    spalten = {
        name.strip()
        for name in (reader.fieldnames or [])
    }

    if not benoetigt.issubset(spalten):
        print("Fehlende Spalten:", benoetigt - spalten)
        return

    kandidaten = []

    for produkt in reader:
        try:
            name = produkt["name"].strip()
            einkauf = geld(produkt["einkauf"])
            verkauf = geld(produkt["verkauf"])
            versand = geld(produkt["versand"])
            link = produkt["amazon_link"].strip()

            if not name or min(
                einkauf, verkauf, versand
            ) < 0:
                continue

            gebuehren = (
                verkauf * GEBUEHREN_SATZ
                + GEBUEHREN_FIX
            )

            gewinn = (
                verkauf - einkauf
                - versand - gebuehren
            ).quantize(Decimal("0.01"))

            if (
                verkauf <= MAX_PREIS
                and gewinn >= MIN_GEWINN
            ):
                kandidaten.append({
                    "name": name,
                    "einkauf": str(einkauf),
                    "verkauf": str(verkauf),
                    "versand": str(versand),
                    "gewinn": str(gewinn),
                    "amazon_link": link,
                    "zielmenge": ZIELMENGE,
                    "status": "Pruefung erforderlich"
                })

            if len(kandidaten) >= MAX_PRODUKTE:
                break

        except (
            ValueError, InvalidOperation,
            KeyError, AttributeError
        ) as fehler:
            print("Produkt übersprungen:", fehler)

    felder = [
        "name", "einkauf", "verkauf",
        "versand", "gewinn", "amazon_link",
        "zielmenge", "status"
    ]

    with AUSGABE.open(
        "w", encoding="utf-8", newline=""
    ) as datei:
        writer = csv.DictWriter(
            datei, fieldnames=felder
        )
        writer.writeheader()
        writer.writerows(kandidaten)

    print("Geeignete Kandidaten:", len(kandidaten))
    for produkt in kandidaten:
        print(
            produkt["name"],
            "| Gewinn:", produkt["gewinn"],
            "EUR | Amazon:", produkt["amazon_link"] or "kein Link"
        )

    print("Datei erstellt:", AUSGABE)
    print("Noch keine eBay-Angebote veröffentlicht.")


if __name__ == "__main__":
    main()
