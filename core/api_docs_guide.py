class APIDocsGuide:
    """Assistant documentaire pas-à-pas pour l'obtention des accès API (US 4.4)."""

    GUIDES = {
        "wordpress": {
            "title": "WordPress - Mot de Passe d'Application (Recommandé & Gratuit)",
            "icon": "🌐",
            "official_url": "https://make.wordpress.org/core/2020/11/05/application-passwords-integration-guide/",
            "summary": "Permet d'autoriser l'application à publier sur votre blog sans donner votre mot de passe principal.",
            "steps": [
                "1. Connectez-vous à votre tableau de bord WordPress (`/wp-admin`).",
                "2. Dans le menu de gauche, allez dans **Comptes** ➡️ **Profil** (ou Utilisateurs).",
                "3. Faites défiler vers le bas jusqu'à la section **Mots de passe d'application**.",
                "4. Entrez le nom de l'application (ex: `MonAssistantPublications`) puis cliquez sur **Ajouter un mot de passe d'application**.",
                "5. Copiez le mot de passe généré à 16 caractères (ex: `xxxx xxxx xxxx xxxx`).",
                "6. Renseignez l'URL de votre blog, votre identifiant et ce mot de passe dans l'onglet **Comptes** de notre application."
            ]
        },
        "lm_studio": {
            "title": "LM Studio - IA Locale Gratuite & Confidentielle",
            "icon": "🤖",
            "official_url": "https://lmstudio.ai/",
            "summary": "LM Studio vous permet de faire tourner des modèles de langage locaux (LLM) sur votre PC Windows 11.",
            "steps": [
                "1. Téléchargez et installez LM Studio depuis `https://lmstudio.ai/`.",
                "2. Lancez LM Studio et cherchez un modèle recommandé (ex: `Mistral-7B-Instruct`, `Llama-3-8B-Instruct` ou `Qwen2.5-7B`).",
                "3. Téléchargez le modèle de votre choix.",
                "4. Allez dans l'onglet **<-> Local Server** (serveur local) dans la barre latérale gauche de LM Studio.",
                "5. Sélectionnez votre modèle en haut et cliquez sur **Start Server** (Port par défaut: 1234).",
                "6. Dans notre application, vérifiez que l'URL est `http://localhost:1234/v1` et cliquez sur **Tester la connexion**."
            ]
        },
        "facebook": {
            "title": "Facebook Page API (Meta for Developers)",
            "icon": "📘",
            "official_url": "https://developers.facebook.com/",
            "summary": "Pour publier automatiquement sur vos Pages Facebook professionnelles.",
            "steps": [
                "1. Rendez-vous sur le portail [Meta for Developers](https://developers.facebook.com/) et connectez-vous.",
                "2. Cliquez sur **Mes applications** ➡️ **Créer une application**.",
                "3. Choisissez le type **Business / Entreprise**.",
                "4. Ajoutez le produit **Graph API Explorer** ou **Page API**.",
                "5. Obtenez un **Page Access Token** avec les autorisations `pages_manage_posts` et `pages_read_engagement`.",
                "6. Copiez l'ID de la Page et le Token d'accès dans l'onglet **Comptes** de l'application."
            ]
        },
        "instagram": {
            "title": "Instagram Content Publishing API",
            "icon": "📸",
            "official_url": "https://developers.facebook.com/docs/instagram-api/guides/content-publishing",
            "summary": "Nécessite un compte Instagram Professionnel ou Créateur relié à une Page Facebook.",
            "steps": [
                "1. Convertissez votre compte Instagram en **Compte Professionnel**.",
                "2. Reliez votre compte Instagram à votre **Page Facebook**.",
                "3. Dans [Meta for Developers](https://developers.facebook.com/), ajoutez le produit **Instagram Graph API**.",
                "4. Demandez l'autorisation `instagram_basic` et `instagram_content_publish`.",
                "5. Récupérez votre `Instagram Account ID` et le jeton d'accès correspondant."
            ]
        },
        "twitter": {
            "title": "Twitter / X API v2 Portal",
            "icon": "🐦",
            "official_url": "https://developer.x.com/",
            "summary": "Pour poster des Tweets de manière automatisée.",
            "steps": [
                "1. Connectez-vous sur [X Developer Portal](https://developer.x.com/).",
                "2. Créez un **Projet** et une **Application**.",
                "3. Dans les paramètres de l'application (**User authentication settings**), activez **Read and Write** (Lecture et Écriture).",
                "4. Dans l'onglet **Keys and Tokens**, générez l'**API Key**, l'**API Key Secret**, le **User Access Token** et l'**Access Token Secret**.",
                "5. Renseignez ces 4 clés dans les paramètres de notre application."
            ]
        },
        "linkedin": {
            "title": "LinkedIn Community Management API",
            "icon": "💼",
            "official_url": "https://developer.linkedin.com/",
            "summary": "Pour publier des posts sur votre profil personnel ou votre page entreprise LinkedIn.",
            "steps": [
                "1. Rendez-vous sur [LinkedIn Developers Portal](https://www.linkedin.com/developers/).",
                "2. Cliquez sur **Create App** (Créez une application) et associez votre page LinkedIn.",
                "3. Dans l'onglet **Products**, faites la demande pour **Share on LinkedIn** et **Sign In with LinkedIn**.",
                "4. Dans l'onglet **Auth**, récupérez votre **Client ID** et **Client Secret**.",
                "5. Générez un OAuth 2.0 Access Token avec le scope `w_member_social` (pour profil) ou `w_organization_social` (pour page)."
            ]
        }
    }

    @classmethod
    def get_guide(cls, platform_key):
        return cls.GUIDES.get(platform_key.lower())

    @classmethod
    def get_all_guides(cls):
        return cls.GUIDES
