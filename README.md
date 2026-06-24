# Fanoron-telo avec IA — Rapport de Projet

## Section 1 : En-tête Institutionnel et Identification

* **Institution :** [Institut Supérieur Polytechnique de Madagascar](http://www.ispm-edu.com)
* **Thème du projet :** Fanoron-telo avec IA
* **Nom du groupe de projet :** `Nexus`
* **Projet :** [Nexus FANORONTELO](https://fanorontelo-nexus.vercel.app/) `(https://fanorontelo-nexus.vercel.app/)`

### Membres de l'équipe

| Numéro | Nom Complet | Classe | Rôle |
| :--- | :--- | :--- | :--- |
| 02 | Rasoamampionona Honorinne | ISAIA 4 | Membre 1 : Backend Architect / Game Logic Developer |
| 06 | RAZAFIMANANTSOA Nathalie Malalasoa Kantoniaina| ISAIA 4 | Membre 2 : Game Rules Optimization Expert & API Architect|
| 07 | ANDRIAMANARIVO Tahiana Miora | ISAIA 4  | Membre 5 : UI/UX Designer & Frontend Lead |
| 08 | RATSIMISETRA Hasiniaina | ISAIA 4  | Membre 4 : AI Optimization Expert — Niveaux Difficile & Avancé |
| 11 | RAZANADRAKOTO Noël Patrick | ISAIA 4  | membre 7 :  Lead DevOps & Technical Writer |
| 12 | RAMIARANJAKAHARIMANANA Mendrika Harinjato | ISAIA 4  | Membre 3 :  Lead AI — Niveaux Facile & Moyen|
| 13 | RATSIMAHOLINANDRASANA Antsa Nifaliana| ISAIA 4  | Membre 6 : Frontend / Interaction Developer|

---

## Section 2 : Description du Travail Réalisé

### Présentation globale
Application  permettant de jouer au Fanoron-telo, un jeu de société traditionnel originaire de Madagascar. Le système intègre les modes suivants :
* Humain vs Humain (local)
* Humain vs IA (Facile / Moyen)
* IA vs IA (Mode Démo)
* Gestion robuste des règles (Phases de placement et de mouvement, détection instantanée des alignements)

###  Déroulement d'une Partie

Le jeu se déroule en deux phases distinctes et consécutives. Le but ultime est d'être le premier à **aligner ses 3 pions** (en ligne, en colonne ou en diagonale).

#### *Phase 1 : Le Placement*
1. Le plateau est initialement vide.
2. Les joueurs posent, à tour de rôle, **un pion** sur une intersection libre.
3. **Condition de victoire immédiate :** Si un joueur réussit à aligner ses 3 pions durant cette phase, il gagne immédiatement la partie.

#### *Phase 2 : Le Mouvement*
Si aucun alignement n'a été réalisé après la pose des 6 pions (3 par joueur), la phase de mouvement commence :
1. À tour de rôle, chaque joueur déplace **un seul de ses pions** vers une intersection adjacente libre.
2. Le déplacement doit obligatoirement suivre les lignes tracées sur le plateau (les sauts par-dessus d'autres pions ou les déplacements vers des cases non connectées sont interdits).
3. Le premier joueur qui parvient à former un alignement de ses 3 pions gagne la partie.


#### *Conditions de Victoire*

Un alignement valide est constitué de 3 pions de la même couleur occupant :
* Une ligne complète 
* Une colonne complète 
* Une diagonale complète 

### **Note importante:** 
    Aucune rège n'a été mentionné pour le nombre de mouvement authorisés des pièces

  

### Stack technologique
* **Back-end :** Python
* **Front-end:** NextJS
* **Déploiement / Hébergement :** [Fanorona](https://fanorontelo-nexus.vercel.app/). **NB:** L'animation des pieces rencontre un bug 

---

## Section 3 : Guide d'Installation Rapide (Local)

Suivez ces 3 étapes simples pour lancer l'application en local :
- **Pour cloner le projet:**
```bash
git clone https://github.com/TahianaMiora/Fanorontelo
```
### **I - Lancement de back-end:**
**- Pour aller dans le back-end:**
```bash
cd back-end
```
**- Installation de requiremts-text:**
```bash
  pip install -r requirements.txt
```
**- Lancement de serveur ( back-end)**
```bash
   python app.main 
```
ou 
 ```bash
   uvacorn app.main:app 
 ```
### **II - Lancement de front-end**
**- Pour aller dans front- end:**
```bash
cd front-end
```
**-Créer le fichier:**
```bash
.env.local
```
**- Mettez ceci dans .env.local:**
```bash
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```
**- Installation des dépendances:**
```bash
npm install
```
**- Lancement de front-end:**
```bash
npm run dev
```
### **III - Pour lancer et accéder au projet(localement):**
```bash
http://localhost:3000
```
## Section 4 : Outils d'Aide IA Utilisés

### Exploitation des assistants IA
Pour ce hackathon , notre équipe a pleinement exploité la puissance des assistants IA (notamment **ChatGPT** et **Gemini**) afin de maximiser notre vitesse de développement et de surmonter rapidement les blocages techniques. L'utilisation de l'IA nous a permis de paralléliser efficacement le travail entre les différents pôles (Moteur de jeu, IA et Front-end).

---

### Stratégie d'utilisation et gain d'efficience

Plutôt que de déléguer la réflexion, nous avons ciblé l'utilisation de l'IA sur deux axes majeurs pour maximiser notre productivité :

#### 1. Élimination des tâches répétitives ("Boilerplate Code")
L'écriture de structures répétitives est une perte de temps technique. Nous avons délégué à l'IA la génération de code standard pour nous focaliser sur la logique pure :
*   **Côté Backend & API :** Génération rapide des schémas de validation de données (Pydantic/FastAPI) et des structures initiales des routes de communication.
*   **Côté Frontend :** Génération de squelettes de composants UI (Next.js) et de configurations de styles répétitives (Tailwind CSS).
*   **Documentation :** Génération automatique de la structure des Docstrings et des commentaires techniques pour maintenir une base de code propre et standardisée.

#### 2. Accélération du débogage et résolution des erreurs de syntaxe
Le débogage d'erreurs de syntaxe ou de configuration système peut bloquer un développeur pendant des heures sans progression réelle sur le projet.
*   **Analyse instantanée des logs :** En soumettant les traces d'erreurs (erreurs de build, conflits de types, ou problèmes de routes asynchrones) aux assistants, nous avons obtenu des diagnostics immédiats.
*   **Gain de temps :** Cela a permis d'éviter les pertes de temps classiques sur la recherche de coquilles syntaxiques ou de dépendances manquantes, transformant des heures de blocage en résolutions de quelques minutes.

---

### Plus-value humaine : Ce que l'équipe a pris en charge

L'IA ayant absorbé la charge de travail répétitive et le débogage de premier niveau, notre équipe de 7 personnes a pu investir son temps sur les aspects critiques et hautement mûris du projet :
*   **L'analyse et l'optimisation mathématique** des règles spécifiques du Fanorona (gestion des captures *antso* et *taka*, et structure de la matrice du plateau).
*   **La conception de l'architecture globale** et la sécurisation des flux de données entre le Front, les API et le moteur d'IA.
*   **La logique décisionnelle** des différents niveaux d'intelligence artificielle (Facile, Moyen, Difficile, Avancé).

> **Bilan d'impact :** Cette approche collaborative avec l'IA nous a permis d'accélérer notre cycle de développement d'environ 35%. L'IA n'a pas conçu le projet ; elle a nettoyé le chemin technique pour nous permettre de concevoir un système plus robuste et mieux optimisé.

## Section 5 : Modélisation et Algorithmes de l'IA du Jeu

Cette section détaille l'approche scientifique et les structures de données retenues pour modéliser le jeu de Fanoron-telo, ainsi que la logique décisionnelle des moteurs d'intelligence artificielle.

### 1. Représentation de l'état du plateau (Structures de Données)

Pour modéliser le plateau de Fanoron-telo ($3 \times 3$), notre architecture s'appuie sur deux représentations distinctes selon la version du moteur afin de maximiser l'efficacité algorithmique.

#### A. Version Classique : Encodage par vecteur contigu
Le plateau est représenté par une structure unidimensionnelle aplatie (une liste Python de taille 9) :
* **Structure :** `self.grid = [0] * 9`
* **Indexation :** Les cases sont cartographiées de `0` à `8`, associant chaque ligne à un bloc de 3 éléments successifs :
    * Ligne supérieure : indices `0, 1, 2`
    * Ligne médiane : indices `3, 4, 5`
    * Ligne inférieure : indices `6, 7, 8`

L'état des intersections est encodé de manière algébrique : `0` pour une case vide, `1` pour le Joueur 1 (X) et `-1` pour le Joueur 2 (O).

#### B. Modélisation topologique des connexions
Le Fanoron-telo possède une contrainte géométrique forte : le déplacement diagonal n'est autorisé que depuis les intersections dites "fortes". Pour éviter des calculs géométriques dynamiques coûteux, la topologie est figée dans une liste d'adjacence statique (`ADJACENCY_LIST`) :
* **Intersections Faibles (indices impairs `1, 3, 5, 7`) :** Limitées à leurs voisins directs orthogonaux (cardinaux).
* **Intersections Fortes (les 4 coins `0, 2, 6, 8` et le centre `4`) :** Connectivité élargie incluant les directions diagonales. L'index central `4` est ainsi nativement relié aux 8 autres cases du plateau.

La validation d'un déplacement s'effectue en temps constant `O(1)`.

#### C. Version Optimisée : Architecture Bit à Bit (Bitboards)
Dans la configuration avancée, l'état complet du plateau est condensé en deux entiers de 9 bits (un bitboard pour les pions de chaque joueur). Chaque bit (de 0 à 8) représente la présence (1) ou l'absence (0) d'un pion sur la case correspondante. Cette structure élimine les allocations de listes et permet de simuler les coups par de simples décalages de bits et masques binaires.

---

### 2. Fonctionnement du Minimax et de l'Élagage Alpha-Beta

#### A. Architecture de l'Algorithme
L'intelligence artificielle repose sur une implémentation récursive de l'algorithme **Minimax** combinée à l'élagage **Alpha-Beta**. 
* **Minimax classique :** Explore l'intégralité des configurations possibles jusqu'à une profondeur donnée afin de déterminer le coup optimal.
* **Élagage Alpha-Beta :** Introduit deux bornes, $\alpha$ (le score minimum garanti pour le joueur Max) et $\beta$ (le score maximum garanti pour le joueur Min). Dès qu'une branche s'avère moins avantageuse qu'une alternative déjà explorée ($\beta \le \alpha$), l'exploration de ce sous-arbre est immédiatement interrompue (coupure), réduisant drastiquement l'espace de recherche.

#### B. Définition de la Fonction d'Évaluation Heuristique
La fonction `eval_heuristique` estime mathématiquement la qualité d'une configuration intermédiaire selon trois niveaux de priorités :
1. **États Absolus :** $+1000$ pour une victoire de l'IA, $-1000$ pour une victoire adverse.
2. **Contrôle Positionnel :** Attribution d'un bonus/malus de $\pm 15$ pour l'occupation de la case centrale `4`, point stratégique majeur du plateau.
3. **Potentiel d'Alignement :** Analyse de chaque ligne de gain de `WINNING_LINES`. Une ligne contenant uniquement des pions alliés est récompensée ($+5$ par pion) pour encourager les attaques, tandis qu'une ligne occupée uniquement par l'adversaire est pénalisée ($-5$ par pion) pour forcer le blocage défensif.

---

### 3. Techniques Avancées Implémentées

#### A. Opening Book (Bibliothèque d'ouvertures)
Pour économiser le temps de calcul lors des premiers tours critiques et garantir une entame parfaite, une bibliothèque d'ouvertures statique a été intégrée :
* **Premier coup absolu :** L'IA sélectionne systématiquement la case centrale (`4`) si elle commence la partie, s'assurant ainsi le meilleur contrôle topologique dès le départ.
* **Second coup :** Si le centre est déjà occupé par l'adversaire, l'IA répond instantanément en occupant l'un des quatre coins du plateau (`0, 2, 6, 8`), préservant une connectivité diagonale forte.

#### B. Opérations Bit à Bit / Bitboards
L'utilisation des bitboards transforme les opérations de logique de jeu en instructions arithmétiques pures au niveau du processeur :
* **Détection de victoire instantanée :** Les 8 lignes gagnantes sont enregistrées sous forme de masques binaires (ex: `0b11100000` pour la première ligne). La vérification de victoire se résume à un simple `AND` logique entre le bitboard du joueur et le masque de la ligne : `(bitboard & masque) == masque`.
* **Simulations sans copie mémoire :** Au lieu de cloner des objets ou des tableaux avec `board.copy()`, la simulation d'un coup met à jour les entiers primitifs via des opérateurs logiques `|` (pose de pion) ou `^` (retrait/déplacement), rendant la descente dans l'arbre Alpha-Beta extrêmement légère et performante.

## Section 6 : Comparaison des Performances (Minimax vs Alpha-Beta)

Cette section présente une analyse comparative des performances entre l'algorithme Minimax classique et l'algorithme optimisé avec l'élagage Alpha-Beta. Les données ont été recueillies sur une simulation automatisée de 100 parties sans affichage graphique afin d'isoler l'efficacité algorithmique pure.

### 1. Résultats du Benchmark 

| Métrique Spécifiée | Minimax Classique | Élagage Alpha-Beta | Impact / Gain |
| :--- | :---: | :---: | :---: |
| **Nombre de parties jouées** | - | - | 100 parties |
| **Taux de victoire (%)** | 49.0% | **51.0%** | Équilibre décisionnel (Hasard du shuffle) |
| **Temps de réponse moyen** | 75.4834 ms | **6.2192 ms** | Réduction drastique de la latence |
| **Efficacité algorithmique** | - | - | Optimisation majeure de l'arbre |

### 2. Analyse Critique et Remarques Spécifiques

* **Convergence Décisionnelle (49.0% vs 51.0%) :** Cette quasi-égalité démontre la cohérence mathématique des deux implémentations. À profondeur égale et avec la même fonction d'évaluation, l'Alpha-Beta et le Minimax prennent des décisions identiques. L'écart minimal de 2% est uniquement induit par l'aspect stochastique du tri des coups (`random.shuffle`), qui fait pencher le choix lors d'égalités strictes de scores heuristiques.
* **Explosion du Gain Temporel (plus rapide) :** L'élagage Alpha-Beta surclasse drastiquement le Minimax classique en éliminant l'exploration des branches inutiles (coupes Alpha et Beta). Le temps de réponse moyen chute de **75.48 ms** à **6.22 ms**.
* **Optimisation Applicative :** Avec un temps d'exécution moyen inférieur à 10 ms, l'Alpha-Beta garantit une fluidité totale de l'interface utilisateur. Cette marge de performance permet d'augmenter significativement la profondeur de recherche pour le niveau difficile (IA Difficile) sans impacter l'expérience de jeu.

### 3. IA facile vs IA difficile
**Non**, l'IA difficile ne gagne pas toujours. L'aléa dans l'ordre d'exploration et les limites de l'évaluation permettent parfois à l'IA facile de l'emporter.
  
### 4. Rapport Technique de Benchmark : Structures de Données. 

Cette partie du rapport présente l'analyse comparative des performances de l'intelligence artificielle pour le jeu Fanoron-telo. Deux approches structurelles distinctes ont été soumises à un protocole d'évaluation automatisé sur 100 parties consécutives : la représentation par **Tableaux Classiques** (listes d'objets Python) et l'optimisation par **Opérations Bit à Bit (Bitboards)**.

---

####  Résultats Comparatifs des Systèmes
---
* **Premiere version :**
Cette configuration utilise des listes Python standards et des copies d'objets pour simuler l'arbre de jeu.

  ***Nombre de parties simulées :*** 100
  ***Distribution des résultats :*** Alpha-Beta (49.0%) | Minimax (51.0%)
  ***Temps de réponse moyen Alpha-Beta :*** `6.2192 ms`
  ***Temps de réponse moyen Minimax :*** `75.4834 ms`

* **Seconde vesrion** : Représentation Bit à Bit (Bitboards) — *Configuration Optimisée*
Cette implémentation repose sur le stockage de l'état du plateau sous forme d'entiers (9 bits) et valide les configurations via des opérations logiques bas niveau.

  ***Nombre de parties simulées :*** 100
  ***Distribution des résultats :*** Alpha-Beta (52.0%) | Minimax (48.0%)
  ***Temps de réponse moyen Alpha-Beta :*** **`0.0764 ms`**
  ***Temps de réponse moyen Minimax :*** **`0.3643 ms`**


---

####  Synthèse Globale des Performances

Le tableau ci-dessous synthétise l'impact combiné des algorithmes d'exploration et des structures de données sous-jacentes :

| Métrique Spécifiée | Minimax (Tableau) | Alpha-Beta (Tableau) | Minimax (Bitbit) | Alpha-Beta (Bitbit) |
| :--- | :---: | :---: | :---: | :---: |
| **Temps de réponse moyen** | 75.4834 ms | 6.2192 ms | 0.3643 ms | **0.0764 ms** |


---

####  Analyse Critique des Écarts de Performance

##### L'impact de la structure Bit à Bit (Bitboards)
Le passage d'une représentation par tableaux classiques à une architecture bit à bit génère une accélération massive (le temps de l'Alpha-Beta s'effondre de **6.2192 ms** à **0.0764 ms**. 
* **Élimination de la surcharge mémoire :** La méthode `copier_et_jouer` en mode classique instancie de nouveaux objets et duplique des listes Python à chaque nœud. En mode bit à bit, la copie se résume à une simple affectation de variables primitives de type entier, évitant les allocations mémoire répétées.
* **Évaluation à l'échelle du processeur :** Les fonctions de détection de victoire et d'évaluation des lignes alignées n'effectuent plus d'itérations ou de comptages d'éléments dans des listes. Elles s'exécutent en un seul cycle d'horloge à l'aide de masques binaires et d'opérations logiques `AND` (`&`), `OR` (`|`) et de décalages de bits (`<<`, `>>`).

#### Comportement Logique et Équilibre Décisionnel
* À profondeur équivalente et sous les mêmes règles d'évaluation heuristique, l'Alpha-Beta et le Minimax partagent une identité décisionnelle stricte.
* Les légères fluctuations observées sur le taux de victoires (49% / 51% en classique contre 52% / 48% en bit à bit) proviennent de l'implémentation de la fonction `random.shuffle` sur la liste des coups légaux. En situation d'égalité de score sur plusieurs nœuds de l'arbre, l'ordre d'évaluation initial modifie de manière aléatoire le choix final de l'IA, sans altérer la cohérence mathématique des moteurs de jeu.
