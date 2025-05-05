import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Simulación de datos (reemplaza con dataset real en producción)
df = pd.read_csv('tus_datos.csv')  # Usa tu dataset real

# Lógica de colores personalizados
rojos = ['#FFA5A5', '#FF7979', '#FF2C2C', '#FF0000', '#D60000', '#AA0000', '#990000']
verdes = ['#B4FF9A', '#92E27A', '#71C55B', '#4EA93B', '#258D19', '#007B00', '#007000']
limites_positivos = [0.0045, 0.0090, 0.0135, 0.0180, 0.0225, 0.0270]
limites_negativos = [-0.0045, -0.0090, -0.0135, -0.0180, -0.0225, -0.0270]

def color_por_rango(valor):
    if valor >= 0:
        for i, lim in enumerate(limites_positivos):
            if valor < lim:
                return verdes[i]
        return verdes[-1]
    else:
        for i, lim in enumerate(limites_negativos):
            if valor > lim:
                return rojos[i]
        return rojos[-1]

# Procesamiento
df["VALOR_ACTUAL"] = pd.to_numeric(df["VALOR_ACTUAL"], errors='coerce')
df["COSTOFACIAL"] = pd.to_numeric(df["COSTOFACIAL"], errors='coerce')
df.dropna(subset=["VALOR_ACTUAL", "COSTOFACIAL"], inplace=True)
df["ALIAS_operador"] = df["ALIAS_operador"].fillna("Desconocido")
df["calc_ganancias_perdidas"] = (df["VALOR_ACTUAL"] / df["COSTOFACIAL"]) - 1
df["color"] = df["calc_ganancias_perdidas"].apply(color_por_rango)

# Crear figura Plotly Treemap
fig = px.treemap(
    df,
    path=['ALIAS_operador', 'TITULO_inversiones'],
    values='VALOR_ACTUAL',
    color='calc_ganancias_perdidas',
    color_continuous_scale=verdes[::-1] + rojos,
    custom_data=['calc_ganancias_perdidas']
)

fig.update_traces(marker_colors=df["color"], hovertemplate='<b>%{label}</b><br>Ganancia/Pérdida: %{customdata[0]:.2%}')

# Inicializar app Dash
app = dash.Dash(__name__)
app.title = "Dashboard Operadores"

app.layout = html.Div([
    html.H1("% Ganancia / Pérdida por OPERADOR", style={'textAlign': 'center'}),
    dcc.Graph(id='treemap', figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
