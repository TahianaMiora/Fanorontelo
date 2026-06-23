# app/core/board.py

class FanoronTeloBoard:
    # Cartographie des 8 alignements gagnants possibles sur le plateau
    WINNING_LINES = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # 3 Lignes horizontales
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # 3 Lignes verticales
        (0, 4, 8), (2, 4, 6)              # 2 Diagonales
    ]

    # Liste d'adjacence pour les mouvements de la Phase 2
    ADJACENCY_LIST = {
        0: [1, 3, 4], 1: [0, 2, 4], 2: [1, 4, 5],
        3: [0, 4, 6], 4: [0, 1, 2, 3, 5, 6, 7, 8], 5: [2, 4, 8],
        6: [3, 4, 7], 7: [6, 4, 8], 8: [7, 4, 5]
    }

    def __init__(self):
        # 0 = Vide, 1 = Joueur X, -1 = Joueur O
        self.grid = [0] * 9
        self.current_player = 1
        self.phase = 1
        self.pieces_placed = {1: 0, -1: 0}
        self.history = []  # Pour l'option Undo (Priorité 3)

    def copy(self):
        """Retourne une copie miroir indépendante (Crucial pour le Minimax)"""
        new_board = FanoronTeloBoard()
        new_board.grid = list(self.grid)
        new_board.current_player = self.current_player
        new_board.phase = self.phase
        new_board.pieces_placed = dict(self.pieces_placed)
        return new_board

    def switch_player(self):
        """Alterne le joueur actuel de manière élégante"""
        self.current_player = -self.current_player

    def display_board(self):
        """Affichage utilitaire dans la console pour déboguer"""
        symbols = {0: ".", 1: "X", -1: "O"}
        print(f"{symbols[self.grid[0]]} -- {symbols[self.grid[1]]} -- {symbols[self.grid[2]]}")
        print(f"|  \\  |  /  |")
        print(f"{symbols[self.grid[3]]} -- {symbols[self.grid[4]]} -- {symbols[self.grid[5]]}")
        print(f"|  /  |  \\  |")
        print(f"{symbols[self.grid[6]]} -- {symbols[self.grid[7]]} -- {symbols[self.grid[8]]}")
        print(f"Tour du joueur : {'X' if self.current_player == 1 else 'O'} | Phase : {self.phase}\n")