import paho.mqtt.client as mqtt
import json
from tinydb import TinyDB
from datetime import datetime

# MQTT-Einstellungen
broker = "158.180.44.197"
port = 1883
username = "bobm"
password = "letmein"
topic_base = "iot1/teaching_factory/#"

# TinyDB vorbereiten
db = TinyDB("daten.json")
table = db.table("messungen")

# Zwischenspeicher für aktuelle Werte
latest_red = None
latest_temp = None

def try_save_entry():
    """Speichert Eintrag nur, wenn beide Daten vorhanden sind."""
    global latest_red, latest_temp

    if latest_red and latest_temp:
        eintrag = {
            "timestamp": datetime.utcnow().isoformat(),
            "bottle": latest_red.get("bottle"),
            "vibration_index_red": latest_red.get("vibration-index"),
            "time_red": latest_red.get("time"),
            "fill_level_grams_red": latest_red.get("fill_level_grams"),
            "recipe": latest_red.get("recipe"),
            "temperature_C_red": latest_temp.get("temperature_C"),
            "final_weight_grams": latest_red.get("fill_level_grams")  # Beispielannahme
        }

        print("✅ Eintrag gespeichert:", eintrag)
        table.insert(eintrag)

        # Nach dem Speichern zurücksetzen
        latest_red = None
        latest_temp = None

# Callback bei Empfang einer Nachricht
def on_message(client, userdata, msg):
    global latest_red, latest_temp

    print("📨 Nachricht empfangen:")
    print("📍 Topic:", msg.topic)
    try:
        payload = json.loads(msg.payload.decode())

        if "dispenser_red" in msg.topic:
            latest_red = payload
            print("🔴 Dispenser-Red aktualisiert.")
        elif "temperature" in msg.topic:
            latest_temp = payload
            print("🌡️ Temperatur aktualisiert.")
        else:
            print("⚠️ Anderes Topic, wird ignoriert.")
            return

        try_save_entry()

    except Exception as e:
        print("❌ Fehler beim Verarbeiten der Nachricht:", e)

# MQTT-Client konfigurieren
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(username, password)
client.on_message = on_message

print("📡 Starte MQTT-Client...")
client.connect(broker, port)
client.subscribe(topic_base, qos=0)  # Alle Untertopics abonnieren
client.loop_forever()
