import os
import tkinter as tk
from tkinter import ttk 

import folder
import theme 
import terminal
import credit

additional_regions = set()
## Placer région avec le delete

def update_recap(check_vars, options, recap_inner_frame):
    # Supprimez tous les éléments précédemment dessinés sur le canvas sauf le titre "Régions"
    for item in recap_inner_frame.find_withtag("region_item"):
        recap_inner_frame.delete(item)

    all_options = sorted(list(additional_regions) + [option for option in options if check_vars.get(option, tk.BooleanVar()).get()])
    
    y_offset = 30  # Commencez à dessiner le texte sous le titre "Régions"
    for option in all_options:
        # Créez le texte pour la région
        text_id = recap_inner_frame.create_text(10, y_offset, text=option, anchor="nw", fill="black", tags=("region_item",))
        
        # Calculez la largeur du texte pour positionner correctement la croix
        text_width = recap_inner_frame.bbox(text_id)[2]
        cross_start_x = text_width + 10  # Définissez une marge après le texte pour la croix
        cross_end_x = cross_start_x + 8  # La taille de la croix
        cross_y = y_offset + 3  # Position Y ajustée pour centrer la croix par rapport au texte

        # Dessinez la croix
        recap_inner_frame.create_line(cross_start_x, cross_y, cross_end_x, cross_y + 10, fill="red", tags=("region_item", f"delete_{option}"))
        recap_inner_frame.create_line(cross_start_x, cross_y + 10, cross_end_x, cross_y, fill="red", tags=("region_item", f"delete_{option}"))

        # Associez la croix à un gestionnaire d'événement pour supprimer la région sur clic
        recap_inner_frame.tag_bind(f"delete_{option}", "<Button-1>", lambda event, opt=option: remove_region(opt, check_vars, options, recap_inner_frame))

        y_offset += 30  # Incrémentez l'offset vertical pour le prochain élément
def remove_region(region, check_vars, options, recap_inner_frame):
    if region in additional_regions:
        additional_regions.remove(region)
    else:
        check_vars[region].set(False)
    update_recap(check_vars, options, recap_inner_frame)


def change_cursor(event):
    event.widget.config(cursor="hand2")  # Change le curseur en main pointant

def change_button_style(button, background_color, foreground_color):
    style = ttk.Style()
    style.configure("Custom.TButton",
                    background=background_color,
                    foreground=foreground_color)

def change_treeview_colors(treeview, text_color, select_color, background_color):
    style = ttk.Style()
    style.configure("Custom.Treeview", foreground=text_color, fieldbackground=background_color, background=background_color)
    style.map("Custom.Treeview", background=[('selected', select_color)])

def change_label_frame_font(label_frame, font_name, font_size):
    style = ttk.Style()
    style.configure("Custom.TLabelframe.Label", font=(font_name, font_size))


## Fonction pour la case à cocher ALL
def all_command():
    all_checked = variables["All"].get()
    if all_checked:
        # Si "All" est cochée, mettez à jour toutes les variables et le texte de récapitulation
        for region, var in check_vars.items():
            var.set(True)
        # Liste toutes les régions sauf "All" pour le récapitulatif
        update_recap(check_vars, [region for region in regions if region != "All"], recap_cases)
    else:
        # Si "All" est décochée, réinitialisez
        for region, var in check_vars.items():
            var.set(False)
        update_recap(check_vars, [], recap_cases)
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

## Fonction pour la zone de texte
def on_text_entry(event=None):
    entered_text = zone_entre.get().strip()  # Obtenez le texte entré
    if entered_text:  # Si du texte a été entré
        # Séparez le texte entré en régions basées sur le séparateur ";"
        entered_regions = entered_text.split(";")
        for entered_region in entered_regions:
            entered_region = entered_region.strip()  # Supprimez les espaces superflus de chaque région
            region_found = False  # Indicateur pour savoir si la région a été trouvée et cochée
            if entered_region.lower() == "all":
                # Si le texte est "all", cochez toutes les cases
                for region, var in check_vars.items():
                    var.set(True)
                update_recap(check_vars, regions, recap_cases)
            else:
                for region in regions:
                    if entered_region.lower() == region.lower():
                        check_vars[region].set(True)  # Cochez la case de la région correspondante
                        update_recap(check_vars, regions, recap_cases)
                        region_found = True  # Marquez que la région a été trouvée et cochée
                        break  # Sortez de la boucle une fois la région trouvée
                if not region_found:
                    # Si la région saisie n'est pas déjà présente, ajoutez-la à `additional_regions`
                    if entered_region.lower() not in [region.lower() for region in regions + list(additional_regions)]:
                        additional_regions.add(entered_region)  # Ajoutez la région à la liste des régions supplémentaires
                        update_recap(check_vars, regions + list(additional_regions), recap_cases)
        zone_entre.set("")  # Nettoyez la zone de texte après l'ajout ou si la région est déjà présente


