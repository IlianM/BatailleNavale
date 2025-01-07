import tkinter as tk
from tkinter import messagebox
import random

# Class navir
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

    def afficher_grille(self):
        for ligne in self.grille:
            print(" ".join(ligne))
        print()

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

    def afficher_plateau(self):
        print(f"Plateau de {self.nom}:")
        self.plateau.afficher_grille()

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

class ApplicationBatailleNavale:
    def __init__(self, root):
        self.root = root
        self.root.title("Bataille Navale - Phase 3")
        
        self.orientation = 'H'   # orientation par defaut
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
        
        navs_ordi = [Navire(n, t) for (n, t) in self.liste_navires]
        self.joueur2.placer_navires_aleatoirement(navs_ordi)

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

        self.btn_nouvelle_partie = tk.Button(self.root, text="Nouvelle Partie", command=self.nouvelle_partie)
        self.btn_nouvelle_partie.pack(pady=10)

        # Bouton pour changer l’orientation
        self.btn_orientation = tk.Button(self.root, text="Orientation: Horizontale", command=self.changer_orientation)
        self.btn_orientation.pack(pady=5)

        self.label_info = tk.Label(self.root, text="Cliquez sur votre grille pur placer un navire.")
        self.label_info.pack(pady=5)

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
            messagebox.showinfo("Placement terminé", "Tous les navires deja placés.")
            return

        if self.navire_index >= len(self.liste_navires):
            messagebox.showinfo("Placement terminé", "Tous les navires deja placés.")
            return

        nom, taille = self.liste_navires[self.navire_index]
        nav = Navire(nom, taille)

        if self.joueur1.plateau.peut_placer_navire(nav, i, j, self.orientation):
            self.joueur1.plateau.placer_navire(nav, i, j, self.orientation)
            self.joueur1.ajouter_navire(nav)

            if self.orientation == 'H':
                for c in range(j, j + taille):
                    self.grille_boutons_joueur[i][c].config(text="N", state="disabled")
            else:
                for r in range(i, i + taille):
                    self.grille_boutons_joueur[r][j].config(text="N", state="disabled")

            self.navire_index += 1
            if self.navire_index == len(self.liste_navires):
                self.phase_placement_terminee = True
                messagebox.showinfo("Placement fini", "Tous les navires placés!")
        else:
            messagebox.showwarning("Impossible", "Placment impossible ici.")

    def on_case_ordinateur_click(self, i, j):
        if not self.phase_placement_terminee:
            messagebox.showinfo("Info", "Placer d’abord tous vos navires!")
            return
        messagebox.showinfo("Tir", f"Tir sur ({i}, {j})... (non implémenté)")

    def nouvelle_partie(self):
        messagebox.showinfo("Nouvelle Partie", "Réinit.")
        self.root.destroy()
        root = tk.Tk()
        ApplicationBatailleNavale(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    ApplicationBatailleNavale(root)
    root.mainloop()
