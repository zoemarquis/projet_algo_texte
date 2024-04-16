import tkinter as tk
from tkinter import ttk
from tkinter import font

#couleur_frame = "#5F90CB"
#couleur_frame = "#A3BBC8"
couleur_frame = "#86A8CF"
#couleur_fond = "#151854"
couleur_fond = "#022B42"
#couleur_fond = "#243F4D"
couleur_texte = "#151854"
couleur_selection = "#048B9A"
couleur_contraste = "pink"
couleur_titre = "#C8E1FE"

def configurer_background(widget):
    assert isinstance(widget, (tk.Frame, tk.Label))
    widget.configure(bg=couleur_fond)

