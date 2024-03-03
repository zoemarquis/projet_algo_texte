#Lancer depuis le dossier src

import threading
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 
import sequence

sys.path.append(os.path.join(os.path.dirname(__file__), '../..')) 
import utils.fio


def get_ids(category, kingdom):
    if kingdom == "viruses":
        return utils.fio.get_ids(category, "viruses")
    elif kingdom == "bacteria":
        return utils.fio.get_ids(category, "bacteria")
    else:
        return []
    
# ids premiers viruses et bacteria
name_viruses = ["Abaca bunchy top virus", 
              "Abalone herpesvirus Victoria/AUS/2009", 
              "Abalone shriveling syndrome-associated virus", 
              "Abelson murine leukemia virus",
              "Abutilon Brazil virus",
              "Abutilon mosaic Bolivia virus",
              "Abutilon mosaic Brazil virus",
              "Abutilon mosaic virus",
              "Acanthamoeba polyphaga mimivirus",
              "Acanthocystis turfacea chlorella virus 1",
              "Acartia tonsa copepod circovirus",
              "Acheta domestica densovirus",
              "Acheta domestica mini ambidensovirus"]

name_bacteria =["'Brassica napus' phytoplasma",
              "'Nostoc azollae' 0708",
              "'Rehmannia glutinosa' phytoplasma",
              "Acaryochloris marina MBIC11017",
              "Acetivibrio clariflavus DSM 19732",
              "Acetivibrio thermocellus",
              "Acetoanaerobium sticklandii",
              "Acetobacter aceti",
              "Acetobacter pasteurianus",
              "Acetobacter pasteurianus 386B",
              "Acetobacter pasteurianus IFO 3283-01",
              "Acetobacter pasteurianus IFO 3283-01-42C"]



ids_viruses = [get_ids(name, "viruses") for name in name_viruses]
ids_bacteria = [get_ids(name, "bacteria") for name in name_bacteria]

#à modifier en fonction de ce que l'on cherche
all_ids = ids_viruses + ids_bacteria

# Nombre de threads (erreur "Too many request" si > 3)
nb_threads = 3
nb_ids_thread = len(all_ids) // nb_threads

# partage ids entre les threads
thread_ids = [all_ids[i:i + nb_ids_thread] for i in range(0, len(all_ids), nb_ids_thread)]


threads = []
for ids in thread_ids:
    thread = threading.Thread(target=sequence.fetch, args=(ids, ["cds", "exon"]))
    thread.start()
    threads.append(thread)


for thread in threads:
    thread.join()

print("Tous les threads ont terminé.")
