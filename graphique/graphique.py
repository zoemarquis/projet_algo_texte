import os
import tkinter as tk
from tkinter import ttk  # Import correct de ScrolledText
# def configurer_background(widget, bg_frame="#282C34", bg_principal="#3C3F41"):
#     # Appliquer la couleur de fond principale au widget principal
#     if isinstance(widget, tk.Tk) or isinstance(widget, tk.Frame):
#         widget.configure(bg=bg_principal)
#     else:
#         # Appliquer la couleur de fond des frames
#         widget.configure(bg=bg_frame)
        
#     for child in widget.winfo_children():
#         configurer_background(child, bg_principal, bg_frame)

def configurer_background(widget, bg_frame="#282C34", bg_principal="#3C3F41"):
    # Appliquer la couleur de fond principale au widget principal
    if isinstance(widget, (tk.Tk, tk.Toplevel, tk.Frame, tk.Label, tk.Button)):
        widget.configure(bg=bg_principal if isinstance(widget, (tk.Tk, tk.Toplevel)) else bg_frame)
    elif isinstance(widget, (ttk.Frame, ttk.Label, ttk.Button)):
        # Pour les widgets ttk, la configuration du fond se fait via un style
        style = ttk.Style()
        # Vous pouvez créer un style personnalisé pour chaque type de widget ttk si nécessaire
        # Par exemple, pour les Progressbar:
        if isinstance(widget, ttk.Progressbar):
            style_name = "Custom.Horizontal.TProgressbar"
            style.configure(style_name, background=bg_frame)
            widget.configure(style=style_name)
        return  # Ne pas essayer de configurer le fond pour d'autres widgets ttk

    for child in widget.winfo_children():
        configurer_background(child, bg_principal, bg_frame)
        
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
frame_arbo = tk.Frame(frame_principal)
frame_arbo.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
label = tk.Label(frame_arbo, text="arbo")
label.pack()

def afficher_arborescence(frame, dossier, indentation=''):
    contenu = os.listdir(dossier)
    label = tk.Label(frame, text=indentation + f"/ {os.path.basename(dossier)}", fg="white", wraplength=300)  # Couleur du texte en blanc
    label.pack(anchor="w")
    for element in contenu:
        chemin = os.path.join(dossier, element)
        if os.path.isdir(chemin):
            sub_frame = tk.Frame(frame)
            sub_frame.pack(anchor="w")
            label = tk.Label(sub_frame, text=indentation + "   / " + element, fg="white", wraplength=300)  # Couleur du texte en blanc
            label.pack(anchor="w")
            afficher_arborescence(sub_frame, chemin, indentation + "       ")
'''
def on_vertical_scroll(*args):
    canvas.yview(*args)

def on_horizontal_scroll(*args):
    canvas.xview(*args)
'''

'''

canvas = tk.Canvas(frame_arbo, bg="black")
# scrollbar_vertical = ttk.Scrollbar(frame_arbo, orient="vertical", command=on_vertical_scroll)
# scrollbar_horizontal = ttk.Scrollbar(frame_arbo, orient="horizontal", command=on_horizontal_scroll)
# canvas.configure(yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set)
# scrollbar_vertical.pack(side="right", fill="y")
# scrollbar_horizontal.pack(side="bottom", fill="x")
canvas.pack(side="left", fill="both", expand=True)

# Créer un frame pour l'arborescence à l'intérieur du canevas
inner_frame = tk.Frame(canvas, bg="black")
canvas.create_window((0, 0), window=inner_frame, anchor="nw")
'''

# Remplacez 'chemin_du_dossier' par le chemin absolu du dossier que vous souhaitez explorer
chemin_du_dossier = './Results'
afficher_arborescence(dossier = chemin_du_dossier, frame = frame_arbo)

'''
# Configurer le canevas pour s'ajuster automatiquement lorsque son contenu change
def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
canvas.bind("<Configure>", on_configure)
'''


frame_recap = tk.Frame(frame_principal)
frame_recap.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
label = tk.Label(frame_recap, text="recap")
label.pack()

## contenu de droite
## haut - bas dans droite
frame_haut = tk.Frame(frame_principal)
frame_haut.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

frame_bas = tk.Frame(frame_principal)
frame_bas.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

### contenu de haut
frame_cases = tk.Frame(frame_haut)
frame_cases.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
label = tk.Label(frame_cases, text="cases")
label.pack()

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

def toggle_all(master_var, all_vars, all_checkboxes):
    # Si la case "All" est cochée, cochez toutes les cases et les désactivez
    # Si elle est décochée, décochez toutes les cases et les activez
    for region, var in all_vars.items():
        if region != "All":
            var.set(master_var.get())
            all_checkboxes[region].config(state=tk.DISABLED if master_var.get() else tk.NORMAL)

# Création des cases à cocher
for i in regions:
    var = tk.BooleanVar(value=False)
    cb = tk.Checkbutton(frame_cases, text=i, variable=var)
    cb.pack(anchor="w")
    variables[i] = var
    checkboxes[i] = cb

# Lien de la case "All" avec la fonction toggle_all
def all_command():
    toggle_all(variables["All"], variables, checkboxes)

variables["All"].trace("w", lambda *args: all_command())

# test=tk.BooleanVar()
# check1=tk.Checkbutton(frame_cases, text="test", variable=test)
# check1.pack(anchor="w")

frame_log = tk.Frame(frame_haut)
frame_log.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
label = tk.Label(frame_log, text="log")
label.pack()

frame_haut.rowconfigure(0, weight=1)
frame_haut.rowconfigure(1, weight=1)
frame_haut.columnconfigure(0, weight=1)

# ## contenu de bas
frame_loadbar = tk.Frame(frame_bas)
frame_loadbar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
label = tk.Label(frame_loadbar, text="loadbar")

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



configurer_background(frame_global)



fenetre.mainloop()