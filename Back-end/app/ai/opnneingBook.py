
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from random import random


class OpeningBook:
    @staticmethod
    def obtenir_coup_ouverture(plateau):
        cases = getattr(plateau, 'cases', None)
        if cases is None:
            cases = getattr(plateau, 'grid', [0] * 9)
        pions_poses = sum(1 for c in cases if c != 0)
        if pions_poses == 0:
            return 4
        if pions_poses == 1 and cases[4] != 0:
            return random.choice([0, 2, 6, 8])
        return None