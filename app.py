from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from inf import app, server
from tabs import intro, predict, explain, evaluate

style = {'maxWidth': '960px', 'margin': 'auto'}

app.layout = html.Div([
    dcc.Markdown('Title'),
    dcc.Tabs(id='tabs', value='tab-intro', children=[
        dcc.Tab(label='Info', value='tab-intro'),
        # dcc.Tab(label='RHO PBE0', value='tab-1'),
        # dcc.Tab(label='DB PBE0', value='tab-2'),
        # dcc.Tab(label='DB Others', value='tab-3'),
    ]),
    html.Div(id='tabs-content'),
], style=style)

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-intro': return intro.layout
    # elif tab == 'tab-1': return 1.layout
    # elif tab == 'tab-2': return 2.layout
    # elif tab == 'tab-3': return 3.layout

if __name__ == '__main__':
    app.run_server(debug=True)