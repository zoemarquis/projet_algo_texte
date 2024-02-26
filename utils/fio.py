import requests


def request_kingdom(kingdom):
    request = requests.get("https://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/IDS/" + kingdom + ".ids")
    with open(kingdom + ".txt", "wb") as f:
        f.write(request.content)
