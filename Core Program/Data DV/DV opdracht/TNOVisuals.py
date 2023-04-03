# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Incorporate data
df = pd.read_csv('DV opdracht/1Day2022.csv')

# Initialize the app - incorporate css
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)


# App layout
app.layout = html.Div([
    html.Div(className='row', children='Interactive Air Pollution Graph',
             style={'textAlign': 'center', 'color': 'blue', 'fontSize': 30}),

    html.Div(className='row', children=[
        dcc.RadioItems(options=['PM1(μg/m³)', 'PM2.5(μg/m³)', 'PM10(μg/m³)', 'NO2(μg/m³)'],
                       value='NO2(μg/m³)',
                       inline=True,
                       id='my-radio-buttons-final')
    ]),

    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dash_table.DataTable(data=df.to_dict('records'), page_size=11, style_table={'overflowX': 'auto'})
        ]),
        html.Div(className='six columns', children=[
            dcc.Graph(figure={}, id='histo-chart-final')
        ])
    ])
])


# Add controls to build the interaction
@callback(
    Output(component_id='histo-chart-final', component_property='figure'),
    Input(component_id='my-radio-buttons-final', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='Time(UTC)', y=col_chosen, histfunc='avg')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)