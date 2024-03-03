from Bio import Entrez, SeqIO
import analyse

import threading


def search(domain, name):
    Entrez.email = "martin.deniau@etu.unistra.fr"

    handle = Entrez.esearch(db="nucleotide", term="("+name+"["+domain+"]"+") AND (NC_*[Accession])", retmax ="9999")

    record = Entrez.read(handle)

    print("Records found:", record["IdList"])

    return record["IdList"]


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
