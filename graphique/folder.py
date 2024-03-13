import os
import tkinter as tk
from tkinter import ttk 
import theme

def create_folder_structure(root_dir):
    folder_structure = []
    dict_path = {}
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        if os.path.isdir(item_path):
            folder = {"name": item}
            dict_path[item] = item_path
            subfolders, subdict = create_folder_structure(item_path)
            if subfolders:
                folder["children"] = subfolders
                dict_path.update(subdict)
            folder_structure.append(folder)
    return folder_structure,dict_path

def change_scrollbar_color(scrollbar, background_color, trough_color, border_color):
    style = ttk.Style()
    style.configure("Custom.Vertical.TScrollbar", background=background_color, troughcolor=trough_color, bordercolor=border_color)

class FolderTree(tk.Frame):
    def __init__(self, master, folder_structure, dict_path, recap, canvas_arbo, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.selected_items = set()
        self.dict_path = dict_path
        self.recap_text = recap
        self.canvas_arbo = canvas_arbo
        
        style = ttk.Style()
        style.configure("Custom.Treeview", background="#d3d3d3", fieldbackground="#d3d3d3", foreground="black")
        # Configure le style pour les éléments sélectionnés avec une couleur de fond spécifique
        style.map("Custom.Treeview", background=[('selected', 'lightblue')])

        self.tree = ttk.Treeview(self, style="Custom.Treeview", selectmode="browse", columns=("fullpath",), show="tree")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill="y")
        self.tree.configure(yscrollcommand=self.scrollbar_y.set)

        self.populate_tree(folder_structure)
        self.tree.bind("<1>", self.on_single_click)
        self.tree.bind("<Double-1>", self.on_double_click)

    def on_single_click(self, event):
        item_id = self.tree.identify_row(event.y)
        if item_id:
            is_open = self.tree.item(item_id, "open")
            self.tree.item(item_id, open=not is_open)

    def on_double_click(self, event):
        item_id = self.tree.identify_row(event.y)
        if item_id:
            if item_id in self.selected_items:
                self.selected_items.remove(item_id)
                # Utilise les tags pour enlever le style de surlignage
                self.tree.item(item_id, tags=())
            else:
                self.selected_items.add(item_id)
                # Utilise les tags pour appliquer le style de surlignage
                self.tree.item(item_id, tags=('selected',))
            self.update_recap()

    def update_recap(self):
        recap_text = "Dossier:\n"
        for item_id in self.selected_items:
            item_name = self.tree.item(item_id)['text']
            item_path = self.dict_path[item_name]
            recap_text += f"{item_path}\n"
        self.canvas_arbo.itemconfig(self.recap_text, text=recap_text)

    def populate_tree(self, folder_structure, parent=""):
        for folder in folder_structure:
            folder_id = self.tree.insert(parent, "end", text=folder['name'], open=False, tags=('folder',))
            if 'children' in folder:
                self.populate_tree(folder['children'], folder_id)
