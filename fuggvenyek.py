import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


def get_tavolsag(varos1,varos2,pos):
    tav = np.sqrt( (pos[varos1][0]-pos[varos2][0])**2 + (pos[varos1][1]-pos[varos2][1])**2)
    return tav


def A_star(start_city,end_city,graf,pos):
    lehetseges_lepesek = {(start_city,): 1}
    megtett_tav=0
    is_finished = False
    #hogy ne lehessen visszalépni már bejárt csomópontra
    bejart_varosok = [start_city]

    while is_finished == False:
        for kulcs in list(lehetseges_lepesek.keys()): #az összes feltárt útvonal
            if kulcs[-1] == start_city: #fejtse ki azokat az útvonalakat amiknek a vége az a város amin éppen állok
                for szomszed in graf[start_city]: # a mostani város szomszédait nézzük meg
                    if szomszed not in bejart_varosok: # ne léphessünk olyan városra ahol már voltunk
                        lehetseges_lepesek[kulcs+(szomszed,)]=0 #előzetesen csak berakjuk a feltárt utakat
                del lehetseges_lepesek[kulcs] # ezt az utat tovább feltártuk, ezt a feltáratlan változatot töröljük

        #A feltárt utakhoz távot és heurisztikus távot adunk
        for lepesek in lehetseges_lepesek:
            tav = 0
            for i in range(len(lepesek)-1):
                aktualis_varosok_tav=get_tavolsag(lepesek[i],lepesek[i+1],pos)
                tav += aktualis_varosok_tav
                #print(f"TÁV-ELLENŐRZÉS: {lepesek[i]} - {lepesek[i+1]} : {aktualis_varosok_tav}")
            heur_tav = get_tavolsag(lepesek[-1],end_city,pos)
            lehetseges_lepesek[lepesek]=tav+heur_tav
            print(f"{lepesek} - {(tav+heur_tav):.2f}")

        #Kiválasztjuk a legjobb opciót
        kovetkezo_varos =  min(lehetseges_lepesek, key=lehetseges_lepesek.get)[-1]
        print(f"LÉPÉS {kovetkezo_varos}-ra/re")
        megtett_tav += get_tavolsag(start_city,kovetkezo_varos,pos)
        start_city = kovetkezo_varos
        bejart_varosok.append(start_city)

        #Ha célba értünk válasszuk ki a legjobb opciót
        if start_city == end_city:
            is_finished = True
            legjobb_utvonal = min(lehetseges_lepesek, key=lehetseges_lepesek.get)
            print("CELBA ERVE")
            print(f"Legjobb utvonal: {legjobb_utvonal}")
    return legjobb_utvonal


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
