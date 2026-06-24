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
* **Déploiement / Hébergement :** [Fanorona](https://fanorontelo-nexus.vercel.app/)

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

### 🛠️ Stratégie d'utilisation et gain d'efficience

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

### 💡 Plus-value humaine : Ce que l'équipe a pris en charge

L'IA ayant absorbé la charge de travail répétitive et le débogage de premier niveau, notre équipe de 7 personnes a pu investir son temps sur les aspects critiques et hautement mûris du projet :
*   **L'analyse et l'optimisation mathématique** des règles spécifiques du Fanorona (gestion des captures *antso* et *taka*, et structure de la matrice du plateau).
*   **La conception de l'architecture globale** et la sécurisation des flux de données entre le Front, les API et le moteur d'IA.
*   **La logique décisionnelle** des différents niveaux d'intelligence artificielle (Facile, Moyen, Difficile, Avancé).

> 📈 **Bilan d'impact :** Cette approche collaborative avec l'IA nous a permis d'accélérer notre cycle de développement d'environ 35%. L'IA n'a pas conçu le projet ; elle a nettoyé le chemin technique pour nous permettre de concevoir un système plus robuste et mieux optimisé.
