import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import geopandas as gpd

app = dash.Dash()

colors = {
    'background': '#111111',
    'text': '#000080'
}

# Pre-processing -------------------------------------------------------------------------------
# Data
# line chart national
national_preds = pd.read_csv(
    "https://raw.githubusercontent.com/csss-resultat/openData/main/datasets/nationella_senaste.csv"
)

# National Map
# Reading the shape file for map plotting
gdf_map = gpd.read_file('data/scb/Lan_Sweref99TM_region.shp', encoding='utf-8')
# Change the CRS to make Sweden thiner
gdf_map = gdf_map.to_crs('EPSG:3021')
gdf_map["Lan"] = ['Stockholm', 'Uppsala', 'Södermanland', 'Östergötland', 'Jönköping', 'Kronoberg', 'Kalmar',
                         'Gotland', 'Blekinge', 'Skåne', 'Halland', 'Västra Götaland', 'Värmland', 'Örebro', 'Västmanland', 'Dalarna',
                         'Gävleborg', 'Västernorrland',  'Jämtland', 'Västerbotten', 'Norrbotten']

# Counties preds
counties_preds = pd.read_csv("https://raw.githubusercontent.com/csss-resultat/openData/main/datasets/lan_senaste.csv"
)
counties_preds.Datum = pd.to_datetime(counties_preds["Datum"])
latest_date = counties_preds["Datum"].max()
counties_preds = counties_preds.loc[counties_preds["Datum"] == latest_date]
counties_preds.Uppskattning = counties_preds.Uppskattning * 100
counties_preds.Low_CI = counties_preds.Low_CI * 100
counties_preds.High_CI = counties_preds.High_CI * 100

gdf_plot = gdf_map.merge(counties_preds, left_on='Lan', right_on = 'Lan', how='left')

# Plots ----------------------------------------------------------------------------------------

lineplot_national = go.Figure()
lineplot_national.add_trace(go.Scatter(x=national_preds.Datum, y=national_preds.Uppskattning, mode='lines+markers', showlegend=False, name ="% uppskattad förekomst"))
lineplot_national.add_trace(go.Scatter(
    name='Upper Bound',
    x=national_preds['Datum'],
    y=national_preds['High_CI'],
    mode='lines',
    marker=dict(color="rgba(255,255,255,0)"),
    showlegend=False)
)
lineplot_national.add_trace(go.Scatter(
    name='Lower Bound',
    x=national_preds['Datum'],
    y=national_preds['Low_CI'],
    marker=dict(color="rgba(255,255,255,0)"),
    mode='lines',
    fillcolor='rgba(68, 68, 68, 0.3)',
    fill='tonexty',
    showlegend=False)
)


lineplot_national.update_layout(title="",
                                xaxis_title='Datum',
                                yaxis_title="Uppskattad förekomst av symtomatisk covid-19",
                                yaxis_range=[0,1],
                                yaxis=dict(
                      tickmode='array',
                      tickvals=[0,0.2, 0.4, 0.6, 0.8, 1.0],
                      ticktext=["0 %","O,2 %", "0,4 %", "0,6 %", "0,8 %", "1,0 %"]
                  )
                                )


xaxis = dict(
    tickmode='array',
    tickvals=[1, 3, 5, 7, 9, 11],
    ticktext=['One', 'Three', 'Five', 'Seven', 'Nine', 'Eleven']
)


app.layout = html.Div(children=[
    html.H1(
        children='COVID Symptom Study Sverige - Dashboard',
        style={
            'textAlign': 'left',
            'color': colors['text']
        }
    ),
    html.H4(
        children='Välkommen till COVID Symptom Study Sveriges dashboard med interaktiv grafik. Du navigerar via menyn till vänster där du hittar våra senaste nationella och regionala kartor. Använd datumreglaget för att välja det datum du vill visa för kartorna. Vi arbetar hela tiden med att utöka funktionaliteten och innehållet på denna sida så vi ber om ert tålamod under tiden som sidan utvecklas',
        style={
            'textAlign': 'left',
            'color': colors['text']
        }
    ),
    dcc.Graph(id="life-exp-vs-gdp", figure=lineplot_national)
])


if __name__ == "__main__":
    app.run_server(debug=True)