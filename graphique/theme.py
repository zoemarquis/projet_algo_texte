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

# style.map("Custom.TButton",
#           background=[("active", theme.couleur_frame), ("!disabled", theme.couleur_frame)],
#           foreground=[("!disabled", "white")],
#           relief = "groove")


def configurer_background(widget):
    assert isinstance(widget, (tk.Frame, tk.Label))
    # style = ttk.Style()
    # style.theme_use("default")
    widget.configure(bg=couleur_fond)

    """
    if isinstance(widget, (tk.Tk, tk.Toplevel, tk.Frame, tk.Label, tk.Button)):
        widget.configure(
            bg=bg_principal if isinstance(widget, (tk.Tk, tk.Toplevel)) else bg_frame
        )
    elif isinstance(widget, (ttk.Frame, ttk.Label, ttk.Button)):
        style = ttk.Style()
        if isinstance(widget, ttk.Progressbar):
            style_name = "Custom.Horizontal.TProgressbar"
            style.configure(style_name, background=bg_frame)
            widget.configure(style=style_name)
        return  # Ne pas essayer de configurer le fond pour d'autres widgets ttk

    for child in widget.winfo_children():
        configurer_background(child, bg_principal, bg_frame)
    """


def change_button_style(bg, fg):
    # style = ttk.Style()
    # style.configure("Custom.TButton", background=bg, foreground=fg)
    return


# def change_label_frame_font(label_frame, font_name, font_size):
#     style = ttk.Style()
#     style.configure("Custom.TLabelframe.Label", font=(font_name, font_size))
