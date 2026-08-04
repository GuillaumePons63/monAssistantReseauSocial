import customtkinter as ctk
from tkinter import messagebox
from ui.theme import Theme

class AccountsTab(ctk.CTkFrame):
    def __init__(self, parent, wp_client, config_mgr, on_import_post_cb=None):
        super().__init__(parent, fg_color="transparent")
        self.wp_client = wp_client
        self.config_mgr = config_mgr
        self.on_import_post_cb = on_import_post_cb
        self._build_ui()
        self._load_current_config()

    def _build_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # En-tête
        lbl_title = ctk.CTkLabel(self, text="⚙️ Comptes, Accès API & Historique WordPress", font=Theme.FONT_TITLE, text_color=Theme.TEXT_MAIN, anchor="w")
        lbl_title.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 10))

        # Zone principale scrollable
        scroll_box = ctk.CTkScrollableFrame(self, fg_color=Theme.CARD_BG, corner_radius=12)
        scroll_box.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        scroll_box.grid_columnconfigure(0, weight=1)

        # --- SECTION 1 : CONFIGURATION WORDPRESS (PRIORITÉ N°1) ---
        lbl_wp_s = ctk.CTkLabel(scroll_box, text="🌐 Connexion au Blog WordPress (Priorité n°1)", font=Theme.FONT_SUBTITLE, text_color=Theme.TEXT_MAIN, anchor="w")
        lbl_wp_s.pack(fill="x", padx=15, pady=(15, 5))

        wp_form = ctk.CTkFrame(scroll_box, fg_color="#0F172A", corner_radius=10, border_color=Theme.BORDER_COLOR, border_width=1)
        wp_form.pack(fill="x", padx=15, pady=5)
        wp_form.grid_columnconfigure(1, weight=1)

        # URL Site
        ctk.CTkLabel(wp_form, text="URL du Blog WordPress :", font=Theme.FONT_BODY, anchor="w").grid(row=0, column=0, padx=15, pady=8, sticky="w")
        self.entry_wp_url = ctk.CTkEntry(wp_form, font=Theme.FONT_BODY, placeholder_text="https://mon-blog-wordpress.com")
        self.entry_wp_url.grid(row=0, column=1, padx=15, pady=8, sticky="ew")

        # Identifiant
        ctk.CTkLabel(wp_form, text="Identifiant / Nom d'utilisateur :", font=Theme.FONT_BODY, anchor="w").grid(row=1, column=0, padx=15, pady=8, sticky="w")
        self.entry_wp_user = ctk.CTkEntry(wp_form, font=Theme.FONT_BODY, placeholder_text="admin")
        self.entry_wp_user.grid(row=1, column=1, padx=15, pady=8, sticky="ew")

        # Mot de passe d'application
        ctk.CTkLabel(wp_form, text="Mot de passe d'application :", font=Theme.FONT_BODY, anchor="w").grid(row=2, column=0, padx=15, pady=8, sticky="w")
        self.entry_wp_pass = ctk.CTkEntry(wp_form, font=Theme.FONT_BODY, show="•", placeholder_text="xxxx xxxx xxxx xxxx")
        self.entry_wp_pass.grid(row=2, column=1, padx=15, pady=8, sticky="ew")

        # Boutons Action WP
        btn_wp_actions = ctk.CTkFrame(wp_form, fg_color="transparent")
        btn_wp_actions.grid(row=3, column=0, columnspan=2, padx=15, pady=(5, 12), sticky="ew")

        btn_test_wp = ctk.CTkButton(btn_wp_actions, text="🔌 Tester Connexion WP", fg_color=Theme.ACCENT_INDIGO, hover_color="#4F46E5", command=self._test_wp_connection)
        btn_test_wp.pack(side="left", padx=(0, 10))

        btn_save_wp = ctk.CTkButton(btn_wp_actions, text="💾 Sauvegarder Identifiants WP", fg_color=Theme.ACCENT_EMERALD, hover_color="#059669", command=self._save_wp_config)
        btn_save_wp.pack(side="left")

        self.lbl_wp_badge = ctk.CTkLabel(wp_form, text="⚪ Status inconnu", font=Theme.FONT_BODY, text_color=Theme.TEXT_MUTED)
        self.lbl_wp_badge.grid(row=4, column=0, columnspan=2, padx=15, pady=(0, 12), sticky="w")

        # --- SECTION 2 : RECYCLAGE & HISTORIQUE DES ARTICLES WORDPRESS (US 5.2) ---
        ctk.CTkFrame(scroll_box, height=2, fg_color=Theme.BORDER_COLOR).pack(fill="x", padx=15, pady=15)

        h_rec_frame = ctk.CTkFrame(scroll_box, fg_color="transparent")
        h_rec_frame.pack(fill="x", padx=15, pady=(5, 5))

        lbl_rec = ctk.CTkLabel(h_rec_frame, text="♻️ Historique & Recyclage d'Articles WordPress (US 5.2)", font=Theme.FONT_SUBTITLE, text_color=Theme.TEXT_MAIN)
        lbl_rec.pack(side="left")

        btn_fetch_posts = ctk.CTkButton(h_rec_frame, text="🔄 Charger mes articles récents", fg_color="#334155", hover_color="#475569", command=self._load_recent_posts)
        btn_fetch_posts.pack(side="right")

        self.posts_scroll_box = ctk.CTkFrame(scroll_box, fg_color="#0F172A", corner_radius=10, border_color=Theme.BORDER_COLOR, border_width=1)
        self.posts_scroll_box.pack(fill="x", padx=15, pady=5)
        self.posts_scroll_box.grid_columnconfigure(0, weight=1)

        self.lbl_posts_status = ctk.CTkLabel(self.posts_scroll_box, text="Cliquez sur 'Charger mes articles récents' pour afficher votre historique.", font=Theme.FONT_BODY, text_color=Theme.TEXT_MUTED)
        self.lbl_posts_status.pack(pady=20)

    def _load_current_config(self):
        wp_cfg = self.config_mgr.get("wordpress")
        self.entry_wp_url.insert(0, wp_cfg.get("url", ""))
        self.entry_wp_user.insert(0, wp_cfg.get("username", ""))
        self.entry_wp_pass.insert(0, wp_cfg.get("application_password", ""))

    def _save_wp_config(self):
        url = self.entry_wp_url.get().strip()
        user = self.entry_wp_user.get().strip()
        pwd = self.entry_wp_pass.get().strip()

        self.config_mgr.set("wordpress", "url", url)
        self.config_mgr.set("wordpress", "username", user)
        self.config_mgr.set("wordpress", "application_password", pwd)

        self.wp_client.site_url = url.rstrip("/")
        self.wp_client.username = user
        self.wp_client.application_password = pwd

        messagebox.showinfo("Configuration WordPress", "Identifiants WordPress sauvegardés avec succès !")

    def _test_wp_connection(self):
        self._save_wp_config()
        res = self.wp_client.verify_connection()
        if res["success"]:
            self.lbl_wp_badge.configure(text=f"🟢 {res['message']}", text_color=Theme.ACCENT_EMERALD)
        else:
            self.lbl_wp_badge.configure(text=f"🔴 {res['message']}", text_color=Theme.ACCENT_ROSE)

    def _load_recent_posts(self):
        for w in self.posts_scroll_box.winfo_children():
            w.destroy()

        lbl_loading = ctk.CTkLabel(self.posts_scroll_box, text="Récupération des articles en cours...", font=Theme.FONT_BODY, text_color=Theme.TEXT_MUTED)
        lbl_loading.pack(pady=20)
        self.update_idletasks()

        res = self.wp_client.get_recent_posts(per_page=8)
        lbl_loading.destroy()

        if not res["success"] or not res["posts"]:
            lbl_err = ctk.CTkLabel(self.posts_scroll_box, text=f"Aucun article récupéré. ({res.get('message', 'Non connecté')})", font=Theme.FONT_BODY, text_color=Theme.TEXT_MUTED)
            lbl_err.pack(pady=20)
            return

        for p in res["posts"]:
            row = ctk.CTkFrame(self.posts_scroll_box, fg_color="#1E293B", corner_radius=6)
            row.pack(fill="x", padx=10, pady=4)
            row.grid_columnconfigure(0, weight=1)

            title_str = p['title'] or "Sans titre"
            lbl_post = ctk.CTkLabel(row, text=f"📄 {title_str} ({p['status'].upper()})", font=Theme.FONT_BODY, text_color=Theme.TEXT_MAIN, anchor="w")
            lbl_post.pack(side="left", padx=10, pady=8)

            btn_recycle = ctk.CTkButton(
                row,
                text="♻️ Importer pour décliner par IA",
                font=Theme.FONT_MUTED,
                fg_color=Theme.ACCENT_INDIGO,
                hover_color="#4F46E5",
                height=26,
                command=lambda post=p: self._recycle_post(post)
            )
            btn_recycle.pack(side="right", padx=10, pady=8)

    def _recycle_post(self, post):
        if self.on_import_post_cb:
            content_text = f"# {post['title']}\n\n{post['content']}"
            self.on_import_post_cb(content_text)
            messagebox.showinfo("Article importé", f"L'article '{post['title']}' a été chargé dans l'Éditeur Direct !")
