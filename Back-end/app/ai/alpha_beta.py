import math
import random

def alpha_beta(plateau, profondeur, alpha, beta, est_maximisant):
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
        return valeur_min, meilleur_coup