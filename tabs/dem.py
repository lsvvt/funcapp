from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from inf import app 
import dgeet as dg

style = {'padding': '1.5em'}

db = [
"MGAE109",
"IP13",
"EA13",
"PA8",
"DBH76",
"NCCE31",
"ABDE4",
"AE17",
"pTC13"]

layout = html.Div([
    html.Div([
        dcc.Markdown('###### DB'),
        dcc.Checklist(
            id = "dbbs",
            options=[{'label': dbv, 'value': dbv} for dbv in db],
            value=db,
            labelStyle={'display': 'inline-block'}),
    ], style=style),

    dcc.Graph(
        id='dm06',
    )
])

@app.callback(
    Output(component_id='dm06', component_property='figure'),
    [Input(component_id='dbbs', component_property='value')]
)
def update_figure(datbases):
    # f = open("/work/funcapp/log.log", "w")
    # f.writelines(datbases)
    # f.close()
    # dbref = [
    # "MGAE109",
    # "IP13",
    # "EA13",
    # "PA8",
    # "DBH76",
    # "NCCE31",
    # "ABDE4",
    # "AE17",
    # "pTC13"]
    fig = dg.figf("M06-2X_S", ["M06-2X_S", "M06-2X-OPT6", "M06-2X-COMB14", "M06-2X-COMB7", "M06-2X-PBE25-OPT1", "PBE0"], datbases)

    return fig