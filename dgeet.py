#!/usr/bin/python3

import numpy as np
import sys
import re
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots


db2a = 1 / 0.529177


def formatq(lines): # Функция форматирования для readlines()
    ans = []
    for j in lines:
        while "\n" in j:
            j = j.replace("\n", "")
        result = re.sub(" +", " ", j).split(" ")
        while result.count('') != 0:
            result.remove('')
        ans.append(result)
    return ans


def get(path):
    f = open(path)
    er = list(map(lambda x: [x[0], float(x[1])], formatq(f.readlines())[:-1]))
    f.close()
    return er


def gg(x, y):
    xy = []

    for i in range(len(x)):
        xy.append([x[i], y[i]])
    return xy


def dbcolor(db):
    ref_E = {
    "MGAE109":"lightcoral",
    "IP13":"black",
    "EA13":"tan",
    "PA8":"gold",
    "DBH76":"forestgreen",
    "NCCE31":"navy",
    "ABDE4":"chartreuse",
    "AE17":"lightskyblue",
    "pTC13":"darkorchid"
    }
    return ref_E[db]


def figf(ref, mass, dbs):
    path = "Ferr/"
    j = True

    x = get(path + ref + ".log")
    x.sort(key = lambda x: x[0])
    minn = min(x, key= lambda x: x[1])[1]
    maxx = max(x, key= lambda x: x[1])[1]

    fig = make_subplots(2, 3)

    i = 1
    k = 1
    for nf in mass:
        name = nf
        nf = nf + ".log"
        if name in mass:
            y = get(path + nf)
            y.sort(key = lambda x: x[0])

            xy = gg(x ,y)
            xy.sort(key = lambda x: x[0][1])
            # xy = np.array(xy)

            if k > 3:
                i += 1
                k = 1

            # print(k, i)

            xyn = []

            for db in xy:
                if db[0][0] in dbs:
                    xyn.append(db)
            
            # print(xy)

            xy = np.array(xyn)

            # print(xy)

            fig.add_trace(go.Scattergl(x = xy[:,1][:,1], y = xy[:,0][:,1], hovertext = xy[:,0][:,0], hoverinfo = "text",
                                mode='markers', marker = {"color" : list(map(dbcolor ,xy[:,0][:,0]))},
                                name=name, showlegend = False), i, k)
            fig.add_trace(go.Scattergl(x = np.linspace(minn, maxx, 2), y = np.linspace(minn, maxx, 2),
                                mode='lines', name = ref, showlegend = j, marker={"color" : "gray"}), i, k)
            if j == True:
                j = False
            fig.update_xaxes(title_text=name, row=i, col=k)
            if k == 1:
                fig.update_yaxes(title_text=ref, row=i, col=k)
            k += 1

    fig.update_xaxes(matches='x')
    fig.update_yaxes(matches='y')

    # fig.update_layout(title='Database Error (' + ref + ")")

    fig.update_layout(
                font=dict(
                    family="Courier New, monospace",
                    size=16,
                    color="#7f7f7f"
                ),
                height = 800
            )

    return fig


def get_rdf(inp):
    with open(inp) as gdf:
        points = formatq(gdf.readlines())
        return np.array(list(map(lambda x: [float(x[0]), float(x[1]), float(x[2])], points)))


def rmsd(inp, ref):
    return np.sqrt(sum((inp - ref) ** 2) / len(inp))


def get_metod(st):
    m = 0
    metod = ""

    for c in st:
        if m == 2 and c != "_":
            metod += c
        if c == "_":
            m += 1
    return metod


def get_type(st):
    m = 0
    metod = ""

    for c in st:
        if m == 3 and c != "_":
            metod += c
        if c == "_":
            m += 1
    return metod


def get_rms(lines, f):
    for line in lines:
        if line[0] == f:
            return float(line[1])
    return 0


def gen_files(lres, metod):
    ans = []
    for line in lres:
        if metod in line[0]:
            ans.append(line[0])
    return ans


