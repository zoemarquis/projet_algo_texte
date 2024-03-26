from utils.fio import get_nc
from utils.misc import generate_join_string

"""
fichier : Region_Organisme_NC.txt
Contenu : 
            Region Organisme NC : bornes
            séquence
"""


def generate_string(region, organism, nc, bornes, seq):
    min_val, max_val = bornes
    return f"{region} {organism} {nc}: {min_val}..{max_val}\n{seq}"


def generate_string_complement(region, organism, nc, bornes, seq):
    min_val, max_val = bornes
    return f"{region} {organism} {nc}: complement({min_val}..{max_val})\n{seq}"


def generate_string_complement_join(region, organism, nc, bornes, seq, cmp):
    join_string = generate_join_string(bornes)
    result = f"{region} {organism} {nc}: complement(join({join_string}))\n{seq}"
    if region in ['exon', 'intron']:
        result = f"{region} {organism} {nc}: complement(join({join_string})) {region[0].upper()}{region[1:]} {cmp}\n{seq}"
    return result


def generate_string_join(region, organism, nc, bornes, seq, cmp):
    join_string = generate_join_string(bornes)
    result = f"{region} {organism} {nc}: join({join_string})\n{seq}"
    if region in ['exon', 'intron']:
        result = f"{region} {organism} {nc}: join({join_string}) {region[0].upper()}{region[1:]} {cmp}\n{seq}"
    return result


def result_to_file(file_path, content):
    with open(file_path, 'a') as f:
        if f.tell() > 0:
            f.write('\n\n')
        f.write(content)


def create_result(path, region, bornes, seq, nc, operation, nb_intron, bornes_intron):
    organism = path.split('/')[-1]
    file_path = f"{path}/{region}_{organism}_{nc}.txt"
    content = ''
    match operation:
        case 'join':
            #create_result_join(file_path, nb_intron, organism, nc, bornes, seq, bornes_intron)
            pass
        case 'complement':
            content = generate_string_complement(region, organism, nc, bornes, seq)
        case 'complement join':
            #create_result_complement_join(file_path, nb_intron, organism, nc, bornes, seq, bornes_intron)
            pass
        case None:
            content = generate_string(region, organism, nc, bornes, seq)
    result_to_file(file_path, content)


def create_result_join(file_path, nb, organism, nc, bornes, seq, bornes_intron):
    for i in range(nb):
        content = generate_string_join('exon', organism, nc, bornes_intron[i-1], seq, i)
        result_to_file(file_path, content)
        content = generate_string_join('intron', organism, nc, bornes[i-1], seq, i)
        result_to_file(file_path, content)

def create_result_complement_join(file_path, nb, organism, nc, bornes, seq, bornes_intron):
    for i in range(nb):
        content = generate_string_complement_join('exon', organism, nc, bornes_intron[i-1], seq, i)
        result_to_file(file_path, content)
        content = generate_string_complement_join('intron', organism, nc, bornes[i-1], seq, i)
        result_to_file(file_path, content)
        