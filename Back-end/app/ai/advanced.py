import math
import time
import random
import alpha_beta as ab

class OpeningBook:
    @staticmethod
    def obtenir_coup_ouverture(plateau):
        # Valable uniquement pour le premier coup absolu de la phase de placement
        pions_poses = sum(1 for c in plateau.cases if c != 0)
        if pions_poses == 0:
            return 4
        if pions_poses == 1 and plateau.cases[4] != 0:
            return random.choice([0, 2, 6, 8])
        return None

class MockPlateau:
    # Graphe des connexions physiques du plateau Fanoron-telo (lignes, colonnes et diagonales)
    ADJACENCES = {
        0: [1, 3, 4],       1: [0, 2, 4],       2: [1, 4, 5],
        3: [0, 4, 6],       4: [0, 1, 2, 3, 5, 6, 7, 8],
        5: [2, 4, 8],       6: [3, 4, 7],       7: [6, 4, 8],
        8: [5, 4, 7]
    }

    def __init__(self, etat_cases=None, phase=1, coups_joues=0):
        self.cases = etat_cases if etat_cases else [0] * 9
        self.phase = phase  # 1: Placement, 2: Déplacement
        self.coups_joues = coups_joues

    def obtenir_coups_legaux(self):
        joueur_actuel = 1 if self.coups_joues % 2 == 0 else 2
        
        # PHASE 1 : Placement (Chaque joueur doit poser 3 pions -> 6 coups au total)
        if self.phase == 1:
            return [i for i, case in enumerate(self.cases) if case == 0]
            
        # PHASE 2 : Déplacement (Glissement vers une case adjacente libre)
        else:
            coups_deplacement = []
            for origine, case in enumerate(self.cases):
                if case == joueur_actuel:
                    for destination in self.ADJACENCES[origine]:
                        if self.cases[destination] == 0:
                            # Un coup est représenté par un tuple (origine, destination)
                            coups_deplacement.append((origine, destination))
            return coups_deplacement

    def copier_et_jouer(self, coup):
        nouvel_etat = list(self.cases)
        joueur_actuel = 1 if self.coups_joues % 2 == 0 else 2
        
        if self.phase == 1:
            nouvel_etat[coup] = joueur_actuel
        else:
            origine, destination = coup
            nouvel_etat[origine] = 0
            nouvel_etat[destination] = joueur_actuel

        prochains_coups = self.coups_joues + 1
        nouvelle_phase = 2 if prochains_coups >= 6 else 1
        
        return MockPlateau(nouvel_etat, nouvelle_phase, prochains_coups)

    def verifier_victoire(self):
        lignes = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]
        for l in lignes:
            if self.cases[l[0]] == self.cases[l[1]] == self.cases[l[2]] != 0:
                return True
        return False

    def evaluer_score_terminal(self):
        # Le joueur qui vient de jouer est le vainqueur
        dernier_joueur = 2 if self.coups_joues % 2 == 0 else 1
        return 100 if dernier_joueur == 1 else -100

    def est_match_nul(self):
        # Bloqué en phase 2 (aucun mouvement possible)
        return len(self.obtenir_coups_legaux()) == 0

    def evaluer_heuristique(self):
        return self.cases.count(1) - self.cases.count(2)

    def afficher(self):
        symboles = {0: '.', 1: 'X', 2: 'O'}
        print(f"\n   Plateau (Phase {self.phase} - Coup {self.coups_joues})")
        for i in range(0, 9, 3):
            print(f"   {symboles[self.cases[i]]} | {symboles[self.cases[i+1]]} | {symboles[self.cases[i+2]]}")
        print("-" * 15)

def calculer_coup_ia(plateau, est_max):
    if plateau.phase == 1:
        coup_ouverture = OpeningBook.obtenir_coup_ouverture(plateau)
        if coup_ouverture is not None:
            print("[Opening Book] Coup précalculé appliqué.")
            return coup_ouverture
            
    # Augmentation de la profondeur pour la phase de déplacement si nécessaire
    prof = 4 if plateau.phase == 1 else 9
    _, coup_calcule = ab.alpha_beta(plateau, profondeur=prof, alpha=-math.inf, beta=math.inf, est_maximisant=est_max)
    return coup_calcule

if __name__ == "__main__":
    plateau = MockPlateau()
    print("=== MODE DÉMO FANORON-TELO : IA 1 (X) VS IA 2 (O) ===")
    plateau.afficher()
    tour_ia_1 = True

    while not plateau.verifier_victoire() and not plateau.est_match_nul():
        if tour_ia_1:
            print("IA 1 (X) calcule...")
            coup = calculer_coup_ia(plateau, est_max=True)
            if plateau.phase == 1:
                print(f"IA 1 place un 'X' en case {coup}")
            else:
                print(f"IA 1 déplace un 'X' de la case {coup[0]} vers {coup[1]}")
            plateau = plateau.copier_et_jouer(coup)
            tour_ia_1 = False
        else:
            print("IA 2 (O) calcule...")
            coup = calculer_coup_ia(plateau, est_max=False)
            if plateau.phase == 1:
                print(f"IA 2 place un 'O' en case {coup}")
            else:
                print(f"IA 2 déplace un 'O' de la case {coup[0]} vers {coup[1]}")
            plateau = plateau.copier_et_jouer(coup)
            tour_ia_1 = True
            
        plateau.afficher()
        time.sleep(1)

    if plateau.verifier_victoire():
        print(f"Résultat : Victoire de l'IA {1 if not tour_ia_1 else 2} !")
    else:
        print("Résultat : Match nul ou situation bloquée !")