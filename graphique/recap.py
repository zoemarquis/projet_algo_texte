import tkinter as tk
from tkinter import ttk

class Recap:

    def __init__(self, frame_parent, region, tree, grid_row, grid_column):
        self.frame_parent = frame_parent
        self.region = region
        self.tree = tree

        f_arbo = tk.Frame(frame_parent)
        f_arbo.grid(row=0, column=0, sticky="nsew")
        self.canvas_arbo = tk.Canvas(f_arbo, bg="pink",height=100, width=100)
        self.canvas_arbo.pack(side="right", fill="both", expand=True)
        self.text_recap_arbo = self.canvas_arbo.create_text(20,20,text="Dossier:", fill="black", anchor="nw")
    
        f_cases = tk.Frame(frame_parent)
        f_cases.grid(row=0, column=1, sticky="nsew")
        self.canvas_regions = tk.Canvas(f_cases, bg="lightblue", height=100, width=100)
        self.canvas_regions.pack(side="left", fill=tk.BOTH, expand=True)
        self.text_recap_cases = self.canvas_regions.create_text(20,20,text="Régions:", fill="black", anchor="nw")
        
        bouton_effacer_selection = ttk.Button(frame_parent, text="TOUT EFFACER", command=self.effacer_selection,style="Custom.TButton")
        bouton_effacer_selection.grid(row=grid_row, column=grid_column,padx=(300,300), pady=(10,10), sticky="ew", columnspan=2)

    def effacer_selection(self):
        self.tree.effacer_selection()
        self.region.effacer_selection()