def configure_grid(num_columns=2):
        frame_width = frame_cases.winfo_height()
        #num_columns = 2
        column_width = frame_width // (num_columns + 2)

        # Calculez l'espacement uniforme en fonction du nombre total de colonnes et de la largeur disponible
        total_spacing = frame_width - (num_columns * column_width)
        spacing_per_column = total_spacing // (num_columns + 1)

        for c in range(num_columns + 1):
            # Configurez l'espacement pour chaque colonne
            frame_cases.grid_columnconfigure(c, minsize=column_width, pad=spacing_per_column)

        r, c = 0, 0
        for region in regions:
            var = tk.BooleanVar(value=False)
            variables[region] = var

            if region == "All":
                cb = ttk.Checkbutton(frame_cases, text=region, variable=var, style="CustomCheckbutton.TCheckbutton")
                # Ajustez la position du bouton "All" si nécessaire, en fonction de votre conception
                cb.grid(row=r, column=0, sticky="w", padx=0, pady=0)
                checkboxes[region] = cb
            else:
                cb = ttk.Checkbutton(frame_cases, text=region, variable=check_vars[region],
                                    command=lambda: update_recap(check_vars, regions, recap_cases), style="CustomCheckbutton.TCheckbutton")
                cb.grid(row=r, column=c, sticky="wns", padx=0, pady=0)
                checkboxes[region] = cb
                style = ttk.Style()
                style.configure("CustomCheckbutton.TCheckbutton", background=theme.couleur_frame, foreground="white")
                #style.map("CustomCheckbutton.TCheckbutton",background=[("!disabled", theme.couleur_frame)],foreground=[("!disabled", "white")])
            
            c += 1
            if c >= num_columns:
                c = 0
                r += 1
        variables["All"].trace("rwua", lambda *args: all_command())
        frame_saisie = tk.Frame(frame_cases, bg=theme.couleur_frame, relief="solid", borderwidth=1)
        # Placer la frame_saisie en bas à gauche
        frame_saisie.grid(row=r, column=1, sticky="nsew")
        zone_texte = tk.Entry(frame_saisie, textvariable=zone_entre)
        zone_texte.pack(expand=True)
        zone_texte.bind('<Return>', on_text_entry)

        return r,c

##Bouton efface
def effacer_selection():
    global folder_tree  # Assurez-vous que folder_tree est accessible

    # Réinitialisez les variables de case à cocher à False
    for var in check_vars.values():
        var.set(False)

    # Effacer les régions supplémentaires ajoutées
    additional_regions.clear()

    # Effacer le contenu de la zone de texte
    zone_entre.set("")

    # Désélectionner et retirer le surlignement de tous les éléments dans l'arbre
    for item_id in folder_tree.tree.selection():
        folder_tree.tree.selection_remove(item_id)
        # Retirer le surlignement appliqué par les tags
        folder_tree.tree.item(item_id, tags=())

    # Réinitialiser également la sélection interne si votre structure le nécessite
    folder_tree.selected_items.clear()

    # Mettez à jour le récapitulatif pour refléter les changements
    update_recap(check_vars, regions + list(additional_regions), recap_cases)
    recap_arbo.itemconfig(text_recap_arbo, text="Dossier:\n")
   
     

if __name__ == "__main__":
    fenetre = tk.Tk()

    style = ttk.Style(fenetre)
    #style.configure(".", font=("Comic Sans MS", 12))

    fenetre.title("GENBANK PARSER")
    fenetre.geometry("1300x800")

    fenetre.update()
    width = fenetre.winfo_width() 
    height = fenetre.winfo_height()
    
    frame_root = tk.Frame(fenetre)
    frame_root.pack(expand = 1, fill = "both")
    frame_root.rowconfigure(0, weight=1)
    frame_root.rowconfigure(1, weight=10)
    frame_root.columnconfigure(0, weight=1)

