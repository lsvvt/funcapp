from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objects as go
from plotly.colors import n_colors
import numpy as np

from inf import app

colorsf = n_colors('rgb(255, 200, 200)', 'rgb(200, 0, 0)', 90, colortype='rgb')
colorsd = n_colors('rgb(255, 200, 200)', 'rgb(200, 0, 0)', 41, colortype='rgb')

a = ["CCSD", "M06-2X-COMB7", "PBE0", "M06-2X-PBE25-OPT1", "M06-2X-COMB14", "TPSS", "M06-2X-OPT6", "M06-2X_S", "M06-2X"]
b = [0, 1.808, 1.818, 1.867, 1.910, 2.043, 2.941, 4.028, 4.028]
c = [0, 24.9783, 83.4887, 89.1403, 19.5589, 0, 16.7704, 19.2325, 18.9840]

bc = list(map(lambda x: round(x * 10), b))
cc = list(map(lambda x: round(x), c))

c = ["?", 24.9783, 83.4887, 89.1403, 19.5589, "?", 16.7704, 19.2325, 18.9840]
hf = ["-", 0.540, 0.250, 0.250, 0.432, "-", 0.510, 0.540, 0.540]

fig = go.Figure(data=[go.Table(
  header=dict(  
    values=['<b>Функционал</b>', '<b>maxNE</b>', '<b>Ferr</b>', '<b>pHF</b>'],
    line_color='white', fill_color='white',
    align='center',font=dict(color='black', size=12)
  ),
  cells=dict(
    values=[a, b, c, hf],
    line_color=['purple', np.array(colorsd)[bc], np.array(colorsf)[cc], "purple"],
    fill_color=['purple', np.array(colorsd)[bc], np.array(colorsf)[cc], "purple"],
    align='center', font=dict(color='white', size=11)
    ))
])

fig.update_layout(height = 400)

layout = html.Div([
    dcc.Markdown("""
### Описание
Функционалы COMB - параметризованы по ошибке по базам данных (Ferr) и плотности энергии PBE0 (гамма - доля ошибки по плотности энергии)

M06-2X-COMB7 - лучший по плотности (гамма = 0.25)

M06-2X-COMB14 - хороший и по плотности и по базам данных (гамма = 0.0625)

M06-2X-PBE25-OPT1 - параметризован по плотности энергии PBE0

M06-2X-OPT6 - параметризован из параметров M06-2X-PBE25-OPT1 по базам данных

#### Таблица ошибок
"""),
    dcc.Graph(
        id='table',
        figure=fig,
        style = {"width" : "50%"}
    ),
    dcc.Markdown("""
p.s Все расчёты ошибок по базам данных выполнены на плотности PBE0 (кроме M06-2X_S)
"""),
])
