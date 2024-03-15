import os
import tkinter as tk
from tkinter import ttk 

import folder
import theme 
import terminal

additional_regions = set()

# def update_recap(check_vars, options, recap_label):
#     # Sélectionnez les options qui sont cochées
#     selected_options = [option for option in options if check_vars.get(option, tk.BooleanVar()).get()]
#     # Ajoutez les régions supplémentaires à la liste des options sélectionnées
#     all_options = selected_options + list(additional_regions)
#     recap_text = "Régions:\n"
#     for i, option in enumerate(all_options):
#         if i > 0:  # Ajouter une virgule avant tous les éléments sauf le premier
#             recap_text += ", "
#         if i % 2 == 0 and i > 0:  # Ajouter un saut de ligne tous les deux éléments
#             recap_text += "\n"
#         recap_text += option
#     recap_cases.itemconfig(text_recap_cases, text=recap_text)

def update_recap(check_vars, options, recap_inner_frame):
    # Nettoyer le frame récapitulatif avant de le mettre à jour
    for widget in recap_inner_frame.winfo_children():
        widget.destroy()

    all_options = sorted(list(additional_regions) + [option for option in options if check_vars.get(option, tk.BooleanVar()).get()])
    
    for option in all_options:
        option_frame = tk.Frame(recap_inner_frame)
        option_frame.pack(fill=tk.X, expand=True)
        
        option_label = tk.Label(option_frame, text=option, bg="lightblue")
        option_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        delete_button = tk.Button(option_frame, text="✕", command=lambda o=option: remove_region(o, check_vars, options, recap_inner_frame))
        delete_button.pack(side=tk.RIGHT)
        
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

# Lien de la case "All" avec la fonction toggle_all
# def all_command():
#     toggle_all(variables["All"], variables, checkboxes)

################# MODIF CHAIMA
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

################# FIN MODIF CHAIMA

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

########## MODIF CHAIMA
# Fonction de rappel pour la zone de texte
# def on_text_entry(event=None):
#     entered_text = zone_entre.get().strip().lower()  # Obtient le texte et le convertit en minuscules
#     if entered_text == "all":
#         # Si "All" est entré, coche toutes les cases sauf "All"
#         for region, var in check_vars.items():
#             if region.lower() != "all":
#                 var.set(True)
#         update_recap(check_vars, [region for region in regions if region.lower() != "all"], recap_cases)  # Met à jour le récapitulatif sans inclure "All"
#     else:
#         # Sinon, vérifie si le texte correspond à une région et coche la case correspondante
#         for region, var in check_vars.items():
#             if entered_text == region.lower():
#                 var.set(True)  # Coche la case à cocher correspondante
#                 update_recap(check_vars, regions, recap_cases)  # Met à jour le récapitulatif
#                 break
# Ensemble pour stocker les régions supplémentaires
# def on_text_entry(event=None):
#     entered_text = zone_entre.get().strip()  # Obtenez le texte entré sans la conversion en minuscules pour conserver la casse
#     if entered_text:  # Si du texte a été entré
#         if entered_text.lower() == "all":  # Si le texte est "all", cochez toutes les cases
#             for region, var in check_vars.items():
#                 var.set(True)
#             update_recap(check_vars, regions, recap_cases)
#         else:
#             # Ajoutez la région entrée à l'ensemble des régions supplémentaires
#             additional_regions.add(entered_text)
#             update_recap(check_vars, regions + list(additional_regions), recap_cases)
#         zone_entre.set("")  # Nettoyez la zone de texte après l'ajout
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

# def on_text_entry(event=None):
#     entered_text = zone_entre.get().strip()  # Obtenez le texte entré
#     if entered_text:  # Si du texte a été entré
#         region_found = False  # Indicateur pour savoir si la région a été trouvée et cochée
#         if entered_text.lower() == "all":
#             # Si le texte est "all", cochez toutes les cases
#             for region, var in check_vars.items():
#                 var.set(True)
#             update_recap(check_vars, regions, recap_cases)
#         else:
#             for region in regions:
#                 if entered_text.lower() == region.lower():
#                     check_vars[region].set(True)  # Cochez la case de la région correspondante
#                     update_recap(check_vars, regions, recap_cases)
#                     region_found = True  # Marquez que la région a été trouvée et cochée
#                     break  # Sortez de la boucle une fois la région trouvée
#             if not region_found:
#                 # Si la région saisie n'est pas déjà présente, ajoutez-la à `additional_regions` et mettez à jour le récapitulatif
#                 # Assurez-vous que `additional_regions` est défini quelque part dans votre code, par exemple en l'initialisant comme un set vide en dehors de cette fonction
#                 if entered_text.lower() not in [region.lower() for region in regions + list(additional_regions)]:
#                     additional_regions.add(entered_text)  # Ajoutez la région à la liste des régions supplémentaires
#                     update_recap(check_vars, regions + list(additional_regions), recap_cases)
#         zone_entre.set("")  # Nettoyez la zone de texte après l'ajout ou si la région est déjà présente
#         # Mettez à jour la scrollbar si nécessaire, en fonction de la hauteur du contenu de votre récapitulatif

