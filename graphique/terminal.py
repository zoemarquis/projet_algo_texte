import os
import tkinter as tk
from tkinter import ttk 

class Terminal(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.canvas = tk.Canvas(self, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.text_lines = []
        self.line_height = 20
        self.max_lines = int(self.canvas.winfo_height() / self.line_height)
        
    def write(self, text):
        # if len(self.text_lines) >= self.max_lines:
        #     self.canvas.delete(self.text_lines.pop(0))
        
        y = len(self.text_lines) * self.line_height
        text_id = self.canvas.create_text(5, y, anchor="nw", text=text, fill="white", font=("Courier", 12))
        self.text_lines.append(text_id)

        self.canvas.update_idletasks()  # Ajout de cette ligne pour forcer la mise à jour du Canvas
