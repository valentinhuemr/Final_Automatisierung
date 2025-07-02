import dash
from dash import dcc, html
import plotly.graph_objs as go
from tinydb import TinyDB
from datetime import datetime

# Daten laden
db = TinyDB("daten.json")
daten = db.table("messungen").all()

# Daten extrahieren
x = [datetime.fromisoformat(e['timestamp']) for e in daten]
y = [float(e['temperature_C_red']) for e in daten]

# Dash App
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Temperaturverlauf"),
    dcc.Graph(figure=go.Figure(data=[go.Scatter(x=x, y=y, mode='lines+markers')]))
])

if __name__ == '__main__':
    # Verwende die neuere Syntax für den Serverstart
    from dash import Dash
    app.run(debug=True)
