# app/core/game_rules.py
from app.core.board import FanoronTeloBoard

class GameRules:
    @staticmethod
    def check_winner(board: FanoronTeloBoard) -> int:
        """
        Vérifie s'il y a un vainqueur via la somme algébrique.
        Retourne 1 (X gagne), -1 (O gagne) ou 0.
        """
        for line in board.WINNING_LINES:
            line_sum = board.grid[line[0]] + board.grid[line[1]] + board.grid[line[2]]
            if line_sum == 3:
                return 1
            elif line_sum == -3:
                return -1
        return 0

    @staticmethod
    def get_legal_moves(board: FanoronTeloBoard):
        """Calcule dynamiquement tous les coups autorisés"""
        if GameRules.check_winner(board) != 0:
            return []

        if board.phase == 1:
            return [i for i, val in enumerate(board.grid) if val == 0]
        else:
            moves = []
            for src in range(9):
                if board.grid[src] == board.current_player:
                    for dest in board.ADJACENCY_LIST[src]:
                        if board.grid[dest] == 0:
                            moves.append((src, dest))
            return moves

    @staticmethod
    def place_piece(board: FanoronTeloBoard, position: int) -> bool:
        """Applique les règles de la Phase 1"""
        if board.phase != 1 or position not in GameRules.get_legal_moves(board):
            return False

        # Sauvegarde pour l'historique
        board.history.append((list(board.grid), board.current_player, board.phase, dict(board.pieces_placed)))

        # Application du coup
        board.set_cell(position, board.current_player)
        board.pieces_placed[board.current_player] += 1

        # Changement de phase automatique si 6 pions au total
        if board.pieces_placed[1] == 3 and board.pieces_placed[-1] == 3:
            board.phase = 2

        # Si pas de vainqueur immédiat, on change de tour
        if GameRules.check_winner(board) == 0:
            board.switch_player()
        return True

    @staticmethod
    def move_piece(board: FanoronTeloBoard, src: int, dest: int) -> bool:
        """Applique les règles de la Phase 2 (Anti-triche inclus)"""
        if board.phase != 2 or (src, dest) not in GameRules.get_legal_moves(board):
            return False
        
        board.redo_history.clear()  # On vide l'historique Redo après un nouveau coup

        # Sauvegarde pour l'historique
        board.history.append((list(board.grid), board.current_player, board.phase, dict(board.pieces_placed)))

        # Application du mouvement (via set_cell pour garder les bitboards à jour)
        board.set_cell(src, 0)
        board.set_cell(dest, board.current_player)

        # Si pas de vainqueur immédiat, on change de tour
        if GameRules.check_winner(board) == 0:
            board.switch_player()
        return True
    
    @staticmethod
    def undo(board: FanoronTeloBoard) -> bool:
        if not board.history: return False
        # Avant d'annuler, on sauvegarde l'état actuel dans le Redo
        board.redo_history.append((list(board.grid), board.current_player, board.phase, dict(board.pieces_placed)))
        # On applique l'ancien état
        board.grid, board.current_player, board.phase, board.pieces_placed = board.history.pop()
        # resync bitboards
        if hasattr(board, '_sync_bits_from_grid'):
            board._sync_bits_from_grid()
        return True

    @staticmethod
    def redo(board: FanoronTeloBoard) -> bool:
        if not board.redo_history: return False
        # Avant de rétablir, on remet l'état actuel dans l'Undo
        board.history.append((list(board.grid), board.current_player, board.phase, dict(board.pieces_placed)))
        # On applique l'état rétabli
        board.grid, board.current_player, board.phase, board.pieces_placed = board.redo_history.pop()
        # resync bitboards
        if hasattr(board, '_sync_bits_from_grid'):
            board._sync_bits_from_grid()
        return True