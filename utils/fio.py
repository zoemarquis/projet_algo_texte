import requests


def request_kingdom(kingdom):
    request = requests.get("https://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/IDS/" + kingdom[0].upper() + kingdom[1:] + ".ids")
    with open(kingdom + ".txt", "wb") as f:
        f.write(request.content)
