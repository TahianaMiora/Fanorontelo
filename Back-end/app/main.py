# app/main.py
from app.core.board import FanoronTeloBoard
from app.core.game_rules import GameRules

if __name__ == "__main__":
    # 1. On crée le plateau vide
    my_board = FanoronTeloBoard()
    
    # 2. On joue des coups via la classe de règles
    GameRules.place_piece(my_board, 0) # X place en 0
    GameRules.place_piece(my_board, 4) # O place en 4
    GameRules.place_piece(my_board, 1) # X place en 1
    
    # Affichage du résultat
    my_board.display_board()
    print(f"Vainqueur : {GameRules.check_winner(my_board)}")