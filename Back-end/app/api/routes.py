# app/api/routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Union, Tuple
from app.core.board import FanoronTeloBoard
from app.core.game_rules import GameRules

router = APIRouter()

# Instance globale de la partie en cours en mémoire vive
current_game = FanoronTeloBoard()

# Modèle de données pour recevoir le coup du Frontend
class MoveRequest(BaseModel):
    # En phase 1: un entier (ex: 4) : position du pion à placer
    # En phase 2: un tuple/liste de 2 entiers (ex: [0, 4]) : [source, destination] du pion à déplacer
    move: Union[int, Tuple[int, int]]

@router.get("/state")
def get_game_state():
    """Retourne l'état complet actuel du plateau au Frontend"""
    return {
        "grid": current_game.grid,
        "current_player": current_game.current_player,
        "phase": current_game.phase,
        "pieces_placed": current_game.pieces_placed,
        "winner": GameRules.check_winner(current_game),
        "legal_moves": GameRules.get_legal_moves(current_game)
    }

@router.post("/move")
def play_move(request: MoveRequest):
    """Exécute un coup envoyé par le joueur humain (X ou O)"""
    move = request.move
    
    # Adapter le type si c'est une liste envoyée en JSON pour la phase 2
    if isinstance(move, list):
        move = tuple(move)

    # Tenter d'appliquer le coup via le moteur de règles (gère l'anti-triche)
    success = False
    if current_game.phase == 1:
        if isinstance(move, int):
            success = GameRules.place_piece(current_game, move)
    else:
        if isinstance(move, tuple) and len(move) == 2:
            success = GameRules.move_piece(current_game, move[0], move[1])

    if not success:
        raise HTTPException(status_code=400, detail="Coup invalide ou non autorisé par les règles.")

    return get_game_state()

@router.post("/undo")
def undo_move():
    """Route bonus pour l'action Annuler du Frontend"""
    success = GameRules.undo(current_game)
    if not success:
        raise HTTPException(status_code=400, detail="Impossible d'annuler, aucun coup en historique.")
    return get_game_state()

@router.post("/redo")
def redo_move():
    """Route pour l'action Rétablir du Frontend"""
    success = GameRules.redo(current_game)
    if not success:
        raise HTTPException(status_code=400, detail="Impossible de rétablir, aucun coup à refaire.")
    return get_game_state()

@router.post("/reset")
def reset_game():
    """Réinitialise complètement la partie"""
    global current_game
    current_game = FanoronTeloBoard()
    return get_game_state()