import os
import tkinter as tk
from tkinter import ttk 
import theme

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


def change_scrollbar_color(scrollbar, background_color, trough_color, border_color):
    style = ttk.Style()
    style.configure("Custom.Vertical.TScrollbar", background=background_color, troughcolor=trough_color, bordercolor=border_color)


###### MODIF CHAIMA POUR SELECTIONNER PLUSIEURS APRES A DECIDER
class FolderTree(tk.Frame):

    def __init__(self, master, folder_structure, recap, canvas_arbo, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.selected_items = set()  # Ensemble pour garder une trace des éléments sélectionnés

        # Configuration du style pour Treeview
        style = ttk.Style()
        style.configure("Custom.Treeview", background="#d3d3d3", fieldbackground="#d3d3d3", foreground="black")
        style.map("Custom.Treeview", background=[('selected', '#347083')])

        self.recap_text = recap
        self.canvas_arbo = canvas_arbo
        #self.recap_text = tk.Label(labelframe_recap)
        #self.recap_text.pack()
        #self.recap_text.pack(side=tk.LEFT, fill="both", expand=True)
        #self.recap_scrollbar = tk.Scrollbar(labelframe_recap, command=self.recap_text.yview)
        #self.recap_scrollbar.pack(side=tk.RIGHT, fill="y")
        # change_scrollbar_color(self.recap_scrollbar, "white", "white", "white")

        #self.recap_text.configure(yscrollcommand=self.recap_scrollbar.set)
        #self.recap_text.bind("<Key>", lambda e: "break")  # Désactiver l'édition

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
        #self.recap_text.delete('1.0', tk.END)
        recap_text = ""
        for i,option in enumerate(self.selected_items):
            if i % 2 == 0:  # Si c'est le début d'une nouvelle ligne
                if i != 0:  # Si ce n'est pas la première ligne
                    recap_text += ", \n"  # Ajouter un saut de ligne pour séparer les lignes
            else:
                recap_text += ", "  # Ajouter une virgule pour séparer les options
            recap_text += self.tree.item(option, "text")
        #self.recap_text.config(text="Arborescence:\n"+recap_text)
        self.canvas_arbo.itemconfig(self.recap_text, text="Arborescence:\n"+recap_text)


    def populate_tree(self, folder_structure, parent=""):
        for folder in folder_structure:
            folder_id = self.tree.insert(parent, "end", text=folder['name'], open=False)
            if 'children' in folder:
                self.populate_tree(folder['children'], folder_id)