########## FIN MODIF CHAIMA


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
    frame_principal.grid(row=1, column=0, sticky="nsew", padx=30, pady=(0,30))

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

    label = tk.Label(frame_titre, text="Acquisition des régions fonctionnelles dans les génomes", font=("Arial", 25), fg=theme.couleur_frame)
    label.grid(row=0, column=0, sticky="ew")

    ##### INFO
    class ToolTip(object):
            # Initialisation sans changement
        def __init__(self, widget):
            self.widget = widget
            self.tipwindow = None
            self.x = self.y = 0

        def show_tip(self, text):
            "Affiche le texte du tooltip"
            if self.tipwindow or not text:
                return
            x = self.widget.winfo_rootx() - 150
            y = self.widget.winfo_rooty() + self.widget.winfo_height() 
            self.tipwindow = tw = tk.Toplevel(self.widget)
            tw.wm_overrideredirect(True)
            tw.wm_geometry("+%d+%d" % (x, y))
            label = tk.Label(tw, text=text, justify=tk.LEFT,
                            background="lightyellow", relief=tk.SOLID, borderwidth=1,
                            font=("Arial", "10", "normal"))
            label.pack(ipadx=1, ipady=1)

        def hide_tip(self):
            if self.tipwindow:
                self.tipwindow.destroy()
                self.tipwindow = None

    def enter(event):
        tooltip.show_tip("Martin DENIAU\nChaïma JAIDANE\nCharlotte KRUZIC\nZoé MARQUIS\nValentin MASSEBEUF\nClément OBERHAUSER")

    def leave(event):
        tooltip.hide_tip()
        
    label_info = tk.Label(frame_titre, text="i", font=("Arial", 14, "bold"), fg="white", bg="white",
                            width=2, height=1, borderwidth=2)
    label_info.grid(row=0, column=1, padx=5, pady=20, sticky="e")
    tooltip = ToolTip(label_info)
    label_info.bind("<Enter>", enter)
    label_info.bind("<Leave>", leave)

