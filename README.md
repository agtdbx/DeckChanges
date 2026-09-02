# DeckChanges

Une application de bureau moderne et légère pour comparer facilement deux listes de decks Magic: The Gathering et voir instantanément les modifications.

## ✨ Fonctionnalités
- **Comparaison claire :** Voyez instantanément quelles cartes ont été ajoutées ou retirées entre deux versions d'un deck.
- **Checklist d'assemblage :** Faites un clic droit sur une modification pour la marquer de façon bien visible (inversion des couleurs) et pointer facilement les changements déjà faits.
- **Prévisualisation des cartes :** Affichez l'illustration des cartes (recto et verso) d'un simple clic grâce à l'intégration de l'API Scryfall.
- **Import Archidekt intelligent :** Collez directement l'URL d'un deck Archidekt ; l'application extraira automatiquement la liste des cartes.
- **Analyse intelligente :** Ignore automatiquement les sections `Maybeboard`, les balises d'édition (ex: `(M21)`), et les catégories personnalisées (ex: `[Commander]`).
- **Validation et gestion des erreurs en temps réel :** Vérifie les tailles de decks standards (40, 60, 100) et affiche des avertissements en temps réel ou des erreurs de formatage directement dans l'interface pendant votre saisie.
- **Copie en un clic :** Copiez facilement le journal des modifications généré dans votre presse-papiers pour le partager avec vos amis.
- **Multiplateforme :** Disponible sous forme d'exécutable natif pour Windows et Linux.

## 🚀 Utilisation
1. Lancez l'application.
2. Collez votre liste de deck d'origine dans la zone de texte **Ancienne deck list**.
3. Collez votre liste de deck modifiée dans la zone de texte **Nouvelle deck list**.
4. Cliquez sur **Voir les changements**.
5. L'application bascule sur l'onglet des changements pour afficher les différences exactes, l'aperçu visuel, et copier le résultat !

### Format supporté
L'outil accepte les formats texte standards exportés par la plupart des sites de construction de decks en ligne. Les quantités doivent précéder le nom de la carte :
```text
1x Thermo-Alchemist
1x Guttersnipe [Mainboard]
1x Black Lotus (M10)
```

## 🛠️ Développement et Compilation

Ce projet utilise `uv`, un gestionnaire de paquets et de projets Python ultra-rapide, pour gérer les dépendances et les environnements de manière totalement transparente.

### Exécution en local
1. Installez [uv](https://github.com/astral-sh/uv). (Sous Linux : `curl -LsSf https://astral.sh/uv/install.sh | sh`)
2. Clonez le dépôt et déplacez-vous dans le dossier.
3. Lancez l'application directement (les dépendances seront installées et gérées automatiquement) :
   ```bash
   uv run src/main.py
   ```

### Builds automatisés (CI/CD)
Le projet est configuré avec des GitHub Actions. Chaque push ou pull request vers la branche `main` compile automatiquement des binaires autonomes et prêts à l'emploi pour **Windows** (`.exe`) et **Linux** (`ELF`) en utilisant PyInstaller.

Pour télécharger la dernière version :
1. Allez dans l'onglet **Releases** sur GitHub.
2. Téléchargez `DeckChanges-windows` ou `DeckChanges-ubuntu` situé dans la dernière release.

## 👥 Auteur
**Auguste Deroubaix** (agtdbx) 🔗 [GitHub](https://github.com/agtdbx)