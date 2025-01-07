import tkinter as tk
from tkinter import messagebox
import random
import time

class Navire:
    def __init__(self, nom, taille):
        self.nom = nom
        self.taille = taille
        self.positions = []
        self.positions_touchees = set()

    def est_touche(self, coord):
        if coord in self.positions:
            self.positions_touchees.add(coord)

    def est_coule(self):
        return len(self.positions_touchees) == self.taille

class Plateau:
    def __init__(self, taille=10):
        self.taille = taille
        self.grille = [[" " for _ in range(taille)] for _ in range(taille)]
        self.navires = []

    def ajouter_navire(self, navire):
        self.navires.append(navire)

    def peut_placer_navire(self, navire, lig, col, orien='H'):
        if orien == 'H':
            if col + navire.taille > self.taille:
                return False
            for c in range(col, col + navire.taille):
                if self.grille[lig][c] != " ":
                    return False
        else:
            if lig + navire.taille > self.taille:
                return False
            for r in range(lig, lig + navire.taille):
                if self.grille[r][col] != " ":
                    return False
        return True

    def placer_navire(self, navire, lig, col, orien='H'):
        pos = []
        if orien == 'H':
            for c in range(col, col + navire.taille):
                self.grille[lig][c] = "N"
                pos.append((lig, c))
        else:
            for r in range(lig, lig + navire.taille):
                self.grille[r][col] = "N"
                pos.append((r, col))
        navire.positions = pos
        self.ajouter_navire(navire)

class Joueur:
    def __init__(self, nom, plateau=None, est_humain=True):
        self.nom = nom
        self.plateau = plateau if plateau else Plateau()
        self.est_humain = est_humain
        self.navires = []

    def ajouter_navire(self, navire):
        self.navires.append(navire)

    def flotte_coulee(self):
        return all(nav.est_coule() for nav in self.navires)

    def placer_navires_aleatoirement(self, liste_navs):
        for nv in liste_navs:
            place = False
            while not place:
                orien = random.choice(['H', 'V'])
                lig = random.randint(0, self.plateau.taille - 1)
                col = random.randint(0, self.plateau.taille - 1)
                if self.plateau.peut_placer_navire(nv, lig, col, orien):
                    self.plateau.placer_navire(nv, lig, col, orien)
                    self.navires.append(nv)
                    place = True

    def tirer(self, adversaire, x, y):
        """
        Retourne (touché, navire_coule):
          - touché: True/False
          - navire_coule: Le navire coulé si un navire vient d'être coulé, sinon None
        """
        case = adversaire.plateau.grille[x][y]
        if case == "N":  # navire présent -> Touché
            for nav in adversaire.navires:
                if (x, y) in nav.positions:
                    nav.est_touche((x, y))
                    adversaire.plateau.grille[x][y] = "X"
                    if nav.est_coule():
                        return True, nav
                    return True, None
        else:
            adversaire.plateau.grille[x][y] = "O"
            return False, None

