"""
fichier : Region_Organisme_NC.txt
Contenu : 
            Region Organisme NC : bornes
            séquence
"""


def generate_string(region, organism, nc, bornes, seq):
    min_val, max_val = bornes
    string = f"{region} {organism} {nc}: {min_val}..{max_val}\n{seq}"
    return string

def create_result(path, region, nc, bornes, seq):
    organism = path.split('/')[-1]
    file_path = f"{path}/{region}_{organism}_{nc}.txt"
    with open(file_path, 'w') as f:
        f.write(generate_string(region, organism, nc, bornes, seq))
