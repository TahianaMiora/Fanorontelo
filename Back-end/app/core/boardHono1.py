# app/core/board.py

class FanoronTeloBoard:
    # Cartographie des 8 alignements gagnants possibles sur le plateau
    WINNING_LINES = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # 3 Lignes horizontales
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # 3 Lignes verticales
        (0, 4, 8), (2, 4, 6)              # 2 Diagonales
    ]

    # Liste d'adjacence : pour chaque index (0-8), quels sont les index connectés ?
    ADJACENCY_LIST = {
        0: [1, 3, 4],     # Le coin haut-gauche est lié à son horizontal (1), vertical (3) et diagonal (4)
        1: [0, 2, 4],     # Le milieu-haut est lié à 0, 2 et au centre 4
        2: [1, 4, 5],     # Coin haut-droit
        3: [0, 4, 6],     # Milieu-gauche
        4: [0, 1, 2, 3, 5, 6, 7, 8], # Le centre est connecté aux 8 autres cases !
        5: [2, 4, 8],     # Milieu-droit
        6: [3, 4, 7],     # Coin bas-gauche
        7: [6, 4, 8],     # Milieu-bas
        8: [7, 4, 5]      # Coin bas-droit
    }

    def __init__(self):
        # Le plateau est une liste "aplatie" de 9 éléments
        # Index : 0, 1, 2 (ligne haut) | 3, 4, 5 (ligne milieu) | 6, 7, 8 (ligne bas)
        self.grid = [0] * 9

        # Le Joueur 1 (X) commence toujours
        self.current_player = 1

        # Le jeu commence à la Phase 1 (Placement des pions)
        self.phase = 1

        # Compteur pour savoir combien de pions chaque joueur a posé (Max 3 chacun)
        self.pieces_placed = {1: 0, -1: 0}
    
    def check_winner(self):
        """
        [Membre 1] Vérifie s'il y a un alignement gagnant sur le plateau.
        Retourne 1 si X gagne, -1 si O gagne, et 0 si personne n'a gagné.
        """
        for line in self.WINNING_LINES:
            # On fait la somme des trois cases de l'alignement
            line_sum = self.grid[line[0]] + self.grid[line[1]] + self.grid[line[2]]

            if line_sum == 3:
                return 1   # Joueur X a aligné ses 3 pions
            elif line_sum == -3:
                return -1  # Joueur O a aligné ses 3 pions

        return 0  # Aucun alignement complet pour le moment
    
    def place_piece(self, position):
        """
       Place un pion pour le joueur actuel durant la Phase 1.
        'position' doit être un entier entre 0 et 8.
        Retourne True si le coup est valide et appliqué, False sinon.
        """
        # Sécurité : On ne peut placer un pion que si on est en Phase 1
        if self.phase != 1:
            print("Erreur : Ce n'est plus la phase de placement !")
            return False

        # Sécurité : La case doit être vide et l'index valide
        if position < 0 or position > 8 or self.grid[position] != 0:
            print(f"Erreur : La position {position} n'est pas valide ou déjà occupée.")
            return False

        # On applique le placement du pion
        self.grid[position] = self.current_player
        self.pieces_placed[self.current_player] += 1
        print(f"Joueur {self.current_player} a posé son pion en {position}.")
        print(f"Nombre de pions du joueur {self.current_player} : {self.pieces_placed[self.current_player]}")
        # On vérifie immédiatement si ce placement est synonyme de victoire
        winner = self.check_winner()
        if winner != 0:
            # Partie terminée directement en Phase 1 !
            return True

        # Si les deux joueurs ont posé leurs 3 pions (6 pions au total), on passe en Phase 2
        if self.pieces_placed[1] == 3 and self.pieces_placed[-1] == 3:
            self.phase = 2

        # Si pas de victoire, on change de joueur de manière élégante (-1 devient 1, 1 devient -1)
        self.current_player = -self.current_player
        return True

    def display_board(self):
        """Une petite fonction utilitaire pour afficher le plateau dans le terminal (Pratique pour déboguer)"""
        symbols = {0: ".", 1: "X", -1: "O"}
        print(f"{symbols[self.grid[0]]} -- {symbols[self.grid[1]]} -- {symbols[self.grid[2]]}")
        print(f"|  \\  |  /  |")
        print(f"{symbols[self.grid[3]]} -- {symbols[self.grid[4]]} -- {symbols[self.grid[5]]}")
        print(f"|  /  |  \\  |")
        print(f"{symbols[self.grid[6]]} -- {symbols[self.grid[7]]} -- {symbols[self.grid[8]]}")
if __name__ == "__main__":
    board = FanoronTeloBoard()
    board.display_board()