import csv
import requests

request = requests.get("https://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/overview.txt")

set_kingdom = {}
#On sauvegarde le fichier overview.txt

with open("overview.txt", "wb") as f:
    f.write(request.content)

# On lit le fichier pour récupérer l'arborescence
with open("overview.txt", "r") as overview_file:
    file = csv.reader(overview_file, delimiter="\t")
    next(file)
    for row in file:
        kingdom, group, subgroup = row[1], row[2], row[3]
        # On cherche l'unicité des éléments, set_kingdom est un dictionnaire dont les valeurs sont des dictionnaires (groups)
        set_kingdom.setdefault(kingdom, {})
        # Même chose avec les groupes, qui auront comme valeur un set de sous-groupes
        set_kingdom[kingdom].setdefault(group, set())
        set_kingdom[kingdom][group].add(subgroup)

# Affichage (temporaire)
for kingdom, groups in set_kingdom.items():
    print(kingdom)
    for group, subgroups in groups.items():
        print("\t" + group)
        #for subgroup in subgroups:
            #print("\t\t" + subgroup)



