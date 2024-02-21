import csv
import os
import requests
from datetime import date
from dateutil import parser

# Date de notre arborescence
tree_date = None

# Dictionnaire des Kingdoms et de leur fichier (NC)
kingdoms_file = {
    "eukaryota": "eukaryota.txt",
    "bacteria": "bacteria.txt",
    "viruses": "viruses.txt",
    "archaea": "archaea.txt"
}


# Récupération des fichiers contenant la liste des séquences NC pour chaque Kingdom
def write_tree_files():
    global tree_date

    request = requests.get("https://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/IDS/Eukaryota.ids")
    with open("eukaryota.txt", "wb") as f:
        f.write(request.content)
    request = requests.get("https://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/IDS/Bacteria.ids")
    with open("bacteria.txt", "wb") as f:
        f.write(request.content)
    request = requests.get("https://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/IDS/Viruses.ids")
    with open("viruses.txt", "wb") as f:
        f.write(request.content)
    request = requests.get("https://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/IDS/Archaea.ids")
    with open("archaea.txt", "wb") as f:
        f.write(request.content)


# Renvoie un booléen, True s'il faut mettre l'arbre à jour, False sinon
def update():
    request = requests.get("https://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/overview.txt")
    with open("overview.txt", "wb") as f:
        f.write(request.content)
    last_modified = parser.parse(request.headers["last-modified"])
    return tree_date is None or last_modified > tree_date


# Fonction principale de création de l'arborescence
def get_tree():
    global kingdoms_file, tree_date
    if update():
        # Mise à jour de la date de notre arborescence si mise à jour
        tree_date = date.today()
        write_tree_files()
        kingdom_nc = {}
        # Pour chaque royaume on récupère le nom des organismes (row[5]) ayant une séquence NC
        for kingdom, filename in kingdoms_file.items():
            with open(filename, "r") as file:
                reader = csv.reader(file, delimiter="\t")
                kingdom_nc[kingdom] = [row[5] for row in reader]

        # Pour tout organisme dans le fichier overview, s'il contient un NC, on l'ajoute à notre arborescence
        with open("overview.txt", "r") as overview_file:
            file = csv.reader(overview_file, delimiter="\t")
            for row in file:
                organism, kingdom, group, subgroup = row[0], row[1], row[2], row[3]
                for k, v in kingdom_nc.items():
                    if organism in v:
                        # Path Result/Kingdom/Group/Subgroup/Organism
                        directory = os.path.join("Results", kingdom, group, subgroup, organism)
                        os.makedirs(directory, exist_ok=True)