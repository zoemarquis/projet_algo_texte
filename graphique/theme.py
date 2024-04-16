import tkinter as tk
from tkinter import ttk

couleur_frame = "#5F90CB"
couleur_fond = "#151854"
couleur_texte = "#151854"
couleur_selection = "#048B9A"
couleur_contraste = "pink"
couleur_titre = "#C8E1FE"


def configurer_background(widget):
    assert isinstance(widget, (tk.Frame, tk.Label))
    widget.configure(bg=couleur_fond)
