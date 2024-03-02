import os
import tkinter as tk
from tkinter import ttk 

import folder
import theme 
import terminal

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

    style = ttk.Style(fenetre)
    #style.configure(".", font=("Comic Sans MS", 12))

    fenetre.title("GENBANK PARSER")
    fenetre.geometry("1300x800")

    fenetre.update()
    width = fenetre.winfo_width() 
    height = fenetre.winfo_height()
    
########### MODIF CHAIMA
    class ToolTip(object):
        def __init__(self, widget):
            self.widget = widget
            self.tipwindow = None
            self.x = self.y = 0
            self.text = ""

        def show_tip(self, text):
            "Affiche le texte du tooltip"
            self.text = text
            if self.tipwindow or not self.text:
                return
            x = self.widget.winfo_rootx() + 20  # Position horizontale légèrement à droite du widget
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 20  # Position verticale juste en dessous
            self.tipwindow = tw = tk.Toplevel(self.widget)
            tw.wm_overrideredirect(True)
            tw.wm_geometry("+%d+%d" % (x, y))
            label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                            background="lightyellow", relief=tk.SOLID, borderwidth=1,
                            font=("Arial", "10", "normal"))
            label.pack(ipadx=4, ipady=4)

            # Ajuster la position pour s'assurer que l'infobulle ne dépasse pas du cadre de la fenêtre
            tw.update_idletasks()
            tw_width = tw.winfo_width()
            tw_height = tw.winfo_height()
            screen_width = tw.winfo_screenwidth()
            screen_height = tw.winfo_screenheight()
            if x + tw_width > screen_width:
                x = screen_width - tw_width
            if y + tw_height > screen_height:
                y = screen_height - tw_height
            tw.wm_geometry("+%d+%d" % (x, y))

        def hide_tip(self):
            if self.tipwindow:
                self.tipwindow.destroy()
                self.tipwindow = None

    def enter(event):
        tooltip.show_tip("Martin DENIAU\nChaïma JAIDANE\nCharlotte KRUZIC\nZoé MARQUIS\nValentin MASSEBEUF\nClément OBERHAUSER")

    def leave(event):
        tooltip.hide_tip()
########### FIN MODIF CHAIMA
    
    frame_root = tk.Frame(fenetre)
    frame_root.pack(expand = 1, fill = "both")

    frame_titre = tk.Frame(frame_root)
    frame_titre.grid(row=0, column=0, sticky="nsew", padx=30, pady=0)

    label = tk.Label(frame_titre, text="Acquisition des régions fonctionnelles dans les génomes", font=("Arial", 25), fg=theme.couleur_frame)
    label.grid(row=0, column=0, sticky="ew")

######### MODIF CHAIMA
    
    label_info = tk.Label(frame_titre, text="i", font=("Arial", 14, "bold"), fg="white", bg="white",
                        width=2, height=1, borderwidth=2, relief="solid")
    label_info.grid(row=0, column=1, padx=5, pady=20, sticky="e")
    
    tooltip = ToolTip(label_info)
    label_info.bind("<Enter>", enter)
    label_info.bind("<Leave>", leave)
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
    frame_cases = tk.Frame(frame_choix, bg=theme.couleur_frame)
    frame_cases.grid(row=0, column=0, sticky="nsew", pady=(0,5))
    # case à cocher
    regions = ["CDS", "ncRNA", "3'UTR", "Centromère", "rRNA", "5'UTR",
               "Intron", "Telomère", "Mobile élément", "tRNA", "All"]

    # Dictionnaires pour stocker les variables et les widgets des cases à cocher
    variables = {}
    checkboxes = {}

    # Zone de saisie
    zone_entre = tk.StringVar()
    frame_saisie = tk.Frame(frame_choix, bg=theme.couleur_frame)
    frame_saisie.grid(row=1, column=0, sticky="nsew")
    #frame_saisie.pack()
    zone_texte = tk.Entry(frame_saisie, textvariable=zone_entre)
    zone_texte.pack(expand=1)
   
    # # Création des cases à cocher
    # r = 1
    # c = 0
    # for i in regions:
    #     var = tk.BooleanVar(value=False)
    #     cb = tk.Checkbutton(frame_cases, text=i, variable=var)
    #     #cb.pack(anchor="w")
    #     if i == "All":
    #         cb.grid(row=2, column=5)
    #     else :
    #         cb.grid(row=r, column=c)
    #     c+=1
    #     if c >= 5 :
    #         c = 0
    #         r += 1
    #     variables[i] = var
    #     checkboxes[i] = cb

    # variables["All"].trace("w", lambda *args: all_command())

