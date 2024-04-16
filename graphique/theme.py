import tkinter as tk
from tkinter import ttk

couleur_frame = "#EDC18D"
# 535878" #556C96"#"#516079"#BE9CC7"#535878"
couleur_fond = "#313950"
# 1B3358"#516079#"#556C96"#1C2942"#1B3358"
couleur_texte = "red"  # "#313950"
# "white"
couleur_selection = "pink"

couleur_contraste = "lightblue"


def configurer_background(widget):
    assert isinstance(widget, (tk.Frame, tk.Label))
    widget.configure(bg=couleur_fond)
