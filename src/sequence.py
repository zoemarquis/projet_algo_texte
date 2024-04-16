import os
import sys

from Bio import Entrez, SeqIO
from concurrent.futures import ThreadPoolExecutor

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import src.analyse
from utils.fio import get_nc
from utils.misc import get_leaf_directories, path_to_ids

"""
def search(domain, name):
    Entrez.email = "martin.deniau@etu.unistra.fr"

    handle = Entrez.esearch(db="nucleotide", term="("+name+"["+domain+"]"+") AND (NC_*[Accession])", retmax ="9999")

    record = Entrez.read(handle)

    print("Records found:", record["IdList"])

    return record["IdList"]

"""

def fetch(path, ids, regions):
    Entrez.email = "martin.deniau@etu.unistra.fr"
    for id in ids:
        print("Fetching sequence", id)
        handle = Entrez.efetch(db="nucleotide", id=id, rettype="gbwithparts", retmode="text")
        print("Fetched")
        for record in SeqIO.parse(handle, "gb"):
            for feature in record.features:
                for region in regions:
                    if feature.type == region:                            
                        kingdom = path.split(os.sep)[0]
                        src.analyse.analyse_bornes(str(feature.location), record.seq, False, path, region, get_nc(id, kingdom))



def fetch_all_sequence(paths, regions):
    all_paths = [] #sous chemin de tous les dossiers selectionnes

    for path in paths:
        base_path = "Results" + os.sep #chemin jusqu'à l'arborescence
        leaf_dirs = get_leaf_directories(base_path + path)
        relative_paths = [os.path.relpath(leaf_dir, base_path) for leaf_dir in leaf_dirs]
        all_paths.extend(relative_paths)

    print(all_paths)
    '''
    Version sans les threads
    for path in all_paths:
        ids = path_to_ids(path)
        print(ids)
        # Fetch avec le path global et les IDs
        fetch(path, ids, regions)'''

    # Threads
    def process_path(path):
        ids = path_to_ids(path)
        fetch(path, ids, regions)

    with ThreadPoolExecutor() as executor:
        executor.map(process_path, all_paths)


#A récupérer de l'interface
paths_interface = ["Archaea"+ os.sep + "Candidatus_Thermoplasmatota", "Eukaryota"]
regions_interface = ["3'UTR", "CDS", "rRNA"]

fetch_all_sequence(paths_interface, regions_interface)