############# MODIF CHAIMA
    def configure_grid():
        frame_width = frame_cases.winfo_width()  # Obtention de la largeur de frame_cases
        num_columns = 5  # Nombre souhaité de colonnes, sans compter la colonne pour "All"
        # Assurez-vous que la colonne pour "All" est considérée séparément
        column_width = frame_width // (num_columns + 1)  # Largeur disponible pour chaque colonne, +1 pour "All"

        # Configuration de la largeur des colonnes pour un espacement équitable
        for c in range(num_columns + 1):  # +1 pour inclure la colonne "All"
            frame_cases.grid_columnconfigure(c, minsize=column_width)

        # Positionnement des cases à cocher
        r = 0  # Ligne de départ
        c = 0  # Colonne de départ
        for region in regions:
            var = tk.BooleanVar(value=False)
            variables[region] = var

            if region == "All":  # Traiter "All" séparément
                cb = tk.Checkbutton(frame_cases, text=region, variable=var, background=theme.couleur_frame)
                # Placer "All" dans sa propre colonne à l'extrémité droite
                cb.grid(row=0, column=num_columns, rowspan=2, sticky="w") 
                checkboxes[region] = cb
            else:
                cb = tk.Checkbutton(frame_cases, text=region, variable=var, background=theme.couleur_frame)
                cb.grid(row=r, column=c, sticky="wns")  # Ajoute un espacement horizontal
                checkboxes[region] = cb

                c += 1
                if c >= num_columns:  # Passage à la ligne suivante après num_columns cases (ne compte pas "All")
                    c = 0
                    r += 1
        variables["All"].trace("rwua", lambda *args: all_command())

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

    loadbar = ttk.Progressbar(frame_bas, orient='horizontal', mode='determinate')
    loadbar.pack(fill='x', expand=True)
    loadbar.pack(ipady=8)

    #style = ttk.Style()
    style.map("Custom.TButton",
              background=[("active", theme.couleur_frame), ("!disabled", theme.couleur_frame)],
              foreground=[("!disabled", "white")],
              relief = "groove")

    bouton = ttk.Button(frame_bas, text="Start", command=toggle_progress, style="Custom.TButton")
    bouton.pack()
    bouton.bind("<Enter>", change_cursor)
    
    frame_bas.rowconfigure(0, weight=1)
    frame_bas.rowconfigure(1, weight=1)
    frame_bas.columnconfigure(0, weight=1)

    #style = ttk.Style()
    #style.theme_use("classic")  # Changer le thème du style, vous pouvez utiliser "clam", "alt", "default", "classic", etc.
    
    # Changer l'apparence du Treeview
    style.configure("Treeview", rowheight=25)
    style.map("Treeview", background=[('selected', '#347083')])

    root_dir = "./Results"
    folder_structure = folder.create_folder_structure(root_dir)

    folder_tree = folder.FolderTree(frame_arbo, folder_structure, frame_recap)
    folder_tree.pack(expand=True, fill=tk.BOTH)
    change_treeview_colors(folder_tree, text_color=theme.couleur_texte, select_color= "lightblue", background_color=theme.couleur_frame)
    theme.configurer_background(frame_root)

    fenetre.mainloop()

