from Bio import Entrez, SeqIO

Entrez.email = "martin.deniau@etu.unistra.fr"

handle = Entrez.esearch(db="nucleotide", term="NC", retmax ="1", usehistory='y', idtype="acc")
record = Entrez.read(handle)

print("Records found:", record["IdList"])

handle_fetch = Entrez.efetch(db="nucleotide", id=record["IdList"], rettype="gbwithparts", retmode="text")
record_fetch = SeqIO.read(handle_fetch, "genbank")
#handle_fetch = Entrez.efetch(db="nuccore", id=record["IdList"], rettype="fasta")
#record_fetch = SeqIO.read(handle_fetch, "fasta")
#print(record_fetch)
print(record_fetch.seq)