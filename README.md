# 🌸 Projet Fanoron-telo — ISPM Hackathon

> Application de jeu Fanoron-telo développée en architecture découplée (FastAPI + Next.js) intégrant un moteur de jeu robuste, une IA Minimax Alpha-Beta à 3 niveaux, et un système d'historique Undo/Redo.

---

## 1. Présentation Générale et Règles du Jeu
Le Fanoron-telo est un jeu de société traditionnel de Madagascar se jouant sur un plateau de $3 \times 3$ intersections reliées par des lignes de déplacement.
* **Phase 1 (Placement) :** Chaque joueur place alternativement ses 3 pions sur les cases vides.
* **Phase 2 (Mouvement) :** Les joueurs glissent alternativement un pion vers une intersection adjacente libre en suivant les lignes du plateau.
* **Condition de Victoire :** Le premier joueur qui réussit à aligner ses 3 pions (horizontalement, verticalement ou diagonalement) remporte la partie.

## 2. Architecture Globale et Structure du Projet
Le projet adopte une approche modulaire et découplée (Clean Architecture) répartie comme suit :
* **Back-end (`/Back-end`) :** Conçu en Python avec **FastAPI**. Il encapsule le moteur de jeu indépendant (`board.py` et `game_rules.py`) et l'arbre de décision de l'IA.
* **Front-end (`/Front-end`) :** Interface client web moderne codée en **Next.js**, stylisée avec **Tailwind CSS** (thématique Aesthetic Girly) et animée de manière réactive.

## 3. Guide d'Installation et Lancement Local
### Back-end (Python)
1. Création et activation de l'environnement virtuel : `python -m venv .venv` puis activation.
2. Installation des dépendances : `pip install -r requirements.txt`
3. Lancement du serveur : `python app/main.py` (accessible sur `http://127.0.0.1:8000`)

### Front-end (Next.js)
1. Installation des modules : `npm install`
2. Lancement en mode développement : `npm run dev` (accessible sur `http://127.0.0.1:3000`)

## 4. Stratégie de Déploiement et Hébergement
* **Hébergement Back-end :** Déployé au sein d'un conteneur isolé **Docker** sur la plateforme cloud **Render / Koyeb**.
* **Hébergement Front-end :** Déployé sur la plateforme **Vercel**, configuré avec un pipeline de déploiement automatique lié à la branche principale GitHub.
* **Sécurité :** Filtrage des requêtes Cross-Origin (CORS) géré dynamiquement par variables d'environnement.

## 5. Modélisation de l'IA et Fonction d'Évaluation
L'Intelligence Artificielle repose sur un algorithme **Minimax optimisé par élagage Alpha-Beta** pour réduire drastiquement le nombre de nœuds explorés.
* **Fonction d'Évaluation :** Attribue un score de $+1000$ en cas de victoire humaine immédiate, $-1000$ en cas de victoire de l'IA, et un bonus de $\pm10$ pour le contrôle stratégique de la case centrale (index 4), essentielle pour bloquer les trajectoires adverses.
* **Niveaux :** *Facile* (coups aléatoires $O(1)$), *Moyen* (recherche limitée à une profondeur de 2), *Difficile* (recherche complète jusqu'à une profondeur de 6).

## 6. Outils d'IA Utilisés et Analyses de Performance
### Outils d'IA d'assistance au développement
* Utilisation de LLMs (Gemini / Copilot) pour la génération des structures de données matricielles, le débogage des types TypeScript du Frontend et la rédaction de la documentation technique.

### Analyses de Performance Algorithmique
* **Complexité Spatiale :** L'état du plateau est modélisé par un vecteur aplati 1D de 9 entiers. L'empreinte mémoire par nœud simulé est donc négligeable ($O(1)$).
* **Temps de Réponse de l'IA (Mesures) :** 
  * En mode *Moyen* (profondeur 2) : < 1 ms (calcul instantané).
  * En mode *Difficile* (profondeur 6) : ~ 2 ms à 5 ms maximum pour explorer l'intégralité des configurations possibles de l'arbre de jeu (l'espace des états d'un plateau $3 \times 3$ étant de seulement 19 683 combinaisons).
