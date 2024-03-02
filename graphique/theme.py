import tkinter as tk
from tkinter import ttk 

# def configurer_background(widget, bg_frame="#282C34", bg_principal="#3C3F41"):
#     # Appliquer la couleur de fond principale au widget principal
#     if isinstance(widget, tk.Tk) or isinstance(widget, tk.Frame):
#         widget.configure(bg=bg_principal)
#     else:
#         # Appliquer la couleur de fond des frames
#         widget.configure(bg=bg_frame)
        
#     for child in widget.winfo_children():
#         configurer_background(child, bg_principal, bg_frame)

def configurer_background(widget, bg_frame="#1B3358", bg_principal="#1B3358"):
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
 