import os
import sys
import time

from Bio import Entrez, SeqIO
#from concurrent.futures import ThreadPoolExecutor

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import src.analyse
from utils.fio import get_nc, save_processed_info, load_processed_info
from utils.misc import get_leaf_directories, path_to_ids, remove_accents_and_lowercase

import threading
from queue import Queue
path_queue = Queue()

emails = ["martin.deniau@etu.unistra.fr", "deniau.martin@gmail.com"]

def fetch(path, ids, regions, progress_bar, email):
    Entrez.email = email
    
    # Trace des séquences et régions traitées (pour optimisation)
    processed_info = load_processed_info()

    create_intron = False

    if 'Intron' in regions:
        create_intron = True
        regions.remove('Intron')

    for id in ids:
        if progress_bar.stop_fetching.is_set():
            return

        for region in regions:
            # Si la séquence a déjà été traitée pour cette région, on ignore
            if (id, region) in processed_info:
                progress_bar.log.write(f"Skipping already processed ID {id} for region {region}")
                continue

            progress_bar.log.write(f"Fetching sequence {id}")
            handle = None
            try:
                handle = Entrez.efetch(db="nucleotide", id=id, rettype="gbwithparts", retmode="text", timeout=10)
                for record in SeqIO.parse(handle, "gb"):
                    for feature in record.features:
                        if remove_accents_and_lowercase(feature.type) == remove_accents_and_lowercase(region):
                            if progress_bar.stop_fetching.is_set():
                                return
                            kingdom = path.split(os.sep)[0]
                            src.analyse.analyse_bornes(str(feature.location), record.seq, create_intron, path, feature.type, get_nc(id, kingdom), progress_bar.log)
                progress_bar.log.write(f"Fetched sequence {id}")
            except Exception as e:
                progress_bar.log.write(f"Erreur lors de la récupération: {e}")
            finally:
                if handle is not None:
                    handle.close()
                # On inscrit la séquence comme traitée pour cette région
            save_processed_info((id, region))


def fetch_all_sequence(paths, regions, progress_bar):
    global path_queue

    all_paths = []

    if paths and regions:
        progress_bar.log.write("Démarrage du fetching")

        #recupération du nombre de chemins pour initialiser la barre de progression
        for path in paths:
            base_path = "Results" + os.sep
            leaf_dirs = get_leaf_directories(base_path + path)
            relative_paths = [os.path.relpath(leaf_dir, base_path) for leaf_dir in leaf_dirs]
            all_paths.extend(relative_paths)
        
        all_paths = list(set(all_paths)) #suppression des doublons

        progress_bar.set_nb_paths_a_traiter(len(all_paths))

        #Ajout des chemins à la liste des chemins à fetch par les threads
        for path in all_paths:
            path_queue.put(path)

        # Lancement des threads (max 4 sinon surcharge du serveur)
        max_threads = 4
        for i in range(max_threads):
            email = emails[i%len(emails)]
            thread = threading.Thread(target=process_paths, args=(regions, progress_bar, email))
            progress_bar.active_threads.append(thread)
            thread.start()

        path_queue.join()

        progress_bar.log.write("Fin du fetching")

    else:
        progress_bar.log.write("Veuillez sélectionner au moins un chemin et une région.")
        progress_bar.toggle_progress()


#Fonction de fetch exécutée par les threads
def process_paths(regions, progress_bar, email):
    if "All" in regions:
        regions.remove("All")
    while not progress_bar.stop_fetching.is_set():
        path = path_queue.get()
        if path is None:  
            break
        ids = path_to_ids(path)
        fetch(path, ids, regions, progress_bar, email)
        path_queue.task_done()
        progress_bar.update_progress()
    
    if progress_bar.stop_fetching.is_set():
        return



