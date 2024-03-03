#Lancer depuis le dossier src

import threading
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'src')) 
import sequence

sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 
import utils.fio


def get_ids(category, kingdom):
    if kingdom == "viruses":
        return utils.fio.get_ids(category, "viruses")
    elif kingdom == "bacteria":
        return utils.fio.get_ids(category, "bacteria")
    else:
        return []
    
#ids premiers viruses
kingdom = ["viruses","bacteria"]
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


all_ids = ids_viruses + ids_bacteria

# Nombre de threads (erreur "Too many request" si > 3)
nb_threads = 3
ids_per_thread = len(all_ids) // nb_threads
def fetch(ids, regions):
    for id in ids:
        print("Fetching sequence", id)
        handle = Entrez.efetch(db="nucleotide", id=id, rettype="gbwithparts", retmode="text")
        print("Fetched")
        for record in SeqIO.parse(handle, "gb"):
            for feature in record.features:
                for region in regions:
                    if feature.type == region:
                        analyse.analyse_bornes(str(feature.location), len(record.seq))

# partage ids entre les threads
thread_ids = [all_ids[i:i + ids_per_thread] for i in range(0, len(all_ids), ids_per_thread)]


threads = []
for ids in thread_ids:
    thread = threading.Thread(target=sequence.fetch, args=(ids, ["cds", "exon"]))
    thread.start()
    threads.append(thread)


for thread in threads:
    thread.join()

print("Tous les threads ont terminé.")



















identifiants = []
regions = []



'''
id_bacteria_1 = utils.fio.get_ids("'Brassica napus' phytoplasma","bacteria")
id_bacteria_2 = utils.fio.get_ids("'Nostoc azollae' 0708","bacteria")
id_bacteria_3 = utils.fio.get_ids("'Rehmannia glutinosa' phytoplasma","bacteria")
id_bacteria_4 = utils.fio.get_ids("Acaryochloris marina MBIC11017","bacteria")
id_bacteria_5 = utils.fio.get_ids("Acetivibrio clariflavus DSM 19732","bacteria")
'''


'''
id_viruses_1 = utils.fio.get_ids("Abaca bunchy top virus","viruses")
print (id_viruses_1)
id_viruses_2 = utils.fio.get_ids("Abalone herpesvirus Victoria/AUS/2009","viruses")
print (id_viruses_2)
id_viruses_3 = utils.fio.get_ids("Abalone shriveling syndrome-associated virus","viruses")
id_viruses_4 = utils.fio.get_ids("Abelson murine leukemia virus","viruses")
id_viruses_5 = utils.fio.get_ids("Abutilon Brazil virus","viruses")
'''

