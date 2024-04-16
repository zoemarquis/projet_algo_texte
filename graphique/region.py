import tkinter as tk
from tkinter import ttk
import theme


class Regions:
    def __init__(self, frame_parent, fenetre, recap):

        self.frame_parent = frame_parent
        self.variables = {}
        self.checkboxes = {}
        self.regions = [
            "CDS",
            "ncRNA",
            "3'UTR",
            "tRNA",
            "rRNA",
            "5'UTR",
            "Telomère",
            "Mobile élément",
            "Centromère",
            "All",
        ]
        self.check_vars = []
        self.check_vars = {
            option: tk.BooleanVar(value=False) for option in self.regions
        }
        self.zone_entre = tk.StringVar()
        self.additional_regions = set()
        self.recap = recap

        r, c = self.configure_grid()
        for i in range(r + 1):
            frame_parent.grid_rowconfigure(i, weight=1)
        for i in range(c + 1):
            frame_parent.grid_columnconfigure(i, weight=1)

        # fenetre.after(100, self.configure_grid()) # ?

    def configure_grid(self, num_columns=3):
        frame_width = self.frame_parent.winfo_height()
        column_width = frame_width // (num_columns + 2)

        total_spacing = frame_width - (num_columns * column_width)
        spacing_per_column = total_spacing // (num_columns)

        for c in range(num_columns):
            self.frame_parent.grid_columnconfigure(
                c, minsize=column_width, pad=spacing_per_column
            )

        r, c = 0, 0
        for region in self.regions:
            var = tk.BooleanVar(value=False)
            self.variables[region] = var

            if region == "All":
                cb = ttk.Checkbutton(
                    self.frame_parent,
                    text=region,
                    variable=var,
                    style="Custom.TCheckbutton",
                )
                cb.grid(row=r, column=0, sticky="w", padx=0, pady=0)
                self.checkboxes[region] = cb
            else:
                cb = ttk.Checkbutton(
                    self.frame_parent,
                    text=region,
                    variable=self.check_vars[region],
                    command=lambda: self.update_recap(self.check_vars, self.regions),
                    style="Custom.TCheckbutton",
                )
                cb.grid(row=r, column=c, sticky="wns", padx=0, pady=0)
                self.checkboxes[region] = cb

            c += 1
            if c >= num_columns:
                c = 0
                r += 1
        self.variables["All"].trace("rwua", lambda *args: self.all_command())

        # zone de texte
        frame_saisie = tk.Frame(self.frame_parent, bg=theme.couleur_frame)
        frame_saisie.grid(row=r, column=1, columnspan=2, sticky="nsew")
        zone_texte = tk.Entry(
            frame_saisie,
            textvariable=self.zone_entre,
            bg="#9FADE4",
            fg=theme.couleur_texte,
        )
        zone_texte.pack(expand=True, fill="both", padx=(0, 10), pady=20)
        zone_texte.bind("<Return>", self.on_text_entry)

        return r, c

    def all_command(self):
        all_checked = self.variables["All"].get()
        if all_checked:
            # Si "All" est cochée, mettez à jour toutes les variables et le texte de récapitulation
            for region, var in self.check_vars.items():
                var.set(True)
            # Liste toutes les régions sauf "All" pour le récapitulatif
            self.update_recap(
                self.check_vars, [region for region in self.regions if region != "All"]
            )
        else:
            # Si "All" est décochée, réinitialisez
            for region, var in self.check_vars.items():
                var.set(False)
            self.update_recap(self.check_vars, [])
        self.toggle_all(self.variables["All"], self.variables, self.checkboxes)

    ## Fonction pour la zone de texte
    def on_text_entry(self, event=None):
        entered_text = self.zone_entre.get().strip()  # Obtenez le texte entré
        if entered_text:  # Si du texte a été entré
            # Séparez le texte entré en régions basées sur le séparateur ";"
            entered_regions = entered_text.split(";")
            for entered_region in entered_regions:
                entered_region = entered_region.strip()
                # Supprimez les espaces superflus de chaque région
                region_found = (
                    False  # Indicateur pour savoir si la région a été trouvée et cochée
                )

                if entered_region.lower() == "all":
                    # Si le texte est "all", cochez toutes les cases
                    for region, var in self.check_vars.items():
                        var.set(True)
                    # self.update_recap(self.check_vars, self.regions)
                else:
                    for region in self.regions:
                        if entered_region.lower() == region.lower():
                            self.check_vars[region].set(
                                True
                            )  # Cochez la case de la région correspondante
                            self.update_recap(self.check_vars, self.regions)
                            region_found = (
                                True  # Marquez que la région a été trouvée et cochée
                            )
                            break  # Sortez de la boucle une fois la région trouvée
                    if not region_found:
                        # Si la région saisie n'est pas déjà présente, ajoutez-la à `additional_regions`
                        if entered_region.lower() not in [
                            region.lower()
                            for region in self.regions + list(self.additional_regions)
                        ]:
                            self.additional_regions.add(
                                entered_region
                            )  # Ajoutez la région à la liste des régions supplémentaires
                            self.update_recap(
                                self.check_vars,
                                self.regions + list(self.additional_regions),
                            )
            self.zone_entre.set(
                ""
            )  # Nettoyez la zone de texte après l'ajout ou si la région est déjà présente

    def toggle_all(self, master_var, all_vars, all_checkboxes):
        for region, var in self.variables.items():
            if region != "All":
                var.set(self.variables["All"].get())
                self.checkboxes[region].config(
                    state=tk.DISABLED if self.variables["All"].get() else tk.NORMAL
                )

    def remove_region(self, region, check_vars, options):
        if region in self.additional_regions:
            self.additional_regions.remove(region)
        else:
            check_vars[region].set(False)
        self.update_recap(check_vars, options)

    def update_recap(self, check_vars, options):
        if self.recap is not None:
            # Effacer les items précédents sauf 'Régions'
            for item in self.recap.canvas_regions.find_withtag("region_item"):
                self.recap.canvas_regions.delete(item)

            # Sélection des options à afficher
            if check_vars["All"].get():
                # Exclure "All" de l'affichage
                options_to_display = [option for option in options if option != "All"]
            else:
                # Afficher uniquement les options sélectionnées
                options_to_display = [
                    option
                    for option in options
                    if check_vars.get(option, tk.BooleanVar()).get()
                ]

            # Tri des options sans tenir compte de la casse
            all_options = sorted(
                list(self.additional_regions) + options_to_display,
                key=lambda x: x.lower(),
            )

            # Mise à jour du texte dans le canvas
            recap_text = "Régions:\n" + "\n".join(all_options)
            self.recap.canvas_regions.itemconfig(
                self.recap.text_recap_cases, text=recap_text
            )

            # Ajuster la zone de défilement pour s'assurer que tout est visible
            self.recap.canvas_regions.configure(
                scrollregion=self.recap.canvas_regions.bbox("all")
            )

    def effacer_selection(self):
        for var in self.check_vars.values():
            var.set(False)
        self.additional_regions.clear()
        self.zone_entre.set("")
        self.update_recap(self.check_vars, self.regions + list(self.additional_regions))

    """
    def get_regions(self):
        ret = []
        for region, var in self.check_vars.items():
            if var.get():
                ret.append(region)
        print(ret)
        return ret 
    """
