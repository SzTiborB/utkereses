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
fig = Figure(figsize=(8,4), dpi=100)
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

#region - rajzolas fuggvenyek
def utvonal_rajzolas(bejart_varosok):
    for i in range(len(bejart_varosok)):
        # eddig bejárt élek
        piros_elek = []
        for j in range(i):
            piros_elek.append(
                (bejart_varosok[j], bejart_varosok[j + 1])
            )
        # piros élek rárajzolása
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=piros_elek,
            edge_color="red",
            width=3,
            ax=ax
        )
        canvas.draw()
        ablak.update()
        time.sleep(1)

def reszletes_utvonal_rajzolas(bejart_varosok,menet):
    print("#### kijelzes inditasa ####")
    for i in range(len(menet)):
        print(f"Választott út: {menet[i]["valasztott"]}")
        print("Nem választott")
        for utvonal in menet[i]["nemvalasztott"]:
            print(f"-- {utvonal}")

    for i in range(len(menet)): # végigmegy a megoldás lépésein

        for utvonal in menet[i]["nemvalasztott"]: # 1 lépés összes lehetséges opcióján végigmegy pirossal

            ax.clear()
            nx.draw(G,pos,with_labels=True,ax=ax)
            piros_elek = list(zip(utvonal[:-1], utvonal[1:]))
            # piros élek rárajzolása
            nx.draw_networkx_edges(G,pos,edgelist=piros_elek,edge_color="red",width=3,ax=ax)
            canvas.draw()
            ablak.update()
            time.sleep(0.2)

        #majd zölddel kijelzi a választott utat
        ax.clear()
        nx.draw(G,pos,with_labels=True,ax=ax)
        valasztott_utvonal = menet[i]["valasztott"]
        zold_elek = list(zip(valasztott_utvonal[:-1], valasztott_utvonal[1:]))
        nx.draw_networkx_edges(G,pos,edgelist=zold_elek,edge_color="green",width=3,ax=ax)
        canvas.draw()
        ablak.update()
        time.sleep(0.6)
        
#endregion

#region - GOMB FUNCTION
def gomb_function():

    #
    ax.clear()
    nx.draw(
    G,
    pos,
    with_labels=True,
    ax=ax)

    start_city = kezdo_lista.get()
    end_city = cel_lista.get()
    #print(f"Kezdo: {start_city}, Cel: {end_city}")

    bejart_varosok,menet = fg.A_star(start_city,end_city,graf,pos)
    #print(f"bejart varosok: {bejart_varosok}")

    #RAJZOLJUK KI AZ UTVONALAT
    time.sleep(0.2)
    reszletes_utvonal_rajzolas(bejart_varosok,menet)
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
kezdo_label = ttk.Label(vezerlo_frame,text="Kezdő város:",font=("Arial", 12))
kezdo_label.grid(row=0, column=0,pady=5)
end_label = ttk.Label(vezerlo_frame,text="Cél város:",font=("Arial", 12))
end_label.grid(row=1,column=0,pady=5)

#legordulo list-ák
kezdo_lista = ttk.Combobox(vezerlo_frame,values=varosok,state="readonly")
kezdo_lista.grid(row=0, column=1,pady=5)
cel_lista = ttk.Combobox(vezerlo_frame,values=varosok,state="readonly")
cel_lista.grid(row=1,column=1,pady=5)

#gomb
inditas_gomb = ttk.Button(vezerlo_frame,text="Keresés indítása",command=gomb_function,width=20)
inditas_gomb.grid(row=2,column=0,columnspan=2)
#endregion
#-----------------------



canvas.get_tk_widget().pack(
    fill="both",
    expand=True
)
ablak.mainloop()