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
        self.redo_history = []  # Pour l'option Redo (Priorité 3)
        # Représentation compacte: deux bitboards 9 bits (X et O)
        self.x_bits = 0
        self.o_bits = 0

    def copy(self):
        """Retourne une copie miroir indépendante (Crucial pour le Minimax)"""
        new_board = FanoronTeloBoard()
        new_board.grid = list(self.grid)
        new_board.current_player = self.current_player
        new_board.phase = self.phase
        new_board.pieces_placed = dict(self.pieces_placed)
        new_board.x_bits = int(self.x_bits)
        new_board.o_bits = int(self.o_bits)
        return new_board

    def _sync_bits_from_grid(self):
        """Met à jour `x_bits` et `o_bits` à partir de `grid`."""
        xb = 0
        ob = 0
        for i, v in enumerate(self.grid):
            if v == 1:
                xb |= 1 << i
            elif v == -1:
                ob |= 1 << i
        self.x_bits = xb
        self.o_bits = ob

    def set_cell(self, idx: int, player: int):
        """Place ou retire une pièce à l'index `idx`.
        player: 1 (X), -1 (O), 0 (empty)
        Garde `grid` et les bitboards synchronisés."""
        if player == 1:
            self.x_bits |= (1 << idx)
            self.o_bits &= ~(1 << idx)
            self.grid[idx] = 1
        elif player == -1:
            self.o_bits |= (1 << idx)
            self.x_bits &= ~(1 << idx)
            self.grid[idx] = -1
        else:
            # vider
            self.x_bits &= ~(1 << idx)
            self.o_bits &= ~(1 << idx)
            self.grid[idx] = 0

    def switch_player(self):
        """Alterne le joueur actuel de manière élégante"""
        self.current_player = -self.current_player

    def display_board(self): # novaiko kely le affichage 
        """Affichage utilitaire clair pour la console."""
        symbols = {0: '.', 1: 'X', -1: 'O'}
        rows = []
        for r in range(3):
            row = ' | '.join(symbols[self.grid[r*3 + c]] for c in range(3))
            rows.append(f" {row} ")

        sep = '\n---+---+---\n'
        print('\n' + sep.join(rows))
        print(f"\nTour : {'X' if self.current_player == 1 else 'O'}    |    Phase : {self.phase}\n")