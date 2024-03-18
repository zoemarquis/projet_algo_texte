import os
import tkinter as tk
from tkinter import ttk 

import folder
import theme 
import log
import credit
import region
import recap

# pour bouton, à placer dans theme plutot ?
def change_cursor(event):
    event.widget.config(cursor="hand2")  # Change le curseur en main pointant

# def change_button_style(button, background_color, foreground_color):
#     style = ttk.Style()
#     style.configure("Custom.TButton",
#                     background=background_color,
#                     foreground=foreground_color)

# on garde ici ou on le met dans le fichier du treeview ou dans theme carrement ?
def change_treeview_colors(treeview, text_color, select_color, background_color):
    style = ttk.Style()
    style.configure("Custom.Treeview", foreground=text_color, fieldbackground=background_color, background=background_color)
    style.map("Custom.Treeview", background=[('selected', select_color)])

# def change_label_frame_font(label_frame, font_name, font_size):
#     style = ttk.Style()
#     style.configure("Custom.TLabelframe.Label", font=(font_name, font_size))


# à placer dans dossier loadbar
# Fonction pour démarrer ou arrêter la progression
def toggle_progress():
    global progress_running
    progress_running = not progress_running  # Bascule l'état de progression
    bouton.config(text="Stop" if progress_running else "Start")
    if progress_running:
        update_progress()
# à placer dans dossier loadbar
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
    root_dir = "Results"
    folder_structure, dict_path = folder.create_folder_structure(root_dir)
    
    fenetre = tk.Tk()
    style = ttk.Style(fenetre)
    fenetre.title("GENBANK PARSER")
    fenetre.geometry("1300x800")
    fenetre.update()
    width = fenetre.winfo_width() 
    height = fenetre.winfo_height()
    
    # FRAME pack pour pouvoir modifier la taille de la fenêtre
    frame_root = tk.Frame(fenetre)
    frame_root.pack(expand = 1, fill = "both")
    frame_root.rowconfigure(0, weight=1)
    frame_root.rowconfigure(1, weight=10)
    frame_root.columnconfigure(0, weight=1)
    theme.configurer_background(frame_root)
    # + utiliser les fonctions pour modifier le theme

    #####################################################################################
    # FRAME titre : contient le texte du titre + le petit i
    frame_titre = tk.Frame(frame_root)
    frame_titre.grid(row=0, column=0, sticky="nsew", padx=30, pady=0)
    frame_titre.rowconfigure(0, weight=1)
    frame_titre.columnconfigure(0, weight=20)
    frame_titre.columnconfigure(1, weight=1)

    # texte titre
    label = tk.Label(frame_titre, text="Acquisition des régions fonctionnelles dans les génomes", font=("Arial", 30), fg=theme.couleur_frame)
    label.grid(row=0, column=0, sticky="ew")

    # le petit i : contient nos noms
    credit = credit.Credits(frame_titre, grid_row=0, grid_column=1) 

    #####################################################################################
    # FRAME contenant tout sauf titre et petit i : en grille
    frame_principal = tk.Frame(frame_root)
    frame_principal.grid(row=1, column=0, sticky="nsew", padx=30, pady=(10,20))
    frame_principal.grid_columnconfigure(0, weight=1)
    frame_principal.grid_columnconfigure(1, weight=1)
    frame_principal.grid_rowconfigure(0, weight=1)
    frame_principal.grid_rowconfigure(1, weight=1)  

    #####################################################################################
    # à gauche : tous les choix : arborescence + régions

    # FRAME arborescence 
    frame_arbo = tk.LabelFrame(frame_principal, text="Arborescence", relief="raised",bg=theme.couleur_frame, foreground="white")
    frame_arbo.grid(row=0, column=0, sticky="nsew", padx=(0,10), pady=(0,10))

    style.configure("Treeview", rowheight=25)
    style.map("Treeview", background=[('selected', '#347083')])
    folder_tree = folder.FolderTree(frame_arbo, folder_structure, dict_path, recap=None)
    folder_tree.pack(expand=True, fill=tk.BOTH)
    change_treeview_colors(folder_tree, text_color=theme.couleur_texte, select_color= "lightblue", background_color=theme.couleur_frame)

    # FRAME régions
    frame_cases = tk.LabelFrame(frame_principal, text="Sélection des régions", bg=theme.couleur_frame, fg="white")    
    frame_cases.grid(row=1, column=0, sticky="nsew", padx=(0,10),pady=(10,0))

    # à placer plus loin : besoin d'avoir déjà créé récap
    regions = region.Regions(frame_parent=frame_cases, fenetre=fenetre, recap=None)


    #####################################################################################
    # à droite : récap + log + loadbar + bouton

    # FRAME HAUT CONTIENT RÉCAP ET LOG
    frame_haut = tk.Frame(frame_principal)
    frame_haut.grid(row=0, column=1, sticky="nsew", padx=(10,0), pady=(0,10))
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
    frame_recap = tk.LabelFrame(frame_choix, text="Récapitulatif", relief="raised", bg=theme.couleur_frame, foreground="white")
    frame_recap.grid(row=1, column=0, sticky="nsew", pady=(0,10))
    frame_recap.rowconfigure(0, weight=1)
    frame_recap.grid_columnconfigure(0, weight=1)
    frame_recap.grid_columnconfigure(1, weight=2)

    recapitulatif = recap.Recap(frame_parent=frame_recap, region=regions, tree=folder_tree,grid_row=1, grid_column=0)
    folder_tree.recap=recapitulatif
    regions.recap=recapitulatif


    # log
    frame_log = tk.LabelFrame(frame_haut, text="log",bg=theme.couleur_frame)
    frame_log.grid(row=1, column=0, sticky="nsew", padx=0, pady=(10,0))

    terminal = log.Log(frame_log, bg="black")
    terminal.pack(fill="both", expand=True)
    terminal.write("SalamAlaykom les pâtissiers\n")
    
    
    # FRAME BAS CONTIENT PROGRESS BAR ET BOUTON
    frame_bas = tk.Frame(frame_principal, background=theme.couleur_frame, relief="solid", borderwidth=1)
    frame_bas.grid(row=1, column=1, sticky="nsew", padx=(10,0), pady=(10,0))
    frame_bas.rowconfigure(0, weight=1)
    frame_bas.rowconfigure(1, weight=1)
    frame_bas.columnconfigure(0, weight=1)


    # progress bar à mettre dans un autre fichier ?
    progress_running = False
    style = ttk.Style()
    style.theme_use('clam')  # Choix d'un thème, ici 'clam'
    style.configure("Custom.Horizontal.TProgressbar", troughcolor=theme.couleur_frame, background=theme.couleur_selection)  # Personnalisation des couleurs
    loadbar = ttk.Progressbar(frame_bas, orient='horizontal', mode='determinate', style="Custom.Horizontal.TProgressbar")
    loadbar.grid(row=0, column=0, sticky="ewns",pady = (0,30))
    #loadbar.pack(fill='x', expand=True)
    #loadbar.pack(ipady=8)
        ##Bouton Start
    #style = ttk.Style()
    style.map("Custom.TButton",
              background=[("active", theme.couleur_frame), ("!disabled", theme.couleur_frame)],
              foreground=[("!disabled", "white")],
              relief = "groove")


    # bouton start / stop
    bouton = ttk.Button(frame_bas, text="Start", command=toggle_progress, style="Custom.TButton")
    bouton.grid(row=1, column=0)
    bouton.bind("<Enter>", change_cursor)
    

    fenetre.mainloop()

