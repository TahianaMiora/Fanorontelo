import math
import random
import time
from typing import List, Optional, Tuple, Union
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

if __name__ == "__main__":
    from alpha_beta import alpha_beta
    from core.board import FanoronTeloBoard
    from core.game_rules import GameRules
else:
    from app.ai.alpha_beta import alpha_beta
    from app.core.board import FanoronTeloBoard
    from app.core.game_rules import GameRules

Move = Union[int, Tuple[int, int]]


class OpeningBook:
    @staticmethod
    def get_opening_move(board: FanoronTeloBoard) -> Optional[int]:
        """Book d'ouverture simple pour la phase de placement."""
        total_placed = sum(1 for value in board.grid if value != 0)
        if total_placed == 0:
            return 4
        if total_placed == 1 and board.grid[4] != 0:
            return random.choice([0, 2, 6, 8])
        return None


class AlphaBetaAdapter:
    """Adaptateur pour utiliser l'alpha-beta avec FanoronTeloBoard."""

    def __init__(self, board: FanoronTeloBoard):
        self.board = board

    def verifier_victoire(self) -> bool:
        return GameRules.check_winner(self.board) != 0

    def est_match_nul(self) -> bool:
        return GameRules.check_winner(self.board) == 0 and len(GameRules.get_legal_moves(self.board)) == 0

    def evaluer_score_terminal(self) -> int:
        winner = GameRules.check_winner(self.board)
        if winner == 1:
            return 100
        if winner == -1:
            return -100
        return 0

    def evaluer_heuristique(self) -> int:
        return self.board.grid.count(1) - self.board.grid.count(-1)

    def obtenir_coups_legaux(self):
        return GameRules.get_legal_moves(self.board)

    def copier_et_jouer(self, move: Move):
        new_board = self.board.copy()
        if new_board.phase == 1:
            new_board.grid[move] = new_board.current_player
            new_board.pieces_placed[new_board.current_player] += 1
            if new_board.pieces_placed[1] == 3 and new_board.pieces_placed[-1] == 3:
                new_board.phase = 2
        else:
            src, dst = move
            new_board.grid[src] = 0
            new_board.grid[dst] = new_board.current_player

        if GameRules.check_winner(new_board) == 0:
            new_board.switch_player()
        return AlphaBetaAdapter(new_board)


class AIPlayer:
    def __init__(self, depth: int = 4):
        self.depth = depth

    def choose_move(self, board: FanoronTeloBoard, maximize: bool) -> Move:
        if board.phase == 1:
            book_move = OpeningBook.get_opening_move(board)
            if book_move is not None:
                return book_move

        score, move = alpha_beta(AlphaBetaAdapter(board), profondeur=self.depth, alpha=-math.inf, beta=math.inf, est_maximisant=maximize)
        if move is None:
            raise ValueError("Aucun coup valide trouvé pour l'IA")
        return move


class FanoronTeloEngine:
    def __init__(self):
        self.board = FanoronTeloBoard()
        self.ai_player = AIPlayer(depth=5)

    def reset(self):
        self.board = FanoronTeloBoard()

    def get_state(self):
        return {
            "grid": self.board.grid,
            "current_player": self.board.current_player,
            "phase": self.board.phase,
            "pieces_placed": self.board.pieces_placed,
            "winner": GameRules.check_winner(self.board),
            "legal_moves": GameRules.get_legal_moves(self.board),
        }

    def apply_move(self, move: Move) -> bool:
        if self.board.phase == 1 and isinstance(move, int):
            return GameRules.place_piece(self.board, move)
        if self.board.phase == 2 and isinstance(move, tuple) and len(move) == 2:
            return GameRules.move_piece(self.board, move[0], move[1])
        return False

    def undo(self) -> bool:
        return GameRules.undo(self.board)

    def redo(self) -> bool:
        return GameRules.redo(self.board)

    def ai_move(self) -> Move:
        maximize = self.board.current_player == 1
        return AIPlayer(depth=5).choose_move(self.board, maximize)

    def is_over(self) -> bool:
        return GameRules.check_winner(self.board) != 0 or len(GameRules.get_legal_moves(self.board)) == 0

    def get_winner(self) -> int:
        return GameRules.check_winner(self.board)

    def display(self):
        symbols = {0: ".", 1: "X", -1: "O"}
        print("\nPlateau Fanoron-telo")
        for row in range(3):
            line = " | ".join(symbols[self.board.grid[row * 3 + col]] for col in range(3))
            print(f" {line} ")
            if row < 2:
                print("---+---+---")
        print(f"Joueur actuel : {'X' if self.board.current_player == 1 else 'O'} | Phase : {self.board.phase}")
        print(f"Winner : {self.get_winner()} | Coups légaux : {GameRules.get_legal_moves(self.board)}\n")


