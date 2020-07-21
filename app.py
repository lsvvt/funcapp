from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from inf import app, server
from tabs import info, de, dem, rho

style = {'maxWidth': '1700px', 'margin': 'auto'}

app.layout = html.Div([
    dcc.Markdown('# Графики ошибок'),
    dcc.Tabs(id='tabs', value='tab-info', children=[
        dcc.Tab(label='Информация', value='tab-info'),
        dcc.Tab(label='Ошибка по базам данных относительно PBE0', value='tab-de'),
        dcc.Tab(label='Ошибка по базам данных относительно M06-2X_S', value='tab-dem'),
        dcc.Tab(label='Ошибка в RHO, GRD и LR относительно PBE0', value='tab-rho'),
    ]),
    html.Div(id='tabs-content'),
], style=style)

@app.callback(Output('tabs-content', 'children'),
                [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-info': return info.layout
    elif tab == 'tab-de': return de.layout
    elif tab == 'tab-dem': return dem.layout
    elif tab == 'tab-rho': return rho.layout

if __name__ == '__main__':
    app.run_server(debug=True)