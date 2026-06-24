from typing import Optional, Tuple
import random

import sys, os
# Aligne dynamiquement le chemin de recherche sur la racine du projet (Back-end)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.board import FanoronTeloBoard
from app.core.game_rules import GameRules
from app.ai import minimax as minimax_module
from app.ai import advanced as ab_module



def display_help():
    print("Commands: 'undo', 'redo', 'quit', or enter move as described.")


def human_move_input(board: FanoronTeloBoard) -> Optional[object]:
    legal = GameRules.get_legal_moves(board)
    if board.phase == 1:
        s = input(f"Entrez une position (0-8) parmi {legal}: ").strip()
        if s in ("undo", "redo", "quit"):
            return s
        try:
            pos = int(s)
            if pos in legal:
                return pos
        except Exception:
            pass
        print("Coup invalide.")
        return None
    else:
        s = input(f"Entrez 'src dest' parmi {legal} (ex: '0 1'): ").strip()
        if s in ("undo", "redo", "quit"):
            return s
        parts = s.split()
        if len(parts) == 2:
            try:
                src, dst = int(parts[0]), int(parts[1])
                if (src, dst) in legal:
                    return (src, dst)
            except Exception:
                pass
        print("Coup invalide.")
        return None


def main():
    print("=== FANORON-TELO : IA vs HUMAIN (terminal) ===")
    board = FanoronTeloBoard()

    # Choix de l'algorithme
    alg = input("Algorithme IA ? Tapez 'minimax' ou 'alphabeta' (default alphabeta): ").strip().lower()
    if alg not in ('minimax', 'alphabeta'):
        alg = 'alphabeta'

    niveau = input("Difficulté ? 'facile' ou 'moyen' (default moyen): ").strip().lower()
    if niveau not in ('facile', 'moyen'):
        niveau = 'moyen'

    # Choix du côté humain
    choice = input("Jouez-vous X (1) ou O (-1) ? Entrez X ou O (default X): ").strip().upper()
    human_player = 1 if choice != "O" else -1
    ai_player = -human_player
    print(f"Vous jouez {'X' if human_player==1 else 'O'}. Algorithme IA: {alg} | Difficulté: {niveau}\n")

    board.display_board()

    while True:
        winner = GameRules.check_winner(board)
        if winner != 0:
            print(f"Victoire de {'X' if winner==1 else 'O'} !")
            break
        legal = GameRules.get_legal_moves(board)
        if not legal:
            print("Plus de coups légaux : match nul ou bloqué.")
            break

        if board.current_player == human_player:
            cmd = None
            while cmd is None:
                val = human_move_input(board)
                if val is None:
                    continue
                if val == 'undo':
                    GameRules.undo(board)
                    board.display_board()
                    cmd = 'undone'
                    break
                if val == 'redo':
                    GameRules.redo(board)
                    board.display_board()
                    cmd = 'redone'
                    break
                if val == 'quit':
                    print('Abandon. Fin du jeu.')
                    return
                # a valid move
                if board.phase == 1:
                    ok = GameRules.place_piece(board, val)
                else:
                    ok = GameRules.move_piece(board, val[0], val[1])
                if not ok:
                    print('Coup refusé par les règles.')
                else:
                    cmd = 'played'
            board.display_board()
        else:
            print("IA calcule...")
            est_max = True if ai_player == 1 else False
            if alg == 'minimax':
                coup = minimax_module.calculer_coup_ia(board, est_max, niveau=niveau)
            else:
                coup = ab_module.calculer_coup_ia(board, est_max, niveau=niveau)
            if coup is None:
                # fallback
                coup = random.choice(legal)
            if board.phase == 1:
                print(f"IA place en {coup}")
                GameRules.place_piece(board, coup)
            else:
                print(f"IA déplace {coup[0]} -> {coup[1]}")
                GameRules.move_piece(board, coup[0], coup[1])
            board.display_board()


if __name__ == '__main__':
    main()
