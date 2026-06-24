# Fanoron-telo avec IA — Rapport de Projet

## Section 1 : En-tête Institutionnel et Identification

* **Institution :** [Institut Supérieur Polytechnique de Madagascar](http://www.ispm-edu.com)
* **Thème du projet :** Fanoron-telo avec IA
* **Nom du groupe de projet :** `Mbola tediavina`

### Membres de l'équipe

| Numéro | Nom Complet | Classe | Rôle |
| :--- | :--- | :--- | :--- |
| 02 | Rasoamampionona Honorinne | ISAIA 4 | Membre 1 : Backend Architect / Game Logic Developer |
| 06 | RAZAFIMANANTSOA Nathalie Malalasoa Kantoniaina| ISAIA 4 | Membre 2 : Optimization Expert & Règles|
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
* **Déploiement / Hébergement :** [Fanorona](https:localhost)

---

## Section 3 : Guide d'Installation Rapide

Suivez ces 3 étapes simples pour lancer l'application en local :

```bash
git clone <https://github.com/TahianaMiora/Fanorontelo>
npm install
npm run dev
```