import tkinter as tk
from tkinter import ttk

import theme


class Recap:

    def __init__(self, frame_parent, region, tree):
        self.frame_parent = frame_parent
        self.region = region
        self.tree = tree

        f_arbo = tk.Frame(frame_parent)
        f_arbo.grid(row=0, column=0, sticky="nsew")
        self.canvas_arbo = tk.Canvas(f_arbo, bg="pink")
        self.canvas_arbo.pack(side="right", fill="both", expand=True)
        self.text_recap_arbo = self.canvas_arbo.create_text(
            10, 10, text="Dossier:", fill=theme.couleur_texte, anchor="nw"
        )
        self.scrollbar_arbo = ttk.Scrollbar(
            self.canvas_arbo, orient="vertical", command=self.canvas_arbo.yview
        )
        self.scrollbar_arbo.pack(side="right", fill="y")
        self.canvas_arbo.configure(yscrollcommand=self.scrollbar_arbo.set)

        f_cases = tk.Frame(frame_parent)
        f_cases.grid(row=0, column=1, sticky="nsew")
        self.canvas_regions = tk.Canvas(f_cases, bg="lightblue")
        self.canvas_regions.pack(side="left", fill="both", expand=True)
        self.text_recap_cases = self.canvas_regions.create_text(
            10, 10, text="Régions:", fill=theme.couleur_texte, anchor="nw"
        )
        self.scrollbar_regions = ttk.Scrollbar(
            self.canvas_regions, orient="vertical", command=self.canvas_regions.yview
        )
        self.scrollbar_regions.pack(side="right", fill="y")
        self.canvas_regions.configure(yscrollcommand=self.scrollbar_regions.set)

        bouton_effacer_selection = ttk.Button(
            frame_parent,
            text="TOUT EFFACER",
            command=self.effacer_selection,
            style="Custom.TButton",
        )
        bouton_effacer_selection.grid(
            row=1,
            column=0,
            padx=(300, 300),
            pady=(10, 10),
            sticky="ew",
            columnspan=2,
        )

    def effacer_selection(self):
        self.tree.effacer_selection()
        self.region.effacer_selection()
