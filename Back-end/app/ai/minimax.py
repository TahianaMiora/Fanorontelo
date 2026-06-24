import random
import math
from app.core.board import FanoronTeloBoard
from app.core.game_rules import GameRules

class OpeningBook:
    @staticmethod
    def obtenir_coup_ouverture(board: FanoronTeloBoard):
        pions_poses = sum(1 for c in board.grid if c != 0)
        if pions_poses == 0:
            return 4  
        if pions_poses == 1 and board.grid[4] != 0:
            return random.choice([0, 2, 6, 8])  
        return None


def eval_heuristique(board: FanoronTeloBoard, joueur: int) -> int:
    winner = GameRules.check_winner(board)
    if winner == joueur:
        return 1000
    if winner == -joueur:
        return -1000

    score = 0

    if board.phase == 2:
        if board.grid[4] == joueur:
            score += 15
        elif board.grid[4] == -joueur:
            score -= 15

    for line in FanoronTeloBoard.WINNING_LINES:
        valeurs = [board.grid[i] for i in line]
        pions_joueur = valeurs.count(joueur)
        pions_adv = valeurs.count(-joueur)

        if pions_adv == 0:  
            score += pions_joueur * 5
        if pions_joueur == 0: 
            score -= pions_adv * 5

    return score


def is_terminal(board: FanoronTeloBoard) -> bool:
    return (
        GameRules.check_winner(board) != 0
        or len(GameRules.get_legal_moves(board)) == 0
    )


def play(board: FanoronTeloBoard, move) -> FanoronTeloBoard:
    next_board = board.copy()
    if board.phase == 1:
        GameRules.place_piece(next_board, move)
    else:
        GameRules.move_piece(next_board, move[0], move[1])
    return next_board


def minimax(board: FanoronTeloBoard, prof: int, joueur: int):
    if prof == 0 or is_terminal(board):
        return eval_heuristique(board, joueur), None

    coups = GameRules.get_legal_moves(board)
    if not coups:
        return 0, None

    random.shuffle(coups)
    best = None

    if board.current_player == joueur:  # Maximisant
        best_value = -math.inf
        for coup in coups:
            copie = play(board, coup)
            val, _ = minimax(copie, prof - 1, joueur)
            if val > best_value:
                best_value = val
                best = coup
        return best_value, best
    else:                               # Minimisant
        best_value = math.inf
        for coup in coups:
            copie = play(board, coup)
            val, _ = minimax(copie, prof - 1, joueur)
            if val < best_value:
                best_value = val
                best = coup
        return best_value, best


def calculer_coup_ia(board: FanoronTeloBoard, est_max: bool, niveau: str = "moyen"):
    coups = GameRules.get_legal_moves(board)
    if not coups:
        return None

    if board.phase == 1:
        coup_ouverture = OpeningBook.obtenir_coup_ouverture(board)
        if coup_ouverture is not None and coup_ouverture in coups:
            print("[Opening Book] Coup précalculé appliqué.")
            return coup_ouverture

    if niveau == "facile":
        prof = 1 if board.phase == 1 else 3
    else:  # moyen
        prof = 3 if board.phase == 1 else 4

    _, meilleur_coup = minimax(board, prof, board.current_player)

    if meilleur_coup is None:
        return random.choice(coups)

    return meilleur_coup