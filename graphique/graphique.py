import os
import tkinter as tk
from tkinter import ttk 

import folder
import theme 
import terminal

def update_recap(check_vars, options, recap_label):
    selected_options = [option for option in options if check_vars[option].get()]
    recap_text = ""
    for i, option in enumerate(selected_options):
        if i % 2 == 0:  # Si c'est le début d'une nouvelle ligne
            if i != 0:  # Si ce n'est pas la première ligne
                recap_text += ", \n"  # Ajouter un saut de ligne pour séparer les lignes
        
        else:
            recap_text += ", "  # Ajouter une virgule pour séparer les options
        recap_text += option  # Ajouter l'option au texte du récapitulatif
    recap_cases.itemconfig(text_recap_cases,text="Régions:\n"+recap_text)

# def update_recap(check_vars, selected_options, recap_label):
#     recap_text = "Régions sélectionnées:\n" + ", ".join(selected_options)        
#     recap_label.config(text=recap_text)
#     variables["All"].trace_add("write", lambda *args: all_command())

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
def on_text_entry(event=None):
    entered_text = zone_entre.get().strip().lower()  # Obtient le texte et le convertit en minuscules
    if entered_text == "all":
        # Si "All" est entré, coche toutes les cases sauf "All"
        for region, var in check_vars.items():
            if region.lower() != "all":
                var.set(True)
        update_recap(check_vars, [region for region in regions if region.lower() != "all"], recap_cases)  # Met à jour le récapitulatif sans inclure "All"
    else:
        # Sinon, vérifie si le texte correspond à une région et coche la case correspondante
        for region, var in check_vars.items():
            if entered_text == region.lower():
                var.set(True)  # Coche la case à cocher correspondante
                update_recap(check_vars, regions, recap_cases)  # Met à jour le récapitulatif
                break

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
    
########### MODIF CHAIMA
    # class ToolTip(object):
    #      # Initialisation sans changement
    #     def __init__(self, widget):
    #         self.widget = widget
    #         self.tipwindow = None
    #         self.x = self.y = 0

    #     def show_tip(self, text):
    #         "Affiche le texte du tooltip"
    #         if self.tipwindow or not text:
    #             return
    #         x = self.widget.winfo_rootx() + 25
    #         y = self.widget.winfo_rooty() + self.widget.winfo_height() + 20
    #         self.tipwindow = tw = tk.Toplevel(self.widget)
    #         tw.wm_overrideredirect(True)
    #         tw.wm_geometry("+%d+%d" % (x, y))
    #         label = tk.Label(tw, text=text, justify=tk.LEFT,
    #                         background="lightyellow", relief=tk.SOLID, borderwidth=1,
    #                         font=("Arial", "10", "normal"))
    #         label.pack(ipadx=1, ipady=1)

    #     def hide_tip(self):
    #         if self.tipwindow:
    #             self.tipwindow.destroy()
    #             self.tipwindow = None

    # # Modification de la façon dont vous liez l'événement et appelez show_tip/hide_tip
    # def enter(event):
    #     tooltip.show_tip("Martin DENIAU\nChaïma JAIDANE\nCharlotte KRUZIC\nZoé MARQUIS\nValentin MASSEBEUF\nClément OBERHAUSER")

    # def leave(event):
    #     tooltip.hide_tip()

########### FIN MODIF CHAIMA
    frame_root = tk.Frame(fenetre)
    frame_root.pack(expand = 1, fill = "both")

    frame_titre = tk.Frame(frame_root)
    frame_titre.grid(row=0, column=0, sticky="nsew", padx=30, pady=0)

    label = tk.Label(frame_titre, text="Acquisition des régions fonctionnelles dans les génomes", font=("Arial", 25), fg=theme.couleur_frame)
    label.grid(row=0, column=0, sticky="ew")
