import csv
import requests
import os
import traceback

request = requests.get("https://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/overview.txt")

set_kingdom = {}
path_arborescence = "Arborescence_GenBank/"
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

generation_dossier = False;
generation_group = False;

# Est ce qu'on met tous les dossiers dans un sous dossier??
# Si oui il faut voir comment l'implementer.
# Fait ici mais a voir pour la maj
if not os.path.exists(path_arborescence):
    os.mkdir(path_arborescence)

# Affichage (temporaire)
for kingdom, groups in set_kingdom.items():
    if not os.path.exists(path_arborescence + kingdom):
        # Simplement pour un affichage visuel qu'on cree l'arborescence
        if not generation_dossier:
            print(f"\033[92mGeneration de l'arborescence...\033[0m")
            generation_dossier = True

        try:
            os.mkdir(path_arborescence + kingdom)
        except OSError as e:
            print(f"Erreur lors de la creation du dossier '{kingdom}': {e}")

        # Affichage du dossier a generer
        print(f"Generation du dossier '{path_arborescence + kingdom}' ...done !")

    # else:
        # A voir pour la mise a jour des dossiers/fichiers ensuite
        # print(f"Le dossier '{path_arborescence + kingdom}' existe deja")

    # Generation et affichage des groupes
    for group, subgroups in groups.items():
        path_group = path_arborescence + os.path.join(kingdom, group)
        path_group = path_group.replace(" ", "_")
        if not os.path.exists(path_group):
            if not generation_dossier:
                print(f"\033[92mGeneration de l'arborescence...\033[0m")
                generation_dossier = True
            if not generation_group:
                print(f"\t\033[92mGeneration (partielle ou complete) des groupes de '{kingdom}'...\033[0m")
                generation_group = True

            # print(path_arborescence +  os.path.join(kingdom, group))
            try:
                os.mkdir(path_group)
            except OSError as e:
                traceback.print_exc()
                print(f"Erreur lors de la creation du groupe '{group}': {e}")

            # Affichage du dossier a generer
            # print(f"Generation du dossier '{group}' ...done !")

        # else:
            # print(f"Groupe existe deja '{path_group}' ")

        # Generation et affichage des sous-groupes
        # for subgroup in subgroups:
        #     print("\t\t" + subgroup)


    if generation_group:
        print(f"--\033[92mFin de la generation des groupes de '{kingdom}'\033[0m")
        generation_group = False

if generation_dossier:
    print("\033[92mFin de la generation de l'arborescence.\033[0m")




