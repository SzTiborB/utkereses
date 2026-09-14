import tkinter as tk
from tkinter import ttk
import networkx as nx
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import time
import fuggvenyek as fg

ablak = tk.Tk()
ablak.title("Az útkereső")
ablak.geometry("800x600")

#region - KONFIGURÁCIÓK
#gráf kezelés betöltése
G = nx.Graph()
#json betöltése
with open("graf.json", "r", encoding="utf-8") as file:
    graf = json.load(file)
# Matplotlib Figure létrehozása
fig = Figure(figsize=(6, 4), dpi=100)
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
       G.add_edge(varos, szomszed)
#endregion

#region - GOMB FUNCTION
def gomb_function():
    start_city = kezdo_lista.get()
    end_city = cel_lista.get()
    print(f"Kezdo: {start_city}, Cel: {end_city}")

    bejart_varosok = fg.A_star(start_city,end_city,graf,pos)
    print(f"bejart varosok: {bejart_varosok}")
#endregion

# subplot
ax = fig.add_subplot(111)
#ABLAK KETTÉOSZTÁSA - GRÁF/VEZÉRLŐ részekre
graf_frame = ttk.Frame(ablak)
graf_frame.grid(row=0, column=0)
vezerlo_frame = ttk.Frame(ablak)
vezerlo_frame.grid(row=1, column=0)


#AZ ABLAK MEGNYITÁSAKOR A GRÁFOT MUTASSA
nx.draw(
    G,
    pos,
    with_labels=True,
    ax=ax
)

# matplotlib beillesztése Tkinterbe
canvas = FigureCanvasTkAgg(fig, master=graf_frame)
#canvas.get_tk_widget().pack(fill="both",expand=True) - ez nem tudom mit csinál
canvas.draw()

#-----------------------
#region---VEZÉRLŐ ELEMEK
#varosok kinyerese a legordulo listahoz
varosok = list(G.nodes)


#label-ek
kezdo_label = ttk.Label(vezerlo_frame,text="Kezdő város:")
kezdo_label.grid(row=0, column=0,pady=5)
end_label = ttk.Label(vezerlo_frame,text="Cél város:")
end_label.grid(row=1,column=0,pady=5)

#legordulo list-ák
kezdo_lista = ttk.Combobox(vezerlo_frame,values=varosok,state="readonly")
kezdo_lista.grid(row=0, column=1,pady=5)
cel_lista = ttk.Combobox(vezerlo_frame,values=varosok,state="readonly")
cel_lista.grid(row=1,column=1,pady=5)

#gomb
inditas_gomb = ttk.Button(vezerlo_frame,text="Keresés indítása",command=gomb_function)
inditas_gomb.grid(row=2,column=0,columnspan=2)
#endregion
#-----------------------



canvas.get_tk_widget().pack(
    fill="both",
    expand=True
)
ablak.mainloop()