######### MODIF CHAIMA
    # label_info = tk.Label(frame_titre, text="i", font=("Arial", 14, "bold"), fg="white", bg="white",
    #                     width=2, height=1, borderwidth=2)
    # label_info.grid(row=0, column=1, padx=5, pady=20, sticky="e")
    
    # tooltip = ToolTip(label_info)
    # label_info.bind("<Enter>", enter)
    # label_info.bind("<Leave>", leave)
  
    
    image = tk.PhotoImage(file="image/info-2.png")
    label_info = tk.Label(frame_titre,image=image, font=("Arial", 14, "bold"), fg="white", bg="white",
                      width=50, height=50, borderwidth=2)
    label_info.config(image=image)
    label_info.grid(row=0, column=1, padx=0, pady=20, sticky="e")

    # Création d'un label pour le texte du tooltip qui sera affiché ou caché
    tooltip_text = tk.Label(frame_titre, text="Martin DENIAU\nChaïma JAIDANE\nCharlotte KRUZIC\nZoé MARQUIS\nValentin MASSEBEUF\nClément OBERHAUSER", fg="white", bg="lightyellow", bd=1, relief="solid")
    tooltip_text.grid(row=0, column=2, sticky="e")
    tooltip_text.grid_remove()  # Cacher initialement le tooltip

    # Fonction pour montrer le tooltip
    def show_tooltip(event):
        tooltip_text.grid()  # Affiche le texte

    # Fonction pour cacher le tooltip
    def hide_tooltip(event):
        tooltip_text.grid_remove()  # Cache le texte

    # Liens d'événements
    label_info.bind("<Enter>", show_tooltip)
    label_info.bind("<Leave>", hide_tooltip)

    # tooltip = ToolTip(label_info)  # Vous devez créer tooltip avec label_info comme widget cible
    # label_info.bind("<Enter>", enter)
    # label_info.bind("<Leave>", leave)
    
    

######### FIN MODIF CHAIMA

    frame_titre.rowconfigure(0, weight=1)
    frame_titre.columnconfigure(0, weight=20)
    frame_titre.columnconfigure(1, weight=1)

    frame_principal = tk.Frame(frame_root)
    frame_principal.grid(row=1, column=0, sticky="nsew", padx=30, pady=(0,30))

    frame_principal.grid_columnconfigure(0, weight=2)
    frame_principal.grid_columnconfigure(1, weight=5)
    frame_principal.grid_rowconfigure(0, weight=9)
    frame_principal.grid_rowconfigure(1, weight=1)

    frame_root.rowconfigure(0, weight=1)
    frame_root.rowconfigure(1, weight=10)
    frame_root.columnconfigure(0, weight=1)

    ## GAUCHE : ARBO + RECAP
    frame_arbo = tk.LabelFrame(frame_principal, text="Arborescence", relief="raised",bg=theme.couleur_frame, foreground="white")
    frame_arbo.grid(row=0, column=0, sticky="nsew", padx=(0,10), pady=(0, 10))

    frame_recap = tk.LabelFrame(frame_principal, text="Récapitulatif", relief="raised", bg=theme.couleur_frame, foreground="white")
    frame_recap.grid(row=1, column=0, sticky="nsew", padx=(0,10), pady=(10,0))

##### arbo
    #recap_arbo = tk.Label(frame_recap, text="Arborescence:\n",foreground="white",relief="solid", borderwidth=2, anchor="w")
    #recap_arbo.grid(row=0, column=0, sticky="nsew")
    f_arbo = tk.Frame(frame_recap)
    f_arbo.grid(row=0, column=0, sticky="nw")

    recap_arbo = tk.Canvas(f_arbo, bg="pink")
    recap_arbo.pack(side="left", fill="both", expand=True)
    #recap_arbo.grid(row=0, column=0, sticky="nw")
    text_recap_arbo = recap_arbo.create_text(20,20,text="Dossiers:", fill="black", anchor="nw")