class ConsoleGame:
    def __init__(self, mode: str = "human_vs_human", human_side: int = 1, ai_depth: int = 5):
        self.engine = FanoronTeloEngine()
        self.mode = mode
        self.human_side = human_side
        self.ai_depth = ai_depth
        self.ai = AIPlayer(depth=ai_depth)

    def _parse_move(self, raw: str) -> Optional[Move]:
        raw = raw.strip().lower()
        if raw in ["undo", "u"]:
            return "undo"
        if raw in ["redo", "r"]:
            return "redo"
        if raw in ["reset", "restart"]:
            return "reset"
        if self.engine.board.phase == 1:
            if raw.isdigit():
                position = int(raw)
                if 0 <= position <= 8:
                    return position
        else:
            parts = [p.strip() for p in raw.replace(";", ",").split(",") if p.strip()]
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                return (int(parts[0]), int(parts[1]))
        return None

    def _execute_command(self, command: str) -> bool:
        if command == "undo":
            if self.engine.undo():
                print("Annulation réussie.")
                return True
            print("Aucun coup à annuler.")
            return False
        if command == "redo":
            if self.engine.redo():
                print("Rétablissement réussi.")
                return True
            print("Aucun coup à rétablir.")
            return False
        if command == "reset":
            self.engine.reset()
            print("Partie réinitialisée.")
            return True
        return False

    def _human_move(self) -> bool:
        prompt = "Entrez un emplacement (0-8), 'undo', 'redo', 'reset' : " if self.engine.board.phase == 1 else "Entrez un mouvement src,dest, 'undo', 'redo', 'reset' : "
        raw = input(prompt)
        parsed = self._parse_move(raw)
        if parsed in ["undo", "redo", "reset"]:
            return self._execute_command(parsed)
        if parsed is None:
            print("Entrée invalide. Réessayez.")
            return False
        if self.engine.apply_move(parsed):
            return True
        print("Coup invalide ou non autorisé.")
        return False

    def _ai_move(self):
        move = self.ai.choose_move(self.engine.board, maximize=self.engine.board.current_player == 1)
        print(f"IA joue : {move}")
        self.engine.apply_move(move)

    def play(self):
        print(f"Lancement du mode {self.mode}...")
        while True:
            self.engine.display()
            if self.engine.is_over():
                winner = self.engine.get_winner()
                if winner == 1:
                    print("Victoire de X !")
                elif winner == -1:
                    print("Victoire de O !")
                else:
                    print("Match nul ou bloqué.")
                break

            if self.mode == "ai_vs_ai":
                self._ai_move()
                time.sleep(0.5)
                continue

            current_player_is_human = self.mode == "human_vs_human" or self.engine.board.current_player == self.human_side
            if current_player_is_human:
                moved = self._human_move()
                if not moved:
                    continue
            else:
                self._ai_move()

    def run(self):
        self.play()


if __name__ == "__main__":
    game_type = input("Choisir mode (hvh / hva / aivai) : ").strip().lower()
    if game_type == "hvh":
        game = ConsoleGame(mode="human_vs_human")
    elif game_type == "hva":
        side = input("Jouer X ou O ? (x/o) : ").strip().lower()
        human_side = 1 if side == "x" else -1
        game = ConsoleGame(mode="human_vs_ai", human_side=human_side)
    else:
        game = ConsoleGame(mode="ai_vs_ai")

    game.run()
