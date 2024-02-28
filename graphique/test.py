import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("LabelFrame Example")

# Création d'un LabelFrame
label_frame = ttk.LabelFrame(root, text="My LabelFrame")
label_frame.pack(padx=10, pady=10)

# Ajout de widgets dans le LabelFrame
label = ttk.Label(label_frame, text="Hello, LabelFrame!")
label.pack(padx=10, pady=10)

button = ttk.Button(label_frame, text="Click Me")
button.pack(padx=10, pady=10)

root.mainloop()
