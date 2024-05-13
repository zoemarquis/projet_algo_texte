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

def rename_other_directories():
    directories_to_rename = []
    cmp_other = 1

    # Traversing through the directory tree and collecting directories named 'Other'
    for root, dirs, files in os.walk("Results"):
        for directory in dirs:
            if directory == "Other":
                directories_to_rename.append(os.path.join(root, directory))

    # Renaming collected directories
    for old_path in directories_to_rename[::-1]:
        new_path = f'{old_path}{cmp_other}'
        os.rename(old_path, new_path)
        cmp_other += 1
