# 🚀 SocialAI Studio - Assistant de Publication Réseaux Sociaux & Blog (IA Locale)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![OS: Windows 11](https://img.shields.io/badge/OS-Windows%2011-blue.svg)]()

**SocialAI Studio** est une application desktop Open-Source développée en **Python** pour **Windows 11**. Elle permet d'automatiser la rédaction, la déclinabilité multi-plateformes via une **IA locale confidentielle (LM Studio)**, la prévisualisation et la publication sur votre blog **WordPress** (auto-hébergé sur O2Switch ou autre) ainsi que sur vos réseaux sociaux (Facebook, Instagram, Twitter/X, LinkedIn).

---

## ✨ Fonctionnalités Principales

- **🤖 IA Locale & Confidentielle (LM Studio)** : Exécutez vos LLM directement sur votre PC (`http://localhost:1234`) sans frais d'API et en toute confidentialité.
- **🌐 Intégration WordPress REST API** : Publication directe, gestion des brouillons et téléversement de l'image à la une (compatible **O2Switch** avec les Mots de passe d'application).
- **✍️ Éditeur Direct & Déclinaison IA** : Rédigez un message unique et déclinez-le automatiquement selon les règles de chaque réseau (Twitter/X, Instagram, Facebook, LinkedIn, WordPress).
- **🔥 Veille de Tendances (US 1.5)** : Agrégateur d'actualités chaudes via Google News RSS pour trouver des idées et les injecter en 1 clic dans l'éditeur.
- **👁️ Aperçu WYSIWYG Réaliste (US 3.1)** : Simulation visuelle fidèle du rendu final pour chaque plateforme.
- **📚 Assistant Documentation Clés API (US 4.4)** : Guides pas-à-pas intégrés pour obtenir vos identifiants sur chaque plateforme.

---

## 🛠️ Stack Technique & Architecture Open-Source

Le projet est conçu pour être **simple à maintenir**, **modulaire** et **100% Open-Source** :

```text
pensioncanine/
├── main.py                    # Point d'entrée principal
├── config.py                  # Gestionnaire de configuration JSON local
├── LICENSE                    # Licence Open-Source MIT
├── README.md                  # Documentation du projet
├── core/                      # Services Backend & Connecteurs API
│   ├── lm_studio_client.py    # Connecteur LM Studio (API OpenAI-compatible)
│   ├── wordpress_client.py   # Connecteur WordPress REST API (O2Switch compatible)
│   ├── trend_watcher.py       # Module de veille de tendances (RSS/Google News)
│   └── api_docs_guide.py      # Assistant documentaire pour clés API
├── ui/                        # Interface Utilisateur (CustomTkinter)
│   ├── app.py                 # Fenêtre principale et navigation
│   ├── theme.py               # Thème graphique Windows 11 Dark Mode
│   └── components/            # Onglets et composants modulaires
│       ├── editor_tab.py      # Éditeur Direct & Actions IA
│       ├── preview_tab.py     # Aperçu WYSIWYG
│       ├── trends_tab.py      # Panneau de Veille
│       ├── lm_studio_tab.py   # Panneau Configuration LM Studio
│       ├── api_guide_tab.py   # Panneau Guide Clés API
│       └── accounts_tab.py    # Panneau Comptes & Connexion WP
└── tests/                     # Tests unitaires
    └── test_app_logic.py
```

---

## 📥 Installation & Lancement rapide

### Prérequis
- **Python 3.10+** (Testé sur Python 3.14 sous Windows 11).
- **LM Studio** (facultatif mais recommandé pour les fonctionnalités IA locales) : [https://lmstudio.ai/](https://lmstudio.ai/).

### 1. Cloner le projet & Installer les dépendances

```powershell
pip install customtkinter requests openai
```

### 2. Lancer l'application

```powershell
python main.py
```

---

## 🔌 Configuration de votre Blog WordPress (ex: Hébergement O2Switch)

Pour connecter votre blog WordPress auto-hébergé sur **O2Switch** :

1. Connectez-vous à votre tableau de bord WordPress (`https://votre-site.com/wp-admin`).
2. Allez dans **Utilisateurs** ➡️ **Profil**.
3. Dans la section **Mots de passe d'application**, saisissez un nom (ex: `SocialAI Studio`) et cliquez sur **Ajouter un mot de passe d'application**.
4. Dans l'onglet **⚙️ Comptes & WordPress** de notre application, renseignez :
   - **URL du Blog** : `https://votre-site.com`
   - **Identifiant** : Votre nom d'utilisateur WordPress
   - **Mot de passe d'application** : Le code à 16 caractères généré
5. Cliquez sur **🔌 Tester Connexion WP**.

---

## 🧪 Lancer les Tests

Pour exécuter la suite de tests automatisés :

```powershell
python -X utf8 tests/test_app_logic.py
```

---

## 🗺️ Roadmap & Évolutions Futures

- [ ] **🔍 Module SEO & Idéation "Zero-Cost" (Clone Answer The Public)** :
  - Générateur automatique de questions fréquentes et de mots-clés longue traîne via l'API Google Autocomplete (100% gratuit, sans compte ni clé API).
  - Injection directe des questions trouvées (*Qui, Que, Pourquoi, Comment, Prix...*) dans l'Éditeur pour rédaction assistée par l'IA locale.
- [ ] **🌐 Hub d'Outils & Ressources Web Gratuits** :
  - Raccourcis et intégrations des outils d'analyse web/SEO gratuits pour enrichir la veille éditoriale.
- [ ] **📊 Import de données SEO (CSV / Excel)** :
  - Support de l'import de listes de mots-clés provenant d'outils externes (LowFruits, Ubersuggest, Google Keyword Planner) pour planifier les articles et posts.

---

## 📄 Licence

Ce projet est distribué sous **Licence MIT Open-Source**. Vous êtes libre de l'utiliser, le modifier et le distribuer. Voir le fichier [LICENSE](LICENSE) pour plus de détails.