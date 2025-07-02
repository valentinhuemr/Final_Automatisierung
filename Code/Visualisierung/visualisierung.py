from tinydb import TinyDB
import matplotlib.pyplot as plt
from datetime import datetime

# Datenbank laden
db = TinyDB("daten.json")
table = db.table("messungen")
daten = table.all()

# Daten extrahieren
timestamps = []
temperaturen = []

for eintrag in daten:
    try:
        # Zeit in datetime-Objekt umwandeln
        zeit = datetime.fromisoformat(eintrag["timestamp"])
        temp = float(eintrag["temperature_C_red"])
        timestamps.append(zeit)
        temperaturen.append(temp)
    except Exception as e:
        print("Überspringe fehlerhaften Eintrag:", e)

# Plot erstellen
plt.figure(figsize=(10, 5))
plt.plot(timestamps, temperaturen, marker='o', linestyle='-')
plt.title("Temperaturverlauf (red dispenser)")
plt.xlabel("Zeit")
plt.ylabel("Temperatur (°C)")
plt.grid(True)
plt.tight_layout()
plt.xticks(rotation=45)
plt.show()
