import sys
import os

# S'assurer que le répertoire courant est dans sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import ConfigManager
from core.lm_studio_client import LMStudioClient
from core.wordpress_client import WordPressClient
from core.trend_watcher import TrendWatcher
from ui.app import MainApp

def main():
    print("=" * 60)
    print("🚀 Lancement d'Assistant Publications Réseaux & Blog WordPress")
    print("   IA Locale : LM Studio (http://localhost:1234)")
    print("   OS Target : Windows 11")
    print("=" * 60)

    # 1. Chargement de la configuration
    config_mgr = ConfigManager()

    # 2. Instanciation des services backend
    lm_cfg = config_mgr.get("lm_studio")
    lm_client = LMStudioClient(base_url=lm_cfg.get("url", "http://localhost:1234/v1"))

    wp_cfg = config_mgr.get("wordpress")
    wp_client = WordPressClient(
        site_url=wp_cfg.get("url", ""),
        username=wp_cfg.get("username", ""),
        application_password=wp_cfg.get("application_password", "")
    )

    trend_cfg = config_mgr.get("trend_watcher")
    trend_watcher = TrendWatcher(
        keywords=trend_cfg.get("keywords"),
        custom_rss_feeds=trend_cfg.get("rss_feeds")
    )

    # 3. Lancement de l'interface GUI Windows 11
    app = MainApp(config_mgr, lm_client, wp_client, trend_watcher)
    app.mainloop()

if __name__ == "__main__":
    main()
