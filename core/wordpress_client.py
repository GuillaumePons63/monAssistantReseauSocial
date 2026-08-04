import requests
from requests.auth import HTTPBasicAuth
import os
import mimetypes

class WordPressClient:
    def __init__(self, site_url, username, application_password):
        self.site_url = site_url.rstrip("/") if site_url else ""
        self.username = username
        self.application_password = application_password

    def is_configured(self):
        return bool(self.site_url and self.username and self.application_password)

    def _get_auth(self):
        return HTTPBasicAuth(self.username, self.application_password)

    def verify_connection(self):
        """Vérifie l'accès à l'API REST WordPress et l'authentification."""
        if not self.is_configured():
            return {"success": False, "message": "Identifiants WordPress non configurés."}

        url = f"{self.site_url}/wp-json/wp/v2/users/me"
        try:
            resp = requests.get(url, auth=self._get_auth(), timeout=8)
            if resp.status_code == 200:
                user_data = resp.json()
                name = user_data.get("name", self.username)
                return {"success": True, "message": f"Connecté à WordPress en tant que '{name}'"}
            elif resp.status_code in (401, 403):
                return {"success": False, "message": "Échec d'authentification WordPress (Mot de passe d'application invalide)."}
            else:
                return {"success": False, "message": f"Erreur WordPress HTTP {resp.status_code}: {resp.text[:150]}"}
        except Exception as e:
            return {"success": False, "message": f"Impossible de contacter WordPress: {str(e)}"}

    def publish_post(self, title, content, status="draft", featured_media_id=None, categories=None, tags=None):
        """Créer un article sur WordPress (US 4.1, US 4.2)."""
        if not self.is_configured():
            return {"success": False, "message": "Identifiants WordPress manquants dans la configuration."}

        url = f"{self.site_url}/wp-json/wp/v2/posts"
        
        payload = {
            "title": title,
            "content": content,
            "status": status  # 'draft', 'publish', 'future' (scheduled)
        }

        if featured_media_id:
            payload["featured_media"] = featured_media_id
        if categories:
            payload["categories"] = categories
        if tags:
            payload["tags"] = tags

        try:
            resp = requests.post(url, json=payload, auth=self._get_auth(), timeout=15)
            if resp.status_code in (200, 201):
                post_data = resp.json()
                return {
                    "success": True,
                    "post_id": post_data.get("id"),
                    "link": post_data.get("link"),
                    "status": post_data.get("status"),
                    "message": f"Article WordPress créé avec succès ({post_data.get('status')}) !"
                }
            else:
                return {"success": False, "message": f"Erreur création article (HTTP {resp.status_code}): {resp.text}"}
        except Exception as e:
            return {"success": False, "message": f"Erreur lors de la publication WordPress: {str(e)}"}

    def upload_media(self, file_path):
        """Envoie une image vers la médiathèque WordPress."""
        if not os.path.exists(file_path):
            return {"success": False, "message": f"Fichier média introuvable: {file_path}"}

        url = f"{self.site_url}/wp-json/wp/v2/media"
        filename = os.path.basename(file_path)
        mime_type, _ = mimetypes.guess_type(file_path)
        mime_type = mime_type or "application/octet-stream"

        headers = {
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Type": mime_type
        }

        try:
            with open(file_path, "rb") as f:
                media_bytes = f.read()

            resp = requests.post(url, data=media_bytes, headers=headers, auth=self._get_auth(), timeout=30)
            if resp.status_code in (200, 201):
                data = resp.json()
                return {
                    "success": True,
                    "media_id": data.get("id"),
                    "source_url": data.get("source_url"),
                    "message": "Média téléversé avec succès sur WordPress."
                }
            else:
                return {"success": False, "message": f"Erreur téléversement média (HTTP {resp.status_code}): {resp.text}"}
        except Exception as e:
            return {"success": False, "message": f"Erreur d'envoi du média: {str(e)}"}

    def get_recent_posts(self, per_page=10):
        """Récupère les derniers articles du blog (US 5.2 Recyclage)."""
        if not self.is_configured():
            return {"success": False, "posts": []}

        url = f"{self.site_url}/wp-json/wp/v2/posts?per_page={per_page}&status=publish,draft"
        try:
            resp = requests.get(url, auth=self._get_auth(), timeout=10)
            if resp.status_code == 200:
                posts = resp.json()
                formatted = []
                for p in posts:
                    formatted.append({
                        "id": p.get("id"),
                        "title": p.get("title", {}).get("rendered", ""),
                        "content": p.get("content", {}).get("rendered", ""),
                        "status": p.get("status"),
                        "link": p.get("link"),
                        "date": p.get("date")
                    })
                return {"success": True, "posts": formatted}
            return {"success": False, "posts": [], "message": f"HTTP {resp.status_code}"}
        except Exception as e:
            return {"success": False, "posts": [], "message": str(e)}
