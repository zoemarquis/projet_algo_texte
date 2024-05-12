import requests
import csv
import os

def request_kingdom(kingdom):
    request = requests.get("https://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/IDS/" + kingdom[0].upper() + kingdom[1:] + ".ids")
    with open(kingdom + ".txt", "wb") as f:
        f.write(request.content)

def get_path_from_organism(organismRecherche):
    
    with open("overview.txt", "r") as overview_file:
        file = csv.reader(overview_file, delimiter="\t")
        for row in file:
            organism, kingdom, group, subgroup = row[0], row[1], row[2], row[3]
            if organismRecherche == organism:
                return os.path.join("Results", kingdom, group, subgroup, organism) #f"Results/{kingdom}/{group}/{subgroup}/{organism}"

def get_ids(organismRecherche, kingdom):
    listeIds = []
    #On cherche 
    #Organism c'est row[5], on cherche ids qui est row[2] 
    with open(f"{kingdom.lower()}.txt", "r") as overview_file:
        file = csv.reader(overview_file, delimiter="\t")
        for row in file:
            organism, ids = row[5], row[2]
            if organismRecherche == organism:
                listeIds.append(ids)

    return listeIds

def get_nc(id_, kingdom):
    #On cherche 
    #Organism c'est row[5], on cherche ids qui est row[2] 
    with open(f"{kingdom.lower()}.txt", "r") as overview_file:
        file = csv.reader(overview_file, delimiter="\t")
        for row in file:
            id, nc = row[2], row[1]
            if id == str(id_):
                return nc

    return None

def load_processed_info(file_path=".processed_info.txt"):
    processed_info = set()
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            for line in file:
                id, region = line.strip().split(",")
                processed_info.add((id, region))
    return processed_info

def save_processed_info(processed_info, file_path=".processed_info.txt"):
    with open(file_path, "a") as file:
        id, region = processed_info
        file.write(f"{id},{region}\n")