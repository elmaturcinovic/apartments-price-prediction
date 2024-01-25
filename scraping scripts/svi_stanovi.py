# Ova skripta služi kako bi se .csv fajlovi sa scrape-anim podacima iz oglasa spojili u jedan dataset.
# Razlog zbog kojeg su podaci scrape-ani u dijelovima je sljedeći:
# - svaka stranica(page) sadrži najviše 40 oglasa
# - maksimalan broj stranica koje će se prikazati u dijelu za navigaciju na dnu stranice je 50

# To znači da, ma koliko imali oglasa od interesa, imat ćemo priliku vidjeti najviše 2000 oglasa.
# Uzet je filter prema stanju stanova (mogao se koristiti bilo koji čijim korištenjem bi se izbjeglo ponavljanje 
# istih podataka), i na osnovu mogućih vrijednosti atributa Stanje("namješten", "nenamješten" i "polunamješten"),
# dataset je inicjalno bio podijeljen na tri dijela, koji će u ovoj dijelu bili objedinjeni.

import pandas as pd

# Putanje pojedinačnih fajlova
file_paths = ['stanovi_namjesteni.csv', 'stanovi_nenamjesteni.csv', 'stanovi_polunamjesteni.csv']

# Inicijalizacija DataFrame-a u koji će sadržavati objedinjene sve podatke
merged_data = pd.DataFrame()

# Iteriramo kroz putanje pojedinačnih fajlova
for file_path in file_paths:
    # Čitanje .csv fajla
    df = pd.read_csv(file_path)
    
    # Append-anje podataka u merged_data DataFrame
    merged_data = merged_data.append(df, ignore_index=True)

# Eksportovanje novodobijenog DataFrame-a u .csv fajl
merged_data.to_csv('svi_stanovi.csv', index=False)

print("Files merged successfully!")
