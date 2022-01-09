import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

app = dash.Dash()

colors = {
    'background': '#111111',
    'text': '#000080'
}

df = pd.read_csv(
    "https://raw.githubusercontent.com/csss-resultat/openData/main/datasets/nationella_senaste.csv"
)

fig = go.Figure()
fig.add_trace(go.Scatter(x=df.Datum, y=df.Uppskattning,mode='lines+markers', showlegend=False))
fig.add_trace(go.Scatter(
    name='Upper Bound',
    x=df['Datum'],
    y=df['High_CI'],
    mode='lines',
    marker=dict(color="rgba(255,255,255,0)"),
    showlegend=False)
)
fig.add_trace(go.Scatter(
    name='Lower Bound',
    x=df['Datum'],
    y=df['Low_CI'],
    marker=dict(color="rgba(255,255,255,0)"),
    mode='lines',
    fillcolor='rgba(68, 68, 68, 0.3)',
    fill='tonexty',
    showlegend=False)
)


fig.update_layout(title="",
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
    dcc.Graph(id="life-exp-vs-gdp", figure=fig)
])


if __name__ == "__main__":
    app.run_server(debug=True)