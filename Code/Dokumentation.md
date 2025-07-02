# Aufgabe 12.1: MQTT-Client für SPS

## Ziel des Versuchs

Ziel dieses Versuchs ist es, eine Beckhoff-SPS über das MQTT-Protokoll mit einem MQTT-Broker zu verbinden und Daten zu veröffentlichen. Als Beispiel wird ein Teamname einmalig an einen MQTT-Topic übermittelt. Die Programmierung erfolgt in TwinCAT 3 mit dem Funktionsbaustein `FB_IotMqttClient`.

---

## Aufbau und Funktionsweise des Programms

Das SPS-Programm besteht aus einem **Deklarationsbereich**, in dem Variablen definiert werden, und einem **Ausführungsbereich**, in dem die Programmlogik implementiert ist.

### 1. Initialisierung und MQTT-Verbindung

Zunächst wird eine Instanz des MQTT-Clients erstellt und mit den notwendigen Parametern konfiguriert:

- **IP-Adresse des MQTT-Brokers** (`sHostName`) wird auf eine konkrete IP gesetzt.
- Der **Port** (`nHostPort`) ist auf 1883 festgelegt, was dem Standard für unverschlüsseltes MQTT entspricht.
- Weitere Einstellungen beinhalten ein **Topic-Präfix**, einen **Client-ID-Namen**, sowie **Benutzername** und **Passwort**.
- Anschließend wird der MQTT-Client mit dem Befehl `Execute(bConnect := TRUE)` aktiviert, wodurch eine Verbindung aufgebaut wird.

### 2. Bedingtes Senden einer Nachricht

Nachdem die Verbindung erfolgreich aufgebaut wurde (d. h. der MQTT-Client ist verbunden), prüft das Programm, ob die Verbindung besteht.

Sobald die Verbindung aktiv ist, wird eine Zeichenkette mit Namen (Teammitglieder) über das MQTT-Protokoll an den Broker gesendet. Das Ziel-Topic ist dabei 'aut/gruppe1/names' zusammengesetzt aus dem konfigurierten Präfix (`aut/gruppe1/`) und einem statischen Teil (`names`). 
![Twincad oben](Screenshots/twincad_oben.png)



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
