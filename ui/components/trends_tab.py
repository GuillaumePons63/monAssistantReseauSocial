import customtkinter as ctk
from tkinter import messagebox
from ui.theme import Theme
import webbrowser

class TrendsTab(ctk.CTkFrame):
    def __init__(self, parent, trend_watcher, config_mgr, on_use_topic_cb=None):
        super().__init__(parent, fg_color="transparent")
        self.trend_watcher = trend_watcher
        self.config_mgr = config_mgr
        self.on_use_topic_cb = on_use_topic_cb
        self._build_ui()

    def _build_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # En-tête
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 10))

        lbl_title = ctk.CTkLabel(header_frame, text="🔥 Veille & Détection des Sujets en Tendance (US 1.5)", font=Theme.FONT_TITLE, text_color=Theme.TEXT_MAIN)
        lbl_title.pack(side="left")

        btn_refresh = ctk.CTkButton(header_frame, text="🔄 Actualiser les Tendances", fg_color=Theme.ACCENT_INDIGO, hover_color="#4F46E5", command=self._refresh_trends)
        btn_refresh.pack(side="right")

        # Conteneur principal 2 colonnes (Gauche: Mots-clés de veille, Droite: Flux d'actualités chaudes)
        main_content = ctk.CTkFrame(self, fg_color="transparent")
        main_content.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        main_content.grid_columnconfigure(1, weight=3)
        main_content.grid_columnconfigure(0, weight=1)
        main_content.grid_rowconfigure(0, weight=1)

        # --- PANNEAU GAUCHE : PARAMÈTRES DE VEILLE (Mots-clés & Flux RSS) ---
        left_box = ctk.CTkScrollableFrame(main_content, fg_color=Theme.CARD_BG, corner_radius=12)
        left_box.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Section 1 : Mots-clés
        lbl_kw = ctk.CTkLabel(left_box, text="⚙️ Mots-Clés (Google News)", font=Theme.FONT_SUBTITLE, text_color=Theme.TEXT_MAIN, anchor="w")
        lbl_kw.pack(fill="x", padx=10, pady=(10, 5))

        self.entry_add_kw = ctk.CTkEntry(left_box, font=Theme.FONT_BODY, placeholder_text="Ex: Web3, Élevage...")
        self.entry_add_kw.pack(fill="x", padx=10, pady=4)

        btn_add = ctk.CTkButton(left_box, text="➕ Ajouter Mot-Clé", fg_color="#334155", hover_color="#475569", command=self._add_keyword)
        btn_add.pack(fill="x", padx=10, pady=4)

        self.kw_scroll_box = ctk.CTkFrame(left_box, fg_color="transparent")
        self.kw_scroll_box.pack(fill="x", padx=10, pady=4)

        # Section 2 : Flux RSS Personnalisés
        lbl_rss = ctk.CTkLabel(left_box, text="📡 Flux RSS Personnalisés", font=Theme.FONT_SUBTITLE, text_color=Theme.TEXT_MAIN, anchor="w")
        lbl_rss.pack(fill="x", padx=10, pady=(15, 5))

        self.entry_add_rss = ctk.CTkEntry(left_box, font=Theme.FONT_BODY, placeholder_text="https://site.com/feed/")
        self.entry_add_rss.pack(fill="x", padx=10, pady=4)

        btn_add_rss = ctk.CTkButton(left_box, text="➕ Ajouter Flux RSS", fg_color="#334155", hover_color="#475569", command=self._add_rss_feed)
        btn_add_rss.pack(fill="x", padx=10, pady=4)

        self.rss_scroll_box = ctk.CTkFrame(left_box, fg_color="transparent")
        self.rss_scroll_box.pack(fill="x", padx=10, pady=4)

        self._render_keyword_chips()
        self._render_rss_chips()

        # --- PANNEAU DROIT : LISTE DES SUJETS CHAUDS ---
        right_box = ctk.CTkFrame(main_content, fg_color=Theme.CARD_BG, corner_radius=12)
        right_box.grid(row=0, column=1, sticky="nsew")
        right_box.grid_rowconfigure(1, weight=1)
        right_box.grid_columnconfigure(0, weight=1)

        lbl_feed_t = ctk.CTkLabel(right_box, text="📰 Actualités & Tendances Détectées", font=Theme.FONT_SUBTITLE, text_color=Theme.TEXT_MAIN, anchor="w")
        lbl_feed_t.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 10))

        self.trends_scroll = ctk.CTkScrollableFrame(right_box, fg_color="transparent")
        self.trends_scroll.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        self.trends_scroll.grid_columnconfigure(0, weight=1)

        # Charger les tendances initiales
        self._refresh_trends()

    def _render_keyword_chips(self):
        for widget in self.kw_scroll_box.winfo_children():
            widget.destroy()

        keywords = self.config_mgr.get("trend_watcher", "keywords", [])
        for kw in keywords:
            chip_frame = ctk.CTkFrame(self.kw_scroll_box, fg_color="#334155", corner_radius=6)
            chip_frame.pack(fill="x", pady=2)
            
            lbl_kw_name = ctk.CTkLabel(chip_frame, text=kw, font=Theme.FONT_BODY, text_color=Theme.TEXT_MAIN)
            lbl_kw_name.pack(side="left", padx=8)

            btn_del = ctk.CTkButton(chip_frame, text="❌", width=25, height=25, fg_color="transparent", hover_color="#EF4444", command=lambda k=kw: self._remove_keyword(k))
            btn_del.pack(side="right", padx=4)

    def _render_rss_chips(self):
        for widget in self.rss_scroll_box.winfo_children():
            widget.destroy()

        rss_feeds = self.config_mgr.get("trend_watcher", "rss_feeds", [])
        for feed in rss_feeds:
            chip_frame = ctk.CTkFrame(self.rss_scroll_box, fg_color="#334155", corner_radius=6)
            chip_frame.pack(fill="x", pady=2)
            
            # Afficher un nom court
            short_name = feed.replace("https://", "").replace("http://", "").replace("www.", "")[:25] + "..."
            lbl_feed_name = ctk.CTkLabel(chip_frame, text=short_name, font=Theme.FONT_MUTED, text_color=Theme.TEXT_MAIN)
            lbl_feed_name.pack(side="left", padx=8)

            btn_del = ctk.CTkButton(chip_frame, text="❌", width=25, height=25, fg_color="transparent", hover_color="#EF4444", command=lambda f=feed: self._remove_rss_feed(f))
            btn_del.pack(side="right", padx=4)

    def _add_keyword(self):
        new_kw = self.entry_add_kw.get().strip()
        if not new_kw:
            return
        keywords = self.config_mgr.get("trend_watcher", "keywords", [])
        if new_kw not in keywords:
            keywords.append(new_kw)
            self.config_mgr.set("trend_watcher", "keywords", keywords)
            self.trend_watcher.keywords = keywords
            self.entry_add_kw.delete(0, "end")
            self._render_keyword_chips()
            self._refresh_trends()

    def _remove_keyword(self, kw):
        keywords = self.config_mgr.get("trend_watcher", "keywords", [])
        if kw in keywords:
            keywords.remove(kw)
            self.config_mgr.set("trend_watcher", "keywords", keywords)
            self.trend_watcher.keywords = keywords
            self._render_keyword_chips()

    def _add_rss_feed(self):
        new_rss = self.entry_add_rss.get().strip()
        if not new_rss:
            return
        if not (new_rss.startswith("http://") or new_rss.startswith("https://")):
            messagebox.showwarning("URL Invalide", "L'URL doit commencer par http:// ou https://")
            return
        rss_feeds = self.config_mgr.get("trend_watcher", "rss_feeds", [])
        if new_rss not in rss_feeds:
            rss_feeds.append(new_rss)
            self.config_mgr.set("trend_watcher", "rss_feeds", rss_feeds)
            self.trend_watcher.custom_rss_feeds = rss_feeds
            self.entry_add_rss.delete(0, "end")
            self._render_rss_chips()
            self._refresh_trends()

    def _remove_rss_feed(self, feed):
        rss_feeds = self.config_mgr.get("trend_watcher", "rss_feeds", [])
        if feed in rss_feeds:
            rss_feeds.remove(feed)
            self.config_mgr.set("trend_watcher", "rss_feeds", rss_feeds)
            self.trend_watcher.custom_rss_feeds = rss_feeds
            self._render_rss_chips()

    def _refresh_trends(self):
        for w in self.trends_scroll.winfo_children():
            w.destroy()

        loading_lbl = ctk.CTkLabel(self.trends_scroll, text="Recherche des tendances en cours...", font=Theme.FONT_BODY, text_color=Theme.TEXT_MUTED)
        loading_lbl.pack(pady=20)
        self.update_idletasks()

        items = self.trend_watcher.get_combined_trends()

        loading_lbl.destroy()

        if not items:
            empty_lbl = ctk.CTkLabel(self.trends_scroll, text="Aucun sujet trouvé pour ces mots-clés.", font=Theme.FONT_BODY, text_color=Theme.TEXT_MUTED)
            empty_lbl.pack(pady=20)
            return

        for item in items:
            card = ctk.CTkFrame(self.trends_scroll, fg_color="#0F172A", corner_radius=8, border_color=Theme.BORDER_COLOR, border_width=1)
            card.pack(fill="x", pady=6)
            card.grid_columnconfigure(0, weight=1)

            title_lbl = ctk.CTkLabel(card, text=f"🔥 {item['title']}", font=(Theme.FONT_FAMILY, 13, "bold"), text_color=Theme.TEXT_MAIN, anchor="w", justify="left", wraplength=550)
            title_lbl.pack(fill="x", padx=12, pady=(10, 4))

            meta_lbl = ctk.CTkLabel(card, text=f"Source: {item['source']} • {item['date']}", font=Theme.FONT_MUTED, text_color=Theme.TEXT_MUTED, anchor="w")
            meta_lbl.pack(fill="x", padx=12, pady=(0, 6))

            if item.get("snippet"):
                snippet_lbl = ctk.CTkLabel(card, text=item["snippet"], font=Theme.FONT_BODY, text_color="#CBD5E1", anchor="w", justify="left", wraplength=550)
                snippet_lbl.pack(fill="x", padx=12, pady=(0, 10))

            actions_frame = ctk.CTkFrame(card, fg_color="transparent")
            actions_frame.pack(fill="x", padx=12, pady=(0, 10))

            btn_use = ctk.CTkButton(
                actions_frame,
                text="📝 Utiliser comme sujet dans l'Éditeur",
                font=Theme.FONT_MUTED,
                fg_color=Theme.ACCENT_INDIGO,
                hover_color="#4F46E5",
                height=28,
                command=lambda it=item: self._use_topic_in_editor(it)
            )
            btn_use.pack(side="left")

            if item.get("link"):
                btn_link = ctk.CTkButton(
                    actions_frame,
                    text="🔗 Ouvrir la source",
                    font=Theme.FONT_MUTED,
                    fg_color="#334155",
                    hover_color="#475569",
                    height=28,
                    command=lambda l=item["link"]: webbrowser.open(l)
                )
                btn_link.pack(side="right")

    def _use_topic_in_editor(self, item):
        topic_text = f"Sujet d'actualité : {item['title']}\n\nContexte / Résumé : {item.get('snippet', '')}"
        if self.on_use_topic_cb:
            self.on_use_topic_cb(topic_text)
            messagebox.showinfo("Sujet transféré", "Le sujet a été injecté dans l'Éditeur Direct !")