class ApplicationBatailleNavale:
    def __init__(self, root):
        self.root = root
        self.root.title("Bataille Navale : Navires & Stats")

        # --- Pour le chrono ---
        self.start_time = time.time()

        self.orientation = 'H'
        self.liste_navires = [
            ("Porte-Avions", 5),
            ("Croiseur", 4),
            ("Destroyer1", 3),
            ("Destroyer2", 3),
            ("Sous-Marin1", 2),
            ("Sous-Marin2", 2)
        ]

        self.joueur1 = Joueur("Joueur 1", est_humain=True)
        self.joueur2 = Joueur("Ordinateur", est_humain=False)

        self.navire_index = 0
        self.phase_placement_terminee = False

        # --- Stats de tir ---
        self.hits_joueur1 = 0
        self.misses_joueur1 = 0
        self.hits_joueur2 = 0
        self.misses_joueur2 = 0

        self.coups_joues_joueur = set()
        self.coups_joues_ordi = set()
        self.tour_joueur = True

        navs_ordi = [Navire(n, t) for (n, t) in self.liste_navires]
        self.joueur2.placer_navires_aleatoirement(navs_ordi)

        # --- Layout ---
        self.frame_joueur = tk.Frame(self.root, padx=10, pady=10, borderwidth=2, relief="groove")
        self.frame_joueur.pack(side="left", expand=True, fill="both")

        self.frame_ordinateur = tk.Frame(self.root, padx=10, pady=10, borderwidth=2, relief="groove")
        self.frame_ordinateur.pack(side="right", expand=True, fill="both")

        tk.Label(self.frame_joueur, text="Grille du Joueur", font=("Arial", 14, "bold")).pack(pady=5)
        tk.Label(self.frame_ordinateur, text="Grille Ordinateur", font=("Arial", 14, "bold")).pack(pady=5)

        self.canvas_joueur = tk.Frame(self.frame_joueur)
        self.canvas_joueur.pack()
        self.canvas_ordinateur = tk.Frame(self.frame_ordinateur)
        self.canvas_ordinateur.pack()

        self.grille_boutons_joueur = []
        self.grille_boutons_ordinateur = []
        self.creer_grille_joueur()
        self.creer_grille_ordinateur()

        # --- Labels navires en vie / stats ---
        self.label_nb_navires_joueur1 = tk.Label(self.frame_joueur, text="Navires en vie: 0")
        self.label_nb_navires_joueur1.pack(pady=10)

        self.label_liste_navires_joueur1 = tk.Label(self.frame_joueur, text="Liste navires en vie: ")
        self.label_liste_navires_joueur1.pack(pady=10)

        self.label_stats_joueur1 = tk.Label(self.frame_joueur, text="Tirs réussis: 0 | Tirs manqués: 0")
        self.label_stats_joueur1.pack(pady=10)

        self.label_nb_navires_joueur2 = tk.Label(self.frame_ordinateur, text="Navires en vie: 0")
        self.label_nb_navires_joueur2.pack(pady=10)

        self.label_liste_navires_joueur2 = tk.Label(self.frame_ordinateur, text="Liste navires en vie: ")
        self.label_liste_navires_joueur2.pack(pady=10)

        self.label_stats_joueur2 = tk.Label(self.frame_ordinateur, text="Tirs réussis: 0 | Tirs manqués: 0")
        self.label_stats_joueur2.pack(pady=10)

        self.btn_nouvelle_partie = tk.Button(self.root, text="Nouvelle Partie", command=self.nouvelle_partie)
        self.btn_nouvelle_partie.pack(pady=10)

        self.btn_orientation = tk.Button(self.root, text="Orientation: Horizontale", command=self.changer_orientation)
        self.btn_orientation.pack(pady=10)

        self.label_info = tk.Label(self.root, text="Placez vos navires. Puis tirez sur la grille ennemie.")
        self.label_info.pack(pady=10)

        # Label chrono en bas, centré
        self.label_time = tk.Label(self.root, text="", font=("Arial", 22, "bold"))
        self.label_time.pack(side="bottom", pady=10)

        # Mise à jour initiale
        self.update_navires_en_vie()
        self.update_time()

    def creer_grille_joueur(self):
        for i in range(self.joueur1.plateau.taille):
            ligne_boutons = []
            for j in range(self.joueur1.plateau.taille):
                btn = tk.Button(self.canvas_joueur, text=" ", width=6, height=2,
                                command=lambda r=i, c=j: self.on_case_joueur_click(r, c))
                btn.grid(row=i, column=j, padx=1, pady=1)
                ligne_boutons.append(btn)
            self.grille_boutons_joueur.append(ligne_boutons)

    def creer_grille_ordinateur(self):
        for i in range(self.joueur2.plateau.taille):
            ligne_boutons = []
            for j in range(self.joueur2.plateau.taille):
                btn = tk.Button(self.canvas_ordinateur, text=" ", width=6, height=2,
                                command=lambda r=i, c=j: self.on_case_ordinateur_click(r, c))
                btn.grid(row=i, column=j, padx=1, pady=1)
                ligne_boutons.append(btn)
            self.grille_boutons_ordinateur.append(ligne_boutons)

    def changer_orientation(self):
        if self.orientation == 'H':
            self.orientation = 'V'
            self.btn_orientation.config(text="Orientation: Verticale")
        else:
            self.orientation = 'H'
            self.btn_orientation.config(text="Orientation: Horizontale")

    def on_case_joueur_click(self, i, j):
        if self.phase_placement_terminee:
            messagebox.showinfo("Placement terminé", "Tous vos navires sont déjà placés.")
            return

        if self.navire_index >= len(self.liste_navires):
            messagebox.showinfo("Placement terminé", "Tous les navires sont placés.")
            return

        nom, taille = self.liste_navires[self.navire_index]
        nav = Navire(nom, taille)

        if self.joueur1.plateau.peut_placer_navire(nav, i, j, self.orientation):
            self.joueur1.plateau.placer_navire(nav, i, j, self.orientation)
            self.joueur1.ajouter_navire(nav)

            # Marquage visuel
            if self.orientation == 'H':
                for c in range(j, j + taille):
                    self.grille_boutons_joueur[i][c].config(text="N", state="disabled")
            else:
                for r in range(i, i + taille):
                    self.grille_boutons_joueur[r][j].config(text="N", state="disabled")

            self.navire_index += 1
            self.update_navires_en_vie()

            if self.navire_index == len(self.liste_navires):
                self.phase_placement_terminee = True
                messagebox.showinfo("Placement fini", "Tous vos navires sont en place!")
                self.tour_joueur = True
        else:
            messagebox.showwarning("Impossible", "Placement invalide ici.")

    def on_case_ordinateur_click(self, i, j):
        if not self.phase_placement_terminee:
            messagebox.showinfo("Info", "Finissez d'abord votre placement.")
            return

        if not self.tour_joueur:
            messagebox.showinfo("Patientez", "Ce n'est pas votre tour.")
            return

        if (i, j) in self.coups_joues_joueur:
            messagebox.showwarning("Déjà joué", "Vous avez déjà tiré ici.")
            return
        self.coups_joues_joueur.add((i, j))

        touche, nav_coule = self.joueur1.tirer(self.joueur2, i, j)
        if touche:
            self.hits_joueur1 += 1
            self.grille_boutons_ordinateur[i][j].config(bg="red", text="X")
        else:
            self.misses_joueur1 += 1
            self.grille_boutons_ordinateur[i][j].config(bg="blue", text="O")

        if nav_coule:
            for (lx, ly) in nav_coule.positions:
                self.grille_boutons_ordinateur[lx][ly].config(bg="black", text="X")

        self.update_navires_en_vie()
        self.update_stats_labels()

        if self.joueur2.flotte_coulee():
            messagebox.showinfo("Victoire!", "Vous avez coulé toute la flotte ennemie!")
            self.desactiver_tout()
            return

        self.tour_joueur = False
        self.root.after(1000, self.tour_ordinateur)

    def tour_ordinateur(self):
        coo = None
        while True:
            i = random.randint(0, self.joueur1.plateau.taille - 1)
            j = random.randint(0, self.joueur1.plateau.taille - 1)
            if (i, j) not in self.coups_joues_ordi:
                coo = (i, j)
                break
        self.coups_joues_ordi.add(coo)

        touche, nav_coule = self.joueur2.tirer(self.joueur1, coo[0], coo[1])
        bouton = self.grille_boutons_joueur[coo[0]][coo[1]]

        if touche:
            self.hits_joueur2 += 1
            bouton.config(bg="red", text="X")
        else:
            self.misses_joueur2 += 1
            bouton.config(bg="blue", text="O")

        if nav_coule:
            for (lx, ly) in nav_coule.positions:
                self.grille_boutons_joueur[lx][ly].config(bg="black", text="X")

        self.update_navires_en_vie()
        self.update_stats_labels()

        if self.joueur1.flotte_coulee():
            messagebox.showinfo("Défaite", "L'ordinateur a coulé toute votre flotte!")
            self.desactiver_tout()
            return

        self.tour_joueur = True

    def desactiver_tout(self):
        for i in range(self.joueur2.plateau.taille):
            for j in range(self.joueur2.plateau.taille):
                self.grille_boutons_ordinateur[i][j].config(state="disabled")

    def nouvelle_partie(self):
        messagebox.showinfo("Nouvelle Partie", "Réinitialisation...")
        self.root.destroy()
        root = tk.Tk()
        ApplicationBatailleNavale(root)
        root.mainloop()

    def update_navires_en_vie(self):
        """Met à jour l'affichage du nombre et du nom des navires restants (non coulés)."""
        # Joueur 1
        navires_pas_coules_j1 = [nav.nom for nav in self.joueur1.navires if not nav.est_coule()]
        nb_joueur1 = len(navires_pas_coules_j1)
        self.label_nb_navires_joueur1.config(text=f"Navires en vie: {nb_joueur1}")
        self.label_liste_navires_joueur1.config(
            text="Liste navires en vie: " + (", ".join(navires_pas_coules_j1) if navires_pas_coules_j1 else "Aucun")
        )

        # Joueur 2
        navires_pas_coules_j2 = [nav.nom for nav in self.joueur2.navires if not nav.est_coule()]
        nb_joueur2 = len(navires_pas_coules_j2)
        self.label_nb_navires_joueur2.config(text=f"Navires en vie: {nb_joueur2}")
        self.label_liste_navires_joueur2.config(
            text="Liste navires en vie: " + (", ".join(navires_pas_coules_j2) if navires_pas_coules_j2 else "Aucun")
        )

    def update_stats_labels(self):
        """Met à jour l'affichage des stats de tirs pour chaque joueur."""
        self.label_stats_joueur1.config(
            text=f"Tirs réussis: {self.hits_joueur1} | Tirs manqués: {self.misses_joueur1}"
        )
        self.label_stats_joueur2.config(
            text=f"Tirs réussis: {self.hits_joueur2} | Tirs manqués: {self.misses_joueur2}"
        )

    def update_time(self):
        """Met à jour l'affichage du temps écoulé depuis le début de la partie."""
        elapsed = int(time.time() - self.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        self.label_time.config(text=f"Temps écoulé: {minutes:02d}:{seconds:02d}")
        # On rappelle cette fonction toutes les 1000 ms
        self.root.after(1000, self.update_time)

if __name__ == "__main__":
    root = tk.Tk()
    ApplicationBatailleNavale(root)
    root.mainloop()
