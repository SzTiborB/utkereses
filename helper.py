import fuggvenyek as fg
start_city = "varos1"
nem_start_city = "varos_A"
lehetseges_lepesek = {(start_city,):10}
lehetseges_lepesek[(nem_start_city,)]=10
for lepes in lehetseges_lepesek:
    print(lepes)

print("##############")
szomszedok =["varos2","varos3","varos4"]
kulcsok = lehetseges_lepesek.keys()
for kulcs in list(kulcsok):
    if kulcs[-1] == start_city:
        for szomszed in szomszedok:
            lehetseges_lepesek[kulcs+(szomszed,)]=8
        del lehetseges_lepesek[kulcs]
for ut,tav in lehetseges_lepesek.items():
    print(f"{ut} - {tav}")

for i in range(len(lehetseges_lepesek)-1):
    print(i)
