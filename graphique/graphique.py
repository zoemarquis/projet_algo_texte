import os
import tkinter as tk
from tkinter import ttk

import folder
import theme
import log
import credit
import region
import recap
import progressbar


# à mettre dans theme
def change_treeview_colors(treeview, text_color, select_color, background_color):
    style = ttk.Style()
    style.configure(
        "Custom.Treeview",
        foreground=text_color,
        fieldbackground=background_color,
        background=background_color,
    )
    style.map("Custom.Treeview", background=[("selected", select_color)])


if __name__ == "__main__":
    root_dir = "Results"
    folder_structure, dict_path = folder.create_folder_structure(root_dir)

    fenetre = tk.Tk()
    # style = ttk.Style(fenetre)
    fenetre.title("GENBANK PARSER")
    fenetre.geometry("1300x800")
    fenetre.update()
    width = fenetre.winfo_width()
    height = fenetre.winfo_height()

    # FRAME pack pour pouvoir modifier la taille de la fenêtre
    frame_root = tk.Frame(fenetre)
    frame_root.pack(expand=1, fill="both")
    frame_root.rowconfigure(0, weight=1)
    frame_root.rowconfigure(1, weight=10)
    frame_root.columnconfigure(0, weight=1)
    # + utiliser les fonctions pour modifier le theme

    #####################################################################################
    # FRAME titre : contient le texte du titre + le petit i
    frame_titre = tk.Frame(frame_root)
    frame_titre.grid(row=0, column=0, sticky="nsew", padx=30, pady=0)
    frame_titre.rowconfigure(0, weight=1)
    frame_titre.columnconfigure(0, weight=20)
    frame_titre.columnconfigure(1, weight=1)

    # texte titre
    label = tk.Label(
        frame_titre,
        text="Acquisition des régions fonctionnelles dans les génomes",
        font=("Arial", 30),
        fg=theme.couleur_frame,
    )
    label.grid(row=0, column=0, sticky="ew")

    # le petit i : contient nos noms
    credit = credit.Credits(frame_titre, grid_row=0, grid_column=1)

    #####################################################################################
    # FRAME contenant tout sauf titre et petit i : en grille
    frame_principal = tk.Frame(frame_root)
    frame_principal.grid(row=1, column=0, sticky="nsew", padx=30, pady=(10, 20))
    frame_principal.grid_columnconfigure(0, weight=1)
    frame_principal.grid_columnconfigure(1, weight=1)
    frame_principal.grid_rowconfigure(0, weight=1)
    frame_principal.grid_rowconfigure(1, weight=1)

    #####################################################################################
    # à gauche : tous les choix : arborescence + régions

    # FRAME arborescence
    frame_arbo = tk.LabelFrame(
        frame_principal,
        text="Arborescence",
        relief="raised",
        bg=theme.couleur_frame,
        foreground=theme.couleur_texte,
    )
    frame_arbo.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 10))

    # style.configure("Treeview", rowheight=25)
    # style.map("Treeview", background=[('selected', '#347083')])
    folder_tree = folder.FolderTree(frame_arbo, folder_structure, dict_path, recap=None)
    folder_tree.pack(expand=True, fill=tk.BOTH)
    change_treeview_colors(
        folder_tree,
        text_color=theme.couleur_texte,
        select_color="lightblue",
        background_color=theme.couleur_frame,
    )

    # FRAME régions
    frame_cases = tk.LabelFrame(
        frame_principal,
        text="Sélection des régions",
        bg=theme.couleur_frame,
        foreground=theme.couleur_texte,
    )
    frame_cases.grid(row=1, column=0, sticky="nsew", padx=(0, 10), pady=(10, 0))

    # à placer plus loin : besoin d'avoir déjà créé récap
    regions = region.Regions(frame_parent=frame_cases, fenetre=fenetre, recap=None)

    #####################################################################################
    # à droite : récap + log + loadbar + bouton

    # FRAME HAUT CONTIENT RÉCAP ET LOG
    frame_haut = tk.Frame(frame_principal)
    frame_haut.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=(0, 10))
    frame_haut.columnconfigure(0, weight=1)
    frame_haut.rowconfigure(0, weight=1)
    frame_haut.rowconfigure(1, weight=2)

    # que contient frame choix ?
    frame_choix = tk.Frame(frame_haut, bg=theme.couleur_frame)
    frame_choix.grid(row=0, column=0, sticky="nsew")
    frame_choix.rowconfigure(0, weight=1)
    frame_choix.rowconfigure(1, weight=1)
    frame_choix.columnconfigure(0, weight=1)

    # recap
    frame_recap = tk.LabelFrame(
        frame_choix,
        text="Récapitulatif",
        relief="raised",
        bg=theme.couleur_frame,
        foreground=theme.couleur_texte,
    )
    frame_recap.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
    frame_recap.rowconfigure(0, weight=1)
    frame_recap.grid_columnconfigure(0, weight=1)
    frame_recap.grid_columnconfigure(1, weight=2)

    recapitulatif = recap.Recap(
        frame_parent=frame_recap,
        region=regions,
        tree=folder_tree,
        grid_row=1,
        grid_column=0,
    )
    folder_tree.recap = recapitulatif
    regions.recap = recapitulatif

    # log
    frame_log = tk.LabelFrame(
        frame_haut, text="Log", foreground=theme.couleur_texte, bg=theme.couleur_frame
    )
    frame_log.grid(row=1, column=0, sticky="nsew", padx=0, pady=(10, 0))

    terminal = log.Log(frame_log)
    terminal.pack(fill="both", expand=True)
    terminal.write("SalamAlaykom les pâtissiers\n")

    # FRAME BAS CONTIENT PROGRESS BAR ET BOUTON
    frame_bas = tk.Frame(frame_principal)
    frame_bas.grid(row=1, column=1, sticky="nsew", padx=(10, 0), pady=(10, 0))
    frame_bas.rowconfigure(0, weight=1)
    frame_bas.rowconfigure(1, weight=1)
    frame_bas.columnconfigure(0, weight=1)

    # style.map("Custom.TButton",
    #           background=[("active", theme.couleur_frame), ("!disabled", theme.couleur_frame)],
    #           foreground=[("!disabled", "white")],
    #           relief = "groove")

    # progress bar + bouton
    pb = progressbar.ProgressBar(
        frame_parent=frame_bas, fenetre=fenetre, grid_row=0, grid_column=0
    )

    theme.configurer_background(frame_root)

    fenetre.mainloop()
