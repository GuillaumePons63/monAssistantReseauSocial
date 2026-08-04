import requests
import json

class LMStudioClient:
    def __init__(self, base_url="http://localhost:1234/v1"):
        self.base_url = base_url.rstrip("/")

    def check_connection(self):
        """Vérifie si le serveur LM Studio est accessible et retourne le premier modèle ou la liste des modèles."""
        try:
            url = f"{self.base_url}/models"
            resp = requests.get(url, timeout=3)
            if resp.status_code == 200:
                data = resp.json()
                models = [m.get("id") for m in data.get("data", [])]
                return {
                    "connected": True,
                    "models": models,
                    "message": f"LM Studio connecté. Modèles disponibles: {len(models)}"
                }
            return {
                "connected": False,
                "models": [],
                "message": f"Serveur accessible mais code retour {resp.status_code}"
            }
        except requests.exceptions.RequestException as e:
            return {
                "connected": False,
                "models": [],
                "message": f"LM Studio non joignable ({e})"
            }

    def generate(self, prompt, system_prompt=None, model=None, temperature=0.7, max_tokens=1000):
        """Exécute une requête Chat Completion auprès de LM Studio."""
        url = f"{self.base_url}/chat/completions"
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        # Si aucun modèle spécifié, essayer d'en récupérer un
        if not model:
            conn_info = self.check_connection()
            if conn_info["connected"] and conn_info["models"]:
                model = conn_info["models"][0]
            else:
                model = "local-model"

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        try:
            resp = requests.post(url, json=payload, timeout=60)
            if resp.status_code == 200:
                result = resp.json()
                content = result["choices"][0]["message"]["content"]
                return {"success": True, "text": content.strip()}
            else:
                return {"success": False, "error": f"Erreur API ({resp.status_code}): {resp.text}"}
        except Exception as e:
            return {"success": False, "error": f"Erreur de génération avec LM Studio: {str(e)}"}

    def adapt_for_platform(self, base_text, platform, model=None):
        """US 1.2: Adapte un texte de base pour une plateforme spécifique."""
        prompts = {
            "wordpress": (
                "Tu es un rédacteur web professionnel. À partir du sujet ou texte suivant, génère un article de blog WordPress complet "
                "au format Markdown avec un Titre percutant au début (ligne 1: '# Titre'), une introduction, des sous-titres (##) et une conclusion.",
                "Rédige un article WordPress complet basant sur ce texte:\n\n"
            ),
            "facebook": (
                "Tu es un expert réseaux sociaux. Adapte ce texte pour un post Facebook engageant, avec un ton convivial, "
                "des sauts de ligne aérés et quelques émojis pertinents.",
                "Adapte pour Facebook:\n\n"
            ),
            "instagram": (
                "Tu es un créateur de contenu Instagram. Adapte ce texte sous forme de légende (caption) Instagram captivante. "
                "Inclus du storytelling, un appel à l'action (CTA) clair et une liste de 5 à 10 hashtags à la fin.",
                "Adapte pour Instagram:\n\n"
            ),
            "twitter": (
                "Tu es un community manager Twitter/X. Rédige un tweet percutant de moins de 260 caractères basés sur le texte fourni. "
                "Inclus 1 ou 2 hashtags clés.",
                "Adapte pour Twitter (max 260 caractères):\n\n"
            ),
            "linkedin": (
                "Tu es un rédacteur LinkedIn professionnel. Rédige un post LinkedIn orienté valeur ajoutée, "
                "avec une accroche forte, des puces de synthèse et une question pour susciter l'engagement en commentaire.",
                "Adapte pour LinkedIn:\n\n"
            )
        }

        system_p, user_prefix = prompts.get(platform.lower(), (
            "Adapte ce texte pour un réseau social.",
            "Adapte ce contenu:\n\n"
        ))

        return self.generate(user_prefix + base_text, system_prompt=system_p, model=model)

    def rewrite_action(self, text, action_type, model=None):
        """US 1.3: Réécrit un texte selon une action spécifique."""
        actions = {
            "tone_pro": "Réécris ce texte dans un ton hautement professionnel et formel.",
            "tone_fun": "Réécris ce texte avec un ton enthousiaste, dynamique et amical.",
            "shorten": "Raccourcis et simplifie ce texte pour aller droit à l'essentiel.",
            "correct": "Corrige l'orthographe, la grammaire et la ponctuation de ce texte sans en changer le sens.",
            "emojis": "Enrichis ce texte en y ajoutant des émojis pertinents pour animer le message."
        }
        
        system_p = actions.get(action_type, "Réécris et améliore ce texte.")
        return self.generate(f"Texte d'origine:\n{text}", system_prompt=system_p, model=model)

    def extract_hashtags(self, text, model=None):
        """US 1.4: Extrait des hashtags pertinents."""
        system_p = "Propose une liste de 8 à 15 hashtags pertinents séparés par des espaces, basés sur le texte fourni."
        return self.generate(f"Génère uniquement les hashtags pour ce texte:\n{text}", system_prompt=system_p, model=model)
