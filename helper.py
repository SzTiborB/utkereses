szotar = {
    "Alma": 30,
    "Körte": 12,
    "Hagyma": 13
}

nev = "Rohod"
tav = 11
print(min(szotar))

szotar[nev]=tav
print(szotar)

nev=min(szotar, key=szotar.get)
print(nev)