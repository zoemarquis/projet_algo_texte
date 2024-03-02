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

# class FolderTree(tk.Frame):
#     def __init__(self, master, folder_structure, labelframe_recap, *args, **kwargs):
#         super().__init__(master, *args, **kwargs)
#         self.recap = tk.Label(labelframe_recap, text="Selected Folder: None", foreground="white", anchor="w")
#         self.recap.pack(fill="x")

#         self.tree = ttk.Treeview(self)
#         self.tree = ttk.Treeview(self, columns=("fullpath",), show="tree")
#         self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

#         self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
#         self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
#         self.tree.configure(yscrollcommand=self.scrollbar_y.set)

#         # self.scrollbar_x = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
#         # self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
#         # self.tree.configure(xscrollcommand=self.scrollbar_x.set)
        
#         self.populate_tree(folder_structure)

#         self.tree.bind("<Button-1>", self.on_item_click)
#         self.tree.bind("<ButtonRelease-1>", self.on_item_select)

#     def on_item_select(self, event):
#         selected_item_id = self.tree.focus()
#         selected_item = self.tree.item(selected_item_id)
#         selected_folder_name = selected_item['text']
#         self.recap.config(text=f"Selected Folder: {selected_folder_name}")

#     def populate_tree(self, folder_structure, parent=""):
#         for folder in folder_structure:
#             folder_id = self.tree.insert(parent, "end", text=folder['name'], open=False)
#             if 'children' in folder:
#                 self.populate_tree(folder['children'], folder_id)

#     def on_item_click(self, event):
#         item_id = self.tree.identify_row(event.y)
#         if item_id:
#             is_open = self.tree.item(item_id, 'open')
#             if is_open:
#                 self.tree.item(item_id, open=False)
#             else:
#                 self.tree.item(item_id, open=True)


###### MODIF CHAIMA POUR SELECTIONNER PLUSIEURS APRES A DECIDER
class FolderTree(tk.Frame):

    def __init__(self, master, folder_structure, labelframe_recap, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.selected_items = set()  # Ensemble pour garder une trace des éléments sélectionnés

        # Configuration du style pour Treeview
        style = ttk.Style()
        style.configure("Custom.Treeview", background="#d3d3d3", fieldbackground="#d3d3d3", foreground="black")
        style.map("Custom.Treeview", background=[('selected', '#347083')])

        self.recap_text = tk.Text(labelframe_recap, height=10, width=50)
        self.recap_text.pack(side=tk.LEFT, fill="both", expand=True)
        self.recap_scrollbar = tk.Scrollbar(labelframe_recap, command=self.recap_text.yview)
        self.recap_scrollbar.pack(side=tk.RIGHT, fill="y")
        self.recap_text.configure(yscrollcommand=self.recap_scrollbar.set)
        self.recap_text.bind("<Key>", lambda e: "break")  # Désactiver l'édition

        # Utilisation du style personnalisé pour le Treeview
        self.tree = ttk.Treeview(self, style="Custom.Treeview", selectmode="none", columns=("fullpath",), show="tree")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.scrollbar_y.set)

        self.populate_tree(folder_structure)
        self.tree.bind("<Button-1>", self.on_item_click)  # Utiliser on_item_click pour gérer la sélection


    def on_item_click(self, event):
        item_id = self.tree.identify_row(event.y)
        if item_id:
            # Basculer la sélection/désélection de l'élément
            if item_id in self.selected_items:
                self.selected_items.remove(item_id)
                self.tree.item(item_id, tags=())
            else:
                self.selected_items.add(item_id)
                self.tree.item(item_id, tags=("selected",))
            
            self.update_recap()  # Mettre à jour le récapitulatif
            
            # Mise à jour visuelle pour montrer la sélection (optionnel)
            self.tree.tag_configure("selected", background="lightblue")

    def update_recap(self):
        # Effacer le contenu précédent et afficher les éléments sélectionnés
        self.recap_text.delete('1.0', tk.END)
        for item_id in self.selected_items:
            folder_name = self.tree.item(item_id)['text']
            self.recap_text.insert(tk.END, folder_name + '\n')

    def populate_tree(self, folder_structure, parent=""):
        for folder in folder_structure:
            folder_id = self.tree.insert(parent, "end", text=folder['name'], open=False)
            if 'children' in folder:
                self.populate_tree(folder['children'], folder_id)