#FRAME PRINCIPAL DE TOUTE LA FENETRE
    frame_principal = tk.Frame(frame_root)
    frame_principal.grid(row=1, column=0, sticky="nsew", padx=30, pady=(10,20))

    frame_principal.grid_columnconfigure(0, weight=1)
    frame_principal.grid_columnconfigure(1, weight=1)
    frame_principal.grid_rowconfigure(0, weight=1)
    frame_principal.grid_rowconfigure(1, weight=1)  

## PARTIE TITRE - PETIT BULLE INFO
    ##### TITRE
    frame_titre = tk.Frame(frame_root)
    frame_titre.grid(row=0, column=0, sticky="nsew", padx=30, pady=0)
    frame_titre.rowconfigure(0, weight=1)
    frame_titre.columnconfigure(0, weight=20)
    frame_titre.columnconfigure(1, weight=1)

    label = tk.Label(frame_titre, text="Acquisition des régions fonctionnelles dans les génomes", font=("Arial", 30), fg=theme.couleur_frame)
    label.grid(row=0, column=0, sticky="ew")

    # le petit i : contient nos noms
    credit = credit.Credits(frame_titre, grid_row=0, grid_column=1) 


#PARTIE GAUCHE
    ##PARTIE ARBORESCENCE
    frame_arbo = tk.LabelFrame(frame_principal, text="Arborescence", relief="raised",bg=theme.couleur_frame, foreground="white")
    frame_arbo.grid(row=0, column=0, sticky="nsew", padx=(0,10), pady=(0,10))

    ##PARTIE SÉLÉCTION DES RÉGIONS
    frame_cases = tk.LabelFrame(frame_principal, text="Sélection des régions", bg=theme.couleur_frame, fg="white")    
    frame_cases.grid(row=1, column=0, sticky="nsew", padx=(0,10),pady=(10,0))

    # frame_cases.rowconfigure(0, weight=1)
    # frame_cases.rowconfigure(1, weight=1)
    
    # case à cocher
    regions = ["CDS", "ncRNA", "3'UTR","tRNA", "rRNA", "5'UTR",
               "Intron", "Telomère", "Mobile élément", "Centromère","All"]

    # Dictionnaires pour stocker les variables et les widgets des cases à cocher
    variables = {}
    checkboxes = {}
    check_vars = []
    check_vars = {option: tk.BooleanVar(value=False) for option in regions}

    # Zone de saisie
    zone_entre = tk.StringVar()
        ###  Recupere les colonnes et les lignes pour la case à cocher
    r, c = configure_grid()

   # Réactive la zone de texte sinon
    for i in range(r+1):
        frame_cases.grid_rowconfigure(i, weight=1)
    for i in range(c+1):
        frame_cases.grid_columnconfigure(i, weight=1)

    # Appel de configure_grid une fois que la fenêtre est affichée pour avoir les bonnes dimensions
    fenetre.after(100, configure_grid)

