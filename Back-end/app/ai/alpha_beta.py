import math
import random
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Table de transposition simple: clé -> (value, best_move, depth)
transposition_table = {}

def alpha_beta(plateau, profondeur, alpha, beta, est_maximisant):
    # clé basée sur bitboards si disponibles
    try:
        b = plateau.board if hasattr(plateau, 'board') else plateau
        key = (getattr(b, 'x_bits', 0), getattr(b, 'o_bits', 0), getattr(b, 'current_player', 0), getattr(b, 'phase', 0), profondeur, est_maximisant)
        if key in transposition_table:
            val, mv, d = transposition_table[key]
            if d >= profondeur:
                return val, mv
    except Exception:
        key = None

    if plateau.verifier_victoire():
        return (plateau.evaluer_score_terminal(), None)
    if profondeur == 0 or plateau.est_match_nul():
        return (plateau.evaluer_heuristique(), None)

    coups_legaux = plateau.obtenir_coups_legaux()
    random.shuffle(coups_legaux)
    meilleur_coup = None

    if est_maximisant:
        valeur_max = -math.inf
        for coup in coups_legaux:
            copie_plateau = plateau.copier_et_jouer(coup)
            score, _ = alpha_beta(copie_plateau, profondeur - 1, alpha, beta, False)
            if score > valeur_max:
                valeur_max = score
                meilleur_coup = coup
            alpha = max(alpha, valeur_max)
            if beta <= alpha:
                break
        if key is not None:
            transposition_table[key] = (valeur_max, meilleur_coup, profondeur)
        return valeur_max, meilleur_coup
    else:
        valeur_min = math.inf
        for coup in coups_legaux:
            copie_plateau = plateau.copier_et_jouer(coup)
            score, _ = alpha_beta(copie_plateau, profondeur - 1, alpha, beta, True)
            if score < valeur_min:
                valeur_min = score
                meilleur_coup = coup
            beta = min(beta, valeur_min)
            if beta <= alpha:
                break
        if key is not None:
            transposition_table[key] = (valeur_min, meilleur_coup, profondeur)
        return valeur_min, meilleur_coup