# MQTT-Datenlogger & Visualisierung – Projektübersicht

## 📡 MQTT-Datenempfang (`getmqttdata.py`)
- Verbindung zu einem öffentlichen MQTT-Broker (`iot1/teaching_factory/#`)
- Empfang und Filterung von Nachrichten zu:
  - `dispenser_red`
  - `temperature`
- Speicherung synchroner Datenpunkte in `daten.json` mittels `TinyDB`
- Automatische Kombination der Daten (Zeitstempel, Füllstand, Temperatur, Rezept, etc.)

## 🗃️ Datenbankstruktur (`daten.json`)
- JSON-basierte NoSQL-Datenbank (`TinyDB`)
- Strukturierte Speicherung in der Tabelle `messungen`
- Jeder Eintrag enthält u.a.:
  - Zeitstempel
  - Flaschennummer
  - Füllstand (g)
  - Temperatur (°C)
  - Rezept-ID

## 📄 CSV-Export (`data_csv.py`)
- Exportiert alle gespeicherten Messungen aus `daten.json` nach `export.csv`
- Verwendung von `csv.DictWriter` zur Strukturierung der Spalten

## 📊 Visualisierung
### 1. Mit `matplotlib` (`visualisierung.py`)
- Extraktion von Zeit und Temperatur aus `daten.json`
- Liniendiagramm zum Temperaturverlauf des Red Dispensers

### 2. Mit `Dash + Plotly` (`plotly_vis.py`)
- Webbasierte interaktive Visualisierung
- Darstellung des Temperaturverlaufs als interaktives Liniendiagramm
- Nutzung von Dash-Komponenten (`dcc.Graph`, `html.Div`)

## 🧰 Abhängigkeiten (`requirements.txt`)
- `tinydb`
- `paho-mqtt`
- `matplotlib`

## 🛠️ Sonstiges
- `.gitignore` schließt `venv/` und `*.json` aus
- Die Daten zeigen plausible Temperaturverläufe und Füllstände