##### cases
    f_cases = tk.Frame(frame_recap)
    f_cases.grid(row=0, column=1, sticky="nw")

    recap_cases = tk.Canvas(f_cases, bg="lightblue")
    #recap_cases.grid(row=0, column=1, sticky="nw")
    recap_cases.pack(side="left", fill="both", expand=True)
    text_recap_cases = recap_cases.create_text(20,20,text="Régions:", fill="black", anchor="nw")

    # Créer une scrollbar pour la direction verticale
    scrollbar_y = tk.Scrollbar(f_cases, orient="vertical", command=recap_cases.yview)
    scrollbar_y.pack(side="right", fill="y")

    # Connecter la scrollbar à la direction verticale du Canvas
    recap_cases.configure(yscrollcommand=scrollbar_y.set)

    #recap_cases = tk.Label(frame_recap, text="Régions:\n",foreground="white",relief="solid", borderwidth=2, anchor="w")
    #recap_cases.grid(row=0, column=1, sticky="nsew")

    frame_recap.rowconfigure(0, weight=1)
    frame_recap.grid_columnconfigure(0, weight=1)
    frame_recap.grid_columnconfigure(1, weight=1)

    ## DROITE : CHOIX + LOG + BOUTON + PROGRESS BAR
    ## haut = choix + log, bas = progress bar + bouton
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

    ### choix
    frame_cases = tk.LabelFrame(frame_choix, text="Sélection des régions", bg=theme.couleur_frame, fg="white")    
    frame_cases.grid(row=0, column=0, sticky="nsew", pady=(0,5))
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
    # frame_saisie = tk.Frame(frame_choix, bg=theme.couleur_frame)
    # frame_saisie.grid(row=1, column=0, sticky="nsew")
    # #frame_saisie.pack()
    # zone_texte = tk.Entry(frame_saisie, textvariable=zone_entre)
    # zone_texte.pack(expand=1)
   
