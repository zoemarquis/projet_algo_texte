import os
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import tkinter.font as tkfont


class Log(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.text_widget = ScrolledText(self, bg="black", fg="white", wrap=tk.WORD, font=("Helvetica", 11), width=40, height=10)
        self.text_widget.pack(fill="both", expand=True)

        self.text_lines = []


    def update_scroll_region(self, event=None):
        canvas_height = self.canvas.winfo_height()
        text_height = len(self.text_lines) * self.line_height
        
        if canvas_height != text_height:
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def write(self, text):
        # if len(self.text_lines) >= self.max_lines:
        #     self.canvas.delete(self.text_lines.pop(0))

        self.text_widget.insert(tk.END, text + "\n")
        self.text_widget.see(tk.END)

        '''
        y = len(self.text_lines) * self.line_height
        text_id = self.canvas.create_text(
            5, y, anchor="nw", text=text, fill="white", font=("Courier", 12)
        )
        self.text_lines.append(text_id)

        self.canvas.update_idletasks()  # Ajout de cette ligne pour forcer la mise à jour du Canvas
        self.update_scroll_region()
        '''
