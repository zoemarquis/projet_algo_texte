import os
import tkinter as tk
from tkinter import ttk 

import folder
import theme 

# Lien de la case "All" avec la fonction toggle_all
def all_command():
    toggle_all(variables["All"], variables, checkboxes)

def toggle_all(master_var, all_vars, all_checkboxes):
    # Si la case "All" est cochée, cochez toutes les cases et les désactivez
    # Si elle est décochée, décochez toutes les cases et les activez
    for region, var in all_vars.items():
        if region != "All":
            var.set(master_var.get())
            all_checkboxes[region].config(state=tk.DISABLED if master_var.get() else tk.NORMAL)

# Fonction pour démarrer ou arrêter la progression
def toggle_progress():
    global progress_running
    progress_running = not progress_running  # Bascule l'état de progression
    bouton.config(text="Stop" if progress_running else "Start")
    if progress_running:
        update_progress()

# Fonction pour mettre à jour la barre de progression
def update_progress():
    global progress_running
    current_value = loadbar['value']
    if progress_running and current_value < 100:
        loadbar['value'] += 1  # Incrémente la valeur de la barre de progression
        # Planifie la mise à jour de la progression après un délai
        fenetre.after(100, update_progress)  # Continue à appeler update_progress toutes les 100 ms
    elif not progress_running or current_value == 100:
        progress_running = False  # Arrête la progression
        bouton.config(text="Start")  # Réinitialise le texte du bouton

if __name__ == "__main__":
    fenetre = tk.Tk()

    fenetre.title("GENBANK PARSER")
    fenetre.geometry("1300x800")

    fenetre.update()
    # Récupére la largeur
    width = fenetre.winfo_width() 
    # Récupére la hauteur
    height = fenetre.winfo_height()

    frame_global = tk.Frame(fenetre)
    frame_global.pack(expand = 1, fill = "both")

    label = tk.Label(frame_global, text="Acquisition des régions fonctionnelles dans les génomes", fg="white", justify="left")
    label.grid(row=0, column=0, sticky="w")

    frame_principal = tk.Frame(frame_global)
    #frame_principal.pack(expand = 1, fill = "both")
    frame_principal.grid(row=1, column=0, sticky="nsew")

    frame_global.rowconfigure(0, weight=1)
    frame_global.rowconfigure(1, weight=10)
    frame_global.columnconfigure(0, weight=1)

    ## gauche - droite
    frame_principal.columnconfigure(0, weight=3)
    frame_principal.columnconfigure(1, weight=5)
    frame_principal.rowconfigure(0, weight=3)
    frame_principal.rowconfigure(1, weight=1)

    ## contenu de gauche
    frame_arbo = tk.LabelFrame(frame_principal, text="Arborescence")
    frame_arbo.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    frame_recap = tk.LabelFrame(frame_principal, text="Récapitulatif")
    frame_recap.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    ## contenu de droite
    ## haut - bas dans droite
    frame_haut = tk.Frame(frame_principal)
    frame_haut.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    frame_bas = tk.Frame(frame_principal)
    frame_bas.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

    ### contenu de haut
    frame_cases = tk.LabelFrame(frame_haut, text="cases")
    frame_cases.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    #case à cocher
    regions = ["All", "CDS", "ncRNA", "3'UTR", "Centromère", "rRNA", "5'UTR",
               "Intron", "Telomère", "Mobile élément", "tRNA"]

    # Dictionnaires pour stocker les variables et les widgets des cases à cocher
    variables = {}
    checkboxes = {}

    # Zone de saisie
    zone_entre = tk.StringVar()
    frame_saisie = tk.Frame(frame_cases)
    frame_saisie.pack()
    zone_texte = tk.Entry(frame_saisie, textvariable=zone_entre)
    zone_texte.pack(padx=10, pady=10)

    # Création des cases à cocher
    for i in regions:
        var = tk.BooleanVar(value=False)
        cb = tk.Checkbutton(frame_cases, text=i, variable=var)
        cb.pack(anchor="w")
        variables[i] = var
        checkboxes[i] = cb

    variables["All"].trace("w", lambda *args: all_command())

    # test=tk.BooleanVar()
    # check1=tk.Checkbutton(frame_cases, text="test", variable=test)
    # check1.pack(anchor="w")

    frame_log = tk.LabelFrame(frame_haut, text="log")
    frame_log.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    frame_haut.rowconfigure(0, weight=1)
    frame_haut.rowconfigure(1, weight=1)
    frame_haut.columnconfigure(0, weight=1)

    # ## contenu de bas
    frame_loadbar = tk.Frame(frame_bas)
    frame_loadbar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    label = tk.Label(frame_loadbar, text="loadbar")

    # Configuration initiale de la progression
    progress_running = False

    loadbar = ttk.Progressbar(frame_loadbar, orient='horizontal', length=280, mode='determinate')
    loadbar.pack( fill='x', expand=True, padx=10, pady=10)
    loadbar.pack(ipady=10)
    bouton = tk.Button(frame_loadbar, text="Start", command=toggle_progress)
    bouton.pack(side='bottom',fill="x",expand=True, padx=10, pady=10)

    frame_bas.rowconfigure(0, weight=1)
    frame_bas.rowconfigure(1, weight=1)
    frame_bas.columnconfigure(0, weight=1)



    root_dir = "./Results"
    folder_structure = folder.create_folder_structure(root_dir)

    folder_tree = folder.FolderTree(frame_arbo, folder_structure, frame_recap)
    folder_tree.pack(expand=True, fill=tk.BOTH)

    theme.configurer_background(frame_global)

    fenetre.mainloop()