import os, warnings
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output
from influxdb_client import InfluxDBClient
from influxdb_client.client.warnings import MissingPivotFunction

# Limpiamos advertencias para una terminal más limpia en tu Fedora
warnings.simplefilter("ignore", MissingPivotFunction)
warnings.filterwarnings("ignore", category=FutureWarning)

# Configuración desde .env
INFLUX_URL    = os.getenv("INFLUX_URL",    "http://influxdb:8086")
INFLUX_TOKEN  = os.getenv("INFLUX_TOKEN",  "")
INFLUX_ORG    = os.getenv("INFLUX_ORG",    "")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "")
DASH_PORT     = int(os.getenv("DASH_PORT", "8050"))

client    = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
query_api = client.query_api()

def query_latest(minutes=10):
    """Obtiene el último estado de cada sensor de Mérida."""
    # Cambiamos 'your_measurement' por 'traffic_measurement'
    # Y '_field == value_1' por '_field == vehicles'
    q = f'''
    from(bucket: "{INFLUX_BUCKET}")
      |> range(start: -{minutes}m)
      |> filter(fn: (r) => r._measurement == "traffic_measurement")
      |> filter(fn: (r) => r._field == "vehicles")
      |> last()
    '''
    try:
        tables = query_api.query(q)
        rows = []
        seen = set()
        for table in tables:
            for r in table.records:
                sid = r.values.get("sensor_id", "")
                if sid in seen: continue
                seen.add(sid)
                rows.append({
                    "sensor_id": sid,
                    "location": r.values.get("location", "Mérida"),
                    "level": r.values.get("level", "low"),
                    "vehicles": r.get_value()
                })
        return pd.DataFrame(rows) if rows else pd.DataFrame()
    except Exception as e:
        print(f"[DASH] Error en query_latest: {e}")
        return pd.DataFrame()

def query_timeseries(sensor_id, minutes=15):
    """Obtiene el histórico de un sensor específico seleccionado en el menú."""
    q = f'''
    from(bucket: "{INFLUX_BUCKET}")
      |> range(start: -{minutes}m)
      |> filter(fn: (r) => r._measurement == "traffic_measurement")
      |> filter(fn: (r) => r._field == "vehicles")
      |> filter(fn: (r) => r["sensor_id"] == "{sensor_id}")
      |> aggregateWindow(every: 30s, fn: mean, createEmpty: false)
    '''
    try:
        df = query_api.query_data_frame(q)
        if df.empty: return pd.DataFrame()
        # Limpiamos el DataFrame para Plotly
        df = df.groupby("_time", as_index=False)["_value"].mean()
        return df.rename(columns={"_time": "tiempo", "_value": "vehiculos"})
    except Exception as e:
        print(f"[DASH] Error en timeseries: {e}")
        return pd.DataFrame()

# --- Interfaz de Usuario ---
app = Dash(__name__, title="Mérida Smart Traffic")

app.layout = html.Div(style={'fontFamily': 'sans-serif', 'padding': '20px'}, children=[
    html.H1("📊 Monitoreo de Tráfico Urbano - Mérida", 
            style={"textAlign": "center", "color": "#2c3e50"}),

    # Gráfico 1: Estado Actual (Barras)
    html.Div([
        dcc.Graph(id="chart-1", style={"height": "350px"}),
    ], style={"padding": "10px"}),

    # Gráfico 2: Distribución (Scatter)
    html.Div([
        dcc.Graph(id="chart-2", style={"height": "350px"}),
    ], style={"padding": "10px"}),

    # Gráfico 3: Histórico con Dropdown (Filtro interactivo)
    html.Div([
        html.H3("Análisis Histórico por Sensor"),
        dcc.Dropdown(id="sensor-dropdown", placeholder="Selecciona un punto de control..."),
        dcc.Graph(id="chart-3", style={"height": "300px"}),
    ], style={"padding": "20px", "backgroundColor": "#f8f9fa", "borderRadius": "10px"}),

    dcc.Interval(id="tick", interval=5_000, n_intervals=0),
])

# --- Lógica de los Gráficos ---
@app.callback(
    Output("chart-1", "figure"),
    Output("chart-2", "figure"),
    Output("sensor-dropdown", "options"),
    Input("tick", "n_intervals"),
)
def update_main_charts(n):
    df = query_latest()
    if df.empty:
        return go.Figure(), go.Figure(), []

    # Gráfico 1: Barras
    fig1 = px.bar(df, x="sensor_id", y="vehicles", color="level",
                  title="Conteo de Vehículos Actual",
                  color_discrete_map={"low": "#2ecc71", "moderate": "#f1c40f", "heavy": "#e74c3c"})

    # Gráfico 2: Scatter (Ubicaciones)
    fig2 = px.scatter(df, x="location", y="vehicles", size="vehicles", color="level",
                      title="Densidad por Zona Geográfica")

    options = [{"label": f"{r['location']} ({r['sensor_id']})", "value": r["sensor_id"]}
               for _, r in df.iterrows()]
    
    return fig1, fig2, options

@app.callback(
    Output("chart-3", "figure"),
    Input("sensor-dropdown", "value"),
    Input("tick", "n_intervals"),
)
def update_timeseries(sensor_id, n):
    if not sensor_id:
        return go.Figure().update_layout(title="Selecciona un sensor para ver su histórico")
    
    df = query_timeseries(sensor_id)
    if df.empty:
        return go.Figure()

    fig = px.line(df, x="tiempo", y="vehiculos", 
                  title=f"Tendencia en: {sensor_id}",
                  line_shape="spline")
    return fig

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=DASH_PORT, debug=False)