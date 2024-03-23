import os
"""
from utils.fio import get_ids

def path_to_ids(path):
    kingdom, _, organism = path.split('/')
    ids = get_ids(organism, kingdom)
    return ids
"""

def get_leaf_directories(path):
    leaf_dirs = []

    for dirpath, dirnames, filenames in os.walk(path):
        if not dirnames:
            leaf_dirs.append(dirpath)

    return leaf_dirs
