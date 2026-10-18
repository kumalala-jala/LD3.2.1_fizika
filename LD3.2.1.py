from kludu_rekinatajs import *
import sympy as sym
import numpy as np
import matplotlib.pyplot as plt
import copy
import word_maker
saurakai_mer = [[0.7],
              [1.31],
              [1.9],
              [2.49],
              [3.1],
              [3.7],
              [4.33],
              [4.92],
              [5.5],
              [6.11],
              [6.86]]
platakai_mer = [[0.19],
              [0.45],
              [0.71],
              [1],
              [1.21],
              [1.45],
              [1.7],
              [1.99],
              [2.18],
              [2.44],
              [2.68]]
a_mer = [[395] for i in range(11)]

merijumi_rekinatajam = [{"merierices pamatkluda": 0.01, "merijumi": saurakai_mer, "simbols": "x_i_saur", "Mērvienība": "mm"},
                        {"merierices pamatkluda": 0.01, "merijumi": platakai_mer, "simbols": "x_i_plat", "Mērvienība": "mm"},
                        {"merierices pamatkluda": 1, "merijumi": a_mer, "simbols": "a", "Mērvienība": "mm"}]


merijumu_kludas = aprekinat_tiesas_kludas(merijumi_rekinatajam)
merijumu_kludas = copy.deepcopy(merijumu_kludas)

### m = 5 vilna gar 
x_i = []
grupas = {}
p = 0
for nr in merijumu_kludas.keys():
    if p > 5:
        break
    mer_grupa = {"x_i": {}, "x_i_plus5": {}, "d": {"vertiba": 0.344, "kluda": 0}, "m": {"vertiba": 5, "kluda": 0}, "a":{"vertiba": merijumu_kludas[nr]["a"]["vertiba"], "kluda": merijumu_kludas[nr]["a"]["kluda"]}}
    for i in range(0+p, 6+p, 11):
        mer_grupa["x_i"] = {"vertiba": merijumu_kludas[f"Nr.{i+1}"]["x_i_saur"]["vertiba"], "kluda": merijumu_kludas[f"Nr.{i+1}"]["x_i_saur"]["kluda"]}
        mer_grupa["x_i_plus5"] = {"vertiba": merijumu_kludas[f"Nr.{i+6}"]["x_i_saur"]["vertiba"], "kluda": merijumu_kludas[f"Nr.{i+6}"]["x_i_saur"]["kluda"]}
    p +=1
    grupas[nr] = mer_grupa

x_i, x_i_plus5, d, a, m = sym.symbols("x_i, x_i_plus5, d, a, m")
syms = [x_i, x_i_plus5, d, a, m]
lambda_ = (d*(x_i_plus5-x_i))/(a*m)
lambdas = aprekinat_netiesas_kludas(grupas, lambda_, "lambda", syms, mervieniba="mm")
lambdas_for_word = {}
for i in range(6):
    lambdas_for_word[f"lambdas no x_{i+1} līdz x_{i+6} šaurajai dubultspraugai"] = lambdas[f"Nr.{i+1}"]
lambda_1, lambda_2, lambda_3, lambda_4, lambda_5, lambda_6 = sym.symbols("lambda_1, lambda_2, lambda_3, lambda_4, lambda_5, lambda_6")
syms = [lambda_1, lambda_2, lambda_3, lambda_4, lambda_5, lambda_6]
lambda_vid = (lambda_1+ lambda_2+ lambda_3+ lambda_4+ lambda_5+ lambda_6)/6
prieks_lambda_vid = {f"vid": {f"lambda_{i+1}": lambdas[f"Nr.{i+1}"]["lambda"] for i in range(6)}}
lambda_vid_r = aprekinat_netiesas_kludas(prieks_lambda_vid, lambda_vid, "lambda_vid", syms, mervieniba="mm")



### m = 6 d platajam
x_i = []
grupas2 = {}
p = 0
for nr in merijumu_kludas.keys():
    if p > 4:
        break
    mer_grupa = {"x_i": {}, "x_i_plus6": {}, "lambda_vid": {"vertiba": lambda_vid_r["vid"]["lambda_vid"]["vertiba"], "kluda": lambda_vid_r["vid"]["lambda_vid"]["kluda"]}, "m": {"vertiba": 6, "kluda": 0}, "a":{"vertiba": merijumu_kludas[nr]["a"]["vertiba"], "kluda": merijumu_kludas[nr]["a"]["kluda"]}}
    for i in range(0+p, 6+p, 11):
        mer_grupa["x_i"] = {"vertiba": merijumu_kludas[f"Nr.{i+1}"]["x_i_plat"]["vertiba"], "kluda": merijumu_kludas[f"Nr.{i+1}"]["x_i_plat"]["kluda"]}
        mer_grupa["x_i_plus6"] = {"vertiba": merijumu_kludas[f"Nr.{i+7}"]["x_i_plat"]["vertiba"], "kluda": merijumu_kludas[f"Nr.{i+7}"]["x_i_plat"]["kluda"]}
    p +=1
    grupas2[nr] = mer_grupa

x_i, x_i_plus6, lambda_vid, a, m  = sym.symbols("x_i, x_i_plus6, lambda_vid, a, m ")
syms = [x_i, x_i_plus6, lambda_vid, a, m ]
d_vien = (lambda_vid*a*m)/(x_i_plus6 - x_i)
d_vertibas = aprekinat_netiesas_kludas(grupas2, d_vien, "d", syms, mervieniba="mm")
d_for_word = {}
for i in range(5):
    d_for_word[f"d no x_{i+1} līdz x_{i+7} platajai dubultspraugai"] = d_vertibas[f"Nr.{i+1}"]
d_1, d_2, d_3, d_4, d_5 = sym.symbols("d_1, d_2, d_3, d_4, d_5")
syms = [d_1, d_2, d_3, d_4, d_5]
d_vid_vien = (d_1+ d_2+ d_3+ d_4+ d_5)/5
prieks_d_vid = {f"vid": {f"d_{i+1}": d_vertibas[f"Nr.{i+1}"]["d"] for i in range(5)}}

d_vid = aprekinat_netiesas_kludas(prieks_d_vid, d_vid_vien, "d_vid", syms, mervieniba="mm")
print(d_vid)


results = [merijumu_kludas, lambdas_for_word, d_for_word, lambda_vid_r, d_vid]
results = round_results(results)
word_maker.generate(results, "LD3.2.1_generated.docx", aprekinu_nr=[1, "vid", f"lambdas no x_1 līdz x_6 šaurajai dubultspraugai", f"d no x_1 līdz x_7 platajai dubultspraugai"])
# grafiki
