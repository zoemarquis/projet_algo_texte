import tkinter as tk
from tkinter import ttk
from tkinter import font


import os
import signal
import sys
import graphique.folder as folder
import graphique.theme as theme
import graphique.log as log
import graphique.credit as credit
import graphique.region as region
import graphique.recap as recap
import graphique.progressbar as progressbar

# chemin_src = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
# sys.path.append(chemin_src)
# # sys.path.insert(1, "../src/")
import src.arborescence as ar

def close_window(window, pb):
    window.destroy()
    os.kill(os.getpid(), signal.SIGINT)


if __name__ == "__main__":
    root_dir = "Results"
    folder_structure, dict_path = folder.create_folder_structure(root_dir)

    ar.get_tree()

    fenetre = tk.Tk()
    bold_font = font.Font(family="Helvetica", size=14, weight="bold")

    fenetre.title("GENBANK PARSER")
    fenetre.geometry("1300x800")
    fenetre.update()
    width = fenetre.winfo_width()
    height = fenetre.winfo_height()

    style = ttk.Style(fenetre)
    style.theme_use("clam")
    style.configure(
        "Custom.Treeview",
        fieldbackground=theme.couleur_frame,
        background=[
            ("selected", "lightblue"),
            ("!selected", theme.couleur_frame),
        ],
        foreground=theme.couleur_texte,
    )
    style.configure("Custom.Treeview.Item", background="lightblue")
    style.configure(
        "Custom.TButton",
        foreground=theme.couleur_texte,
        background=theme.couleur_frame,
        font=("Arial", 12),
    )
    style.map(
        "Custom.TButton",
        background=[("active", theme.couleur_selection)],
        foreground=[("active", theme.couleur_texte)],
    )
    style.configure(
        "Custom.Vertical.TScrollbar",
        background="lightgrey",
        troughcolor=theme.couleur_fond,
        bordercolor=theme.couleur_frame,
        arrowcolor=theme.couleur_fond,
        # gripcolor="purple",
        # slidercolor="yellow",
    )
    style.map(
        "Custom.Vertical.TScrollbar",
        background=[("disabled", "lightgrey")],
        troughcolor=[("disabled", theme.couleur_fond)],
        bordercolor=[("disabled", theme.couleur_frame)],
        arrowcolor=[("disabled", theme.couleur_fond)],
        # gripcolor=[("disabled", "purple")],
        # slidercolor=[("disabled", "yellow")],
    )
    style.configure(
        "Custom.Horizontal.TScrollbar",
        background="lightgrey",
        troughcolor=theme.couleur_fond,
        bordercolor=theme.couleur_frame,
        arrowcolor=theme.couleur_fond,
        # gripcolor="purple",
        # slidercolor="yellow",
    )
    style.map(
        "Custom.Horizontal.TScrollbar",
        background=[("disabled", "lightgrey")],
        troughcolor=[("disabled", theme.couleur_fond)],
        bordercolor=[("disabled", theme.couleur_frame)],
        arrowcolor=[("disabled", theme.couleur_fond)],
        # gripcolor=[("disabled", "purple")],
        # slidercolor=[("disabled", "yellow")],
    )
    style.configure(
        "Custom.Horizontal.TProgressbar",
        background=theme.couleur_selection,
        troughcolor=theme.couleur_fond,
        bordercolor=theme.couleur_frame,
    )
    style.configure(
        "Custom.TCheckbutton",
        background=theme.couleur_frame,
        foreground=theme.couleur_texte,
        font=("Arial", 12),
    )
    style.map("Custom.TCheckbutton", background=[("selected", theme.couleur_frame)])

    # FRAME pack pour pouvoir modifier la taille de la fenêtre
    frame_root = tk.Frame(fenetre)
    frame_root.pack(expand=1, fill="both")
    frame_root.rowconfigure(0, weight=1)
    frame_root.rowconfigure(1, weight=10)
    frame_root.columnconfigure(0, weight=1)

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
        fg=theme.couleur_titre,
    )
    label.grid(row=0, column=0, sticky="ew")

    # le petit i : contient nos noms
    credit = credit.Credits(frame_titre, grid_row=0, grid_column=1)

    #####################################################################################
    # FRAME contenant tout sauf titre et petit i : en grille
    frame_principal = tk.Frame(frame_root)
    frame_principal.grid(row=1, column=0, sticky="nsew", padx=30, pady=(10, 30))
    frame_principal.grid_columnconfigure(0, weight=1)
    frame_principal.grid_columnconfigure(1, weight=1)
    frame_principal.grid_rowconfigure(0, weight=1)

    frame_gauche = tk.Frame(frame_principal)
    frame_gauche.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
    frame_gauche.grid_rowconfigure(0, weight=2)
    frame_gauche.grid_rowconfigure(1, weight=1)
    frame_gauche.grid_columnconfigure(0, weight=1)

    frame_droite = tk.Frame(frame_principal)
    frame_droite.grid(row=0, column=1, sticky="nsew")
    frame_droite.grid_rowconfigure(0, weight=2)
    frame_droite.grid_rowconfigure(1, weight=3)
    frame_droite.grid_rowconfigure(2, weight=1)
    frame_droite.grid_columnconfigure(0, weight=1)

    #####################################################################################
    # à gauche : tous les choix : arborescence + régions
    
    # FRAME arborescence
    frame_arbo = tk.LabelFrame(
        frame_gauche,
        text="Séléction des dossiers",
        relief="flat",
        font=bold_font,
        bg=theme.couleur_frame,
        foreground=theme.couleur_texte,
    )
    frame_arbo.grid(row=0, column=0, sticky="nsew", pady=(0, 10))

    folder_tree = folder.FolderTree(frame_arbo, folder_structure, dict_path, recap=None)
    folder_tree.pack(expand=True, fill=tk.BOTH)

    # FRAME régions
    frame_cases = tk.LabelFrame(
        frame_gauche,
        text="Sélection des régions",
        relief="flat",
        font=bold_font,
        bg=theme.couleur_frame,
        foreground=theme.couleur_texte,
    )
    frame_cases.grid(row=1, column=0, sticky="nsew", pady=(10, 0))

    # à placer plus loin : besoin d'avoir déjà créé récap
    regions = region.Regions(frame_parent=frame_cases, fenetre=fenetre, recap=None)

    #####################################################################################
    # à droite : récap + log + loadbar + bouton

    # recap
    frame_recap = tk.LabelFrame(
        frame_droite,
        text="Récapitulatif",
        relief="flat",
        font=bold_font,
        bg=theme.couleur_frame,
        foreground=theme.couleur_texte,
        height=200,
    )
    frame_recap.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
    frame_recap.rowconfigure(0, weight=1)
    frame_recap.grid_columnconfigure(0, weight=1)
    frame_recap.grid_columnconfigure(1, weight=1)

    recapitulatif = recap.Recap(
        frame_parent=frame_recap, region=regions, tree=folder_tree
    )
    folder_tree.recap = recapitulatif
    regions.recap = recapitulatif

    # log
    frame_log = tk.LabelFrame(
        frame_droite, 
        text="Log", 
        font=bold_font,
        relief="flat",
        foreground=theme.couleur_texte, 
        bg=theme.couleur_frame
    )
    frame_log.grid(row=1, column=0, sticky="nsew", pady=(10, 20))

    terminal = log.Log(frame_log)
    terminal.pack(fill="both", expand=True)

    # FRAME BAS CONTIENT PROGRESS BAR ET BOUTON
    frame_bas = tk.Frame(frame_droite)
    frame_bas.grid(row=2, column=0, sticky="nsew", pady=(0, 0))
    frame_bas.rowconfigure(0, weight=1)
    frame_bas.rowconfigure(1, weight=1)
    frame_bas.columnconfigure(0, weight=1)

    # progress bar + bouton
    pb = progressbar.ProgressBar(
        frame_parent=frame_bas, fenetre=fenetre, grid_row=0, grid_column=0, folder_tree=folder_tree, regions=regions, log=terminal
    )

    theme.configurer_background(frame_root)
    theme.configurer_background(frame_titre)
    theme.configurer_background(frame_principal)
    theme.configurer_background(frame_bas)
    theme.configurer_background(frame_gauche)
    theme.configurer_background(frame_droite)
    theme.configurer_background(label)
    
    fenetre.protocol("WM_DELETE_WINDOW", lambda: close_window(fenetre, pb))
    fenetre.mainloop()

