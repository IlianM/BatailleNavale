import tkinter as tk
from tkinter import messagebox

# =====================================================
# Phase 1 : Mise en place des classes de base
# =====================================================

class Navire:
    """
    Classe représentant un navire dans la Bataille Navale.
    
    Attributs :
    -----------
    nom : str
        Nom du navire (ex: "Porte-Avions", "Croiseur", etc.)
    taille : int
        Nombre de cases occupées par le navire.
    positions : list of tuple
        Liste des coordonnées (ligne, colonne) occupées par le navire.
    positions_touchees : set of tuple
        Ensemble des coordonnées du navire qui ont été touchées par un tir.
    """
    
    def __init__(self, nom, taille):
        self.nom = nom
        self.taille = taille
        self.positions = []
        self.positions_touchees = set()
        
    def est_touche(self, coord):
        """
        Marque la position 'coord' (tuple (ligne, colonne)) comme touchée.
        """
        if coord in self.positions:
            self.positions_touchees.add(coord)
    
    def est_coule(self):
        """
        Vérifie si le navire est complètement coulé.
        """
        return len(self.positions_touchees) == self.taille
    
    def __repr__(self):
        return f"Navire({self.nom}, taille={self.taille})"


class Plateau:
    """
    Classe représentant le plateau de jeu (une grille 10x10 par défaut).
    
    Attributs :
    -----------
    taille : int
        Taille de la grille (10 par défaut).
    grille : list of list
        Représentation interne de la grille. Peut être utilisée pour
        stocker des informations (navire, tir manqué, etc.).
    navires : list of Navire
        Liste des navires placés sur le plateau.
    """
    
    def __init__(self, taille=10):
        self.taille = taille
        # On initialise la grille avec des valeurs vides (par exemple " ").
        self.grille = [[" " for _ in range(taille)] for _ in range(taille)]
        self.navires = []
    
    def ajouter_navire(self, navire):
        """
        Ajoute un navire à la liste des navires. 
        """
        self.navires.append(navire)
    
    def afficher_grille(self):
        """
        Affiche la grille dans la console (debug). 
        """
        for ligne in self.grille:
            print(" ".join(ligne))
        print()
        

class Joueur:
    """
    Classe représentant un joueur (humain ou ordinateur).
    
    Attributs :
    -----------
    nom : str
        Nom du joueur.
    plateau : Plateau
        Plateau associé au joueur, sur lequel se trouvent ses navires.
    navires : list of Navire
        Liste des navires que le joueur possède (optionnel si on les stocke déjà dans Plateau).
    est_humain : bool
        Indique si le joueur est contrôlé par un humain ou par l'ordinateur.
    """
    
    def __init__(self, nom, plateau=None, est_humain=True):
        self.nom = nom
        self.plateau = plateau if plateau else Plateau()
        self.navires = []
        self.est_humain = est_humain

    def ajouter_navire(self, navire):
        """
        Ajoute un navire à la flotte du joueur.
        """
        self.navires.append(navire)
        self.plateau.ajouter_navire(navire)

    def afficher_plateau(self):
        """
        Affiche la grille du joueur (debug).
        """
        print(f"Plateau de {self.nom}:")
        self.plateau.afficher_grille()

    # Méthodes possibles pour plus tard :
    # def tirer(self, adversaire, coord):
    #     """
    #     Tire sur une coordonnée du plateau de l'adversaire.
    #     """
    #     pass


# =====================================================
# Phase 2 : Interface utilisateur (Tkinter)
# =====================================================

