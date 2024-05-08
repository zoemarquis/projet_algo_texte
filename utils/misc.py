import os
from unidecode import unidecode

from utils.fio import get_ids

def path_to_ids(path):
    organism = os.path.basename(path)
    kingdom = path.split(os.sep)[0]
    ids = get_ids(organism, kingdom)
    return ids

def get_leaf_directories(path):
    leaf_dirs = []

    for dirpath, dirnames, filenames in os.walk(path):
        if not dirnames:
            leaf_dirs.append(dirpath)

    return leaf_dirs


def generate_join_string(bornes):
    join_string = ""

    start = bornes[0]
    end = bornes[1]

    if join_string:
        join_string += ", "

    if start == end:
        join_string += str(start)
    else:
        join_string += f"{start}..{end}"

    return join_string


def remove_accents_and_lowercase(text):
    text_without_accents = unidecode(text)
    lowercase_text = text_without_accents.lower()
    return lowercase_text
