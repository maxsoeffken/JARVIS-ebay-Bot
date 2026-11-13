
import csv
from pathlib import Path
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation

MAX_PREIS = Decimal("40.00")
MIN_GEWINN = Decimal("10.00")
MAX_PRODUKTE = 100
MIN_STUECKZAHL = 4
MAX_ALTER_STUNDEN = 6

# Nur geschätzte Gebühren
GEBUEHREN = Decimal("0.13")
FIXGEBUEHR = Decimal("0.35")

QUELLE = Path("produkte.csv")
AUSGABE = Path("kandidaten.csv")

FELDER = [
    "name", "einkauf", "verkauf", "versand",
    "amazon_link", "prime_lieferdatum",
    "stueckzahl", "geprueft_am"
]


def geld(wert):
    return Decimal(str(wert).strip().replace(",", "."))


def main():
    print("JARVIS Prime-Prüfung gestartet")

    if not QUELLE.exists():
        print("FEHLER: produkte.csv fehlt")
        return

    with QUELLE.open(encoding="utf-8-sig", newline="") as f:
        zeilen = [z for z in f if z.strip()]

    if not zeilen:
        print("Keine Produktdaten vorhanden")
        return

    reader = csv.DictReader(zeilen, skipinitialspace=True)
    spalten = [s.strip() for s in (reader.fieldnames or [])]

    if not set(FELDER).issubset(spalten):
        print("FEHLER: Fehlende Spalten")
        print(set(FELDER) - set(spalten))
        return

    jetzt = datetime.now().astimezone()
    morgen = jetzt.date() + timedelta(days=1)
    kandidaten = []

    for zeile in reader:
        try:
            p = {
                str(k).strip(): (v or "").strip()
                for k, v in zeile.items()
                if k is not None
            }

            if not p["amazon_link"].startswith(
                ("https://www.amazon.de/", "https://amazon.de/")
            ):
                continue

            lieferdatum = datetime.strptime(
                p["prime_lieferdatum"], "%Y-%m-%d"
            ).date()

            pruefzeit = datetime.fromisoformat(
                p["geprueft_am"]
            )

            if pruefzeit.tzinfo is None:
                print("Prüfzeit ohne Zeitzone übersprungen")
                continue

            alter = jetzt - pruefzeit

            if not (
                timedelta(0) <= alter <= timedelta(hours=MAX_ALTER_STUNDEN)
                and jetzt.date() <= lieferdatum <= morgen
                and int(p["stueckzahl"]) >= MIN_STUECKZAHL
            ):
                continue

            einkauf = geld(p["einkauf"])
            verkauf = geld(p["verkauf"])
            versand = geld(p["versand"])

            if min(einkauf, verkauf, versand) < 0:
                continue

            gewinn = (
                verkauf - einkauf - versand
                - verkauf * GEBUEHREN - FIXGEBUEHR
            ).quantize(Decimal("0.01"))

            if verkauf <= MAX_PREIS and gewinn >= MIN_GEWINN:
                kandidaten.append({
                    **p,
                    "gewinn": str(gewinn),
                    "status": "Manuelle Freigabe erforderlich"
                })

            if len(kandidaten) >= MAX_PRODUKTE:
                break

        except (
            ValueError, KeyError, InvalidOperation,
            OverflowError
        ) as fehler:
            print("Produkt übersprungen:", fehler)

    with AUSGABE.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=FELDER + ["gewinn", "status"]
        )
        writer.writeheader()
        writer.writerows(kandidaten)

    print("Geeignete Kandidaten:", len(kandidaten))
    print("Ergebnisdatei:", AUSGABE)
    print("Keine eBay-Angebote veröffentlicht.")


if __name__ == "__main__":
    main()