#PARTIE GAUCHE
    ##PARTIE ARBORESCENCE
    frame_arbo = tk.LabelFrame(frame_principal, text="Arborescence", relief="raised",bg=theme.couleur_frame, foreground="white")
    frame_arbo.grid(row=0, column=0, sticky="nsew", padx=(0,10), pady=(0,10))

    ##PARTIE SÉLÉCTION DES RÉGIONS
    frame_cases = tk.LabelFrame(frame_principal, text="Sélection des régions", bg=theme.couleur_frame, fg="white")    
    frame_cases.grid(row=1, column=0, sticky="nsew", padx=(0,10),pady=(10,0))

    frame_cases.rowconfigure(0, weight=1)
    frame_cases.rowconfigure(1, weight=1)
    frame_cases.grid_columnconfigure(0, weight=1)
    frame_cases.grid_columnconfigure(1, weight=1)
    frame_cases.grid_columnconfigure(2, weight=1)
    frame_cases.grid_columnconfigure(3, weight=1)
    frame_cases.grid_columnconfigure(4, weight=1)
    frame_cases.grid_columnconfigure(5, weight=1)
    
    # case à cocher
    regions = ["CDS", "ncRNA", "3'UTR", "Centromère", "rRNA", "5'UTR",
               "Intron", "Telomère", "Mobile élément", "tRNA", "All"]

    # Dictionnaires pour stocker les variables et les widgets des cases à cocher
    variables = {}
    checkboxes = {}
    check_vars = []
    check_vars = {option: tk.BooleanVar(value=False) for option in regions}

    # Zone de saisie
    zone_entre = tk.StringVar()

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
        # Ajuster la hauteur de la frame_saisie pour correspondre aux autres éléments si nécessaire
        #frame_saisie.grid_rowconfigure(0, minsize=20)  # Aju

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
    frame_recap.grid_columnconfigure(1, weight=1)
    
        ##FRAME BAS CONTIENT PROGRESS BAR ET BOUTON
    frame_bas = tk.Frame(frame_principal, background=theme.couleur_frame, relief="solid", borderwidth=1)
    frame_bas.grid(row=1, column=1, sticky="nsew", padx=(10,0), pady=(10,0))
    
    ###Bouton effacé
    def effacer_selection():
        # Réinitialisez les variables de case à cocher à False
        for var in check_vars.values():
            var.set(False)
        
        # Effacer les régions supplémentaires ajoutées
        additional_regions.clear()

        # Effacer le contenu de la zone de texte
        zone_entre.set("")

        # Mettez à jour le récapitulatif pour refléter les changements
        update_recap(check_vars, regions + list(additional_regions), recap_cases)
        recap_arbo.itemconfig(text_recap_arbo, text="Dossier:\n")

    ###Créer un bouton dans la frame récapitulative pour effacer la sélection
    bouton_effacer_selection = ttk.Button(frame_recap, text="TOUT EFFACER", command=effacer_selection,style="Custom.TButton")
    bouton_effacer_selection.grid(row=1, column=0, sticky="nsew", pady=(0,0))

    ###Créer un Canvas pour le récapitulatif de l'arborescence
    f_arbo = tk.Frame(frame_recap)
    f_arbo.grid(row=0, column=0, sticky="w")

    recap_arbo = tk.Canvas(f_arbo, bg="pink",height=100, width=400)
    recap_arbo.pack(side="left", fill="both", expand=True)
    
    #recap_arbo.grid(row=0, column=0, sticky="nw")
    text_recap_arbo = recap_arbo.create_text(20,20,text="Dossier:", fill="black", anchor="nw")
    # Appel de configure_grid une fois que la fenêtre est affichée pour avoir les bonnes dimensions
    #fenetre.after(100, configure_grid)

    
    ###Créer un Canvas pour le récapitulatif des régions
    f_cases = tk.Frame(frame_recap)
    f_cases.grid(row=0, column=1, sticky="w")

    recap_cases = tk.Canvas(f_cases, bg="lightblue", height=100, width=200)
    #recap_cases.grid(row=0, column=1, sticky="nw")
    recap_cases.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    text_recap_cases = recap_cases.create_text(20,20,text="Régions:", fill="black", anchor="nw")
    
    scrollbar_regions = tk.Scrollbar(f_cases, orient="vertical", command=recap_cases.yview)
    scrollbar_regions.pack(side=tk.RIGHT, fill="y")
    # # Créer une scrollbar pour la direction verticale
    # scrollbar_y = tk.Scrollbar(f_cases, orient="vertical", command=recap_cases.yview)
    # scrollbar_y.pack(side="right", fill="y")
    # # Connecter la scrollbar à la direction verticale du Canvas
    recap_cases.configure(yscrollcommand=scrollbar_regions.set)

    #recap_cases = tk.Label(frame_recap, text="Régions:\n",foreground="white",relief="solid", borderwidth=2, anchor="w")
    #recap_cases.grid(row=0, column=1, sticky="nsew")

    

    ##FENETRE LOG ET BARRE PROGRESSION
    ## haut = choix + log, bas = progress bar + bouton


    # test=tk.BooleanVar()
    # check1=tk.Checkbutton(frame_cases, text="test", variable=test)
    # check1.pack(anchor="w")

    frame_log = tk.LabelFrame(frame_haut, text="log",bg=theme.couleur_frame)
    frame_log.grid(row=1, column=0, sticky="nsew", padx=0, pady=(10,0))

    term = terminal.Terminal(frame_log, bg="black")
    term.pack(fill="both", expand=True)

    term.write("triple monstre")
    
    ## BAS

    label = tk.Label(frame_bas, text="loadbar") 

    # Configuration initiale de la progression
    progress_running = False

    style = ttk.Style()
    style.theme_use('clam')  # Choix d'un thème, ici 'clam'
    style.configure("Custom.Horizontal.TProgressbar", troughcolor=theme.couleur_frame, background=theme.couleur_selection)  # Personnalisation des couleurs


    loadbar = ttk.Progressbar(frame_bas, orient='horizontal', mode='determinate', style="Custom.Horizontal.TProgressbar")
    loadbar.grid(row=0, column=0, sticky="ewns",pady = (0,30))
    #loadbar.pack(fill='x', expand=True)
    #loadbar.pack(ipady=8)

    #style = ttk.Style()
    style.map("Custom.TButton",
              background=[("active", theme.couleur_frame), ("!disabled", theme.couleur_frame)],
              foreground=[("!disabled", "white")],
              relief = "groove")

    bouton = ttk.Button(frame_bas, text="Start", command=toggle_progress, style="Custom.TButton")
    bouton.grid(row=1, column=0)
    bouton.bind("<Enter>", change_cursor)
    
    frame_bas.rowconfigure(0, weight=1)
    frame_bas.rowconfigure(1, weight=1)
    frame_bas.columnconfigure(0, weight=1)

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