#PARTIE DROITE
    ##PARTIE RÉCAPITULATIF
        ##FRAME HAUT CONTIENT RÉCAP ET LOG
    frame_haut = tk.Frame(frame_principal)
    frame_haut.grid(row=0, column=1, sticky="nsew", padx=(10,0), pady=(0,10))
    frame_haut.columnconfigure(0, weight=1)
    frame_haut.rowconfigure(0, weight=1)
    frame_haut.rowconfigure(1, weight=2)

    frame_choix = tk.Frame(frame_haut, bg=theme.couleur_frame)
    frame_choix.grid(row=0, column=0, sticky="nsew")
    frame_choix.rowconfigure(0, weight=1)
    frame_choix.rowconfigure(1, weight=1)
    frame_choix.columnconfigure(0, weight=1)
    
    frame_recap = tk.LabelFrame(frame_choix, text="Récapitulatif", relief="raised", bg=theme.couleur_frame, foreground="white")
    frame_recap.grid(row=1, column=0, sticky="nsew", pady=(0,10))
    frame_recap.rowconfigure(0, weight=1)
    frame_recap.grid_columnconfigure(0, weight=1)
    frame_recap.grid_columnconfigure(1, weight=2)
    
    
        ###Créer un bouton dans la frame récapitulative pour effacer la sélection
    bouton_effacer_selection = ttk.Button(frame_recap, text="TOUT EFFACER", command=effacer_selection,style="Custom.TButton")
    bouton_effacer_selection.grid(row=1, column=0,padx=(300,300), pady=(10,10), sticky="ew", columnspan=2)
   
        ###Créer un Canvas pour le récapitulatif de l'arborescence
    f_arbo = tk.Frame(frame_recap)
    f_arbo.grid(row=0, column=1, sticky="nsew")

    recap_arbo = tk.Canvas(f_arbo, bg="pink",height=100, width=100)
    recap_arbo.pack(side="right", fill="both", expand=True)
    
    text_recap_arbo = recap_arbo.create_text(20,20,text="Dossier:", fill="black", anchor="nw")
    # Création et configuration de la scrollbar verticale

    # scrollbar_arbo = tk.Scrollbar(f_arbo, orient="vertical", command=recap_arbo.yview)
    # scrollbar_arbo.pack(side="right", fill="y")
    # recap_arbo.configure(yscrollcommand=scrollbar_arbo.set)

        ###Créer un Canvas pour le récapitulatif des régions
    f_cases = tk.Frame(frame_recap)
    f_cases.grid(row=0, column=0, sticky="nsew")

    recap_cases = tk.Canvas(f_cases, bg="lightblue", height=100, width=100)
    recap_cases.pack(side="left", fill=tk.BOTH, expand=True)
    
    text_recap_cases = recap_cases.create_text(20,20,text="Régions:", fill="black", anchor="nw")
    
    # scrollbar_regions = tk.Scrollbar(f_cases, orient="vertical", command=recap_cases.yview)
    # scrollbar_regions.pack(side="left", fill="y")
    
    # recap_cases.configure(yscrollcommand=scrollbar_regions.set)

    #recap_cases = tk.Label(frame_recap, text="Régions:\n",foreground="white",relief="solid", borderwidth=2, anchor="w")
    #recap_cases.grid(row=0, column=1, sticky="nsew")

        ###Fenetre de terminal
    frame_log = tk.LabelFrame(frame_haut, text="log",bg=theme.couleur_frame)
    frame_log.grid(row=1, column=0, sticky="nsew", padx=0, pady=(10,0))

    term = terminal.Terminal(frame_log, bg="black")
    term.pack(fill="both", expand=True)

    term.write("SalamAlaykom les pâtissiers\n")
    
    
        ##FRAME BAS CONTIENT PROGRESS BAR ET BOUTON
    frame_bas = tk.Frame(frame_principal, background=theme.couleur_frame, relief="solid", borderwidth=1)
    frame_bas.grid(row=1, column=1, sticky="nsew", padx=(10,0), pady=(10,0))
    frame_bas.rowconfigure(0, weight=1)
    frame_bas.rowconfigure(1, weight=1)
    frame_bas.columnconfigure(0, weight=1)
    
    #label = tk.Label(frame_bas, text="loadbar") 

    # Configuration initiale de la progression
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

    bouton = ttk.Button(frame_bas, text="Start", command=toggle_progress, style="Custom.TButton")
    bouton.grid(row=1, column=0)
    bouton.bind("<Enter>", change_cursor)
    
    #style = ttk.Style()
    #style.theme_use("classic")  # Changer le thème du style, vous pouvez utiliser "clam", "alt", "default", "classic", etc.
    
    # Changer l'apparence du Treeview
    style.configure("Treeview", rowheight=25)
    style.map("Treeview", background=[('selected', '#347083')])

    #root_dir = "./Results"
    root_dir = "Results"
    folder_structure, dict_path = folder.create_folder_structure(root_dir)

    #folder_tree = folder.FolderTree(frame_arbo, folder_structure, recap_arbo)
    folder_tree = folder.FolderTree(frame_arbo, folder_structure, dict_path, text_recap_arbo, recap_arbo)
    folder_tree.pack(expand=True, fill=tk.BOTH)
    change_treeview_colors(folder_tree, text_color=theme.couleur_texte, select_color= "lightblue", background_color=theme.couleur_frame)
    theme.configurer_background(frame_root)

    fenetre.mainloop()

