import math
import time
import random
import alpha_beta as ab
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import random
from app.core.board import FanoronTeloBoard
from app.core.game_rules import GameRules

class OpeningBook:
    @staticmethod
    def obtenir_coup_ouverture(plateau):
        # Valable uniquement pour le premier coup absolu de la phase de placement
        cases = getattr(plateau, 'cases', None)
        if cases is None:
            cases = getattr(plateau, 'grid', [0] * 9)
        pions_poses = sum(1 for c in cases if c != 0)
        if pions_poses == 0:
            return 4
        if pions_poses == 1 and cases[4] != 0:
            return random.choice([0, 2, 6, 8])
        return None


class AdapterPlateau:
    """Adaptateur qui expose l'API attendue par `alpha_beta` en enveloppant
    un `FanoronTeloBoard` et en utilisant `GameRules` pour les opérations."""
    def __init__(self, board: FanoronTeloBoard):
        self.board = board

    def verifier_victoire(self):
        return GameRules.check_winner(self.board) != 0

    def evaluer_score_terminal(self):
        winner = GameRules.check_winner(self.board)
        if winner == 1:
            return 100
        if winner == -1:
            return -100
        return 0

    def est_match_nul(self):
        return len(GameRules.get_legal_moves(self.board)) == 0

    def evaluer_heuristique(self):
        # Simple heuristique: différence de pions (X - O)
        return self.board.grid.count(1) - self.board.grid.count(-1)

    def obtenir_coups_legaux(self):
        return GameRules.get_legal_moves(self.board)

    def copier_et_jouer(self, coup):
        new_board = self.board.copy()
        if new_board.phase == 1:
            GameRules.place_piece(new_board, coup)
        else:
            GameRules.move_piece(new_board, coup[0], coup[1])
        return AdapterPlateau(new_board)

# efa nofafako le Mockplateau de nosoloiko anle Borad tao amn Nathalie

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
    elif niveau == "difficile":
        prof = 4 if board.phase == 1 else 9
    else:  # moyen
        prof = 3 if board.phase == 1 else 5

    adapter = AdapterPlateau(board)
    _, meilleur_coup = ab.alpha_beta(adapter, profondeur=prof, alpha=-math.inf, beta=math.inf, est_maximisant=est_max)

    if meilleur_coup is None:
        return random.choice(coups)

    return meilleur_coup

if __name__ == "__main__":
    plateau = FanoronTeloBoard()
    print("=== MODE DÉMO FANORON-TELO : IA 1 (X) VS IA 2 (O) ===")
    plateau.display_board()
    tour_ia_1 = True
    nombre_de_coups = 0
    while GameRules.check_winner(plateau) == 0 and len(GameRules.get_legal_moves(plateau)) > 0:
        nombre_de_coups += 1
        print(f"\n--- Tour {nombre_de_coups} ---")
        if tour_ia_1:
            print("IA 1 (X) calcule...")
            coup = calculer_coup_ia(plateau, est_max=True, niveau="difficile")
            if plateau.phase == 1:
                print(f"IA 1 place un 'X' en case {coup}")
                GameRules.place_piece(plateau, coup)
            else:
                print(f"IA 1 déplace un 'X' de la case {coup[0]} vers {coup[1]}")
                GameRules.move_piece(plateau, coup[0], coup[1])
            tour_ia_1 = False
        else:
            print("IA 2 (O) calcule...")
            coup = calculer_coup_ia(plateau, est_max=False, niveau="moyen")
            if plateau.phase == 1:
                print(f"IA 2 place un 'O' en case {coup}")
                GameRules.place_piece(plateau, coup)
            else:
                print(f"IA 2 déplace un 'O' de la case {coup[0]} vers {coup[1]}")
                GameRules.move_piece(plateau, coup[0], coup[1])
            tour_ia_1 = True

        plateau.display_board()
        # time.sleep(1) 

    winner = GameRules.check_winner(plateau)
    if winner != 0:
        print(f"Résultat : Victoire de {'X' if winner==1 else 'O'} !")
        print(f"Nombre de coups joués : {nombre_de_coups}")
    else:
        print("Résultat : Match nul ou situation bloquée !")