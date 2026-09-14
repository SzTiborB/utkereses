import networkx as nx
import json
import matplotlib.pyplot as plt
import numpy as np
import fuggvenyek as fg
import time

#gráf kezelés betöltése
G = nx.Graph()

#json betöltése
with open("graf.json", "r", encoding="utf-8") as file:
    graf = json.load(file)

#2 város légvonalbeli távolságát számoló függvény
def get_tavolsag(varos1,varos2):
    tav = np.sqrt( (pos[varos1][0]-pos[varos2][0])**2 + (pos[varos1][1]-pos[varos2][1])**2)
    return tav

#pozíció manuális megadása:
pos = {
    "Nyíregyháza": (0, 2),
    "Nagyhalász": (1, 5),
    "Nagykálló": (2, 1),
    "Bakta": (5, 3),
    "Kisvárda": (5.5, 5.5),
    "Záhony": (6, 7),
    "Rohod": (6, 3.2),
    "Nyírbátor": (6, 1),
    "Vásárosnamény": (8, 4),
    "Mátészalka": (8, 2),
    "Nagyecsed": (9.5, 1.3),
    "Fehérgyarmat": (10.5, 2.2)
}

#Eltároljuk a városokat a G gráfban
#A szomszédos városok távolságait
for varos, szomszedok in graf.items():
    for szomszed, tavolsag in szomszedok.items():
       tavolsag = get_tavolsag(varos,szomszed)*9
       #print(f"{varos} - {szomszed}: {tavolsag}")
       G.add_edge(varos, szomszed, weight=tavolsag)



print("####Fügvény hívva ####")
bejart_varosok = fg.A_star("Nagykálló","Záhony",graf,pos)
fg.utvonal_animacio(G,pos,bejart_varosok)