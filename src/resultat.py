from utils.fio import get_nc
from utils.misc import generate_join_string
import os

"""
fichier : Region_Organisme_NC.txt
Contenu : 
            Region Organisme NC : bornes
            séquence
"""

logger = None

def generate_string(region, organism, nc, bornes, seq):
    min_val, max_val = bornes
    return f"{region} {organism} {nc}: {min_val}..{max_val}\n{seq}"

def generate_string_complement(region, organism, nc, bornes, seq):
    min_val, max_val = bornes
    return f"{region} {organism} {nc}: complement({min_val}..{max_val})\n{seq}"

def generate_string_complement_join(region, organism, nc, bornes, seq, intron, cmp, index):
    join_string = generate_join_string(bornes)
    result = f"{region} {organism} {nc}: complement(join({join_string}))\n{seq}"
    if intron:
        result = f"{region} {organism} {nc}: complement(join({join_string})) Intron {cmp}\n{seq[cmp-1]}"
    else:
        result = f"{region} {organism} {nc}: complement(join({join_string})) Exon {cmp}\n{seq[cmp-1]}"
    return result

def generate_string_join(region, organism, nc, bornes, intron, seq, cmp, index):
    join_string = generate_join_string(bornes)
    result = f"{region} {organism} {nc}: join({join_string})\n{seq}"
    if intron:
        result = f"{region} {organism} {nc}: join({join_string}) Intron {cmp}\n{seq[cmp-1]}"
    else:
        result = f"{region} {organism} {nc}: join({join_string}) Exon {cmp}\n{seq[cmp-1]}"
    return result

def result_to_file(file_path, content):
    with open('Results' + os.sep + file_path, 'a') as f:
        if f.tell() > 0:
            f.write('\n')
        f.write(content)

def create_result(path, region, bornes, seq, nc, operation, nb_intron, bornes_intron, log, seq_intron=None):
    global logger
    logger = log

    try:
        if region == 'CDS':
            if isinstance(seq, list):
                if operation == 'complement join':
                    seq = seq[::-1]
                if seq[0][:3] not in {'ATG', 'CTG', 'TTG', 'GTG', 'ATA', 'ATC', 'ATT', 'TTA'}:
                    logger.write(f'Analysis Error : Illegal Start CDS {seq[0][:3]}')
                    return 0
            else:
                if seq[:3] not in {'ATG', 'CTG', 'TTG', 'GTG', 'ATA', 'ATC', 'ATT', 'TTA'}:
                    logger.write(f'Analysis Error : Illegal Start CDS {seq[:3]}')
                    return 0
    except:
        return 0

    organism = path.split(os.sep)[-1]
    file_path = f"{path}{os.sep}{region}_{organism}_{nc}.txt"
    intron_path = f"{path}{os.sep}intron_{organism}_{nc}.txt"
    content = ''
    match operation:
        case 'join':
            content = create_result_join(file_path, intron_path, nb_intron, organism, nc, region, bornes, seq, bornes_intron, seq_intron)
        case 'complement':
            content = generate_string_complement(region, organism, nc, bornes, seq)
        case 'complement join':
            content = create_result_complement_join(file_path, intron_path, nb_intron, organism, nc, region, bornes, seq, bornes_intron, seq_intron)
        case None:
            content = generate_string(region, organism, nc, bornes, seq)
    if content != None:
        result_to_file(file_path, content)

def create_result_join(file_path, intron_path, nb, organism, nc, region, bornes, seq, bornes_intron, seq_intron):


    cmp = 0
    if nb == 0:
        for i in range(len(bornes)):
            content = generate_string_join(region, organism, nc, bornes, False, seq, i + 1, cmp)
            result_to_file(file_path, content)
            cmp += 1
    else:
        for i in range(1, nb + 1):
            content = generate_string_join(f"{region}", organism, nc, bornes, False, seq, i, cmp)
            result_to_file(file_path, content)
            cmp += 1

            content = generate_string_join(f"intron", organism, nc, bornes, True, seq_intron, i, cmp)
            result_to_file(intron_path, content)
            cmp += 1
        return generate_string_join(region, organism, nc, bornes, False, seq, nb + 1, cmp)

def create_result_complement_join(file_path, intron_path, nb, organism, nc, region, bornes, seq, bornes_intron, seq_intron):

    bornes = [(a, b) for a, b in reversed(bornes)]
    
    cmp = 0
    if nb == 0:
        for i in range(len(bornes)):
            content = generate_string_complement_join(region, organism, nc, bornes, seq, False, i + 1, cmp)
            result_to_file(file_path, content)
            cmp += 1
    else:
        for i in range(1, nb + 1):
            content = generate_string_complement_join(f"{region}", organism, nc, bornes, seq, False, i, cmp)
            result_to_file(file_path, content)
            cmp += 1

            content = generate_string_complement_join(f"intron", organism, nc, bornes, seq_intron, True, i, cmp)
            result_to_file(intron_path, content)
            cmp += 1
        return generate_string_complement_join(region, organism, nc, bornes, seq, False, nb + 1, cmp)
