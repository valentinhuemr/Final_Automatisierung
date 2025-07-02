from tinydb import TinyDB
import csv

# Daten auslesen
db = TinyDB("daten.json")
table = db.table("messungen")
daten = table.all()

# CSV-Datei schreiben
with open("export.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=daten[0].keys())
    writer.writeheader()
    writer.writerows(daten)

print("✅ export.csv wurde erstellt.")
