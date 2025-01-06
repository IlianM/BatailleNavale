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
        (La logique de placement n'est pas encore implémentée ici.)
        """
        self.navires.append(navire)
    
    def afficher_grille(self):
        """
        Affiche la grille dans la console (principalement pour le débogage).
        Chaque case est séparée par un espace.
        """
        for ligne in self.grille:
            print(" ".join(ligne))
        print()
        
    # Méthode possible pour plus tard (exemple) :
    # def placer_navire(self, navire, ligne_depart, col_depart, orientation):
    #     """
    #     Place le navire sur la grille à partir de (ligne_depart, col_depart).
    #     Orientation peut être 'H' ou 'V'.
    #     """
    #     pass


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
        Affiche la grille du joueur (principalement pour le débogage).
        """
        print(f"Plateau de {self.nom}:")
        self.plateau.afficher_grille()

    # Méthodes possibles pour plus tard (exemple) :
    # def tirer(self, adversaire, coord):
    #     """
    #     Tire sur une coordonnée du plateau de l'adversaire.
    #     """
    #     pass


# =====================================================
# Exemple d'utilisation et initialisation
# =====================================================

if __name__ == "__main__":
    # Création d'un joueur humain
    joueur1 = Joueur("Joueur 1", est_humain=True)
    
    # Création d'un deuxième joueur (ordinateur)
    joueur2 = Joueur("Ordinateur", est_humain=False)
    
    # Exemple de création de navires
    porte_avions = Navire("Porte-Avions", 5)
    croiseur = Navire("Croiseur", 4)
    
    # Ajout des navires au premier joueur
    joueur1.ajouter_navire(porte_avions)
    joueur1.ajouter_navire(croiseur)
    
    # Affichage du plateau du joueur 1 (pour debug)
    joueur1.afficher_plateau()
    
    # Même chose pour l'ordinateur
    destroyer = Navire("Destroyer", 3)
    joueur2.ajouter_navire(destroyer)
    joueur2.afficher_plateau()