class ApplicationBatailleNavale:
    """
    Classe gérant l'interface utilisateur avec Tkinter.
    Elle crée deux grilles : 
      - La grille du joueur
      - La grille de l'ordinateur
    Ainsi que des boutons pour les interactions.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Bataille Navale - Phase 2")

        # Création de deux joueurs (humain et ordinateur)
        self.joueur1 = Joueur("Joueur 1", est_humain=True)
        self.joueur2 = Joueur("Ordinateur", est_humain=False)

        # Exemple de navires (vous pourrez ajouter la phase de placement plus tard)
        porte_avions = Navire("Porte-Avions", 5)
        croiseur = Navire("Croiseur", 4)
        destroyer = Navire("Destroyer", 3)
        
        # On ajoute quelques navires au joueur1 et au joueur2 pour illustrer
        self.joueur1.ajouter_navire(porte_avions)
        self.joueur1.ajouter_navire(croiseur)
        self.joueur2.ajouter_navire(destroyer)

        # Frames pour les deux grilles
        self.frame_joueur = tk.Frame(self.root, padx=10, pady=10, borderwidth=2, relief="groove")
        self.frame_joueur.pack(side="left", expand=True, fill="both")

        self.frame_ordinateur = tk.Frame(self.root, padx=10, pady=10, borderwidth=2, relief="groove")
        self.frame_ordinateur.pack(side="right", expand=True, fill="both")

        # Titre sur chaque frame
        tk.Label(self.frame_joueur, text="Grille du Joueur", font=("Arial", 14, "bold")).pack(pady=5)
        tk.Label(self.frame_ordinateur, text="Grille de l'Ordinateur", font=("Arial", 14, "bold")).pack(pady=5)

        # Conteneurs pour les grilles (on va y placer des boutons)
        self.canvas_joueur = tk.Frame(self.frame_joueur)
        self.canvas_joueur.pack()

        self.canvas_ordinateur = tk.Frame(self.frame_ordinateur)
        self.canvas_ordinateur.pack()

        # Création des grilles de boutons
        self.grille_boutons_joueur = []
        self.grille_boutons_ordinateur = []

        self.creer_grille_joueur()
        self.creer_grille_ordinateur()

        # Bouton pour lancer une nouvelle partie (exemple)
        self.btn_nouvelle_partie = tk.Button(self.root, text="Nouvelle Partie", command=self.nouvelle_partie)
        self.btn_nouvelle_partie.pack(pady=10)

    def creer_grille_joueur(self):
        """
        Crée la grille de boutons pour le joueur.
        """
        for i in range(self.joueur1.plateau.taille):
            ligne_boutons = []
            for j in range(self.joueur1.plateau.taille):
                btn = tk.Button(
                    self.canvas_joueur,
                    text=" ",
                    width=3,
                    height=1,
                    command=lambda r=i, c=j: self.on_case_joueur_click(r, c)
                )
                btn.grid(row=i, column=j, padx=1, pady=1)
                ligne_boutons.append(btn)
            self.grille_boutons_joueur.append(ligne_boutons)

    def creer_grille_ordinateur(self):
        """
        Crée la grille de boutons pour l'ordinateur.
        """
        for i in range(self.joueur2.plateau.taille):
            ligne_boutons = []
            for j in range(self.joueur2.plateau.taille):
                btn = tk.Button(
                    self.canvas_ordinateur,
                    text=" ",
                    width=3,
                    height=1,
                    command=lambda r=i, c=j: self.on_case_ordinateur_click(r, c)
                )
                btn.grid(row=i, column=j, padx=1, pady=1)
                ligne_boutons.append(btn)
            self.grille_boutons_ordinateur.append(ligne_boutons)

    def on_case_joueur_click(self, i, j):
        """
        Clique sur la grille du joueur.
        """
        messagebox.showinfo("Info", f"Vous avez cliqué sur la case ({i}, {j}) de votre propre grille.")

    def on_case_ordinateur_click(self, i, j):
        """
        Clique sur la grille de l'ordinateur.
        """
        messagebox.showinfo("Tir", f"Vous tirez sur la case ({i}, {j}) de la grille de l'ordinateur.")

    def nouvelle_partie(self):
        """
        Réinitialise les plateaux
        """
        messagebox.showinfo("Nouvelle Partie", "Réinitialisation des plateaux.")
        # Vous pourriez ici recréer des instances de Joueur, vider les grilles, etc.


# =====================================================
# Exemple d'utilisation et lancement de l'interface
# =====================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = ApplicationBatailleNavale(root)
    root.mainloop()
