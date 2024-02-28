import os
import tkinter as tk
from tkinter import ttk 

def create_folder_structure(root_dir):
    folder_structure = []
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        if os.path.isdir(item_path):
            folder = {"name": item}
            subfolders = create_folder_structure(item_path)
            if subfolders:
                folder["children"] = subfolders
            folder_structure.append(folder)
    return folder_structure

class FolderTree(tk.Frame):
    def __init__(self, master, folder_structure, labelframe_recap, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.recap = tk.Label(labelframe_recap, text="Selected Folder: None", foreground="white")
        self.recap.pack()

        self.tree = ttk.Treeview(self)
        self.tree = ttk.Treeview(self, columns=("fullpath",), show="tree")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.scrollbar_y.set)

        # self.scrollbar_x = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        # self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        # self.tree.configure(xscrollcommand=self.scrollbar_x.set)
        
        self.populate_tree(folder_structure)

        self.tree.bind("<Button-1>", self.on_item_click)
        self.tree.bind("<ButtonRelease-1>", self.on_item_select)

    def on_item_select(self, event):
        selected_item_id = self.tree.focus()
        selected_item = self.tree.item(selected_item_id)
        selected_folder_name = selected_item['text']
        self.recap.config(text=f"Selected Folder: {selected_folder_name}")

    def populate_tree(self, folder_structure, parent=""):
        for folder in folder_structure:
            folder_id = self.tree.insert(parent, "end", text=folder['name'], open=False)
            if 'children' in folder:
                self.populate_tree(folder['children'], folder_id)

    def on_item_click(self, event):
        item_id = self.tree.identify_row(event.y)
        if item_id:
            is_open = self.tree.item(item_id, 'open')
            if is_open:
                self.tree.item(item_id, open=False)
            else:
                self.tree.item(item_id, open=True)
