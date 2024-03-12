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

# class FolderTree(tk.Frame):

#     def __init__(self, master, folder_structure, dict_path, recap, canvas_arbo, *args, **kwargs):
#         super().__init__(master, *args, **kwargs)
#         self.selected_items = set()  # Ensemble pour garder une trace des éléments sélectionnés

#         # Configuration du style pour Treeview
#         style = ttk.Style()
#         style.configure("Custom.Treeview", background="#d3d3d3", fieldbackground="#d3d3d3", foreground="black")
#         style.map("Custom.Treeview", background=[('selected', '#347083')])

#         self.recap_text = recap
#         self.canvas_arbo = canvas_arbo
#         self.dict_path = dict_path
#         #self.recap_text = tk.Label(labelframe_recap)
#         #self.recap_text.pack()
#         #self.recap_text.pack(side=tk.LEFT, fill="both", expand=True)
#         #self.recap_scrollbar = tk.Scrollbar(labelframe_recap, command=self.recap_text.yview)
#         #self.recap_scrollbar.pack(side=tk.RIGHT, fill="y")
#         # change_scrollbar_color(self.recap_scrollbar, "white", "white", "white")

#         #self.recap_text.configure(yscrollcommand=self.recap_scrollbar.set)
#         #self.recap_text.bind("<Key>", lambda e: "break")  # Désactiver l'édition

#         # Utilisation du style personnalisé pour le Treeview
#         self.tree = ttk.Treeview(self, style="Custom.Treeview", selectmode="none", columns=("fullpath",), show="tree")
#         self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#         self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
#         self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
#         self.tree.configure(yscrollcommand=self.scrollbar_y.set)

#         self.populate_tree(folder_structure)
#         self.tree.bind("<1>", self.on_single_click)  # Simple clic pour ouvrir/fermer un dossier
#         self.tree.bind("<Double-1>", self.on_double_click)  # Double clic pour sélectionner un dossier

#     def on_item_click(self, event):
#         item_id = self.tree.identify_row(event.y)
#         if item_id:
#             # Basculer la sélection/désélection de l'élément
#             if item_id in self.selected_items:
#                 self.selected_items.remove(item_id)
#                 self.tree.item(item_id, tags=())
#             else:
#                 self.selected_items.add(item_id)
#                 self.tree.item(item_id, tags=("selected",))
            
#             self.update_recap()  # Mettre à jour le récapitulatif
            
#             # Mise à jour visuelle pour montrer la sélection (optionnel)
#             self.tree.tag_configure("selected", background="lightblue")

#     def update_recap(self):
#         # Effacer le contenu précédent et afficher les éléments sélectionnés
#         #self.recap_text.delete('1.0', tk.END)
#         recap_text = ""

#         for item_id in self.selected_items:
#             print(str(self.tree.item(item_id)['text']))
#             recap_text += self.dict_path[self.tree.item(item_id)['text']]+"\n"

#         self.canvas_arbo.itemconfig(self.recap_text, text="Dossier:\n"+recap_text)

#     def populate_tree(self, folder_structure, parent=""):
#         for folder in folder_structure:
#             folder_id = self.tree.insert(parent, "end", text=folder['name'], open=False)
#             if 'children' in folder:
#                 self.populate_tree(folder['children'], folder_id)


# class FolderTree(tk.Frame):
#     def __init__(self, master, folder_structure, dict_path, recap, canvas_arbo, *args, **kwargs):
#         super().__init__(master, *args, **kwargs)
#         self.selected_items = set()
#         self.dict_path = dict_path
#         self.recap_text = recap
#         self.canvas_arbo = canvas_arbo
        
#         style = ttk.Style()
#         style.configure("Custom.Treeview", background="#d3d3d3", fieldbackground="#d3d3d3", foreground="black")
#         style.map("Custom.Treeview", background=[('selected', '#347083')])

#         self.tree = ttk.Treeview(self, style="Custom.Treeview", selectmode="none", columns=("fullpath",), show="tree")
#         self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

#         self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
#         self.scrollbar_y.pack(side=tk.RIGHT, fill="y")
#         self.tree.configure(yscrollcommand=self.scrollbar_y.set)

#         self.populate_tree(folder_structure)
#         self.tree.bind("<1>", self.on_single_click)
#         self.tree.bind("<Double-1>", self.on_double_click)

#     def on_single_click(self, event):
#         # Cette méthode gère maintenant l'ouverture/fermeture des dossiers
#         item_id = self.tree.identify_row(event.y)
#         if item_id:
#             is_open = self.tree.item(item_id, "open")
#             self.tree.item(item_id, open=not is_open)

#     def on_double_click(self, event):
#         # Cette méthode gère maintenant la sélection des dossiers
#         item_id = self.tree.identify_row(event.y)
#         if item_id:
#             if item_id in self.selected_items:
#                 self.selected_items.remove(item_id)
#                 self.tree.item(item_id, tags=())
#             else:
#                 self.selected_items.add(item_id)
#                 self.tree.item(item_id, tags=("selected",))
#             self.update_recap()

#     def update_recap(self):
#         recap_text = "Dossier:\n"
#         for item_id in self.selected_items:
#             item_name = self.tree.item(item_id)['text']
#             item_path = self.dict_path[item_name]
#             recap_text += f"{item_path}\n"
#         self.canvas_arbo.itemconfig(self.recap_text, text=recap_text)

#     def populate_tree(self, folder_structure, parent=""):
#         for folder in folder_structure:
#             folder_id = self.tree.insert(parent, "end", text=folder['name'], open=False, tags=('folder',))
#             if 'children' in folder:
#                 self.populate_tree(folder['children'], folder_id)

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
            # Supprime le chemin racine pour ne montrer que le chemin relatif
            item_path = self.dict_path[item_name].replace("chemin/de/la/racine/", "")
            recap_text += f"{item_path}\n"
        self.canvas_arbo.itemconfig(self.recap_text, text=recap_text)

    def populate_tree(self, folder_structure, parent=""):
        for folder in folder_structure:
            folder_id = self.tree.insert(parent, "end", text=folder['name'], open=False, tags=('folder',))
            if 'children' in folder:
                self.populate_tree(folder['children'], folder_id)
