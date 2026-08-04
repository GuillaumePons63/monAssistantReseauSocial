import requests
import xml.etree.ElementTree as ET
import urllib.parse
from html import unescape
import re

class TrendWatcher:
    def __init__(self, keywords=None, custom_rss_feeds=None):
        self.keywords = keywords or ["Intelligence Artificielle", "Réseaux Sociaux", "Marketing Digital", "Innovation"]
        self.custom_rss_feeds = custom_rss_feeds or []

    def fetch_google_news_trends(self, topic=None):
        """Récupère les sujets d'actualités chauds via le flux RSS Google News FR."""
        search_query = topic or " ".join(self.keywords[:2])
        encoded_query = urllib.parse.quote(search_query)
        url = f"https://news.google.com/rss/search?q={encoded_query}&hl=fr&gl=FR&ceid=FR:fr"
        
        try:
            resp = requests.get(url, timeout=6)
            if resp.status_code == 200:
                return self._parse_rss_xml(resp.text, source_name="Google News")
            return []
        except Exception as e:
            print(f"[TrendWatcher] Erreur flux Google News: {e}")
            return []

    def fetch_rss_feed(self, rss_url, source_name="RSS Feed"):
        """Lit un flux RSS personnalisé."""
        try:
            resp = requests.get(rss_url, timeout=6)
            if resp.status_code == 200:
                return self._parse_rss_xml(resp.text, source_name=source_name)
            return []
        except Exception as e:
            print(f"[TrendWatcher] Erreur lecture flux {rss_url}: {e}")
            return []

    def _clean_html(self, raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return unescape(cleantext).strip()

    def _parse_rss_xml(self, xml_content, source_name="RSS"):
        items = []
        try:
            root = ET.fromstring(xml_content)
            # Accepter à la fois les structures RSS 2.0 (channel/item) et Atom (entry)
            channel = root.find("channel")
            if channel is not None:
                for elem in channel.findall("item")[:15]:
                    title = elem.findtext("title", default="Sans titre")
                    link = elem.findtext("link", default="")
                    pub_date = elem.findtext("pubDate", default="")
                    desc = elem.findtext("description", default="")
                    
                    items.append({
                        "title": self._clean_html(title),
                        "link": link,
                        "date": pub_date,
                        "snippet": self._clean_html(desc)[:200] + "...",
                        "source": source_name
                    })
        except Exception as e:
            print(f"[TrendWatcher] Erreur parsing XML: {e}")
        return items

    def get_combined_trends(self, active_keyword=None):
        """Combine les résultats de recherche de tendances Google News et des flux configurés."""
        trends = []
        if active_keyword:
            trends.extend(self.fetch_google_news_trends(active_keyword))
        else:
            for kw in self.keywords[:3]:
                trends.extend(self.fetch_google_news_trends(kw))

        for feed_url in self.custom_rss_feeds:
            trends.extend(self.fetch_rss_feed(feed_url, source_name="Flux Perso"))

        # Dédupliquer par titre
        unique_trends = []
        seen_titles = set()
        for item in trends:
            t = item["title"].lower()
            if t not in seen_titles:
                seen_titles.add(t)
                unique_trends.append(item)

        return unique_trends[:25]
