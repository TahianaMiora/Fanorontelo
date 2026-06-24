import math
import time
import random
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.board import FanoronTeloBoard
from app.core.game_rules import GameRules

import alpha_beta as ab
import minimax as mm

class AdapterPlateau:
    def __init__(self, board: FanoronTeloBoard):
        self.board = board

    def verifier_victoire(self):
        return GameRules.check_winner(self.board) != 0

    def evaluer_score_terminal(self):
        winner = GameRules.check_winner(self.board)
        if winner == 1: return 1000
        if winner == -1: return -1000
        return 0

    def est_match_nul(self):
        return len(GameRules.get_legal_moves(self.board)) == 0

    def evaluer_heuristique(self):
        return mm.eval_heuristique(self.board, 1)

    def obtenir_coups_legaux(self):
        return GameRules.get_legal_moves(self.board)

    def copier_et_jouer(self, coup):
        new_board = self.board.copy()
        if new_board.phase == 1:
            GameRules.place_piece(new_board, coup)
        else:
            GameRules.move_piece(new_board, coup[0], coup[1])
        return AdapterPlateau(new_board)

def executer_benchmarks(nombre_parties=100):
    victoires_alpha_beta = 0
    victoires_minimax = 0
    nuls = 0
    
    temps_alpha_beta = []
    temps_minimax = []

    print(f"Lancement de {nombre_parties} affrontements : Alpha-Beta VS Minimax Classique...")

    for partie in range(nombre_parties):
        plateau = FanoronTeloBoard()
        ab_est_joueur_1 = random.choice([True, False])
        
        nombre_coups = 0
        # Limite stricte à 60 coups pour casser les boucles infinies de déplacements tactiques
        while GameRules.check_winner(plateau) == 0 and len(GameRules.get_legal_moves(plateau)) > 0 and nombre_coups < 60:
            coups_possibles = GameRules.get_legal_moves(plateau)
            
            # Ajustement des profondeurs (Phase 1: 3, Phase 2: 4) pour éviter l'explosion combinatoire
            prof = 3 if plateau.phase == 1 else 7

            # prof_1 = 7 # difficile
            # prof_2 = 2 # facile
            
            if plateau.current_player == 1:
                adapter = AdapterPlateau(plateau)
                if ab_est_joueur_1:
                    debut = time.perf_counter()
                    _, coup = ab.alpha_beta(adapter, profondeur=prof, alpha=-math.inf, beta=math.inf, est_maximisant=True)
                    temps_alpha_beta.append(time.perf_counter() - debut)
                else:
                    debut = time.perf_counter()
                    _, coup = mm.minimax(plateau, prof, 1)
                    # _, coup = ab.alpha_beta(adapter, profondeur=prof, alpha=-math.inf, beta=math.inf, est_maximisant=True)
                    temps_minimax.append(time.perf_counter() - debut)
            else:
                if not ab_est_joueur_1:
                    # adapter = AdapterPlateau(plateau)
                    debut = time.perf_counter()
                    _, coup = ab.alpha_beta(adapter, profondeur=prof, alpha=-math.inf, beta=math.inf, est_maximisant=False)
                    temps_alpha_beta.append(time.perf_counter() - debut)
                else:
                    debut = time.perf_counter()
                    _, coup = mm.minimax(plateau, prof, -1)
                    # _, coup = ab.alpha_beta(adapter, profondeur=prof, alpha=-math.inf, beta=math.inf, est_maximisant=False)
                    temps_minimax.append(time.perf_counter() - debut)

            if coup is None:
                coup = random.choice(coups_possibles)

            if plateau.phase == 1:
                GameRules.place_piece(plateau, coup)
            else:
                GameRules.move_piece(plateau, coup[0], coup[1])
                
            nombre_coups += 1

        winner = GameRules.check_winner(plateau)
        if winner == 1:
            if ab_est_joueur_1: victoires_alpha_beta += 1
            else: victoires_minimax += 1
        elif winner == -1:
            if not ab_est_joueur_1: victoires_alpha_beta += 1
            else: victoires_minimax += 1
        else:
            nuls += 1

    moyen_ab = (sum(temps_alpha_beta) / len(temps_alpha_beta)) * 1000 if temps_alpha_beta else 0
    moyen_mm = (sum(temps_minimax) / len(temps_minimax)) * 1000 if temps_minimax else 0
    gain_vitesse = (moyen_mm / moyen_ab) if moyen_ab > 0 else 1

    print("\n==================================================")
    print("      RAPPORT DE BENCHMARK    ")
    print("==================================================")
    print(f"Nombre total de parties simulées : {nombre_parties}")
    print(f"Victoires Alpha-Beta            : {victoires_alpha_beta} ({victoires_alpha_beta/nombre_parties*100:.1f}%)")
    print(f"Victoires Minimax               : {victoires_minimax} ({victoires_minimax/nombre_parties*100:.1f}%)")
    print(f"Matches Nuls (ou boucles) : {nuls} ({nuls/nombre_parties*100:.1f}%)")
    print("--------------------------------------------------")
    print(f"Temps de réponse Alpha-Beta     : {moyen_ab:.4f} ms")
    print(f"Temps de réponse Minimax        : {moyen_mm:.4f} ms")
    print(f"Gain d'efficacité algorithmique   : {gain_vitesse:.1f}x plus rapide")
    print("==================================================")

if __name__ == "__main__":
    executer_benchmarks(100)