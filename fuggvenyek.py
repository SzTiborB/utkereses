import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

def A_star(start_city,end_city,graf,pos):
    bejart_varosok_lista = [start_city]
    megtett_tav=0
    is_finished = False

    def get_tavolsag(varos1,varos2,pos):
        tav = np.sqrt( (pos[varos1][0]-pos[varos2][0])**2 + (pos[varos1][1]-pos[varos2][1])**2)
        return tav

    def A_star_next_step(start_city,end_city,graf):
        lehetseges_lepesek = {}
        for szomszed, tavolsag in graf[start_city].items():
            

            heur_tav = get_tavolsag(szomszed,end_city,pos)
            ut_tav = get_tavolsag(start_city,szomszed,pos)
            ossztav = float(heur_tav+ut_tav) #alapból np.double
            lehetseges_lepesek[szomszed]=ossztav
            print(f"Lehetseges lepes: {szomszed} - {ossztav}")
        kovetkezo_varos = min(lehetseges_lepesek, key=lehetseges_lepesek.get)
        print(f"LÉPÉS {start_city}-ről {kovetkezo_varos}-ra")
        return kovetkezo_varos,lehetseges_lepesek[kovetkezo_varos]

    varos,lepes_tav = A_star_next_step(start_city,end_city,graf)
    bejart_varosok_lista.append(varos)
    start_city = varos
    megtett_tav += lepes_tav
    if varos == end_city:
        is_finished = True
    while not is_finished:
        varos,lepes_tav = A_star_next_step(start_city,end_city,graf)
        bejart_varosok_lista.append(varos)
        start_city = varos
        megtett_tav += lepes_tav
        if varos == end_city:
            is_finished = True
    #print(f"celba erve ezen az utvonalon: {bejart_varosok_lista}, tav: {megtett_tav}")
    print("A* veget ert")
    return bejart_varosok_lista

def utvonal_animacio(G, pos, utvonal):
    plt.ion()   # interaktív mód bekapcsolása

    for i in range(len(utvonal)):
        plt.clf()   # előző rajz törlése
        # teljes gráf újrarajzolása
        nx.draw(
            G,
            pos,
            with_labels=True
        )
        # eddig bejárt élek
        piros_elek = []
        for j in range(i):
            piros_elek.append(
                (utvonal[j], utvonal[j + 1])
            )
        # piros élek rárajzolása
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=piros_elek,
            edge_color="red",
            width=3
        )
        plt.pause(1)

    plt.ioff()
    plt.show()
