import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from sequence import fetch_all_sequence

import threading

import tkinter as tk
from tkinter import ttk

import theme


class ProgressBar:
    def __init__(self, frame_parent, fenetre, grid_row, grid_column, folder_tree, regions):
        self.folder_tree = folder_tree
        self.regions=regions
        self.progress_running = False
        self.length = 100 #valeur par défaut
        self.pas = 1 #valeur par défaut
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

    def update_progress(self):
        current_value = self.loadbar["value"]
        print("current_value: ", current_value)
        if current_value + self.length/self.pas <= self.length:
            self.loadbar["value"] += self.length/self.pas
            self.fenetre.update_idletasks()
        if current_value + self.length/self.pas == self.length:
            self.toggle_progress()
        
    def commands(self):
        self.toggle_progress()
        if self.progress_running:
            threading.Thread(target=self.start_fetch).start()

    def start_fetch(self):
        selected_folders = self.folder_tree.get_selected_paths()
        selected_regions = self.regions.get_selected_regions()
        fetch_all_sequence(selected_folders, selected_regions, self)

    def toggle_progress(self):
        self.progress_running = not self.progress_running
        self.bouton.config(text="Stop" if self.progress_running else "Start")
        if not self.progress_running:
            self.loadbar["value"] = 0
            #self.toggle_progress()

    def set_pas(self, new_pas):
        self.pas = new_pas
    
    
    '''
    # à placer dans theme plutot ?
    def change_cursor(self, event):
        event.widget.config(cursor="hand2")  # Change le curseur en main pointant
    '''


    '''

    pb.bouton.config(command=start_fetch)'''
    