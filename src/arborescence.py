import csv
import os
import shutil
import requests
from datetime import date
from dateutil import parser
import re

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.fio import request_kingdom
from utils.misc import rename_other_directories

# Dictionnaire des Kingdoms et de leur fichier (NC)
kingdoms_file = {
    "eukaryota": "eukaryota.txt",
    "bacteria": "bacteria.txt",
    "viruses": "viruses.txt",
    "archaea": "archaea.txt"
}


# Récupération des fichiers contenant la liste des séquences NC pour chaque Kingdom
def write_kingdom_files():
    for kingdom in kingdoms_file.keys():
        request_kingdom(kingdom)


# Renvoie un booléen, True s'il faut mettre l'arbre à jour, False sinon
def update():
    request = requests.get("https://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/overview.txt")

    with open("overview.txt", "wb") as f:
        f.write(request.content)
    # On récupère la date de la dernière modification de la liste des organismes de la base de données
    last_modified = parser.parse(request.headers["last-modified"])

    # On récupère la date de notre arborescence
    try:
        with open(".date", "r") as f:
            tree_date = f.read()
    except FileNotFoundError:
        return True

    return last_modified.date() > parser.parse(tree_date).date()


# Fonction principale de création de l'arborescence
def get_tree():
    global kingdoms_file

    if update():
        print("Création de l'arborescence")
        # Mise à jour de la date de notre arborescence
        with open(".date", "wb") as f:
            f.write(str(date.today()).encode('utf-8'))
        write_kingdom_files()
        kingdom_nc = {}

        # Pour chaque royaume on récupère le nom des organismes (row[5]) ayant au moins une séquence NC
        for kingdom, filename in kingdoms_file.items():
            with open(filename, "r") as file:
                reader = csv.reader(file, delimiter="\t")
                kingdom_nc[kingdom] = [row[5] for row in reader]

        # On supprime l'arborescence (si elle existe) pour ne pas laisser d'organisme qui n'existe plus
        try:
            shutil.rmtree('Results')
        except FileNotFoundError:
            pass

        # Pour tout organisme dans le fichier overview, s'il contient un NC, on l'ajoute à notre arborescence
        with open("overview.txt", "r") as overview_file:
            file = csv.reader(overview_file, delimiter="\t")
            for row in file:
                if len(row) < 4:
                    print("La ligne ", row, "ne contient pas assez d'infos")
                    continue
                organism, kingdom, group, subgroup = row[0], row[1], row[2], row[3]
                for k, v in kingdom_nc.items():
                    if organism in v:
                        # Path Result/Kingdom/Group/Subgroup/Organism
                        organism = re.sub(r'[<>:"/\\|?*]', '-', organism) #supprime les caractères interdit sur Windows
                        directory = os.path.join("Results", kingdom, group, subgroup, organism)
                        os.makedirs(directory, exist_ok=True)

        # On renomme tous les dossiers 'Other' car ils ne sont pas uniques et sont confondus dans l'interface
        rename_other_directories()

get_tree()