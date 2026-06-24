# app/api/routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Union, Tuple
from app.core.board import FanoronTeloBoard
from app.core.game_rules import GameRules
from app.ai.advanced import calculer_coup_ia
from app.ai import minimax as minimax_module
from app.ai import alpha_beta as alpha_beta_module

router = APIRouter()

# Instance globale de la partie en cours en mémoire vive
current_game = FanoronTeloBoard()

# Modèle de données pour recevoir le coup du Frontend
class MoveRequest(BaseModel):
    # En phase 1: un entier (ex: 4) : position du pion à placer
    # En phase 2: un tuple/liste de 2 entiers (ex: [0, 4]) : [source, destination] du pion à déplacer
    move: Union[int, Tuple[int, int]]

# Modèle de configuration pour le mode IA vs IA ou choix de difficulté
class AIConfigRequest(BaseModel):
    level_ia_x: str = "facile"  # "facile", "moyen", "difficile"
    level_ia_o: str = "moyen"   # "facile", "moyen", "difficile"

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

@router.post("/ai-move")
def play_ai_move(niveau: str = "moyen"):
    """
    Exécute le coup de l'IA pour le joueur actuel (Mode Joueur vs IA).
    """
    # Vérification si la partie est déjà terminée
    if GameRules.check_winner(current_game) != 0 or not GameRules.get_legal_moves(current_game):
        raise HTTPException(status_code=400, detail="La partie est terminée. Impossible de faire jouer l'IA.")

    # Déterminer si l'IA en cours doit maximiser ou non
    est_max = (current_game.current_player == 1)

    # Calcul du coup
    coup = calculer_coup_ia(current_game, est_max=est_max, niveau=niveau)
    if coup is None:
        raise HTTPException(status_code=400, detail="L'IA n'a trouvé aucun coup légal.")

    # Application du coup calculé
    if current_game.phase == 1:
        GameRules.place_piece(current_game, coup)
    else:
        GameRules.move_piece(current_game, coup[0], coup[1])

    return get_game_state()

@router.post("/ai-vs-ai")
def play_ai_vs_ai_step(config: AIConfigRequest):
    """
    Exécute un unique coup automatique (IA vs IA) sur la partie globale 
    en fonction du tour du joueur actuel et des difficultés configurées.
    """
    # Vérification si la partie est finie
    if GameRules.check_winner(current_game) != 0 or not GameRules.get_legal_moves(current_game):
        raise HTTPException(status_code=400, detail="La partie est terminée ou bloquée.")

    # Sélection de la configuration selon le joueur actif
    if current_game.current_player == 1:
        est_max = True
        niveau_actuel = config.level_ia_x
    else:
        est_max = False
        niveau_actuel = config.level_ia_o

    # Calcul et application du coup de l'IA désignée
    coup = calculer_coup_ia(current_game, est_max=est_max, niveau=niveau_actuel)
    if coup is None:
        raise HTTPException(status_code=400, detail="Aucun coup valide trouvé par l'IA.")

    if current_game.phase == 1:
        GameRules.place_piece(current_game, coup)
    else:
        GameRules.move_piece(current_game, coup[0], coup[1])

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
    # Vider les tables de transposition pour éviter les interférences entre parties
    try:
        minimax_module.transposition_table.clear()
    except Exception:
        pass
    try:
        alpha_beta_module.transposition_table.clear()
    except Exception:
        pass
    return get_game_state()