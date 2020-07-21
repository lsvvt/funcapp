import dash_core_components as dcc
import dash_html_components as html

from inf import app 
import dgeet as dg

fig1 = dg.figf("PBE0", ["M06-2X_S", "M06-2X-OPT6", "M06-2X-COMB14", "M06-2X-COMB7", "M06-2X-PBE25-OPT1", "PBE0"])

layout = html.Div([
    dcc.Graph(
        id='dpbe0',
        figure=fig1,
    )
])
