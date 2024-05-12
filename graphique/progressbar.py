import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from sequence import fetch_all_sequence

import threading

import tkinter as tk
from tkinter import ttk

import theme


class ProgressBar:
    def __init__(self, frame_parent, fenetre, grid_row, grid_column, folder_tree, regions, log):
        
        self.length = 100 #valeur par défaut
        self.nb_paths_a_traiter = 1 #valeur par défaut
        self.paths_traite = 0 #valeur par défaut

        self.folder_tree = folder_tree
        self.regions=regions
        self.log=log

        self.progress_running = False
        self.active_threads = []
        self.stop_fetching = threading.Event() 
        
        self.loadbar = ttk.Progressbar(
            frame_parent,
            orient="horizontal",
            mode="determinate",
            length=self.length,
            style="Custom.Horizontal.TProgressbar",
        )

        self.loadbar.grid(row=grid_row, column=grid_column, sticky="ewns", pady=(0, 20))
        self.fenetre = fenetre

        # bouton start / stop
        self.bouton = ttk.Button(
            frame_parent,
            text="Start",
            command=self.commands,
            style="Custom.TButton",
        )
        self.bouton.grid(row=grid_row + 1, column=grid_column)
       # self.bouton.bind("<Enter>", self.change_cursor)
       
    # Mise à jour de la barre de progression
    def update_progress(self):
        if self.stop_fetching.is_set():  
            return
        # Augmentation
        if self.paths_traite + 1 < self.nb_paths_a_traiter:
            self.paths_traite +=1
            self.loadbar["value"] += self.length/self.nb_paths_a_traiter
            self.fenetre.update_idletasks()
        #Remise à 0
        if self.paths_traite + 1 == self.nb_paths_a_traiter:
            self.toggle_progress()
    
    #Exécutée lors d'un clique sur le bouton
    def commands(self):
        self.toggle_progress()
        if self.progress_running:
            threading.Thread(target=self.start_fetch).start()
        else:
            self.log.write("Arrêt volontaire du fetching")

    #Démarrage du thread principale de fetching
    def start_fetch(self):
        selected_folders = self.folder_tree.get_selected_paths()
        selected_regions = self.regions.get_selected_regions()
        fetch_thread = threading.Thread(target=self.fetch_wrapper, args=(selected_folders, selected_regions))
        fetch_thread.start()
        self.active_threads.append(fetch_thread)

    def fetch_wrapper(self, selected_folders, selected_regions):
        fetch_all_sequence(selected_folders, selected_regions, self)

    #Changement de l'état du bouton
    def toggle_progress(self):
        #Inversion
        self.progress_running = not self.progress_running
        self.bouton.config(text="Stop" if self.progress_running else "Start")
        #Si stop : remise à 0
        if not self.progress_running:
            self.loadbar["value"] = 0
            self.paths_traite = 0
            self.stop_fetching.set()
        # Sinon activation du fetch
        else:
            self.stop_fetching.clear()

    #Mise à jour du nombre de fichiers à fetch
    def set_nb_paths_a_traiter(self, new_nb_paths_a_traiter):
        self.nb_paths_a_traiter = new_nb_paths_a_traiter


    '''
    # à placer dans theme plutot ?
    def change_cursor(self, event):
        event.widget.config(cursor="hand2")  # Change le curseur en main pointant
    '''


    '''

    pb.bouton.config(command=start_fetch)'''
    