def figrho(ref, metods):
    metod_ref = "CCSD"

    path = "ktestin/"

    fres = open(path + "res.log", "r")
    lres = formatq(fres.readlines())
    fres.close()

    fres = open(path + "res.log", "a")
    outlines = []

    fig = make_subplots(2, 3)

    xr = []
    xg = []
    xl = []
    j = True

    i = 1
    k = 1
    for metod in metods:
        if os.path.exists(path + metod):
            inf = os.listdir(path + metod)
        else:
            # print("WARNING")
            inf = gen_files(lres, metod)
        yr = []
        yg = []
        yl = []

        for f in inf:
            if get_metod(f[:-4]) == metod and ".rdf" in f:

                rms = get_rms(lres, f)

                if rms == 0:
                    tmp = get_rdf(path + metod + "/" + f)[:,2] * db2a
                    tmp_ref = get_rdf(path + metod_ref + "/" + f.replace(metod, metod_ref))[:,2] * db2a

                    rms = rmsd(tmp, tmp_ref)

                    outlines.append(f + " " + str(rms) + "\n")

                # print(f)
                # print(rms)
                # print()

                t = get_type(f[:-4])

                if t == "RHO":
                    rms = rms / 0.009943368
                    yr.append([f, rms])
                    if metod == ref:
                        xr.append([f, rms])
                elif t == "GRD":
                    rms = rms / 0.092398036
                    yg.append([f, rms])
                    if metod == ref:
                        xg.append([f, rms])
                elif t == "LR":
                    rms = rms / 1.445110833
                    yl.append([f, rms])
                    if metod == ref:
                        xl.append([f, rms])

        y = yg + yl + yr
        # y.sort()
        if metod == ref:
            x = xg + xl + xr

            x.sort(key = lambda x: x[0])
            # x = np.array(x)
        y.sort(key = lambda x: x[0])
        # y = np.array(y)

        xy = gg(x ,y)
        # print(xy)


        xy.sort(key = lambda x: x[0][1])
        xy = np.array(xy)

        if k > 3:
                i += 1
                k = 1

        if metod != metods[0]:
            fig.add_trace(go.Scattergl(x = xy[:,1][:,1], y = xy[:,0][:,1], hovertext = list(map(lambda x: x.replace("_PBE0_", " ")[:-4].replace("_", " "), xy[:,0][:,0])), hoverinfo = "text",
                                mode='markers',
                                name=metod, showlegend = False), i, k)
            fig.add_trace(go.Scattergl(x = np.linspace(float(min(xy[:,0][:,1])), float(max(xy[:,0][:,1])), 2), y = np.linspace(float(min(xy[:,0][:,1])), float(max(xy[:,0][:,1])), 2),
                                mode='lines',
                                name=ref, showlegend = j, marker={"color" : "gray"}), i, k)
            if j == True:
                j = False
            fig.update_xaxes(title_text=metod, row=i, col=k)
            if k == 1:
                fig.update_yaxes(title_text=ref, row=i, col=k)

            k += 1

    if len(outlines) > 0:
        fres.writelines(outlines)

    fres.close()

    fig.update_xaxes(matches='x')
    fig.update_yaxes(matches='y')

    # fig.update_layout(title='RHO, GRD and LR Error (' + ref + ")")

    fig.update_layout(
                font=dict(
                    family="Courier New, monospace",
                    size=16,
                    color="#7f7f7f"
                ),
                height = 800
            )

    return fig

if __name__ == '__main__':
    fig1 = figf("PBE0", ["M06-2X_S", "M06-2X-OPT6", "M06-2X-COMB14", "M06-2X-COMB7", "M06-2X-PBE25-OPT1", "PBE0"])
    fig2 = figf("M06-2X_S", ["M06-2X_S", "M06-2X-OPT6", "M06-2X-COMB14", "M06-2X-COMB7", "M06-2X-PBE25-OPT1", "PBE0"])
    fig3 = figrho("PBE0", ["PBE0", "M06-2X", "M06-2X-OPT6", "M06-2X-COMB14", "M06-2X-COMB7", "M06-2X-PBE25-OPT1", "TPSS"])

    # app.run_server(debug=True)