import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
from tinydb import TinyDB
from datetime import datetime
import os

# Datenbank laden
db = TinyDB("daten.json")
daten = db.table("messungen").all()

if not daten:
    print("Keine Daten in der Datenbank gefunden!")
    exit()

# Bestimme alle numerischen Felder (außer timestamp)
sample_entry = daten[0]
numeric_fields = []

for key, value in sample_entry.items():
    if key != 'timestamp':
        try:
            float(value)
            numeric_fields.append(key)
        except (ValueError, TypeError):
            pass

if not numeric_fields:
    print("Keine numerischen Datenfelder gefunden!")
    exit()

print(f"Gefundene Datenfelder: {numeric_fields}")

# Extrahiere Zeitstempel
timestamps = [datetime.fromisoformat(entry['timestamp']) for entry in daten]

# Erstelle ein Diagramm für alle Datenreihen - mit weniger Abstand
fig = make_subplots(rows=len(numeric_fields), cols=1, 
                    subplot_titles=[field.replace('_', ' ').title() for field in numeric_fields],
                    shared_xaxes=True, 
                    vertical_spacing=0.03)  # Reduzierter Abstand zwischen Diagrammen

for i, field in enumerate(numeric_fields):
    # Extrahiere Daten für dieses Feld
    try:
        values = [float(entry[field]) for entry in daten]
        
        # Füge Trace hinzu
        fig.add_trace(
            go.Scatter(
                x=timestamps, 
                y=values, 
                mode='lines+markers',
                name=field.replace('_', ' ').title()
            ),
            row=i+1, col=1
        )
    except (KeyError, ValueError) as e:
        print(f"Fehler beim Verarbeiten von {field}: {e}")

# Layout anpassen
fig.update_layout(
    title="Alle Messdaten im Zeitverlauf",
    height=200 * len(numeric_fields),  # Reduzierte Höhe pro Diagramm
    width=1000,
    showlegend=True,
    margin=dict(t=50, b=50, l=50, r=50)  # Kompaktere Ränder
)

# Zeige nun Zeitstempel bei ALLEN Diagrammen an
for i in range(len(numeric_fields)):
    # Zeige die X-Achsenbeschriftung bei allen Diagrammen
    fig.update_xaxes(showticklabels=True, row=i+1, col=1)
    
    # Nur beim letzten Diagramm zusätzlich den Titel "Zeitpunkt" anzeigen
    if i == len(numeric_fields) - 1:
        fig.update_xaxes(title_text="Zeitpunkt", row=i+1, col=1)

# Als HTML-Datei speichern
output_file = "alle_messdaten.html"
fig.write_html(output_file)
print(f"Diagramm wurde gespeichert als: {os.path.abspath(output_file)}")

# Diagramm im Browser öffnen
pio.renderers.default = "browser"
fig.show()

# Einzeldiagramme für jedes Datenfeld erstellen
os.makedirs("einzeldiagramme", exist_ok=True)

for field in numeric_fields:
    try:
        values = [float(entry[field]) for entry in daten]
        
        single_fig = go.Figure()
        single_fig.add_trace(go.Scatter(
            x=timestamps, 
            y=values, 
            mode='lines+markers'
        ))
        
        single_fig.update_layout(
            title=f"{field.replace('_', ' ').title()} im Zeitverlauf",
            xaxis_title="Zeitpunkt",
            yaxis_title=field.replace('_', ' ').title(),
            height=600,
            width=1000
        )
        
        # Speichern
        single_file = f"einzeldiagramme/{field}.html"
        single_fig.write_html(single_file)
        print(f"Einzeldiagramm gespeichert als: {os.path.abspath(single_file)}")
        
    except (KeyError, ValueError) as e:
        print(f"Fehler beim Erstellen des Einzeldiagramms für {field}: {e}")