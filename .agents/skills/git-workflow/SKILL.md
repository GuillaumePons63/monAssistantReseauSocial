---
name: git-workflow
description: Guide et instructions pour la gestion du dépôt Git du projet SocialAI Studio selon la convention Conventional Commits.
---

# 🐙 Workflow Git & Convention de Commits - SocialAI Studio

Ce skill définit les règles et processus pour la gestion des commits, des branches et du dépôt distant pour le projet **SocialAI Studio**.

---

## 📌 Convention de Commits : Conventional Commits

Tous les messages de commit doivent impérativement suivre le format standard **Conventional Commits** :

```text
<type>(<périmètre optionnel>): <description courte au présent en minuscules>
```

### 🏷️ Types de Commits Autorisés

- **`feat`** : Nouvelle fonctionnalité utilisateur ou module (ex: `feat(editor): ajout du sélecteur de ton`).
- **`fix`** : Correction de bug (ex: `fix(trends): résolution du plantage sur les flux RSS invalides`).
- **`docs`** : Mise à jour de la documentation (ex: `docs: ajout des étapes d'installation dans le README`).
- **`style`** : Modifications graphiques, thème ou formatage sans impact logique (ex: `style(theme): ajustement des bordures du mode sombre`).
- **`refactor`** : Réorganisation ou nettoyage du code sans modification de fonctionnalité (ex: `refactor(wordpress): simplification du téléversement des images`).
- **`test`** : Ajout ou correction de tests unitaires/d'intégration (ex: `test(core): ajout des tests pour TrendWatcher`).
- **`chore`** : Tâches de maintenance, dépendances, configuration (ex: `chore(git): mise à jour du fichier .gitignore`).

---

## 🌿 Gestion des Branches

- **`main`** : Branche stable de production. Tout code fusionné sur `main` doit passer les tests unitaires.
- **`feature/<nom-fonctionnalite>`** : Branche dédiée pour le développement de nouvelles fonctionnalités (ex: `feature/wordpress-drafts`).
- **`bugfix/<nom-correctif>`** : Branche dédiée pour la résolution de bugs.

---

## ⚡ Procédure Standard pour un Commit & Push

1. **Vérifier le statut du dépôt** :
   ```powershell
   git status
   ```

2. **Exécuter la suite de tests avant tout commit** :
   ```powershell
   python -X utf8 tests/test_app_logic.py
   ```

3. **Stager les fichiers modifiés** :
   ```powershell
   git add .
   ```

4. **Créer le commit avec la convention** :
   ```powershell
   git commit -m "<type>(<périmètre>): <description>"
   ```

5. **Publier sur le dépôt distant (GitHub)** :
   ```powershell
   git push origin main
   ```
