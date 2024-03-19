import tkinter as tk
from tkinter import ttk

import theme


class ProgressBar:
    def __init__(self, frame_parent, fenetre, grid_row, grid_column):
        self.progress_running = False
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=theme.couleur_frame,
            background=theme.couleur_selection,
        )
        self.loadbar = ttk.Progressbar(
            frame_parent,
            orient="horizontal",
            mode="determinate",
            style="Custom.Horizontal.TProgressbar",
        )
        self.loadbar.grid(row=grid_row, column=grid_column, sticky="ewns", pady=(0, 30))
        self.fenetre = fenetre

        # bouton start / stop
        self.bouton = ttk.Button(
            frame_parent,
            text="Start",
            command=self.toggle_progress,
            style="Custom.TButton",
        )
        self.bouton.grid(row=grid_row + 1, column=grid_column)
        self.bouton.bind("<Enter>", self.change_cursor)

    def update_progress(self):
        current_value = self.loadbar["value"]
        if self.progress_running and current_value < 100:
            self.loadbar[
                "value"
            ] += 1  # Incrémente la valeur de la barre de progression
            # Planifie la mise à jour de la progression après un délai
            self.fenetre.after(
                100, self.update_progress
            )  # Continue à appeler update_progress toutes les 100 ms
        elif not self.progress_running or current_value == 100:
            self.progress_running = False  # Arrête la progression
            self.bouton.config(text="Start")  # Réinitialise le texte du bouton

    def toggle_progress(self):
        self.progress_running = (
            not self.progress_running
        )  # Bascule l'état de progression
        self.bouton.config(text="Stop" if self.progress_running else "Start")
        if self.progress_running:
            self.update_progress()

    # à placer dans theme plutot ?
    def change_cursor(self, event):
        event.widget.config(cursor="hand2")  # Change le curseur en main pointant
