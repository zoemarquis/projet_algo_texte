import tkinter as tk
from tkinter import ttk

import theme


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.tipwindow = None
        self.x = self.y = 0
        self.text = text

        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event):
        self.show_tip(self.text)

    def leave(self, event):
        self.hide_tip()

    def show_tip(self, text):
        if self.tipwindow or not text:
            return
        x = self.widget.winfo_rootx() - 100
        y = self.widget.winfo_rooty() + self.widget.winfo_height()
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(
            tw,
            text=text,
            justify=tk.LEFT,
            background="lightyellow",
            relief=tk.SOLID,
            borderwidth=1,
            font=("Arial", 10, "normal"),
            foreground=theme.couleur_texte,
        )
        label.pack(ipadx=1, ipady=1)

    def hide_tip(self):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None


class Credits:
    def __init__(self, frame_parent, grid_row, grid_column):
        label_info = tk.Label(
            frame_parent,
            text="i",
            font=("Arial", 14, "bold"),
            fg="white",
            width=2,
            height=1,
            borderwidth=2,
        )
        label_info.grid(row=grid_row, column=grid_column, padx=10, pady=20, sticky="e")

        self.tooltip = ToolTip(
            label_info,
            "Martin DENIAU\nChaïma JAIDANE\nCharlotte KRUZIC\nZoé MARQUIS\nValentin MASSEBEUF\nClément OBERHAUSER",
        )
