# DeckChanges

Une application de bureau moderne et légère pour comparer facilement deux listes de decks Magic: The Gathering et voir instantanément les modifications.

## ✨ Fonctionnalités
- **Comparaison claire :** Voyez instantanément quelles cartes ont été ajoutées ou retirées entre deux versions d'un deck.
- **Interface moderne :** Construite avec `customtkinter` pour une interface soignée avec prise en charge automatique du mode Sombre/Clair.
- **Analyse intelligente :** Ignore automatiquement les sections `Maybeboard`, les balises d'édition (ex: `(M21)`), et les catégories personnalisées (ex: `[Commander]`).
- **Validation et gestion des erreurs :** Vérifie les tailles de decks standards (40, 60, 100) et affiche des avertissements en temps réel ou des erreurs de formatage directement dans l'interface.
- **Copie en un clic :** Copiez facilement le journal des modifications généré dans votre presse-papiers pour le partager avec vos amis.
- **Multiplateforme :** Disponible sous forme d'exécutable natif pour Windows et Linux.

## 🚀 Utilisation
1. Lancez l'application.
2. Collez votre liste de deck d'origine dans la zone de texte **Ancienne deck list**.
3. Collez votre liste de deck modifiée dans la zone de texte **Nouvelle deck list**.
4. Cliquez sur **Voir les changements**.
5. Une fenêtre contextuelle affichera les différences exactes, prêtes à être copiées !

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
   uv run main.py
   ```

### Builds automatisés (CI/CD)
Le projet est configuré avec des GitHub Actions. Chaque push ou pull request vers la branche `main` compile automatiquement des binaires autonomes et prêts à l'emploi pour **Windows** (`.exe`) et **Linux** (`ELF`) en utilisant PyInstaller.

Pour télécharger la dernière version :
1. Allez dans l'onglet **Releases** sur GitHub.
2. Téléchargez `DeckUpdater-windows` ou `DeckUpdater-ubuntu` situé dans la dernière release.

## 👥 Auteur
**Auguste Deroubaix** (agtdbx) 🔗 [GitHub](https://github.com/agtdbx)