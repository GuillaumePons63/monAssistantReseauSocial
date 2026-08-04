import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import ConfigManager
from core.lm_studio_client import LMStudioClient
from core.wordpress_client import WordPressClient
from core.trend_watcher import TrendWatcher
from core.api_docs_guide import APIDocsGuide

def test_config():
    cm = ConfigManager()
    assert cm.get("lm_studio", "url") == "http://localhost:1234/v1"
    print("✅ Test Config OK")

def test_lm_studio_offline():
    client = LMStudioClient("http://localhost:1234/v1")
    conn = client.check_connection()
    print(f"✅ Connection test check executed (Connected: {conn['connected']}, Message: {conn['message']})")

def test_wordpress_init():
    wp = WordPressClient("https://example.com", "user", "pass")
    assert wp.is_configured() == True
    print("✅ Test WordPress client init OK")

def test_trend_watcher():
    tw = TrendWatcher(keywords=["IA", "Technologie"])
    trends = tw.get_combined_trends()
    print(f"✅ Test Trend Watcher OK ({len(trends)} articles de tendances récupérés)")

def test_api_docs_guide():
    guides = APIDocsGuide.get_all_guides()
    assert "wordpress" in guides
    assert "facebook" in guides
    assert "lm_studio" in guides
    print("✅ Test API Docs Guide OK")

if __name__ == "__main__":
    test_config()
    test_lm_studio_offline()
    test_wordpress_init()
    test_trend_watcher()
    test_api_docs_guide()
    print("🎉 TOUS LES TESTS UNITAIRES DES MODULES BACKEND ONT RÉUSSI !")