############# MODIF CHAIMA
    def configure_grid():
        frame_width = frame_cases.winfo_width()  # Obtention de la largeur de frame_cases
        num_columns = 5  # Nombre souhaité de colonnes, sans compter la colonne pour "All"
        # Assurez-vous que la colonne pour "All" est considérée séparément
        column_width = frame_width // (num_columns + 1)
        

        # Configuration de la largeur des colonnes pour un espacement équitable
        for c in range(num_columns + 1):  # +1 pour inclure la colonne "All"
            frame_cases.grid_columnconfigure(c, minsize=column_width)

        # Positionnement des cases à cocher
        r = 0  # Ligne de départ
        c = 0  # Colonne de départ
        for region in regions:
            var = tk.BooleanVar(value=False)
            variables[region] = var
            #check_vars.append(var)

            if region == "All":  # Traiter "All" séparément
                #cb = tk.Checkbutton(frame_cases, text=region, variable=var,background=theme.couleur_frame)#)
                cb = ttk.Checkbutton(frame_cases, text=region, variable=var, style="CustomCheckbutton.TCheckbutton")
                # Placer "All" dans sa propre colonne à l'extrémité droite
                cb.grid(row=0, column=num_columns, rowspan=2, sticky="w") 
                checkboxes[region] = cb
            else:
                cb = ttk.Checkbutton(frame_cases, text=region, variable=check_vars[region], 
                                     command=lambda: update_recap(check_vars, regions, recap_cases),style="CustomCheckbutton.TCheckbutton")#,background=theme.couleur_frame)
                                     # #,
                # style = ttk.Style()
                # style.configure("CustomCheckbutton.TCheckbutton", background=theme.couleur_frame, foreground="white")
                style = ttk.Style()
                style.map("CustomCheckbutton.TCheckbutton",
                        background=[("!disabled", theme.couleur_frame)],foreground=[("!disabled", "white")])


                cb.grid(row=r, column=c, sticky="wns")  # Ajoute un espacement horizontal
                checkboxes[region] = cb

                c += 1
                if c >= num_columns:  # Passage à la ligne suivante après num_columns cases (ne compte pas "All")
                    c = 0
                    r += 1
    def configure_grid():
        frame_width = frame_cases.winfo_width()
        num_columns = 5
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
                cb.grid(row=0, column=num_columns, sticky="w", padx=0, pady=0)
                checkboxes[region] = cb
            else:
                cb = ttk.Checkbutton(frame_cases, text=region, variable=check_vars[region],
                                    command=lambda: update_recap(check_vars, regions, recap_cases), style="CustomCheckbutton.TCheckbutton")
                cb.grid(row=r, column=c, sticky="wns", padx=0, pady=5)
                checkboxes[region] = cb
                style = ttk.Style()
                style.configure("CustomCheckbutton.TCheckbutton", background=theme.couleur_frame, foreground="white")
                #style.map("CustomCheckbutton.TCheckbutton",background=[("!disabled", theme.couleur_frame)],foreground=[("!disabled", "white")])

                c += 1
                if c >= num_columns:
                    c = 0
                    r += 1
        variables["All"].trace("rwua", lambda *args: all_command())
        frame_saisie = tk.Frame(frame_cases, bg=theme.couleur_frame)
        # Placer la frame_saisie en bas à gauche
        frame_saisie.grid(row=r-1, column=num_columns, sticky="nsew")
        zone_texte = tk.Entry(frame_saisie, textvariable=zone_entre)
        zone_texte.pack(expand=True)
        zone_texte.bind('<KeyRelease>', on_text_entry)


        # Ajuster la hauteur de la frame_saisie pour correspondre aux autres éléments si nécessaire
        frame_saisie.grid_rowconfigure(0, minsize=20)  # Aju
   # Réactive la zone de texte sinon

        

    
    frame_cases.rowconfigure(0, weight=1)
    frame_cases.rowconfigure(1, weight=1)
    frame_cases.grid_columnconfigure(0, weight=1)
    frame_cases.grid_columnconfigure(1, weight=1)
    frame_cases.grid_columnconfigure(2, weight=1)
    frame_cases.grid_columnconfigure(3, weight=1)
    frame_cases.grid_columnconfigure(4, weight=1)
    frame_cases.grid_columnconfigure(5, weight=1)

    # Appel de configure_grid une fois que la fenêtre est affichée pour avoir les bonnes dimensions
    fenetre.after(100, configure_grid)
    
    
################### FIN MODIF CHAIMA

    # test=tk.BooleanVar()
    # check1=tk.Checkbutton(frame_cases, text="test", variable=test)
    # check1.pack(anchor="w")

    frame_log = tk.LabelFrame(frame_haut, text="log",bg=theme.couleur_frame)
    frame_log.grid(row=1, column=0, sticky="nsew", padx=0, pady=(10,0))

    term = terminal.Terminal(frame_log, bg="black")
    term.pack(fill="both", expand=True)
    
    ## BAS
    frame_bas = tk.Frame(frame_principal, background=theme.couleur_frame, relief="solid", borderwidth=2)
    frame_bas.grid(row=1, column=1, sticky="nsew", padx=(10,0), pady=(10,0))

    label = tk.Label(frame_bas, text="loadbar") 

    # Configuration initiale de la progression
    progress_running = False

    style = ttk.Style()
    style.theme_use('clam')  # Choix d'un thème, ici 'clam'
    style.configure("Custom.Horizontal.TProgressbar", troughcolor=theme.couleur_frame, background="lightblue")  # Personnalisation des couleurs


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
    folder_structure = folder.create_folder_structure(root_dir)

    #folder_tree = folder.FolderTree(frame_arbo, folder_structure, recap_arbo)
    folder_tree = folder.FolderTree(frame_arbo, folder_structure, text_recap_arbo, recap_arbo)
    folder_tree.pack(expand=True, fill=tk.BOTH)
    change_treeview_colors(folder_tree, text_color=theme.couleur_texte, select_color= "lightblue", background_color=theme.couleur_frame)
    theme.configurer_background(frame_root)

    fenetre.mainloop()

