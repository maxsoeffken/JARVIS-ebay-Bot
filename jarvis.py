
from datetime import datetime, timezone

MAX_VERKAUFSPREIS = 40.00
MIN_GEWINN = 10.00
MAX_PRODUKTE_PRO_TAG = 100

def gewinn_berechnen(einkauf, verkauf, versand=0):
    gebuehren = verkauf * 0.13 + 0.35
    return round(verkauf - einkauf - versand - gebuehren, 2)

def produkt_pruefen(einkauf, verkauf, versand=0):
    gewinn = gewinn_berechnen(einkauf, verkauf, versand)
    return verkauf <= MAX_VERKAUFSPREIS and gewinn >= MIN_GEWINN

print("JARVIS gestartet")
print("Zeit:", datetime.now(timezone.utc).isoformat())
print("Maximaler Verkaufspreis:", MAX_VERKAUFSPREIS, "EUR")
print("Mindestgewinn:", MIN_GEWINN, "EUR")
print("Produktlimit:", MAX_PRODUKTE_PRO_TAG)

print("Test:", produkt_pruefen(15, 30))
print("Automatische Produktsuche noch nicht verbunden.")
